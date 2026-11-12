# Beach Pump V2 — actual editable native Blender master

Core30 [native run 43287477872](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43287477872) built and independently reopened a genuine **Blender 5.2.3** model featuring an inclined 3-turn editable Archimedes screw, open wooden discharge trough, eight-paddle wheel, **oversized wheel crank**, coupled rotation and animated water.

Blender master `beach-pump-v2.blend`: **3,399,311 bytes**, SHA256 `ee9c9ba560f8b28a580c7307e642f1f6c420627a3165131a0c4f6b53987d0646`.

Because GitHub Actions artifact storage was exhausted, the *exact unchanged native Blender source bytes* are versioned as 12 Git blob parts (eleven 300,000-byte parts and a final 99311-byte part). This is **not** a sprite reconstruction or generated substitute. Reassemble locally from repository root:

```bash
python3 models/island-survival/beach-pump/generated-v2/assemble_native.py
```

The assembler refuses overwrites, validates all part sizes and checks the **entire rebuilt Blender SHA256** before atomically completing. The actual file can then be opened in Blender as an editable scene. The separate `review-four-directions.png` is real Blender proof and `native-reopen-qa.json` is the independent Blender 5.2.3 re-open certificate. Original V1 and game assets are untouched.

All production gameplay invariants remain: direct world water extraction, 0.01 fluid/tick, one south output, no power. User visual acceptance and game-client acceptance remain distinct from native modeling proof.
