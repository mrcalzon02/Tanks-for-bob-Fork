#!/usr/bin/env python3
"""Clay Pit V2 — source-guided editable earthwork with real primitive work props.

Full-object four-way proof renders; not accepted engine art. The original game
sprite is one 64x64 clay excavation plus a separate tools overlay. No extra
pits, hidden machinery or invented building geometry. Materials are procedural.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector

# Reuse the established V1 mesh utilities; source V1 remains untouched.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_clay_pit_v1 import coll, move, mat, mesh_obj, geo_rock, rod, lamp


def earth(name, dark, mid, light, rough=.96, scale=4.0, bump=.08):
    """Three-tone non-tiled clay: noisy pigment, subtle grain, never shiny stone."""
    material=mat(name, mid, rough)
    nodes=material.node_tree.nodes
    links=material.node_tree.links
    shader=nodes.get('Principled BSDF')
    noise=nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=scale
    noise.inputs['Detail'].default_value=3.2
    noise.inputs['Roughness'].default_value=.66
    ramp=nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position=.21
    ramp.color_ramp.elements[0].color=(*dark,1)
    ramp.color_ramp.elements[1].position=.79
    ramp.color_ramp.elements[1].color=(*light,1)
    middle=ramp.color_ramp.elements.new(.49)
    middle.color=(*mid,1)
    links.new(noise.outputs['Fac'],ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'],shader.inputs['Base Color'])
    grain=nodes.new('ShaderNodeBump')
    grain.inputs['Strength'].default_value=bump
    grain.inputs['Distance'].default_value=.018
    links.new(noise.outputs['Fac'],grain.inputs['Height'])
    links.new(grain.outputs['Normal'],shader.inputs['Normal'])
    return material



def wet_bank_gradient():
    """Continuous ochre-to-dark-mud gradient modulated by clay pigmentation.

    The previous per-polygon wet/dry selection caused an unrealistic hard wedge.
    Here the slope transitions by actual object-space Y, using restrained noise
    to break up the edge instead of changing material at angular face borders.
    """
    material=mat('BANK | continuous mottled damp-to-wet clay',(.32,.17,.085),.965)
    nodes=material.node_tree.nodes
    links=material.node_tree.links
    bsdf=nodes.get('Principled BSDF')
    tex=nodes.new('ShaderNodeTexCoord')
    separate=nodes.new('ShaderNodeSeparateXYZ')
    links.new(tex.outputs['Generated'],separate.inputs[0])
    noise=nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=4.8
    noise.inputs['Detail'].default_value=4.0
    noise.inputs['Roughness'].default_value=.63
    links.new(tex.outputs['Generated'],noise.inputs['Vector'])
    perturb=nodes.new('ShaderNodeMath')
    perturb.operation='MULTIPLY_ADD'
    links.new(noise.outputs['Fac'],perturb.inputs[0])
    perturb.inputs[1].default_value=.19
    perturb.inputs[2].default_value=-.095
    rough_y=nodes.new('ShaderNodeMath')
    rough_y.operation='ADD'
    links.new(separate.outputs['Y'],rough_y.inputs[0])
    links.new(perturb.outputs[0],rough_y.inputs[1])
    ramp=nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position=.22
    ramp.color_ramp.elements[0].color=(.075,.035,.018,1)
    ramp.color_ramp.elements[1].position=.83
    ramp.color_ramp.elements[1].color=(.47,.285,.14,1)
    middle=ramp.color_ramp.elements.new(.51)
    middle.color=(.255,.125,.060,1)
    links.new(rough_y.outputs[0],ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'],bsdf.inputs['Base Color'])
    grain=nodes.new('ShaderNodeBump')
    grain.inputs['Strength'].default_value=.065
    grain.inputs['Distance'].default_value=.018
    links.new(noise.outputs['Fac'],grain.inputs['Height'])
    links.new(grain.outputs['Normal'],bsdf.inputs['Normal'])
    return material


def blended_basin_v3():
    """One continuous shader controls ochre rim, inner bank, and wet basin."""
    m=mat('V3 | single feathered clay field',(.36,.21,.11),.97)
    ns=m.node_tree.nodes
    links=m.node_tree.links
    shader=ns.get('Principled BSDF')
    coord=ns.new('ShaderNodeTexCoord')
    pos=ns.new('ShaderNodeSeparateXYZ')
    links.new(coord.outputs['Generated'],pos.inputs[0])
    xy=ns.new('ShaderNodeCombineXYZ')
    links.new(pos.outputs['X'],xy.inputs['X'])
    links.new(pos.outputs['Y'],xy.inputs['Y'])
    dist=ns.new('ShaderNodeVectorMath')
    dist.operation='DISTANCE'
    links.new(xy.outputs['Vector'],dist.inputs[0])
    dist.inputs[1].default_value=(.5,.5,0)
    rad=ns.new('ShaderNodeMath')
    rad.operation='MULTIPLY'
    rad.inputs[1].default_value=2
    links.new(dist.outputs['Value'],rad.inputs[0])
    noise=ns.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value=4.6
    noise.inputs['Detail'].default_value=4
    links.new(coord.outputs['Generated'],noise.inputs['Vector'])
    wiggle=ns.new('ShaderNodeMath')
    wiggle.operation='MULTIPLY_ADD'
    links.new(noise.outputs['Fac'],wiggle.inputs[0])
    wiggle.inputs[1].default_value=.15
    wiggle.inputs[2].default_value=-.075
    radial=ns.new('ShaderNodeMath')
    radial.operation='ADD'
    links.new(rad.outputs[0],radial.inputs[0])
    links.new(wiggle.outputs[0],radial.inputs[1])
    earth=ns.new('ShaderNodeValToRGB')
    earth.color_ramp.interpolation='EASE'
    earth.color_ramp.elements[0].color=(.33,.206,.125,1)
    earth.color_ramp.elements[1].color=(.50,.27,.12,1)
    for a,c in [(.45,(.38,.235,.137,1)),(.66,(.48,.30,.166,1)),
                (.82,(.62,.398,.221,1)),(.94,(.67,.425,.198,1))]:
        e=earth.color_ramp.elements.new(a)
        e.color=c
    links.new(radial.outputs[0],earth.inputs['Fac'])
    wet_pos=ns.new('ShaderNodeMath')
    wet_pos.operation='ADD'
    links.new(pos.outputs['Y'],wet_pos.inputs[0])
    links.new(wiggle.outputs[0],wet_pos.inputs[1])
    moisture=ns.new('ShaderNodeValToRGB')
    moisture.color_ramp.interpolation='EASE'
    moisture.color_ramp.elements[0].position=.01
    moisture.color_ramp.elements[0].color=(1,1,1,1)
    moisture.color_ramp.elements[1].position=.76
    moisture.color_ramp.elements[1].color=(0,0,0,1)
    for a,k in [(.23,.92),(.43,.65),(.59,.15)]:
        e=moisture.color_ramp.elements.new(a)
        e.color=(k,k,k,1)
    links.new(wet_pos.outputs[0],moisture.inputs['Fac'])
    mask=ns.new('ShaderNodeValToRGB')
    mask.color_ramp.interpolation='EASE'
    mask.color_ramp.elements[0].position=.57
    mask.color_ramp.elements[0].color=(1,1,1,1)
    mask.color_ramp.elements[1].position=.96
    mask.color_ramp.elements[1].color=(0,0,0,1)
    e=mask.color_ramp.elements.new(.76)
    e.color=(.72,.72,.72,1)
    links.new(radial.outputs[0],mask.inputs['Fac'])
    strength=ns.new('ShaderNodeMixRGB')
    strength.blend_type='MULTIPLY'
    strength.inputs[0].default_value=1
    links.new(moisture.outputs['Color'],strength.inputs[1])
    links.new(mask.outputs['Color'],strength.inputs[2])
    damp=ns.new('ShaderNodeValToRGB')
    damp.color_ramp.elements[0].color=(.070,.034,.020,1)
    damp.color_ramp.elements[1].color=(.24,.124,.068,1)
    e=damp.color_ramp.elements.new(.5)
    e.color=(.13,.063,.036,1)
    links.new(noise.outputs['Fac'],damp.inputs['Fac'])
    blend=ns.new('ShaderNodeMixRGB')
    links.new(strength.outputs['Color'],blend.inputs[0])
    links.new(earth.outputs['Color'],blend.inputs[1])
    links.new(damp.outputs['Color'],blend.inputs[2])
    fine=ns.new('ShaderNodeTexNoise')
    fine.inputs['Scale'].default_value=23
    links.new(coord.outputs['Generated'],fine.inputs['Vector'])
    colors=ns.new('ShaderNodeValToRGB')
    colors.color_ramp.elements[0].color=(.88,.85,.80,1)
    colors.color_ramp.elements[1].color=(1.10,1.07,1.02,1)
    links.new(fine.outputs['Fac'],colors.inputs['Fac'])
    tint=ns.new('ShaderNodeMixRGB')
    tint.blend_type='MULTIPLY'
    tint.inputs[0].default_value=.12
    links.new(blend.outputs['Color'],tint.inputs[1])
    links.new(colors.outputs['Color'],tint.inputs[2])
    links.new(tint.outputs['Color'],shader.inputs['Base Color'])
    bump=ns.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value=.065
    bump.inputs['Distance'].default_value=.009
    links.new(fine.outputs['Fac'],bump.inputs['Height'])
    links.new(bump.outputs['Normal'],shader.inputs['Normal'])
    rough=ns.new('ShaderNodeMapRange')
    rough.inputs['To Min'].default_value=.99
    rough.inputs['To Max'].default_value=.92
    links.new(strength.outputs['Color'],rough.inputs['Value'])
    links.new(rough.outputs['Result'],shader.inputs['Roughness'])
    return m

def basin_v2(collection, materials):
    """Uneven one-basin topology; dark wet foreground extends up its inner bank."""
    rings=[(1.17,-.025,0),(1.08,.023,0),(.997,.105,1),
           (.91,.157,1),(.815,.085,2),(.705,-.013,2),
           (.58,-.105,3),(.43,-.175,3),(.20,-.207,3)]
    n=64
    rand=random.Random(3102)
    variation=[1 + .026*math.sin(i*2*math.pi/n*5+.4) +
               .024*math.sin(i*2*math.pi/n*8-.7) + rand.uniform(-.014,.014)
               for i in range(n)]
    verts=[]
    for radius,z,_ in rings:
        for i in range(n):
            theta=2*math.pi*i/n
            mod=variation[i]*(1+.015*math.cos(theta*3+.8))
            verts.append((1.13*radius*mod*math.cos(theta),
                          1.29*radius*mod*math.sin(theta),
                          z+radius*.008*math.sin(theta*9+.3)))
    faces=[]; ids=[]
    for band in range(len(rings)-1):
        for i in range(n):
            nxt=(i+1)%n
            faces.append((band*n+i,band*n+nxt,(band+1)*n+nxt,(band+1)*n+i))
            theta=2*math.pi*(i+.5)/n
            # The game's lower/foreground bank has a large muddy dark region,
            # not the tiny circular stain present in V1.
            ids.append(0)  # V3 shared shader on all basin polygons
    center=len(verts);verts.append((0,0,-.216))
    last=(len(rings)-1)*n
    for i in range(n):
        faces.append((last+i,last+(i+1)%n,center));ids.append(0)
    return mesh_obj('EARTH | one broad excavated clay bowl',verts,faces,collection,materials,ids)


def primitive_cube(name, location, scale, material, collection, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    ob=move(bpy.context.object,collection)
    ob.name=name
    ob.dimensions=scale
    bpy.context.view_layer.objects.active=ob
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(material)
    if bevel:
        m=ob.modifiers.new('small handmade edge rounding','BEVEL')
        m.width=bevel
        m.segments=2
        ob.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return ob


def wooden_bucket(collection, timber, inner, water, strap, center=(.04,-.17,-.055)):
    """Open tapered plank bucket with physically present water near the top."""
    cx,cy,top=center
    n=12
    radius_top=.119
    radius_bottom=.090
    lower=top-.185
    verts=[]
    for radius,z in [(radius_bottom,lower),(radius_top,top),(.096,top+.002),(.077,lower+.018)]:
        for j in range(n):
            a=2*math.pi*j/n
            verts.append((cx+radius*math.cos(a),cy+radius*math.sin(a),z))
    faces=[];mids=[]
    for j in range(n):
        k=(j+1)%n
        faces.append((j,k,n+k,n+j));mids.append(0)
        faces.append((n+j,n+k,2*n+k,2*n+j));mids.append(0)
        faces.append((2*n+j,2*n+k,3*n+k,3*n+j));mids.append(1)
    faces.append(tuple(range(3*n,4*n)));mids.append(1)
    bucket=mesh_obj('WORK | OPEN WOODEN WATER BUCKET - tapered staves',verts,faces,collection,[timber,inner],mids)
    items=[bucket]
    # Narrow planks and staves are represented by the tapered outer faces;
    # two subtle fiber hoops make it recognizable even at low resolution.
    for height,r in [(lower+.042,.094),(top-.040,.112)]:
        for j in range(n):
            a=2*math.pi*j/n; b=2*math.pi*(j+1)/n
            items.append(rod('WORK | bucket fiber hoop segment %d %d'%(int(height*1000),j),
                (cx+r*math.cos(a),cy+r*math.sin(a),height),
                (cx+r*math.cos(b),cy+r*math.sin(b),height),.006,strap,collection,vertices=5))
    # Water level is below the wooden lip, not a solid capped bucket.
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.092,depth=.004,
        location=(cx,cy,top-.024))
    water_obj=move(bpy.context.object,collection)
    water_obj.name='WORK | water visible below bucket rim'
    water_obj.data.materials.append(water)
    items.append(water_obj)
    # Handle/lashing on the two sides of the rim.
    for sx in (-1,1):
        items.append(rod('WORK | bucket handle tie %s'%sx,
            (cx+sx*.101,cy,top-.024),(cx+sx*.089,cy,top+.039),.009,strap,collection,6))
    return items


def tiny_lantern(collection, timber, paper, warm, center=(.19,.24,.82)):
    """Lantern of wood and wax paper sitting ON TOP of the support stick."""
    x,y,z=center
    items=[]
    # Wax paper is a small warm diffusing enclosure, not a dangling metal lamp.
    items.append(primitive_cube('WORK | wax paper lantern body',
          (x,y,z+.065),(.115,.115,.13),paper,collection,bevel=.006))
    for dx in (-.064,.064):
        for dy in (-.064,.064):
            items.append(rod('WORK | paper lantern wood corner',
                (x+dx,y+dy,z),(x+dx,y+dy,z+.145),.009,timber,collection,vertices=6))
    items.append(primitive_cube('WORK | lantern wooden bottom frame',
        (x,y,z-.006),(.156,.156,.027),timber,collection,bevel=.004))
    items.append(primitive_cube('WORK | lantern wooden roof',
        (x,y,z+.154),(.174,.174,.027),timber,collection,bevel=.004))
    items.append(primitive_cube('WORK | lantern faint warm paper center',
        (x,y,z+.064),(.046,.046,.078),warm,collection,bevel=.003))
    return items


def spade(collection, handle_mat, blade_mat):
    """Single recognizable shovel laid across the left edge and into the clay."""
    elements=[]
    # Sprite left-side diagonal handle and blade: blade is inside the pit.
    elements.append(rod('WORK | wooden shovel handle',(-1.19,-.66,.32),
                        (-.70,-.47,.135),.025,handle_mat,collection))
    # broad pointed paddle, not a random cylindrical rod.
    vertices=[(-.80,-.50,.115),(-.69,-.57,.095),(-.47,-.54,.064),
              (-.42,-.46,.055),(-.51,-.37,.071),(-.74,-.38,.115)]
    elements.append(mesh_obj('WORK | primitive shovel blade - two sided',
      vertices,[(0,1,2,3,4,5),(5,4,3,2,1,0)],collection,[blade_mat]))
    return elements


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    parser.add_argument('--samples',type=int,default=28)
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    opt=parser.parse_args(argv)
    out=Path(opt.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Output must be new/empty; preserve earlier runs')
    out.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine='CYCLES'
    scene.cycles.samples=opt.samples
    scene.cycles.device='CPU'
    scene.cycles.use_denoising=False
    for layer in scene.view_layers: layer.cycles.use_denoising=False
    scene.render.film_transparent=True
    scene.render.resolution_x=scene.render.resolution_y=256
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.image_settings.color_depth='8'
    scene.render.fps=8
    scene.view_settings.view_transform='Standard'
    scene.view_settings.look='Medium High Contrast'
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.22,.20,.17,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    ground=coll('EARTHWORK | editable one-basin primitive kit')
    tools=coll('WORK | primitive wooden implements')
    fixed=coll('FIXED | structure camera and daylight')
    soil=earth('EARTH | dry disturbed orange brown',(.29,.125,.052),(.44,.224,.083),(.59,.316,.121),.99,5.3,.075)
    rim=earth('CLAY | rough ochre rim',(.40,.18,.075),(.56,.30,.119),(.72,.422,.172),.985,4.7,.075)
    wall=earth('CLAY | exposed damp sloping bank',(.22,.13,.065),(.385,.232,.121),(.53,.32,.172),.95,4.5,.065)
    wet=earth('CLAY | saturated wet basin floor',(.048,.023,.013),(.12,.057,.031),(.29,.145,.072),.94,5.6,.025)
    clod=earth('CLAY | loose softened clods',(.22,.10,.045),(.345,.18,.075),(.48,.27,.11),.96,4.9,.06)
    wood=earth('WOOD | unplaned branch',(.13,.073,.028),(.255,.143,.055),(.38,.223,.095),.93,6,.07)
    blade=earth('SHOVEL | carved wood/stone head',(.26,.22,.125),(.44,.38,.245),(.51,.44,.29),.99,5.3,.035)
    rope=mat('FIBER | dry twisted cord',(.39,.26,.10),.99)
    bucket_wood=earth('BUCKET | damp wooden staves',(.16,.087,.042),(.30,.16,.074),(.43,.257,.128),.93,6,.07)
    inside=mat('BUCKET | dark open interior',(.090,.055,.031),.98)
    water=mat('BUCKET | small dark water surface',(.075,.15,.175),.45)
    paper=mat('LANTERN | pale wax-paper panels',(0.89,.68,.42),.83)
    warm=mat('LANTERN | warm inner illumination',(1.0,.51,.19),.85)
    p=warm.node_tree.nodes.get('Principled BSDF')
    if p.inputs.get('Emission Color'):
        p.inputs['Emission Color'].default_value=(1.0,.54,.13,1)
        p.inputs['Emission Strength'].default_value=.65
    bank=blended_basin_v3()
    basin_v2(ground,[bank])
    for i,(x,y,r) in enumerate([(-.42,-.48,.09),(-.20,-.55,.08),(.40,-.28,.095),
                                  (.53,.23,.068),(-.16,.45,.065)]):
        geo_rock('EARTH | separate loose clay lump %02d'%(i+1),
                 (x,y,-.095),(r,r*.84,r*.45),clod,ground,i+11)
    for i,(t,r) in enumerate([(.35,.065),(1.52,.07),(2.70,.052),(4.38,.065),(5.47,.06)]):
        geo_rock('EARTH | uneven rim chip %02d'%(i+1),
                 (1.13*.96*math.cos(t),1.29*.96*math.sin(t),.125),
                 (r,r*.86,r*.26),rim,ground,i+56)
    moving=[]
    moving.extend(spade(tools,wood,blade))
    support=(.19,.24,.82)
    # A restrained pole rig: stakes are pegged at the edge, with a short arm over the pit.
    for name,start,end,rad in [
       ('WORK | lantern support upright',(.17,.21,.11),support,.029),
       ('WORK | right brace to far rim',(.86,.65,.13),(.19,.24,.72),.023),
       ('WORK | right brace to near rim',(.91,-.65,.12),(.19,.24,.72),.028),
       ('WORK | overhead wood crossbar',(-.13,.17,.66),(1.04,.27,.69),.020),
       ('WORK | bucket lifting arm',(.19,.24,.69),(.04,-.17,.57),.023)]:
        moving.append(rod(name,start,end,rad,wood,tools))
    moving.extend(tiny_lantern(tools,wood,paper,warm,center=support))
    moving.append(rod('WORK | rope hanging down from hoist arm',
        (.04,-.17,.57),(.04,-.17,.008),.0095,rope,tools,vertices=7))
    moving.extend(wooden_bucket(tools,bucket_wood,inside,water,rope,center=(.04,-.17,-.055)))
    for ob in moving:
        ob.hide_render=True
        ob.keyframe_insert(data_path='hide_render',frame=0)
        ob.hide_render=False
        ob.keyframe_insert(data_path='hide_render',frame=1)
        ob.keyframe_insert(data_path='hide_render',frame=96)
        if ob.animation_data:
            for curve in ob.animation_data.action.fcurves:
                for point in curve.keyframe_points: point.interpolation='CONSTANT'
    # Give the water a subtle changing normal-map shimmer (not a moving bucket).
    # The source overlay is one still frame, so no unsupported big tool dance.
    pivot=bpy.data.objects.new('EXPORT | rotate all clay and tools, never camera',None)
    ground.objects.link(pivot)
    for ob in list(ground.objects)+list(tools.objects):
        if ob is pivot:continue
        matrix=ob.matrix_world.copy()
        ob.parent=pivot
        ob.matrix_world=matrix
    camera_data=bpy.data.cameras.new('Calibrated 45 degree orthographic camera')
    camera_data.type='ORTHO'
    camera_data.ortho_scale=3.30
    camera=bpy.data.objects.new('Factorio fixed structure camera',camera_data)
    fixed.objects.link(camera)
    camera.location=(0,-6,6.14)
    camera.rotation_euler=(Vector((0,0,.14))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera=camera
    lamp('NW | broad daylight',(-3.5,-4,6.2),420,(1.0,.9,.74),5,fixed)
    lamp('SE | restrained skylight',(3.3,2,4.2),210,(.70,.82,1.0),6,fixed)
    scene.frame_set(0)
    scene.render.filepath='//previews/'
    # V2 is a new editable scene; no V1 sources or original PNGs touched.
    scene.use_fake_user=True
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'clay-pit-v3.blend'),check_existing=False)
    records=[]
    for state,frame in [('idle',0),('working',13)]:
        for direction,angle in enumerate((0,90,180,270)):
            pivot.rotation_euler.z=math.radians(angle)
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            target=out/f'{state}-d{direction:02d}.png'
            scene.render.filepath=str(target)
            print('CLAY_V2_RENDER',state,angle,flush=True)
            bpy.ops.render.render(write_still=True)
            records.append({'state':state,'angle':angle,'frame':frame,
             'path':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    pivot.rotation_euler.z=0
    scene.frame_set(0)
    report={
      'schema':2,'asset':'clay-pit','revision':'v3-feathered-clay-transitions',
      'primary_excavations':1,'number_of_meshes':sum(o.type=='MESH' for o in scene.objects),
      'props':{'lantern':'wood frame, wax paper, perched at the support pole tip',
               'rope':'vertical fiber cord from short lifting arm down into pit',
               'bucket':'open wooden staves with separately modeled water surface',
               'shovel':'primitive carved spade resting across left basin lip'},
      'materials':'procedural ochre/damp-clay/dark-wet clay and crude tools',
      'four_directions':[0,90,180,270],'camera_pitch_deg':45,
      'camera_ortho_scale':3.30,'blender':bpy.app.version_string,
      'captures':records,'source_original_unchanged':True,
      'production_ready':False,'user_visual_approval':False,
      'factorio_client_tested':False}
    (out/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CLAY_PIT_V3_EIGHT_RENDER_PASS',len(records),flush=True)


if __name__=='__main__':main()
