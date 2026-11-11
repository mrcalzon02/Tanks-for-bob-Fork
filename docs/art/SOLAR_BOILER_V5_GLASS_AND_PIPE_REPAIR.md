# Solar Boiler V5 — Glass boiling accumulator and timber pipe-socket correction

**Production source:** `bbddbdbd940bef49ad82a2b4c299b20f3745aca3`
**Blender job:** https://github.com/mrcalzon02/Tanks-for-bob-Fork/actions/runs/42943111518

## Accepted geometry inherited without destructive editing

The V4 wooden boiler pressure vessel is **not** reverted to copper. Preserve
18 bowed timber staves, 65 wooden conduit planks, 2 polished-wood parabolic
reflectors, 9 packed ferrocrete maps and the authentic packed Campfire V8
wood-material family. The original 3×2 occupancy, one 45-degree orthographic
camera and all three metal native boiler fluid interfaces remain unchanged.

## New construction in this V5 candidate

A supported **separate handblown-style hollow glass accumulator tube** sits
above the wooden barrel. Its refraction/transparent procedural shader is
deliberately a new editable candidate, not falsely claimed as an imported
approved FMPL glass library file; the wood/ferrocrete inputs remain pinned to
their previously verified sources.

Inside the glass are a separately modeled filled liquid body, moving
meniscus with three keyed deformation channels, animated waterline foam and
22 true 3D rising bubbles. The liquid and interior are clear enough to
distinguish idle from boiling at Factorio scale.

Each glass end has a perforated end membrane, small bronze seam/vent ring
and six staggered volume-noise-feathered steam lobes. Working-state vents are
**intermittent and asymmetric**, seven sampled frames per side; there is no
artificial vapor from a closed Factorio pipe connection. The historical
twelve V4 roof plumes are render-hidden but remain in the source.

The previous barrel end-cap builder left a gap above both large side-pipe
join points. V5 adds a fitted wooden annular patch at each end, clipped to
the barrel outline and preserving a **0.132-tile radius open bore** at the
true conduit. This physically closes the visible timber roof holes without
putting a flat board across the water line.

## Source, render and native QA

- Editable native: `models/island-survival/solar-boiler/generated-v5/solar-boiler-v5.blend`
- Source builder/independent verifier: `models/island-survival/solar-boiler/v5/`
- Four-direction idle/working contact: `generated-v5/review-four-directions.png`
- Genuine 16-frame animated north cycle: `generated-v5/working-north-boiling-and-venting.gif`
- Native test: `generated-v5/native-reopen-qa.json`
- Cycles image test: `generated-v5/proof-qa.json`

The native test reopened the exact saved 3D source and checked all 18 wooden
staves, 65 wooden pipe planks, 2 parabolas, both gap repairs, the real glass
wall, true fluid volume, shape keys, 22 bubbles, 12 vent wisps, 3 original
adjacent-mating boiler fluid ports and 1 unchanged camera.

The Cycles proof contains **24 actual model renders** (4 idle, 4 working,
16 working north) plus **4 same-frame liquid/steam isolation images**.
At 64px its changed RGB pixel counts were **28 fluid** and **13 steam**,
above the gated minima of 3 and 2. This is technically verified motion,
**not** owner visual acceptance.

The source before V5 was retained unchanged; no new GitHub workflow was
created. The bounded one-shot push trigger is retired after publication.
The active Factorio 2.1 prototype was not altered. Remaining gates are:
human visual review, 16-frame capture for east/south/west and native Factorio
sprite registration/pipe-connection smoke once specifically accepted.
