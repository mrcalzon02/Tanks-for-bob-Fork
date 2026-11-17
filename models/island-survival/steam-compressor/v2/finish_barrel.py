"""Finish the owner-identified barrel/frame source as Tanks' canister compressor."""
import bpy,bmesh,hashlib,json,math,sys,tempfile
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[3]
SOURCE=REPO/'models/island-survival/steam-condenser/candidates/v1-production01/steam-condenser-v1.blend'
OUT=REPO/'models/island-survival/steam-compressor/candidates/v2-barrel02'
sys.path.insert(0,str(REPO/'models/island-survival/primitive-steam-powered-pump/v3'))
from mesh_util import box,cylinder,tube
import surfaces
sys.path.insert(0,str(REPO.parent/'model-production/tools/fmpl'))
from blender_camera_guard import install_canonical_camera,assert_clean
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def curves(o):
    if not o.animation_data or not o.animation_data.action:return []
    return [c for l in o.animation_data.action.layers for s in l.strips for b in s.channelbags for c in b.fcurves]
if OUT.exists():raise FileExistsError(OUT)
OUT.mkdir(parents=True)
temp=REPO/'build/compressor-export-temp';temp.mkdir(exist_ok=True);tempfile.tempdir=str(temp)
assert sha(SOURCE)=='b943a54aa0cd35ead07971f71f8d8c45936bf29ca1c425f597b21f3b15ca46f7'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene;scene.frame_set(1)
root=bpy.data.objects['EXPORT | rotate Tanks Steam Condenser, never camera']
root.name='EXPORT | Tanks barrel compressor all parts';root['prototype']='Steam-Compressor';root['source_identity']='Owner identified build_steam_condenser_v1.py; historical label corrected'
preserved={o.name:[list(v.co) for v in o.data.vertices] for o in root.children_recursive if o.type=='MESH'}
removed=[]
for o in list(root.children_recursive):
    if o.name.startswith(('MOISTURE |','STEAM |')) or 'visibly blue retained water' in o.name:
        removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
mats=surfaces.create(OUT)
for mat in mats.values():
    mat.name=mat.name.replace('PUMP V3','TANKS BARREL COMPRESSOR');mat['surface_authorship']='Barrel compressor role-specific maps and physical part UVs'
for o in root.children_recursive:
    if o.type!='MESH':continue
    n=o.name
    if 'pressure drum' in n or 'separate stave' in n or 'weathered timber' in n or 'lateral bracing' in n:surfaces.apply(o,mats['wood'],mats['endgrain'])
    elif 'closed copper crown' in n or 'copper serpentine' in n:surfaces.apply(o,mats['copper'])
    elif 'bronze hoop' in n:surfaces.apply(o,mats['bronze'])
    elif 'inspectable sight tube' in n:
        surfaces.apply(o,mats['copper']);o.name='CANISTER | removable copper charging vessel'
    elif 'sealed brass cap' in n:
        surfaces.apply(o,mats['bronze']);o.name=n.replace('GLASS |','CANISTER |')
    elif 'COOLING | fin' in n:surfaces.apply(o,mats['iron'])
collection=bpy.data.collections.new('COMPRESSOR | fuel drive crank piston and canister');scene.collection.children.link(collection)
def B(n,p,d,m,parent=root):
    o=box('COMPRESSOR | '+n,p,d,m,collection,parent);surfaces.apply(o,m,mats['endgrain'] if m==mats['wood'] else None);return o
def C(n,p,r,d,m,axis='Z',parent=root):
    o=cylinder('COMPRESSOR | '+n,p,r,d,m,collection,parent,axis);surfaces.apply(o,m);return o
def T(n,pts,r=.035,bore=.022):
    samples=[]
    for i,p in enumerate(pts):samples.append((p,(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)])).normalized(),r,bore))
    return tube('COMPRESSOR | '+n,samples,mats['copper'],collection,root)
# Reuse the saved vanes as a primitive flywheel/crank, with grounded timber bearings.
rotor=bpy.data.objects['COOLING | rotating vane drive']
rotor.name='MECHANISM | reused four-arm crank wheel'
bearing=bpy.data.objects.new('MECHANISM | fixed horizontal shaft frame',None);scene.collection.objects.link(bearing)
bearing.parent=root;bearing.location=(0,0,2.42);bearing.rotation_euler.x=math.pi/2
rotor.parent=bearing;rotor.location=(0,0,0);rotor.scale=(.45,)*3
for x in (-.87,.87):
    for y in (-.28,.28):B('grounded crank tower',(x,y,1.34),(.11,.12,2.16),mats['wood'])
for y in (-.28,.28):
    B('bearing bridge',(0,y,2.33),(1.85,.14,.12),mats['wood'])
    C('shaft pillow bearing',(0,y,2.42),.075,.12,mats['bronze'],'Y')
C('horizontal crank shaft',(0,0,2.42),.035,.68,mats['iron'],'Y')
sleeve=C('pressure piston gland',(0,.10,1.815),.075,.06,mats['bronze'])
piston=C('working piston',(0,.10,1.92),.036,.40,mats['iron'])
slider=B('guided crosshead',(0,.10,2.0),(.16,.10,.07),mats['bronze'])
for x in (-.13,.13):C('crosshead guide',(x,.10,2.09),.018,.42,mats['iron'])
rod=C('rigid connecting rod',(0,.10,2.16),.025,.36,mats['iron'])
pin=C('retained crank pin',(0,.10,2.42),.038,.16,mats['bronze'],'Y')
# Two clay fireboxes reflect the actual two-cooking-fire building ingredient.
for x in (-.83,.83):
    B('refractory firebox sole',(x,.68,.12),(.46,.45,.12),mats['brick'])
    for z in (.23,.35):
        for y in (.50,.85):B('firebox brick wall',(x,y,z),(.46,.10,.115),mats['brick'])
        for xx in (x-.18,x+.18):B('firebox side brick',(xx,.68,z),(.10,.26,.115),mats['brick'])
    B('iron stoke door',(x,.435,.28),(.30,.035,.22),mats['iron'])
    B('stoke door handle',(x,.409,.28),(.12,.035,.025),mats['bronze'])
    C('steam heating cap',(x,.68,.45),.23,.12,mats['copper'])
    T('heated steam branch',[(x,.68,.51),(x,.58,.65),(x*.7,.45,.8)])
    T('firebox exhaust',[(x+.16,.75,.45),(x+.22,.75,.7),(x+.22,.75,1.0)],.035,.024)
B('canister cradle',(.83,-.18,.64),(.38,.35,.07),mats['wood'])
T('canister charging valve',[(.83,-.18,1.42),(.70,-.18,1.46),(.62,-.18,1.46)],.027,.016)
# One rotating crank, one rigid rod, one guided piston; all joints share endpoints.
scene.render.fps=24;scene.frame_start=1;scene.frame_end=97
for o in (rotor,piston,slider,rod,pin):
    o.animation_data_clear()
for f in range(1,98):
    a=(f-1)*math.tau/96
    crank=Vector((.15*math.cos(a),.10,2.42+.15*math.sin(a)))
    slide=Vector((0,.10,crank.z-math.sqrt(.36**2-crank.x**2)))
    rotor.rotation_euler.z=a
    # Wheel local Y becomes world Z after the bearing's 90deg rotation.
    pin.location=crank
    slider.location=slide
    piston.location=(0,.10,slide.z-.20)
    rod.location=(crank+slide)/2;rod.rotation_euler=(crank-slide).to_track_quat('Z','Y').to_euler()
    for o in (rotor,piston,slider,pin):o.keyframe_insert(data_path='rotation_euler' if o==rotor else 'location',frame=f)
    rod.keyframe_insert(data_path='location',frame=f);rod.keyframe_insert(data_path='rotation_euler',frame=f)
for o in root.children_recursive:
    for curve in curves(o):
        for key in curve.keyframe_points:key.interpolation='LINEAR'
    if o.type=='MESH' and not o.data.uv_layers:surfaces.physical_box_uv(o)
profile={'camera_policy':'fmpl.factorio45.v1','capture_kind':'entity','orientation_policy':'rotatable','directions':[0,90,180,270],'states':{'idle':[0],'working':list(range(1,92,6))},'source_size':256,'fps':4,'camera_override':{'type':'ORTHO','elevation_deg':45,'azimuth_deg':0,'distance':math.sqrt(72),'ortho_scale':5.6,'target':[0,0,1.1]}}
install_canonical_camera(scene,profile,bpy);scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.film_transparent=True
scene.frame_set(1);bpy.ops.file.pack_all();assert_clean(scene,profile,bpy)
native=OUT/'steam-compressor-v2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(native));scene=bpy.context.scene;root=bpy.data.objects['EXPORT | Tanks barrel compressor all parts']
bpy.ops.object.select_all(action='DESELECT')
for o in [root,*root.children_recursive]:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'steam-compressor-v2.glb'),export_format='GLB',use_selection=True,export_cameras=False,export_lights=False,export_animations=True,export_animation_mode='SCENE',export_anim_scene_split_object=False,export_frame_range=True,export_force_sampling=True,export_frame_step=1,export_apply=True,export_extras=True)
(OUT/'capture-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
unchanged=[o.name for o in root.children_recursive if o.type=='MESH' and o.name in preserved and [list(v.co) for v in o.data.vertices]==preserved[o.name]]
(OUT/'reuse-receipt.json').write_text(json.dumps(dict(source=str(SOURCE.relative_to(REPO)),source_sha256=sha(SOURCE),derivative_sha256=sha(native),unchanged_meshes=unchanged,removed_condensation_effects=removed,original_source_preserved=sha(SOURCE)=='b943a54aa0cd35ead07971f71f8d8c45936bf29ca1c425f597b21f3b15ca46f7',owner_identified_source=True,owner_visual_approved=False,native_game_verified=False),indent=2)+'\n')
projection=bpy.data.objects.new('SPRITE ONLY | square ground grid',None);scene.collection.objects.link(projection);projection.scale.y=math.sqrt(2);root.parent=projection
for facing,yaw in [('north',0),('east',270),('south',180),('west',90)]:
    root.rotation_euler.z=math.radians(yaw);scene.frame_set(25);assert_clean(scene,profile,bpy)
    scene.render.filepath=str(OUT/(facing+'-pilot.png'));bpy.ops.render.render(write_still=True)
print('OWNER_BARREL_COMPRESSOR_SAVED',len(unchanged),flush=True)
