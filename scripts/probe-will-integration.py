"""Read Unreal animation/retarget APIs and export a reference mannequin."""
from pathlib import Path
import json
import unreal as u
root=Path(u.Paths.project_dir()).parent
out=root/'characters/will/integration-v1';out.mkdir(parents=True,exist_ok=True)
report={'assets':[],'api':{}}
for path in u.EditorAssetLibrary.list_assets('/Game/Characters/Mannequins',recursive=True,include_folder=False):
    if any(s in path for s in ['IK_','RTG_','ABP_','BS_']):report['assets'].append(path)
for cls in ['IKRigController','IKRetargeterController','IKRetargetBatchOperation','IKRigDefinitionFactory',
            'IKRetargetFactory','IKRigDefinition','IKRetargeter','RetargetSourceOrTarget','AutoMapChainType']:
    typ=getattr(u,cls,None)
    if typ:
        report['api'][cls]={name:str(getattr(typ,name).__doc__)[:6500] for name in dir(typ)
            if any(term in name for term in ['auto','chain','retarget','skeletal_mesh','ik_rig','root','operation','op_','batch']) and not name.startswith('_')}
mesh=u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
assert mesh
report['mannequin_skeleton']=mesh.get_editor_property('skeleton').get_path_name()
(out/'unreal-animation-api.json').write_text(json.dumps(report,indent=2))
u.log('WILL_INTEGRATION_PROBE_READY')
