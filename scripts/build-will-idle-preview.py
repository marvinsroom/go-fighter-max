"""Package unchanged RGBA PNG frames as SFF v2.1 for an idle-only engine preview.

Container layout follows IKEMEN GO v1.0.0 src/image.go. PNG bytes are embedded
unchanged; Pillow is used only for reading frame dimensions/alpha bounds.
"""
from pathlib import Path
from PIL import Image
import struct,json,hashlib
root=Path(__file__).resolve().parents[1]
source=root/'sprite-fighter/characters/will'
target=root/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/will_idle'
target.mkdir(exist_ok=True)
filenames=['will-stance-v1.png','will-idle-inhale-v1.png','will-idle-exhale-v1.png']
sprites=[];data=bytearray();frames=[]
# An ordinary palette entry keeps palette lookup valid for true-color sprites.
palette=b''.join(bytes((i,i,i,0 if i==0 else 255)) for i in range(256))
data.extend(palette)
for index,name in enumerate(filenames):
    path=source/'art'/name;png=path.read_bytes()
    with Image.open(path) as image:
        assert image.mode=='RGBA' and image.size==(1024,1536)
        bounds=image.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()
        assert bounds and image.getchannel('A').getextrema()[0]==0
        width,height=image.size
    axis=(512,bounds[3])
    offset=len(data);payload=struct.pack('<I',width*height*4)+png
    data.extend(payload)
    sprites.append(struct.pack('<HHHHhhHBBIIHH',0,index,width,height,*axis,0,12,32,offset,len(payload),0,0))
    frames.append({'sprite':[0,index],'file':'art/'+name,'size':[width,height],
        'axis':list(axis),'solid_bounds':list(bounds),'sha256':hashlib.sha256(png).hexdigest()})
header=bytearray(512);header[:12]=b'ElecbyteSpr\x00';header[12:16]=bytes((0,0,1,2))
sprite_offset=512;palette_offset=512+28*len(sprites);data_offset=palette_offset+16
struct.pack_into('<IIIIIIII',header,36,sprite_offset,len(sprites),palette_offset,1,
                 data_offset,len(data),data_offset+len(data),0)
palette_header=struct.pack('<HHHHII',1,1,256,0,0,len(palette))
archive=bytes(header)+b''.join(sprites)+palette_header+data
(target/'will-idle.sff').write_bytes(archive)
# Parse back the container and compare the embedded PNG payloads byte for byte.
for i,frame in enumerate(frames):
    values=struct.unpack_from('<HHHHhhHBBIIHH',archive,512+i*28)
    offset,length=values[9:11]
    payload=archive[data_offset+offset+4:data_offset+offset+length]
    assert hashlib.sha256(payload).hexdigest()==frame['sha256']
(target/'will_idle.def').write_text('''; Will idle-only animation preview, not a playable fighter
[Info]
name = "Will Idle Preview"
displayname = "Will - Idle Preview"
author = "Sitcom Fighter project"
mugenversion = 1.1
localcoord = 1280,720
[Files]
cmd = will-idle.cmd
cns = will-idle.cns
st = will-idle.cns
stcommon = common1.cns
sprite = will-idle.sff
anim = will-idle.air
''',encoding='utf-8')
(target/'will-idle.cmd').write_text('''[Command]
name = "start"
command = s
time = 1
[Statedef -1]
''',encoding='utf-8')
(target/'will-idle.cns').write_text('''; Idle only. No movement, hit reactions or attacks are implemented.
[Data]
life = 1000
attack = 100
defence = 100
fall.defence_up = 50
liedown.time = 60
airjuggle = 15
sparkno = 2
guard.sparkno = 40
KO.echo = 0
volume = 0
[Size]
xscale = .25
yscale = .25
ground.back = 50
ground.front = 70
air.back = 50
air.front = 70
height = 375
attack.dist = 0
proj.attack.dist = 0
head.pos = 0,-350
mid.pos = 0,-210
shadowoffset = 0
draw.offset = 0,0
[Velocity]
walk.fwd = 0
walk.back = 0
[Movement]
yaccel = 1.76
stand.friction = .85
crouch.friction = .82
[Statedef 5900]
type = S
physics = N
ctrl = 0
[State 5900, Enter idle]
type = ChangeState
trigger1 = 1
value = 0
ctrl = 0
[Statedef 0]
type = S
movetype = I
physics = N
anim = 0
ctrl = 0
velset = 0,0
sprpriority = 0
[State 0, Stay grounded]
type = PosSet
trigger1 = 1
y = 0
[State 0, No hit reactions in art preview]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[Statedef 190]
type = S
physics = N
anim = 0
ctrl = 0
[State 190, Finish intro]
type = ChangeState
trigger1 = 1
value = 0
ctrl = 0
''',encoding='utf-8')
(target/'will-idle.air').write_text('''; Three distinct PNG drawings, four animation elements, 72 ticks / 1.2 seconds.
[Begin Action 0]
0,0,0,0,18
0,1,0,0,18
0,0,0,0,18
0,2,0,0,18
''',encoding='utf-8')
report={'stage':'Idle animation and scale preview only','design_approved':True,
        'idle_animation_approved':False,'frames':frames,'sequence':[0,1,0,2],
        'ticks_per_frame':18,'loop_seconds':1.2,'sprite_scale':.25,
        'png_payloads_unchanged':True,'sff_roundtrip':'Passed byte comparison',
        'engine_folder':str(target.relative_to(root)),
        'limitations':['No controls/movement','No attack/hit/guard frames','No portraits',
                       'Generated garment details vary between frames; cleanup may be needed']}
(source/'idle-build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('WILL_IDLE_PACKAGE_BUILT',len(archive),'bytes',flush=True)
