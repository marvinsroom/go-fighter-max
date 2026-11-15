"""Fit the detailed head to the weighted outfit/body; preserve a detailed master.

Run with Blender --background --factory-startup --python this-file.
All dimensions are metres. Source models remain untouched.
"""
from pathlib import Path
import bpy, bmesh, json, math
from mathutils import Vector,Matrix

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/integration-v1';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/v2/will.blend'))
keep={'Will_FaceBody','Will_OpenPatternShirt','Will_WhiteUndershirt',
      'Will_LooseShorts','Will_ColorBlockSneakersAndSocks'}
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
for obj in list(bpy.data.objects):
    if obj!=rig and obj.name not in keep:bpy.data.objects.remove(obj,do_unlink=True)

def activate(obj):
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
    bpy.context.view_layer.objects.active=obj

# Freeze the shape keys and helper masks, retaining deform groups, then restore rig.
body=bpy.data.objects['Will_FaceBody']
for obj in [o for o in bpy.data.objects if o.type=='MESH']:
    for mod in list(obj.modifiers):
        if mod.type=='ARMATURE':obj.modifiers.remove(mod)
    activate(obj);bpy.ops.object.convert(target='MESH')
    assert len(obj.vertex_groups)>0, obj.name+' lost weights'
    mod=obj.modifiers.new('Will skeleton','ARMATURE');mod.object=rig

join_z=1.515
def cut(obj,z,upper):
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
        dist=.000001,plane_co=(0,0,z),plane_no=(0,0,1),
        clear_outer=upper,clear_inner=not upper)
    bm.to_mesh(obj.data);bm.free();obj.data.update()

cut(body,join_z,True)
ring=[v for v in body.data.vertices if abs(v.co.z-join_z)<.00001]
assert len(ring)>=8,len(ring)
center=sum((v.co for v in ring),Vector())/len(ring)
ring.sort(key=lambda v:math.atan2(v.co.y-center.y,v.co.x-center.x))
ring_indices=[v.index for v in ring]
group_names={g.index:g.name for g in body.vertex_groups}

def nearest_seam(point):
    best=None
    for a,b in zip(ring,ring[1:]+ring[:1]):
        delta=b.co-a.co;t=max(0,min(1,(point-a.co).dot(delta)/delta.length_squared)) if delta.length_squared else 0
        p=a.co+delta*t;d=(point-p).length_squared
        if best is None or d<best[0]:
            weights={}
            for v,f in [(a,1-t),(b,t)]:
                for g in v.groups:
                    name=group_names[g.group]
                    if name in rig.data.bones:weights[name]=weights.get(name,0)+g.weight*f
            total=sum(weights.values());weights={k:v/total for k,v in weights.items()} if total else {'neck_01':1}
            best=(d,p,weights)
    return best[1:]

source=root/'characters/will/reference-reconstruction/detailed-v4/will-head-detailed-export.blend'
with bpy.data.libraries.load(str(source),link=False) as (src,dst):
    dst.objects=[n for n in src.objects if n in ['Will_HeadSkin','Will_FineEyelashes','Will_FineFacialHair','Will_TexturedCurlClusters','Will_CurlLoops']]
heads=list(dst.objects)
scale=1.02;offset=Vector((0,center.y-.001,join_z-.026*scale))
for obj in heads:
    bpy.context.collection.objects.link(obj)
    for v in obj.data.vertices:v.co=v.co*scale+offset
    obj.parent=rig
    mod=obj.modifiers.new('Will skeleton','ARMATURE');mod.object=rig
    if obj.name=='Will_HeadSkin':
        cut(obj,join_z,False)
        for bone in rig.data.bones:obj.vertex_groups.new(name=bone.name)
        for v in obj.data.vertices:
            dz=v.co.z-join_z
            if dz<.045:
                seam,weights=nearest_seam(Vector((v.co.x,v.co.y,join_z)))
                fade=max(0,1-dz/.045)**2
                v.co.x=v.co.x*(1-fade)+seam.x*fade
                v.co.y=v.co.y*(1-fade)+seam.y*fade
                head_weight=max(0,min(1,dz/.065))
                for name,value in weights.items():obj.vertex_groups[name].add([v.index],value*(1-head_weight),'REPLACE')
                obj.vertex_groups['head'].add([v.index],head_weight,'ADD')
            else:obj.vertex_groups['head'].add([v.index],1,'REPLACE')
    else:
        group=obj.vertex_groups.new(name='head');group.add(list(range(len(obj.data.vertices))),1,'REPLACE')

head=bpy.data.objects['Will_HeadSkin']
seam_error=max(math.sqrt(nearest_seam(v.co)[0].__sub__(v.co).length_squared) for v in head.data.vertices if abs(v.co.z-join_z)<.00001)
assert seam_error<.0001,seam_error

# Use the portable head colour for exposed body skin, avoiding mismatched neck tone.
# Keep the body's UVs; its colour is deliberately uniform until a full-body atlas pass.
skin=bpy.data.materials.new('Will_BodySkin');skin.use_nodes=True
skin.diffuse_color=(.25,.11,.061,1)
shader=skin.node_tree.nodes.get('Principled BSDF')
shader.inputs['Base Color'].default_value=skin.diffuse_color
shader.inputs['Roughness'].default_value=.62
body.data.materials.clear();body.data.materials.append(skin)
for p in body.data.polygons:p.material_index=0

def triangles(obj):return sum(len(p.vertices)-2 for p in obj.data.polygons)
report={'units':'metres','rig_bones':len(rig.data.bones),'neck_seam_rest_error_mm':seam_error*1000,
        'head_scale':scale,'head_offset':list(offset),'source_head_triangles':sum(triangles(o) for o in heads),
        'limitations':['No facial rig or separate eyes','Outfit remains the first modeled pass','Likeness review pending']}
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-fitted-master.blend'))

# Keep a deterministic, evenly distributed subset of tiny disconnected hair strands.
for name,block,stride in [('Will_TexturedCurlClusters',12,20),('Will_CurlLoops',56,10),
                           ('Will_FineFacialHair',8,4),('Will_FineEyelashes',8,2)]:
    obj=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(obj.data);bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if (v.index//block)%stride],context='VERTS')
    bm.to_mesh(obj.data);bm.free()
activate(head)
dec=head.modifiers.new('Runtime skin reduction','DECIMATE');dec.ratio=.5
bpy.ops.object.modifier_move_up(modifier=dec.name)
bpy.ops.object.modifier_apply(modifier=dec.name)

meshes=[o for o in bpy.data.objects if o.type=='MESH']
report['runtime_mesh_triangles']={o.name:triangles(o) for o in meshes}
report['runtime_triangles']=sum(report['runtime_mesh_triangles'].values())
assert report['runtime_triangles']<160000,report['runtime_triangles']
assert all(any(m.type=='ARMATURE' for m in o.modifiers) for o in meshes)
for obj in meshes:
    assert all(sum(g.weight for g in v.groups if obj.vertex_groups[g.group].name in rig.data.bones)>.98 for v in obj.data.vertices),obj.name+' has unweighted vertices'

# Validate attachment through actual evaluated bone poses.
errors={}
for label,axis,degrees in [('rest',2,0),('turn_left',2,45),('turn_right',2,-45),('look_down',0,20),('look_up',0,-20)]:
    bone=rig.pose.bones['head'];bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0)
    bone.rotation_euler[axis]=math.radians(degrees);bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    evaluated_body=body.evaluated_get(deps);bodymesh=evaluated_body.to_mesh()
    evaluated_head=head.evaluated_get(deps);headmesh=evaluated_head.to_mesh()
    # The decimator may simplify the seam, so measure distance to the posed body ring segments.
    posed_ring=[bodymesh.vertices[i].co.copy() for i in ring_indices]
    maximum=0
    for v in head.data.vertices:
        if abs(v.co.z-join_z)>.00001:continue
        point=headmesh.vertices[v.index].co
        minimum=100
        for a,b in zip(posed_ring,posed_ring[1:]+posed_ring[:1]):
            delta=b-a;t=max(0,min(1,(point-a).dot(delta)/delta.length_squared)) if delta.length_squared else 0
            minimum=min(minimum,(point-a-delta*t).length)
        maximum=max(maximum,minimum)
    errors[label]=maximum*1000
    evaluated_body.to_mesh_clear();evaluated_head.to_mesh_clear()
rig.pose.bones['head'].rotation_euler=(0,0,0);bpy.context.view_layer.update()
report['pose_neck_seam_error_mm']=errors
assert max(errors.values())<2,errors
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-runtime.blend'))
# Export in native centimetres. A metre-scaled FBX armature imports with a 100x
# container bone; retargeted local translations then collapse to one hundredth.
for obj in meshes:
    obj.data.transform(Matrix.Scale(100,4))
rig.data.transform(Matrix.Scale(100,4))
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=.01
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
for obj in meshes:obj.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(out/'will-runtime.fbx'),use_selection=True,object_types={'ARMATURE','MESH'},
    add_leaf_bones=False,bake_anim=False,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',path_mode='COPY',embed_textures=True,mesh_smooth_type='FACE')
materials=[]
for mat in {m for obj in meshes for m in obj.data.materials if m}:
    bsdf=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if mat.use_nodes else None
    materials.append({'name':mat.name,'base_color':list(bsdf.inputs['Base Color'].default_value) if bsdf else list(mat.diffuse_color),
                      'roughness':bsdf.inputs['Roughness'].default_value if bsdf else .6,
                      'head_maps':mat==head.data.materials[0]})
report['materials']=materials
(out/'assembly-report.json').write_text(json.dumps(report,indent=2))
print('WILL_ASSEMBLY_READY',json.dumps(report),flush=True)
