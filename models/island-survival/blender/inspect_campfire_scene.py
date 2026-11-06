#!/usr/bin/env python3
"""Audit real mesh objects inside the saved .blend, not merely preview PNG files."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import bpy

args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
if len(args)!=1:
    raise SystemExit("Usage: blender -b scene.blend --python inspect_campfire_scene.py -- /output/manifest.json")
output=Path(args[0])
scene=bpy.context.scene
objects=list(scene.objects)
mesh_objects=[o for o in objects if o.type=="MESH"]
stone=[o for o in mesh_objects if o.name.startswith("stone_")]
wood=[o for o in mesh_objects if o.name.startswith("cross_log")]
ash=[o for o in mesh_objects if o.name.startswith("ash_")]
flame=[o for o in mesh_objects if o.name.startswith("flame_tongue")]
names={o.name for o in objects}

assert len(stone)==15, f"Missing stones: found {len(stone)}"
assert len(wood)>=3, f"Missing wooden logs: found {len(wood)}"
assert len(ash)>=1, f"Missing ash bed: found {len(ash)}"
assert len(flame)==6, f"Missing flames: found {len(flame)}"
assert sum(len(o.data.polygons) for o in mesh_objects)==12152, "Wrong mesh face count"
assert scene.render.engine=="CYCLES" and scene.camera is not None
assert len([im for im in bpy.data.images if im.packed_file])>=15, "Missing packed shader textures"
assert len([m for m in bpy.data.materials if m.name.startswith("CF7")])>=18

expected_collections={
 "01 | Stones + ash + coals": stone+ash,
 "02 | Firewood":wood,
 "03 | Animated fire tongues":flame,
}
for collection,its in expected_collections.items():
    col=bpy.data.collections.get(collection)
    assert col is not None and not col.hide_render, f"Missing or hidden collection: {collection}"
    assert all(col in o.users_collection for o in its), f"Objects misplaced from {collection}"

for ob in mesh_objects:
    assert not ob.hide_render, f"Mesh hidden from render: {ob.name}"
    assert ob.data.vertices and ob.data.polygons, f"Empty mesh: {ob.name}"
    assert ob.data.uv_layers, f"No UV maps: {ob.name}"
    assert len(ob.data.materials), f"No materials: {ob.name}"
    for vertex in ob.data.vertices:
        assert all(math.isfinite(v) for v in vertex.co), f"Invalid vertex coordinate: {ob.name}"
for ob in flame:
    assert ob.animation_data and ob.animation_data.action, f"Not keyed: {ob.name}"
fl=bpy.data.objects.get("04 | animated fire light")
assert fl and fl.type=="LIGHT" and fl.data.animation_data, "Missing keyed firelight"
scene.frame_set(1)
state_a=[tuple(o.scale) for o in flame]
scene.frame_set(37)
state_b=[tuple(o.scale) for o in flame]
assert state_a!=state_b, "Flames do not change along timeline"
manifest={
 "native_blend":bpy.data.filepath,
 "blender_version":bpy.app.version_string,
 "render_engine":scene.render.engine,
 "camera":scene.camera.name,
 "timeline_frames":[scene.frame_start,scene.frame_end],
 "mesh_object_count":len(mesh_objects),
 "stone_objects":[o.name for o in stone],
 "log_objects":[o.name for o in wood],
 "ash_objects":[o.name for o in ash],
 "animated_flame_objects":[o.name for o in flame],
 "total_triangles":sum(len(o.data.polygons) for o in mesh_objects),
 "packed_images":len([im for im in bpy.data.images if im.packed_file]),
 "lighting_objects":[o.name for o in objects if o.type=="LIGHT"],
 "objects_sample":[{"name":o.name,"faces":len(o.data.polygons),"collection":[c.name for c in o.users_collection]} for o in mesh_objects[:24]],
 "verified_editable":True,
 "verified_keyframed":True
}
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(manifest,indent=2)+"\n")
print("BLENDER_OBJECTS_VERIFIED "+json.dumps({k:manifest[k] for k in ["mesh_object_count","total_triangles","packed_images","verified_editable","verified_keyframed"]}))
