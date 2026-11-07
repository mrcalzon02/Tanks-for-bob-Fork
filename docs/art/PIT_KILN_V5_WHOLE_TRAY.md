# Pit Kiln V5 — ENTIRE wooden tray and brick pile wobble

The V4 error was that the four wet bricks each had their own small wobble, so the
visible effect resembled a single brick twitching while the wooden staging board
remained stationary. This V5 correction replaces **all four independent brick
actions** with one shared Blender empty parented to the existing model rotation
root. That empty parents five distinct editable objects: the rough-cut wooden
staging plank AND the four hand-formed damp bricks. All five now move rigidly
together, never independently.

Motion is a restrained ±7° rock with a slight ±0.04 Blender-unit transverse
translation, phased over 16 source frames (1,7,...91) with a matching seam key
at 97. The board, not merely a top brick, must visibly move. Only the firing
bank's ten bricks remain stationary. The central fire still uses the six
original animated Campfire V9 flames, V3b-authored refinements, V4 crackling
controls, two embers and V4 keyed light. No new fake fire replaces it.

V5 capture: 4 real idle + 64 real burning RGBA Blender renders under a fixed
45° structure camera with 0/90/180/270° model rotation, plus four GIF
previews. CI measures projected tray movement from the actual wooden board
mesh for each of the four directions and rejects a stationary tray regardless
of fire flicker; it independently reopens the native .blend to verify five
children under ONE keyed control and no remaining brick actions.

Run .github/workflows/pit-kiln-v5.yml. The output goes to
models/island-survival/pit-kiln/generated-v5/ and never overwrites V4.
No Factorio prototype/mod portal changes are part of this model work.
