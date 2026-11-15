"""Reopen the saved local study and inspect portable geometry/material artifacts."""
from pathlib import Path
import bpy,json,sys,argparse
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--study-dir',default='characters/will/sculpt-study-v1')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=root/args.study_dir
bpy.ops.wm.open_mainfile(filepath=str(out/'will-head-toon-review.blend'))
head=bpy.data.objects.get('Will_Head_EditableCage');eyes=bpy.data.objects.get('Separate_eyes')
assert head and len(head.data.vertices)>1000 and eyes,'Head/eye geometry missing'
used={mat for obj in bpy.context.scene.objects if obj.type in {'MESH','CURVE'} for mat in obj.data.materials if mat}
texture_nodes=[(m.name,n.name) for m in used for n in m.node_tree.nodes if n.type=='TEX_IMAGE']
assert not texture_nodes,'Unexpected projected/image skin texture'
assert any(n.bl_idname=='ShaderNodeShaderToRGB' for m in used for n in m.node_tree.nodes)
assert bpy.data.objects.get('Head_outline_hull'),'Outline mesh missing'
images=['toon-front','toon-three-quarter','toon-profile']
assert all((out/(name+'.png')).is_file() for name in images),'Review image missing'
reference=bpy.data.objects.get('REFERENCE - cel design, not a skin texture')
assert reference and reference.data.packed_file,'Reference image not portable'
report={'artifact_checks':'Passed','likeness_approved':False,'render_engine':bpy.context.scene.render.engine,
    'head_base_vertices':len(head.data.vertices),'surface_image_textures':texture_nodes,'separate_eyes':True,
    'shader':'Three hard diffuse-light bands via Shader to RGB','outline':'inverted mesh hull',
    'reference_image':'Packed unrendered empty, not a surface texture','unreal_assets_changed':False,
    'scope':'Local editable proportion/material study. Facial likeness still needs work.'}
(out/'toon-review-validation.json').write_text(json.dumps(report,indent=2))
print('HEAD_STUDY_REOPENED_AND_INSPECTED',json.dumps(report),flush=True)
