"""Refine the generated head locally with eyes, lids, curls and skin shading.

This edits real mesh geometry in a new version. No uploads or landmark fitting.
"""
from pathlib import Path
import math
import json
import random
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

root=Path(__file__).resolve().parents[1]
parent=root/'characters/will/reference-reconstruction'
out=parent/'detailed-v4';out.mkdir(exist_ok=True)
source=out/'will-head-detailed.blend'
if source.exists():raise RuntimeError('Refusing to overwrite the detailed head.')
bpy.ops.wm.open_mainfile(filepath=str(parent/'will-head-textured-v2.blend'))
head=next(o for o in bpy.context.scene.objects if o.type=='MESH')
head.name='Will_HeadSkin'
mesh=head.data
original=np.array([list(v.co) for v in mesh.vertices])
lo=original.min(axis=0);hi=original.max(axis=0)
rng=random.Random(70841)

def smooth(a,b,x):
    t=max(0.,min(1.,(x-a)/(b-a)))
    return t*t*(3-2*t)

def hair_weight(p):
    x,y,z=p
    front=1-smooth(-.10,-.025,y)
    front_line=.260-.018*(min(abs(x)/.105,1)**1.4)
    back_line=.207+.006*min(abs(x)/.10,1)
    line=back_line*(1-front)+front_line*front
    return smooth(line-.012,line+.012,z)

# Correct the inflated rear silhouette and soften the angular jaw/chin.
for vertex in mesh.vertices:
    p=vertex.co
    if p.y>0:p.y*=.60
    jaw=math.exp(-((p.z-.095)/.029)**2)*(1-smooth(-.015,.035,p.y))
    if abs(p.x)>.022:
        p.x+=math.copysign(.0030*jaw*smooth(.022,.06,abs(p.x)),p.x)
    crown=smooth(.29,.338,p.z)
    p.x*=1-.055*crown
    p.y=-.015+(p.y+.015)*(1-.035*crown)
    if p.z>.295:p.z-=.003*crown
    if p.y<-.06:
        for sign in [-1,1]:
            dx=p.x-sign*.0425;dz=p.z-.1825
            influence=math.exp(-((dx/.019)**4+(dz/.012)**4))
            p.z+=dz*.11*influence
mesh.update()
surface=BVHTree.FromPolygons([v.co.copy() for v in mesh.vertices],[list(p.vertices) for p in mesh.polygons])

def skin_y(x,z,offset=0):
    hit=surface.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
    return hit[0].y-offset if hit[0] else -.1-offset

def material(name,color,rough=.5,spec=.3):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=(*color,1)
    shader.inputs['Roughness'].default_value=rough
    shader.inputs['Specular IOR Level'].default_value=spec
    mat.diffuse_color=(*color,1)
    return mat,shader

def add_micro_normal(mat,shader,scale=5200,strength=.16,distance=.00007):
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    coord=nodes.new('ShaderNodeTexCoord')
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale
    noise.inputs['Detail'].default_value=2.0;noise.inputs['Roughness'].default_value=.65
    links.new(coord.outputs['Object'],noise.inputs['Vector'])
    bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength
    bump.inputs['Distance'].default_value=distance
    links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs['Normal'],shader.inputs['Normal'])

def mesh_obj(name,verts,faces,mat,uv=None):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    for poly in data.polygons:poly.use_smooth=True
    if uv:
        layer=data.uv_layers.new(name='ReferenceUV')
        for loop in data.loops:layer.data[loop.index].uv=uv(data.vertices[loop.vertex_index].co)
    return obj

ref=bpy.data.images.load(str(parent/'will-head-input-v1.png'),check_existing=True)
pixels=np.asarray(ref.pixels[:]).reshape(ref.size[1],ref.size[0],4)
yy,xx=np.where(pixels[:,:,3]>.5)
uvlo=np.array([xx.min()/ref.size[0],yy.min()/ref.size[1]])
uvhi=np.array([(xx.max()+1)/ref.size[0],(yy.max()+1)/ref.size[1]])
def reference_uv(p):
    return tuple(uvlo+np.array([(p.x-lo[0])/(hi[0]-lo[0]),(p.z-lo[2])/(hi[2]-lo[2])])*(uvhi-uvlo))

# Keep the photographed front but replace its stretched side/back projection.
mat,shader=material('Will skin - detailed',(.27,.11,.05),.52,.28)
nodes=mat.node_tree.nodes;links=mat.node_tree.links
old_image=next(n.image for n in head.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE')
photo=nodes.new('ShaderNodeTexImage');photo.image=old_image
color=mesh.color_attributes.new(name='PhotoFrontWeight',type='FLOAT_COLOR',domain='CORNER')
scalp=mesh.color_attributes.new(name='ScalpFadeWeight',type='FLOAT_COLOR',domain='CORNER')
eye_mask=mesh.color_attributes.new(name='EyeSurfaceMask',type='FLOAT_COLOR',domain='CORNER')
for loop in mesh.loops:
    p=mesh.vertices[loop.vertex_index].co
    front=(1-smooth(-.075,-.012,p.y))*(1-.75*smooth(.073,.106,abs(p.x)))
    color.data[loop.index].color=(front,front,front,1)
    weight=hair_weight(p);scalp.data[loop.index].color=(weight,weight,weight,1)
    eye=0.
    if p.y<-.06:
        for sign in [-1,1]:
            radius=((p.x-sign*.0425)/.018)**2+((p.z-.1825)/.006)**2
            eye=max(eye,1-smooth(.7,1.2,radius))
    eye_mask.data[loop.index].color=(eye,eye,eye,1)
attr=nodes.new('ShaderNodeVertexColor');attr.layer_name='PhotoFrontWeight'
mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.29,.125,.060,1)
links.new(attr.outputs['Color'],mix.inputs[0]);links.new(photo.outputs['Color'],mix.inputs[2])
hairattr=nodes.new('ShaderNodeVertexColor');hairattr.layer_name='ScalpFadeWeight'
hairmix=nodes.new('ShaderNodeMixRGB');hairmix.inputs[2].default_value=(.006,.0035,.0025,1)
links.new(hairattr.outputs['Color'],hairmix.inputs[0]);links.new(mix.outputs[0],hairmix.inputs[1])
links.new(hairmix.outputs[0],shader.inputs['Base Color'])
rough=nodes.new('ShaderNodeMath');rough.operation='MULTIPLY_ADD'
rough.inputs[1].default_value=.31;rough.inputs[2].default_value=.54
links.new(hairattr.outputs['Color'],rough.inputs[0])
eye_attribute=nodes.new('ShaderNodeVertexColor');eye_attribute.layer_name='EyeSurfaceMask'
eye_rough=nodes.new('ShaderNodeMixRGB');eye_rough.inputs[2].default_value=(.20,.20,.20,1)
links.new(eye_attribute.outputs['Color'],eye_rough.inputs[0]);links.new(rough.outputs[0],eye_rough.inputs[1])
links.new(eye_rough.outputs[0],shader.inputs['Roughness'])
if 'Subsurface Weight' in shader.inputs:
    shader.inputs['Subsurface Weight'].default_value=.07
    shader.inputs['Subsurface Radius'].default_value=(1.,.4,.2)
    shader.inputs['Subsurface Scale'].default_value=.002
add_micro_normal(mat,shader)
for node in nodes:
    if node.type=='BUMP':
        pore_strength=nodes.new('ShaderNodeMath');pore_strength.operation='MULTIPLY_ADD'
        pore_strength.inputs[1].default_value=-.16;pore_strength.inputs[2].default_value=.16
        links.new(eye_attribute.outputs['Color'],pore_strength.inputs[0]);links.new(pore_strength.outputs[0],node.inputs['Strength'])
        break
skin_normal=shader.inputs['Normal'].links[0].from_socket
hair_noise=nodes.new('ShaderNodeTexVoronoi');hair_noise.inputs['Scale'].default_value=1600
hair_coord=nodes.new('ShaderNodeTexCoord');links.new(hair_coord.outputs['Object'],hair_noise.inputs['Vector'])
hair_bump=nodes.new('ShaderNodeBump');hair_bump.inputs['Distance'].default_value=.00075
links.new(hairattr.outputs['Color'],hair_bump.inputs['Strength']);links.new(hair_noise.outputs['Distance'],hair_bump.inputs['Height'])
links.new(skin_normal,hair_bump.inputs['Normal']);links.new(hair_bump.outputs['Normal'],shader.inputs['Normal'])
mesh.materials.clear();mesh.materials.append(mat)
for poly in mesh.polygons:poly.material_index=0

# Keep the reference eye surfaces and add fine upper lashes. Socket replacement
# experiments were visually rejected; they are preserved only in older files.
lash_paths=[]
for sign in [-1,1]:
    for i in range(45):
        dx=rng.uniform(-.017,.017)
        x=sign*.0425+dx
        z=.1825+.0045*max(0,1-(dx/.0185)**2)**.65
        y=skin_y(x,z,.00013)
        lash_paths.append([(x,y,z),(x+sign*.00015,y-.00035,z+rng.uniform(.0005,.0010))])
hair_mats=[]
for index,color in enumerate([(.003,.002,.0015),(.005,.003,.002),(.008,.005,.003)]):
    h,hs=material('Black curl variation '+str(index),color,.84,.15)
    hair_mats.append(h)

def paths_obj(name,paths,radius,mat):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D'
    curve.bevel_depth=radius;curve.bevel_resolution=0;curve.resolution_u=1
    for points in paths:
        spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
        for point,co in zip(spline.points,points):point.co=(*co,1)
    obj=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
    bpy.ops.object.convert(target='MESH');obj=bpy.context.object;obj.data.materials.append(mat)
    for poly in obj.data.polygons:poly.use_smooth=True
    return obj

paths_obj('Will_FineEyelashes',lash_paths,.000055,hair_mats[0])

# Fine brow/moustache fibers sit on the skin instead of being only in its color map.
face_fibers=[]
for sign in [-1,1]:
    for i in range(180):
        t=rng.random();x=sign*(.018+.049*t)
        z=.207+.007*math.sin(t*math.pi)-.006*t+rng.uniform(-.0013,.0013)
        endx=x+sign*rng.uniform(.0006,.0016);endz=z+rng.uniform(.001,.0025)
        face_fibers.append([(x,skin_y(x,z,.00012),z),(endx,skin_y(endx,endz,.00018),endz)])
    for i in range(280):
        t=rng.random();x=sign*(.002+.028*t)
        z=.129-.008*t-rng.random()*.004
        endz=z-rng.uniform(.0007,.0016)
        face_fibers.append([(x,skin_y(x,z,.0001),z),(x+sign*.00015,skin_y(x,endz,.00015),endz)])
paths_obj('Will_FineFacialHair',face_fibers,.000055,hair_mats[0])

# Real curl clusters around all sides of the high top replace its smooth block.
triangles=[];areas=[]
for poly in mesh.polygons:
    points=[mesh.vertices[i].co.copy() for i in poly.vertices]
    center=poly.center
    if hair_weight(center)<.90:continue
    for j in range(1,len(points)-1):
        tri=(points[0],points[j],points[j+1]);area=(tri[1]-tri[0]).cross(tri[2]-tri[0]).length*.5
        if area>0:triangles.append(tri);areas.append(area)
cumulative=np.cumsum(areas)
bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1)
bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
for i,vertex in enumerate(bm.verts):vertex.index=i
ico_v=[v.co.copy() for v in bm.verts];ico_f=[[v.index for v in f.verts] for f in bm.faces];bm.free()
verts=[];faces=[];material_indices=[];curl_paths=[]
for index in range(20000):
    tri=triangles[int(np.searchsorted(cumulative,rng.random()*cumulative[-1]))]
    a,b,c=tri;u=math.sqrt(rng.random());v=rng.random();p=(1-u)*a+u*(1-v)*b+u*v*c
    normal=(b-a).cross(c-a).normalized()
    tangent=normal.cross(Vector((0,0,1)))
    if tangent.length<.1:tangent=normal.cross(Vector((0,1,0)))
    tangent.normalize();bitangent=normal.cross(tangent)
    radius=rng.uniform(.00115,.00185)
    start=len(verts)
    for iv in ico_v:
        irregular=.90+rng.random()*.2
        point=p+normal*(radius*.3)+radius*irregular*(iv.x*tangent+iv.y*bitangent+iv.z*.85*normal)
        verts.append(tuple(point))
    for face in ico_f:faces.append(tuple(start+i for i in face));material_indices.append(rng.choices([0,1,2],[.6,.3,.1])[0])
    if index%40==0:
        points=[]
        for k in range(14):
            t=k*math.pi/5
            points.append(tuple(p+radius*(math.cos(t)*tangent+math.sin(t)*bitangent)+normal*(radius*.5+k*.000055)))
        curl_paths.append(points)
clusters=mesh_obj('Will_TexturedCurlClusters',verts,faces,hair_mats[0])
for h in hair_mats[1:]:clusters.data.materials.append(h)
for poly,mi in zip(clusters.data.polygons,material_indices):poly.material_index=mi
paths_obj('Will_CurlLoops',curl_paths,.00013,hair_mats[0])

scene=bpy.context.scene
for name,energy in [('Key',9),('Fill',4),('Rim',10)]:bpy.data.lights[name].energy=energy
scene.world.color=(.025,.025,.025)
scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=0
scene.render.resolution_x=1100;scene.render.resolution_y=1100
scene.cycles.samples=40;scene.cycles.use_denoising=True
camera=scene.camera;camera.data.ortho_scale=.385
camera.location=(.50,-1,.19);camera.rotation_euler=(Vector((0,0,.17))-camera.location).to_track_quat('-Z','Y').to_euler()
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
        area.spaces.active.region_3d.view_location=(0,0,.17)
        area.spaces.active.region_3d.view_distance=.65
        area.spaces.active.shading.type='MATERIAL'
meshes=[o for o in scene.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes:obj.select_set(True)
bpy.context.view_layer.objects.active=head
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(source))
report={'stage':'Detailed head study; not rigged or fitted to body',
        'changes':['Less inflated rear skull','Broader lower jaw','Subtle eye-opening sculpt and smoother eye shading',
                   'Fine modeled upper lashes','20000 curl clusters with 500 curl loops',
                   'Modeled brow/moustache fibers','Blended side/rear skin and scalp fade','Skin micro-normal and softer lighting'],
        'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons)} for o in meshes],
        'limitations':['Likeness requires review','No facial rig','No game integration','Portable detail-map bake/export pending']}
(out/'detail-report.json').write_text(json.dumps(report,indent=2))
for name,location in [('three-quarter',(.50,-1,.19)),('front',(0,-1,.17)),('profile',(1,0,.17))]:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.17))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('DETAILED_HEAD_REVIEW_READY',flush=True)

