# Wood Basin V1 — native passive cistern

The actual Tanks machine is `storage-tank/wood-basin`, 3×3, capacity 25,000,
with four bidirectional corner sockets and `two_direction_only=true`. Its
building recipe uses 18 wood, 8 stone and one stone-tools in category Seablock;
Wood Basin technology follows Beach Pump. There are no processing recipes,
fuel inventory or power demand.

The saved source refines the tracked starter OBJ's floor and four corner
posts into the correct native size. Separate timber staves, restraint bands,
stone piers, a supported service hatch, sealed sight panels and hollow joined
corner manifolds explain storage and fluid access. Grain follows individual
pieces; cut ends, iron restraints, bronze fasteners and stone have separate
image surfaces. Earlier failed boolean/export studies remain preserved.

Source and runtime are in `models/island-survival/wood-basin/candidates/v1-production02/`.
The packed source reopens; the actual animated GLB reimports with 18 embedded
image maps, valid UVs, no degenerate triangles, six matching sampled poses and
stationary collars. Its front, rear, clay and corner inspection images were
viewed. The source has an editable filling/draining demonstration.

The native body uses one genuine static capture per facing. Four body views
and 64 genuine fill-preview renders are archived. The tank's real fluid amount
controls its native sight window; scrolling liquid and animated gas use the
existing engine fields. Production body captures use window holdouts, so
painted liquid never hides or substitutes for the actual tank contents. The
two native art orientations and four port rotations remain unchanged.

Factorio 2.1.24 verifies twelve tanks with water, oil and steam, 48 normal
player-grid pipe joints, full-capacity saturation through ordinary external
pumps, blocked/full storage, stopped flow, draining and refilling. The client
fixture separately seeds empty/half/full/drained/refill states for clean visual
comparisons; it does not substitute for those real transfer tests. Thirty-two
client screenshots show the states, and pixel checks prove contents-driven
level changes and changing flow texture at a stable full level in all four
views. A filled save reloads with fluid names, amounts, temperatures and all
connections preserved. The tested mod inputs match the active source by hash.

Review is delegated operational close-enough judgment, not individual owner
visual approval. No Mod Portal release or full user-pack installation is
claimed. `FMPL_MODEL.json`, the engine/capture receipts, saved fixture and raw
native/reload logs preserve these distinctions.
