"""Render Factorio structure-camera candidates from the existing editable V9 campfire.
This is a diagnostic, not approved game art. Rotations are model-only, camera/light fixed
within each group. No pre-existing sprite, master .blend or accepted asset is changed.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_sprite_frames import matte_stones

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def configure_camera(camera, elevation, azimuth, target):
    radius = 6.0
    e, a = math.radians(elevation), math.radians(azimuth)
    camera.location = Vector(target) + Vector((
        radius * math.sin(a), -radius * math.cos(a), radius * math.tan(e)))
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    return [[round(float(c), 8) for c in row] for row in camera.matrix_world]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    opts = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    out = Path(opts.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    original = Path(bpy.data.filepath)
    scene = bpy.context.scene
    if scene.render.engine != 'CYCLES' or not scene.camera or scene.camera.data.type != 'ORTHO':
        raise RuntimeError('This diagnostic requires the authored Cycles/orthographic scene')
    changes = matte_stones(scene)
    catcher = scene.objects.get("Ground | shadow catcher")
    if catcher:
        catcher.hide_render = True
    scene.render.engine = 'CYCLES'
    scene.render.film_transparent = True
    scene.render.resolution_x = 256
    scene.render.resolution_y = 256
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.cycles.samples = 24
    scene.cycles.seed = 5855
    scene.cycles.use_animated_seed = False
    scene.cycles.device = "CPU"
    camera = scene.camera
    camera.data.ortho_scale = 2.65
    target = (0.0, 0.0, 0.37)
    pivot = bpy.data.objects.new("STRUCTURE_CALIBRATION | model-only pivot", None)
    scene.collection.objects.link(pivot)
    roots = set()
    for ob in list(scene.objects):
        if ob.type not in {'MESH', 'ARMATURE', 'CURVE', 'SURFACE', 'META', 'FONT'}:
            continue
        if ob.name == "Ground | shadow catcher":
            continue
        root = ob
        while root.parent:
            root = root.parent
        if root.type in {'LIGHT', 'CAMERA'}:
            raise RuntimeError("Unexpected camera/light parent in model")
        roots.add(root)
    for root in roots:
        root.parent = pivot
        root.matrix_parent_inverse = Matrix.Identity(4)
    candidate_sets = [
        ("previous_32", 32.4, 35.0, [0]),
        ("candidate_38", 38.0, 0.0, [0]),
        ("factorio_45", 45.0, 0.0, [0, 90, 180, 270]),
        ("candidate_50", 50.0, 0.0, [0]),
        ("diagonal_45", 45.0, 35.0, [0, 90, 180, 270]),
    ]
    captured = []
    for key, elevation, azimuth, directions in candidate_sets:
        camera_matrix = configure_camera(camera, elevation, azimuth, target)
        for angle in directions:
            pivot.rotation_euler.z = math.radians(angle)
            scene.frame_set(0)
            bpy.context.view_layer.update()
            path = out / f"{key}_d{angle:03d}.png"
            scene.render.filepath = str(path)
            print("CALIBRATION_RENDER", key, angle, flush=True)
            bpy.ops.render.render(write_still=True)
            captured.append(dict(
                name=key, elevation_deg=elevation, azimuth_deg=azimuth,
                model_rotation_deg=angle, image=path.name,
                sha256=sha(path), camera_matrix=camera_matrix))
    # A world-plane 1x1 tile proves the ortho 45° ground compression.
    # It is a geometry control, NOT a Wube/Factorio model.
    for root in roots:
        root.hide_render = True
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, 0.02))
    tile = bpy.context.object
    tile.name = "CALIBRATION | 1x1 untextured world tile (proxy)"
    mat = bpy.data.materials.new("CALIBRATION | neutral proxy")
    mat.diffuse_color = (0.32, 0.55, 0.77, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.32, 0.55, 0.77, 1)
    tile.data.materials.append(mat)
    pivot.rotation_euler.z = 0
    configure_camera(camera, 45.0, 0.0, target)
    scene.frame_set(0)
    bpy.context.view_layer.update()
    tile_path = out / "tile_proxy_45.png"
    scene.render.filepath = str(tile_path)
    bpy.ops.render.render(write_still=True)
    captured.append(dict(name="ground_plane_proxy", elevation_deg=45,
        azimuth_deg=0, model_rotation_deg=0, image=tile_path.name,
        sha256=sha(tile_path), notes="1x1 geometric proxy only; not a published Wube mesh"))
    report = dict(
        schema=1, passed=True, approved=False, input_blend=original.name,
        input_sha256=sha(original), blender=bpy.app.version_string,
        pitch_reference="Wube FFF #133: 45-degree dimetric projection",
        original_camera_approx_elevation_deg=32.4,
        model_root_count=len(roots), stone_material_count=len(changes),
        candidate_count=len(captured),
        notes=[
            "No original game sprites or source Blender file overwritten",
            "Candidate elevation/azimuth only; artwork and registration not approved",
            "1x1 tile is a procedural geometric diagnostic, NOT an official STL",
            "All cardinal views rotate the model beneath a fixed camera and daylight",
        ], captures=captured)
    (out / "capture.json").write_text(json.dumps(report, indent=2)+"\n")
    print("CALIBRATION_CAPTURE_OK", len(captured), flush=True)

if __name__=="__main__":
    main()
