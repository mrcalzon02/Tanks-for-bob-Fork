# Clay Pit V4c: bucket movement visible at sprite scale

The user correctly observed that the V4b bucket appeared stationary. Pixel audit of real 256px native Blender frames found only about 10.25px total travel north, 7.05px east, 8.98px south, and 8.5px west. At 64px game scale this is only 1.8 to 2.6px. The previous test compared whole frames, so lantern flicker could pass even when the bucket hardly moved.

V4c keeps V4b geometry, softly feathered dark clay materials, tiny wax-paper lantern, 2.4-unit local point light and original 45-degree orthographic camera. It changes only the pendulum range from +/-6 degrees to +/-15 degrees. The motion remains cosine-eased over 16 frames (source timeline 1,7,13,...91, seam key 97). Rope, bucket, water and hoop geometry remain parented to one pivot; lantern support and shovel remain still.

A new quantitative QA gate isolates the BLUE WATER in the bucket and tracks its centroid in each of the 16 RGBA Blender frames for EACH of the four directions. It requires at least 14px extreme-to-extreme movement at 256px (3.5px at 64px), and checks loop seam. This is movement of the actual bucket, not a whole-frame difference caused by lighting. Any direction below that threshold fails the build.

Run Blender against the unchanged generated-v3 clay-pit-v3.blend, with models/island-survival/clay-pit/v4c/build_clay_pit_v4c.py, output to a fresh directory. Run models/island-survival/clay-pit/v4c/make_v4c_review.py against that directory. GitHub Actions workflow clay-pit-v4c.yml performs native render, precise pixel QA, independent saved-master reopen and publication to a NEW generated-v4c directory. All earlier models, original sprites and game prototypes are preserved; V4c remains a visual-review candidate.
