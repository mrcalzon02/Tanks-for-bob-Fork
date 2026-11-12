# Beach Pump V1 — full verified Blender art-candidate export

**Real production run:** [Core30 #43262584206](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43262584206), Blender **5.2.3 LTS**. This native run **passed** its own source preflight, 68 genuine Cycles PNG render hashes (4 idle + 64 working), separate saved .blend native reopening, fixed south FMPL full-bore collar and mesh checks, 16-pose 8 FPS/97 loop, four-cardinal 64px proof and six SHA-verified atlas files.

- Native full-source Blender .blend SHA256: `022ff8b827f326bb351515b5180be06527a6c7daf5028d9b24fb3fdcab084ee0`.
- Full native Blender source, all 68 individual frames, six atlases and receipts are saved separately on OLD-CORE30-homebrew under `_homebrew/reports/beach-pump-v1-full-43262584206-1` with verified copies. They were *not* uploaded to GitHub Actions artifact storage because the account's artifact quota is exhausted.
- This folder contains the **genuine** four-way contact PNG, complete native build/QA reports and **six actual PNG atlases** recovered from that pinned run as ordinary Git commits. Their source hashes and cell dimensions are in `candidate-atlas-qa.json`.
- The independently verified original editable V1 Blender .blend from the 8-view pilot is reproducible byte-for-byte from `../generated-v1/assemble_native.py` and the native source parts. The full run's own `.blend` has a different SHA and is retained on Core30; do not substitute one SHA for the other.
- No vanilla-graphics fallback removed, no Factorio 2.1 `OffshorePumpGraphicsSet` game-client schema or fluid connection tested in-game, no human visual approval, and no release published.

## Render output

- `idle-64.png`, `idle-128.png`, `idle-256.png`: four cardinal idle cells
- `working-64.png`, `working-128.png`, `working-256.png`: 8×8 atlases, 16 working frames for each cardinal direction, **8 fps**
- `review-four-directions.png`: genuine full Blender source contact and 64px readability comparisons

These are complete machine sprites, **not** overlay layers. They are *candidates*. Native gameplay and Factorio renderer/shoreline fit remain unchanged until separate engine visual approval.
