# Fluid connection modeling reference

Use this reusable environment whenever a machine needs an attachment to the
project's standard Factorio pipe. Start with the existing reference joint and
build the machine's receiving box, collar, manifold or reducing neck around it.

## Canonical asset

- [Editable Blender reference](../../models/reference/factorio-fluid-interface/factorio-fluid-interface-reference.blend)
- [Reproducible generator](../../models/reference/factorio-fluid-interface/build_reference.py)
- [Optional append helper](../../models/reference/factorio-fluid-interface/append_reference.py)
- [Dimensions, object identities and verification receipt](../../models/reference/factorio-fluid-interface/reference-manifest.json)
- [Asset directory and usage notes](../../models/reference/factorio-fluid-interface/README.md)

Append the collection **`FACTORIO_FLUID_INTERFACE_REFERENCE`**. It contains the
reference pipe, machine-side mount guide, socket markers and one placement
root. Ground grid, camera and lights belong to the separate review environment;
they are not part of the appendable connection asset.

The Blender file is the reusable geometry authority. The manifest records its
dimensions and identities; this document explains how to place and use it.

## Fixed dimensions

**One Blender unit equals one Factorio tile.** These are this project's
boiler reference dimensions, reused by Cooking Fire V2.

| Measurement | Blender units / tiles |
|---|---:|
| Pipe barrel outside diameter | 0.57 |
| Pipe barrel outside radius | 0.285 |
| Open bore inside diameter | 0.49 |
| Open bore inside radius | 0.245 |
| Mounting collar outside diameter | 0.68 |
| Mounting collar outside radius | 0.34 |
| Collar axial thickness | 0.075 |
| Pipe centreline above ground | 0.36 |
| Adjacent pipe barrel length | 1.0 |

Keep these dimensions fixed when adapting a new machine. The machine-side
transition can widen, narrow or bend between the standard mount and its vessel
or pump housing. Preserve the accepted machine's visible geometry while adding
that transition and any necessary physical support.

## Local coordinate contract

The placement root, **`IFACE | ground placement root`**, is at **`(0, 0, 0)`**, on the ground directly beneath the
joint. Ground is Z0. The joint centre is **`(0, 0, 0.36)`**, its mating plane is
Y0, and the outward connection direction is **+Y**.

| Reference element | Local placement |
|---|---|
| Machine-side collar | Centre `(0, -0.0375, 0.36)`; spans Y−0.075 to Y0 |
| Adjacent pipe barrel | Centre `(0, 0.5, 0.36)`; spans Y0 to Y1 |
| Pipe's near collar | Centre `(0, 0.0375, 0.36)`; spans Y0 to Y0.075 |
| Pipe's far collar | Centre `(0, 0.9625, 0.36)`; spans Y0.925 to Y1 |

The machine collar's outer face and the pipe collar's near face meet at Y0.
Their open bores and centreline coincide; the mating face normals oppose each
other. Keep the root scale at **`(1, 1, 1)`** and preserve the children's local
transforms. Place the assembly by translating and rotating its root.

## Append and fit a machine

1. **Open the actual machine source.** Read its intended tile footprint and
   declared fluid connection position/direction from the current prototype.
   Establish the machine's ground origin and units before fitting the reference.
   Record any uniform placement calibration separately from mesh edits.
2. **Append the reference collection.** In Blender, use **File → Append**, open
   `factorio-fluid-interface-reference.blend`, enter **Collection**, and select
   `FACTORIO_FLUID_INTERFACE_REFERENCE`. Keep it as an editable local collection.
   For multiple ports, give each appended assembly a distinct name and role.
3. **Place the root at the joint's ground projection.** Translate the root in
   X/Y; leave its Z at ground height. Rotate the root to face outward. The socket
   marker then supplies the correct Z0.36 centreline automatically. Do not place
   the ground root at the socket's height and accidentally add that height twice.
4. **Build the receiving structure.** Fit the machine's pump box, manifold or
   reducing neck to the mount guide. A reusable copy of the machine-side collar
   can become an authored machine part: move that copy into the machine's own
   collection, preserving the original reference geometry for comparison.
   Retain the full-size opening at the external joint. Add only visible,
   supported geometry needed to join it to the machine.
5. **Inspect the actual seam.** Compare the annular mating faces, bore, height
   and direction. Use the reference pipe as the ruler rather than resizing it to
   make an existing small fitting appear to match. Check clearance in open and
   moving poses where the machine has animation.
6. **Capture four views and preserve the source.** Use the fixed 45-degree
   orthographic camera. Show the adjacent pipe for interface review, then hide
   the reference pipe, guide meshes, markers and environmental grid for the
   production asset capture. Save and reopen the resulting native file.

### Direction mapping

Blender +Y maps to Factorio north, which is native −Y. Blender +X maps to native
east. Native ground coordinates `(x, y)` therefore map to Blender `(x, -y)`.

| Native facing | Root rotation around Blender Z | Blender outward direction |
|---|---:|---|
| North | 0° | +Y |
| East | −90° / 270° | +X |
| South | 180° | −Y |
| West | 90° | −X |

### Pipe cell, mating plane and adjacent cell are different locations

For a conventional edge connection on an axis-aligned W×H footprint, the ground
boundary is at X±W/2 or Y±H/2. The edge pipe-cell centre is half a tile inside
that boundary; the adjacent pipe centre is half a tile outside it. Use the
prototype's actual declared position and facing, especially for irregular
footprints or nonstandard interfaces. Collision boxes and sprite bounds alone
do not establish a fluid connection.

| Example | Native pipe-cell centre | Native ground joint | Native adjacent pipe centre | Blender root location | Root yaw |
|---|---|---|---|---|---:|
| 3×3 Cooking Fire, north | `(0, -1)` | `(0, -1.5)` | `(0, -2)` | `(0, 1.5, 0)` | 0° |
| 2×2 boiler, east rear row | `(0.5, -0.5)` | `(1, -0.5)` | `(1.5, -0.5)` | `(1, 0.5, 0)` | −90° |

For the Cooking Fire example, the socket centre becomes `(0, 1.5, 0.36)` and
the reference barrel spans Y1.5 to Y2.5. This is the same reference assembly
translated to a different machine boundary.

## Verification and export handoff

Record the following with each machine's source and captured evidence:

- **Authority:** exact machine source revision and reference asset/manifest.
- **Placement:** tile scale, ground origin, native pipe cell and facing, reference
  root transform, socket centre and outward normal.
- **Model fit:** matching bore/collar dimensions, coincident mating faces and
  visible support. The 64-segment annuli provide 128 outer/inner face vertices;
  the existing fit check uses a maximum positional residual of `0.000001` tile.
- **Visual evidence:** actual 45-degree captures in all four directions,
  including a view in which each joint is visible. Record any natural occlusion
  rather than treating a hidden seam as visual proof.
- **Source integrity:** save/reopen result, retained geometry/material evidence
  and any model-specific motion/interface checks that were actually performed.
- **Production separation:** final machine graphics contain the machine's
  authored fitting; the adjacent reference pipe and review environment are
  excluded. Follow [SPRITE_EXPORT.md](../../tools/art/SPRITE_EXPORT.md) for the
  existing static/animated and standard/HR export process.

**Model fit and native sprite placement are separate results.** When integrating
the machine, measure its own projected mouth position and sprite scale/shift,
then inspect the real connected and disconnected pipe views in Factorio. The
boiler's final draw offsets were fitted to its particular two-mouth layout;
they are not a general offset preset for other machines. Record any native
placement work still outstanding without weakening the verified model fit.

## Provenance

- [Boiler V05 dimensional record](https://github.com/mrcalzon02/Tech-Priests/blob/0ea7ed22d508fb2f5c7d71102679b0be80a379ab/art/source-to-3d/boiler-v05/README.md)
- [Boiler V05 reference-pipe and collar constructor](https://github.com/mrcalzon02/Tech-Priests/blob/0ea7ed22d508fb2f5c7d71102679b0be80a379ab/art/source-to-3d/boiler-v05/build_boiler_v05.py)
- [Boiler's native four-direction visual registration](https://github.com/mrcalzon02/Tech-Priests/blob/0ea7ed22d508fb2f5c7d71102679b0be80a379ab/docs/art/boiler-v08-visual-alignment/visual-registration-validation.json)
- [Cooking Fire V2 implementation and reference-pipe proof](https://github.com/mrcalzon02/Tanks-for-bob-Fork/tree/807d024e74507d60fbdc04d17cd4738a02eaf225/models/island-survival/cooking-fire/v2)

Keep this shared reference independent of any one machine. Extend or revise the
canonical asset deliberately, with a new manifest and visible dimensional
comparison, so later models can identify exactly which standard they used.
