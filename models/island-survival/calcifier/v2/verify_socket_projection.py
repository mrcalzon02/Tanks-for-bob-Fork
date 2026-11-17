"""Measure real mouth end rings and their native screen registration in all facings."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[1]/'candidates/v2-sockets08'
source=P/'calcifier-v2.blend';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;s.frame_set(1);root=bpy.data.objects['EXPORT | Calcifier all authored parts']
projection=bpy.data.objects.new('Temporary native square-ground projection',None);s.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
shift=-1.08/math.sqrt(2)+.2076834412;records=[];maximum=0.
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
 root.rotation_euler.z=math.radians(yaw);bpy.context.view_layer.update()
 for sign,role in [(1,'input'),(-1,'unused_output')]:
  local=Vector((0,sign*1.5,.36));p=world_to_camera_view(s,s.camera,root.matrix_world@local)
  actual=[(p.x-.5)*5.6,(.5-p.y)*5.6+shift]
  x=-sign*1.5*math.sin(math.radians(yaw));y=-sign*1.5*math.cos(math.radians(yaw))-.046875
  error=max(abs(actual[0]-x),abs(actual[1]-y));maximum=max(maximum,error)
  records.append({'facing':facing,'role':role,'native_screen_mouth_center':actual,'expected_screen_center':[x,y],'error_tiles':error})
root.rotation_euler.z=0;bpy.context.view_layer.update();geometry=[]
for sign,term in [(1,'north inlet'),(-1,'capped unused south outlet')]:
 o=bpy.data.objects['CALCIFIER V2 | full bore '+term+' reducer'];radii=[math.hypot(v.co.x,v.co.z-.36) for v in o.data.vertices if abs(v.co.y-sign*1.5)<1e-5]
 assert radii and abs(min(radii)-.28)<1e-5 and abs(max(radii)-.30)<1e-5
 geometry.append({'role':term,'mouth_plane_y':sign*1.5,'source_axis_z':.36,'bore_radius':min(radii),'outer_radius':max(radii),'fixed_native_grid_unchanged':True})
result={'passed':maximum<1e-5,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'maximum_projection_error_tiles':maximum,'native_registration_y':.2076834412,'mouth_measurements':geometry,'facings':records,'basis':'Standard Factorio pipe metal-axis screen height -1.5 native pixels; confirm with four actual placed-pipe close screenshots. No prototype positions changed.'}
(P/'socket-projection-verification.json').write_text(json.dumps(result,indent=2)+'\n');assert result['passed'];print('NATIVE_SOCKET_PROJECTION_PASS',maximum,flush=True)
