# Copyable Factorio Output module

Copy `factorio-output/` into your repository root, then copy `factorio-output/workflow.template.yml` to `.github/workflows/factorio-output.yml`.
Provide an authored Blender `.blend` and job/profile JSON. Run the **Factorio Output** GitHub Action in `review` mode.
The workflow produces four-direction animation atlases, icons, Lua and actual Blender proof, and can opt into `publish` or `deploy` with exact-target safeguards.
See [README.md](README.md) for commands, required dependencies and safety gates.
