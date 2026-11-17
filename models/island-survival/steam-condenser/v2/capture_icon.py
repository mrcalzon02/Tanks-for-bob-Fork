import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[4]
im=bpy.data.images.load(str(R/'models/island-survival/steam-condenser/candidates/v2-production05/north-idle-00.png'));im.scale(64,64);im.file_format='PNG';im.filepath_raw=str(R/'tanks_for_bob_fork_1.8.104/graphics/icons/steam-condenser-v2.png');im.save()
