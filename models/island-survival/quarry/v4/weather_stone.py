"""Weather the natural outcrop geometrically, retaining marked fresh cuts and load seats."""
import bpy,bmesh,hashlib,json,math,sys,tempfile
import numpy as np
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;R=H.parents[3];P=R/'models/island-survival/quarry/candidates/v3-geology02';O=R/'models/island-survival/quarry/candidates/v4-weathered01'
if O.exists():raise FileExistsError(O)
O.mkdir(parents=True);tempfile.tempdir=str(R/'build/quarry-export-temp')
sys.path.insert(0,str(R/'models/island-survival/primitive-steam-powered-pump/v3'));import surfaces
sys.path.insert(0,str(R.parent/'model-production/tools/fmpl'));from blender_camera_guard import assert_clean,temporary_inspection_camera
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=P/'quarry-v3.blend';assert sha(source)==json.loads((P/'geology-receipt.json').read_text())['source_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1)
root=bpy.data.objects['EXPORT | Quarry all authored parts'];rock=bpy.data.objects['QUARRY | REUSED quarry_base_stone']
bpy.context.view_layer.objects.active=rock
for mod in list(rock.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
mod=rock.modifiers.new('Close and resolve weathered outcrop surfaces','REMESH');mod.mode='VOXEL';mod.voxel_size=.012;mod.use_smooth_shade=True
bpy.ops.object.modifier_apply(modifier=mod.name)
mod=rock.modifiers.new('Worn fracture transitions','SMOOTH');mod.factor=.45;mod.iterations=3
bpy.ops.object.modifier_apply(modifier=mod.name)
group=rock.vertex_groups.new(name='Natural stone weathering; preserve worked seats')
for v in rock.data.vertices:
 x,y,z=v.co
 fresh=(abs(y-.745)<.018 and .36<z<.74) or (abs(y-.885)<.018 and .70<z<1.14)
 hewn=(abs(z-.88)<.025 and x>.60 and y<.91)
 ground=z<.045
 weight=0 if fresh or hewn or ground else 1 if z>.36 or max(abs(x),abs(y))>1.22 else .10
 group.add([v.index],weight,'REPLACE')
texture=bpy.data.textures.new('Quarry actual weathered cleavage relief',type='CLOUDS');texture.noise_scale=.13;texture.noise_depth=2
mod=rock.modifiers.new('Physical weathering and small fractures','DISPLACE');mod.texture=texture;mod.texture_coords='GLOBAL';mod.strength=.022;mod.mid_level=.5;mod.vertex_group=group.name
bpy.ops.object.modifier_apply(modifier=mod.name)
mod=rock.modifiers.new('Preserve erosion silhouette with practical topology','DECIMATE');mod.ratio=.35
bpy.ops.object.modifier_apply(modifier=mod.name)
for v in rock.data.vertices:
 v.co.x=max(-1.485,min(1.485,v.co.x));v.co.y=max(-1.485,min(1.485,v.co.y))
 if v.co.z<.008:v.co.z=0
for face in rock.data.polygons:face.use_smooth=True
# True physical-scale image normals supplement geometry; they do not fake the silhouette.
rng=np.random.default_rng(171132);size=512;shape=(size,size);u,v=np.meshgrid(np.linspace(0,1,size),np.linspace(0,1,size))
coarse=surfaces.field(rng,shape,.012);mid=surfaces.field(rng,shape,.07);fine=surfaces.field(rng,shape,.27)
nearest=np.full(shape,100.);second=nearest.copy()
for x,y in rng.uniform(0,1,(35,2)):
 d=(u-x)**2+(v-y)**2
 lesser=d<nearest;second=np.where(lesser,nearest,np.minimum(second,d));nearest=np.minimum(nearest,d)
crack=np.exp(-np.maximum(second-nearest,0)/.00075)
calcite=np.clip((coarse-.35)*.6,0,.5)
tone=np.clip(.245+.038*coarse+.017*mid+.009*fine-.035*crack,.11,.43)
color=np.stack([tone*1.04,tone,tone*.94],axis=-1)
color=color*(1-calcite[:,:,None]*.35)+np.array([.47,.46,.42])*calcite[:,:,None]*.35
height=.0012*mid+.00035*fine-.0018*crack+.001*calcite
dy,dx=np.gradient(height)
normal=np.stack([-dx*size/.5,-dy*size/.2,np.ones(shape)],axis=-1);normal/=np.linalg.norm(normal,axis=-1)[:,:,None]
maps={'albedo':surfaces.image('quarry-v4-weathered-rock-albedo',color,O),'roughness':surfaces.image('quarry-v4-weathered-rock-roughness',np.clip(.86+.035*mid+.06*crack,.65,.98),O,True),'normal':surfaces.image('quarry-v4-weathered-rock-normal',normal*.5+.5,O,True)}
material=bpy.data.materials.new('QUARRY V4 | actual weathered limestone imagery');material.use_nodes=True
shader=material.node_tree.nodes.get('Principled BSDF')
for role,im in maps.items():
 node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=im
 if role=='normal':
  n=material.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.65;material.node_tree.links.new(node.outputs['Color'],n.inputs['Color']);material.node_tree.links.new(n.outputs['Normal'],shader.inputs['Normal'])
 else:material.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color' if role=='albedo' else 'Roughness'])
material['surface_authorship']='Physical limestone microfractures, calcite inclusions, roughness and correctly scaled tangent normal maps; geometry defines weathered outlines'
surfaces.apply(rock,material)
# Keep extracted chunks angular but soften damaged corners, not pristine factory cubes.
for name in ('QUARRY | REUSED quarry_quarried_block_b','QUARRY | reused lifted stone'):
 o=bpy.data.objects[name]
 for face in o.data.polygons:face.use_smooth=False
# Clean actual remesh triangles and retain all existing kinematic curves.
bm=bmesh.new();bm.from_mesh(rock.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(rock.data);bm.free()
rock.data.calc_loop_triangles();bad={t.polygon_index for t in rock.data.loop_triangles if t.area<1e-12}
if bad:
 bm=bmesh.new();bm.from_mesh(rock.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES');bm.to_mesh(rock.data);bm.free()
profile=json.loads((P/'capture-profile.json').read_text());assert_clean(scene,profile,bpy);bpy.ops.file.pack_all()
native=O/'quarry-v4.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Quarry all authored parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'quarry-v4.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(O/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
(O/'weathering-receipt.json').write_text(json.dumps({'parent_sha256':sha(source),'source_sha256':sha(native),'runtime_sha256':sha(O/'quarry-v4.glb'),'physical_voxel_scale':.012,'physical_weathering_relief':.022,'native_footprint_tiles':[3,3],'worked_seats_and_kinematics_preserved':True,'owner_visual_approved':False,'native_integrated':False},indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | quarry square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
scene.cycles.samples=48;scene.render.resolution_x=scene.render.resolution_y=512
for name,yaw in [('front',0),('east',270),('rear',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);scene.frame_set(49);scene.render.filepath=str(O/(name+'-review512.png'));bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0
with temporary_inspection_camera(scene,bpy,'quarry winch construction') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=1.45;camera.location=(-2.4,-3.4,3.3);camera.rotation_euler=(Vector((0,.55,1.98))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(O/'winch-close512.png');bpy.ops.render.render(write_still=True)
with temporary_inspection_camera(scene,bpy,'quarry thermal construction') as camera:
 camera.data.type='ORTHO';camera.data.ortho_scale=1.28;camera.location=(3,-3,2.7);camera.rotation_euler=(Vector((1.02,-.42,1.20))-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
 scene.render.filepath=str(O/'thermal-close512.png');bpy.ops.render.render(write_still=True)
print('QUARRY_WEATHERED_GEOMETRY_SOURCE',native,flush=True)
