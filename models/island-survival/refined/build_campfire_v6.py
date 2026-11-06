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

SEED=20261107
rng=random.Random(SEED)
MATS={
 'stone_base': (0.48,0.47,0.45),'stone_light':(0.60,0.595,0.575),
 'stone_pale':(0.67,0.67,0.645),'stone_dark':(0.35,0.35,0.35),
 'stone_warm':(0.55,0.52,0.48),'ash':(0.20,0.195,0.185),
 'ash_light':(0.31,0.305,0.29),'char':(0.085,0.076,0.066),
 'wood_bark':(0.287,0.175,0.095),'wood_bark_light':(0.385,0.257,0.148),
 'wood_bark_dark':(0.206,0.132,0.073),'wood_cut':(0.68,0.45,0.25),
 'wood_cut_ring':(0.51,0.325,0.17),'wood_sapwood':(0.59,0.395,0.217),
 'wood_heart':(0.415,0.255,0.137),'wood_weathered':(0.365,0.325,0.255),'embers':(0.93,0.29,0.04),
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
    n=18; group=f'stone_{i:02d}';phi=rng.random()*2*math.pi
    rings=[]
    levels=[(.02,.78),(.15,.89),(.33,.97),(.52,1.0),(.72,.86),(.89,.63),(1.0,.30)]
    wave=[rng.uniform(.90,1.10) for _ in range(n)]
    heights=[rng.uniform(-.046,.046) for _ in range(n)]
    for k,(zrel,width) in enumerate(levels):
        ring=[]
        for j in range(n):
            a=2*math.pi*j/n+phi
            jitter=wave[j]*(1+.035*math.sin(3*a+k))
            xx=x+rx*width*jitter*math.cos(a)
            yy=y+ry*width*jitter*math.sin(a)
            zz=max(.012,.035+rz*(zrel + (heights[j] if k in (1,2,3,4,5) else heights[j]*.12)))
            ring.append(vertex((xx,yy,zz)))
        rings.append(ring)
    for k in range(len(rings)-1):
        for j in range(n):
            a,b=rings[k][j],rings[k][(j+1)%n]
            c,d=rings[k+1][(j+1)%n],rings[k+1][j]
            m=color
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

def log(index,p0,p1,radius,mat,curv=0.02,lift=0.0):
    """Crooked tapered branch: rough bark, knots, exposed sapwood + split endgrain.

    All detail is visible at the Factorio viewing angle. No hidden mechanics.
    Curved longitudinal path, deformable oval cross sections, interrupted
    bark striae, root knot and nonplanar broken ends; deterministic seeded RNG.
    """
    group=f'cross_log_{index}'
    a=list(p0);b=list(p1); d=[b[k]-a[k] for k in range(3)]
    L=math.sqrt(sum(x*x for x in d));axis=[q/L for q in d]
    side=[-axis[1],axis[0],0]
    sideL=math.hypot(side[0],side[1]);side=[v/sideL for v in side]
    top=[axis[1]*side[2]-axis[2]*side[1],axis[2]*side[0]-axis[0]*side[2],axis[0]*side[1]-axis[1]*side[0]]
    # top is up for horizontal logs; use it to expose bark and cuts to camera
    if top[2]<0:top=[-v for v in top];side=[-v for v in side]
    n=22;steps=25
    az=rng.uniform(-.15,.25)
    barknoise=[rng.uniform(.96,1.04) for _ in range(n)]
    phase=rng.uniform(-2,2)
    lengthwise=[(.024*math.sin((k+phase)*.4)+.012*math.cos((k+phase)*.9)) for k in range(steps)]
    # Knots and uneven grain deliberately disturb the perfectly smooth cylinder.
    knot_t=rng.uniform(.24,.70);knot_a=rng.choice([3,6,11,15,19])
    centers=[];rings=[];radials=[]
    for k in range(steps):
        t=k/(steps-1)
        sideways=curv*math.sin(math.pi*t)*math.sin(3.2*t+phase)
        center=[a[q]+d[q]*t+side[q]*sideways for q in range(3)]
        center[2]+=lift*math.sin(math.pi*t)+.012*math.sin(2*math.pi*t+phase)
        # Exposed ends aren't uniformly circular and the logs taper irregularly.
        radius_t=radius*(1.065-.21*t+lengthwise[k])*(1+.08*math.sin(3*math.pi*t+phase))
        centers.append(center);radials.append(radius_t)
        ring=[]
        for j in range(n):
            theta=2*math.pi*j/n+az
            knot=max(0,1-abs(t-knot_t)/.15)*max(0,1-abs(j-knot_a)/2)
            rough=(.98+.022*math.cos(t*20+3*theta)+.019*math.sin(5*theta+13*t))
            r=radius_t*barknoise[j]*(rough + .13*knot)
            # Distinct asymmetric circular form, not a square beam.
            r_side=r; r_up=r*(.9+.05*math.sin(t*5+phase))
            pos=[center[q]+r_side*math.cos(theta)*side[q]+r_up*math.sin(theta)*top[q] for q in range(3)]
            if k==0 or k==steps-1:
                pos=[pos[q]+axis[q]*rng.uniform(-.014,.014) for q in range(3)]
            ring.append(vertex(pos))
        rings.append(ring)
    for k in range(steps-1):
        t=k/(steps-1)
        for j in range(n):
            # Bark runs lengthwise with charcoal scorching near central fire.
            # Longitudinal coherent stripes: real bark grain, no checkerboarding.
            m=('wood_bark_dark' if j in (1,2,16) else
               ('wood_bark_light' if j in (8,20) else mat))
            # Limited scorch only on the upper exposed face near central embers.
            if .36<t<.61 and j in (3,4,5) and radius>.06:m='char'
            if radius>.07 and .61<t<.78 and j==14:m='wood_weathered'
            quad(rings[k][j],rings[k][(j+1)%n],rings[k+1][(j+1)%n],rings[k+1][j],m,group+'_bark')
    # Each end is an actual recessed annular cross section, not an applied decal.
    for end,is_tip in ((0,False),(steps-1,True)):
        direction=1 if is_tip else -1
        outer=rings[end]; cp=centers[end];rad=radials[end]
        endpt=[cp[q]+.008*direction*axis[q] for q in range(3)]
        inrings=[]
        for factor in (.76,.43):
            ring=[]
            for j in range(n):
                th=2*math.pi*j/n+az
                rr=factor*rad*(1+.05*math.sin(j*2.7))
                ring.append(vertex(tuple(endpt[q]+rr*(math.cos(th)*side[q]+math.sin(th)*top[q]) for q in range(3))))
            inrings.append(ring)
        center=vertex(tuple(endpt[q]+.009*direction*axis[q] for q in range(3)))
        for j in range(n):
            nextj=(j+1)%n
            quad(outer[j],outer[nextj],inrings[0][nextj],inrings[0][j],'wood_sapwood',group+'_end_sapwood')
            quad(inrings[0][j],inrings[0][nextj],inrings[1][nextj],inrings[1][j],'wood_cut_ring',group+'_end_ring')
            tri(inrings[1][j],inrings[1][nextj],center,'wood_cut' if j%4 else 'wood_heart',group+'_end_heart')
        # Endgrain radial checks, just enough to survive 64px downsampling.
        for jj in (1,5,10):
            tri(center,inrings[0][jj],inrings[0][(jj+1)%n],'wood_heart',group+'_end_checks')
    # Bark strips: short ragged plaques, tapered/offset, no floating stripes.
    for stripe,theta in enumerate((.44,1.15,1.94,2.87,3.91,5.04) if radius>.07 else (1.15,3.91)):
        start=rng.randint(3,7);finish=rng.randint(19,24)
        points=[];shifts=[]
        for k in range(start,finish):
            t=k/(steps-1);p=centers[k]; th=theta+az+.045*math.sin(6*t+stripe)
            rr=radials[k]*1.035
            point=tuple(p[q]+rr*(math.cos(th)*side[q]+math.sin(th)*top[q]) for q in range(3))
            point_b=tuple(p[q]+rr*(math.cos(th+.065)*side[q]+math.sin(th+.065)*top[q]) for q in range(3))
            points.append(vertex(point));shifts.append(vertex(point_b))
        for k in range(len(points)-1):
            if k%4==2:continue
            quad(points[k],shifts[k],shifts[k+1],points[k+1],
                 'wood_bark_dark' if stripe%2 else 'wood_bark_light',group+'_grain')
    # Raised branch scar -- attached to log circumference, not an additional floating twig.
    k=int(knot_t*(steps-1));j=knot_a
    if 1<k<steps-2:
        tri(rings[k][j],rings[k+1][j],rings[k][(j+1)%n],
            'wood_bark_light',group+'_knot')

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
# Rough firewood. Deliberately NOT a symmetrical X of square beams.
# Lower pieces bear against the rocks; only the crossing upper piece arches up.
log('lower_west_east',(-.53,.22,.335),(.51,-.26,.355),.119,'wood_bark',curv=.045,lift=.013)
log('upper_diagonal',(-.34,-.48,.345),(.40,.39,.355),.108,'wood_bark',curv=.06,lift=.162)
log('rear_ember_log',(-.37,.04,.265),(.30,.24,.290),.080,'wood_bark_dark',curv=.03,lift=.005)
log('kindling_left',(-.15,-.26,.192),(.29,.02,.197),.040,'wood_bark_dark',curv=.015)
log('kindling_right',(.21,-.24,.182),(-.22,.02,.192),.037,'wood_bark',curv=.018)
log('charred_twig',(-.20,.23,.188),(.18,-.04,.192),.032,'char',curv=.01)
for i,(x,y) in enumerate([(-.17,-.18),(.03,-.27),(.23,-.10),(.10,.21),(-.24,.11),(.28,.25),(-.08,.32)]):
 coal_piece(i,x,y,.12+rng.uniform(0,.035),rng.uniform(.045,.09),rng.uniform(.03,.065))
# Fire tongues are optional overlay groups; choose only active groups during rendering.
flames=[(-.12,-.04,.23,.18,.73,.16,'flame_orange'),(.13,.07,.24,.21,.90,.15,'flame_gold'),
 (.0,-.13,.25,.14,.69,.13,'flame_yellow'),(.25,.11,.28,.13,.54,.15,'flame_orange'),
 (-.26,.05,.24,.12,.55,.13,'flame_gold'),(.07,.15,.24,.12,.48,.10,'flame_yellow')]
for i,args in enumerate(flames,1):flame_tongue(i,*args)

def write_obj(path):
    lines=['# Tanks for Bob campfire v6 - refined visible geometry',
     '# Procedurally authored. No source art replaced. X east, Y north, Z up.',
     'mtllib campfire-smoothed-v6.mtl','o campfire_refined_v4']
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
    lines=['# Material palette for campfire v6; editable inside Blender']
    for name,rgba in MATS.items():
        lines+=['newmtl '+name,'Ka 0.0800 0.0800 0.0800',
        'Kd %.4f %.4f %.4f'%rgba,'Ks 0.0450 0.0450 0.0450',
        'Ns 9.0000','d 1.0000','illum 2','']
    path.write_text('\n'.join(lines))

if __name__=='__main__':
    out=Path(sys.argv[1] if len(sys.argv)>1 else '.')
    out.mkdir(parents=True,exist_ok=True)
    write_obj(out/'campfire-smoothed-v6.obj')
    write_mtl(out/'campfire-smoothed-v6.mtl')
    print(f'Generated campfire v6: {len(verts)} vertices, {len(faces)} triangles, {len(set(g for *_,g in faces))} groups')
