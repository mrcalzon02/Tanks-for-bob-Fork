import json,os
from pathlib import Path
REPO=Path(__file__).resolve().parents[3]
ROOT=Path(os.environ.get('ICON_PIPELINE_ROOT',str(REPO.parent/'Tech-Priests'))).resolve()
os.environ['ICON_PIPELINE_ROOT']=str(ROOT)
PILOTS=json.loads(Path(__file__).with_name('assets.json').read_text())
for spec in PILOTS.values():
 spec['repo']=REPO
 for key in ['source_glb','editable_master']:
  if key in spec:spec[key]=REPO/spec[key]
def folder(id):return REPO/'art/source-to-3d/material-icons'/PILOTS[id].get('revision','v01')/id
