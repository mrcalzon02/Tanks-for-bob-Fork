# Beach Pump V2 — genuine native Blender 68-frame production

**Production PASS — game installation pending separate visual/engine acceptance.** Source: [Core30 single-job Blender 5.2.3 run #43293980849](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43293980849), successfully independently reopened and SHA-verified. [Original builder + tests](../v2/).

## Directly viewable on GitHub

- [Genuine Blender four-way contact proof](review-four-directions.png) (four idle, four working views and 64-pixel previews); SHA256 `69ab1b8bf535c15e7e5da32612efd94c2321b145ecb40e7ab07d161b6deb9692`.
- [64px idle atlas](idle-64.png), [64px working atlas](working-64.png), [128px idle atlas](idle-128.png), [256px idle atlas](idle-256.png).
- Source receipts: [full 68-render manifest](build-report.json), [independent native Blender QA](native-reopen-qa.json), [four-way proof QA](proof-qa.json), [six atlas QA](candidate-atlas-qa.json).

## Reassemble original unmodified native binaries

```sh
python3 models/island-survival/beach-pump/generated-v2-full/assemble_assets.py
python3 models/island-survival/beach-pump/generated-v2-full/assemble_assets.py --verify-only
```

GitHub's binary upload request-size limit required the **actual immutable binary bytes** of the editable .blend master and the two largest working atlases to be split into Git blobs. `assemble_assets.py` joins the original parts, verifies sizes and complete SHA256, then atomically emits the full files without overwriting anything.

| Original file | Bytes | Git parts | SHA256 |
|---|---:|---:|---|
| `beach-pump-v2.blend` | 3,399,312 | 19 | `77e212ecd01df4e1795e19bb1bb81c207917b1ac248420c4777a86f5b3924bf9` |
| `working-128.png` | 345,371 | 2 | `6610fab65021c423d9bfd265435b40ea18639765a402ea6dc2b21ee0595d93fe` |
| `working-256.png` | 1,179,754 | 7 | `da22edade7abe0fb421bb47400954ead9e36a03a494f23bfdc3cefeea8fe3d65` |

This is **not** a sprite-only recreation or image generation. Independent Blender reopened the native model with its editable 580-vertex three-turn screw, genuine eight-paddle waterwheel and large crank, fixed south pipe fittings (256 vertices each), identical frame 1/97 pose and one stationary 45-degree camera. Four idle plus 64 working RGBA Cycles PNG frames were rendered at 8 FPS; all individual raw frames also remain saved on the authorized Core30 runner under the `beach-pump-v2-43293980849-1/native-full` persistent evidence directory.

Factorio direction order: **north / east / south / west** with original Blender indices `0,3,2,1`. Each working atlas is 8×8 cells (two rows per direction, 16 working poses per direction); idle atlas 4×1.

**Do not attach to live Factorio yet.** `offshore-pump/beachpump` still uses its old wooden graphics. The model is a candidate until owner visual inspection and a real Factorio 2.1 in-client shoreline/pipe-mouth check. Gameplay remains unchanged: native 1×1 offshore-pump, direct world-water suction at `(0,-1)`, one south pipe connection at `(0,+0.25)`, `0.01` water/tick, no fuel/power. Earlier V1 and V2 proof assets remain unmodified.
