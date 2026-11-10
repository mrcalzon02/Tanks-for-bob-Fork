#!/usr/bin/env python3
"""Solar Boiler V2: replace incorrect flat collectors with true parabolic troughs.

Derives the immutable 3x2 V1 Blender source, preserves the three registered
hollow Factorio boundary ports, the accepted FMPL PBR map bytes, boiler drum,
existing gauge and steam, then models a parabolic reflector with a physically
located focal absorber on each of the two solar-thermal collectors. Rigid fluid
lines only connect stationary troughs; no implausible rocking pipe disconnects.

All final views are genuine Cycles renders of ONE canonical 45 degree camera.
No live game prototype is modified by this program.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys

HERE=Path(__file__).resolve().parent
V1_ROOT=HERE.parent/'v1'
FRAMES=(0,25)
DIRECTIONS=(0,90,180,270)
FOCAL_HEIGHT=.28
TROUGH_HALF_WIDTH=.34
TROUGH_HALF_LENGTH=.45
TROUGH_TILT_DEG=11.0
REPLACE_PREFIXES=(
    'SOLAR | west | cast reflector backing',
    'SOLAR | east | cast reflector backing',
    'SOLAR | west | segmented mirror strip',
    'SOLAR | east | segmented mirror strip',
    'SOLAR | west | folded end rail',
    'SOLAR | east | folded end rail',
    'SOLAR | west | side retaining rail',
    'SOLAR | east | side retaining rail',
    'SOLAR | west | black thermal absorber',
    'SOLAR | east | black thermal absorber',
    'SOLAR | west | copper transfer strip',
    'SOLAR | east | copper transfer strip',
    'SOLAR | west | absorber termination',
    'SOLAR | east | absorber termination',
    'SOLAR | hot copper transfer pipe from collector',
)


def sha256(p:Path)->str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def parabola(y:float, focal:float=FOCAL_HEIGHT)->float:
    return y*y/(4*focal)


def reflected_vertical_ray_hits_focus(y:float, focal:float=FOCAL_HEIGHT)->float:
    """Ray-traced interception height of vertically incident light at Y=0.

    This is the true optical relationship, not a visually estimated 'rod'.
    """
    if abs(y)<1e-9:
        return focal
    p=y/(2*focal)
    dy=-2*p/(1+p*p)
    dz=(1-p*p)/(1+p*p)
    return parabola(y,focal)-y*dz/dy


def self_check():
    for y in (-.34,-.27,-.18,-.08,.08,.18,.27,.34):
        assert abs(reflected_vertical_ray_hits_focus(y)-FOCAL_HEIGHT)<1e-12,(y,reflected_vertical_ray_hits_focus(y))
        assert parabola(y)>=0
    assert parabola(TROUGH_HALF_WIDTH)<FOCAL_HEIGHT
    assert TROUGH_HALF_LENGTH*2<.96
    assert (abs(-.66)+TROUGH_HALF_LENGTH)<1.5
    contract=json.loads((V1_ROOT/'port-contract.json').read_text())
    assert contract['footprint_tiles']==[3,2]
    assert {x['id'] for x in contract['ports']}=={'water-west','water-east','steam-north'}
    print('SOLAR_V2_PARABOLIC_FOCUS_AND_3X2_CONTRACT_PASS',flush=True)


def material(bpy,name,color,metal,rough):
    mat=bpy.data.materials.new('Solar Boiler V2 | '+name)
    mat.use_nodes=True
    b=mat.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*color,1)
    b.inputs['Metallic'].default_value=metal
    b.inputs['Roughness'].default_value=rough
    # Subtle metal wear, not a blue photovoltaic-cell grid.
    n=mat.node_tree.nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value=25
    n.inputs['Detail'].default_value=2
    bump=mat.node_tree.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value=.07
    bump.inputs['Distance'].default_value=.0012
    mat.node_tree.links.new(n.outputs['Fac'],bump.inputs['Height'])
    mat.node_tree.links.new(bump.outputs['Normal'],b.inputs['Normal'])
    mat['optical_function']='Concentrating parabolic solar thermal mirror, not photovoltaic electricity'
    return mat


def mesh_hash(obj):
    h=hashlib.sha256()
    for v in obj.data.vertices:
        h.update(struct.pack('<3f',*v.co))
    for p in obj.data.polygons:
        h.update(struct.pack('<I',len(p.vertices)))
        for index in p.vertices: h.update(struct.pack('<I',index))
    return h.hexdigest()


def curved_trough(bpy,base,rig,label,col,mat):
    """Closed pressed steel backing with one truly continuous curved mirror."""
    y_n=32;x_n=14
    vs=[]
    for offset in (0.,-.025):
        for i in range(x_n+1):
            x=-TROUGH_HALF_LENGTH+2*TROUGH_HALF_LENGTH*i/x_n
            for j in range(y_n+1):
                y=-TROUGH_HALF_WIDTH+2*TROUGH_HALF_WIDTH*j/y_n
                vs.append((x,y,parabola(y)+offset))
    n=(x_n+1)*(y_n+1);fs=[];assigned=[]
    def index(i,j):return i*(y_n+1)+j
    for i in range(x_n):
        for j in range(y_n):
            fs.append((index(i,j),index(i+1,j),index(i+1,j+1),index(i,j+1)))
            assigned.append((j//4)%2)
    for i in range(x_n):
        for j in range(y_n):
            fs.append((n+index(i,j+1),n+index(i+1,j+1),n+index(i+1,j),n+index(i,j)))
            assigned.append(2)
    for i in (0,x_n):
        for j in range(y_n):
            a=index(i,j);b=index(i,j+1)
            fs.append((a,b,n+b,n+a) if i==x_n else (b,a,n+a,n+b))
            assigned.append(2)
    for j in (0,y_n):
        for i in range(x_n):
            a=index(i,j);b=index(i+1,j)
            fs.append((b,a,n+a,n+b) if j==y_n else (a,b,n+b,n+a))
            assigned.append(2)
    shell=base.new_mesh(bpy,f'CONCENTRATOR | {label} | true parabolic continuous mirror',vs,fs,mat['mirror'],col,rig)
    shell.data.materials.append(mat['mirror_highlight'])
    shell.data.materials.append(mat['iron'])
    for face,idx in zip(shell.data.polygons,assigned):
        face.material_index=idx
        face.use_smooth=(idx!=2)
    shell['parabola_equation']='z=y*y/(4*f)'
    shell['focal_height_bu']=FOCAL_HEIGHT
    shell['sun_incidence']='vertical sky rays; unobstructed concave aperture'
    shell['transverse_range_bu']=[-TROUGH_HALF_WIDTH,TROUGH_HALF_WIDTH]
    # End ribs FOLLOW the real curved bowl, not a rectangular frame.
    for x in (-TROUGH_HALF_LENGTH,TROUGH_HALF_LENGTH):
        for j in range(16):
            ya=-TROUGH_HALF_WIDTH+2*TROUGH_HALF_WIDTH*j/16
            yb=-TROUGH_HALF_WIDTH+2*TROUGH_HALF_WIDTH*(j+1)/16
            base.rod(bpy,f'CONCENTRATOR | {label} | curved end rib',
                     (x,ya,parabola(ya)+.008),(x,yb,parabola(yb)+.008),
                     .014,mat['iron'],col,rig)
    # Protect both longitudinal edges without any opaque overhead plate.
    for y in (-TROUGH_HALF_WIDTH,TROUGH_HALF_WIDTH):
        base.rod(bpy,f'CONCENTRATOR | {label} | upturned rim bead',
                 (-TROUGH_HALF_LENGTH,y,parabola(y)+.012),
                 (TROUGH_HALF_LENGTH,y,parabola(y)+.012),.016,mat['iron'],col,rig)
    for x in (-.37,.37):
        base.rod(bpy,f'CONCENTRATOR | {label} | focal pipe vertical standoff',
                 (x,0,.02),(x,0,FOCAL_HEIGHT),.017,mat['bronze'],col,rig)
        base.rod(bpy,f'CONCENTRATOR | {label} | brace to curved reflector',
                 (x,.26,parabola(.26)+.02),(x,0,FOCAL_HEIGHT-.018),
                 .009,mat['bronze'],col,rig)
    # A genuinely hollow thin receiver at the optical focus, with two rings
    # and open bores, not a heavy rod applied to a sheet of flat PV tiles.
    tube=base.annulus(bpy,f'CONCENTRATOR | {label} | focal black absorber tube',
              (0,0,FOCAL_HEIGHT),(1,0,0),.044,.027,.90,mat['absorber'],col,rig,segments=64)
    tube['optical_focal_axis']=[[-TROUGH_HALF_LENGTH,0,FOCAL_HEIGHT],[TROUGH_HALF_LENGTH,0,FOCAL_HEIGHT]]
    for x in (-.425,.425):
        base.annulus(bpy,f'CONCENTRATOR | {label} | copper absorber union',
                     (x,0,FOCAL_HEIGHT),(1,0,0),.061,.027,.05,mat['copper'],col,rig)
    return tube,shell


def add_transfer_loop(bpy,base,label,sign,rig,materials,root,col):
    """Continuous metal line from both ends of the fixed solar receiver to drum."""
    from mathutils import Vector
    bpy.context.view_layer.update()
    # Inner absorber end feeds hot thermal fluid into the copper drum.
    inner_x=.45 if sign<0 else -.45
    outer_x=-inner_x
    h=rig.matrix_world@Vector((inner_x,0,FOCAL_HEIGHT))
    c=rig.matrix_world@Vector((outer_x,0,FOCAL_HEIGHT))
    assert h.x*sign>0 and c.x*sign>0
    hpts=[tuple(h),
          (h.x,h.y-.07,h.z-.025),
          (sign*.29,.10,1.29),
          (sign*.34,-.08,1.13),
          (sign*.35,-.10,1.055)]
    cpts=[tuple(c),
          (c.x,c.y+.035,c.z-.045),
          (sign*1.01,.06,1.12),
          (sign*.83,-.06,.96),
          (sign*.70,-.10,.83)]
    for kind,points,radius in [('hot collector outlet to drum',hpts,.039),
                                ('cool thermal return from drum',cpts,.032)]:
        obj=base.hollow_sweep(bpy,f'CONCENTRATOR | {label} | continuous {kind}',points,
             [radius]*len(points),materials['copper'] if kind.startswith('hot') else materials['iron'],col,root,segments=32)
        obj['source_focal_endpoint_world']=list(points[0])
        obj['pressure_drum_endpoint_world']=list(points[-1])
        obj['thermal_loop_role']='hot-out' if kind.startswith('hot') else 'cool-return'
        # Small visibly seated unions at the pressure drum. Avoid terminal caps.
        end=points[-1]
        a=Vector(points[-1])-Vector(points[-2])
        base.annulus(bpy,f'CONCENTRATOR | {label} | {kind} | drum receiver collar',
            end,a.normalized(),radius*1.4,radius*.80,.035,materials['bronze'],col,root,segments=32)
    return {'hot_start':list(h),'cool_start':list(c),'hot_drum':list(hpts[-1]),'cool_drum':list(cpts[-1])}


def build(opts):
    import bpy
    from mathutils import Vector
    sys.path.insert(0,str(V1_ROOT))
    import build_solar_boiler_v1 as base
    self_check()
    source=(opts.source or HERE.parent/'generated-v1'/'solar-boiler-v1.blend').resolve()
    dest=opts.output.resolve()
    if dest.exists() and any(dest.iterdir()):raise FileExistsError('Refuse to overwrite prior Solar Boiler asset evidence')
    original=HERE.parent/'generated-v1'/'build-report.json'
    source_receipt=json.loads(original.read_text())
    expected=source_receipt['native_sha256']
    assert sha256(source)==expected,(sha256(source),expected)
    before=sha256(source)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene
    root=bpy.data.objects['EXPORT | rotate Solar Boiler model, never camera']
    refs=bpy.data.collections['REFERENCE ONLY | adjacent matched 1-tile pipe fixtures']
    assert refs.hide_render
    scene.frame_set(0);root.rotation_euler.z=0;bpy.context.view_layer.update()
    cameras=[o for o in bpy.data.objects if o.type=='CAMERA']
    assert len(cameras)==1 and cameras[0] is scene.camera
    original_camera=source_receipt['camera']
    def camera_record():
        ob=scene.camera
        return {'name':ob.name,'matrix_world':[list(r) for r in ob.matrix_world],
                'type':ob.data.type,'ortho_scale':ob.data.ortho_scale,
                'shift_x':ob.data.shift_x,'shift_y':ob.data.shift_y,
                'resolution':[scene.render.resolution_x,scene.render.resolution_y]}
    assert camera_record()==original_camera
    preserved={o.name:mesh_hash(o) for o in scene.objects if o.type=='MESH'
               and not o.name.startswith(REPLACE_PREFIXES)}
    discarded=[]
    for ob in list(scene.objects):
        if ob.type=='MESH' and ob.name.startswith(REPLACE_PREFIXES):
            discarded.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
    if len(discarded)<25:raise RuntimeError('Wrong V1 source: old flat collector geometry missing')
    c=bpy.data.collections.new('06 | V2 parabolic mirrors, focal absorber and real thermal circulation')
    scene.collection.children.link(c)
    mat={
        'mirror':material(bpy,'clean curved silver mirror',(.66,.69,.69),.80,.19),
        'mirror_highlight':material(bpy,'slightly brighter curved mirror faceting',(.79,.80,.73),.78,.18),
        'iron':bpy.data.materials['Solar Boiler | aged_iron'],
        'copper':bpy.data.materials['Solar Boiler | aged_copper'],
        'bronze':bpy.data.materials['Solar Boiler | bronze'],
        'absorber':bpy.data.materials['Solar Boiler | absorber']
    }
    endpoints={}
    for label,sign in (('west',-1),('east',1)):
        rig=bpy.data.objects[f'SOLAR | {label} | adjustable trough pivot']
        assert rig.parent is root
        rig.animation_data_clear()
        rig.rotation_euler.x=math.radians(TROUGH_TILT_DEG)
        rig['solar_thermal_design']='Stationary open-sky parabolic concentrator (no rigid pipe motion)'
        rig['focal_z_local_bu']=FOCAL_HEIGHT
        curved_trough(bpy,base,rig,label,c,mat)
        # The V1 saddle stops below the collector; bridge that air gap with
        # four actual steel cleats seated between saddle tops and bowl shell.
        for ylocal in (-.30,.30):
            foot=Vector((sign*.66,.25+ylocal,.99))
            seat=rig.matrix_world@Vector((0,ylocal,parabola(ylocal)-.025))
            base.rod(bpy,f'CONCENTRATOR | {label} | load-bearing collector saddle extension',
                     foot,seat,.024,mat['iron'],c,root)
        endpoints[label]=add_transfer_loop(bpy,base,label,sign,rig,mat,root,c)
    for name,digest in preserved.items():
        ob=bpy.data.objects.get(name)
        assert ob and mesh_hash(ob)==digest,('Unrelated original source mesh altered',name)
    for id in ('water-west','water-east','steam-north'):
        assert bpy.data.objects.get(f'PORT | {id} | full machine collar') is not None
    for id in ('ferrocrete','ferrocrete_light','ferrocrete_dark'):
        m=bpy.data.materials.get('TP Library | '+id)
        assert m and len([n for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.packed_file])==3
    scene['solar_boiler_revision']='V2 true parabolic thermal concentrators; not user approved'
    scene['solar_boiler_focus_bu']=FOCAL_HEIGHT
    scene['solar_boiler_v1_sha256']=expected
    scene['game_integration']=False
    scene.frame_start=0;scene.frame_end=96
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=opts.samples
    if hasattr(scene.cycles,'use_denoising'):scene.cycles.use_denoising=False
    for layer in scene.view_layers:
        if hasattr(layer.cycles,'use_denoising'):layer.cycles.use_denoising=False
    scene.render.film_transparent=True
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8'
    scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100
    scene.render.fps=8
    bpy.context.view_layer.update()
    dest.mkdir(parents=True,exist_ok=True)
    native=dest/'solar-boiler-v2.blend'
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True,check_existing=False)
    report={
      'schema':'tanks.solar-boiler.parabolic.v2','status':'3D review candidate','revision':'v2',
      'source_v1':'models/island-survival/solar-boiler/generated-v1/solar-boiler-v1.blend',
      'source_v1_sha256':expected,'source_v1_unchanged_sha256':before,
      'native_sha256':sha256(native),'blender':bpy.app.version_string,
      'model_meshes_preserved':len(preserved),'removed_flat_collector_meshes':discarded,
      'native_footprint_tiles':[3,2],
      'ports':json.loads((V1_ROOT/'port-contract.json').read_text())['ports'],
      'parabolic_concentrators':2,'parabola_z':'y^2/(4*f)',
      'focus_height_bu':FOCAL_HEIGHT,'rim_height_bu':parabola(TROUGH_HALF_WIDTH),
      'aperture_half_width_bu':TROUGH_HALF_WIDTH,'absorber_outer_diameter_bu':.088,
      'tilt_deg':TROUGH_TILT_DEG,'stationary_collector_and_continuous_thermal_lines':True,
      'solar_thermal_endpoints':endpoints,'camera':camera_record(),
      'uses_packed_fmpl_pbr':True,'visual_approved':False,'game_integrated':False,
      'renders':[]}
    record=dest/'build-report.json'
    record.write_text(json.dumps(report,indent=2)+'\n')
    if opts.render=='none':return
    for state,timeline in (('idle',0),('working',25)):
        for i,yaw in enumerate(DIRECTIONS):
            root.rotation_euler.z=math.radians(yaw)
            scene.frame_set(timeline);refs.hide_render=True
            bpy.context.view_layer.update()
            assert camera_record()==original_camera
            filename=f'{state}-d{i:02d}.png'
            scene.render.filepath=str(dest/filename)
            print('SOLAR_V2_GENUINE_CYCLES_RENDER',state,i,flush=True)
            bpy.ops.render.render(write_still=True)
            report['renders'].append({'state':state,'index':i,'yaw':yaw,'frame':timeline,
                                     'file':filename,'sha256':sha256(dest/filename)})
            record.write_text(json.dumps(report,indent=2)+'\n')
    root.rotation_euler.z=0;scene.frame_set(0)
    assert sha256(source)==before
    print('SOLAR_V2_PARABOLIC_BLEND_AND_EIGHT_PROOFS_COMPLETE',len(report['renders']),flush=True)


def main():
    if '--self-check' in sys.argv:
        self_check();return
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--samples',type=int,default=24)
    p.add_argument('--render',choices=('none','proof'),default='proof')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError('samples must be 4..64')
    build(args)

if __name__=='__main__':main()
