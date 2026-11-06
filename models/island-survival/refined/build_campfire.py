#!/usr/bin/env python3
"""Tanks for Bob campfire: deterministic, editable low-poly refinement.
Authoritative reference: tanks_for_bob_fork_1.8.95/graphics/entity/campfire.png
The model is intentionally an art-source, not a runtime sprite replacement.
Run: python build_campfire.py [output_directory]
Axes: X east, Y north, Z up; nominal tile units.
"""
from __future__ import annotations
import math, random, os, sys
from pathlib import Path

SEED=20261105
rng=random.Random(SEED)
MATS={
 'stone_base': (0.48,0.47,0.45),'stone_light':(0.65,0.64,0.60),
 'stone_pale':(0.73,0.71,0.68),'stone_dark':(0.35,0.35,0.35),
 'stone_warm':(0.60,0.56,0.52),'ash':(0.20,0.195,0.185),
 'ash_light':(0.34,0.32,0.29),'char':(0.095,0.080,0.070),
 'wood_bark':(0.30,0.175,0.095),'wood_bark_light':(0.43,0.255,0.13),
 'wood_bark_dark':(0.20,0.115,0.060),'wood_cut':(0.66,0.42,0.22),
 'wood_cut_ring':(0.45,0.27,0.13),'embers':(0.93,0.29,0.04),
 'ember_hot':(1.0,0.68,0.11),
 'flame_orange':(1.0,0.26,0.02),'flame_gold':(1.0,0.57,0.035),
 'flame_yellow':(1.0,0.90,0.18)
}
verts=[]; faces=[]; groups=[]

def vertex(p):
    verts.append(tuple(float(x) for x in p));return len(verts)

def tri(a,b,c,mat,group):
    faces.append((int(a),int(b),int(c),mat,group))

def quad(a,b,c,d,mat,group):
    tri(a,b,c,mat,group); tri(a,c,d,mat,group)

def irregular_stone(i,x,y,rx,ry,rz,color,tilt=0):
    """Small sculpted boulder, natural flat underside, 8-sided 3-ring shell."""
    n=9; group=f'stone_{i:02d}';phi=rng.random()*2*math.pi
    rings=[]
    levels=[(.02,.82),(.25,1.0),(.70,.92),(1.0,.35)]
    wave=[rng.uniform(.79,1.14) for _ in range(n)]
    heights=[rng.uniform(-.08,.08) for _ in range(n)]
    for k,(zrel,width) in enumerate(levels):
        ring=[]
        for j in range(n):
            a=2*math.pi*j/n+phi
            jitter=wave[j]*(1+.035*math.sin(3*a+k))
            xx=x+rx*width*jitter*math.cos(a)
            yy=y+ry*width*jitter*math.sin(a)
            zz=max(.012,.035+rz*(zrel + (heights[j] if k in (1,2) else heights[j]*.15)))
            ring.append(vertex((xx,yy,zz)))
        rings.append(ring)
    for k in range(len(rings)-1):
        for j in range(n):
            a,b=rings[k][j],rings[k][(j+1)%n]
            c,d=rings[k+1][(j+1)%n],rings[k+1][j]
            m=color if rng.random()>.25 else rng.choice(['stone_light','stone_pale','stone_dark','stone_warm'])
            quad(a,b,c,d,m,group)
    top=vertex((x, y,.035+rz*1.02))
    for j in range(n):tri(rings[-1][j],rings[-1][(j+1)%n],top,color,group)

def ash_patch():
    g='ash_and_coals';n=15
    center=vertex((0.02,0.00,.045))
    ring=[]
    for i in range(n):
        a=i*2*math.pi/n;rr=.60+rng.uniform(-.08,.07)
        ring.append(vertex((.02+rr*math.cos(a),rr*.76*math.sin(a),.035+rng.uniform(-.005,.02))))
    for i in range(n): tri(center,ring[i],ring[(i+1)%n],rng.choice(['ash','ash','ash_light','char']),g)

def log(index,p0,p1,radius,mat):
    """Tapered, jointed 10-sided branch with exposed ends and bark-strip details."""
    group=f'cross_log_{index}'
    a=tuple(p0);b=tuple(p1)
    d=[b[k]-a[k] for k in range(3)]
    L=math.sqrt(sum(x*x for x in d));axis=[q/L for q in d]
    # local basis. Bark grooves are model geometry, not fake photo details.
    up=[0,0,1];side=[axis[1],-axis[0],0]
    sL=math.hypot(side[0],side[1]);side=[v/sL for v in side]
    other=[axis[1]*side[2]-axis[2]*side[1],axis[2]*side[0]-axis[0]*side[2],axis[0]*side[1]-axis[1]*side[0]]
    radial=10; along=7;angular=rng.uniform(0,.25)
    barkwaves=[rng.uniform(.90,1.1) for _ in range(radial)]
    rings=[]
    for i in range(along):
        t=i/(along-1);pos=[a[k]+t*d[k] for k in range(3)]
        rad=radius*(1.04-.10*t)*(0.90 if i in (0,along-1) else 1)
        ring=[]
        for j in range(radial):
            th=j*2*math.pi/radial+angular
            cs=math.cos(th);sn=math.sin(th)
            rr=rad*barkwaves[j]*(1+0.025*math.sin(t*24+j))
            ring.append(vertex((pos[k]+rr*(cs*side[k]+sn*other[k]) for k in range(3))))
        rings.append(ring)
    for i in range(along-1):
        for j in range(radial):
            use=mat if j%4 else 'wood_bark_light'
            if i>=along-2 and (j in [2,3,4]):use='char'
            quad(rings[i][j],rings[i][(j+1)%radial],rings[i+1][(j+1)%radial],rings[i+1][j],use,group)
    ca=vertex(a);cb=vertex(b)
    for j in range(radial):
        tri(ca,rings[0][(j+1)%radial],rings[0][j],'wood_cut',group+'_cut')
        tri(cb,rings[-1][j],rings[-1][(j+1)%radial],'wood_cut',group+'_cut')
    # ring of cut end grain visible at one end
    for endpoint, sign in ((a,0),(b,1)):
        pos=[endpoint[k]+axis[k]*(.003 if sign else -.003) for k in range(3)]
        rs=[]
        for j in range(radial):
            th=j*2*math.pi/radial+angular
            rr=radius*.57
            rs.append(vertex(tuple(pos[k]+rr*(math.cos(th)*side[k]+math.sin(th)*other[k]) for k in range(3))))
        for j in range(radial):
            v1=rings[-1 if sign else 0][j];v2=rings[-1 if sign else 0][(j+1)%radial]
            # small defined wood ring (thin accent only)
            tri(v1,v2,rs[(j+1)%radial],'wood_cut_ring',group+'_end_grain')
            tri(v1,rs[(j+1)%radial],rs[j],'wood_cut_ring',group+'_end_grain')
    # Long bark ridges: only upper-facing sectors need crisp readable details.
    for ang in (0.8,1.55,2.35):
        points=[]
        for i in range(1,along-1):
            t=i/(along-1);pos=[a[k]+t*d[k] for k in range(3)]
            th=ang+angular+.08*math.sin(i*1.1)
            rr=radius*(1.10-.10*t)
            points.append(vertex(tuple(pos[k]+rr*(math.cos(th)*side[k]+math.sin(th)*other[k]) for k in range(3))))
        for i in range(len(points)-1):
            # skinny ridge triangle, one point near neighboring angle
            pidx=points[i];v=verts[pidx-1]
            delta=.017
            offset=vertex(tuple(v[k]+delta*other[k] for k in range(3)))
            tri(pidx,offset,points[i+1],'wood_bark_dark',group+'_bark_ridges')

def coal_piece(i,x,y,z,rx=.08,ry=.07,rz=.045):
    g=f'coal_{i:02d}'
    top=vertex((x,y,z+rz))
    vs=[]
    for j in range(7):
        a=j*2*math.pi/7
        vs.append(vertex((x+rx*math.cos(a),y+ry*math.sin(a),z+rng.uniform(-.012,.005))))
    for j in range(7):tri(vs[j],vs[(j+1)%7],top,rng.choice(['ash','char','embers']),g)

def flame_tongue(i,x,y,z,base,height,width,material):
    # Layer of camera-friendly open flame geometry. Deliberately separate from physical solid parts.
    g=f'flame_tongue_{i:02d}'
    steps=7;nodes=[];phase=rng.random()*math.pi*2
    for k in range(steps):
        t=k/(steps-1)
        spread=base*(1-t)**.9+.012
        bend=width*math.sin(phase+t*4)*(t**1.3)
        cx=x+bend;cy=y+0.17*t*math.cos(phase)
        cz=z+height*t
        ring=[]
        for j in range(5):
            a=2*math.pi*j/5+phase
            ring.append(vertex((cx+spread*math.cos(a),cy+spread*.7*math.sin(a),cz)))
        nodes.append(ring)
    for k in range(steps-1):
        for j in range(5):
            quad(nodes[k][j],nodes[k][(j+1)%5],nodes[k+1][(j+1)%5],nodes[k+1][j],material,g)

ash_patch()
# asymmetrical stones based on small original sprite: heavy pale front stones, fewer behind.
rocks=[
 (-.71,.16,.20,.25,.26,'stone_pale'),(-.60,.46,.19,.22,.23,'stone_light'),
 (-.40,.68,.19,.17,.21,'stone_light'),(-.12,.62,.23,.20,.29,'stone_warm'),
 (.20,.61,.18,.17,.21,'stone_dark'),(.49,.47,.19,.23,.24,'stone_light'),
 (.71,.18,.23,.24,.32,'stone_pale'),(.72,-.20,.18,.24,.28,'stone_light'),
 (.48,-.50,.27,.26,.34,'stone_pale'),(.17,-.65,.30,.24,.31,'stone_light'),
 (-.22,-.66,.29,.25,.35,'stone_pale'),(-.57,-.42,.27,.24,.37,'stone_pale'),
 (-.78,-.12,.18,.20,.24,'stone_warm'),
 (.05,.19,.18,.14,.13,'stone_dark'),(-.02,-.17,.16,.13,.10,'stone_dark')]
for i,r in enumerate(rocks,1): irregular_stone(i,*r)
# Crossed timber well above the central ash, ends resting against perimeter stones.
log('northwest_southeast',(-.55,.44,.43),(.58,-.48,.40),.125,'wood_bark')
log('southwest_northeast',(-.50,-.45,.41),(.53,.46,.46),.115,'wood_bark')
log('small_starter',(-.23,.06,.22),(.35,.18,.21),.063,'wood_bark_dark')
for i,(x,y) in enumerate([(-.17,-.18),(.03,-.27),(.23,-.10),(.10,.21),(-.24,.11),(.28,.25),(-.08,.32)]):
 coal_piece(i,x,y,.12+rng.uniform(0,.035),rng.uniform(.045,.09),rng.uniform(.03,.065))
# Fire tongues are optional overlay groups; choose only active groups during rendering.
flames=[(-.12,-.04,.23,.18,.73,.16,'flame_orange'),(.13,.07,.24,.21,.90,.15,'flame_gold'),
 (.0,-.13,.25,.14,.69,.13,'flame_yellow'),(.25,.11,.28,.13,.54,.15,'flame_orange'),
 (-.26,.05,.24,.12,.55,.13,'flame_gold'),(.07,.15,.24,.12,.48,.10,'flame_yellow')]
for i,args in enumerate(flames,1):flame_tongue(i,*args)

def write_obj(path):
    lines=['# Tanks for Bob campfire v2 - refined visible geometry',
     '# Procedurally authored. No source art replaced. X east, Y north, Z up.',
     'mtllib campfire-refined.mtl','o campfire_refined']
    for p in verts: lines.append('v %.5f %.5f %.5f'%p)
    current=None
    for a,b,c,m,g in faces:
        pair=(g,m)
        if pair!=current:
            if current is None or g!=current[0]:lines.append('g '+g)
            lines.append('usemtl '+m)
            current=pair
        lines.append(f'f {a} {b} {c}')
    path.write_text('\n'.join(lines)+'\n')

def write_mtl(path):
    lines=['# Material palette for campfire v2; editable inside Blender']
    for name,rgba in MATS.items():
        lines+=['newmtl '+name,'Ka 0.0800 0.0800 0.0800',
        'Kd %.4f %.4f %.4f'%rgba,'Ks 0.0450 0.0450 0.0450',
        'Ns 9.0000','d 1.0000','illum 2','']
    path.write_text('\n'.join(lines))

if __name__=='__main__':
    out=Path(sys.argv[1] if len(sys.argv)>1 else '.')
    out.mkdir(parents=True,exist_ok=True)
    write_obj(out/'campfire-refined.obj')
    write_mtl(out/'campfire-refined.mtl')
    print(f'Generated campfire v2: {len(verts)} vertices, {len(faces)} triangles, {len(set(g for *_,g in faces))} groups')
