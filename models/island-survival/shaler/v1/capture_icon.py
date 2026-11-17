"""One canonical item view from the genuine fixed-camera idle capture."""
import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[4]
p=R/'models/island-survival/shaler/candidates/v1-production04/north-idle-00.png'
im=bpy.data.images.load(str(p));im.scale(64,64)
im.file_format='PNG';im.filepath_raw=str(R/'tanks_for_bob_fork_1.8.104/graphics/icons/shaler-v1.png');im.save()
