# Fish Pond V2 — finish the existing basin

Baseline: Tanks main `fbfc91c47504a4dedfe8b51bbfa1ba725298ee92`.
Source: `../generated-v1/fish-pond-v1.blend`, SHA-256
`0a7a738ddeba0f3675ce40724a20bf5acf1a0537e0bef085032cfc3d13100427`.
This is an unapproved candidate; V1 and installed graphics remain preserved.

## Contract and restrained refinement

- Actual prototype: `assembling-machine/fish-pond`, 3×3 tiles; chemical burner
  15 kW, crafting speed .60, category `fishery`. Preserve gameplay fields.
- Native north input and south output remain volume 1000. Their joint planes
  are Blender Y ±1.5, raised socket centres Z .36. Current fishery recipes use
  no fluids; `off_when_no_fluid_recipe` must remain true. Do not invent a water
  requirement or claim the dormant boxes currently process water.
- Retain the V4c-derived continuous excavated basin and loose earth. Add only
  supported continuous hollow ceramic walls with canonical full-bore mouth
  dimensions. Separate reference collar/throat meshes overlap internally, so
  the final model rebuilds their section into one wall, retaining the .003 arris.
- Keep four fish, existing editable tail shape keys and a 16-pose/two-second
  loop. Correct elliptical headings, separate their paths into a school, and
  add small eyes. Idle remains a filled pond without swimmers.

## Surface and capture plan

Preserve the source's dry ochre rim / dark damp floor transition and granular
clay, baking the actual procedural surfaces to a padded shared UV atlas.
Fish have species-specific backs, lighter bodies and separate darker fins;
eyes are small and dark. Fittings are fired clay, with roughness and subtle
surface grain. Bake base colour, roughness and tangent normal; pack all maps
in the editable source and actual GLB. Water uses a glTF-compatible Principled
alpha surface, rather than the source's nonportable Mix Shader.

Use the pinned FMPL camera authority already recorded for the pump. One fixed
45° orthographic camera; model rotations N0/E270/S180/W90. Unit-scale source
and GLB; derived sprite projection alone unforeshortens global Y by sqrt(2).
Four idle and 64 working PNGs; 64/128/256 atlases after pilot review.

## Gates

Contract/source, independently reopened source and GLB, UV/PBR channels,
97-pose export comparison, front/rear/close/clay review, 68 true frames and
six atlases: complete. Factorio 2.1.24 candidate and active-source tests passed,
including production, no fuel, stop/restart, blocked output, 55-second harvest,
test-only fluid transfer and save/reload. All four native pipe alignments were
viewed in actual client captures. Source and GLB stay at unit scale.

Owner accepted the concrete in-client comparison on 2026-11-15 and explicitly
requested integration; see `owner-disposition.json`. The active source is
promoted. Canonical FMPL registration and remote receipt are closed in the
final delivery record. See `docs/art/fish-pond-v2/README.md` for the evidence.

Bounded repairs: pilot 02 caught split per-object GLB clips and top-edge
clipping; pilot 03 combined the scene animation and corrected framing. Its
close view exposed coincident collar/throat bores from the reference templates.
Pilot 04 rebuilt one continuous wall per port and passed closed-manifold,
component, nominal-bore, mating-plane and stationary-socket checks. Earlier
studies are retained, not promoted. The native proof harness was updated for
2.1's recipe categories and crafter inventory API before the graphical run.
