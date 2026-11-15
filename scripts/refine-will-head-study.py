"""Explicit vertex-shaping study with separate eyes and graphic hair.

This is an editable proportion experiment, not an automatic likeness fit.
"""
from pathlib import Path
import bpy,bmesh,math,json,random
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'characters/will/sculpt-study-v1'
bpy.ops.wm.open_mainfile(filepath=str(out/'head-baseline.blend'))
head=bpy.data.objects['Will_Head_EditableCage']

def bump(x,z,cx,cz,sx,sz):return math.exp(-.5*((x-cx)/sx)**2-.5*((z-cz)/sz)**2)
def shape(point):
    x,y,z=point;ax=abs(x);front=max(0,min(1,(-y-.035)/.075))
    # Widen the lower jaw and chin without widening the whole skull.
    x*=1+.085*math.exp(-.5*((z-.078)/.035)**2)*front
    # Broad expressive mouth; preserve the existing lip edge loops.
    mouth=bump(ax,z,0,.102,.037,.018)*front
    x*=1+.17*mouth
    y-=.0025*mouth
    # Lift corners subtly; do not bake a broad smile into the resting mesh.
    z+=.0015*bump(ax,z,.032,.101,.012,.012)*front
    # Cheek planes taper into a fuller jaw; reduce the old hollow cheek.
    cheek=bump(ax,z,.052,.145,.025,.022)*front
    y-=.0035*cheek
    # Slightly broader nasal base and a defined bridge/tip.
    nose=bump(ax,z,0,.142,.019,.020)*front
    x*=1+.10*nose;y-=.003*nose
    # Open upper eyelids a little and raise the outer brow.
    eye=bump(ax,z,.039,.183,.022,.013)*front
    z+=.0012*eye*max(-1,min(1,(z-.181)/.006))
    z+=.0025*bump(ax,z,.049,.202,.025,.012)*front
    # Narrow the neck at its cut, keeping the head and ears intact.
    neck=max(0,1-z/.055)**2;x*=1-.38*neck
    return Vector((x,y,z))
for v in head.data.vertices:v.co=shape(v.co)
head.shape_key_add(name='Study rest geometry')
sub=head.modifiers.new('Editable surface refinement','SUBSURF');sub.levels=1;sub.render_levels=1

def material(name,color):
    mat=bpy.data.materials.new(name);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(*color,1)
    shader.inputs['Roughness'].default_value=.76;return mat
clay=material('Review clay',(.33,.33,.33))
skin=material('Flat warm skin',(.38,.16,.075))
black=material('Graphic hair',(.008,.006,.005))
facial_hair=material('Fine facial hair',(.055,.026,.015))
fade=material('Hair fade',(.055,.027,.016))
white=material('Eye ivory',(.75,.72,.65));brown=material('Iris brown',(.032,.014,.007));pupil=material('Pupil',(.002,.002,.002))
head.data.materials.clear();head.data.materials.append(skin)

# Retain only the eye mesh topology from the source; replace all texture materials.
with bpy.data.libraries.load(str(root/'characters/will/v2/will.blend'),link=False) as (src,dst):
    dst.objects=['Will_FaceBody.low-poly']
eyes=dst.objects[0];bpy.context.collection.objects.link(eyes)
for mod in list(eyes.modifiers):eyes.modifiers.remove(mod)
matrix=eyes.matrix_world.copy();eyes.parent=None
for v in eyes.data.vertices:v.co=shape(matrix@v.co-Vector((0,-.03,1.505)))
eyes.matrix_world.identity();eyes.name='Separate_eyes'
eyes.data.materials.clear()
for mat in [white,brown,pupil]:eyes.data.materials.append(mat)
centres=[]
for sign in [-1,1]:
    verts=[v.co for v in eyes.data.vertices if v.co.x*sign>0]
    lo=Vector([min(v[i] for v in verts) for i in range(3)])
    hi=Vector([max(v[i] for v in verts) for i in range(3)])
    c=(lo+hi)/2;centres.append({'centre':list(c),'lo':list(lo),'hi':list(hi)})
    radius=(hi.x-lo.x)/2
    for poly in eyes.data.polygons:
        cpoly=sum((eyes.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
        if cpoly.x*sign<=0:continue
        radial=math.sqrt((cpoly.x-c.x)**2+(cpoly.z-c.z)**2)
        poly.material_index=2 if radial<radius*.20 and cpoly.y<c.y else (1 if radial<radius*.47 and cpoly.y<c.y else 0)
        poly.use_smooth=True

# Continuous procedural iris boundaries avoid low-poly material-slot stair steps.
eye_mat=material('Procedural eyes - no image textures',(.75,.72,.65))
nodes=eye_mat.node_tree.nodes;links=eye_mat.node_tree.links
geometry=nodes.new('ShaderNodeNewGeometry');separate=nodes.new('ShaderNodeSeparateXYZ')
links.new(geometry.outputs['Position'],separate.inputs[0])
def mathnode(op,a,b=None):
    node=nodes.new('ShaderNodeMath');node.operation=op
    if isinstance(a,(int,float)):node.inputs[0].default_value=a
    else:links.new(a,node.inputs[0])
    if b is not None:
        if isinstance(b,(int,float)):node.inputs[1].default_value=b
        else:links.new(b,node.inputs[1])
    return node.outputs[0]
dx=mathnode('SUBTRACT',mathnode('ABSOLUTE',separate.outputs['X']),abs(centres[0]['centre'][0]))
dz=mathnode('SUBTRACT',separate.outputs['Z'],centres[0]['centre'][2]+.001)
distance=mathnode('SQRT',mathnode('ADD',mathnode('MULTIPLY',dx,dx),mathnode('MULTIPLY',dz,dz)))
ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
for index,(position,color) in enumerate([(0,(.002,.002,.002,1)),(.0038,(.075,.031,.012,1)),(.0078,(.75,.72,.65,1))]):
    element=ramp.color_ramp.elements[0] if index==0 else ramp.color_ramp.elements.new(position)
    element.position=position;element.color=color
links.new(distance,ramp.inputs[0]);links.new(ramp.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
eyes.data.materials.clear();eyes.data.materials.append(eye_mat)
for poly in eyes.data.polygons:poly.material_index=0
smooth=eyes.modifiers.new('Smooth eye surface','SUBSURF');smooth.levels=2;smooth.render_levels=2

def mesh(name,verts,faces,mat):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);data.materials.append(mat)
    return obj
def path(name,points,radius,mat):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=radius;data.bevel_resolution=2
    spline=data.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
    for bp,co in zip(spline.bezier_points,points):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);data.materials.append(mat);return obj

# Query the real face surface for brows, then place broad tapered eyebrow strips.
from mathutils.bvhtree import BVHTree
surface=BVHTree.FromPolygons([v.co for v in head.data.vertices],[list(p.vertices) for p in head.data.polygons])
def surface_y(x,z):
    hit=surface.ray_cast(Vector((x,-.4,z)),Vector((0,1,0)))
    return hit[0].y-.0006 if hit[0] else -.14
for sign in [-1,1]:
    verts=[];faces=[]
    for i in range(12):
        t=i/11;x=sign*(.017+.045*t);z=.204+.004*math.sin(t*math.pi*.9)-.003*t
        width=.003*(1-.7*t)
        for dz in [-width,width]:verts.append((x,surface_y(x,z+dz),z+dz))
        if i:faces.append((2*i-2,2*i,2*i+1,2*i-1))
    mesh('Eyebrow_'+str(sign),verts,faces,black)
    verts=[];faces=[]
    for i in range(12):
        t=i/11;x=sign*(.003+.030*t);z=.114+.0005*math.sin(t*math.pi)-.0015*t
        width=.0011*math.sin(math.pi*(.10+.9*t))
        for dz in [-width,width]:verts.append((x,surface_y(x,z+dz)-.0002,z+dz))
        if i:faces.append((2*i-2,2*i,2*i+1,2*i-1))
    mesh('Fine_moustache_'+str(sign),verts,faces,facial_hair)

# Simple high-top mass, with a separate tapered fade and sparse graphic curls.
N=64;verts=[];faces=[]
rings=[(.181,.052,.084,.106),(.216,.036,.086,.103),(.264,.005,.086,.096),(.290,0,.084,.089),(.300,0,.079,.084)]
for j,(zbase,zfront,rx,ry) in enumerate(rings):
    for i in range(N):
        a=2*math.pi*i/N;front=(1+math.cos(a))/2
        x=rx*math.copysign(abs(math.sin(a))**.86,math.sin(a));y=-.038-ry*math.copysign(abs(math.cos(a))**.86,math.cos(a))
        z=zbase+zfront*front
        if j<2:
            direction=Vector((math.sin(a),-math.cos(a),0))
            hit=surface.ray_cast(Vector((0,-.038,z)),direction)
            if hit[0]:
                point=hit[0]+direction*[.0015,.003][j];x=point.x;y=point.y
        verts.append((x,y,z))
        if j:faces.append(((j-1)*N+i,(j-1)*N+(i+1)%N,j*N+(i+1)%N,j*N+i))
verts.append((0,-.038,.302));tip=len(verts)-1
for i in range(N):faces.append(((len(rings)-1)*N+i,(len(rings)-1)*N+(i+1)%N,tip))
hair=mesh('Graphic_high_top',verts,faces,black);hair.data.materials.append(fade)
hair.data.materials.clear();hair.data.materials.append(fade)
attribute=hair.data.attributes.new('HairFade','FLOAT','POINT')
for i,value in enumerate(attribute.data):value.value=[.18,.84,1,1,1][min(i//N,4)]
node=fade.node_tree.nodes.new('ShaderNodeAttribute');node.attribute_name='HairFade'
mix=fade.node_tree.nodes.new('ShaderNodeMixRGB')
mix.inputs[1].default_value=skin.diffuse_color;mix.inputs[2].default_value=black.diffuse_color
fade.node_tree.links.new(node.outputs['Fac'],mix.inputs[0])
fade.node_tree.links.new(mix.outputs[0],fade.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
for p in hair.data.polygons:
    p.material_index=0
    p.use_smooth=True
# Remove covered scalp surfaces, rather than letting bald skin poke through hair.
head.shape_key_clear()
bm=bmesh.new();bm.from_mesh(head.data)
bmesh.ops.delete(bm,geom=[face for face in bm.faces if all(v.co.z>.242 for v in face.verts)],context='FACES')
bm.to_mesh(head.data);bm.free()
rng=random.Random(2718)
for i in range(115):
    x=rng.uniform(-.077,.077);y=rng.uniform(-.118,.042)
    if (x/.080)**4+((y+.038)/.085)**4>1:continue
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=rng.uniform(.003,.0045),location=(x,y,.302))
    curl=bpy.context.object;curl.name='Graphic_curl';curl.scale.z=.65;curl.data.materials.append(black)

scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=20
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=0
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for light in [o for o in scene.objects if o.type=='LIGHT']:light.data.energy*=.12
camera=scene.camera;camera.data.ortho_scale=.415
target=Vector((0,-.044,.175))
def render(name,location):
    camera.location=location;camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)

# Neutral material review: geometry carries the likeness, no photo texture nodes.
objects=[o for o in scene.objects if o.type=='MESH']
slots={o.name:list(o.data.materials) for o in objects}
for obj in objects:
    if obj==eyes:continue
    for i in range(len(obj.data.materials)):obj.data.materials[i]=clay
render('clay-front',(0,-1,.175));render('clay-profile',(1,-.044,.175))
for obj in objects:
    for i,mat in enumerate(slots[obj.name]):obj.data.materials[i]=mat
camera.location=(.55,-1,.20);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-head-shape-study.blend'))
render('color-three-quarter',(.55,-1,.20));render('color-front',(0,-1,.175))
report={'stage':'Editable vertex-shaping study, not a finished or approved likeness',
    'method':'Explicit region edits on a human topology cage; no landmarks or photo projection',
    'eye_components':centres,'head_vertices':len(head.data.vertices),'head_faces':len(head.data.polygons),
    'separate_eyes':True,'photographic_textures':False,'game_assets_changed':False,
    'limitations':['No face rig','Toon shading and expression work pending','Artist review and likeness approval pending']}
(out/'study-report.json').write_text(json.dumps(report,indent=2));print('WILL_HEAD_SHAPE_STUDY_READY',json.dumps(report),flush=True)
