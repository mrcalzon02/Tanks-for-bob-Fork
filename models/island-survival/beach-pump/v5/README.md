# Beach Pump V5 — glass-housed Archimedes screw and genuine moving water

**Source status: Blender candidate; not integrated and not visually approved.**

V5 loads and retains the complete V4 construction chain without modifying it, then replaces the rejected disconnected water-blob geometry. The twelve old water pocket/drop meshes are removed. A stationary 14 mm-in-model-scale thick physically hollow tinted sea-glass jacket encloses the rotating three-turn brass Archimedes screw. Inside the housing a **single connected actual 3D seawater mesh** carries Blender 4D procedural noise with cyclic 16-keyframe animation. A continuous thin water sheet pours from the elevated gutter onto the waterwheel. Two hollow narrow metal bands hold the glass without opaque cuffs. Original eight cupped wooden buckets, oversized eccentric crank, shaft gearing, frame and native Factorio output ports remain as in V4.

The native offshore-pump prototype remains 1×1 tile, source offset (0,-1), south output (0,+0.25), rate 0.01 water/tick. Game graphics are **not** overwritten until visual approval.

Native production command:

```powershell
blender.exe -b -t 4 --factory-startup --python-exit-code 1 --python models/island-survival/beach-pump/v5/build_beach_pump_v5.py -- --out output/beach-pump-v5 --render all --samples 16
blender.exe -b output/beach-pump-v5/beach-pump-v5.blend --python-exit-code 1 --python models/island-survival/beach-pump/v5/verify_beach_pump_v5.py -- output/beach-pump-v5
python models/island-survival/beach-pump/v5/make_proof_sheet.py --out output/beach-pump-v5
python models/island-survival/beach-pump/v5/pack_verified_atlases.py --source output/beach-pump-v5 --out output/beach-pump-v5-atlases
```

Expected review artifacts: real four-facing eight-state contact sheet, authentic 16-frame animation GIF, 68 Cycles 256px RGBA render frames, six atlas candidates, native .blend and independent socket/kinematic QA. **Do not claim completed renders until the runner actually finishes.**
