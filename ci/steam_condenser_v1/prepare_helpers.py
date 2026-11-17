"""Reuse the already-tested sprite packer and isolated Factorio runners."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
replacements=[('fish-pond-v2','steam-condenser-v1'),('fish_pond_v2','steam_condenser_v1'),
 ('fish-pond/v2','steam-condenser/v1'),('Fish Pond V2','Steam Condenser V1'),
 ('"fish-pond"','"steam-condenser"'),('"fishery"','"Steam"')]
for source,target in [
 ('models/island-survival/fish-pond/v2/pack_sprites.py','models/island-survival/steam-condenser/v1/pack_sprites.py'),
 ('models/island-survival/fish-pond/v2/graphics.lua','models/island-survival/steam-condenser/v1/graphics.lua'),
 ('ci/fish_pond_v2/run_native.py','ci/steam_condenser_v1/run_native.py'),
 ('ci/fish_pond_v2/capture_gui.py','ci/steam_condenser_v1/capture_gui.py')]:
    path=ROOT/target
    if path.exists():raise FileExistsError(path)
    text=(ROOT/source).read_text()
    for a,b in replacements:text=text.replace(a,b)
    if target.endswith('graphics.lua'):
        text=text.replace('32*3.9/256','32*5.2/256').replace('-.28/math.sqrt(2)','-.93/math.sqrt(2)')
    if target.endswith('capture_gui.py'):
        text=text.replace("('normal','close','idle-close','fluid-close','motion-close','legacy-close')","('close',)")
    path.write_text(text)
print('REUSED_EXISTING_CAPTURE_AND_NATIVE_TOOLS')
