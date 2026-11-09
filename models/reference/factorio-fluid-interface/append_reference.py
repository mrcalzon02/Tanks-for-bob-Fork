"""Append an editable, locally owned fluid-interface reference into a machine.

Blender Python API::

    collection, root = append_interface(
        "/path/to/factorio-fluid-interface-reference.blend",
        joint_ground=(0, 1.5, 0), facing="N", name="Cooking Fire north inlet"
    )

The placement root is the ground projection of the joint, not its raised socket
centre. One unit is one tile; the canonical socket is Z0.36 above this root.
Only FACTORIO_FLUID_INTERFACE_REFERENCE is appended, with link=False. The
environment, camera and lights are not imported. Multiple calls create separate
editable assemblies; object names are never used to identify the placement root.

The function preserves the asset's visibility settings. It does not hide or
promote any guide geometry for production, change the machine, reset the scene,
or save a file. The CLI saves a new output file only when explicitly requested::

    blender --background machine.blend --python append_reference.py -- \
        --reference factorio-fluid-interface-reference.blend \
        --output machine-with-pipe-reference.blend --joint 0 1.5 0 --facing N

Existing output files are refused. The active machine scene remains intact.
"""

import argparse
import json
import math
from pathlib import Path
import sys

import bpy


COLLECTION_NAME = "FACTORIO_FLUID_INTERFACE_REFERENCE"
STANDARD_ID = "factorio-fluid-interface-v1"
YAW_DEGREES = {"N": 0.0, "E": -90.0, "S": 180.0, "W": 90.0}
EXPECTED_ROLES = {
    "placement_root",
    "reference_barrel",
    "reference_near_collar",
    "reference_far_collar",
    "machine_collar",
    "machine_throat",
    "socket_marker",
    "machine_cell_marker",
    "adjacent_cell_marker",
}

# A rejected import removes only IDs that this call created. Existing scene IDs
# are never unlinked or altered. Dependency IDs are removed only when unused.
_ID_GROUPS = (
    "collections", "objects", "meshes", "curves", "materials", "images",
    "cameras", "lights", "worlds", "actions", "node_groups",
)


def _snapshot_ids():
    return {name: set(getattr(bpy.data, name)) for name in _ID_GROUPS}


def _discard_import(before):
    for name in ("collections", "objects"):
        ids = getattr(bpy.data, name)
        for item in list(ids):
            if item not in before[name]:
                ids.remove(item, do_unlink=True)
    # Repeat for dependencies such as a material that releases an image or a
    # node group only after the owning material has been removed.
    for _ in range(3):
        removed = False
        for name in _ID_GROUPS[2:]:
            ids = getattr(bpy.data, name)
            for item in list(ids):
                if item not in before[name] and item.users == 0:
                    ids.remove(item)
                    removed = True
        if not removed:
            break


def _ground_coordinates(value):
    try:
        coordinates = tuple(float(component) for component in value)
    except (TypeError, ValueError) as exc:
        raise ValueError("joint_ground must contain three finite numbers") from exc
    if len(coordinates) != 3 or not all(math.isfinite(v) for v in coordinates):
        raise ValueError("joint_ground must contain three finite numbers")
    return coordinates


def _placement_root(collection):
    objects = list(collection.all_objects)
    roots = [obj for obj in objects if obj.get("interface_role") == "placement_root"]
    if len(roots) != 1:
        raise ValueError(f"Expected one placement_root, found {len(roots)}")
    root = roots[0]
    if root.type != "EMPTY" or root.parent is not None:
        raise ValueError("The placement root must be an unparented Empty")
    if any(not math.isfinite(float(v)) or abs(float(v) - 1.0) > 1e-6 for v in root.scale):
        raise ValueError("Reference root scale must be (1, 1, 1)")
    if root.constraints or root.animation_data:
        raise ValueError("The reference placement root must be static and unconstrained")

    standard_ids = [owner.get("standard_id") for owner in (collection, root)]
    declared = [value for value in standard_ids if value is not None]
    if not declared or any(value != STANDARD_ID for value in declared):
        raise ValueError(f"Expected reference standard_id={STANDARD_ID!r}")

    roles = {}
    for obj in objects:
        role = obj.get("interface_role")
        if role not in EXPECTED_ROLES:
            raise ValueError(f"Unexpected or missing interface_role on appended object: {role!r}")
        roles.setdefault(role, []).append(obj)
        if obj.type in {"CAMERA", "LIGHT"}:
            raise ValueError("Reference collection contains a review camera or light")
        if obj is root:
            continue
        ancestor = obj.parent
        while ancestor is not None and ancestor is not root:
            ancestor = ancestor.parent
        if ancestor is not root:
            raise ValueError(f"Reference component {role!r} is outside the placement hierarchy")
    if set(roles) != EXPECTED_ROLES or any(len(items) != 1 for items in roles.values()):
        raise ValueError("Reference must contain exactly one object for every canonical interface role")
    return root


def append_interface(reference_blend, joint_ground=(0, 0, 0), facing="N", name=None, scene=None):
    """Append one reference assembly and return ``(collection, placement_root)``.

    ``scene`` is a Blender Scene, defaulting to the active scene. ``facing`` is
    N/E/S/W; Blender +Y is north and +X is east. ``name`` optionally labels the
    new collection and root; Blender resolves name collisions automatically.
    The whole assembly is placed through its root at unit scale. Source role
    properties, socket identities, geometry and visibility flags are retained.
    """
    reference_path = Path(reference_blend).expanduser().resolve()
    if not reference_path.is_file():
        raise FileNotFoundError(reference_path)
    if reference_path.suffix.lower() != ".blend":
        raise ValueError("reference_blend must identify a .blend file")
    ground = _ground_coordinates(joint_ground)
    if not isinstance(facing, str) or facing.strip().upper() not in YAW_DEGREES:
        raise ValueError("facing must be one of N, E, S or W")
    facing = facing.strip().upper()
    target_scene = scene if scene is not None else bpy.context.scene
    if not isinstance(target_scene, bpy.types.Scene):
        raise TypeError("scene must be a Blender Scene")
    if name is not None and (not isinstance(name, str) or not name.strip()):
        raise ValueError("name must be a nonempty string when provided")

    before = _snapshot_ids()
    try:
        with bpy.data.libraries.load(str(reference_path), link=False) as (source, loaded):
            if COLLECTION_NAME not in source.collections:
                raise ValueError(f"Source file does not contain {COLLECTION_NAME!r}")
            loaded.collections = [COLLECTION_NAME]
        collection = loaded.collections[0]
        if collection is None or collection in before["collections"]:
            raise RuntimeError("A new local reference collection was not appended")
        if collection.library is not None:
            raise RuntimeError("The reference was linked instead of appended locally")
        root = _placement_root(collection)
        if name is not None:
            collection.name = name.strip()
            root.name = name.strip() + " | ground placement root"
        root.rotation_mode = "XYZ"
        root.location = ground
        root.rotation_euler = (0.0, 0.0, math.radians(YAW_DEGREES[facing]))
        root.scale = (1.0, 1.0, 1.0)
        root["placed_ground"] = list(ground)
        root["placed_facing"] = facing
        target_scene.collection.children.link(collection)
        return collection, root
    except Exception:
        _discard_import(before)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--joint", nargs=3, type=float, default=(0, 0, 0), metavar=("X", "Y", "Z"))
    parser.add_argument("--facing", choices=tuple(YAW_DEGREES), default="N")
    parser.add_argument("--name")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(argv)
    output = args.output.expanduser().resolve()
    if output.suffix.lower() != ".blend":
        raise ValueError("--output must be a .blend path")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {output}")
    collection, root = append_interface(args.reference, args.joint, args.facing, args.name)
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False, compress=True)
    print(json.dumps({
        "output": str(output),
        "collection": collection.name,
        "root": root.name,
        "standard_id": STANDARD_ID,
        "joint_ground": list(root.location),
        "facing": args.facing,
        "root_scale": list(root.scale),
    }))


if __name__ == "__main__":
    main()
