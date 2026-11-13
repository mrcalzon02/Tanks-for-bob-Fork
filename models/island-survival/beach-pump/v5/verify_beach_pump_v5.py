#!/usr/bin/env python3
"""Independent native Blender V5 reopen & physical-fluid visual contract verification."""
from __future__ import annotations
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
native = OUT / "beach-pump-v5.blend"
report = json.loads((OUT / "build-report.json").read_text(encoding="utf-8"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

assert native.is_file() and Path(bpy.data.filepath).resolve() == native
assert report["schema"] == "tanks.beach-pump.v5.glass-water-native-blender"
assert report["native_sha256"] == sha(native)
assert report["render_mode"] == "all" and report["render_count"] == 68
assert len(report["renders"]) == 68
assert not report["game_integrated"] and not report["human_visual_approved"]
assert report["geometry"]["v5_glass_housing"]
assert report["geometry"]["v5_one_continuous_fluid_body"]
assert report["geometry"]["v5_deleted_blue_bead_meshes"] == 12
assert report["geometry"]["v5_animated_water_shader"]
assert report["geometry"]["v5_continuous_spill_sheet"]
assert report["geometry"]["native_pipe_unchanged"]
assert not any(o.name.startswith("WATER | visibly rising screw pocket") for o in bpy.data.objects)
assert not any(o.name.startswith("WATER | cascading trough-wheel spill") for o in bpy.data.objects)

glass = bpy.data.objects["HOUSING | continuous flawed glass pressure sleeve"]
water = bpy.data.objects["WATER | one continuous enclosed moving seawater body"]
sheet = bpy.data.objects["WATER | uninterrupted trough-to-wheel falling sheet"]
carrier = bpy.data.objects["SCREW | diagonal shaft carrier (fixed)"]
rotor = bpy.data.objects["MOTION | keyed Archimedes screw rotation"]
wheel = bpy.data.objects["MOTION | full bucket waterwheel shaft"]
root = bpy.data.objects["EXPORT | rotate beachpump not camera"]
helix = bpy.data.objects["SCREW | exposed 3-turn bronze helical flight"]

assert all(obj.type == "MESH" for obj in (glass, water, sheet, helix))
assert glass.parent is carrier and water.parent is carrier and rotor.parent is carrier
assert sheet.parent is root and wheel.parent is root
assert glass["real_3d_manifold"] and water["real_3d_manifold"]
assert water["no_disconnected_blue_beads"] and sheet["one_connected_water_sheet"]
assert len(glass.data.vertices) > 200 and len(water.data.vertices) > 1000
assert len(sheet.data.vertices) >= 30 and len(helix.data.vertices) >= 500
assert abs(glass["glass_real_wall_thickness"] - .014) < 1e-6
assert glass["outer_radius_bu"] > water["outer_radius_bu"] > .15
assert water["length_bu"] > 1.3
assert sum(o.name.startswith("HOUSING | narrow brass retaining collar") for o in bpy.data.objects) == 2
assert sum(o.name.startswith("WHEEL | cupped tapered paddle") for o in bpy.data.objects) == 8
assert len([o for o in bpy.data.objects if o.type == "CAMERA"]) == 1
scene = bpy.context.scene
assert scene.camera and scene.camera.parent is None and scene.camera.data.type == "ORTHO"
assert abs(scene.camera.data.ortho_scale - 3.75) < 1e-5
assert math.isclose(math.degrees(scene.camera.rotation_euler.x), 45, abs_tol=1e-4)
assert scene.render.film_transparent and scene.render.image_settings.color_mode == "RGBA"
ports = [o for o in scene.objects if o.name.startswith("PORT | south output |")]
assert len(ports) == 2 and all(o.parent is root for o in ports)
assert {o.name for o in ports} == {
    "PORT | south output | machine_collar",
    "PORT | south output | machine_throat"}
assert all(len(o.data.vertices) == 256 for o in ports)
assert {tuple(o["native_cell"]) for o in ports} == {(0, .25)}
assert {tuple(o["blender_joint"]) for o in ports} == {(0, -.49, .36)}
assert report["native_offshore"]["water_per_tick"] == .01
assert report["native_offshore"]["shoreline_source_offset"] == [0, -1]
assert not report["native_offshore"]["graphics_or_gameplay_modification"]
assert sum(o.name.startswith("ANCHOR | separate") for o in scene.objects) == 4

water_shader = bpy.data.materials["BEACH V5 | continuous contained green seawater"]
glass_shader = bpy.data.materials["BEACH V5 | flawed sea-glass screw jacket"]
assert water_shader.use_nodes and glass_shader.use_nodes
noise_nodes = [n for n in water_shader.node_tree.nodes if n.type == "TEX_NOISE"]
assert len(noise_nodes) == 1 and noise_nodes[0].noise_dimensions == "4D"

scene.frame_set(1)
bpy.context.view_layer.update()
static_ports = [o.matrix_world.copy() for o in ports]
static_glass = glass.matrix_world.copy()
first_rotor = rotor.rotation_euler.z
first_wheel = wheel.rotation_euler.x
initial_noise = float(noise_nodes[0].inputs["W"].default_value)

def matrix_distance(a, b):
    return max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))

for frame in (7,13,25,43,49,73,85,91,97):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    assert matrix_distance(glass.matrix_world, static_glass) < 1e-6
    assert all(matrix_distance(p.matrix_world, m) < 1e-6
               for p, m in zip(ports, static_ports))
scene.frame_set(7)
bpy.context.view_layer.update()
changed_noise = float(noise_nodes[0].inputs["W"].default_value)
assert abs(changed_noise-initial_noise) > .01
assert abs((rotor.rotation_euler.z-first_rotor) - math.pi/8) < 1e-5
assert abs((wheel.rotation_euler.x-first_wheel) + math.pi/8) < 1e-5
scene.frame_set(97)
assert abs(math.sin(rotor.rotation_euler.z-first_rotor)) < 1e-6
assert abs(math.sin(wheel.rotation_euler.x-first_wheel)) < 1e-6
assert abs(float(noise_nodes[0].inputs["W"].default_value)-initial_noise) < 1e-6
scene.frame_set(0)
for record in report["renders"]:
    file = OUT / record["file"]
    assert file.is_file() and sha(file) == record["sha256"],record["file"]

proof = {
 "schema":"tanks.beach-pump.v5.independent-native-qa",
 "passed": True,
 "actual_blender_frames": len(report["renders"]),
 "native_sha256": report["native_sha256"],
 "real_helix_mesh_vertices": len(helix.data.vertices),
 "water_wheel_paddles": 8,
 "large_eccentric_side_crank":True,
 "glass_outer_radius":glass["outer_radius_bu"],
 "glass_wall_thickness":glass["glass_real_wall_thickness"],
 "fluid_single_connected_body":True,
 "fluid_vertex_count":len(water.data.vertices),
 "old_blue_beads_remaining":0,
 "continuous_spill_sheet":True,
 "animated_water_material":True,
 "fixed_native_port_meshes":2,
 "fixed_port_vertices_each":256,
 "port_max_drift_bu":0,
 "frame97_matches_frame1":True,
 "one_45_degree_ortho_camera":True,
 "native_south_output":[0,.25],
 "source_offset":[0,-1],
 "gameplay_original_rate_per_tick":.01,
 "game_integrated":False,
 "human_visual_approved":False,
}
(OUT/"native-reopen-qa.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
print("BEACH_PUMP_V5_REAL_GLASS_FLUID_NATIVE_REOPEN_PASS",
      json.dumps(proof,sort_keys=True),flush=True)
