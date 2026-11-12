# Tanks Steam Condenser V1 — native 3×3 build candidate

This is the **next structure after completed Solar Boiler V8 gameplay integration**.
It is a new Tanks 3×3 machine, not a copy of the Tech-Priests 2×2 emergency condenser.

## Actual prototype constraints

- Current entity: `assembling-machine/steam-condenser`, 3×3 selection box.
- Native steam intake: north `(0,-1)`; native water output: south `(0,+1)`.
- Blender axes are X east / Y north / Z up, one world unit per tile.
- Two full-bore 0.57 OD / 0.49 bore / 0.68 collar reference interfaces
  come from the exact checked-in canonical `factorio-fluid-interface-v1`
  fixture; joint planes are `(0,+1.5,.36)` and `(0,-1.5,.36)`.
- One fixed Wube 45° orthographic camera; model rotates 0/90/180/270.
- No full concrete ground slab: four separate load-bearing footings.
- Packed ferrocrete PBR materials are imported from the **approved Solar V8
  native Blender**, itself using the user's pinned FMPL materials.
- The water/steam interfaces, pipe manifolds and barrel supports are static;
  only the fan, gauge, droplets and small intake mist move.
- 16-frame working loop at 8 FPS, loop return frame 97. Four idle states.

## Build on an existing Blender runner

```sh
python models/island-survival/steam-condenser/v1/build_steam_condenser_v1.py --self-check
blender -b --factory-startup --python-exit-code 1 \
  --python models/island-survival/steam-condenser/v1/build_steam_condenser_v1.py -- \
  --output models/island-survival/steam-condenser/generated-v1 --render proof --samples 16
```

The builder saves an editable native `.blend`, per-frame SHA256 hashes and
eight genuine four-direction Blender PNGs in a **new** directory. It rejects
modified donor bytes and refuses to overwrite existing output. Only after the
actual proof is inspected should `--render all` produce 68 frames for atlases.

**Not yet complete:** original sprite comparison, genuine rendering on Blender,
independent native file reopening, 64/128/256 atlases, Factorio integration,
human visual approval. These gates must not be claimed passed just because a
source-generation script or a manifest was committed. No live mod files,
gameplay values or existing GitHub workflows are changed by this stage.
