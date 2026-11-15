"""Import the assembled fighter and retarget the existing locomotion assets."""
from pathlib import Path
import json,re
import unreal as u
root=Path(u.Paths.project_dir()).parent;out=root/'characters/will/integration-v1'
base='/Game/Characters/WillV2';tools=u.AssetToolsHelpers.get_asset_tools()
u.EditorAssetLibrary.make_directory(base)
report={}
def save_report(): (out/'unreal-import-report.json').write_text(json.dumps(report,indent=2))
mesh=u.load_asset(base+'/SK_Will')
if not mesh:
    opts=u.FbxImportUI();opts.import_mesh=True;opts.import_as_skeletal=True
    opts.mesh_type_to_import=u.FBXImportType.FBXIT_SKELETAL_MESH
    opts.import_materials=False;opts.import_textures=False;opts.import_animations=False
    task=u.AssetImportTask();task.filename=str(out/'will-runtime.fbx');task.destination_path=base
    task.destination_name='SK_Will';task.automated=True;task.save=True;task.options=opts
    tools.import_asset_tasks([task]);report['imported_paths']=list(task.imported_object_paths);save_report()
    mesh=next((u.load_asset(p) for p in task.imported_object_paths if isinstance(u.load_asset(p),u.SkeletalMesh)),None)
assert mesh,'Skeletal FBX import failed'
report['mesh']=mesh.get_path_name();report['skeleton']=mesh.skeleton.get_path_name();save_report()
assembly=json.loads((out/'assembly-report.json').read_text())
materials={}
for item in assembly['materials']:
    name='M_'+re.sub('[^A-Za-z0-9_]','_',item['name'])
    mat=u.load_asset(base+'/Materials/'+name)
    if not mat:
        mat=tools.create_asset(name,base+'/Materials',u.Material,u.MaterialFactoryNew())
        edit=u.MaterialEditingLibrary
        if item['head_maps']:
            for label,prop,compression in [('basecolor',u.MaterialProperty.MP_BASE_COLOR,None),('normal',u.MaterialProperty.MP_NORMAL,u.TextureCompressionSettings.TC_NORMALMAP),('roughness',u.MaterialProperty.MP_ROUGHNESS,u.TextureCompressionSettings.TC_GRAYSCALE)]:
                texture_name='will_head_'+label
                task=u.AssetImportTask();task.filename=str(root/'characters/will/reference-reconstruction/detailed-v4'/('will-head-'+label+'.png'))
                task.destination_path=base+'/Textures';task.destination_name=texture_name;task.automated=True;task.save=True
                tools.import_asset_tasks([task]);tex=u.load_asset(base+'/Textures/'+texture_name)
                if compression:tex.set_editor_property('compression_settings',compression);tex.set_editor_property('srgb',False)
                if label=='normal':tex.set_editor_property('flip_green_channel',True)
                node=edit.create_material_expression(mat,u.MaterialExpressionTextureSample)
                node.texture=tex
                if label=='normal':node.sampler_type=u.MaterialSamplerType.SAMPLERTYPE_NORMAL
                elif label=='roughness':node.sampler_type=u.MaterialSamplerType.SAMPLERTYPE_LINEAR_GRAYSCALE
                edit.connect_material_property(node,'RGB' if label!='roughness' else 'R',prop)
                u.EditorAssetLibrary.save_loaded_asset(tex)
        else:
            node=edit.create_material_expression(mat,u.MaterialExpressionConstant3Vector)
            node.constant=u.LinearColor(*item['base_color']);edit.connect_material_property(node,'',u.MaterialProperty.MP_BASE_COLOR)
            node=edit.create_material_expression(mat,u.MaterialExpressionConstant);node.r=item['roughness']
            edit.connect_material_property(node,'',u.MaterialProperty.MP_ROUGHNESS)
        edit.recompile_material(mat);u.EditorAssetLibrary.save_loaded_asset(mat)
    mat.set_editor_property('used_with_skeletal_mesh',True)
    u.EditorAssetLibrary.save_loaded_asset(mat)
    materials[item['name']]=mat
slots=mesh.get_editor_property('materials');report['material_slots']=[]
for i,slot in enumerate(slots):
    slotname=str(slot.material_slot_name)
    matching=next((mat for name,mat in materials.items() if re.sub('[^A-Za-z0-9]','',name)==re.sub('[^A-Za-z0-9]','',slotname)),None)
    assert matching,'Unmapped material '+slotname
    slot.material_interface=matching;report['material_slots'].append({'slot':slotname,'material':matching.get_path_name()})
    slots[i]=slot
mesh.set_editor_property('materials',slots);u.EditorAssetLibrary.save_loaded_asset(mesh);save_report()
assert all(slot.material_interface and slot.material_interface.get_path_name().startswith(base+'/Materials/') for slot in mesh.materials),'Material assignments did not persist'
source=u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
chains={'Spine':('spine_01','spine_05','spine_03'),'Head':('neck_01','head','head'),
        'LeftArm':('upperarm_l','hand_l','hand_l'),'RightArm':('upperarm_r','hand_r','hand_r'),
        'LeftLeg':('thigh_l','ball_l','ball_l'),'RightLeg':('thigh_r','ball_r','ball_r'),
        'LeftClavicle':('clavicle_l','clavicle_l','clavicle_l'),'RightClavicle':('clavicle_r','clavicle_r','clavicle_r')}
for side,label in [('l','Left'),('r','Right')]:
    for finger in ['thumb','index','middle','ring','pinky']:
        chains[label+finger.title()]=(finger+'_01_'+side,finger+'_03_'+side,finger+'_03_'+side)
def make_rig(name,preview,target):
    asset=u.load_asset(base+'/Rig/'+name) or tools.create_asset(name,base+'/Rig',u.IKRigDefinition,u.IKRigDefinitionFactory())
    control=u.IKRigController.get_controller(asset);assert control.set_skeletal_mesh(preview)
    control.set_retarget_root('pelvis')
    for chain in list(control.get_retarget_chains()):control.remove_retarget_chain(chain.chain_name)
    for name,(start,end_src,end_target) in chains.items():control.add_retarget_chain(name,start,end_target if target else end_src,'')
    u.EditorAssetLibrary.save_loaded_asset(asset);return asset
src=make_rig('IK_Manny_ForWill',source,False);dst=make_rig('IK_Will',mesh,True)
rtg=u.load_asset(base+'/Rig/RTG_Manny_Will') or tools.create_asset('RTG_Manny_Will',base+'/Rig',u.IKRetargeter,u.IKRetargetFactory())
control=u.IKRetargeterController.get_controller(rtg)
control.set_ik_rig(u.RetargetSourceOrTarget.SOURCE,src);control.set_ik_rig(u.RetargetSourceOrTarget.TARGET,dst)
if control.get_num_retarget_ops()==0:control.add_default_ops()
control.assign_ik_rig_to_all_ops(u.RetargetSourceOrTarget.SOURCE,src)
control.assign_ik_rig_to_all_ops(u.RetargetSourceOrTarget.TARGET,dst)
control.auto_map_chains(u.AutoMapChainType.EXACT,True)
control.auto_align_all_bones(u.RetargetSourceOrTarget.TARGET)
report['chain_mapping']={name:str(control.get_source_chain(name)) for name in chains};save_report()
u.EditorAssetLibrary.save_loaded_asset(rtg)
abp=u.EditorAssetLibrary.find_asset_data('/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed')
retargeted=[]
if not u.EditorAssetLibrary.does_asset_exist(base+'/Animations/Will_ABP_Unarmed'):
    retargeted=u.IKRetargetBatchOperation.duplicate_and_retarget([abp],source,mesh,rtg,prefix='Will_',target_path=base+'/Animations',include_referenced_assets=True,overwrite_existing_files=False)
else:
    retargeted=[u.EditorAssetLibrary.find_asset_data(p) for p in u.EditorAssetLibrary.list_assets(base+'/Animations',recursive=True,include_folder=False)]
report['retargeted_assets']=[str(a.package_name) for a in retargeted];save_report()
u.EditorAssetLibrary.save_directory(base,only_if_is_dirty=False,recursive=True)
assert u.load_asset(base+'/Animations/Will_ABP_Unarmed'),'Missing retargeted animation BP'
report['status']='Imported and retargeted';save_report();u.log('WILL_IMPORT_RETARGET_READY')
