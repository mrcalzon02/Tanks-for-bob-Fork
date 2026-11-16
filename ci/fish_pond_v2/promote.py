"""Promote the explicitly accepted, independently checked pond; preserve receipts."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT/'models/island-survival/fish-pond'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data,indent=2)+'\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--gui',type=Path,required=True)
    a = p.parse_args()
    native,gui = a.native.resolve(),a.gui.resolve()
    source = MODEL/'candidates/v2-production01'
    atlas = MODEL/'candidates/v2-atlases01'
    inspect = json.loads((source/'runtime-inspection.json').read_text())
    approval = json.loads((MODEL/'v2/owner-disposition.json').read_text())
    engine = json.loads((native/'engine-receipt.json').read_text())
    capture = json.loads((gui/'capture-receipt.json').read_text())
    sheets = json.loads((atlas/'atlas-manifest.json').read_text())
    assert approval['accepted'] and inspect['technical_checks_passed'] and sheets['verified']
    assert approval['source_sha256'] == inspect['source_sha256'] == sha(source/'fish-pond-v2.blend')
    assert approval['runtime_sha256'] == inspect['glb_sha256'] == sha(source/'fish-pond-v2.glb')
    assert engine['native_pass'] and engine['reload_pass'] and capture['genuine_factorio_client_capture']
    assert engine['atlas_sha256'] == sheets['files']['working-256.png']['sha256']
    assert len(capture['screenshots']) == 24
    docs = ROOT/'docs/art/fish-pond-v2'
    docs.mkdir(parents=True,exist_ok=True)
    for item in capture['screenshots']:
        file = gui/item['file']
        assert sha(file) == item['sha256']
        shutil.copy2(file,docs/file.name)
    shutil.copy2(gui/'capture-receipt.json',docs/'capture-receipt.json')
    shutil.copy2(native/'engine-receipt.json',docs/'candidate-engine-receipt.json')
    for name in ('native.log','reload.log'):
        shutil.copy2(native/name,docs/('candidate-'+name))
    shutil.copy2(native/'runtime/script-output/fish-pond-v2/native-runtime.json',docs/'native-runtime.json')
    shutil.copy2(MODEL/'v2/owner-disposition.json',docs/'owner-disposition.json')
    destination = ROOT/'tanks_for_bob_fork_1.8.103/graphics/entity/fish-pond-v2'
    destination.mkdir(parents=True,exist_ok=True)
    for state in ('idle','working'):
        file = atlas/(state+'-256.png')
        assert sha(file) == sheets['files'][file.name]['sha256']
        shutil.copy2(file,destination/file.name)
    adapter = (MODEL/'v2/graphics.lua').read_text().replace(
        '-- Staged Fish Pond V2 adapter. Promotion must replace only the asset prefix.',
        '-- Owner-accepted Fish Pond V2: native four-way states, original gameplay.')
    adapter = adapter.replace('__fish-pond-v2-proof__/graphics/',
                              '__tanks_for_bob_fork__/graphics/entity/fish-pond-v2/')
    lua = ROOT/'tanks_for_bob_fork_1.8.103/prototypes/generated_graphics/fish-pond-v2-production.lua'
    lua.write_text(adapter)
    final = ROOT/'tanks_for_bob_fork_1.8.103/data-final-fixes.lua'
    require = 'require("prototypes.generated_graphics.fish-pond-v2-production")'
    text = final.read_text()
    assert require not in text, 'Already promoted; inspect rather than append twice'
    final.write_text(text+'\n-- Accepted Fish Pond: preserved clay basin and restrained swimming animation.\n'+require+'\n')
    manifest = {'schema':'tanks.fish-pond.v2.installed-source','source_sha256':inspect['source_sha256'],
        'runtime_sha256':inspect['glb_sha256'],'working_sha256':sha(destination/'working-256.png'),
        'idle_sha256':sha(destination/'idle-256.png'),'adapter_sha256':sha(lua),'owner_approved':True,
        'candidate_native_verified':True,'production_native_verified':False,'native_engine':'2.1.24',
        'genuine_blender_frames':68,'fps':8,'frame_count':16,'line_length':8,
        'idle_unique_poses_per_facing':1,'idle_native_repeated_cells_per_facing':16,
        'source_cell_size':256,'native_scale':32*3.9/256,'native_shift':[0,-.28/(2**.5)],
        'sprite_only_global_y_scale':2**.5,'runtime_geometry_unit_scale':True,
        'production_recipes_use_fluids':False,'gameplay_fields_changed':False}
    write(destination/'source-manifest.json',manifest)
    review = {'schema':'tanks.fish-pond.v2.visual-review','reviewer':'Codex; explicit owner acceptance recorded separately',
        'source_sha256':inspect['source_sha256'],'runtime_sha256':inspect['glb_sha256'],
        'reference':{'path':'models/island-survival/fish-pond/generated-v1/review-four-directions.png',
                     'sha256':sha(MODEL/'generated-v1/review-four-directions.png')},
        'scores_out_of_five':{'silhouette':4,'construction':4,'surfaces':4,'motion':4,'native_fit':5},
        'disposition':'Accept the restrained existing-basin refinement. Owner accepted and requested integration.',
        'findings':['The continuous excavated basin remains recognizable at native zoom.',
            'Clay banks retain the source damp-floor and dry-rim distinction through baked image maps.',
            'Canonical hollow mouths have continuous closed walls and grounded saddles; no coincident bore surfaces.',
            'Four distinct swimmers follow ellipse tangents and editable tail strokes; all 97 source/export poses match.',
            'Actual native idle/working and all four connected-pipe facings were viewed. No doubled legacy sprite is drawn.'],
        'limitations':['Current fishery recipes do not use fluids; plumbing was additionally exercised with a test-only fluid recipe.',
            'The original native burner smoke and light remain; FMPL GLB contains the working loop, with idle fish visibility described in metadata.'],
        'actual_export_renders':inspect['runtime_renders'],
        'native_images_viewed':['north-normal.png','north-close.png','east-close.png','south-close.png','west-close.png',
            'north-idle-close.png','north-motion-close.png','north-fluid-close.png','east-fluid-close.png',
            'south-fluid-close.png','west-fluid-close.png','north-legacy-close.png'],
        'native_image_hashes':{v['file']:v['sha256'] for v in capture['screenshots']},
        'preview_manifest':json.loads((docs/'preview-manifest.json').read_text()),'owner_approved':True}
    write(docs/'visual-review.json',review)
    fmpl = {'schema':'fmpl.model-delivery.v1','id':'tanks-fish-pond-v2','status':'owner-approved-source-integrated-native-final-check-pending',
        'source_repository':'mrcalzon02/Tanks-for-bob-Fork','prototype':{'type':'assembling-machine','name':'fish-pond'},
        'footprint_tiles':[3,3],'scene_units_per_tile':1,
        'source':{'path':'models/island-survival/fish-pond/candidates/v2-production01/fish-pond-v2.blend','sha256':inspect['source_sha256']},
        'runtime':{'path':'models/island-survival/fish-pond/candidates/v2-production01/fish-pond-v2.glb','sha256':inspect['glb_sha256']},
        'source_and_runtime_pose_checks':97,'packed_pbr_images':3,'capture_policy':'fmpl.factorio45.v1',
        'capture_authority_ref':'939ff2d0fea5d236d7092b907c5f08961d5a7560','production_frames':68,
        'orientations':['north','east','south','west'],'fps':8,'source_fps':48,
        'native_capture_projection':{'global_ground_y_scale':2**.5,'runtime_geometry_changed':False},
        'native_connections':[{'type':'input','prototype_position':[0,-1],'joint_ground':[0,1.5,0]},
                              {'type':'output','prototype_position':[0,1],'joint_ground':[0,-1.5,0]}],
        'idle_state_note':inspect['idle_state_note'],'owner_approved':True,'gameplay_changed':False,
        'native_engine':'2.1.24','candidate_native_test_passed':True,'client_alignment_reviewed':True,
        'evidence':'docs/art/fish-pond-v2/','central_library_registration':'pending final native proof and immutable source commit'}
    write(MODEL/'v2/FMPL_MODEL.json',fmpl)
    print('FISH_POND_ACCEPTED_SOURCE_PROMOTED',json.dumps(manifest))


if __name__ == '__main__':
    main()
