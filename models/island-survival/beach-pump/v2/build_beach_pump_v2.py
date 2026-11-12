#!/usr/bin/env python3
"""Blender Beach Pump V2: genuine Archimedes screw -> trough -> wheel + large drive crank.

Re-uses exact V1 FMPL fixture and verified PBR/camera, with old rocker/paddle
removed from Blender's scene. Never modifies Factorio game data or the donor.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CFG=HERE/"contract.json"
FRAMES=tuple(range(1,92,6))
DIRECTIONS=(0,90,180,270)
SEAM=97

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def blob_sha(path):
    data=Path(path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()

def source():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    v1source=ROOT/cfg["v1_builder"]["path"]
    if blob_sha(v1source)!=cfg["v1_builder"]["git_blob_sha1"]:
        raise RuntimeError("V1 authored Blender builder source was modified")
    spec=importlib.util.spec_from_file_location("tanks_beach_pump_v1",v1source)
    if not spec or not spec.loader:raise RuntimeError("Cannot load approved donor builder")
    v1=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=v1
    spec.loader.exec_module(v1)
    original=v1.preflight()
    lock=cfg["lock"]
    assert lock["prototype_type"]==original["entity"]["type"]=="offshore-pump"
    assert lock["prototype_name"]==original["entity"]["name"]=="beachpump"
    assert original["entity"]["pumping_speed"]==lock["water_per_tick"]==.01
    assert original["entity"]["fluid_source_offset"]==lock["shoreline_source_offset"]==[0,-1]
    assert original["entity"]["energy_source"]==lock["energy_source"]=="void"
    assert original["entity"]["output_connection"]["position_native"]==lock["native_output_position"]==[0,.25]
    assert original["entity"]["output_connection"]["flow_direction"]=="output"
    assert original["entity"]["output_connection"]["direction"]=="south"
    assert original["entity"]["tile_width"]==original["entity"]["tile_height"]==1
    assert cfg["dimensions"]["stationary_outlet_xyz"]==[0,-.49,.36]
    assert tuple(cfg["animation"]["frames"])==FRAMES
    assert cfg["animation"]["loop_end"]==SEAM
    assert original["camera"]["elevation_deg"]==45 and original["camera"]["model_yaws_deg"]==list(DIRECTIONS)
    return cfg,original,v1

def remove_old_mechanism(bpy,root):
    old_prefixes=("02 | ","03 | ","05 | ","06 | ")
    count=0
    for collection in tuple(bpy.data.collections):
        if collection.name.startswith(old_prefixes):
            for ob in list(collection.all_objects):
                bpy.data.objects.remove(ob,do_unlink=True)
                count+=1
            bpy.data.collections.remove(collection)
    for ob in list(bpy.data.objects):
        if ob.name.startswith("OUTPUT | "):
            bpy.data.objects.remove(ob,do_unlink=True)
            count+=1
    if count<30:raise RuntimeError("V1 rocker/diaphragm donor removal incomplete")
    assert bpy.data.objects.get("EXPORT | rotate beachpump not camera") is root
    assert sum(o.name.startswith("ANCHOR | separate") for o in bpy.data.objects)==4
    assert sum(o.name.startswith("PORT | south output |") for o in bpy.data.objects)==2
    for needle in ("MOTION | wave-actuated intake paddle pivot",
                   "MOTION | hand-hewn twin-arm mechanical rocker",
                   "MOTION | wet leather diaphragm actuator"):
        assert bpy.data.objects.get(needle) is None,needle
    return count

def helix(bpy,name,length,inner,outer,pitch_turns,mat,col,parent):
    """True swept thick helical blade, editable mesh, not an image or helix decal."""
    n=144
    vertices=[]
    faces=[]
    thickness=.022
    for i in range(n+1):
        f=i/n
        a=pitch_turns*2*math.pi*f
        z=(f-.5)*(length-.11)
        for r,dz in ((inner,-thickness),(outer,-thickness),
                     (outer,thickness),(inner,thickness)):
            vertices.append((r*math.cos(a),r*math.sin(a),z+dz))
    for i in range(n):
        a=4*i;b=a+4
        faces.extend(((a,a+1,b+1,b),(a+3,b+3,b+2,a+2),
                      (a,a+3,b+3,b),(a+1,b+1,b+2,a+2)))
    faces.extend(((0,3,2,1),(4*n,4*n+1,4*n+2,4*n+3)))
    mesh=bpy.data.meshes.new(name+" editable helical blade geometry")
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    ob.parent=parent
    ob.data.materials.append(mat)
    ob["pitch_turns"]=pitch_turns
    ob["source_object_type"]="REAL_EDITABLE_HELIX"
    return ob

def torus(bpy,v1,name,center,major,minor,mat,col,parent):
    bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=12,
       location=center,rotation=(0,math.pi/2,0),
       major_radius=major,minor_radius=minor)
    ob=v1.move(bpy,bpy.context.object,col,parent)
    ob.name=name
    ob.data.materials.append(mat)
    return ob

def tilted_board(v1,bpy,name,p0,p1,width,thickness,mat,col,root):
    from mathutils import Vector
    a,b=Vector(p0),Vector(p1)
    d=b-a
    obj=v1.block(bpy,name,(a+b)/2,(d.length,width,thickness),mat,col,root,.012)
    obj.rotation_euler=d.to_track_quat("X","Z").to_euler()
    return obj

def construct(bpy,v1,c,original,root,ports):
    from mathutils import Vector
    removed=remove_old_mechanism(bpy,root)
    mats={
      "wood":bpy.data.materials.get("BEACH | pitted salt driftwood"),
      "dark":bpy.data.materials.get("BEACH | wet salt-darkened timber"),
      "iron":bpy.data.materials.get("BEACH | black wet forged iron"),
      "copper":bpy.data.materials.get("BEACH | dented copper"),
      "brass":bpy.data.materials.get("BEACH | weathered brass"),
      "water":bpy.data.materials.get("BEACH | green-blue water"),
      "rope":bpy.data.materials.get("BEACH | hemp tied lashings")
    }
    if not all(mats.values()):raise RuntimeError("Approved V1 source materials unavailable")
    # Increase contrast/readability, never reduce chemical/water to barely-visible alpha.
    mats["flow"]=v1.material(bpy,"bright visibly blue-green moving water",(.04,.52,.62,1),.21,.06,.06)
    frame=v1.group(bpy,"V2 | weathered open screw rail supports")
    screw_col=v1.group(bpy,"V2 | animated actual helical screw and water pockets")
    channel=v1.group(bpy,"V2 | explicit wooden discharge trough")
    wheel_col=v1.group(bpy,"V2 | physical paddle wheel and large crank")
    drive=v1.group(bpy,"V2 | linked drive shaft and bevel gear housing")
    water_col=v1.group(bpy,"V2 | falling and flowing water")
    outlet=v1.group(bpy,"V2 | static water return and output pipe")
    geo=c["dimensions"]
    low=Vector(geo["screw_intake_xyz"])
    top=Vector(geo["screw_discharge_xyz"])
    axis=top-low
    length=axis.length
    if not 1.3<length<1.7:raise RuntimeError("Unexpected screw span")
    direction=axis.normalized()
    # Water side +Y: below-water inlet cage, set behind the screw.
    v1.cylinder(bpy,"SCREW | submerged open intake cage",low,.205,.15,mats["iron"],frame,root,n=32)
    for i in range(6):
        x=-.34+i*.06
        v1.block(bpy,"SCREW | visible intake grill slat",(x,1.275,.30),
                 (.021,.035,.18),mats["dark"],frame,root,.003)
    # Exposed inclined U-trough with railings that do not hide the screw.
    for x in (-.39,.01):
        a=tuple(low+Vector((x-low.x,0,-.07)))
        b=tuple(top+Vector((x-top.x,0,-.07)))
        v1.rod(bpy,"SCREW | full length wooden open casing side rail",a,b,.047,mats["wood"],frame,root)
    for fraction in (.15,.43,.72,.95):
        p=low+(top-low)*fraction
        v1.rod(bpy,"SCREW | transverse trough support",
               (p.x-.21,p.y,p.z-.13),(p.x+.22,p.y,p.z-.13),
               .036,mats["dark"],frame,root)
        v1.rod(bpy,"SCREW | diagonal support strut",
               (p.x,p.y,p.z-.14),(p.x,p.y+.11,max(.35,p.z-.36)),
               .031,mats["wood"],frame,root)
    # Align a real rotating shaft along the diagonal intake->outlet vector.
    carrier=v1.empty(bpy,"SCREW | diagonal shaft carrier (fixed)",screw_col,root)
    carrier.location=(low+top)/2
    carrier.rotation_euler=direction.to_track_quat("Z","Y").to_euler()
    rotor=v1.empty(bpy,"MOTION | keyed Archimedes screw rotation",screw_col,carrier)
    v1.cylinder(bpy,"SCREW | solid copper helical axle",(0,0,0),
                .052,length+.09,mats["iron"],screw_col,rotor,n=32)
    flight=helix(bpy,"SCREW | exposed 3-turn bronze helical flight",
                 length,.063,.174,3,mats["brass"],screw_col,rotor)
    flight["mechanical_role"]="water-lifting Archimedes screw"
    # Open blue water pockets above the core make lifting water unmistakable.
    pockets=[]
    for i in range(6):
        bead=v1.cylinder(bpy,f"WATER | visibly rising screw pocket {i:02d}",
             (0,0,0),.063,.095,mats["flow"],water_col,rotor,n=12)
        bead["animated_water_pocket"]=True
        pockets.append(bead)
    # Split trough: open floor, two wood sidewalls, colored water racing across.
    trough_a=Vector((-.19,.085,1.385))
    trough_b=Vector((.225,-.105,1.345))
    tilted_board(v1,bpy,"TROUGH | continuous open wooden gutter bottom",
       trough_a,trough_b,.205,.051,mats["wood"],channel,root)
    for sign in (-1,1):
        a=trough_a+Vector((0,sign*.092,.086))
        b=trough_b+Vector((0,sign*.092,.086))
        tilted_board(v1,bpy,"TROUGH | raised visible retaining side",
            a,b,.033,.128,mats["dark"],channel,root)
    water_lane=v1.rod(bpy,"TROUGH | clearly visible blue-green water ribbon",
        trough_a+Vector((0,0,.045)),trough_b+Vector((0,0,.045)),
        .065,mats["flow"],water_col,root)
    water_lane["mechanical_role"]="screw discharge to water wheel"
    # The water wheel is in a vertical YZ plane, facing to the right (+X),
    # with a large actual crank protruding on its right side.
    wheel=v1.empty(bpy,"MOTION | full bucket waterwheel shaft",wheel_col,root)
    wheel.location=geo["waterwheel_center_xyz"]
    for x in (-.068,.068):
        torus(bpy,v1,"WHEEL | 3D timber rim", (x,0,0),.256,.026,
              mats["dark"],wheel_col,wheel)
    v1.cylinder(bpy,"WHEEL | broad brass hub",(0,0,0),
                 .094,.22,mats["brass"],wheel_col,wheel,
                 rotation=(0,math.pi/2,0),n=32)
    for k in range(8):
        ang=2*math.pi*k/8
        v1.rod(bpy,f"WHEEL | heavy wooden spoke {k:02d}",
              (0,0,0),(0,.247*math.cos(ang),.247*math.sin(ang)),
              .029,mats["wood"],wheel_col,wheel)
        paddle=v1.block(bpy,f"WHEEL | chunky bucket paddle {k:02d}",
             (0,.267*math.cos(ang),.267*math.sin(ang)),
             (.20,.125,.048),mats["wood"],wheel_col,wheel,.01)
        paddle.rotation_euler.x=ang+math.pi/2
    # Oversized lever crank and real protruding hand-hold rotate WITH wheel.
    v1.rod(bpy,"CRANK | oversized side offset forged lever",
        (.118,0,0),(.118,0,.246),.045,mats["iron"],wheel_col,wheel)
    v1.cylinder(bpy,"CRANK | thick offset brass eccentric pin",
                (.118,0,.246),.054,.085,mats["brass"],wheel_col,wheel,
                rotation=(0,math.pi/2,0))
    v1.rod(bpy,"CRANK | large rotating external handle",
        (.14,0,.246),(.29,0,.246),.055,mats["wood"],wheel_col,wheel)
    # Stationary axle bearing and crosspiece: support wheel at true center.
    v1.rod(bpy,"WHEEL | fixed axle support",(0,-.13,.97),
           (.28,-.13,.97),.056,mats["iron"],drive,root)
    for y in (-.34,.10):
        v1.rod(bpy,"WHEEL | fixed timber bearing frame",
            (.25,y,.50),(.28,-.13,.96),.046,mats["dark"],drive,root)
    # Exterior gear drive makes the waterwheel-powering-screw visual explicit.
    v1.rod(bpy,"DRIVE | exposed rigid wheel-to-screw gearbox input",
            (.23,-.13,.98),(-.08,.085,1.36),.058,mats["iron"],drive,root)
    v1.cylinder(bpy,"DRIVE | massive bronze right angle bevel housing",
            (-.15,.07,1.37),.116,.16,mats["brass"],drive,root,
            rotation=(0,math.pi/4,0),n=20)
    v1.rod(bpy,"DRIVE | timber brace under bevel gear",
           (-.12,.065,1.25),(-.10,.12,.76),.047,mats["wood"],drive,root)
    # A shallow catch sump feeds the game-exact fixed south pipe mouth.
    v1.block(bpy,"SUMP | wood catch basin underneath wheel",
        (.195,-.17,.51),(.47,.47,.085),mats["dark"],outlet,root,.01)
    v1.block(bpy,"SUMP | blue-green collected flow",
        (.195,-.17,.57),(.34,.34,.024),mats["flow"],outlet,root,.005)
    v1.pipe(bpy,"OUTPUT | permanent water run to native south pipe mouth",
        [(.14,-.23,.55),(.02,-.31,.45),(0,-.40,.36),(0,-.488,.36)],
        .237,mats["copper"],outlet,root)
    v1.rod(bpy,"OUTPUT | rigid timber flow support",
         (-.18,-.34,.38),(.18,-.34,.38),.034,mats["wood"],outlet,root)
    # Visible spill: real 3D water droplets cascade down onto waterwheel.
    spill=[]
    for i in range(6):
        d=v1.cylinder(bpy,f"WATER | cascading trough-wheel spill {i:02d}",
            (.22,-.11,1.24),.034,.074,mats["flow"],water_col,root,n=12)
        d.hide_render=True
        d.keyframe_insert(data_path="hide_render",frame=0)
        d.hide_render=False
        d.keyframe_insert(data_path="hide_render",frame=1)
        d.keyframe_insert(data_path="hide_render",frame=SEAM)
        spill.append(d)
    # Wheel drives screw one-to-one; no free-floating counterrotation.
    for k,frame in enumerate((*FRAMES,SEAM)):
        phase=2*math.pi*k/16
        rotor.rotation_euler.z=phase
        rotor.keyframe_insert(data_path="rotation_euler",frame=frame)
        wheel.rotation_euler.x=-phase
        wheel.keyframe_insert(data_path="rotation_euler",frame=frame)
        for i,pocket in enumerate(pockets):
            t=((k/16)+(i/6))%1
            a=2*math.pi*(3*t+.18)
            pocket.location=(.124*math.cos(a),.124*math.sin(a),
                             (t-.5)*(length-.18))
            pocket.keyframe_insert(data_path="location",frame=frame)
        for i,d in enumerate(spill):
            t=((k/16)+(i/6))%1
            d.location=(.222+.03*math.sin(t*math.pi),
                        -.115-.04*t,1.31-.35*t)
            d.scale=(1,1,.75+.22*math.sin(phase+i))
            d.keyframe_insert(data_path="location",frame=frame)
            d.keyframe_insert(data_path="scale",frame=frame)
    # Validate as source, never claim that Factorio water flow is rendered here.
    return {
      "removed_v1_objects":removed,"length_bu":round(length,5),
      "helix_mesh_vertices":len(flight.data.vertices),
      "wheel_spokes":8,"wheel_paddles":8,
      "crank_handle_count":1,
      "water_pockets":len(pockets),"spill_droplets":len(spill),
      "static_south_port_meshes":len(ports),
      "screw_low_xyz":list(low),"screw_high_xyz":list(top),
      "wheel_xyz":geo["waterwheel_center_xyz"],
      "no_game_data_changed":True}

def native_checks(bpy,c,root,ports,geometry):
    scene=bpy.context.scene
    assert len(ports)==2
    assert {o.name for o in ports}=={
        "PORT | south output | machine_collar",
        "PORT | south output | machine_throat"}
    assert all(len(o.data.vertices)==256 for o in ports)
    assert all(o.parent==root for o in ports)
    assert {tuple(o["native_cell"]) for o in ports}=={(0,.25)}
    assert len([o for o in scene.objects if o.type=="CAMERA"])==1
    assert scene.camera.parent is None and scene.camera.data.type=="ORTHO"
    assert abs(scene.camera.data.ortho_scale-3.75)<1e-5
    assert sum(o.name.startswith("ANCHOR | separate") for o in scene.objects)==4
    assert bpy.data.objects.get("MOTION | hand-hewn twin-arm mechanical rocker") is None
    assert bpy.data.objects.get("MOTION | wet leather diaphragm actuator") is None
    helix=bpy.data.objects.get("SCREW | exposed 3-turn bronze helical flight")
    assert helix and helix.type=="MESH" and len(helix.data.vertices)>500
    wheel=bpy.data.objects.get("MOTION | full bucket waterwheel shaft")
    screw=bpy.data.objects.get("MOTION | keyed Archimedes screw rotation")
    assert wheel is not None and screw is not None
    assert bpy.data.objects.get("CRANK | large rotating external handle")
    assert bpy.data.objects.get("TROUGH | clearly visible blue-green water ribbon")
    scene.frame_set(1);bpy.context.view_layer.update()
    static=[o.matrix_world.copy() for o in ports]
    initial=(wheel.rotation_euler.x,screw.rotation_euler.z)
    for fr in (7,13,25,43,49,73,85,91,97):
        scene.frame_set(fr);bpy.context.view_layer.update()
        for o,ref in zip(ports,static):
            diff=max(abs(a-b) for ra,rb in zip(o.matrix_world,ref) for a,b in zip(ra,rb))
            assert diff<1e-6,(o.name,fr,diff)
    scene.frame_set(97)
    assert abs(math.sin(wheel.rotation_euler.x-initial[0]))<1e-6
    assert abs(math.sin(screw.rotation_euler.z-initial[1]))<1e-6
    scene.frame_set(0)
    return {"valid":True,"native_type":"offshore-pump","source_offset":[0,-1],
            "native_south_output":[0,.25],"port_fitted":True,
            "all_external_fittings_static":True,
            "loop97_matches_frame1":True,
            "real_helix_vertices":len(helix.data.vertices),
            "wheel_paddles":8,"oversize_crank":True,
            "gameplay_unchanged":True}

def build(args):
    import bpy
    cfg,original,v1=source()
    output=args.out.resolve()
    if output.exists():
        raise FileExistsError("Do not overwrite approved V1 or existing V2 proof: "+str(output))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    v1.camera(bpy,original)
    scene=bpy.context.scene
    scene.cycles.samples=args.samples
    root,ports,pbr=v1.model(bpy,original)
    geometry=construct(bpy,v1,cfg,original,root,ports)
    qa=native_checks(bpy,cfg,root,ports,geometry)
    output.mkdir(parents=True,exist_ok=False)
    master=output/"beach-pump-v2.blend"
    scene["native_offshore_behavior"]="unchanged: direct water from adjacent shoreline"
    scene["source_model"]="tanks beachpump V2 Archimedes screw and water wheel"
    scene["game_integrated"]=False
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True,check_existing=False)
    report={
      "schema":"tanks.beach-pump.v2.archimedes-native-blender",
      "native_sha256":sha(master),"donor_builder_blob_sha1":cfg["v1_builder"]["git_blob_sha1"],
      "footprint":[1,1],"shoreline_selection":original["entity"]["selection_box_native"],
      "native_offshore":cfg["lock"],
      "geometry":geometry,"native_reopen_preview_checks":qa,
      "source_materials":[m.name for m in bpy.data.materials if m.name.startswith("BEACH |")],
      "four_facings":list(DIRECTIONS),"fps":8,"working_frames":list(FRAMES),
      "render_mode":args.render,"render_count":0,"renders":[],
      "game_integrated":False,"human_visual_approved":False
    }
    manifest=output/"build-report.json"
    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if args.render!="none":
        for d,deg in enumerate(DIRECTIONS):
            root.rotation_euler.z=math.radians(deg)
            for state,indices in (("idle",[-1]),("working",range(16) if args.render=="all" else [4])):
                for k in indices:
                    frame=0 if k<0 else FRAMES[k]
                    scene.frame_set(frame)
                    bpy.context.view_layer.update()
                    name=(f"idle-d{d:02d}.png" if k<0 else f"working-d{d:02d}-f{k:03d}.png")
                    scene.render.filepath=str(output/name)
                    bpy.ops.render.render(write_still=True)
                    report["renders"].append({"file":name,"state":state,"direction":d,"index":k,
                                             "frame":frame,"sha256":sha(output/name)})
                    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    report["render_count"]=len(report["renders"])
    expected={"none":0,"proof":8,"all":68}[args.render]
    if report["render_count"]!=expected:
        raise RuntimeError("Genuine Blender frame count mismatch")
    manifest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_V2_REAL_ARCHIMEDES_BLENDER_BUILT",
          report["render_count"],report["native_sha256"],flush=True)

def main():
    if "--self-check" in sys.argv:
        source()
        print("BEACH_PUMP_V2_SOURCE_AND_OFFSHORE_CONTRACT_PASS",flush=True)
        return
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--render",choices=("none","proof","all"),default="proof")
    ap.add_argument("--samples",type=int,default=16)
    args=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError("Native Cycles sample budget 4..64 only")
    build(args)
if __name__=="__main__":
    main()
