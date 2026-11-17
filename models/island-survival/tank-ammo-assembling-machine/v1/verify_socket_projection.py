import bpy,json,math,sys,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(sys.argv[sys.argv.index('--')+1]).resolve();source=P/'tank-ammo-assembler-v1.blend';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;root=bpy.data.objects['EXPORT | Tanks ammunition component works'];collars=[o for o in root.children_recursive if o.name.startswith('AMMO | full-size fixed pipe collar')];assert len(collars)==2;points={}
for o in collars:
 pts=[o.matrix_world@v.co for v in o.data.vertices];sign=1 if o.location.y>0 else -1;y=(max if sign>0 else min)(p.y for p in pts);points['input' if sign>0 else 'output']=Vector(((max(p.x for p in pts)+min(p.x for p in pts))/2,y,(max(p.z for p in pts)+min(p.z for p in pts))/2))
projection=bpy.data.objects.new('Temporary native square-ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection;rows=[];shift=-1/math.sqrt(2)+.36/math.sqrt(2)-.046875
for name,yaw,ix,iy in [('north',0,0,-1),('east',270,1,0),('south',180,0,1),('west',90,-1,0)]:
 root.rotation_euler.z=math.radians(yaw);bpy.context.view_layer.update()
 for flow,point in points.items():
  ndc=world_to_camera_view(s,s.camera,root.matrix_world@point);actual=((ndc.x-.5)*5.8,(.5-ndc.y)*5.8+shift);sign=1 if flow=='input' else -1;expected=(sign*1.5*ix,sign*1.5*iy-.046875);error=max(abs(actual[i]-expected[i]) for i in range(2));assert error<1e-5,(name,flow,actual,expected);rows.append(dict(facing=name,flow=flow,actual_scene_mouth=list(point),projected_native_mouth=actual,ordinary_pipe_face_anchor=expected,error_tiles=error))
(P/'socket-projection.json').write_text(json.dumps(dict(passed=True,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),scope='Actual collar front-plane geometry projected with canonical camera and square ground correction; independently compared with native ordinary-pipe face anchors at +/-1.5 tile and native vertical pipe axis -0.046875.',source_bore_diameter=.49,source_collar_outside_diameter=.68,source_axis_height=.36,registration_shift=shift,sockets=rows),indent=2)+'\n');print('AMMO_NATIVE_SOCKET_PROJECTION_PASS',max(r['error_tiles'] for r in rows),flush=True)
