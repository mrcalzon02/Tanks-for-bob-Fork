# Beach Pump V5 — genuine Cycles Blender proof and original native master

**Native Blender 5.2.3 production PASS:** [Core30 run 43362715067](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43362715067), source commit \`0eb9c93add4526042ae77090e8463185f52817c8\`.

- [Real four-facing contact proof](review-four-directions.png): four actual camera yaw facings, idle and working
- [Genuine 16-frame / 8 FPS animation](motion-review.gif): real linked wheel and screw motion
- [256px idle sprite candidate](idle-256.png), [64px running candidate](working-64.png)
- [Independent native Blender reopen QA](native-reopen-qa.json), [per-frame SHA256 build report](build-report.json), [render visual QA](proof-qa.json), [six-atlas packing QA](candidate-atlas-qa.json)
- [Editable V5 source builder](../v5/build_beach_pump_v5.py)

**Original Blender \`.blend\` master preserved exactly** as ten verified Git binary parts. Original native master length **3,501,567 bytes**, SHA256 \`a6f7c938835b98e2a24e4bac513627daccc83e6cd9d4c600e81b20c81eb93db1\`. Reconstruct with:

\`\`\`sh
python3 models/island-survival/beach-pump/generated-v5-review/assemble_native.py
\`\`\`

The assembler independently validates each Git blob, byte count and full Blender SHA256, refusing to overwrite conflicting files. \`--verify-only\` checks without writing.

**Review caveat:** V5 eliminated the previous disconnected blue water beads, but transparent-water readability through the glass remains a potential visual refinement. This is candidate-only. The mod's original shoreline intake, native south pipe port (0,+0.25), 1×1 footprint and 0.01 water/tick are unchanged. **Human visual approval and in-client integration are not claimed.**
