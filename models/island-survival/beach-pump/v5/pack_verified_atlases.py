#!/usr/bin/env python3
"""Pack SHA-verified 68 native Beach Pump V5 Cycles frames; never attach game graphics.

Factorio direction slots are North, East, South, West. Blender's cardinal
root yaw sequence is North, West, South, East in Factorio sprite coordinates;
therefore the input direction slots are (0, 3, 2, 1), NOT (0, 1, 2, 3).
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

STATES = ("idle", "working")
SIZES = (64, 128, 256)
DIRECTIONS = ("north", "east", "south", "west")
BLENDER_FOR_FACTORIO = (0, 3, 2, 1)
FRAMES = tuple(range(1, 92, 6))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(source: Path):
    report = json.loads((source / "build-report.json").read_text(encoding="utf-8-sig"))
    proof = json.loads((source / "native-reopen-qa.json").read_text(encoding="utf-8-sig"))
    assert report["schema"] == "tanks.beach-pump.v5.glass-water-native-blender"
    assert report["render_mode"] == "all" and report["render_count"] == 68
    assert len(report["renders"]) == 68
    assert tuple(report["four_facings"]) == (0, 90, 180, 270)
    assert tuple(report["working_frames"]) == FRAMES and report["fps"] == 8
    assert proof["schema"] == "tanks.beach-pump.v5.independent-native-qa"
    assert proof["passed"] and proof["actual_blender_frames"] == 68
    assert proof["native_sha256"] == report["native_sha256"] == sha(source / "beach-pump-v5.blend")
    assert proof["fixed_native_port_meshes"] == 2
    assert proof["fixed_port_vertices_each"] == 256
    assert proof["port_max_drift_bu"] == 0
    assert proof["frame97_matches_frame1"] and proof["one_45_degree_ortho_camera"]
    assert proof["native_south_output"] == [0, .25] and proof["source_offset"] == [0, -1]
    assert proof["gameplay_original_rate_per_tick"] == report["native_offshore"]["water_per_tick"] == .01
    assert proof["real_helix_mesh_vertices"] >= 500
    assert proof["water_wheel_paddles"] == 8 and proof["large_eccentric_side_crank"]
    assert not report["game_integrated"] and not proof["game_integrated"]
    assert not report["human_visual_approved"] and not proof["human_visual_approved"]
    assert report["shoreline_selection"] == [[-.6, -1.49], [.6, .49]]

    inputs = {}
    for row in report["renders"]:
        d = int(row["direction"])
        state, k = row["state"], int(row["index"])
        assert 0 <= d < 4 and state in STATES
        assert (state == "idle" and k == -1 and row["frame"] == 0) or (
            state == "working" and 0 <= k < 16 and row["frame"] == FRAMES[k])
        expected_name = (f"idle-d{d:02d}.png" if state == "idle" else
                         f"working-d{d:02d}-f{k:03d}.png")
        assert row["file"] == expected_name
        key = (state, d, k)
        assert key not in inputs, ("duplicate source frame", key)
        path = source / expected_name
        assert path.is_file() and sha(path) == row["sha256"], expected_name
        with Image.open(path) as img:
            assert img.mode == "RGBA" and img.size == (256, 256)
            bounds = img.getchannel("A").getbbox()
            assert bounds and bounds[0] > 0 and bounds[1] > 0 and bounds[2] < 256 and bounds[3] < 256
        inputs[key] = path
    assert len(inputs) == 68
    for d in range(4):
        assert ("idle", d, -1) in inputs
        for k in range(16):
            assert ("working", d, k) in inputs
        with Image.open(inputs["working", d, 0]) as first, Image.open(inputs["working", d, 4]) as fifth:
            assert ImageChops.difference(first.convert("RGB"), fifth.convert("RGB")).getbbox(), d
    return report, proof, inputs


def pack(source: Path, out: Path):
    if out.exists():
        raise FileExistsError(f"Refusing to overwrite any atlas candidate: {out}")
    report, proof, inputs = validate(source)
    out.mkdir(parents=True, exist_ok=False)
    files = {}
    for size in SIZES:
        for state in STATES:
            columns, rows = ((4, 1) if state == "idle" else (8, 8))
            atlas = Image.new("RGBA", (columns * size, rows * size), (0, 0, 0, 0))
            for slot, source_direction in enumerate(BLENDER_FOR_FACTORIO):
                for index in ((-1,) if state == "idle" else range(16)):
                    with Image.open(inputs[state, source_direction, index]) as img:
                        cell = img.copy() if size == 256 else img.resize((size, size), Image.Resampling.LANCZOS)
                    col = slot if state == "idle" else index % 8
                    row = 0 if state == "idle" else slot * 2 + index // 8
                    x, y = col * size, row * size
                    atlas.paste(cell, (x, y))
                    assert atlas.crop((x, y, x + size, y + size)).tobytes() == cell.tobytes()
            filename = f"{state}-{size}.png"
            destination = out / filename
            atlas.save(destination, optimize=True)
            with Image.open(destination) as reopened:
                reopened.verify()
            with Image.open(destination) as reopened:
                assert reopened.mode == "RGBA" and reopened.size == (columns * size, rows * size)
            files[filename] = {"sha256": sha(destination), "width": columns * size,
                               "height": rows * size, "bytes": destination.stat().st_size}
    manifest = {
        "schema": "tanks.beach-pump.v5.68-frame-six-candidate-atlases",
        "passed": True,
        "native_blender_sha256": report["native_sha256"],
        "independent_blender_reopen_passed": True,
        "actual_cycles_frames": 68,
        "offshore_entity": "offshore-pump/beachpump",
        "water_per_tick": .01,
        "fluid_source_offset": [0, -1],
        "native_south_output": [0, .25],
        "directions_factorio": list(DIRECTIONS),
        "blender_direction_by_factorio_slot": list(BLENDER_FOR_FACTORIO),
        "fps": 8,
        "working_frames_each_direction": 16,
        "atlas_layout": {"idle": [4, 1], "working": [8, 8]},
        "files": files,
        "official_factorio_offshore_schema_tested": False,
        "original_game_graphics_replaced": False,
        "native_client_visual_approved": False
    }
    (out / "candidate-atlas-qa.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("BEACH_PUMP_V5_68_REAL_CYCLES_FRAMES_SIX_ATLASES_PASS", report["native_sha256"], flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    pack(args.source.resolve(), args.out.resolve())


if __name__ == "__main__":
    main()
