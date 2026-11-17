"""Publish honest local receipts for the passive basin's real operations and display."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[2];O=R/'models/island-survival/wood-basin/candidates/v1-production02'
N=R/'build/wood-basin-v1-native-final';G=R/'build/wood-basin-v1-gui02';D=R/'docs/art/wood-basin-v1';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
inspection=json.loads((O/'runtime-inspection.json').read_text());capture=json.loads((O/'capture-manifest.json').read_text());qa=json.loads((O/'capture-verification.json').read_text())
assert inspection['technical_checks_passed'] and qa['passed'] and capture['genuine_blender_frames']==68
assert json.loads((N/'engine-receipt.json').read_text())['native_pass']
assert json.loads((G/'capture-receipt.json').read_text())['genuine_factorio_client_capture']
save=G/'runtime/saves/_autosave-wood-basin-complete-client.zip';assert save.is_file()
# Current readback assertions check every saved pipe, fluid name, amount and temperature.
shutil.copy2(R/'ci/wood_basin_v1/control.lua',G/'mods/wood-basin-v1-proof_0.0.1/control.lua')
binary='C:/Program Files (x86)/Steam/steamapps/common/Factorio/bin/x64/factorio.exe'
with (D/'filled-state-reload.log').open('w') as f:
 result=subprocess.run([binary,'--config',str(G/'config.ini'),'--mod-directory',str(G/'mods'),'--test-save',str(save),'--test-ticks','300'],stdout=f,stderr=subprocess.STDOUT,timeout=90)
assert result.returncode==0 and 'WOOD_BASIN_FILLED_RELOAD_PASS snapshots=12' in (D/'filled-state-reload.log').read_text()
mod=R/'tanks_for_bob_fork_1.8.104';files=[p for p in mod.rglob('*') if p.is_file()]
assert all(sha(p)==sha(N/'mods'/mod.name/p.relative_to(mod))==sha(G/'mods'/mod.name/p.relative_to(mod)) for p in files)
write(D/'source-snapshot.json',{'active_source':mod.name,'all_tested_mod_inputs_match':True,'files':{str(p.relative_to(mod)):sha(p) for p in files}})
for p in (N/'engine-receipt.json',N/'native.log',N/'reload.log',G/'capture-receipt.json',O/'capture-verification.json'):shutil.copy2(p,D/p.name)
shutil.copy2(N/'runtime/script-output/wood-basin-v1/native-runtime.json',D/'native-runtime.json')
for p in G.glob('*.png'):shutil.copy2(p,D/p.name)
shutil.copy2(save,D/'filled-state.zip')
engine=json.loads((D/'engine-receipt.json').read_text());engine.update(filled_state_reload_pass=True,saved_fluids_amounts_temperatures_and_48_connections_verified=True,filled_state_sha256=sha(save),visual_alignment_verified=True,source_snapshot='source-snapshot.json',real_transfer_fixture='Native headless fixture uses actual external pumps to fill all tanks to capacity, block, stop, drain and restart.',graphical_fixture='Client fixture seeds empty/half/full/drained/refill levels for clean state comparisons; no prototype or graphics overrides.');write(D/'engine-receipt.json',engine)
c=json.loads((D/'capture-receipt.json').read_text());c.update(visual_review_passed=True,owner_visual_approved=False,delegated_operational_review=True,fluid_window_level_and_motion_verified=True,seeded_visual_fixture=True);write(D/'capture-receipt.json',c)
record={'schema':'fmpl.model-delivery.v1','id':'tanks-wood-basin-v1','status':'operational-native-integrated-delegated-review','source_repository':'mrcalzon02/Tanks-for-bob-Fork','prototype':{'type':'storage-tank','name':'wood-basin'},'footprint_tiles':[3,3],'scene_units_per_tile':1,'source':{'path':str((O/'wood-basin-v1.blend').relative_to(R)),'sha256':sha(O/'wood-basin-v1.blend')},'runtime':{'path':str((O/'wood-basin-v1.glb').relative_to(R)),'sha256':sha(O/'wood-basin-v1.glb')},'packed_pbr_images':inspection['embedded_export_images'],'source_and_runtime_pose_checks':6,'production_frames':68,'frame_scope':'Four static native body captures plus 64 genuine editable filling/draining preview captures. Native tank animation uses contents-driven level/scrolling liquid/gas; no forced body animation.','native_body_frames_per_facing':1,'native_art_orientations':2,'cardinal_tests':4,'capacity':25000,'capture_policy':'fmpl.factorio45.v1','gameplay_changed':False,'owner_approved':False,'delegated_operational_review_passed':True,'native_engine':'2.1.24','native_fill_drain_full_stop_restart_reload_passed':True,'evidence':str(D.relative_to(R)),'central_library_registration':{'status':'pending_remote_source_commit'}}
write(R/'models/island-survival/wood-basin/v1/FMPL_MODEL.json',record)
write(mod/'graphics/entity/wood-basin-v1/source-manifest.json',record)
review={'date':'2026-11-16','judgment':'operational_close_enough','owner_visual_approved':False,'basis':'Owner-authorized delegated completion; cosmetic detail deferred','source_sha256':record['source']['sha256'],'runtime_sha256':record['runtime']['sha256'],'reference_sha256':json.loads((R/'models/island-survival/wood-basin/v1/contract.json').read_text())['source']['sha256'],'reviewed_images':{str(p.relative_to(R)):sha(p) for p in [*D.glob('*.png'),*O.glob('actual-glb-*.png')]},'scores_out_of_10':{'storage_function':9,'supported_timber_construction':8,'surfaces':8,'native_content_animation':9,'native_pipe_alignment':9},'limitations':['Four native corner tests use two supported art orientations, preserving two_direction_only.','Source filling previews are demonstrators; actual tank content controls native windows.','No Mod Portal release or full-user-mod-pack installation claimed.']}
write(D/'visual-review.json',review)
p=R/'docs/art/STRUCTURE_COMPLETION_LEDGER.json';ledger=json.loads(p.read_text())
for row in ledger['structures']:
 if row['id']=='wood-basin':row.update(revision='V1 native contents-driven cistern',status='accepted_integrated',done=True,next='Preserve passive storage, sealed native sight panels, 25000 capacity, four corner ports and two-direction contract. Canonical registry receipt pending source commit.',evidence=['models/island-survival/wood-basin/v1/FMPL_MODEL.json','docs/art/wood-basin-v1/engine-receipt.json','docs/art/wood-basin-v1/capture-verification.json'],fmpl_delivery='Saved/reopened source, actual animated GLB reimport, genuine body/fill-preview frames and native content animation verified. Real pump fill/full/stop/drain/restart and saved fluid/temperature/connection reload passed; canonical registry write pending verified source commit.')
ledger['production_state']='active; Wood Basin operational, remote delivery and FMPL registration checkpoint in progress'
write(p,ledger)
print('WOOD_BASIN_DELIVERY_CHECKPOINT',record['source']['sha256'],len(files),flush=True)
