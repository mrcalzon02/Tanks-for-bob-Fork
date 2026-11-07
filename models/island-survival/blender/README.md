# Campfire — Native Blender scene and animation

The executable static/animated sprite capture and atlas process is now [documented here](../../../tools/art/SPRITE_EXPORT.md). See `production-v10/` for locally verified full-state atlases, editable master and QA evidence; V10's matte-stone correction is still awaiting visual acceptance. The [5855 recovery audit](../../../docs/art/CAMPFIRE_5855_RECOVERY_AUDIT.md) records what the prior work did and did not commit.

The source of truth for editing and animation is a native Blender scene, **not** a flattened OBJ render. The Blender scene build reconstructs the V6 6,763-vertex/12,152-triangle geometry deterministically from the tracked V4 generator, then creates distinct Blender objects by physical group with material nodes, tangent-space image **Normal Map** nodes, camera, lighting rig, and fire animations.

## Scene structure and controls

- **01 | Stones + ash + coals:** 15 individual stones, ash and charcoal objects.
- **02 | Firewood:** six crossing logs and kindling pieces, split cut-end material regions, editable as separate Blender objects.
- **03 | Animated fire tongues:** six individual fire meshes keyed over 96 frames. Hide this collection for the unlit/idle state.
- **04 | Factorio lighting rig:** stable broad warm upper-left key, low-intensity cool fill, rear edge/rim, and a distinct flickering orange fire point light.
- **05 | Camera + controls:** orthographic Factorio-view camera, user-facing instructions in `CAMPFIRE CONTROLS` object's custom properties.
- **06 | Ground shadow catcher:** maintains grounded contact in renders while allowing transparent PNG output.

## Lighting and material policies

1. The daylight lighting rig is **stable**, so idle/burning comparisons remain valid. A broad warm key dominates; restrained cool fill and rear edge light prevent the rocks from disappearing. Fire light is separately animated; do not keyframe the daylight rig merely to create flicker.
2. Cycles physically computes ambient occlusion and cast shadows; avoid arbitrary bright ambient fill, flat unlit surfaces, and glowy stone materials.
3. All five material families (stone, bark, exposed endgrain, ash, charcoal) have separate **albedo**, **roughness** and **tangent-space normal map** images generated **within Blender**, packed into the `.blend`. Normal maps are connected as `Image Texture (Non-Color) → Normal Map → Principled BSDF Normal`. Roughness maps are Non-Color as well. Texture and node intensity are editable in Material Properties / Shader Editor.
4. Camera stays orthographic and consistent across renders, with native **64 × 64** study output. The reference sprite remains the visual target, not proof of achieved equivalence.
5. Geometry includes only visible elements. Stones and timber remain animated fire's independent stationary surroundings.

## Rebuild (Blender 3.6+)

From repository root:

```bash
python3 models/island-survival/blender/rebuild_campfire_v6.py \
  --v4 models/island-survival/refined/build_campfire_v4.py --out /tmp/campfire-v6

blender -b -t 4 --python models/island-survival/blender/build_campfire_scene.py -- \
  --obj /tmp/campfire-v6/campfire-smoothed-v6.obj \
  --out models/island-survival/blender/generated \
  --resolution 512 --samples 24
```

Outputs: `generated/campfire-v7-animated.blend`, idle and active PNGs, a 64px preview, and a test report. The native `.blend` includes packed textures and keyframed flames; you can scrub frames 1–96 or render animation in Blender directly. The source scripts also support reuse of a V6 OBJ source for further custom edits.

The dedicated GitHub Actions workflow may regenerate and publish the Blender scene without changing game sprites, technology, recipes, or the one-job runtime testing workflow. The workflow is scoped to this 3D asset; **no new in-game sprite is deployed automatically**.

## Provenance

Original procedural geometry and materials in the Blender build; no other mod's texture/sprite or Wube's base-game artwork is copied into the scene. Rendering references and potential permissively licensed alternatives are acknowledged in `docs/art/UNUSED_RENDERS_WORKFLOW_AND_CREDITS.md` and `docs/art/FACTORIO_GRAPHICS_SOURCE_REFERENCES.md`. When any specific third-party image is actually incorporated later, record exact author/file/URL/license and any adaptations before distribution. The MIT/CC/GPL status of one source must never be generalized to Snouz's entire mixed-license catalog.

## Production render and Factorio export (separate approval)

Execute [FACTORIO-SPRITE-PRODUCTION-v1](../../../docs/art/FACTORIO_PRODUCTION_SPRITE_WORKFLOW.md) using the [campfire production work order](CAMPFIRE_PRODUCTION_EXPORT_CHECKLIST.md). The existing Blender workflow creates editable development renders and a GIF; it does **not** yet verify the 4.5 LTS community preset, calibrated HDRI/sun camera, engine-ready frame layout, overlay masks, generated prototype Lua or real game behavior. Preserve active sprites until the checklist's integration gates pass.
