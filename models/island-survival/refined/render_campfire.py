#!/usr/bin/env python3
"""Standalone software preview of the *actual* OBJ triangles, no Blender required."""
import math,random,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np

DIR=Path(__file__).resolve().parent
OBJ=DIR/'campfire-refined.obj';MTL=DIR/'campfire-refined.mtl'
COLORS={}; color=None
for ln in MTL.read_text().splitlines():
    tok=ln.split()
    if len(tok)>=2 and tok[0]=='newmtl':color=tok[1]
    elif len(tok)==4 and tok[0]=='Kd':COLORS[color]=np.array([float(c) for c in tok[1:]])

verts=[];faces=[];mat='stone_base';group=''
for ln in OBJ.read_text().splitlines():
    tok=ln.split()
    if len(tok)==4 and tok[0]=='v':verts.append([float(x) for x in tok[1:]])
    elif len(tok)==2 and tok[0]=='usemtl':mat=tok[1]
    elif len(tok)>=2 and tok[0]=='g':group=tok[1]
    elif len(tok)==4 and tok[0]=='f':faces.append((tuple(int(x.split('/')[0])-1 for x in tok[1:]),mat,group))
verts=np.array(verts)

def font(px,bold=False):
    for p in (['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']):
        if Path(p).exists():return ImageFont.truetype(p,px)
    return ImageFont.load_default()

def norm(v):
    n=np.linalg.norm(v);return v/n if n>1e-8 else v

def render(elevation=47,azimuth=-56,active=False,tag='',W=1200,H=1050,scale=420):
    # camera position on unit sphere: azimuth from world east toward north
    e=math.radians(elevation);a=math.radians(azimuth)
    outward=np.array([math.cos(e)*math.cos(a),math.cos(e)*math.sin(a),math.sin(e)])
    view=-outward
    right=norm(np.cross(view,np.array([0.,0.,1.])))
    up=norm(np.cross(right,view))
    center=np.array([0.,0.,.28])
    midx=W/2;midy=H*.53
    def project(p):
        pp=np.asarray(p)-center
        return (midx + np.dot(pp,right)*scale,midy - np.dot(pp,up)*scale)
    # muted dark slate studio ground + centered floating shadow
    img=Image.new('RGB',(W,H),(28,33,39));pix=np.array(img)
    yy,xx=np.ogrid[:H,:W];distance=((xx-W/2)/(W*.90))**2+((yy-H*.58)/(H*.92))**2
    shade=np.clip(1-distance*.4,0.68,1.)
    pix=np.clip(pix*shade[:,:,None]+np.array([12,14,15])[None,None,:],0,255).astype(np.uint8)
    img=Image.fromarray(pix,'RGB').convert('RGBA'); d=ImageDraw.Draw(img,'RGBA')
    # grid lines on ground (local inspection aid)
    for i in np.arange(-2.5,2.6,.5):
        for direction in (0,1):
            p1=(i,-2.5,0) if direction==0 else (-2.5,i,0)
            p2=(i,2.5,0) if direction==0 else (2.5,i,0)
            d.line([project(p1),project(p2)], fill=(142,154,156,15),width=1)
    # physical contact shadows, soft transparency
    shadow=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(shadow,'RGBA')
    for k in range(28,0,-1):
        rad=.74+.015*k
        pts=[]
        for j in range(50):
            th=j*2*math.pi/50
            pts.append(project((rad*math.cos(th),rad*.88*math.sin(th),.003)))
        sd.polygon(pts,fill=(0,0,0,2))
    img=Image.alpha_composite(img,shadow.filter(ImageFilter.GaussianBlur(9)))
    # Painter's model, explicitly read from the saved OBJ.
    light=norm(np.array([-.48,-.56,1.5]))
    opaque=[];transparent=[]
    for fi,(indices,m,g) in enumerate(faces):
        p=verts[np.asarray(indices)]
        normal=norm(np.cross(p[1]-p[0],p[2]-p[0]))
        depth=np.dot(np.mean(p,axis=0),outward)
        kind='flame' if g.startswith('flame_') else 'solid'
        uv=[project(q) for q in p]
        if np.linalg.norm(np.cross(p[1]-p[0],p[2]-p[0]))<1e-8:continue
        color=COLORS.get(m,np.array([.7,.4,.2]))
        # broad soft light; don't black out down-facing angled facets
        diffuse=max(0.,float(np.dot(normal,light)))
        illumination=(.49+.50*diffuse+.11*max(0.,float(np.dot(normal,np.array([0,0,1])))))
        if g.startswith('cross_log') and 'bark_ridges' in g:illumination*=.8
        irregular=(.93 + .14*((fi*31%97)/97))
        rgb=tuple(int(np.clip(255*pow(max(.01,c*illumination*irregular),.9),0,255)) for c in color)
        if kind=='flame':transparent.append((depth,uv,rgb,m))
        else:opaque.append((depth,uv,rgb,m))
    for depth,points,color,m in sorted(opaque,key=lambda x:x[0]):
        ImageDraw.Draw(img,'RGBA').polygon(points, fill=(*color,255))
    if active:
        # emissive and soft bloom behind geometry; flame remains an overlay not baked stone texture
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));od=ImageDraw.Draw(overlay,'RGBA')
        for depth,points,color,m in sorted(transparent,key=lambda x:x[0]):
            opacity=105 if m=='flame_orange' else (122 if m=='flame_gold' else 130)
            od.polygon(points, fill=(*color,opacity))
        glow=overlay.filter(ImageFilter.GaussianBlur(34))
        glow.putalpha(glow.getchannel('A').point(lambda alpha:int(alpha*.45)))
        img=Image.alpha_composite(img,glow)
        img=Image.alpha_composite(img,overlay)
    # typography
    d=ImageDraw.Draw(img,'RGBA')
    d.rectangle((30,25,W-30,125),fill=(23,29,34,220))
    d.text((55,43),'TANKS FOR BOB  /  ISLAND SURVIVAL',font=font(18,True),fill=(159,172,173,255))
    d.text((55,73),tag or ('CAMPFIRE  •  BURNING' if active else 'CAMPFIRE  •  UNLIT'),font=font(28,True),fill=(242,237,220,255))
    bottom='SOURCE: REAL PROCEDURAL OBJ GEOMETRY     •     1,194 VERTICES / 1,945 TRIANGLES'
    d.rectangle((30,H-83,W-30,H-28),fill=(23,29,34,220))
    d.text((55,H-65),bottom,font=font(17),fill=(190,199,200,255))
    return img.convert('RGB')

if __name__=='__main__':
    one=render(47,-56,False,'CAMPFIRE V2   /   PHYSICAL GEOMETRY')
    two=render(47,-56,True,'CAMPFIRE V2   /   WORKING FIRE STUDY')
    three=render(76,-56,False,'CAMPFIRE V2   /   TOP PROFILE',scale=400)
    one.save(DIR/'campfire-v2-unlit.png');two.save(DIR/'campfire-v2-burning.png');three.save(DIR/'campfire-v2-top.png')
    for name in ['campfire-v2-unlit.png','campfire-v2-burning.png','campfire-v2-top.png']:
        print(name,(DIR/name).stat().st_size)
