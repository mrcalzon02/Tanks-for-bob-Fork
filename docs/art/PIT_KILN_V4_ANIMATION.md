# Pit Kiln V4 — wet-brick wobble and original campfire crackle

The V4 source builds on the saved V3b native Blender kiln. It preserves the six
actual Campfire V9 keyframed flame meshes, their original animation actions,
the original keyed campfire light, all ten unmoving firing-bank bricks, and
the four loose wet bricks on the little wooden slab.

- Staged bricks independently wobble about 2.3–3.9° and gently tilt; board stays still.
- Six identity-parent crackle controls overlay the real campfire animations;
  none of the original campfire flame meshes, actions or materials is replaced.
- Two tiny keyed ember sparks and a low-intensity additional warm light suggest crackle.
- 16 frames at 8 FPS in all four real model orientations under the fixed 45° camera.
- 68 original RGBA renders, four GIF previews, SHA checks, and a native .blend reopen.
- Old V3b, original 2.1 game sprite and Factorio prototype remain unchanged.

Run using the single GitHub Actions workflow `.github/workflows/pit-kiln-v4.yml`.
Output is committed to `models/island-survival/pit-kiln/generated-v4/` only
after Blender, capture, image, and native keyframe checks pass.
Visual review is still required before live Factorio replacement.
