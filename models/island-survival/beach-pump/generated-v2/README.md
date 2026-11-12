# Genuine Blender V2 source proof (not image generation)

- Core30 native run: [43287477872](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43287477872) — **successful**.
- Blender: 5.2.3, Cycles, one fixed 45° camera.
- Actual editable Blender V2 master SHA256:
  `ee9c9ba560f8b28a580c7307e642f1f6c420627a3165131a0c4f6b53987d0646`.
- Real render: 4 idle + 4 operating PNGs (north/east/south/west).
- Independent native reopen: **pass**, 580 real screw vertices; 8 waterwheel spokes and 8 buckets; large external rotating crank; 6 water pockets + 6 falling droplets; fixed 256-vertex collar and throat; exact 16-frame 8 FPS seam.
- Fluid behavior unchanged: `offshore-pump/beachpump`, shoreline world water intake, 0.01 water/tick, native south output `(0,+0.25)`, no electricity or fuel.
- The original V1 source and accepted assets remain unchanged.
- Actual Factorio in-world graphics, shoreline pipe overlap and human final art acceptance remain **pending**.

The true V2 contact render and raw QA receipts are committed here as ordinary
Git files. The editable native .blend is preserved independently on Core30.
Its byte-preserving Git source parts and SHA-checked assembler are published separately.
No Actions artifact upload was used.
