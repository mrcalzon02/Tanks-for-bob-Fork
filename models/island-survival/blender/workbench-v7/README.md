# Workbench V7: striking-face correction

This continues the approved rough timber model. The animation rolls the hammer
90 degrees around its handle during pickup, so the end face of the head strikes
the plate. The six strikes, central sparks, heating, lay-down and cooling remain
an eight-second, cold-rest-to-cold-rest cycle. No model geometry is replaced.

## Reproduce

Extract `source.zip` to `source/`, then run from this directory:

```sh
blender -b --python-exit-code 1 --python workbench_v7.py -- --source-blend source/rough_timber_workbench_v4.blend --output-dir output --render all
```

`--render proof` renders the contact comparison and five representative poses.
`--render none` builds, validates, saves and reopens the editable scene without
rendering. The generator uses only Blender's included Python libraries.

The actual evaluated head and handle are checked for plate clearance through
all 192 timeline frames. Each of the six impacts is checked in all four views:
the head's local +Y face must point down, its face center must meet the sheet
center, and the geometry must stay above the plate. These checks run again
after reopening the saved `.blend`. They diagnose the animation; visual review
of the resulting renders remains necessary.

Game export: fixed 45-degree orthographic camera, north/east/south/west model
rotations, 96 frames at 12 fps, 128px transparent cells, 12 columns. Timeline
frames 2,4,...,192 include every actual impact and the fully cooled endpoint.
Full working frames replace idle frames; they are not an overlay. Standard
64px atlases are packed from the same rendered cells. Camera/light and source
hashes are recorded by the export.

## Source provenance

The approved V4 mesh and original V5 animation were recovered from
`mrcalzon02/Tech-Priests`, rather than rebuilt:

- V4 source: `art/source-to-3d/workbench-v4/rough_timber_workbench_v4_source.zip`
  at commit `0ea7ed22d508fb2f5c7d71102679b0be80a379ab`.
- Source ZIP SHA-256:
  `26f1402a2aa1920cdaaa8e8e15399250a86e6a6aa9bb9a00c832a76068d6c2cb`.
- V5 animation: commit `0251d186d82b5027dcaf81880237be35d4c980a2`.
- `build_workbench_v4.py` is the original generator retained with the source.

The V5 center-position assertion allowed the broad side of the head to make
contact. V7 checks the designated striking face, rather than merely its origin.
The target integration is Tanks-for-Bob's existing `workbench` entity.
