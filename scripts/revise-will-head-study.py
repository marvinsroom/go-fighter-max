"""Second editable head study: proportion controls and modeled curl silhouette."""
from pathlib import Path
import bpy, bmesh, math, random, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
out=root/'characters/will/sculpt-study-v2';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/sculpt-study-v1/will-head-shape-study.blend'))
head=bpy.data.objects['Will_Head_EditableCage']
def gauss(x,z,cx,cz,sx,sz):return math.exp(-.5*((x-cx)/sx)**2-.5*((z-cz)/sz)**2)
head.shape_key_clear();head.shape_key_add(name='Previous study')
key=head.shape_key_add(name='Tapered jaw, fuller lips, relaxed lids');key.value=1
for v in key.data:
    x,y,z=v.co;front=max(0,min(1,(-y-.025)/.075))
    # Taper cheek-to-chin silhouette, preserving the ears and skull.
    x*=1-.13*math.exp(-.5*((z-.075)/.044)**2)*front
    mouth=gauss(abs(x),z,0,.105,.037,.014)*front
    x*=1+.16*mouth
    y-=.0035*mouth
    z+=.0018*gauss(abs(x),z,.033,.104,.012,.012)*front
    # Bring upper lids down while retaining eyeball placement and lower rims.
    lid=gauss(abs(x),z,.036,.190,.021,.007)*front
    z-=.0028*lid
    # Broaden the nostril wings without swelling the upper bridge.
    x*=1+.12*gauss(abs(x),z,.014,.139,.010,.009)*front
    # Ear silhouette is deliberately more prominent than the starting cage.
    ear=max(0,min(1,(abs(x)-.071)/.012))*math.exp(-.5*((z-.158)/.037)**2)
    x*=1+.09*ear
    v.co=(x,y,z)
deps=bpy.context.evaluated_depsgraph_get();evaluated=head.evaluated_get(deps)
mesh=evaluated.to_mesh();surface=BVHTree.FromPolygons([v.co for v in mesh.vertices],[list(p.vertices) for p in mesh.polygons]);evaluated.to_mesh_clear()
visible=head.vertex_groups.new(name='Visible face below hair')
visible.add([v.index for v in head.data.vertices if v.co.z<.244],1,'REPLACE')
mask=head.modifiers.new('Hide scalp beneath hair','MASK');mask.vertex_group=visible.name
def skin_y(x,z):
    hit=surface.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
    return hit[0].y-.0008 if hit[0] else -.15
for obj in list(bpy.data.objects):
    if obj.name.startswith(('Graphic_high_top','Graphic_curl','Eyebrow_','Fine_moustache_')):bpy.data.objects.remove(obj,do_unlink=True)
black=bpy.data.materials['Graphic hair'];facial=bpy.data.materials['Fine facial hair']
def make_mesh(name,verts,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.scene.collection.objects.link(obj);data.materials.append(mat)
    for p in data.polygons:p.use_smooth=True
    return obj
for sign in [-1,1]:
    for name,start,length,zbase,width,mat in [('Brow',.016,.047,.200,.0027,black),('Moustache',.003,.034,.116,.0018,facial)]:
        verts=[];faces=[]
        for i in range(20):
            t=i/19;x=sign*(start+length*t)
            z=zbase+(.006*math.sin(math.pi*t)-.004*t if name=='Brow' else -.003*t)
            w=width*(.45+.55*math.sin(math.pi*t))*(1-.4*t)
            for dz in [-w,w]:verts.append((x,skin_y(x,z+dz),z+dz))
            if i:faces.append((2*i-2,2*i,2*i+1,2*i-1))
        make_mesh(name+'_'+str(sign),verts,faces,mat)
# A close scalp fade replaces the old broad smooth hair shell.
with bpy.data.libraries.load(str(root/'characters/will/sculpt-study-v1/head-baseline.blend'),link=False) as (src,dst):dst.objects=['Will_Head_EditableCage']
scalp=dst.objects[0];bpy.context.scene.collection.objects.link(scalp);scalp.name='Close_cut_fade'
scalp.shape_key_clear();scalp.modifiers.clear()
bm=bmesh.new();bm.from_mesh(scalp.data);bm.normal_update()
def hairline(v):
    front=max(0,min(1,(-v.co.y-.025)/.115))
    return .190+.053*front**2
bmesh.ops.delete(bm,geom=[f for f in bm.faces if any(v.co.z<hairline(v) or v.co.z>.265 for v in f.verts)],context='FACES')
for v in bm.verts:v.co+=v.normal*.0015
bm.to_mesh(scalp.data);bm.free()
fade=bpy.data.materials.new('Close fade charcoal');fade.diffuse_color=(.035,.018,.010,1);fade.use_nodes=True
fade.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=fade.diffuse_color
scalp.data.materials.clear();scalp.data.materials.append(fade)
sub=scalp.modifiers.new('Fade smoothing','SUBSURF');sub.levels=1
# Rounded box high-top volume, covered by actual small curl clusters.
N=64;verts=[];faces=[]
for j,(z,rx,ry) in enumerate([(.246,.080,.090),(.269,.083,.092),(.294,.077,.085)]):
    for i in range(N):
        a=2*math.pi*i/N
        verts.append((rx*math.copysign(abs(math.sin(a))**.72,math.sin(a)),-.035-ry*math.copysign(abs(math.cos(a))**.72,math.cos(a)),z))
        if j:faces.append(((j-1)*N+i,(j-1)*N+(i+1)%N,j*N+(i+1)%N,j*N+i))
verts.append((0,-.035,.296))
for i in range(N):faces.append((2*N+i,2*N+(i+1)%N,3*N))
make_mesh('High_top_core',verts,faces,black)
rng=random.Random(160)
curlverts=[];curlfaces=[]
def curl(center,radius):
    # Reuse a low-poly spherical curl topology, joined into one editable mesh.
    bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=2,radius=radius)
    bm.verts.ensure_lookup_table();base=len(curlverts)
    curlverts.extend([tuple(center+Vector((v.co.x,v.co.y,v.co.z*.85))) for v in bm.verts])
    curlfaces.extend([tuple(base+v.index for v in f.verts) for f in bm.faces]);bm.free()
for row in range(5):
    z=.247+row*.011
    for i in range(64):
        a=2*math.pi*(i+rng.uniform(-.25,.25))/64
        rx=.081-(max(0,row-2))*.002;ry=.091-(max(0,row-2))*.002
        curl(Vector((rx*math.copysign(abs(math.sin(a))**.72,math.sin(a)),-.035-ry*math.copysign(abs(math.cos(a))**.72,math.cos(a)),z+rng.uniform(-.002,.002))),rng.uniform(.0035,.0052))
for ix in range(-9,10):
    for iy in range(-10,11):
        x=ix*.008;y=iy*.008
        if (x/.079)**4+(y/.086)**4>1:continue
        curl(Vector((x+rng.uniform(-.002,.002),y-.035+rng.uniform(-.002,.002),.296+rng.uniform(-.0015,.0025))),rng.uniform(.004,.0057))
make_mesh('Modeled_curl_clusters',curlverts,curlfaces,black)
# Preserve editable geometry before a separate rendering script adds toon nodes.
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-head-shape-study.blend'))
(out/'revision-notes.json').write_text(json.dumps({'likeness_approved':False,'method':'Explicit vertex edits and modeled curl clusters, existing human topology','changes':['Tapered lower jaw','Wider fuller mouth','Relaxed upper lids','Lower arched brows','Prominent ears','Close scalp fade and clustered high-top silhouette'],'unreal_assets_changed':False},indent=2))
print('HEAD_V2_GEOMETRY_SAVED',flush=True)
