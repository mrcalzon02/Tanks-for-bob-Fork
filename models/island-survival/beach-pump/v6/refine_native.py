"""Refine the checksum-verified V5 native model; no gameplay or atlas edits.

Run in Blender: --background V5.blend --python refine_native.py -- --out DIR
Water is an authored looping mesh surface, not a fluid dynamics simulation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument('--out', type=Path, required=True)
ap.add_argument('--baseline', action='store_true')
ap.add_argument('--animation', action='store_true')
args = ap.parse_args(sys.argv[sys.argv.index('--')+1:])
out = args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
s = bpy.context.scene
root = bpy.data.objects['EXPORT | rotate beachpump not camera']
root.rotation_euler.z = math.radians(-45)
s.frame_set(25)
s.render.engine = 'CYCLES'
s.cycles.device = 'CPU'
s.cycles.samples = 32
s.cycles.use_denoising = True
s.render.resolution_x = s.render.resolution_y = 768
s.render.resolution_percentage = 100
s.render.image_settings.file_format = 'PNG'
s.render.film_transparent = False
s.world.color = (.075, .075, .075)
s.camera.data.ortho_scale = 2.75
s.render.threads_mode = 'FIXED'
s.render.threads = 8

def render(name):
    s.render.filepath = str(out / name)
    bpy.ops.render.render(write_still=True)

if args.baseline:
    render('v5-baseline.png')
    sys.exit(0)

ports = [o for o in bpy.data.objects if o.name.startswith('PORT |')]
def port_vertices():
    bpy.context.view_layer.update()
    return [[tuple(o.matrix_world @ v.co) for v in o.data.vertices] for o in ports]
original_ports = port_vertices()
glass = bpy.data.materials['BEACH V5 | flawed sea-glass screw jacket']
for n in glass.node_tree.nodes:
    if n.type == 'BSDF_GLASS':
        n.inputs['Color'].default_value = (.94, .985, .98, 1)
        n.inputs['Roughness'].default_value = .035
    elif n.type == 'VALTORGB':
        n.color_ramp.elements[0].color = (.055, .055, .055, 1)
        n.color_ramp.elements[1].color = (.40, .40, .40, 1)
glass.name = 'BEACH V6 | clear glass with restrained edge reflections'

water = bpy.data.materials.new('BEACH V6 | clear shallow seawater')
water.use_nodes = True
bs = water.node_tree.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value = (.30, .65, .63, 1)
bs.inputs['Roughness'].default_value = .085
bs.inputs['Transmission Weight'].default_value = .88
bs.inputs['IOR'].default_value = 1.333
old = bpy.data.objects['WATER | one continuous enclosed moving seawater body']
carrier = old.parent
col = old.users_collection[0]
length = float(old['length_bu'])
bpy.data.objects.remove(old, do_unlink=True)
# A closed lower half-cylinder, with a free surface instead of an opaque full bore.
# Project gravity onto the cross section in the fixed screw-carrier coordinate frame.
down = carrier.rotation_euler.to_matrix().inverted() @ Vector((0, 0, -1))
down.z = 0
down.normalize()
side = Vector((-down.y, down.x, 0))
rows, arc, radius = 64, 24, .181
verts, faces = [], []
for k in range(rows+1):
    z = (k/rows-.5)*length
    for j in range(arc+1):
        a = math.pi*j/arc
        p = radius*(side*math.cos(a)+down*math.sin(a))
        verts.append((p.x, p.y, z))
stride = arc+1
for k in range(rows):
    for j in range(arc):
        a = k*stride+j
        faces.append((a,a+1,a+stride+1,a+stride))
    a=k*stride
    faces.append((a,a+stride,a+stride+arc,a+arc))
faces.extend([tuple(reversed(range(stride))),tuple(rows*stride+j for j in range(stride))])
mesh=bpy.data.meshes.new('V6 continuous half-filled water volume')
mesh.from_pydata(verts, [], faces)
mesh.update()
fluid=bpy.data.objects.new('WATER | continuous shallow volume with traveling free surface',mesh)
col.objects.link(fluid)
fluid.parent=carrier
fluid.data.materials.append(water)
for p in mesh.polygons:
    p.use_smooth = len(p.vertices)==4
fluid.shape_key_add(name='Basis')
# Three periodic displacement modes make a continuous traveling ripple, wrapping at 97.
for phase in range(3):
    key=fluid.shape_key_add(name=f'Traveling ripple {phase}')
    for k in range(rows+1):
        amp=.007*math.sin(2*math.pi*(3*k/rows-phase/3))
        for j in (0,arc):
            key.data[k*stride+j].co -= down*amp
    for frame in range(1,98,6):
        key.value=(1+math.cos(2*math.pi*((frame-1)/96-phase/3)))/3
        key.keyframe_insert('value',frame=frame)
fluid['animation_method']='authored traveling free-surface mesh, not fluid simulation'
fluid['water_level']='lower half bore; screw flights and central axle visible above water'

# Give the trough and falling film the same quiet water response.
for ob in bpy.data.objects:
    if ob.name.startswith(('TROUGH | clearly visible','WATER | uninterrupted')):
        ob.data.materials.clear()
        ob.data.materials.append(water)

# V5 retaining collars were accidentally coincident at z=0: separate them along sleeve.
for i,z in enumerate((-.44,.44)):
    bpy.data.objects[f'HOUSING | narrow brass retaining collar {i:02d}'].location.z=z

# Stop pouring in idle. V5 left its continuous falling sheet on at frame zero.
spill=bpy.data.objects['WATER | uninterrupted trough-to-wheel falling sheet']
for frame,hidden in ((0,True),(1,False),(97,False)):
    spill.hide_render=hidden
    spill.keyframe_insert('hide_render',frame=frame)

# Smooth genuine bronze flight faces without changing the authored helical mesh.
flight=bpy.data.objects['SCREW | exposed 3-turn bronze helical flight']
bev=flight.modifiers.new('V6 softened bronze flight edges','BEVEL')
bev.width=.003
bev.segments=3
flight.modifiers.new('V6 bronze weighted normals','WEIGHTED_NORMAL')
s['source_model']='Beach Pump V6 optical and water-surface review'
s['human_visual_approved']=False
s['game_integrated']=False
s['water_simulation']='authored periodic mesh displacement'

checks={'source':'exact reconstructed V5 master','blender':bpy.app.version_string,
        'port_vertices_unchanged':port_vertices()==original_ports,
        'collars_separated':True,'game_integrated':False,'human_visual_approved':False,
        'water_method':'authored traveling mesh free surface, no fluid simulation'}
wheel=bpy.data.objects['MOTION | full bucket waterwheel shaft']
rotor=bpy.data.objects['MOTION | keyed Archimedes screw rotation']
samples={}
for fr in (1,25,49,73,97):
    s.frame_set(fr)
    samples[fr]=[wheel.rotation_euler.x,rotor.rotation_euler.z,
                 fluid.data.shape_keys.key_blocks[1].value]
checks['motion_samples']=samples
checks['wheel_moves']=abs(samples[25][0]-samples[1][0])>1
checks['screw_moves']=abs(samples[25][1]-samples[1][1])>1
checks['loop_transform_error']=max(abs(math.sin(samples[97][i]-samples[1][i])) for i in (0,1))
assert checks['port_vertices_unchanged'] and checks['wheel_moves'] and checks['screw_moves']
assert checks['loop_transform_error']<1e-5
s.frame_set(25)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'beach-pump-v6-review.blend'),compress=True)
render('v6-review.png')
if args.animation:
    s.render.resolution_x=s.render.resolution_y=448
    s.cycles.samples=16
    for i,fr in enumerate(range(1,97,6)):
        s.frame_set(fr)
        render(f'frame-{i:02d}.png')
checks['native_sha256']=hashlib.sha256((out/'beach-pump-v6-review.blend').read_bytes()).hexdigest()
(out/'review-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('V6_REVIEW_VERIFIED',json.dumps(checks),flush=True)
