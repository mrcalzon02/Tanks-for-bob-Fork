#!/usr/bin/env python3
"""V4 visual silhouette correction on actual native Blender V3, no image generation."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,math,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
PARENT_BUILDER=HERE.parent/"v3"/"build_beach_pump_v3.py"
spec=importlib.util.spec_from_file_location("tanks_beach_pump_v3",PARENT_BUILDER)
v3=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=v3
spec.loader.exec_module(v3)
CONSTRUCT_V3=v3.refine_construct

def final_silhouette(bpy,v1,contract,original,root,ports):
    from mathutils import Vector
    result=CONSTRUCT_V3(bpy,v1,contract,original,root,ports)
    # Preserve the four anchored footings, separate skids, 45-degree
    # camera and full-bore native endpoint; thin only the visible woodwork.
    floor=sorted((o for o in bpy.data.objects if
                  o.name.startswith("DOCK | narrow separated driftwood plank")),
                 key=lambda ob:ob.name)
    if len(floor)!=5:raise RuntimeError("V3 floor source count changed")
    for i in (1,2,3):
        bpy.data.objects.remove(floor[i],do_unlink=True)
    slim_names=(
        "DOCK | crooked wooden upright",
        "DOCK | tied longitudinal side rail",
        "DOCK | rope post",
        "SCREW | full length wooden open casing side rail",
        "SCREW | transverse trough support",
        "SCREW | diagonal support strut",
    )
    slim_count=0
    for ob in bpy.data.objects:
        if any(ob.name.startswith(n) for n in slim_names):
            ob.scale.x*=.74
            ob.scale.y*=.74
            slim_count+=1
        elif ob.name.startswith("DOCK | long warped skids"):
            ob.scale.x*=.80
            ob.scale.z*=.80
        elif ob.name.startswith("TROUGH | raised visible retaining side"):
            ob.scale.z*=.82
    if slim_count<12:raise RuntimeError("Lattice/slat thinning incomplete")
    # V3's 0.28 BU wheel was largely unreadable at 64px next to an 1.5 BU
    # sloped screw; enlarge radial wheel only, retaining exact axle center.
    wheel=bpy.data.objects["MOTION | full bucket waterwheel shaft"]
    if tuple(round(v,4) for v in wheel.scale)!=(1.,1.,1.):
        raise RuntimeError("Unexpected V3 wheel parent scale")
    wheel.scale=(.96,1.38,1.38)
    # Wheel-readable asymmetry: moving index bead and well-defined grip bands
    # live on the true rotating wheel parent, not stationary overlay art.
    col=bpy.data.objects["WHEEL | cupped tapered paddle 00"].users_collection[0]
    brass=bpy.data.materials["BEACH | weathered brass"]
    for i,x in enumerate((.185,.270)):
        ring=v1.cylinder(bpy,f"CRANK | V4 grip band {i:02d}",
                 (x,0,.246),.061,.018,brass,col,wheel,
                 rotation=(0,math.pi/2,0),n=32)
        ring["rotates_with_crank"]=True
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,
                                         radius=.023,location=(0,.302,0))
    marker=v1.move(bpy,bpy.context.object,col,wheel)
    marker.name="WHEEL | asymmetrical bright face index"
    marker.data.materials.append(brass)
    marker["motion_proof"]="on actual rotating parent, not billboard"
    result.update(
       v4_silhouette_open=True,
       remaining_dock_planks=2,
       slim_supports=slim_count,
       wheel_scale_radial=1.38,
       native_pipe_unchanged=True,
       face_index_count=1,
       crank_grip_bands=2)
    return result

def main():
    if "--self-check" in sys.argv:
        c,original,donor=v3.v2.source()
        assert c["lock"]["native_output_position"]==[0,.25]
        assert c["lock"]["water_per_tick"]==.01
        print("BEACH_PUMP_V4_OFFSHORE_NATIVE_DONOR_SOURCE_PASS",flush=True)
        return
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--render",choices=("none","proof","all"),default="all")
    ap.add_argument("--samples",type=int,default=16)
    args=ap.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:])
    if not 4<=args.samples<=64:raise ValueError("Cycles samples 4..64")
    # Native construction happens before any Cycles frame render.
    v3.refine_construct=final_silhouette
    v3.main()
    import bpy
    output=args.out.resolve()
    original_path=output/"beach-pump-v3.blend"
    if not original_path.is_file():raise RuntimeError("Native V3-derived editable source not saved")
    result=output/"beach-pump-v4.blend"
    if result.exists():raise RuntimeError("V4 proof destination already exists")
    root=bpy.data.objects["EXPORT | rotate beachpump not camera"]
    root.rotation_euler.z=0
    bpy.context.scene.frame_set(0)
    bpy.context.scene["source_model"]="Tanks beachpump V4: open native screw + prominent 8-bucket waterwheel"
    bpy.context.scene["game_integrated"]=False
    bpy.context.scene["human_visual_approved"]=False
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(result),compress=True,check_existing=False)
    if not result.is_file() or result.stat().st_size<500000:
        raise RuntimeError("V4 genuine native .blend not preserved")
    original_path.unlink()
    reportpath=output/"build-report.json"
    report=json.loads(reportpath.read_text(encoding="utf-8"))
    report["schema"]="tanks.beach-pump.v4.archimedes-native-blender"
    report["native_sha256"]=hashlib.sha256(result.read_bytes()).hexdigest()
    report["visual_refinement"]="V4 open deck, thin wood braces, 38% enlarged real wheel radial geometry, rotating face index"
    report["game_integrated"]=False
    report["human_visual_approved"]=False
    reportpath.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("BEACH_PUMP_V4_TRUE_NATIVE_BLENDER_ALL_FRAMES_PASS",
          report["render_count"],report["native_sha256"],flush=True)

if __name__=="__main__":main()
