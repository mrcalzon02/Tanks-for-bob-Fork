# Steam Lumberyard V2b — visible powertrain refinement

V2b reopens the actual V2 Blender model rather than generating a second scene.
Preserves the six round bark logs, six D-profile split half logs, the crude
Franklin-style firebox/pressure boiler, steam-cylinder body, flywheel, continuous
leather belt, rotating circular saw, feeding hero log, two cut halves and their
ejection frames, and all four fixed-camera 45-degree orientations.

Refinement: add a real visible reciprocating bronze piston slider and
connecting crank rod. The crank rod follows the spinning engine flywheel using
17 keyed poses synchronized with the existing 16-frame/8fps fire and belt loop.
Widen/lighten the existing leather belt slightly and increase the exposed blade
tooth silhouette for native Factorio 64px readability. Keep the identity of
the mechanism: boiler heat -> reciprocating steam engine -> spinning flywheel ->
moving continuous leather belt -> saw spindle/blade -> longitudinal log cut ->
two halves ejected onto finished stack.

No change to the live `assembling-machine/growing-plot` gameplay/prototype.
The earlier V2 source stays preserved as a rollback. Publish exact 68 RGBA
renders, all four animated GIF previews and independently reopened .blend to
`models/island-survival/lumberyard/generated-v2b/`.
