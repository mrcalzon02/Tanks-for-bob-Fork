# CLAY PIT — visual source audit and V1 Blender reconstruction work order

Status: **V1 BLOCKOUT / NOT APPROVED ART / NOT INSTALLED**. Authoritative visual sources are the actual currently installed mod sprite paths, not descriptive guesses about how a clay pit should operate. Do not modify live Factorio prototype or sprite assets during blockout.

## Source-of-truth finding — critical

- The current main-branch `tanks_for_bob_fork_1.8.95/graphics/entity/clay-pit.png` is **64 × 64**. The previously packaged 2.1 build `tanks_for_bob_fork_1.8.96.zip` has a **120 × 64** variant with one dominant basin at the left and two extra smaller bowl drawings to the right. In either case, the entity's `graphics_set.animation` reads **one 64 × 64 frame**, with `line_length=1`, at `(0, 0)`. Only **one dominant basin** is visible in the current game. The two extras in the archived file fall outside the active sprite crop and should be reusable optional variants, not new visible pits.
- `graphics/entity/clay-pit-w.png` is **64 × 64**, one-frame active overlay. It draws several slim straight implements *over* the primary bowl. Treat their identity as interpretive where pixels cannot resolve it. The overlay appears to show a left-hand spade/scoop, a central upright marked with a yellow tip, a small suspended scoop or weight, and diagonal/crossbar sticks to the right. Preserve their relative arrangement, not imagined moving gears.
- Visible alpha bounds in the prototype crop: base approximately `(0,0,62,62)`, working overlay `(0,2,62,56)` in top-left-origin pixel coordinates. The current base already fills most of its 64px canvas.
- Current graphics: idle base plus active overlay. Future modernized sprites should instead use complete idle/active states **as alternatives** (not full-object duplicate overlays), following the accepted campfire four-way pipeline.

## Sprite-space construction map (the actual first 64 × 64 crop)

These are approximate visual reading zones, deliberately not purported pixel-perfect object bounding boxes:

| Visual element | Approx. sprite zone (x, y) | Model interpretation | Confidence |
|---|---|---|---|
| Primary outside ochre lip | x~2–61, y~0–61 | One uneven, thick dry-earth/clay rim enclosing a recessed basin; soft rounded edges | High |
| Warm inner bank | x~8–55, y~8–54 | Sloped inside wall, not a second separate pit | High |
| Dark muddy depression | x~12–52, y~28–55 | Low, irregular wet clay bottom; strong occlusion and low specular response | High |
| Left narrow rod with pale tip | x~0–23, y~21–37 | Crude spade / paddle oriented obliquely into pit | Medium |
| Central yellow-tipped upright | x~24–33, y~9–43 | Primitive pole/stake with lash or small marker | High as a pole, lower as to purpose |
| Hanging dark/light detail | x~25–34, y~31–49 | Suspended small scoop, lump, or weighted handle; avoid definite invented machinery | Medium-low |
| Right cross/diagonal poles | x~28–61, y~2–55 | Crude pole-frame, crossbar, diagonal supports | High as lines, medium as assembled mechanism |
| Two extra bowls beyond game crop | x~70–119 in *120px file* | **Unused source artwork**, retain as reusable variants for future pit/pond/kiln kits | High |

## Blender object hierarchy: durable primitive earthwork kit

- `CLAY PIT | reusable earthwork module` — one layered, editable excavated bowl mesh with irregular outer soil skirt, raised ochre lip, inner banks, wet recessed floor, and separate sparse clay clods/rim fragments. NO invented huts, brick walls, metal engine, underground pipe mechanism, or a huge rectangular foundation slab.
- `WORKING | primitive implements` — separate simple spade, pole assembly, rough wood support rods, fiber cord and small suspended scoop-shaped mass. Animation may be subtle stirring / oscillation, but does not prove the sprite itself was animated (original overlay is a still).
- `FIXED | Factorio lighting and camera` — fixed 45° orthographic camera, matte clay materials, stable soft area lights. Only the model rotates to generate 0/90/180/270°.
- `EXPORT | model rotation pivot` — common hierarchy root for reusable four-way capture.

## V1 modeling measurements — relative Blender units, not real-world dimensions

- Footprint: target about 2.5 × 2.9 in a 3 × 3 nominal tile area; adjust camera ortho scale independently to preserve artwork readability.
- Main bowl outer footprint: radii approximately `(1.12×1.18, 1.30×1.18)` with a deliberately irregular perimeter. A slightly raised dry rim is physically connected to the inner wall.
- Inner lip and depression: layered rings reduce from outer radius to center; rim peaks near Z=0.15, dark wet center near Z=-0.215. Surface is shallow and concave (not a deep quarry).
- Rough wooden poles: lengths and positions approximate the separate overlay, muted matte wood, not polished metal. The original active layer is one static frame; V1 may introduce slight deliberate paddle movement for the full-state animation pipeline, subject to user review.
- No specular sparkle: dry clay roughness ~0.98 and damp center roughness ~0.83; treat the dark center as wet by **color and slope**, not glossy mirror reflection.
- The archived 120px source contains two unused small bowl drawings suitable for **future geometry variants**; current main source is cropped to 64px. Neither reference justifies depicting three simultaneous pits in this asset.

## Execution and proof

From repository root: 

```bash
blender -b -t 4 --python-exit-code 1 --python models/island-survival/clay-pit/build_clay_pit_v1.py -- --out /tmp/clay-pit-v1 --samples 28
/usr/bin/python3 models/island-survival/clay-pit/make_clay_pit_review.py --out /tmp/clay-pit-v1 --mod tanks_for_bob_fork_1.8.95
```

One-click repeatable CI: `.github/workflows/clay-pit-greybox.yml`, which renders eight independent camera views (idle and working for all four orientations), validates actual RGBA output and differences, saves a native `.blend`, and publishes candidate proof to `models/island-survival/clay-pit/generated-v1/`. The in-chat preview must be shown to the user; source/working/reference files are included in the QA output. CI passing does not grant art acceptance or authorize replacing active game graphics.

## Next acceptance milestones

1. Confirm **one dominant wet-clay bowl** is recognizable at actual 64px scale, matching the sprite *concept* without overbuilding.
2. Verify active primitive props: location, angle, palette, and where they overlap the basin.
3. Once appearance is accepted, author an actual 16-frame loop with no popping/obvious tile seams and run the reusable production entrypoint with `idle` and `working` states, all four orientations, versioned 64/128/256px atlases.
4. Attach only to the exact `assembling-machine/clay-pit` target and update icon/prototype after Factorio 2.1 load tests. Preserve original graphics and validated C-block fluid input/output gameplay fields.

The intended purpose of the V1 blockout is **physical source reconstruction and primitive kit establishment**, not invisible mechanical simulation. All visible mesh/mat work must be shown as actual renders, not assertions or download-only links.
