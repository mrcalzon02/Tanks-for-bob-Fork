"""Authored construction/surface revision of the real two-port primitive pump."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import sys

import bpy
import bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import mesh_util as mu
import surfaces

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

v2=load_module('pump_v2',HERE.parent/'v2/refine_pipe_pump.py')
SPEC=json.loads((HERE/'contract.json').read_text())

def geometry_hash(obj):
    h=hashlib.sha256()
    for v in obj.data.vertices:h.update(struct.pack('<3f',*v.co))
    for p in obj.data.polygons:h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
    return h.hexdigest()

def remove_prefixes(prefixes):
    for obj in list(bpy.context.scene.objects):
        if any(obj.name.startswith(s) for s in prefixes):bpy.data.objects.remove(obj,do_unlink=True)

def boolean_bore(obj,position,radius,depth,axis='Y'):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=position)
    cutter=bpy.context.object
    if axis=='Y':cutter.rotation_euler.x=math.pi/2
    elif axis=='X':cutter.rotation_euler.y=math.pi/2
    mod=obj.modifiers.new('Actual fitted bore','BOOLEAN')
    mod.object,mod.operation=cutter,'DIFFERENCE'
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

def clean_applied(obj):
    bpy.context.view_layer.objects.active=obj
    for modifier in list(obj.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data);bm.free();obj.data.update()

def make_ring(name,pos,outer,inner,height,mat,collection,parent):
    x,y,z=pos
    return mu.lathe(name,[(outer,z-height/2),(outer,z+height/2),(inner,z+height/2),(inner,z-height/2)],(x,y),mat,collection,parent)

def construct(args,out):
    assert v2.sha(args.source)==SPEC['source_sha256']
    bpy.ops.wm.open_mainfile(filepath=str(args.source))
    scene=bpy.context.scene;scene.frame_set(1)
    root=bpy.data.objects['EXPORT | rotate primitive steam-powered pump, never camera']
    root.rotation_euler=(0,0,0)
    ports=[o for o in root.children_recursive if o.name.startswith('PORT | ')]
    port_records={o.name:{'mesh':geometry_hash(o),'matrix':[list(r) for r in o.matrix_world]} for o in ports}
    mats=surfaces.create(out)
    all_objects=list(root.children_recursive)
    for obj in all_objects:
        if obj.type!='MESH' or obj in ports:continue
        names=[m.name.lower() for m in obj.data.materials if m]
        if any('driftwood' in n for n in names):surfaces.apply(obj,mats['wood'],mats['endgrain'])
        elif any('forged iron' in n for n in names):surfaces.apply(obj,mats['iron'])
        elif any('oxidized copper' in n for n in names):surfaces.apply(obj,mats['copper'])
        elif any('brass collar' in n for n in names):surfaces.apply(obj,mats['bronze'])
    # Exact port geometry stays untouched; finishing changes only its material.
    for obj in ports:
        obj.data.materials.clear();obj.data.materials.append(mats['bronze' if obj.name.endswith('machine_collar') else 'iron'])
        surfaces.physical_box_uv(obj)
    construction=bpy.data.collections.new('V3 | authored firebox, jacket and fitted flow passages')
    scene.collection.children.link(construction)
    remove_prefixes(('PIPE | ','FIREBOX | ','STEAM | ','PUMP | forged upright pressure barrel','PUMP | bronze retaining band','PUMP | upper sealing band'))
    # Shorter skid ends clear the preserved standard full-bore port throats.
    for obj in root.children_recursive:
        if obj.name.startswith('FRAME | rough lengthwise timber runner'):
            for vertex in obj.data.vertices:vertex.co.y*=1.28/1.60
            surfaces.physical_box_uv(obj,True)
        if obj.name.startswith('FRAME | independent blackened steel riser'):obj.location.y-=.07
    # A real hollow pressure barrel, with a floor and bored side junctions.
    body=mu.lathe('V3 PRESSURE | hollow cast pump barrel',[(0,.38),(.215,.38),(.215,1.08),(.178,1.08),(.178,.41),(0,.41)],(0,-.16),mats['iron'],construction,root)
    boolean_bore(body,(0,-.375,.53),.141,.26)
    boolean_bore(body,(0,.035,.77),.091,.24)
    clean_applied(body)
    for z in (.46,1.05):
        ring=make_ring('V3 PRESSURE | seated bronze gland',(0,-.16,z),.229,.214,.052,mats['bronze'],construction,root)
        for i in range(6):
            a=i*math.tau/6
            mu.cylinder('V3 PRESSURE | mounted gland bolt',(.225*math.cos(a),-.16+.225*math.sin(a),z+.029),.012,.018,mats['iron'],construction,root,segments=6)
    # No pipe wall exceeds its elbow's bend radius. External mouth geometry and
    # full bore are retained; reductions occur inside the machine.
    inlet=mu.join_samples(
        mu.line_samples((0,-.71,.36),(0,-.51,.36),(.285,.245),(.14,.10)),
        mu.arc_samples(-.51,.52,.16,-math.pi/2,0,.14,.10),
        mu.line_samples((0,-.35,.52),(0,-.35,.56),(.14,.10),steps=3))
    outlet=mu.join_samples(
        mu.line_samples((0,-.04,.77),(0,.055,.77),(.09,.06),steps=4),
        mu.arc_samples(.055,.62,.15,math.pi/2,0,.09,.06),
        mu.line_samples((0,.205,.62),(0,.205,.46),(.09,.06),steps=5),
        mu.arc_samples(.305,.46,.10,math.pi,math.pi*1.5,.09,.06),
        mu.line_samples((0,.305,.36),(0,.52,.36),(.09,.06)),
        mu.line_samples((0,.52,.36),(0,.71,.36),(.09,.06),(.285,.245)))
    inlet_obj=mu.tube('V3 FLOW | hollow inlet reducer and circular elbow',inlet,mats['iron'],construction,root)
    outlet_obj=mu.tube('V3 FLOW | hollow discharge beneath firebox',outlet,mats['copper'],construction,root)
    # The hot assembly has its own load path into the right-hand structural skid.
    for y in (.22,.48):
        mu.box('V3 HEARTH | anchored cantilever bearer',(.25,y,.3325),(.28,.065,.045),mats['iron'],construction,root)
        for x in (.15,.32):
            mu.box('V3 HEARTH | supported short leg',(x,y,.415),(.045,.045,.15),mats['iron'],construction,root)
        for x in (.30,.36):mu.cylinder('V3 HEARTH | skid anchor bolt',(x,y,.365),.012,.025,mats['bronze'],construction,root,segments=6)
    mu.box('V3 HEARTH | cast bottom tray',(.235,.35,.50),(.32,.39,.035),mats['iron'],construction,root)
    # Individually bedded refractory bricks; the outer side contains a real door aperture.
    for layer in range(3):
        z=.555+layer*.096
        for y in (.215,.35,.485):
            mu.box('V3 HEARTH | left refractory course',(.117,y,z),(.035,.127,.088),mats['brick'],construction,root,.006)
            if layer!=1 or y!=.35:
                mu.box('V3 HEARTH | door-side refractory course',(.353,y,z),(.035,.127,.088),mats['brick'],construction,root,.006)
        for y in (.165,.535):
            for x in (.177,.293):mu.box('V3 HEARTH | front and rear refractory course',(x,y,z),(.108,.034,.088),mats['brick'],construction,root,.005)
    mu.box('V3 HEARTH | seated boiler cap plate',(.235,.35,.825),(.32,.39,.04),mats['iron'],construction,root)
    # Fuel door, frame, grate and hinges actually mount to the brick opening.
    for y in (.268,.432):mu.box('V3 DOOR | jamb',(.381,y,.65),(.022,.022,.20),mats['iron'],construction,root,.004)
    for z in (.55,.75):mu.box('V3 DOOR | lintel and sill',(.381,.35,z),(.022,.184,.023),mats['iron'],construction,root,.004)
    mu.box('V3 DOOR | cast hinged panel',(.393,.35,.665),(.018,.14,.145),mats['iron'],construction,root,.007)
    for y in (.31,.35,.39):mu.box('V3 DOOR | lower draft grille',(.397,y,.568),(.018,.012,.035),mats['bronze'],construction,root,.002)
    for z in (.60,.72):mu.cylinder('V3 DOOR | seated hinge barrel',(.405,.427,z),.013,.043,mats['iron'],construction,root)
    mu.cylinder('V3 DOOR | latch pivot',(.408,.30,.68),.014,.028,mats['bronze'],construction,root,axis='X')
    mu.box('V3 DOOR | latch lever',(.426,.30,.68),(.012,.06,.013),mats['bronze'],construction,root,.003)
    # Single joined pressure jacket profile, seated directly on the lined hearth.
    jacket=mu.lathe('V3 BOILER | joined copper jacket and shouldered dome',[(0,.846),(.136,.846),(.153,.865),(.158,.91),(.158,1.12),(.151,1.18),(.13,1.225),(.085,1.26),(.052,1.275),(.052,1.365),(0,1.365)],(.235,.35),mats['copper'],construction,root)
    for z in (.885,1.125):
        make_ring('V3 BOILER | fitted iron pressure band',(.235,.35,z),.165,.157,.034,mats['iron'],construction,root)
        for i in range(8):
            a=i*math.tau/8
            mu.cylinder('V3 BOILER | supported band fastener',(.160*math.cos(a)+.235,.160*math.sin(a)+.35,z+.021),.009,.012,mats['bronze'],construction,root,segments=6)
    mu.cylinder('V3 RELIEF | threaded valve base',(.235,.35,1.385),.065,.043,mats['bronze'],construction,root)
    mu.cylinder('V3 RELIEF | pressure stem',(.235,.35,1.425),.018,.055,mats['iron'],construction,root)
    mu.box('V3 RELIEF | mounted weighted lever',(.235,.35,1.457),(.115,.025,.016),mats['bronze'],construction,root,.005)
    # Small internal steam feed. It is part of the machine, never a third native port.
    steam=mu.join_samples(mu.line_samples((.235,.18,1.12),(.235,.06,1.12),(.027,.018)),mu.line_samples((.235,.06,1.12),(.14,-.08,1.12),(.027,.018)))
    # Retain separate engineered unions at the angled feed rather than pretending
    # this short internal joint is the canonical full-bore liquid pipe.
    mu.tube('V3 STEAM | internal boiler-to-drive feed',steam,mats['copper'],construction,root,segments=32)
    for xyz in ((.235,.18,1.12),(.14,-.08,1.12)):
        mu.cylinder('V3 STEAM | fitted drive union',xyz,.037,.038,mats['bronze'],construction,root,axis='Y',segments=24)
    # Crosshead guide holes and bronze sleeves; move the rod to a clear parallel plane.
    piston=bpy.data.objects['MOTION | vertically reciprocating piston']
    wheel=bpy.data.objects['MOTION | keyed lateral 3D drive flywheel']
    link=bpy.data.objects['MOTION | hinged connecting rod']
    pin=bpy.data.objects['MOTION | crank eccentric pin']
    head=bpy.data.objects['V2 JOINT | real crosshead pivot']
    pin.location.x=.105
    for v in pin.data.vertices:v.co.z*=.21/.095
    head.location.x=.375
    crosshead=bpy.data.objects['MOTION | crosshead on straight guides']
    for v in crosshead.data.vertices:v.co.x*=.80/.74
    bpy.context.view_layer.update()
    for x in (-.30,.30):
        boolean_bore(crosshead,(x,-.16,1.53+piston.location.z),.032,.30,'Z')
        sleeve=make_ring('V3 GUIDE | moving bronze crosshead sleeve',(x,-.16,1.53),.031,.024,.11,mats['bronze'],construction,piston)
    clean_applied(crosshead)
    crosshead.data.materials.clear();crosshead.data.materials.append(mats['wood']);crosshead.data.materials.append(mats['endgrain'])
    surfaces.physical_box_uv(crosshead,True)
    for obj in root.children_recursive:
        if obj.name.startswith('FRAME | narrow crosshead guide'):
            for v in obj.data.vertices:v.co.z*=.65/.61
            obj.location.z+=.02
    for x in (-.30,.30):
        mu.cylinder('V3 GUIDE | fixed upper stop',(x,-.16,1.735),.035,.025,mats['bronze'],construction,root)
        for z in (1.09,1.39):
            mu.box('V3 GUIDE | riser-mounted guide bracket',(x,-.26,z),(.075,.23,.035),mats['iron'],construction,root)
    for obj in (piston,wheel,link):obj.animation_data_clear()
    for frame in range(1,98):
        phase=(frame-1)*math.tau/96
        crank=Vector((.375,-.15-.103*math.sin(phase),.94+.103*math.cos(phase)))
        end=Vector((.375,-.16,crank.z+math.sqrt(.6**2-(-.16-crank.y)**2)))
        wheel.rotation_euler.x=phase;piston.location.z=end.z-1.54
        link.location=(end+crank)/2;link.rotation_quaternion=(end-crank).to_track_quat('Z','Y')
        for obj,field in ((wheel,'rotation_euler'),(piston,'location'),(link,'location'),(link,'rotation_quaternion')):obj.keyframe_insert(data_path=field,frame=frame)
    for obj in (piston,wheel,link):v2.linear_keys(obj)
    # Actual dial face/ticks, with the preserved keyed needle in front of it.
    ivory=bpy.data.materials.new('PUMP V3 | ivory gauge enamel');ivory.use_nodes=True
    ivory.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.67,.61,.43,1)
    ivory.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.58
    mu.cylinder('V3 GAUGE | inset ivory dial',(-.26,.199,1.23),.106,.006,ivory,construction,root,axis='Y')
    for i in range(11):
        a=math.radians(-130+i*26)
        obj=mu.box('V3 GAUGE | engraved tick',(-.26+.083*math.sin(a),.194,1.23+.083*math.cos(a)),(.007,.003,.016),mats['iron'],construction,root,.001)
        obj.rotation_euler.y=a
    mu.cylinder('V3 GAUGE | mounted needle spindle',(-.26,.184,1.23),.018,.018,mats['bronze'],construction,root,axis='Y',segments=24)
    # Assign physical UVs to newly built pieces, retaining the tube unwraps.
    for obj in construction.objects:
        if obj.type=='MESH' and not obj.data.uv_layers:surfaces.physical_box_uv(obj)
    for obj in ports:
        assert geometry_hash(obj)==port_records[obj.name]['mesh'],obj.name
    scene.frame_set(1);bpy.context.view_layer.update()
    for obj in ports:
        assert max(abs(obj.matrix_world[i][j]-port_records[obj.name]['matrix'][i][j]) for i in range(4) for j in range(4))<1e-7
    profile=json.loads((args.source.parent/'capture-profile.json').read_text())
    from blender_camera_guard import install_canonical_camera,assert_clean
    install_canonical_camera(scene,profile,bpy)
    assert_clean(scene,profile,bpy)
    scene['construction_revision']='V3 authored lined firebox, seated jacket, hollow circular elbows and clear rigid drive'
    scene['surface_plan']=json.dumps(SPEC['surface_plan'])
    scene['crank_plane_x']=.375
    scene.cycles.samples=64;scene.cycles.use_denoising=False
    bpy.data.orphans_purge(do_recursive=True)
    v2.record(out/'capture-profile.json',profile)
    v2.record(out/'construction-receipt.json',{'source_sha256':v2.sha(args.source),'builder_sha256':v2.sha(__file__),
        'immutable_ports':port_records,'circular_elbow_clearance_tiles':{'inlet':.02,'discharge_upper':.06,'discharge_lower':.01},
        'rod_guide_minimum_x_clearance_tiles':.375-.031-(.30+.023),
        'firebox_discharge_x_clearance_tiles':.0995-.09,
        'remaining':'Independent source/export geometry, motion, clearance and actual visual inspection required; not approved'})
    return scene,root,profile

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--fmpl-tools',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);args.source=args.source.resolve();out=args.out.resolve()
    if out.exists():raise FileExistsError(out)
    out.mkdir(parents=True);sys.path.insert(0,str(args.fmpl_tools.resolve()))
    scene,root,profile=construct(args,out)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'pipe-pump-v3.blend'),compress=True)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [root,*list(root.children_recursive)]:obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out/'pipe-pump-v3.glb'),export_format='GLB',use_selection=True,
        export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,
        export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
    from blender_camera_guard import assert_clean
    renders=[]
    for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw)
        for frame in (1,49):
            scene.frame_set(frame);assert_clean(scene,profile,bpy)
            path=out/(facing+'-working-'+str(frame)+'.png');scene.render.filepath=str(path)
            bpy.ops.render.render(write_still=True)
            renders.append({'file':path.name,'frame':frame,'sha256':v2.sha(path)})
    v2.record(out/'candidate-receipt.json',{'source_sha256':v2.sha(out/'pipe-pump-v3.blend'),'glb_sha256':v2.sha(out/'pipe-pump-v3.glb'),
        'renders':renders,'game_integrated':False,'visual_approved':False,'overall_finished':False})
    print('AUTHORED_PIPE_PUMP_V3_BUILT',str(out),flush=True)

if __name__=='__main__':main()
