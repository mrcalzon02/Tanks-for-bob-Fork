# Native editable Beach Pump V1 — exact byte reconstruction

The trusted Core30 native Blender 5.2.3 build and separate reopen verification
produced a **3,360,030-byte native file** with SHA256
`aed52dad68e16f40d626e713c525081ce77eb93210fc622e8cfa55ddecb5428d`.

Because the GitHub Actions artifact quota was exhausted and the GitHub binary
connector cannot upload a 3.36 MB file in one request, the **unchanged** master
is versioned here as 12 binary parts, with exactly 300,000 bytes each except
the final 60,030-byte part. This is byte-preserving packaging, **not** a
re-created, AI-rendered, or approximate model. The source and proof were
extracted by the authorized Core30 GitHub runner after SHA256 readback.

To recreate the real editable file in this folder:

```bash
python models/island-survival/beach-pump/generated-v1/assemble_native.py
```

Output: `models/island-survival/beach-pump/generated-v1/beach-pump-v1.blend`.
The assembler refuses to overwrite, checks all 12 part sizes and the exact
final SHA256, then completes atomically. Source parts are kept for provenance.

Genuine screenshot proof is `review-four-directions.png`; native and art QA
receipts are in this same directory. **Game graphics are not yet replaced**.
