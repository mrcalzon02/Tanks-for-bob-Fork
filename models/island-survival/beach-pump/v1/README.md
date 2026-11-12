# Beach Pump V1 — shoreline wave-lift, not offshore-pump sprite reuse

This is an **original editable 3D model source** for the Tanks for Bob `offshore-pump/beachpump`, a slow starter water source. It does not substitute the live graphics until native Blender and official Factorio 2.1 graphical validation are complete.

## Measured game contract

The source prototype is deep-copied from Factorio's offshore pump and currently has a **vanilla-graphics fallback**, because the custom wooden offshore-pump PNG dimensions do not match the inherited sprite metadata.

- Game selection box is **X -0.6…+0.6, Y -1.49…+0.49**: shoreward-offset, elongated footprint. Its `tile_width` and `tile_height` are both 1; do **not** confuse them with the visual selection bounds.
- Native water output connection: **(0,+0.25), south**. Water intake source offset: **(0,-1)**. Blender Y runs opposite native Y.
- Therefore model the single full-bore **south outlet at Blender (0,-0.49,0.36)**, separate from its **native fluid box position at Blender Y=-0.25**. Keep both! The +Y shore-facing intake extends over the water-side end.
- The native one-tile barrel/collar/throat is appended from the SHA-pinned `factorio-fluid-interface-v1`. Only authored machine-side collar/throat geometry appears; all external reference pipes are discarded.
- No gameplay change: retain original void power, 0.01 pumping speed, offshore placement logic, collision box, water source and output connection.
- No large concrete pad. Four separate small pinned FMPL ferrocrete stilt feet; weathered timber dock slats, rope, intake cage, wet bucket/diaphragm chamber and copper outlet.

## Distinctive mechanism

A shoreline wave-actuated intake paddle rocks on an iron pin and lifts a timber rocker. The rocker moves a vertical leather-lined pumping diaphragm. A true connecting rod ties the rocker to its actuated head; an intake screen and moisture sight tube make the lifting process readable. Visible droplet motion and a pressure dial register flow. The rocker, scoop/paddle, link, diaphragm and droplets are the only animated parts; **the actual outlet flange and pipe remain fixed**.

One Wube-style 45° orthographic camera stays static while the model root rotates 0°, 90°, 180° and 270°. Save/reopen editable Blender, render 4 idle + 64 working Cycles PNGs (16 poses per view at 8 FPS, frame-97 seamless return), verify rigid full-bore geometry and source hashes, then generate 64/128/256 candidate atlases.

```sh
python models/island-survival/beach-pump/v1/build_beach_pump_v1.py --self-check
blender -b --factory-startup --python-exit-code 1 \
  --python models/island-survival/beach-pump/v1/build_beach_pump_v1.py -- \
  --out models/island-survival/beach-pump/generated-v1 --render proof --samples 16
```

`--render proof` saves an editable `.blend` and eight true Blender PNGs. `--render all` saves 68 frames. The independent native opener and proof contact generator are required before calling Blender production complete. No new workflow, unapproved art attachment, fabricated screenshot, or live mod prototype mutation.
