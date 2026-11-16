"""True 3D material icon pilots; source and runtime exports live in the owning repository."""
import argparse,json,math,random,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_hydrogen_resource_models as p
from material_icon_registry import ROOT,PILOTS,folder
from unit_icon_pose import pose_matrix,PRESETS
from material_icon_geometry import BUILDERS as EXTRA,COLORS
from blender_camera_guard import install_canonical_camera,assert_clean
def mats(id):
 values={'clay':((.31,.135,.058),0,.83,0,.45),'fired':((.32,.075,.035),0,.84,0,.35),
  'pulp':((.50,.42,.25),0,.95,0,.22),'paper':((.64,.59,.43),0,.93,0,.16),
  'char':((.055,.060,.057),0,.91,0,.5),'ash':((.21,.22,.20),0,.98,0,.35),
  'glass':((.018,.032,.05),.05,.17,0,.06),'ink':((.008,.01,.018),0,.14,0,.03),
  'brass':((.32,.20,.055),.8,.35,0,.19),'steel':((.24,.26,.25),.8,.4,0,.18),
  'dark':((.025,.031,.026),.35,.67,0,.20),'cloth':((.14,.16,.07),0,.96,0,.25),
  'leather':((.09,.05,.025),0,.79,0,.22),'stitch':((.43,.38,.23),0,.93,0,.2),
  'green':((.15,.30,.04),.08,.35,.15,.1)}
 values.update({'stone':((.28,.29,.25),0,.91,0,.35),'wood':((.23,.13,.055),0,.79,0,.25),
  'copper':((.39,.18,.06),.8,.37,0,.18),'ceramic':((.55,.53,.44),0,.67,0,.12),
  'red':((.30,.035,.02),.05,.65,0,.13),'yellow':((.55,.35,.025),.03,.54,0,.10)})
 spec=PILOTS[id]
 if 'color' in spec:
  metallic=.7 if spec['color'] in ['silver','steel','brass'] else 0
  glossy=spec['shape'] in ['vessel','bowl','cartridge','canister','froth','resin','droplet','glass-sheets']
  values['product']=(COLORS[spec['color']],metallic,.24 if glossy else .68,0,.15)
  values['secondary']=((.56,.50,.31),0,.65,0,.15)
 return {k:p.material(id+' | '+k,*v) for k,v in values.items()}
def lump(name,pos,scale,mat,seed=1):
 ob=p.sphere(name,pos,scale,mat,3);rng=random.Random(seed)
 for v in ob.data.vertices:v.co*=.89+rng.random()*.2
 return ob
def carve(ob,name,pos,size):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);cut=bpy.context.object;cut.scale=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=ob
 mod=ob.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
def clay(m):
 for i,(pos,size) in enumerate([((-.31,.04,-.08),(.44,.32,.32)),((.30,.08,-.08),(.39,.31,.3)),((.05,-.14,.15),(.43,.27,.30))]):
  ob=lump('Thumb compressed wet clay',pos,size,m['clay'],i+3)
  for v in ob.data.vertices:
   if v.co.z<-.2:v.co.z=-.2+(v.co.z+.2)*.25
 for i in range(7):
  a=i*.95;lump('Coarse mineral inclusion',(.43*math.cos(a),-.21,.13+.15*math.sin(a)),(.018,.012,.016),m['pulp'],i+30)
def brick(m):
 for index,(x,y,z,angle) in enumerate([(-.15,.14,-.25,-.06),(.12,.12,.07,.04),(-.05,-.12,.37,-.08)]):
  ob=p.box('Fired brick '+str(index),(x,y,z),(1.12,.43,.25),m['fired'],.025)
  carve(ob,'Real recessed brick frog',(x,y-.21,z),(.65,.075,.12))
  ob.rotation_euler.y=angle
def charcoal(m):
 for i,(x,y,z,size) in enumerate([(-.28,.08,-.18,(.4,.25,.25)),(.30,.08,-.14,(.38,.25,.26)),
  (-.16,-.12,.17,(.34,.23,.23)),(.32,-.05,.28,(.24,.21,.21))]):
  ob=lump('Irregular split charcoal chunk '+str(i),(x,y,z),size,m['char'],20+i)
  for j in range(3):
   xx=x-.12+j*.105
   p.tube('Ash caught in longitudinal char checking',[(xx,-.19+y,z-.1),(xx+.02,-.22+y,z),
    (xx+.01,-.19+y,z+.13)],.006,m['ash'])
  for j in range(2):
   p.tube('Charred end-grain fissure',[(x-.24,-.10+y,z-.07+j*.11),(x+.1,-.13+y,z-.06+j*.11)],.004,m['dark'])
def paper(m):
 for i in range(5):
  ob=p.box('Unbleached handmade pulp sheet '+str(i),((i%3)*.075-.075,.07-i*.032,(i%2)*.062),
   (1.12,.019,.78),m['paper'],.009)
  ob.rotation_euler.y=(i-2)*.035
  for j in range(3):
   p.tube('Visible edge fiber',[(-.58,-.07+i*.02,-.24+j*.17),(-.61,-.07+i*.02,-.245+j*.17)],.0028,m['pulp'])
 # A physical curl follows the top page; it is not a flat painted rectangle.
 p.tube('Curled pulp sheet edge',[(.4,-.082,.42),(.51,-.09,.43),(.59,-.12,.40),(.61,-.16,.34)],.012,m['paper'])
def ink(m):
 p.box('Squat thick glass inkwell',(0,0,-.12),(.88,.65,.6),m['glass'],.11)
 p.cylinder('Brass bottle shoulder',.31,.1,.23,m['brass'])
 p.cylinder('Short glass neck',.23,.19,.35,m['glass'])
 p.ring('Supported threaded brass neck',.245,.024,.43,m['brass'])
 p.cylinder('Visible black ink meniscus',.21,.025,.40,m['ink'])
 cap=p.cylinder('Detached fitted screw cap',.26,.13,-.37,m['brass'],xy=(.51,-.1));cap.rotation_euler.y=.18
 p.box('Small bone-paper bottle label',(0,-.329,-.13),(.42,.012,.25),m['paper'],.014)
 for x in (-.11,0,.11):p.box('Impressed label rule',(x,-.338,-.13),(.012,.005,.13),m['ink'],.002)
def fieldpack(m):
 p.box('Canvas power supply pouch',(0,0,0),(1.24,.46,.76),m['cloth'],.10)
 p.box('Folded canvas top flap',(0,-.255,.22),(1.18,.07,.37),m['cloth'],.07)
 for x in (-.4,.4):
  p.box('Supported leather retaining strap',(x,-.31,-.02),(.17,.045,.69),m['leather'],.02)
  p.box('Brass buckle frame',(x,-.346,-.08),(.25,.04,.21),m['brass'],.02)
  p.box('Buckle opening',(x,-.371,-.08),(.13,.012,.10),m['dark'],.007)
  p.box('Buckle pin',(x,-.385,-.08),(.025,.02,.14),m['steel'],.004)
  for z in (-.26,-.18,.04):p.sphere('Stitch on supported strap',(x-.055,-.336,z),(.008,.005,.013),m['stitch'],1)
 p.box('Armored contact access cover',(.02,-.31,-.06),(.39,.06,.27),m['dark'],.025)
 p.box('Recessed fuel state lens',(.02,-.346,-.06),(.22,.015,.055),m['green'],.007)
 for x in (-.12,.12):p.cylinder('Insulated power coupling',.075,.1,.43,m['dark'],xy=(x,0))
 p.tube('Canvas carry handle',[(-.22,.03,.39),(-.2,.03,.55),(.2,.03,.55),(.22,.03,.39)],.03,m['cloth'])
BUILDERS={'clay':clay,'brick':brick,'charcoal':charcoal,'paper':paper,'ink':ink,'fieldpack':fieldpack}
def lighting(scene):
 scene.world=bpy.data.worlds.new('Canonical northwest daylight');scene.world.use_nodes=True
 bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.7,.78,1,1);bg.inputs['Strength'].default_value=.18
 light=bpy.data.lights.new('Northwest sun','SUN');light.energy=2.3;light.color=(1,.94,.85);light.angle=math.radians(18)
 ob=bpy.data.objects.new(light.name,light);scene.collection.objects.link(ob);ob.rotation_euler=Vector((4,6,-8)).to_track_quat('-Z','Y').to_euler()
 scene.render.engine='CYCLES';scene.cycles.use_denoising=True;scene.view_settings.view_transform='AgX'
def build(id):
 spec=PILOTS[id];dest=folder(id)
 if dest.exists():raise FileExistsError('Preserve prior candidates: '+str(dest))
 dest.mkdir(parents=True);bpy.ops.wm.read_factory_settings(use_empty=True)
 material_map=mats(id)
 if spec['shape'] in EXTRA:EXTRA[spec['shape']](material_map,spec.get('parameters',{}))
 else:BUILDERS[spec['shape']](material_map)
 scene=bpy.context.scene;bpy.context.view_layer.update()
 regions=[dict(part=o.name,materials=[m.name for m in o.data.materials]) for o in scene.objects if o.type=='MESH']
 (dest/'surface-plan.json').write_text(json.dumps(dict(asset=id,construction=spec['construction'],regions=regions,
  principles=['Model-specific construction and material regions','No borrowed crate artwork','No floating fittings','Pose C under unchanged FMPL camera']),indent=2)+'\n')
 meshes=[o for o in scene.objects if o.type=='MESH'];bounds=p.measure(meshes);center=Vector([(bounds[0][i]+bounds[1][i])/2 for i in range(3)])
 transform=Matrix.Translation(center)@pose_matrix(**PRESETS['C'])@Matrix.Translation(-center)
 for ob in meshes:ob.matrix_world=transform@ob.matrix_world
 bpy.context.view_layer.update();bounds=p.measure(meshes);target=[(bounds[0][i]+bounds[1][i])/2 for i in range(3)]
 extent=max(bounds[1][0]-bounds[0][0],((bounds[1][1]-bounds[0][1])+(bounds[1][2]-bounds[0][2]))/math.sqrt(2))
 cfg=json.loads((ROOT/'tools/fmpl/profiles/item-icon.example.json').read_text());cfg.update(asset=id,source='runtime-reimport.blend',source_size=256,sizes=[64,128,256],samples=32,threads=4)
 cfg['camera_override'].update(target=target,ortho_scale=extent*1.20)
 lighting(scene);install_canonical_camera(scene,cfg,bpy);ob=p.unwrap_and_bake(dest,bake_resolution=1024);before=p.measure([ob])
 bpy.ops.export_scene.gltf(filepath=str(dest/'model.glb'),export_format='GLB',use_selection=True,export_animations=False)
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(dest/'model.glb'));p.preserve_glb_images(dest)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.context.view_layer.update();after=p.measure(meshes)
 error=max(abs(before[j][i]-after[j][i]) for j in range(2) for i in range(3));triangles=invalid=0
 for ob in meshes:
  ob.data.calc_loop_triangles();triangles+=len(ob.data.loop_triangles);invalid+=sum(t.area<1e-12 for t in ob.data.loop_triangles)
  assert ob.data.uv_layers and all(math.isfinite(v) for vert in ob.data.vertices for v in vert.co)
 assert error<1e-5 and invalid==0,(id,error,invalid)
 bpy.data.orphans_purge(do_recursive=True)
 for image in bpy.data.images:
  if image.source=='FILE':image.pack()
 lighting(bpy.context.scene);install_canonical_camera(bpy.context.scene,cfg,bpy);assert_clean(bpy.context.scene,cfg,bpy)
 bpy.ops.wm.save_as_mainfile(filepath=str(dest/'runtime-reimport.blend'))
 (dest/'capture-profile.json').write_text(json.dumps(cfg,indent=2)+'\n')
 (dest/'runtime-inspection.json').write_text(json.dumps(dict(passed=True,asset=id,triangles=triangles,degenerate_triangles=invalid,
  bounds_max_error=error,glb_sha256=p.sha(dest/'model.glb'),authored_sha256=p.sha(dest/'authored.blend'),
  pose=dict(preset='C',screen_diagonal=35,end_view=12,top_view=18),map_size=1024),indent=2)+'\n')
 print('MATERIAL_MODEL_BUILT',id,flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--assets',nargs='+',choices=list(PILOTS),default=list(PILOTS))
 parser.add_argument('--pending',action='store_true')
 args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
 for id in args.assets:
  if args.pending and (folder(id)/'runtime-inspection.json').exists():continue
  build(id)
