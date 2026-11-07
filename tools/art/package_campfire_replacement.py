#!/usr/bin/env python3
"""Package a verified four-way campfire capture into Factorio 2.0 replacement assets.

Full-object burning and idle are *alternative* animations, never overlaid.
The original campfire.png and campfire-w.png remain unchanged for rollback.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image


DIRS = ("north", "east", "south", "west")
FRAMES = 16
COLUMNS = 8
CELL_SIZES = (64, 128)


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_idle_sheet(source, size):
    with Image.open(source) as original:
        original.load()
        if original.mode != "RGBA" or original.size != (size, 4*size):
            raise ValueError(f"Invalid four-view idle source: {source}")
        sheet = Image.new("RGBA", (COLUMNS*size, 2*4*size))
        for d in range(4):
            cell = original.crop((0, d*size, size, (d+1)*size))
            if cell.getchannel("A").getbbox() is None:
                raise ValueError(f"Empty idle direction {d}")
            for frame in range(FRAMES):
                x = (frame % COLUMNS)*size
                y = (d*2 + frame//COLUMNS)*size
                sheet.paste(cell, (x, y))
    return sheet


def verify_sheet(sheet, size, *, idle):
    if sheet.mode != "RGBA" or sheet.size != (8*size, 8*size):
        raise ValueError("Replacement atlas dimensions/mode incorrect")
    directions = set()
    for d in range(4):
        first = None
        frame_hashes = set()
        for frame in range(FRAMES):
            x, y = frame % 8*size, (d*2+frame//8)*size
            cell = sheet.crop((x, y, x+size, y+size))
            alpha = cell.getchannel("A")
            if alpha.getbbox() is None or alpha.getextrema()[0] == 255:
                raise ValueError(f"Invalid alpha at direction {d}, frame {frame}")
            signature = hashlib.sha256(cell.tobytes()).hexdigest()
            frame_hashes.add(signature)
            if first is None:
                first = signature
            elif idle and signature != first:
                raise ValueError("Idle animation is not static across all sixteen frames")
        if not idle and len(frame_hashes) != FRAMES:
            raise ValueError(f"Duplicate burning frames in direction {d}")
        directions.add(first)
    if len(directions) < 2:
        raise ValueError("Directions are indistinguishable")


def render_cardinal_lua(filename, size, fps, *, idle):
    fields = []
    for d, label in enumerate(DIRS):
        fields.append(
            f"        {label} = {{ filename = \"__tanks_for_bob_fork__/graphics/entity/{filename}\", "
            f"priority = \"high\", width = {size}, height = {size}, "
            f"x = 0, y = {d*2*size}, frame_count = {FRAMES}, line_length = {COLUMNS}, "
            f"animation_speed = {fps}/60, scale = 0.5, shift = {{0, 0}} }}"
        )
    return "{\n"+",\n".join(fields)+"\n      }"


def patch_entity(lua, fps):
    anchor = lua.index('    --campfire')
    start = lua.index('    graphics_set =', anchor)
    end = lua.index('    crafting_categories =', start)
    old = lua[start:end]
    if ('campfire-w.png' not in old or 'campfire.png' not in old or
            'working_visualisations' not in old):
        raise ValueError("Campfire prototype unexpectedly modified; refusing replacement")
    active = render_cardinal_lua("campfire-v12-burning.png", 128, fps, idle=False)
    idle = render_cardinal_lua("campfire-v12-idle.png", 128, fps, idle=True)
    new = ('    -- V12: complete 45-degree, 4-way render states; no duplicate overlaid base.\n'
           '    graphics_set = {\n'
           '      animation = '+active+',\n'
           '      idle_animation = '+idle+',\n'
           '      always_draw_idle_animation = false,\n'
           '      working_visualisations = {{light = {intensity = 0.4, size = 6}}}\n'
           '    },\n\n')
    revised = lua[:start]+new+lua[end:]
    pos = revised.index('    crafting_speed =', anchor)
    eol = revised.index('\n',pos)
    revised = revised[:eol+1]+'    match_animation_speed_to_activity = false,\n'+revised[eol+1:]
    # Existing collision, energy source, recipes, item names and sounds are preserved.
    return revised


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--output-receipt", type=Path, required=True)
    args = parser.parse_args()
    out = args.capture
    mod = args.mod_root
    qa = json.loads((out/"qa.json").read_text())
    manifest = json.loads((out/"capture.json").read_text())
    config = manifest["config"]
    if not qa.get("passed") or qa["capture_count"] != 68 or qa["atlas_count"] != 6:
        raise ValueError("Capture QA gate failed or wrong number of frames/atlases")
    if config["directions"] != [0,90,180,270] or config["states"]["idle"] != [0] or len(config["states"]["burning"]) != 16:
        raise ValueError("Replacement direction/state config mismatch")
    camera = config.get("camera_override")
    if not camera or camera["elevation_deg"] != 45 or camera["azimuth_deg"] != 0 or abs(camera["ortho_scale"]-2.2)>0.00001:
        raise ValueError("Replacement does not have the approved structure camera")
    if abs(manifest["camera"]["ortho_scale"]-2.2) > 0.0001:
        raise ValueError("Camera ortho scale was not applied")
    if len(manifest["frames"]) != 68:
        raise ValueError("Frame manifest is incomplete")
    records = {(s["state"],s["cell_size"]):s for s in qa["sheets"]}
    for size in CELL_SIZES:
        for state in ("burning","idle"):
            sheet = records[(state,size)]
            expected = [8*size,8*size] if state=="burning" else [size,4*size]
            if sheet["dimensions"] != expected or sheet["direction_count"] != 4:
                raise ValueError("Source sheet dimension/direction validation failed")
            if checksum(out/sheet["path"]) != sheet["sha256"]:
                raise ValueError("Source sheet hash mismatch")
    graphics = mod/"graphics/entity"
    if not graphics.is_dir():
        raise ValueError("Original mod graphics folder missing")
    for name in ("campfire.png","campfire-w.png"):
        if not (graphics/name).is_file():
            raise ValueError(f"Original rollback asset missing: {name}")
    legacy = {name:checksum(graphics/name) for name in ("campfire.png","campfire-w.png")}
    sprites = {}
    for size in CELL_SIZES:
        suffix = "" if size==128 else "-64"
        idle_name = f"campfire-v12-idle{suffix}.png"
        burning_name = f"campfire-v12-burning{suffix}.png"
        idle = build_idle_sheet(out/f"idle-{size}.png",size)
        burning = Image.open(out/f"burning-{size}.png").convert("RGBA")
        verify_sheet(idle,size,idle=True)
        verify_sheet(burning,size,idle=False)
        # Refuse to overwrite previously published output on rerun.
        for name, image in ((idle_name,idle),(burning_name,burning)):
            target=graphics/name
            if target.exists():
                raise FileExistsError(f"Refusing to overwrite already published replacement: {target}")
            image.save(target)
            sprites[name]={"sha256":checksum(target),"size":list(image.size),"cell_size":size}
    entity_file=mod/"prototypes/entity/entities.lua"
    item_file=mod/"prototypes/item/item.lua"
    entity=entity_file.read_text()
    item=item_file.read_text()
    revised=patch_entity(entity,config["fps"])
    old_icon="__tanks_for_bob_fork__/graphics/icons/campfire.png"
    new_icon="__tanks_for_bob_fork__/graphics/icons/campfire-v12.png"
    # Change only the campfire's own item and entity icon, not unrelated appearances.
    campfire_at=item.index('name = "campfire"')
    if old_icon not in item[campfire_at:campfire_at+180]:
        raise ValueError("Unexpected item icon layout")
    item = item[:campfire_at]+item[campfire_at:].replace(old_icon,new_icon,1)
    entity_at=revised.index('    --campfire')
    next_entity=revised.index('    -- tank-assembly',entity_at)
    segment=revised[entity_at:next_entity]
    if segment.count(old_icon)!=1:
        raise ValueError("Unexpected entity icon layout")
    revised=revised[:entity_at]+segment.replace(old_icon,new_icon)+revised[next_entity:]
    icon_file=mod/"graphics/icons/campfire-v12.png"
    if icon_file.exists():
        raise FileExistsError(f"Refusing icon overwrite: {icon_file}")
    with Image.open(out/"frames/idle/d00/f000.png") as src:
        icon = src.convert("RGBA").resize((64,64), Image.Resampling.LANCZOS)
        icon.save(icon_file)
    sprites[icon_file.name]={"sha256":checksum(icon_file),"size":[64,64],"cell_size":64}
    entity_file.write_text(revised)
    item_file.write_text(item)
    if any(checksum(graphics/name) != legacy[name] for name in legacy):
        raise ValueError("Rollback assets changed")
    receipt=dict(passed=True, runtime_tested=False, replacement=True,
        camera=camera,directions=DIRS,states={"idle":4,"burning":64},
        frame_count=16,direction_count=4,atlas_columns=8,atlas_rows=8,
        source_sha256=manifest["source_sha256"],original_sprites_unchanged=legacy,
        assets=sprites,prototype_paths=[str(entity_file),str(item_file)],
        outstanding="Actual Factorio client launch and visual review not exercised by this packer")
    args.output_receipt.parent.mkdir(parents=True,exist_ok=True)
    args.output_receipt.write_text(json.dumps(receipt,indent=2)+"\n")
    print("CAMPFIRE_REPLACEMENT_PACKAGED",json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
