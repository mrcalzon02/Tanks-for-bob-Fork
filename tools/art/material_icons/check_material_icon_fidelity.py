import argparse,hashlib,json
from PIL import Image,ImageChops,ImageStat
from material_icon_registry import PILOTS,folder
parser=argparse.ArgumentParser();parser.add_argument('--assets',nargs='+',choices=list(PILOTS),default=list(PILOTS));args=parser.parse_args()
reports=[]
for id in args.assets:
 dest=folder(id);review=dest/'export-review'
 a=Image.open(review/'source-basecolor.png').convert('RGBA');b=Image.open(review/'export-basecolor.png').convert('RGBA')
 mask=ImageChops.darker(a.getchannel('A'),b.getchannel('A')).point(lambda x:255 if x>=250 else 0)
 assert mask.getbbox(),id
 diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'));mean=ImageStat.Stat(diff,mask).mean
 values=sorted(max(pixel) for pixel,m in zip(diff.get_flattened_data(),mask.get_flattened_data()) if m);p95=values[int(.95*(len(values)-1))]
 a=Image.open(review/'source-beauty.png').getchannel('A').point(lambda x:255 if x>128 else 0)
 b=Image.open(review/'export-beauty.png').getchannel('A').point(lambda x:255 if x>128 else 0)
 union=sum(v>0 for v in ImageChops.lighter(a,b).get_flattened_data());intersection=sum(v>0 for v in ImageChops.darker(a,b).get_flattened_data());iou=intersection/union
 report=dict(asset=id,passed=max(mean)<=4 and p95<=12 and iou>=.995,mean_absolute_rgb_error_8bit=mean,p95_max_channel_error_8bit=p95,
  silhouette_iou=iou,limits=dict(mean_max=4,p95_max=12,iou_min=.995),glb_sha256=hashlib.sha256((dest/'model.glb').read_bytes()).hexdigest())
 (dest/'material-fidelity.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report);print(id,report['passed'],[round(v,3) for v in mean],p95,iou)
assert all(r['passed'] for r in reports),'Repair failed source/export fidelity before integrating'
