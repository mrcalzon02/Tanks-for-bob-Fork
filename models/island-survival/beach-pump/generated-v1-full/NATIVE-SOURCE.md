# Exact full-animation Beach Pump V1 Blender source

The **real, independently reopened** Blender 5.2.3 full 68-frame master
is preserved in `native-blend-parts/` as 12 Git-native binary parts.
There are 11 parts of 300,000 bytes and one of 60,006 bytes. They reproduce
exactly **3,360,006 bytes**, SHA256
`022ff8b827f326bb351515b5180be06527a6c7daf5028d9b24fb3fdcab084ee0`.

From the repo root:

```bash
python models/island-survival/beach-pump/generated-v1-full/assemble_native.py
```

Output is the original `beach-pump-v1.blend` in this directory. The assembler
refuses to overwrite, validates all source-part lengths and final SHA256, and
does not regenerate geometry or render any image.

Original source: [Core30 run 43262584206](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43262584206)
(68 real Cycles PNGs; native saved-file reopen verified; six complete 64/128/256
frame-aligned atlases validated). GitHub Actions artifacts were blocked by
storage quota; the true model and complete atlases were preserved through
authorized Core30 source proof transfers instead.

The actual Factorio beachpump remains unchanged; `OffshorePumpGraphicsSet`
schema and client graphical pipe fit have not been approved.
