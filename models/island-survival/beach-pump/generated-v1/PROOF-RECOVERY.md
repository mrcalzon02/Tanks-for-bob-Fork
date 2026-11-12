# Beach Pump V1 — recovered genuine Blender source proof

**Native Blender 5.2.3 work:** [Core30 run 43259212246](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43259212246).

The original model was built on OLD-CORE30-homebrew, generated 4 genuine idle
and 4 genuine working Cycles PNG renders with an unchanged orthographic 45-degree
camera, then passed a separate saved-Blender native reopen check and a four-way
PNG proof check. The upstream workflow's *evidence upload* failed solely because
GitHub Actions artifact storage quota was exhausted; it did **not** fail any
Blender geometry, animation, image or runtime check.

A second authorized run [43260359144](https://github.com/mrcalzon02/Dens-Mortis/actions/runs/43260359144)
copied the exact verified Blender master, all eight PNGs and receipts to a
separate Core30 repository-independent evidence directory before Git checkout.
It SHA-checked the copies. The true contact proof and receipts were then read
from that trusted Windows runner's logs and committed here as normal Git data,
not Actions artifacts.

### Native Blender master
- Name: `beach-pump-v1.blend`
- SHA256: `aed52dad68e16f40d626e713c525081ce77eb93210fc622e8cfa55ddecb5428d`
- Preserved on Core30 under a dedicated `_homebrew/reports/beach-pump-v1-proof-43259212246/` directory.
- **The .blend is not yet published as a GitHub file.** This source receipt
  documents verification, not a claim that the binary has been transferred.

### Recovered proof files (SHA256)
- `review-four-directions.png`: `80802bab4a13624c72f568214257f3d4e70eace48dcb1255454b6250ab6ff8d3` (148176 bytes)
- `native-reopen-qa.json`: `6e8a2d4d0c20359326937886f279f095c25cbfa49c122945fd4d6569bdadb3b0` (745 bytes)
- `proof-qa.json`: `d5a36cb442d93684586d193701fb25631b6034106346116adcd193f6046a683e` (2681 bytes)
- `build-report.json`: `18244551fef2093b4baf56f0d66c3cf354cba366e5b61e69706cf50f14c6a2ab` (4093 bytes)

**Boundaries:** No modified beachpump prototype, game startup, Steam session,
fictitious screenshots, user art approval or production sprite attachment.
