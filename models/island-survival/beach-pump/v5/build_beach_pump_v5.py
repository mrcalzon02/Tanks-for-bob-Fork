#!/usr/bin/env python3
"""Beach Pump V5: native Blender glass-housed Archimedes screw with continuous water.
Derived non-destructively from the exact V4 donor; never alters Factorio gameplay.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V4_PATH = HERE.parent / "v4" / "build_beach_pump_v4.py"
spec = importlib.util.spec_from_file_location("beach_pump_v4_locked", V4_PATH)
v4 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v4
spec.loader.exec_module(v4)
BASE_CONSTRUCT = v4.final_silhouette


def axial_tube(bpy, name, radius, interior_radius, length, material, collection, parent,
               slices=72, levels=2, wave=0.0):
    """Real editable cylindrical surface, optional closed wall or solid contained fluid."""
    verts = []
    faces = []
    # Both glass and water have actual 3D thickness, not cylinder texture decals.
    radii = (radius, interior_radius) if interior_radius else (radius, 0.0)
    for side, rad in enumerate(radii):
        for k in range(levels + 1):
            t = k / levels
            z = (t - 0.5) * length
            for j in range(slices):
                a = 2 * math.pi * j / slices
                r = rad + (wave * math.sin(8 * math.pi * t + 3 * a) if side == 0 else 0)
                verts.append((r * math.cos(a), r * math.sin(a), z))
    stride = (levels + 1) * slices
    for side in range(2):
        offset = side * stride
        for k in range(levels):
            for j in range(slices):
                a = offset + k * slices + j
                b = offset + k * slices + ((j + 1) % slices)
                c = b + slices
                d = a + slices
                faces.append((a, b, c, d) if side == 0 else (d, c, b, a))
    for j in range(slices):
        next_j = (j + 1) % slices
        faces.append((j, next_j, stride + next_j, stride))
        a = levels * slices + j
        b = levels * slices + next_j
        faces.append((b, a, stride + a, stride + b))
    mesh = bpy.data.meshes.new(name + " | real manifold mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    collection.objects.link(ob)
    ob.parent = parent
    mesh.materials.append(material)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    ob["real_3d_manifold"] = True
    ob["outer_radius_bu"] = radius
    ob["inner_radius_bu"] = interior_radius
    ob["length_bu"] = length
    return ob


def shader_materials(bpy, frames):
    glass = bpy.data.materials.new("BEACH V5 | flawed sea-glass screw jacket")
    glass.use_nodes = True
    nodes = glass.node_tree.nodes
    nodes.clear()
    links = glass.node_tree.links
    output = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    actual_glass = nodes.new("ShaderNodeBsdfGlass")
    actual_glass.inputs["Color"].default_value = (.60, .82, .79, 1)
    actual_glass.inputs["Roughness"].default_value = .12
    actual_glass.inputs["IOR"].default_value = 1.45
    facing = nodes.new("ShaderNodeLayerWeight")
    facing.inputs["Blend"].default_value = .3
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = .0
    ramp.color_ramp.elements[0].color = (.17, .17, .17, 1)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (.72, .72, .72, 1)
    links.new(facing.outputs["Fresnel"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix.inputs[0])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(actual_glass.outputs["BSDF"], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    glass["role"] = "optically translucent physical thick glass jacket"

    water = bpy.data.materials.new("BEACH V5 | continuous contained green seawater")
    water.use_nodes = True
    wn = water.node_tree.nodes
    wl = water.node_tree.links
    bsdf = wn.get("Principled BSDF")
    bsdf.inputs["Metallic"].default_value = 0
    bsdf.inputs["Roughness"].default_value = .17
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = .52
    else:
        bsdf.inputs["Transmission"].default_value = .52
    bsdf.inputs["IOR"].default_value = 1.333
    noise = wn.new("ShaderNodeTexNoise")
    noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = 7.8
    noise.inputs["Detail"].default_value = 3.0
    noise.inputs["Roughness"].default_value = .57
    color = wn.new("ShaderNodeValToRGB")
    color.color_ramp.elements[0].position = .24
    color.color_ramp.elements[0].color = (.018, .22, .30, 1)
    color.color_ramp.elements[1].position = .78
    color.color_ramp.elements[1].color = (.09, .67, .70, 1)
    wl.new(noise.outputs["Fac"], color.inputs["Fac"])
    wl.new(color.outputs["Color"], bsdf.inputs["Base Color"])
    bump = wn.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = .12
    bump.inputs["Distance"].default_value = .012
    wl.new(noise.outputs["Fac"], bump.inputs["Height"])
    wl.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    for k, fr in enumerate((*frames, 97)):
        # 97 is an exact wrap, not a visibly discontinuous material seam.
        cycle = (k % len(frames)) / len(frames)
        noise.inputs["W"].default_value = 1.2 * math.sin(2 * math.pi * cycle)
        noise.inputs["W"].keyframe_insert("default_value", frame=fr)
    water["material_animation"] = "cyclic volumetric-color/roughness ripples, 16 keyframes"
    return glass, water


def spill_sheet(bpy, name, start, end, material, col, root, width=.055):
    """One continuous non-beaded physical water sheet from the trough to wheel."""
    from mathutils import Vector
    a, b = Vector(start), Vector(end)
    vertices = []
    segments = 18
    for k in range(segments + 1):
        t = k / segments
        center = a.lerp(b, t)
        center.x += .014 * math.sin(2 * math.pi * t)
        center.y += .009 * math.sin(5 * math.pi * t)
        w = width * (.75 + .20 * math.sin(math.pi * t))
        for sign in (-1, 1):
            vertices.append((center.x + sign * w, center.y, center.z))
    faces = [(2*k, 2*k+1, 2*k+3, 2*k+2) for k in range(segments)]
    mesh = bpy.data.meshes.new(name + " | continuous pouring film")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    col.objects.link(obj)
    obj.parent = root
    obj.data.materials.append(material)
    obj["one_connected_water_sheet"] = True
    return obj


def make_glass_water(bpy, v1, c, original, root, ports):
    result = BASE_CONSTRUCT(bpy, v1, c, original, root, ports)
    carrier = bpy.data.objects["SCREW | diagonal shaft carrier (fixed)"]
    rotor = bpy.data.objects["MOTION | keyed Archimedes screw rotation"]
    flight = bpy.data.objects["SCREW | exposed 3-turn bronze helical flight"]
    if not flight or rotor.parent is not carrier:
        raise RuntimeError("Donor screw rig has changed")
    pockets = [o for o in bpy.data.objects if o.name.startswith("WATER | visibly rising screw pocket")]
    drips = [o for o in bpy.data.objects if o.name.startswith("WATER | cascading trough-wheel spill")]
    if len(pockets) != 6 or len(drips) != 6:
        raise RuntimeError("Expected twelve prior bead-like water meshes")
    for ob in pockets + drips:
        bpy.data.objects.remove(ob, do_unlink=True)

    screw_collection = flight.users_collection[0]
    glass, water = shader_materials(bpy, v4.v3.v2.FRAMES)
    length = float(result["length_bu"])
    sleeve = axial_tube(
        bpy, "HOUSING | continuous flawed glass pressure sleeve",
        .209, .195, length - .085, glass, screw_collection, carrier, levels=2)
    sleeve["glass_real_wall_thickness"] = .014
    fluid = axial_tube(
        bpy, "WATER | one continuous enclosed moving seawater body",
        .164, 0.0, length - .16, water, screw_collection, carrier,
        levels=20, wave=.004)
    fluid["no_disconnected_blue_beads"] = True
    fluid["animated_material"] = water.name

    brass = bpy.data.materials["BEACH | weathered brass"]
    for index, position in enumerate((-.44, .44)):
        v1.cylinder(
            bpy, f"HOUSING | narrow mechanically fastened glass collar {index:02d}",
            (0, 0, position), .218, .028, brass, screw_collection, carrier, n=48)
        # A wide cylinder would occlude the glass; real narrow band can be seen.
        band = bpy.data.objects[f"HOUSING | narrow mechanically fastened glass collar {index:02d}"]
        # Replace solid disk with a true hollow non-occluding ring.
        bpy.data.objects.remove(band, do_unlink=True)
        axial_tube(
            bpy, f"HOUSING | narrow brass retaining collar {index:02d}",
            .224, .210, .026, brass, screw_collection, carrier, levels=1, slices=48)

    # Replace individual falling beads with one uninterrupted water film.
    spill_sheet(bpy, "WATER | uninterrupted trough-to-wheel falling sheet",
                (.225, -.11, 1.34), (.245, -.17, 1.045),
                water, screw_collection, root, width=.06)

    bpy.context.scene["v5_fluid_design"] = "thick real glass, continuous enclosed water, no decorative beads"
    result.update(
        v5_glass_housing=True,
        v5_one_continuous_fluid_body=True,
        v5_deleted_blue_bead_meshes=12,
        v5_animated_water_shader=True,
        v5_continuous_spill_sheet=True,
        v5_materials=[glass.name, water.name],
        v5_screw_rotation_parent_unchanged=True,
        native_pipe_unchanged=True,
    )
    return result


def main():
    if "--self-check" in sys.argv:
        c, original, donor = v4.v3.v2.source()
        assert c["lock"]["native_output_position"] == [0, .25]
        assert c["lock"]["water_per_tick"] == .01
        print("BEACH_PUMP_V5_CONTRACT_AND_DONOR_PASS", flush=True)
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--render", choices=("none", "proof", "all"), default="all")
    parser.add_argument("--samples", type=int, default=16)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:]
                             if "--" in sys.argv else sys.argv[1:])
    if not 4 <= args.samples <= 64:
        raise ValueError("Cycles samples must be in range 4..64")
    v4.final_silhouette = make_glass_water
    v4.main()
    import bpy
    out = args.out.resolve()
    prior = out / "beach-pump-v4.blend"
    native = out / "beach-pump-v5.blend"
    if not prior.is_file() or native.exists():
        raise RuntimeError("V4-derived editable native master not available for V5")
    bpy.context.scene["source_model"] = "Beach Pump V5: enclosed active fluid in glass screw housing"
    bpy.context.scene["game_integrated"] = False
    bpy.context.scene["human_visual_approved"] = False
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native), compress=True,
                               check_existing=False)
    prior.unlink()
    report_path = out / "build-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["schema"] = "tanks.beach-pump.v5.glass-water-native-blender"
    report["native_sha256"] = hashlib.sha256(native.read_bytes()).hexdigest()
    report["visual_refinement"] = "thick transparent glass sleeve, single enclosed fluid body, continuous pouring sheet; twelve prior blue blobs deleted"
    report["game_integrated"] = False
    report["human_visual_approved"] = False
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("BEACH_PUMP_V5_ACTUAL_BLENDER_NATIVE_RENDER_PASS",
          report["render_count"], report["native_sha256"], flush=True)


if __name__ == "__main__":
    main()
