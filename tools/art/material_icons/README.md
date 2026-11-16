# Modeled inventory icons

`assets.json` is the per-prototype construction/selection registry. The editable selected `.blend`, unchanged runtime `.glb`, packed maps, source/export comparison renders and capture receipts are in `art/source-to-3d/material-icons/<revision>/<asset>/`. Rejected earlier revisions remain preserved. The active runtime icon bindings are in `prototypes/generated_graphics/material-icons-v01.lua` under the mod source directory.

The consumer uses the existing Tech Priests FMPL camera/export library. Material props use selected item pose C beneath the canonical 45-degree orthographic camera. The three reused factory models remain upright under the same optics. Use a local Tech-Priests checkout containing `tools/fmpl` and `tools/art/export_sprites.py` as `--pipeline-root`; the sibling permanent checkout supplies this in the current workspace. No network, model download or image-generation service is required to rebuild.

Example from this repository, substituting the local pipeline root:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.0/blender.exe' -b --factory-startup -t 4 --python-exit-code 1 --python tools/art/material_icons/build_models.py -- --pipeline-root ../Tech-Priests --assets ASSET-ID --revision v03
```

Existing selected folders are never silently overwritten. Update the registry revision only after reviewing a successful new export. `review_material_icon_exports.py` independently reopens the source and actual runtime export; `check_material_icon_fidelity.py` enforces the recorded color/silhouette limits. Capture with the existing FMPL exporter and the generated `capture-profile.json`. All textures are packed, so opening a selected source does not depend on these Python modules.

Current technical/assistant review is separate from owner visual acceptance. The icon pass changes inventory artwork only; gameplay and unit/weapon unlocks retain their native definitions.
