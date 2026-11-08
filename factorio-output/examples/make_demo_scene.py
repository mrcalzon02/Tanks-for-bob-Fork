"""Generate a real editable Blender press for the portable workflow smoke test."""
import bpy
from mathutils import Vector
from pathlib import Path
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="CYCLES"
scene.cycles.device="CPU"
scene.cycles.samples=12
scene.cycles.use_denoising=False
for layer in scene.view_layers: layer.cycles.use_denoising=False
scene.render.film_transparent=True
scene.render.resolution_x=scene.render.resolution_y=256
scene.render.resolution_percentage=100
wood=bpy.data.materials.new("Wood")
wood.use_nodes=True
wood.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(.38,.20,.095,1)
iron=bpy.data.materials.new("Iron")
iron.use_nodes=True
iron.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(.26,.31,.35,1)
def beam(name,pos,size,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
    ob=bpy.context.object
    ob.name=name
    ob.dimensions=size
    ob.data.materials.append(material)
    return ob
beam("Square timber footing",(0,0,.18),(1.10,.8,.24),wood)
beam("Left post",(-.43,0,.64),(.12,.16,.82),wood)
beam("Right post",(.43,0,.64),(.12,.16,.82),wood)
beam("Top timber",(0,0,1.04),(1.1,.2,.14),wood)
pivot=bpy.data.objects.new("Animated lever",None)
scene.collection.objects.link(pivot)
pivot.location=(0,0,.86)
lever=beam("Driven iron lever",(.12,0,.85),(.58,.12,.12),iron)
matrix=lever.matrix_world.copy()
lever.parent=pivot
lever.matrix_world=matrix
for frame,angle in ((0,-.18),(1,-.18),(5,.03),(9,.22),(13,-.06),(17,-.18)):
    pivot.rotation_euler.z=angle
    pivot.keyframe_insert(data_path="rotation_euler",frame=frame)
camera_data=bpy.data.cameras.new("Structure camera")
camera_data.type="ORTHO"
camera_data.ortho_scale=3.0
camera=bpy.data.objects.new("Structure camera",camera_data)
scene.collection.objects.link(camera)
focus=Vector((0,0,.56))
camera.location=(0,-5,5.56)
camera.rotation_euler=(focus-camera.location).to_track_quat("-Z","Y").to_euler()
scene.camera=camera
daylight=bpy.data.lights.new("Fixed daylight","AREA")
daylight.energy=440
daylight.shape="DISK"
daylight.size=4.5
lamp=bpy.data.objects.new("Fixed daylight",daylight)
scene.collection.objects.link(lamp)
lamp.location=(-3,-4,7)
lamp.rotation_euler=(focus-lamp.location).to_track_quat("-Z","Y").to_euler()
scene.world.use_nodes=True
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.6
scene.frame_set(0)
target=Path(__file__).resolve().parent/"demo.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(target),check_existing=False)
print("FACT_OUTPUT_EDITABLE_BLENDER_EXAMPLE_SAVED",target)
