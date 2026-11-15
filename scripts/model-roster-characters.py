"""Build editable first-pass character meshes from MPFB and custom costume geometry.

Run in Blender: --background --python scripts/model-roster-characters.py -- will
Use a new --revision directory to preserve any hand-edited models.
"""
from pathlib import Path
import argparse
import json
import math
import random
import sys
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
from bl_ext.blender_org.mpfb.services.humanservice import HumanService
from bl_ext.blender_org.mpfb.services.targetservice import TargetService
from bl_ext.blender_org.mpfb.services.locationservice import LocationService

args = argparse.ArgumentParser()
args.add_argument('character', choices=['will', 'prince'])
args.add_argument('--revision', default='v1')
opt = args.parse_args(sys.argv[sys.argv.index('--')+1:])
root = Path(__file__).resolve().parents[1]
out = root / 'characters' / opt.character / opt.revision
out.mkdir(parents=True, exist_ok=True)
source = out / (opt.character + '.blend')
if source.exists():
    raise RuntimeError('Use a new revision; refusing to overwrite a saved character.')
data = Path(LocationService.get_user_data())
rng = random.Random(2718 if opt.character == 'will' else 3141)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, color, rough=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_fake_user = True
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Base Color'].default_value = (*color, 1)
    node.inputs['Roughness'].default_value = rough
    node.inputs['Metallic'].default_value = metallic
    return mat

black = material('Hair - near black', (0.004, 0.0025, 0.003), .88)
black.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.16
ivory = material('Ivory cotton and lace', (.84, .79, .67), .72)
white = material('Clean white tee and socks', (.91, .93, .92), .7)
teal = material('Turquoise', (.004, .24, .19), .7)
purple = material('Deep violet satin', (.075, .004, .18), .4)
violet = material('Violet trim', (.16, .009, .34), .6)
yellow = material('Golden yellow', (.75, .40, .008), .7)
gold = material('Antique gold buttons', (.63, .36, .075), .3, .65)
navy = material('Midnight shorts', (.018, .024, .043), .85)
bootmat = material('Black polished leather', (.012, .01, .018), .23)
palette = [teal, violet, yellow, navy]

macro = TargetService.get_default_macro_info_dict()
macro.update(gender=1.0, age=.28 if opt.character == 'will' else .43,
             muscle=.57 if opt.character == 'will' else .42, weight=.43, height=.53)
macro['race'] = {'african': 1., 'caucasian': 0., 'asian': 0.}
body = HumanService.create_human(scale=.118, macro_detail_dict=macro)
body.name = opt.character.title() + '_FaceBody'
if opt.character == 'will':
    targets = {'head-scale-vert-incr':.08,'head-scale-horiz-incr':.25,
               'chin-width-incr':.55,'chin-prominent-incr':.30,
               'nose-scale-depth-incr':.15,'nose-nostrils-width-incr':.12,
               'mouth-scale-horiz-incr':.17,'mouth-upperlip-volume-incr':.14,
               'mouth-lowerlip-volume-incr':.12,'mouth-angles-up':.12}
    for side in ['l','r']:
        targets.update({side+'-ear-scale-incr':.43,side+'-ear-wing-incr':.25,
                        side+'-cheek-bones-incr':.17,side+'-eye-height1-incr':.1})
else:
    targets = {'head-scale-vert-incr':.2,'head-scale-horiz-decr':.17,
               'chin-width-decr':.18,'chin-height-incr':.13,
               'nose-scale-depth-incr':.32,'nose-scale-vert-incr':.18,
               'nose-point-down':.13,'nose-nostrils-width-incr':.15,
               'mouth-scale-horiz-incr':.08,'mouth-upperlip-volume-incr':.15,
               'mouth-lowerlip-volume-incr':.22}
    for side in ['l','r']:
        targets.update({side+'-cheek-inner-incr':.24,side+'-cheek-bones-incr':.17,
                        side+'-eye-height1-decr':.22,side+'-eye-bag-incr':.12})
for name in targets:
    assert TargetService.target_full_path(name), name
TargetService.bulk_load_targets(body, [{'target':k,'value':v} for k,v in targets.items()])
bpy.context.view_layer.update()
# Full evaluated vertex positions with stable source indices, including shape-key offsets.
coords = [v.co.copy() for v in body.data.shape_keys.key_blocks[0].data]
for key in body.data.shape_keys.key_blocks[1:]:
    for i, v in enumerate(key.data):
        coords[i] += (v.co - body.data.shape_keys.key_blocks[0].data[i].co) * key.value
bodygroup = body.vertex_groups['body'].index
skinindices = [v.index for v in body.data.vertices if any(g.group == bodygroup and g.weight > .5 for g in v.groups)]
H = max(coords[i].z for i in skinindices)
s = H / 1.52405
rig = HumanService.add_builtin_rig(body, 'game_engine')
rig.name = opt.character.title() + '_Rig'
rig.show_in_front = True
HumanService.set_character_skin(str(data/'skins/young_african_male/young_african_male.mhmat'),
                                body, skin_type='GAMEENGINE')
for mat in body.data.materials:
    mat.diffuse_color = (.30,.135,.067,1)
    for node in mat.node_tree.nodes:
        if node.type=='BSDF_PRINCIPLED':
            node.inputs['Roughness'].default_value=.68
            node.inputs['Specular IOR Level'].default_value=.22
bone_names = set(rig.data.bones.keys())
tree = KDTree(len(skinindices))
for n,i in enumerate(skinindices):
    tree.insert(coords[i], i)
tree.balance()
skinset = set(skinindices)
skinfaces = [list(p.vertices) for p in body.data.polygons if all(i in skinset for i in p.vertices)]
surface = BVHTree.FromPolygons(coords, skinfaces)

def surface_y(x,z,offset=.001):
    hit = surface.ray_cast(Vector((x,-2*s,z)), Vector((0,1,0)))
    return hit[0].y-offset*s if hit[0] else -.12*s

def skin_weights(obj, fixed=None):
    obj.parent = rig
    mod = obj.modifiers.new('Skin deformation', 'ARMATURE')
    mod.object = rig
    if fixed:
        obj.vertex_groups.new(name=fixed).add(list(range(len(obj.data.vertices))),1,'REPLACE')
        return obj
    groups = {n:obj.vertex_groups.new(name=n) for n in bone_names}
    for v in obj.data.vertices:
        accum = {}
        for _, i, distance in tree.find_n(v.co, 3):
            importance = 1/max(distance,.0005)**2
            for group in body.data.vertices[i].groups:
                name = body.vertex_groups[group.group].name
                if name in bone_names:
                    accum[name] = accum.get(name,0)+importance*group.weight
        total = sum(accum.values())
        if not total:
            accum,total = {'pelvis':1},1
        for name,value in accum.items():
            if value/total>.001:
                groups[name].add([v.index],value/total,'REPLACE')
    return obj

def mesh_obj(name, vertices, faces, mat, fixed=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    obj = bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    for p in mesh.polygons: p.use_smooth=True
    return skin_weights(obj,fixed)

def replace_material(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    for p in obj.data.polygons: p.material_index=0

def asset(path, kind='Clothes', mat=None):
    obj = HumanService.add_mhclo_asset(str(data/path),body,asset_type=kind,
                                    subdiv_levels=0,material_type='GAMEENGINE')
    if mat: replace_material(obj,mat)
    return obj

def crop(obj, delete):
    bm=bmesh.new(); bm.from_mesh(obj.data)
    remove=[f for f in bm.faces if delete(f.calc_center_median()/s)]
    bmesh.ops.delete(bm,geom=remove,context='FACES')
    # Remove unreferenced vertices so exports do not retain deleted sleeves/legs.
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(obj.data); bm.free(); obj.data.update()

def keep_garment_parts(obj, top):
    """Separate shirt and trousers before cropping a combined library outfit."""
    bm=bmesh.new();bm.from_mesh(obj.data)
    visited=set();remove=[]
    for vertex in bm.verts:
        if vertex in visited:continue
        component=set([vertex]);stack=[vertex];visited.add(vertex)
        while stack:
            current=stack.pop()
            for edge in current.link_edges:
                other=edge.other_vert(current)
                if other not in visited:
                    component.add(other);visited.add(other);stack.append(other)
        lo=min(v.co.z for v in component)/s;hi=max(v.co.z for v in component)/s
        keep=(hi>1.10 or (lo>.96)) if top else (hi<1.04 and lo<.8)
        if not keep:remove.extend(component)
    bmesh.ops.delete(bm,geom=remove,context='VERTS')
    bm.to_mesh(obj.data);bm.free();obj.data.update()

def curve_mesh(name, paths, radius, mat, fixed=None):
    curve = bpy.data.curves.new(name,'CURVE')
    curve.dimensions='3D'; curve.resolution_u=1
    curve.bevel_depth=radius; curve.bevel_resolution=0; curve.resolution_u=1
    for points in paths:
        poly = curve.splines.new('POLY'); poly.points.add(len(points)-1)
        for p,co in zip(poly.points,points): p.co=(*co,1)
    obj=bpy.data.objects.new(name,curve); bpy.context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True)
    bpy.context.view_layer.objects.active=obj
    bpy.ops.object.convert(target='MESH')
    obj=bpy.context.object
    obj.data.materials.append(mat)
    for p in obj.data.polygons: p.use_smooth=True
    return skin_weights(obj,fixed)

def sphere(name, center, scale, mat, fixed=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=center)
    obj=bpy.context.object; obj.name=name
    obj.scale=scale
    bpy.ops.object.transform_apply(location=True,rotation=False,scale=True)
    obj.data.materials.append(mat)
    for p in obj.data.polygons:p.use_smooth=True
    return skin_weights(obj,fixed)

eyes=asset('eyes/low-poly/low-poly.mhclo','Eyes')
asset('eyebrows/eyebrow001/eyebrow001.mhclo','Eyebrows',black)

if opt.character == 'will':
    shirt=asset('clothes/male_casualsuit03/male_casualsuit03.mhclo')
    shirt.name='Will_OpenPatternShirt'
    keep_garment_parts(shirt,True)
    # Keep the collar, open the placket, shorten sleeves, and remove trousers.
    crop(shirt,lambda p: p.z<.86 or (abs(p.x)>.24 and p.z<1.15) or
                         (p.y<-.045 and abs(p.x)<.043 and .86<p.z<1.225))
    for v in shirt.data.vertices:
        if abs(v.co.x)<.2*s:
            v.co.x*=1.045; v.co.y*=1.055
    shirt.data.materials.clear()
    for mat in palette:shirt.data.materials.append(mat)
    for p in shirt.data.polygons:
        c=p.center/s
        # Large irregular angular patches carried by actual mesh material slots.
        grid=(math.floor((c.x+c.z*.34)*25), math.floor((c.y-c.z*.13)*22),math.floor(c.z*23))
        hashed=(grid[0]*73+grid[1]*179+grid[2]*43)%13
        p.material_index=0 if hashed<5 else (1 if hashed<8 else (2 if hashed<11 else 3))
    tee=asset('clothes/male_casualsuit04/male_casualsuit04.mhclo',mat=white)
    tee.name='Will_WhiteUndershirt'
    keep_garment_parts(tee,True)
    crop(tee,lambda p:p.z<.89 or abs(p.x)>.205)
    for v in tee.data.vertices: v.co.x*=.995; v.co.y*=.995
    shorts=asset('clothes/male_casualsuit04/male_casualsuit04.mhclo',mat=navy)
    shorts.name='Will_LooseShorts'
    keep_garment_parts(shorts,False)
    crop(shorts,lambda p:p.z>.895 or p.z<.535)
    for v in shorts.data.vertices:
        sign=1 if v.co.x>0 else -1
        center=sign*.112*s
        v.co.x=center+(v.co.x-center)*1.18
        v.co.y*=1.14
    shoes=asset('clothes/shoes05/shoes05.mhclo',mat=white)
    shoes.name='Will_ColorBlockSneakersAndSocks'
    for mat in [teal,violet,yellow,navy]:shoes.data.materials.append(mat)
    for p in shoes.data.polygons:
        c=p.center/s
        p.material_index = 0 if c.z>.09 or c.z<.024 else (1 if c.y<-.1 else (2 if c.x>0 else 3))
    # Hair cap: tapered fade and a broad, nearly flat textured crown.
    vertices=[];faces=[];N=64
    rings=[(1.44,.065,.078),(1.475,.075,.086),(1.51,.080,.088),
           (1.54,.078,.086),(1.553,.065,.065),(1.558,.035,.034),(1.559,.001,.001)]
    for j,(z,rx,ry) in enumerate(rings):
        for i in range(N):
            a=2*math.pi*i/N
            noise=rng.uniform(-.0018,.0018)
            # Sides start above ears; front hairline sits higher on the forehead.
            dz=.025*max(0,-math.sin(a)) if j==0 else 0
            vertices.append(((rx+noise)*math.cos(a)*s,(-.078+(ry+noise)*math.sin(a))*s,(z+dz+noise)*s))
    for j in range(len(rings)-1):
        for i in range(N):
            a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
    mesh_obj('Will_HighTopFade',vertices,faces,black,'head')
    # Dense small raised clumps on the crown give real geometry to the curl texture.
    paths=[]
    for i in range(210):
        x=rng.uniform(-.073,.073); y=rng.uniform(-.071,.071)
        if (x/.075)**2+(y/.078)**2>1:continue
        z=1.552+rng.uniform(-.002,.004)
        paths.append([((x+.0025*math.cos(t))*s,(-.078+y+.0025*math.sin(t))*s,(z+.002*math.sin(t*2))*s) for t in [j*math.pi/3 for j in range(7)]])
    curve_mesh('Will_CrownCurlTexture',paths,.0016*s,black,'head')
else:
    suit=asset('clothes/male_elegantsuit01/male_elegantsuit01.mhclo',mat=purple)
    suit.name='Prince_TailoredPurpleSuit'
    suit.data.materials.append(ivory)
    suit.data.materials.append(violet)
    for p in suit.data.polygons:
        c=p.center/s
        if c.y<-.075 and abs(c.x)<.055 and c.z>1.04:p.material_index=1
        elif c.y<-.075 and .035<abs(c.x)<.095 and 1.01<c.z<1.23:p.material_index=2
    boots=asset('clothes/shoes03/shoes03.mhclo',mat=bootmat)
    boots.name='Prince_BlackBoots'
    # Flared coat tails, split in the back, following the hips and upper legs.
    vertices=[];faces=[];N=36
    for j,(z,rx,ry) in enumerate([(.93,.153,.11),(.83,.172,.12),(.69,.20,.13),(.54,.22,.135)]):
        for i in range(N+1):
            a=-.12+ (math.pi+.24)*i/N
            vertices.append((rx*math.cos(a)*s,(.02+ry*math.sin(a))*s,(z+.012*math.cos(3*a))*s))
    for j in range(3):
        for i in range(N):
            # A small center vent is visible at the lower hem.
            if j==2 and abs(i-N/2)<1:continue
            a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
    mesh_obj('Prince_FlaredCoatTails',vertices,faces,purple)
    # Overlapping, rippled ivory jabot tiers, not a flat printed detail.
    vertices=[];faces=[];W=18
    for tier in range(5):
        z=1.245-tier*.035; width=.033+tier*.006
        start=len(vertices)
        for row in range(4):
            for col in range(W+1):
                u=col/W; x=(u*2-1)*width
                zz=z-row*.012-abs(x)*.22
                y=surface_y(x*s,zz*s,.012)-(.009*math.sin(u*math.pi*8)+row*.002)*s
                vertices.append((x*s,y,zz*s))
        for row in range(3):
            for col in range(W):
                a=start+row*(W+1)+col;faces.append((a,a+1,a+W+2,a+W+1))
    mesh_obj('Prince_LayeredIvoryJabot',vertices,faces,ivory,'spine_03')
    # Wrist ruffles follow each forearm, with fluted edges.
    for side in ['l','r']:
        wrist=rig.data.bones['hand_'+side].head_local
        elbow=rig.data.bones['lowerarm_'+side].head_local
        direction=(wrist-elbow).normalized()
        u=direction.cross(Vector((0,1,0))).normalized();v=direction.cross(u)
        vertices=[];faces=[];N=40
        for row in range(4):
            c=wrist+direction*((row-1)*.014*s)
            for i in range(N):
                a=i*math.tau/N;rad=(.029+row*.003+.004*math.sin(a*10))*s
                vertices.append(tuple(c+rad*(math.cos(a)*u+math.sin(a)*v)))
        for row in range(3):
            for i in range(N):
                a=row*N+i;b=row*N+(i+1)%N;faces.append((a,b,b+N,a+N))
        mesh_obj('Prince_LaceCuff_'+side,vertices,faces,ivory,'hand_'+side)
    # Gold button rows and fine piping along the front of the jacket.
    for sign in [-1,1]:
        for z in [.94,.985,1.03,1.075]:
            x=sign*.055*s;y=surface_y(x,z*s,.02)
            sphere('Prince_GoldButton',(x,y,z*s),(.004*s,.0025*s,.004*s),gold,'spine_02')
    # Curly wig: dense scalp coverage, then shoulder-length side/back ringlets.
    vertices=[];faces=[];N=56
    for j in range(13):
        theta=.05+(math.pi*.62)*j/12
        for i in range(N):
            a=math.tau*i/N
            x=.093*math.sin(theta)*math.cos(a)
            y=-.023+.099*math.sin(theta)*math.sin(a)
            z=1.466+.113*math.cos(theta)
            # Keep the forehead and face free below the hairline.
            vertices.append((x*s,y*s,z*s))
    for j in range(12):
        for i in range(N):
            a=j*N+i;b=j*N+(i+1)%N
            center=(Vector(vertices[a])+Vector(vertices[b+N]))/2/s
            if center.y<-.065 and center.z<1.475:continue
            faces.append((a,b,b+N,a+N))
    mesh_obj('Prince_WigBase',vertices,faces,black,'head')
    paths=[]
    for j in range(10):
        theta=.1+1.9*j/9
        for i in range(18):
            a=math.tau*i/18+rng.uniform(-.07,.07)
            center=Vector((.101*math.sin(theta)*math.cos(a),-.023+.108*math.sin(theta)*math.sin(a),1.466+.12*math.cos(theta)))
            if center.y<-.066 and center.z<1.47:continue
            normal=Vector((center.x,center.y+.023,center.z-1.466)).normalized()
            u=normal.cross(Vector((0,0,1)))
            if u.length<.01:u=Vector((1,0,0))
            u.normalize();v=normal.cross(u)
            points=[]
            for k in range(25):
                t=math.tau*k/12
                p=center+u*(.012*math.cos(t))+v*(.012*math.sin(t))+normal*(.0018*k)
                points.append(tuple(p*s))
            paths.append(points)
    for layer in range(4):
        for i in range(20):
            a=-.1+(math.pi+.2)*i/19
            center=Vector((.105*math.cos(a),.005+.105*math.sin(a),1.34-layer*.036))
            points=[]
            for k in range(31):
                t=k*math.tau/12
                points.append(tuple((center+Vector((.012*math.cos(t),.012*math.sin(t),-.002*k)))*s))
            paths.append(points)
    curve_mesh('Prince_BlackRingletWig',paths,.0038*s,black,'head')

# MPFB delete masks were based on the unedited library clothes. Keep exposed skin
# after shortening sleeves/legs, while retaining the body-only helper mask.
for mod in list(body.modifiers):
    if mod.type=='MASK' and mod.name.startswith('Delete.'):
        body.modifiers.remove(mod)

# A slim moustache follows the actual deformed face surface.
paths=[]
for i in range(240 if opt.character=='prince' else 140):
    sign=rng.choice([-1,1]);u=rng.random()
    x=sign*(.003+u*.024)*s
    z=(1.365-rng.random()*.006-.003*u)*s
    endz=z-.0018*s
    paths.append([(x,surface_y(x,z,.0003),z),(x+sign*.0002*s,surface_y(x,endz,.0003),endz)])
curve_mesh(opt.character.title()+'_Moustache',paths,.00018*s,black,'head')

# Add the concept as a packed reference, hidden from renders and FBX export.
reference = root/'concepts'/('will-face-study-v3.png' if opt.character=='will' else 'chappelle-prince-face-study-v2.png')
image=bpy.data.images.load(str(reference));image.pack()
ref=bpy.data.objects.new('REFERENCE - concept only',None)
ref.empty_display_type='IMAGE';ref.data=image;ref.empty_display_size=H
ref.location=(1.3*H,.6*H,.6*H);ref.rotation_euler=(math.pi/2,0,0)
ref.hide_render=True;bpy.context.collection.objects.link(ref)

scene=bpy.context.scene
scene.unit_settings.system='METRIC'
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.resolution_x=840;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.world.color=(.12,.12,.12)
scene.view_settings.view_transform='AgX'
for name,location,power,size in [('Key',(-2,-3,4),550,3),('Fill',(3,-1,2.5),380,2.5),('Rim',(1,2,3),700,2)]:
    lamp=bpy.data.lights.new(name,'AREA');lamp.energy=power;lamp.shape='DISK';lamp.size=size
    obj=bpy.data.objects.new(name,lamp);bpy.context.collection.objects.link(obj)
    obj.location=location;obj.rotation_euler=(Vector((0,0,H*.65))-obj.location).to_track_quat('-Z','Y').to_euler()
floor_mat=material('Studio floor',(.045,.054,.075),.8)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.012))
floor=bpy.context.object;floor.name='STUDIO - floor';floor.data.materials.append(floor_mat)
bpy.ops.object.camera_add(location=(H*1.1,-H*3.5,H*1.2))
camera=bpy.context.object;camera.name='STUDIO - camera';camera.data.type='ORTHO'
camera.data.ortho_scale=H*1.27
target=Vector((0,-.015,H*.53))
camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera=camera
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=H*1.8
        area.spaces.active.region_3d.view_location=target
        area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
        area.spaces.active.shading.type='MATERIAL'
meshes=[o for o in scene.objects if o.type=='MESH' and o!=floor]
for obj in meshes:
    assert any(m.type=='ARMATURE' and m.object==rig for m in obj.modifiers),obj.name
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes+[rig]:obj.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(source))
bpy.ops.export_scene.fbx(filepath=str(out/(opt.character+'.fbx')),use_selection=True,
    object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False,
    path_mode='COPY',embed_textures=True,axis_forward='-Z',axis_up='Y')
report={'character':opt.character,'revision':opt.revision,'stage':'First modeled pass; likeness review and Unreal retargeting pending',
        'bones':len(rig.data.bones),'base_height_m':H,'face_targets':targets,
        'meshes':[{'name':o.name,'vertices':len(o.data.vertices)} for o in meshes]}
(out/'model-report.json').write_text(json.dumps(report,indent=2))
scene.render.filepath=str(out/'full-body.png')
bpy.ops.render.render(write_still=True)
camera.location=(H*.27,-H*2,H*.97)
camera.rotation_euler=(Vector((0,-.065*s,1.42*s))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=.42*s
scene.render.resolution_x=840;scene.render.resolution_y=840
scene.render.filepath=str(out/'face.png')
bpy.ops.render.render(write_still=True)
print('CHARACTER_MODEL_READY',opt.character,str(source),flush=True)
