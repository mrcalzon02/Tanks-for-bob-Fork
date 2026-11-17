# REJECTED WRONG SOURCE: Tech-Priests hydrogen compressor. Historical script only.
raise RuntimeError("Owner rejected this source. Use steam-compressor/v2/finish_barrel.py")
"""Derive Tanks' burner/canister compressor without replacing the saved mechanism."""
import bpy
import bmesh
import hashlib
import json
import math
from pathlib import Path
import sys
from mathutils import Vector

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
SHARED=REPO.parent/'model-production'
SOURCE=SHARED/'art/source-to-3d/metallic-hydrogen-chain/hydrogen-compressor/v05-slow-and-audio/compressor-v05.blend'
OUT=REPO/'models/island-survival/steam-compressor/candidates/v1-reuse01'
sys.path.insert(0,str(REPO/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box,cylinder,tube,lathe
import surfaces
sys.path.insert(0,str(SHARED/'tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')

def main():
    assert sha(SOURCE)=='29e62716acc5fa52bb4cedc8f3b4f713ac3fb857cb42b46714749910da4013ad'
    if OUT.exists():raise FileExistsError(OUT)
    OUT.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
    scene=bpy.context.scene;scene.frame_set(1)
    original=list(scene.objects)
    removed=[]
    for o in original:
        n=o.name.lower()
        if o.type=='MESH' and (any(k in n for k in ['cogitator','console','electric drive motor','motor cooling fin','motor mounting leg','equipment footing','full size receiving barrel','cast mouth reducer']) or o.get('library_instance') in ('hydrogen_suction','hydrogen_discharge')):
            removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
    root=bpy.data.objects.new('EXPORT | Tanks compressor all parts',None);scene.collection.objects.link(root)
    mechanism=bpy.data.objects.new('REUSE | unchanged crank geometry and eight-second cycle',None);scene.collection.objects.link(mechanism)
    mechanism.parent=root;mechanism.scale=(.72,)*3
    for o in list(scene.objects):
        if o not in (root,mechanism) and o.type in ('MESH','EMPTY') and o.parent is None:o.parent=mechanism
    mats=surfaces.create(OUT)
    for m in mats.values():
        m.name=m.name.replace('PUMP V3','TANKS COMPRESSOR V1');m['surface_authorship']='Compressor-specific role assignment and physical UV placement'
    for o in list(scene.objects):
        if o.type!='MESH':continue
        if any(k in o.name for k in ['bed rail','bed tie','guide bearing pedestal','shaft bearing tower','header support post']):
            surfaces.apply(o,mats['wood'],mats['endgrain'])
        elif 'closed horizontal compressor cylinder' in o.name:
            # Keep existing cylinder-specific UV/image materials and all pressure seams.
            o['tanks_role']='Retained pressure cylinder and original image maps'
    collection=bpy.data.collections.new('TANKS | timber burner canister and native sockets');scene.collection.children.link(collection)
    def B(n,p,d,m):
        o=box('TANKS | '+n,p,d,m,collection,root);surfaces.apply(o,m,mats['endgrain'] if m==mats['wood'] else None);return o
    def C(n,p,r,d,m,axis='Z'):
        o=cylinder('TANKS | '+n,p,r,d,m,collection,root,axis);surfaces.apply(o,m);return o
    def T(n,points,outer=.065,inner=.044):
        samples=[]
        for i,p in enumerate(points):
            a=Vector(points[max(0,i-1)]);b=Vector(points[min(len(points)-1,i+1)])
            samples.append((p,(b-a).normalized(),outer,inner))
        o=tube('TANKS | '+n,samples,mats['copper'],collection,root);return o
    for x in (-.82,.82):
        for y in (-1.15,1.1):B('stone footing', (x,y,.045),(.32,.32,.09),mats['brick'])
    for x in (-.78,-.39,0,.39,.78):B('timber bed plank '+str(x),(x,0,.095),(.37,2.75,.07),mats['wood'])
    # A fuel-fired steam driver occupies the saved electric drive's mounting bay.
    for z in (.17,.29):
        for y in (-1.06,-.82):B('firebox brick course',(-.74,y,z),(.43,.115,.115),mats['brick'])
        for x in (-.94,-.54):B('firebox end brick',(x,-.94,z),(.105,.3,.115),mats['brick'])
    B('firebox iron front',(-.74,-1.123,.245),(.31,.025,.21),mats['iron'])
    B('fire door handle',(-.74,-1.145,.25),(.11,.035,.027),mats['bronze'])
    C('copper steam drive jacket',(-.74,-.94,.45),.20,.25,mats['copper'])
    C('steam driver lid',(-.74,-.94,.59),.215,.035,mats['bronze'])
    C('steam-driver shaft bearing',(-.74,-.9,.562),.085,.20,mats['bronze'],'X')
    T('firebox chimney',[(-.91,-.84,.34),(-.96,-.8,.6),(-.96,-.8,1.03)],.047,.032)
    # Removable canister is clamped to the pressure manifold on a supported shelf.
    B('canister filling shelf',(.0,1.0,.29),(.5,.48,.09),mats['wood'])
    for x in (-.2,.2):B('shelf leg',(x,1.02,.205),(.07,.07,.2),mats['wood'])
    C('removable steam canister',(0,1.0,.57),.15,.47,mats['copper'])
    for z in (.38,.75):C('canister iron hoop',(0,1.0,z),.16,.035,mats['iron'])
    C('canister neck',(0,1.0,.84),.048,.08,mats['bronze'])
    T('canister filling neck',[(0,1.0,.88),(0,.91,.93),(0,.72,.93),(0,.54,.89)],.034,.021)
    # Correct ports stay fixed in the entity frame; opposite faces at native height.
    # The widened mouth is the same measured .245 bore/.34 collar as the reference.
    for label,sign in [('north inlet',1),('south recovery outlet',-1)]:
        T(label+' fixed socket',[(0,sign*1.5,.36),(0,sign*1.425,.36),(0,sign*1.30,.36)],.285,.245)
        T(label+' collar',[(0,sign*1.5,.36),(0,sign*1.425,.36)],.34,.245)
    # Route outside the retained cranks and below the pressure headers.
    T('inlet manifold route',[(0,1.30,.36),(-.28,1.18,.36),(-.78,1.18,.36),(-.78,.8,.50),(-.78,.36,.56)])
    T('recovery manifold route',[(0,-1.30,.36),(.3,-1.22,.36),(.84,-1.22,.36),(.84,-.5,.36),(.84,.36,.56)])
    T('driver steam feed',[(-.74,-.94,.60),(-.86,-.75,.64),(-.86,.15,.86),(-.78,.15,.86)],.027,.017)
    # Clean evaluated degenerate triangles only; do not merge intentional joints.
    repaired={}
    for o in scene.objects:
        if o.type!='MESH':continue
        if not o.data.uv_layers:surfaces.physical_box_uv(o)
        o.data.calc_loop_triangles();bad=sum(t.area<1e-12 for t in o.data.loop_triangles)
        if bad:
            bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
            bm.to_mesh(o.data);bm.free();repaired[o.name]=bad
    profile=json.loads((SHARED/'art/source-to-3d/metallic-hydrogen-chain/hydrogen-compressor/v05-slow-and-audio/captures/export-config.json').read_text())
    profile.update(asset='tanks-steam-compressor-v1',source_size=256,fps=2,states={'idle':[0],'working':list(range(1,193,12))})
    profile['camera_override'].update(target=[0,0,.6],ortho_scale=4.8)
    install_canonical_camera(scene,profile,bpy);scene.render.film_transparent=True
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
    scene.frame_set(0);bpy.ops.file.pack_all();assert_clean(scene,profile,bpy)
    target=OUT/'steam-compressor-v1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(target));scene=bpy.context.scene
    root=bpy.data.objects[root.name] if False else bpy.data.objects['EXPORT | Tanks compressor all parts']
    bpy.ops.object.select_all(action='DESELECT')
    for o in [root,*root.children_recursive]:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/'steam-compressor-v1.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
    write('capture-profile.json',profile)
    write('reuse-receipt.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE),derivative_sha256=sha(target),removed_only_from_derivative=removed,mechanism_scale=.72,retained_eight_second_motion=True,degenerate_repairs=repaired,native_game_verified=False,owner_visual_approved=False))
    projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
    for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
        root.rotation_euler.z=math.radians(yaw);scene.frame_set(25);assert_clean(scene,profile,bpy)
        scene.render.filepath=str(OUT/('pilot-'+facing+'.png'));bpy.ops.render.render(write_still=True)
    print('TANKS_COMPRESSOR_REUSE_SAVED',target,flush=True)

if __name__=='__main__':main()
