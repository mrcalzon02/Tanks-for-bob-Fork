import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[4]
im=bpy.data.images.load(str(R/'models/island-survival/stone-water-wheel/candidates/v3-production04/north-idle-00-full.png'));im.scale(64,64);im.file_format='PNG';im.filepath_raw=str(R/'tanks_for_bob_fork_1.8.104/graphics/icons/stone-water-wheel-v3.png');im.save()
