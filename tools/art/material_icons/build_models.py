"""Run using Blender --background --python this-file -- --pipeline-root PATH --assets ID --revision v03."""
import argparse,os,sys
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--pipeline-root',type=Path,required=True)
parser.add_argument('--assets',nargs='+',required=True);parser.add_argument('--revision')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
os.environ['ICON_PIPELINE_ROOT']=str(args.pipeline_root.resolve())
sys.path.insert(0,str(Path(__file__).parent))
from material_icon_registry import PILOTS
selected={id:PILOTS[id] for id in args.assets};PILOTS.clear();PILOTS.update(selected)
if args.revision:
 for spec in PILOTS.values():spec['revision']=args.revision
from build_material_icon_pilots import build
for id,spec in PILOTS.items():
 if spec['shape']!='reuse-building':build(id)
if any(spec['shape']=='reuse-building' for spec in PILOTS.values()):import prepare_existing_factory_icons
