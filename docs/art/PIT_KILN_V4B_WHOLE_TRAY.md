# Pit Kiln V4b — THE ENTIRE TRAY of four wet bricks rocks together

The V4 version accidentally animated the four individual wet bricks independently while leaving the supporting wooden slab static. That was not the requested behavior.

The V4b correction creates **one named Blender parent control**, `V4b | COMPLETE TRAY AND FOUR BRICKS | rock together`, at the center of the wooden board. It parents the rough wooden slab and **all four wet bricks** under that single control while preserving each component's original world transform. It inserts 17 consistent two-second keyframes at source timeline frames 1,7,...91 and a matching seam key at 97. No individual brick carries an independent wobble action.

The entire tray now rocks as one rigid unit: modest roll (~4.4°), pitch (~5.3°), yaw (~3.2°), and slight smooth lateral/bobbing movement. The ten inner firing-bank bricks stay fixed. The six original Campfire V9 flame meshes/actions, the V3b original hand-authored motion, and the V4 crackle parent controls, ember sparks and flickering light are preserved.

**Release-blocking visual geometry check:** for each of four directions, calculate camera-projected displacement (at 256px) of actual geometric corners of the plank and each of the four bricks between opposite swing poses (timeline frames 1 and 49). All five objects must move at least 2px. This tests solid object motion independently from flickering fire. Blender reopening also asserts the five components have the same parent and no independent brick actions.

Output: four idle frames and four sets of 16 burning frames, 256px transparent, a source .blend, four previews, integrity reports. The V4 source/renders and live Factorio prototypes remain untouched. A new directory `generated-v4b/` is published after validation.

Source script: `models/island-survival/pit-kiln/v4b/build_pit_kiln_v4b.py`. Workflow: `.github/workflows/pit-kiln-v4b.yml`.
