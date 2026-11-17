"""Root the quarry in one continuous landform; no placed-boulder or plinth silhouette."""
import bpy,bmesh,hashlib,json,math,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/quarry/candidates/v3-geology02';O=R/'models/island-survival/quarry/candidates/v5-rooted02'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box
import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean,temporary_inspection_camera
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'quarry-v3.blend';assert sha(source)==json.loads((P/'geology-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1);root=bpy.data.objects['EXPORT | Quarry all authored parts']
def material(s):return next(m for m in bpy.data.materials if m.name.endswith(' | '+s))
weathered=material('quarry-v2-weathered-strata');cut=material('quarry-v2-fresh-cleavage');soil=material('quarry-v3-rock-dust-and-floor')
fresh=cut;bed=weathered;col=bpy.data.collections.new('QUARRY V5 | continuous rooted landform');scene.collection.children.link(col)
# Machine coordinates remain unchanged relative to one another; the site now meets world ground.
OFFSET_X=-.10;OFFSET_Z=-.42;root.location=(OFFSET_X,0,OFFSET_Z)
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)
poly=[(-1.30,-1.27),(.62,-1.26),(.63,-.20),(.60,.25),(.48,.30),(.45,.83),(-.46,.83),(-.52,.36),(-1.27,.39)]
def inside_distance(x,y):
 inside=np.zeros(np.broadcast(x,y).shape,dtype=bool);distance=np.full_like(x+y,1e6,dtype=float)
 for i,a in enumerate(poly):
  b=poly[(i+1)%len(poly)];ax,ay=a;bx,by=b;dx,dy=bx-ax,by-ay
  inside^=((ay>y)!=(by>y))&(x<dx*(y-ay)/(dy if abs(dy)>1e-12 else 1e-12)+ax)
  t=np.clip(((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy),0,1)
  distance=np.minimum(distance,np.sqrt((x-ax-t*dx)**2+(y-ay-t*dy)**2))
 return inside,distance
def height(x,y):
 wx=x+OFFSET_X
 angle=np.arctan2(y,wx)
 boundary=1-((np.abs(wx)/1.49)**4+(np.abs(y)/1.49)**4)**.25+.018*np.sin(angle*7)+.012*np.sin(angle*11+1.2)
 side=smooth((1.48-np.abs(wx))/.38);back=smooth((1.48-y)/.32);front=smooth((y+1.48)/.30)
 floor_inside,floor_d=inside_distance(x,y)
 floor=.11*floor_inside*smooth(floor_d/.035)
 ridge=(.86+.025*np.sin(x*4.2)+.014*np.sin(x*11.0))*smooth((y-.52)/.42)*side*back
 # The visible bay is hand-cut into this continuous ridge, not assembled from slabs.
 bay=smooth((x+1.10)/.08)*smooth((.70-x)/.08)
 worked=np.where(y<.745,0,np.where(y<.885,np.minimum(ridge,.41),ridge))
 ridge=ridge*(1-bay)+worked*bay
 for px in (-.86,-.62,-.38,-.14,.10,.34,.58):
  kerf=(np.abs(x-px)<.013)&(y>=.745)&(y<.81)
  ridge=np.where(kerf,np.maximum(0,ridge-.22),ridge)
 east=.50*smooth((x-.62)/.23)*smooth((1.48-wx)/.22)*smooth((y+1.30)/.20)*smooth((1.04-y)/.18)
 h=np.maximum(floor,np.maximum(ridge,east))
 # Recessed worked pads support the retained timber thrust feet.
 for px in (-.95,.95):
  seat=(np.abs(x-px)<.17)&(np.abs(y-1.14)<.155)
  h=np.where(seat,np.minimum(h,.785),h)
 natural=(ridge>.10)&(y>.885)&(np.abs(x)<1.25)
 relief=.010*np.sin(x*13+y*4)*np.cos(y*17-x*3)+.004*np.sin(x*31-y*19)
 h+=np.where(natural,relief,0)
 edge=smooth(boundary/.10)
 h=np.maximum(0,h-.10)*smooth(boundary/.17)
 return h,edge,floor,ridge,east
# Dense vertices are allocated at actual cut transitions; the rest is a broad connected slope.
xs=list(np.linspace(-1.38,1.58,89));ys=list(np.linspace(-1.48,1.48,89))
for px in (-.86,-.62,-.38,-.14,.10,.34,.58):xs.extend([px-.014,px-.012,px+.012,px+.014])
ys.extend([.740,.744,.746,.752,.807,.809,.811,.820,.880,.884,.886,.895])
xs=np.array(sorted(set(round(float(v),6) for v in xs)));ys=np.array(sorted(set(round(float(v),6) for v in ys)))
X,Y=np.meshgrid(xs,ys);Z,fade,floors,ridges,easts=height(X,Y)
verts=[(float(x),float(y),float(z-OFFSET_Z)) for x,y,z in zip(X.ravel(),Y.ravel(),Z.ravel())]
nx,ny=len(xs),len(ys);faces=[]
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.append((a,a+1,a+nx+1,a+nx))
data=bpy.data.meshes.new('Continuous excavation surface and buried outcrop roots');data.from_pydata(verts,[],faces);data.update()
terrain=bpy.data.objects['QUARRY | REUSED quarry_base_stone'];terrain.data=data
# Ground fading blends the excavated edge with the actual placed terrain, without a vertical base.
copies=[]
for m in (weathered,cut,soil):
 new=m.copy();new.name='QUARRY V5 | rooted '+m.name.split('|')[-1].strip();new.surface_render_method='DITHERED'
 node=new.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='QuarryGroundFade';shader=new.node_tree.nodes.get('Principled BSDF');new.node_tree.links.new(node.outputs['Alpha'],shader.inputs['Alpha']);copies.append(new);data.materials.append(new)
colors=data.color_attributes.new(name='QuarryGroundFade',type='FLOAT_COLOR',domain='CORNER')
for face in data.polygons:
 cx,cy,cz=face.center;h=cz+OFFSET_Z
 face.material_index=2 if h<.13 else 1 if -.99<cx<.65 and .735<cy<.90 else 0
 face.use_smooth=face.material_index!=1
 for loop_index in face.loop_indices:
  idx=data.loops[loop_index].vertex_index;j,i=divmod(idx,nx)
  alpha=float(fade[j,i]);colors.data[loop_index].color=(1,1,1,alpha)
surfaces.physical_box_uv(terrain)
oldfloor=bpy.data.objects.get('QUARRY | REUSED quarry_excavation_floor')
if oldfloor:bpy.data.objects.remove(oldfloor,do_unlink=True)
# Existing foundation stones remain explicit worked bearing seats, embedded in the terrain.
o=box('QUARRY V5 | outboard pier worked footing',(1.16,.59,.83),(.25,.25,.10),fresh,col,root,.015);surfaces.apply(o,fresh)
# Ground chips are reseated on the continuous surface, not perched on obsolete slabs.
for o in root.children_recursive:
 if 'quarry chips' in o.name:
  x,y=o.location.x,o.location.y;ground=float(height(np.array(x),np.array(y))[0])
  low=min(v.co.z for v in o.data.vertices);o.location.z=ground-OFFSET_Z-low
# Preserve fixed camera/scale; lowered origin puts the site into world terrain.
profile=json.loads((P/'capture-profile.json').read_text());profile['camera_override']['target']=[0,0,.63]
install_canonical_camera(scene,profile,bpy);scene.frame_set(1);assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
native=O/'quarry-v5.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'quarry-v5.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'terrain-receipt.json').write_text(json.dumps({'parent_sha256':sha(source),'source_sha256':sha(native),'runtime_sha256':sha(O/'quarry-v5.glb'),'owner_feedback':'Rock roots read as placed boulders; make them part of terrain','terrain':'One continuous heightfield landform with buried ridge roots, an excavated bay, worked bearing seats and an alpha-faded world-ground boundary','open_ground_boundary':True,'root_translation':[OFFSET_X,0,OFFSET_Z],'native_footprint_tiles':[3,3],'kinematic_relationships_preserved':True,'owner_visual_approved':False,'native_integrated':False},indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | quarry square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(scene,bpy,'quarry detailed winch') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=1.45;camera.location=(-2.4,-3.4,3.0);camera.rotation_euler=(Vector((-.10,.55,1.66))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(O/'winch-close512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(scene,bpy,'quarry detailed thermal drive') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=1.28;camera.location=(3,-3,2.4);camera.rotation_euler=(Vector((.92,-.42,.88))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(O/'thermal-close512.png');bpy.ops.render.render(write_still=True)
print('QUARRY_ROOTED_LANDFORM_SOURCE',native,flush=True)
