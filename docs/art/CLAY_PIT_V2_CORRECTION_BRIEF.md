# Clay Pit V2 — source-faithful props and wet-earth material correction

Status: **V2 MODEL AND TEXTURE CANDIDATE ONLY**. Do not install as the game's sprite before user approval. Retain V1 and all original game sprites unchanged.

## Authority: user clarification (2026-11-06 Sitka)

The small warm object sitting **on the tip of the supporting stick** is a lantern with a **wooden frame and wax-paper sides**. A **rope dangles from the support over the pit** to an **open wooden bucket filled with water**, suspended low inside the basin. The large object projecting into the side of the pit is a **shovel**, not a generic rod or random plate. These functional identities override the speculative "scoop" and "weight" wording in the V1 work order.

The current source entity still renders only **one excavated clay pit** at a time. Existing `clay-pit.png` may contain spare smaller basin sketches outside the current 64px crop, but they are **not** extra game-world pits. V2 does not add them.

## V2 structure reconstruction

- **Ground and pit:** One asymmetrical, shallow depression, rich ochre rim, sloped damp walls, broader and darkened near-side wet interior. Keep the same 3×3-ish placement footprint; no invented industrial machine.
- **Lantern:** Small hand-built square wooden frame, wax-paper enclosure, warm interior, perched *on the support pole tip*. It must not look like a big metal lantern or a hanging weight.
- **Rope:** Thin fiber cord from the short lifting arm; no disconnected dangling bits.
- **Bucket:** Physically modeled, open, tapered wooden-stave bucket, water visible just below its rim; two fiber hoops and tied handle points. It hangs close to the muddy floor, not outside the pit.
- **Shovel:** One proper long wooden shaft with a wide flattened spade blade crossing the left lip into the pit. No random extra cylinders.
- **Materials:** Procedural three-tone clay pigment variation, rough non-reflective dry rim, darker high-roughness wet clay, subtle surface bump. Avoid polished stone-like shimmer or an isolated tiny black dot.
- **Camera:** Fixed Factorio 45° orthographic structure profile. Actual 0°, 90°, 180°, 270° model rotations under the same camera and lights. V2 records true 256px transparent RGBA captures.
- **Working states:** Frame 0 hides tools, frame 13 shows them. Source game's working overlay is static. Do not invent complex mechanical cycles or claim a looping 16-frame animation has been accepted.

## Commands and output

From repository root with Blender/Pillow:

```sh
blender -b -t 4 --python-exit-code 1 --python models/island-survival/clay-pit/v2/build_clay_pit_v2.py -- --out /tmp/clay-pit-model-v2 --samples 28
/usr/bin/python3 models/island-survival/clay-pit/v2/make_v2_review.py --out /tmp/clay-pit-model-v2 --mod tanks_for_bob_fork_1.8.95 --v1 models/island-survival/clay-pit/generated-v1/working-d00.png
```

Workflow: `.github/workflows/clay-pit-v2.yml`. It validates the 8 true native Blender views, independent `.blend` reopen, non-empty alpha and clipping, source comparisons, then publishes to `models/island-survival/clay-pit/generated-v2/` with GitHub remote readback. This is a candidate for visual review, not authorization to deploy to `assembling-machine/clay-pit` yet. A later explicitly approved production run should use the reusable Factorio exporter and existing correct fluid input/output prototype; it must preserve the original rollback sprites.
