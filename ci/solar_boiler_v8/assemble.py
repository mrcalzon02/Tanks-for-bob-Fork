#!/usr/bin/env python3
"""Attach approved floorless V8 Solar Boiler to *BoilerPictureSet* (Factorio 2.1).

No Blender remodeling, no prototype pipe edits, no new workflows. Native V8
renders are authoritative; the in-client visual acceptance remains a separate
test. The generated graphics live INSIDE the selected versioned mod.
"""
from __future__ import annotations
import argparse,hashlib,json,math,re,shutil
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
MOD=ROOT/"tanks_for_bob_fork_1.8.102"
SOURCE=ROOT/"models/island-survival/solar-boiler/generated-v8"
CONTRACT=ROOT/"models/island-survival/solar-boiler/v1/port-contract.json"
DEST=MOD/"graphics/entity/solar-boiler-v8"
MODULE=MOD/"prototypes/generated_graphics/solar-boiler-v8-production.lua"
ENTRY=MOD/"data-final-fixes.lua"
ARTIFACTS=("idle","working")
SIZES=(64,128,256)
DIRS=("north","east","south","west")
# Blender yaw is positive counterclockwise. Factorio rotates boiler clockwise.
# The approved V8 sheet labels its +90 and +270 views opposite Factorio facing.
MODEL_INDEX=(0,3,2,1)
TILE_PX=32
MAX_PILOT_VISUAL_ERROR_PX=24.0 # diagnostic limit, NOT an acceptance threshold
LOADER='require("prototypes.generated_graphics.solar-boiler-v8-production")'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_contract():
    b=json.loads((SOURCE/"build-report.json").read_text())
    q=json.loads((SOURCE/"native-reopen-qa.json").read_text())
    proof=json.loads((SOURCE/"proof-qa.json").read_text())
    ports=json.loads(CONTRACT.read_text())
    assert q["passed"] and proof["passed"] and b["render_count"]==68
    assert q["v8_native_sha256"]==b["native_sha256"]==sha(SOURCE/"solar-boiler-v8.blend")
    assert q["absent_floor_mesh_count"]==11 and q["retained_stationary_supports"]==20
    assert q["max_support_vertex_drift_bu"]==q["max_native_port_vertex_drift_bu"]==0
    assert b["footprint"]==ports["footprint_tiles"]==[3,2]
    assert ports["scene_units_per_tile"]==1 and len(ports["ports"])==3
    assert {p["id"] for p in ports["ports"]}=={"water-west","water-east","steam-north"}
    return b,q,proof,ports

def images_and_integrity(b,proof):
    images={}
    for size in SIZES:
        for state in ARTIFACTS:
            path=SOURCE/f"preview-only-solar-v8-{state}-{size}.png"
            with Image.open(path) as im:
                assert im.mode=="RGBA"
                expected=(4*size,size) if state=="idle" else (8*size,8*size)
                assert im.size==expected,(path,im.size,expected)
                assert im.getchannel("A").getbbox()
                images[(state,size)]=path
    for record in b["renders"]:
        path=SOURCE/record["file"]
        assert sha(path)==record["sha256"],path
    assert sha(SOURCE/"review-four-directions.png")==proof["contact_sha256"]
    return images

def camera_calibration(b):
    cam=b["camera"]
    assert cam["type"]=="ORTHO" and cam["resolution"]==[256,256]
    m=cam["matrix_world"]
    assert abs(m[0][0]-1)<1e-6 and abs(m[1][0])<1e-6
    assert abs(m[2][1]-1/math.sqrt(2))<1e-5
    # 1 Blender unit = 1 Factorio tile; image pixel pitch from orthographic camera.
    pitch=256/cam["ortho_scale"]
    scale256=TILE_PX/pitch
    # Camera looks toward Z~0.93; counter-shift to ground-based Factorio origin.
    shift_y=-(m[1][1]*m[1][3]+m[2][1]*m[2][3])
    shift_x=-(m[0][0]*m[0][3]+m[1][0]*m[1][3]+m[2][0]*m[2][3])
    assert .55<scale256<.57 and -.68<shift_y<-.63 and abs(shift_x)<1e-4
    return {"scale256":scale256,"shift":[shift_x,shift_y],
            "source_pixels_per_tile":pitch,"camera_ortho_scale":cam["ortho_scale"],
            "normal_resolution_scale128":scale256*2,
            "preview_resolution_scale64":scale256*4,
            "correction_tiles":[0,0]}

def lua_module(b,ports,cal):
    # Only the graphics schema is replaced. Boiler fluid boxes and gameplay
    # fields remain on the original prototype; assert contract before touching.
    name="solar-boiler-v8"
    xshift,yshift=cal["shift"]
    scale=cal["scale256"]
    lines=[]
    lines.append("-- Approved native Blender V8 / graphics-only Factorio 2.1 integration.")
    lines.append("-- 3x2 footprint, native fluid boxes and collision unchanged.")
    lines.append('local boiler = assert(data.raw["boiler"] and data.raw["boiler"]["solar-boiler"], "Solar Boiler prototype not found")')
    lines.append('assert(boiler.type=="boiler", "Solar Boiler is not a boiler prototype")')
    lines.append('assert(boiler.selection_box[1][1]==-1.5 and boiler.selection_box[2][1]==1.5, "Solar Boiler footprint unexpectedly changed")')
    lines.append('local water = assert(boiler.fluid_box, "Solar Boiler water fluid box missing")')
    lines.append('local steam = assert(boiler.output_fluid_box, "Solar Boiler steam fluid box missing")')
    lines.append('assert(#water.pipe_connections==2 and #steam.pipe_connections==1, "Boiler pipe connector count changed")')
    lines.append('local function port(p,x,y,direction)')
    lines.append('  assert(p.position[1]==x and p.position[2]==y and p.direction==direction, "Boiler native pipe position changed")')
    lines.append('end')
    lines.append('port(water.pipe_connections[1],-1,0.5,defines.direction.west)')
    lines.append('port(water.pipe_connections[2],1,0.5,defines.direction.east)')
    lines.append('port(steam.pipe_connections[1],0,-0.5,defines.direction.north)')
    lines.append('-- Captures are 256px, 4 directions x 16 frames in one 8x8 atlas.')
    lines.append('-- Camera 45deg ground-center correction; see pipe-placement QA.')
    lines.append('-- Blender +90 is Factorio WEST, so east/west source rows are swapped.')
    lines.append('local texture="__tanks_for_bob_fork__/graphics/entity/solar-boiler-v8/working-256.png"')
    lines.append('local pictures={}')
    for direction,render_index in zip(DIRS,MODEL_INDEX):
        lines.extend((f'pictures.{direction}={{structure={{',
          f'  filename=texture,priority="high",width=256,height=256,',
          f'  x=0,y={render_index*2*256},frame_count=16,line_length=8,',
          f'  animation_speed={8/60:.9f},scale={scale:.9f},',
          f'  shift={{{xshift:.9f},{yshift:.9f}}}',
          '}}'))
    lines.append('boiler.pictures=pictures')
    lines.append('-- Suppress legacy independent boiler layers; full-object V8 art includes all details.')
    lines.append('boiler.structure=nil; boiler.patch=nil; boiler.fire=nil; boiler.fire_glow=nil')
    lines.append('-- No inventory icon, energy, collision, recipes, fluidboxes or prototypes changed.')
    return "\n".join(lines)+"\n"

def rotate_native(x,y,d):
    for _ in range(d):x,y=-y,x
    return x,y

def rotate_model(x,y,index):
    q=math.radians(index*90)
    return x*math.cos(q)-y*math.sin(q),x*math.sin(q)+y*math.cos(q)

def projection_qa(b,ports,cal):
    m=b["camera"]["matrix_world"]
    up=(m[0][1],m[1][1],m[2][1])
    cam=(m[0][3],m[1][3],m[2][3])
    right=(m[0][0],m[1][0],m[2][0])
    scale=cal["scale256"]
    shift=cal["shift"]
    records=[]
    for d,name in enumerate(DIRS):
        row=[]
        for p in ports["ports"]:
            xx,yy=rotate_model(*p["blender_flange_xyz"][:2],MODEL_INDEX[d])
            pt=(xx,yy,p["blender_flange_xyz"][2])
            diff=[pt[i]-cam[i] for i in range(3)]
            px=128+sum(diff[i]*right[i] for i in range(3))*256/b["camera"]["ortho_scale"]
            py=128-sum(diff[i]*up[i] for i in range(3))*256/b["camera"]["ortho_scale"]
            actual=[(px-128)*scale+32*shift[0],(py-128)*scale+32*shift[1]]
            # Native flange at entity edge; x ±1.5; north at y=-1.
            ref=(p["blender_flange_xyz"][0],-p["blender_flange_xyz"][1])
            tx,ty=rotate_native(*ref,d)
            target=[32*tx,32*ty]
            residual=math.dist(actual,target)
            assert residual < MAX_PILOT_VISUAL_ERROR_PX,(name,p["id"],residual)
            row.append({"id":p["id"],"render_direction":MODEL_INDEX[d],
                        "projected_mouth_px":actual,"native_tile_edge_px":target,
                        "center_distance_px":residual})
        records.append({"facing":name,"ports":row})
    return records

def contact_overlay(records):
    # A diagnostic of projected Blender flange centers against Factorio grid
    # edges, not a claim of actual in-game sprite rendering.
    bg=(28,32,36)
    image=Image.new("RGB",(1200,670),bg)
    draw=ImageDraw.Draw(image)
    draw.text((20,12),"SOLAR BOILER V8 — FACTORIO PIPE FIT ALIGNMENT PROJECTION (NOT GAME SCREENSHOT)",fill="white")
    draw.text((20,31),"Red circle = native tile-edge goal | cyan = projected Blender flange | yellow = difference | in-client confirmation pending",fill=(212,224,224))
    for d,record in enumerate(records):
        left=20+295*d;top=80
        with Image.open(SOURCE/f"idle-d{MODEL_INDEX[d]:02d}.png") as src:
            tile=src.convert("RGBA")
        image.paste(tile,(left,top),tile)
        draw.text((left+7,58),record["facing"].upper(),fill="white")
        for p in record["ports"]:
            a=p["projected_mouth_px"];b=p["native_tile_edge_px"]
            # work in approved Blender source pixels, rather than stretched sprites
            s=1/(32/(256/4.45))
            ox=left+128;oy=top+128
            u=(ox+a[0]*s,oy+a[1]*s)
            v=(ox+b[0]*s,oy+b[1]*s)
            draw.line((u[0],u[1],v[0],v[1]),fill=(255,213,94),width=2)
            for pt,color in ((u,(39,234,223)),(v,(247,81,80))):
                draw.ellipse((pt[0]-5,pt[1]-5,pt[0]+5,pt[1]+5),outline=color,width=2)
        worst=max(p["center_distance_px"] for p in record["ports"])
        draw.text((left+8,top+264),f"largest projection difference: {worst:.1f}px",fill=(232,208,160))
        draw.text((left+8,top+286),"Requires in-game confirmation",fill=(240,225,191))
    draw.text((20,630),"Approved V8 source kept unchanged. No claim of native Factorio image alignment until the actual client screenshot is reviewed.",fill=(232,222,190))
    image.save(SOURCE/"pipe-placement-qa.png",optimize=True)

def preflight():
    b,q,p,ports=read_contract()
    images=images_and_integrity(b,p)
    cal=camera_calibration(b)
    records=projection_qa(b,ports,cal)
    source=(MOD/"prototypes/entity/entities.lua").read_text()
    assert re.search(r'local solar_boiler\s*=\s*table\.deepcopy\(data\.raw\["boiler"\]\["boiler"\]\)',source)
    assert source.count('solar_boiler.name = "solar-boiler"')==1
    assert json.loads((MOD/"info.json").read_text())["factorio_version"]=="2.1"
    return b,q,p,ports,images,cal,records

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--install",action="store_true")
    args=ap.parse_args()
    b,q,p,ports,images,cal,records=preflight()
    report={"schema":"tanks.solar-boiler.v8.engine-candidate",
      "approved_v8_native_sha256":b["native_sha256"],
      "mod":"tanks_for_bob_fork_1.8.102","footprint":[3,2],
      "source_blender_directions":list(MODEL_INDEX),
      "factorio_directions":list(DIRS),
      "calibration":cal,"port_projections":records,
      "pipe_visual_test":"pending-client-screenshots",
      "engine_smoke":"pending-engine-execution",
      "sprite_qa":True,"model_accepted":True,
      "visual_alignment_accepted":False}
    if args.install:
        assert not DEST.exists() and not MODULE.exists(), "Do not overwrite published Factorio graphics"
        for (state,size),path in images.items():
            DEST.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,DEST/f"{state}-{size}.png")
            assert sha(path)==sha(DEST/f"{state}-{size}.png")
        MODULE.parent.mkdir(parents=True,exist_ok=True)
        MODULE.write_text(lua_module(b,ports,cal))
        code=ENTRY.read_text()
        assert LOADER not in code
        ENTRY.write_text(code.rstrip()+"\n\n-- Approved V8 Solar Boiler; BoilerPictureSet adapter, 3x2 original connections.\n"+LOADER+"\n")
        contact_overlay(records)
        report["files"]={str(path.relative_to(MOD)):sha(path) for path in sorted(DEST.glob("*.png"))}
        report["module_sha256"]=sha(MODULE)
        report["stage_loader_sha256"]=sha(ENTRY)
        report["candidate_installed"]=True
        report["pipe_overlay_sha256"]=sha(SOURCE/"pipe-placement-qa.png")
    out=SOURCE/"factorio-placement-receipt.json"
    if args.install:out.write_text(json.dumps(report,indent=2)+"\n")
    print("SOLAR_V8_INTEGRATION_ASSET_PROJECTION_PASS",len(records),"directions; best-effort placement diagnostic, visual client QA pending",flush=True)
if __name__=="__main__":main()
