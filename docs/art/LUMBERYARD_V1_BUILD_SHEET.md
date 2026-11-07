# Primitive lumberyard V1 — actual Blender blockout and working animation

Intended eventual replacement of the old C-block `assembling-machine/growing-plot` visuals;
**the current mod prototype remains unchanged** pending visual approval.

The source tree sprite (187×310px idle and 751×310px four-frame leaf animation) is NOT
the desired model. This new structure replaces that graphic concept with a visibly
readable chain: INPUT pile of six complete bark-covered round logs → CENTER primitive
hand-operated splitting wedge mounted between thick wooden uprights → OUTPUT six
individual longitudinally split half trunks with pale, flat exposed wood faces.

Built as editable mesh components: irregular earthwork footprint; six full round
bark trunks with end caps, timber posts, diagonal braces, lifting head and wedge,
wooden cradle rails; one active hero trunk switching into two visibly separating
halves; six D-profile output split half-logs; scattered wood splinters.
The cutter uses a wedge, not a modern circular saw or industrial conveyor.
No leaf-covered trees, motors, power cables, factory walls, or hidden mechanisms.

Animation: 16-frame 8fps authored split cycle (wedge descends, trunk is actually
split lengthwise into two halves, they spread, chips jump, reset for next trunk).
Four actual model rotations under a fixed orthographic 45° structure camera,
256×256 transparent RGBA captures. Camera/lighting do not rotate.

Reproducible one-run workflow: `.github/workflows/lumberyard-v1.yml`.
Editable source, 4 idle views, 64 working frames, 4 preview GIFs, and QA saved at
`models/island-survival/lumberyard/generated-v1/`.
No Factorio mod or Mod Portal publication is authorized at this stage.
