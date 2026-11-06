#!/usr/bin/env python3
"""V9: localized blackened inner firewood ONLY while the native Blender fire is active."""
import argparse,sys,json
from pathlib import Path
import bpy
argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
ap=argparse.ArgumentParser()
ap.add_argument("--out",type=Path,required=True)
ap.add_argument("--samples",type=int,default=20)
ap.add_argument("--resolution",type=int,default=512)
opts=ap.parse_args(argv)
opts.out.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
assert s.render.engine=="CYCLES"
ctrl=bpy.data.objects["CAMPFIRE CONTROLS | collection 03 toggle fire"]
ctrl["Fire Active"]=1.0
ctrl.id_properties_ui("Fire Active").update(min=0.0,max=1.0,description="0 = cold uncharred wood; 1 = burning fire with a charred core")
ctrl["V9 intent"]="One Fire Active control: flames, light, charred wood; idle keeps original wood"
wood=[o for o in bpy.data.collections["02 | Firewood"].objects if o.type=="MESH"]
flames=[o for o in s.objects if o.name.startswith("flame_tongue")]
light=bpy.data.objects["04 | animated fire light"]
assert len(wood)>=25 and len(flames)==6
def node(nodes,kind,label,xy):
    n=nodes.new(kind);n.label=label;n.location=xy;return n
def add_driver(target,property,expression):
    f=target.driver_add(property)
    d=f.driver;d.type="SCRIPTED";d.expression=expression
    v=d.variables.new();v.name="active";v.type="SINGLE_PROP"
    v.targets[0].id=ctrl;v.targets[0].data_path='["Fire Active"]'
    return f
seen=set()
for obj in wood:
  for m in obj.data.materials:
    if not m or m.name in seen:continue
    seen.add(m.name)
    ns=m.node_tree.nodes;ln=m.node_tree.links
    bsdf=next(n for n in ns if n.bl_idname=="ShaderNodeBsdfPrincipled")
    old=bsdf.inputs["Base Color"].links[0]
    old_color=old.from_socket;ln.remove(old)
    geom=node(ns,"ShaderNodeNewGeometry","WORLD-POSITION for firewood core",(-1100,-780))
    dist=node(ns,"ShaderNodeVectorMath","Distance from live coal bed",(-900,-760))
    dist.operation="DISTANCE";dist.inputs[1].default_value=(0,0,0.40)
    ln.new(geom.outputs["Position"],dist.inputs[0])
    radial=node(ns,"ShaderNodeMapRange","Scorched core with gradual outer fade",(-700,-760))
    radial.inputs["From Min"].default_value=.12;radial.inputs["From Max"].default_value=.90
    radial.inputs["To Min"].default_value=1.0;radial.inputs["To Max"].default_value=0.0
    radial.clamp=True;ln.new(dist.outputs["Value"],radial.inputs["Value"])
    noise=node(ns,"ShaderNodeTexNoise","Irregular carbonized borders",(-900,-1100))
    noise.inputs["Scale"].default_value=13.0;noise.inputs["Detail"].default_value=3.2
    ln.new(geom.outputs["Position"],noise.inputs["Vector"])
    variation=node(ns,"ShaderNodeMapRange","Non-repeating 75%-100% char",(-700,-1030))
    variation.inputs["To Min"].default_value=.75;variation.inputs["To Max"].default_value=1
    ln.new(noise.outputs["Fac"],variation.inputs["Value"])
    mask=node(ns,"ShaderNodeMath","Spatially local char mask",(-500,-800))
    mask.operation="MULTIPLY"
    ln.new(radial.outputs["Result"],mask.inputs[0])
    ln.new(variation.outputs["Result"],mask.inputs[1])
    on=node(ns,"ShaderNodeValue","FIRE ACTIVE control, 0 cold / 1 burning",(-540,-1190))
    on.outputs[0].default_value=1
    add_driver(on.outputs[0],"default_value","active")
    gated=node(ns,"ShaderNodeMath","Only char when FIRE ACTIVE",(-280,-800))
    gated.operation="MULTIPLY"
    ln.new(mask.outputs[0],gated.inputs[0]);ln.new(on.outputs[0],gated.inputs[1])
    colors=node(ns,"ShaderNodeValToRGB","Black charcoal with soot-brown edges",(-260,-1150))
    colors.color_ramp.elements[0].position=.15
    colors.color_ramp.elements[0].color=(.010,.008,.006,1)
    colors.color_ramp.elements[1].position=.8
    colors.color_ramp.elements[1].color=(.092,.039,.020,1)
    k=colors.color_ramp.elements.new(.47);k.color=(.034,.021,.014,1)
    ln.new(noise.outputs["Fac"],colors.inputs["Fac"])
    mix=node(ns,"ShaderNodeMixRGB","CF9 wood char / original wood switch",(-30,315))
    mix.blend_type="MIX"
    ln.new(gated.outputs[0],mix.inputs[0])
    ln.new(old_color,mix.inputs[1])
    ln.new(colors.outputs["Color"],mix.inputs[2])
    ln.new(mix.outputs["Color"],bsdf.inputs["Base Color"])
    m["V9 char"]="Blackened center only when Fire Active > 0; normal mapped wood preserved"
for o in flames+[light]:
    o.hide_render=False
    add_driver(o,"hide_render","1-active")
s.render.film_transparent=True
s.render.image_settings.file_format="PNG"
s.render.image_settings.color_mode="RGBA"
s.cycles.samples=opts.samples
s.render.resolution_percentage=100
def render(name,on,res):
    ctrl["Fire Active"]=float(on)
    s.frame_set(13);bpy.context.view_layer.update()
    s.render.resolution_x=res;s.render.resolution_y=res
    s.render.filepath=str(opts.out/name)
    bpy.ops.render.render(write_still=True)
render("campfire-v9-idle-natural-wood.png",0,opts.resolution)
render("campfire-v9-burning-charred-core.png",1,opts.resolution)
render("campfire-v9-native64.png",1,64)
ctrl["Fire Active"]=1.0
s.frame_set(13);bpy.context.view_layer.update()
s.render.resolution_x=opts.resolution;s.render.resolution_y=opts.resolution
s.render.filepath="//campfire-v9-burning-charred-core.png"
bpy.ops.wm.save_as_mainfile(filepath=str(opts.out/"campfire-v9-animated.blend"),compress=True)
(opts.out/"campfire-v9-build-report.txt").write_text(
    "Native Blender V9 core firewood char\n"+
    "Fire state: CAMPFIRE CONTROLS / Fire Active\n"+
    "Wood objects: "+str(len(wood))+"\n"+
    "Char-aware wood materials: "+str(len(seen))+"\n"+
    "Flames: "+str(len(flames))+"\n"+
    "Cycles. Normal maps preserved. No generated illustration.\n")
print("V9_NATIVE_BLENDER_SAVED, char materials:",len(seen),flush=True)
