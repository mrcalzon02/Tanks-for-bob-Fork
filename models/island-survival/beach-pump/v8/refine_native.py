"""Continue recovered V7: bucket-carried water, timed draining, worn wood.
Authored looping mesh animation; no fluid simulation or game integration.
"""
import bpy, math, json, sys, hashlib
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]);out.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;root=bpy.data.objects['EXPORT | rotate beachpump not camera'];wheel=bpy.data.objects['MOTION | full bucket waterwheel shaft']
root.rotation_euler.z=0;s.frame_set(1);bpy.context.view_layer.update()
ports=[o for o in bpy.data.objects if o.name.startswith('PORT |')]
def port_points():
 bpy.context.view_layer.update();return [tuple(o.matrix_world@v.co) for o in ports for v in o.data.vertices]
baseline_ports=port_points()
# Denser phase inspection found the V7 cheek clipping the gutter between samples.
wheel.location.z-=.025
bpy.data.objects['WHEEL | fixed axle support'].location.z-=.025
for support in bpy.data.objects:
 if support.name.startswith('WHEEL | fixed timber bearing frame'):
  axis=support.rotation_euler.to_matrix()@Vector((0,0,1))
  half=(max(v.co.z for v in support.data.vertices)-min(v.co.z for v in support.data.vertices))*support.scale.z/2
  ends=[support.location-axis*half,support.location+axis*half]
  high=max(range(2),key=lambda i:ends[i].z);ends[high].z-=.025
  d=ends[1]-ends[0];support.location=(ends[0]+ends[1])/2;support.rotation_euler=d.to_track_quat('Z','Y').to_euler();support.scale.z*=d.length/(2*half)
drive=bpy.data.objects['DRIVE | exposed rigid wheel-to-screw gearbox input']
a,b=Vector((.23,-.13,.905)),Vector((-.08,.085,1.36));d=b-a
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.058,depth=d.length)
temp=bpy.context.object;mat=drive.data.materials[0];drive.data=temp.data.copy();drive.data.materials.append(mat);bpy.data.objects.remove(temp,do_unlink=True)
drive.location=(a+b)/2;drive.rotation_euler=d.to_track_quat('Z','Y').to_euler();drive.scale=(1,1,1)
col=wheel.users_collection[0];water=bpy.data.materials['BEACH V6 | clear shallow seawater']
foam=bpy.data.materials['BEACH V7 | aerated splash highlights']
# Replace static runoff with streams whose source moves with each bucket.
for ob in list(bpy.data.objects):
 if ob.name.startswith('WATER | V7 bucket runoff thread'):bpy.data.objects.remove(ob,do_unlink=True)
# Suppress old glints that read as beads laid along the trough.
for ob in list(bpy.data.objects):
 if ob.name.startswith('WATER | running stream glint'):bpy.data.objects.remove(ob,do_unlink=True)

def mesh(name,verts,faces,material,parent):
 m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
 ob=bpy.data.objects.new(name,m);col.objects.link(ob);ob.parent=parent;m.materials.append(material)
 return ob
fills=[];drains=[];records=[]
for k in range(8):
 a=2*math.pi*k/8;cs,sn=math.cos(a),math.sin(a)
 verts=[(0,.312*cs,.312*sn)];faces=[]
 for ring in range(1,5):
  fraction=ring/4
  for j in range(48):
   theta=2*math.pi*j/48
   x=.094*fraction*math.cos(theta);t=.053*fraction*math.sin(theta)
   r=.312+.0012*math.sin(theta*3+k)*fraction+.001*fraction**4
   verts.append((x,r*cs-t*sn,r*sn+t*cs))
 for j in range(48):faces.append((0,1+j,1+(j+1)%48))
 for ring in range(3):
  lo=1+48*ring;hi=lo+48
  for j in range(48):faces.append((lo+j,hi+j,hi+(j+1)%48,lo+(j+1)%48))
 ob=mesh(f'WATER | V8 carried bucket water {k:02d}',verts,faces,water,wheel)
 for poly in ob.data.polygons:poly.use_smooth=True
 # Scale around the pool center instead of moving water through the bucket walls.
 center=Vector((0,.312*cs,.312*sn))
 for v in ob.data.vertices:v.co-=center
 ob.location=center
 sol=ob.modifiers.new('Shallow retained water','SOLIDIFY');sol.thickness=.002
 fills.append(ob)
 curve=bpy.data.curves.new(f'V8 bucket {k} draining ribbon','CURVE');curve.dimensions='3D';curve.bevel_depth=.004;curve.bevel_resolution=3
 spline=curve.splines.new('POLY');spline.points.add(12)
 dr=bpy.data.objects.new(f'WATER | V8 moving bucket drain {k:02d}',curve);col.objects.link(dr);dr.parent=root;curve.materials.append(water);drains.append(dr)
 for fr in range(1,98):
  s.frame_set(fr);bpy.context.view_layer.update()
  angle=(a+wheel.rotation_euler.x)%(2*math.pi)
  # Retain near the top, empty on the descending side before the cup overturns.
  topdistance=abs((angle-math.pi/2+math.pi)%(2*math.pi)-math.pi)
  retained=max(0,1-(topdistance/.92)**4)
  ob.scale=(1,max(.001,retained),max(.001,retained));ob.keyframe_insert('scale',frame=fr)
  strength=max(0,math.sin(math.pi*(angle-.10)/1.10)) if .10<angle<1.20 else 0
  # Start on the front lip of the actual moving bucket; fall into the basin.
  origin=wheel.matrix_world@Vector((-.080,.326*cs-.070*sn,.326*sn+.070*cs))
  velocity=Vector((-.007,.08,-.045))
  for j,p in enumerate(spline.points):
   t=j/12*((-.045+math.sqrt(.045**2+4*1.3*max(.01,origin.z-.555)))/(2*1.3));v=origin+velocity*t+Vector((0,0,-1.30*t*t))
   p.co=(*v,1);p.keyframe_insert('co',frame=fr)
  dr.scale=(1,1,1)
  # Animate radius, preserving the real emitter position rather than scaling it about world zero.
  curve.bevel_depth=.0045*strength;curve.keyframe_insert('bevel_depth',frame=fr)
  for effect in (ob,dr):
   effect.hide_render=(fr==0);effect.keyframe_insert('hide_render',frame=fr)
 for effect in (ob,dr):
  effect.hide_render=True;effect.keyframe_insert('hide_render',frame=0)
  effect.hide_render=False;effect.keyframe_insert('hide_render',frame=1)
 # New per-frame motion should interpolate directly without overshoot.
 records.append({'bucket':k,'pool':ob.name,'drain':dr.name})
# Add elongated grain, soft color variation and worn dry/wet contrast to real wood.
for name in ('BEACH | pitted salt driftwood','BEACH | wet salt-darkened timber'):
 m=bpy.data.materials[name];n=m.node_tree.nodes;l=m.node_tree.links;bs=n.get('Principled BSDF')
 tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(3,38,6)
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.7
 ramp=n.new('ShaderNodeValToRGB');wet='wet salt' in name
 ramp.color_ramp.elements[0].position=.20;ramp.color_ramp.elements[0].color=(.075,.050,.026,1) if wet else (.19,.135,.076,1)
 ramp.color_ramp.elements[1].position=.80;ramp.color_ramp.elements[1].color=(.25,.19,.10,1) if wet else (.48,.37,.22,1)
 l.new(tex.outputs['Generated'],mapping.inputs[0]);l.new(mapping.outputs['Vector'],noise.inputs['Vector']);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],bs.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.009
 l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);bs.inputs['Roughness'].default_value=.51 if wet else .77
# Make the existing crown flex as each bucket passes under the falling water.
for ob in bpy.data.objects:
 if ob.name.startswith('WATER | V7 impact crown finger'):
  # Geometry is stored in world-local points. Change the bevel to avoid shifting its origin.
  for fr in range(1,98):
   ob.data.bevel_depth=.0022+.0011*(.5+.5*math.cos(2*math.pi*8*(fr-1)/96))
   ob.data.keyframe_insert('bevel_depth',frame=fr)
s.frame_set(25);assert port_points()==baseline_ports
s['source_model']='Beach Pump V8 continuation of recovered unpublished V7'
s['water_simulation']='authored bucket pools, moving drain curves, impact spray and traveling free surface'
s['game_integrated']=False;s['human_visual_approved']=False
root.rotation_euler.z=math.radians(-45)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True
s.render.threads_mode='FIXED';s.render.threads=8
s.render.resolution_x=s.render.resolution_y=768;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.camera.data.ortho_scale=2.75
bpy.ops.wm.save_as_mainfile(filepath=str(out/'beach-pump-v8-review.blend'),compress=True)
def render(name):
 s.render.filepath=str(out/name);bpy.ops.render.render(write_still=True)
render('v8-review.png')
oldcam=s.camera.location.copy();oldscale=s.camera.data.ortho_scale
target=root.matrix_world@Vector((.26,-.13,1.02));s.camera.location=target+Vector((0,-6,6));s.camera.data.ortho_scale=1.42
render('v8-buckets-closeup.png')
s.render.resolution_x=s.render.resolution_y=512;s.cycles.samples=16
# 32 phases avoid the old 16-frame sequence's two-positions-per-bucket sampling.
for i,fr in enumerate(range(1,97,3)):
 s.frame_set(fr);render(f'close-frame-{i:02d}.png')
s.camera.location=oldcam;s.camera.data.ortho_scale=oldscale
s.render.resolution_x=s.render.resolution_y=448
if '--full-motion' in sys.argv:
 for i,fr in enumerate(range(1,97,3)):
  s.frame_set(fr);render(f'frame-{i:02d}.png')
(out/'build-review.json').write_text(json.dumps({'source':'Recovered unpublished native V7','blender':bpy.app.version_string,'bucket_pools':8,'moving_drains':8,'rendered_motion_phases':32,'port_vertices_unchanged':True,'game_integrated':False,'human_visual_approved':False,'native_sha256':hashlib.sha256((out/'beach-pump-v8-review.blend').read_bytes()).hexdigest()},indent=2)+'\n')
