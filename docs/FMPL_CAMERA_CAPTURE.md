# Factorio FMPL camera capture consumption

FMPL version 0.4.0 is pinned by the repository root fmpl-consumer.json.
For any NEW asset capture, use the canonical Tech-Priests capture authority
tools/fmpl/capture_policy.py and derived-scene camera guard. The model and its
source files remain in their project repositories. Do not add new workflows
or copy private/full-sized source Blender scenes into this repository.

Exactly one stationary, grid-aligned orthographic camera at 45 degrees.
- Entity: 4 rotations (0 / 90 / 180 / 270); the model rotates, camera fixed.
- Item: 1 canonical 45deg icon view, one frame only.
- Temporary inspection cameras: never persist in the saved derivative.
- Camera cleanup operates on derived exports only; keep source .blend intact.
- Never infer native Factorio port positioning from decorative geometry.

The legacy Tanks-for-bob-Fork exporter remains a separate implementation.
Do not describe its old profiles as camera-policy compliant without first
updating/validating their actual config with the canonical FMPL preflight.
