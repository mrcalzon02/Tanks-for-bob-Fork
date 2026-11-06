# Campfire V6 — smoothed procedural 3D art source

This pass increases visible shell geometry (15 stone shells, 22-sided timber cross sections), reduces abrupt per-face stone coloring, and preserves the original crossed-log and independent fire layout.

The original V5 model had 2,933 vertices and 4,995 triangles. The V6 **tested textured OBJ** has **6,763 vertices, 12,152 triangles, 36,456 UV corners and 7,009 vertex normals**. The texture package includes procedural stone, bark, cut wood, ash and charcoal **albedo, normal and roughness** maps. These are original generated images, not copied vanilla graphics or uncredited third-party textures.

Validated V6 textured OBJ SHA-256: `dccf8083aca631fcd3b2654fd8e1fc22f66cbc142ceeff882fd6e40c1b510eaa`.

The **geometry builder** is committed beside this note. Generate source geometry with:

```sh
python models/island-survival/refined/build_campfire_v6.py output-directory
```

The **full texture generator, smooth-normal UV OBJ, material maps, test renders and validator** have been delivered as a downloadable conversation artifact. They have not been included in this Git commit, so this commit is **not** claimed to contain the entire textured source package.

### Source references and rights

- Malcolm Riley — [Unused Renders](https://github.com/malcolmriley/unused-renders) (CC BY 4.0).
- snouz — [Factorio Free Graphics for Modders](https://github.com/snouz/factorio_free_graphics_for_modders). A **mixed-license index** only, not blanket permission to import. Check each original author's license; some assets are Wube EULA, GPL, MIT, CC BY-NC-SA, etc.

No files from either source were copied into this V6 textured model. Source sprite `tanks_for_bob_fork_1.8.95/graphics/entity/campfire.png` remains authoritative. Original game assets were not replaced.

See [source selection and per-asset attribution](../../../../docs/art/FACTORIO_GRAPHICS_SOURCE_REFERENCES.md).
