# Beach Pump V4 — genuine Blender four-direction animation proof

**Actual native Blender 5.2.3 production PASS**: [Core30 run 43305148603](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43305148603). Source pinned to commit `2319edc1d1037af0a12b62e9292871bca74289be`.

- [Four-way real Blender visual proof](review-four-directions.png) — four idle and four working views.
- [True 16-frame 8 FPS Blender animation](motion-review.gif) — motion visible from all four directions.
- [64px working atlas](working-64.png) and [64px idle atlas](idle-64.png) — real game-scale readability check.
- [Native Blender independent reopen receipt](native-reopen-qa.json), [full 68-render report](build-report.json), [render QA hashes](proof-qa.json).
- [V4 editable Python source](../v4/) and complete V1–V3 donor chain.

## Reconstruct *original* editable native Blender master

10 exact Git binary parts preserve the actual production `beach-pump-v4.blend` master, not a reconstructed approximation. The original is **3,443,478 bytes**, SHA256 `ee5887f02b9fca9b4c8ac0046384280ee2f7fbaf9eb638a5f2aa2efc9a06f210`.

From a cloned repository:

```sh
python3 models/island-survival/beach-pump/generated-v4-review/assemble_native.py
```

The assembly script validates every part's Git blob SHA-1, expected part lengths, combined length and full Blender SHA256, refusing to overwrite an existing mismatched file. Use `--verify-only` to check bytes without writing.

This is a candidate-only native Blender asset. **Human visual acceptance and Factorio in-client connection testing remain outstanding.** Preserve original 1×1 shoreline pump, north intake, stationary south pipe at (0,+0.25), 0.01 water/tick and original game assets; no game sprite replacement.
