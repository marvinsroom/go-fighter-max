"""Build a separate movement study from unchanged PNGs and engine animation data."""
from pathlib import Path
from PIL import Image
import struct,json,hashlib
root=Path(__file__).resolve().parents[1]
source=root/'sprite-fighter/characters/will'
engine=root/'sprite-fighter/engine/ikemen-go-v1.0.0'
target=engine/'chars/will_motion';target.mkdir(exist_ok=True)
names=['will-stance-v1.png','will-walk-pass-v1.png','will-walk-plant-v1.png','will-walk-lead-v1.png']
data=bytearray(b''.join(bytes((i,i,i,0 if i==0 else 255)) for i in range(256)))
headers=[];frames=[]
for index,name in enumerate(names):
    path=source/'art'/name;png=path.read_bytes()
    with Image.open(path) as image:
        assert image.mode=='RGBA' and image.size==(1024,1536)
        assert image.getchannel('A').getextrema()[0]==0
        bounds=image.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()
    # Keep the same scene axis even when a foot is lifted. Bounding-box bottoms
    # are not valid foot anchors on airborne/passing-step drawings.
    offset=len(data);payload=struct.pack('<I',1024*1536*4)+png;data.extend(payload)
    headers.append(struct.pack('<HHHHhhHBBIIHH',0,index,1024,1536,512,1520,0,12,32,offset,len(payload),0,0))
    frames.append({'sprite':[0,index],'file':'art/'+name,'axis':[512,1520],
        'solid_bounds':list(bounds),'sha256':hashlib.sha256(png).hexdigest()})
header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2))
paloffset=512+len(headers)*28;dataoffset=paloffset+16
struct.pack_into('<IIIIIIII',header,36,512,len(headers),paloffset,1,dataoffset,len(data),dataoffset+len(data),0)
archive=bytes(header)+b''.join(headers)+struct.pack('<HHHHII',1,1,256,0,0,1024)+data
(target/'will-motion.sff').write_bytes(archive)
for i,frame in enumerate(frames):
    values=struct.unpack_from('<HHHHhhHBBIIHH',archive,512+i*28);offset,length=values[9:11]
    assert hashlib.sha256(archive[dataoffset+offset+4:dataoffset+offset+length]).hexdigest()==frame['sha256']
(target/'will_motion.def').write_text('''[Info]
name = "Will Movement Study"
displayname = "Will - Movement Study"
author = "Sitcom Fighter project"
mugenversion = 1.1
localcoord = 1280,720
[Files]
cmd = will-motion.cmd
cns = will-motion.cns
st = will-motion.cns
stcommon = common1.cns
sprite = will-motion.sff
anim = will-motion.air
''',encoding='utf-8')
(target/'will-motion.cmd').write_text('''[Defaults]
command.time = 1
command.buffer.time = 1
[Command]
name = "holdfwd"
command = /$F
time = 1
[Command]
name = "holdback"
command = /$B
time = 1
[Statedef -1]
[State -1, Walk forward]
type = ChangeState
triggerall = roundstate = 2
triggerall = stateno = 0
trigger1 = command = "holdfwd"
value = 20
ctrl = 0
[State -1, Walk backward]
type = ChangeState
triggerall = roundstate = 2
triggerall = stateno = 0
trigger1 = command = "holdback"
value = 21
ctrl = 0
''',encoding='utf-8')
constants=(engine/'chars/will_idle/will-idle.cns').read_text(encoding='utf-8').split('[Statedef 5900]')[0]
constants=constants.replace('; Idle only. No movement, hit reactions or attacks are implemented.','; Movement study. No attacks or hit reactions.')
constants=constants.replace('ground.back = 50','ground.back = 300').replace('ground.front = 70','ground.front = 340')
constants=constants.replace('walk.fwd = 0','walk.fwd = 3.2').replace('walk.back = 0','walk.back = -2.6')
states='''[Statedef 5900]
type = S
physics = N
ctrl = 0
[State 5900, Enter idle]
type = ChangeState
trigger1 = 1
value = 0
ctrl = 0
[Statedef -2]
[State -2, Keep study invulnerable]
type = NotHitBy
trigger1 = 1
value = SCA
time = 1
[State -2, Ground plane]
type = PosSet
trigger1 = 1
y = 0
[State -2, Face opponent]
type = Turn
trigger1 = roundstate = 2
trigger1 = p2dist x < 0
[Statedef 0]
type = S
movetype = I
physics = N
anim = 0
ctrl = 0
velset = 0,0
sprpriority = 0
[State 0, Stop]
type = VelSet
trigger1 = 1
x = 0
y = 0
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
'''
for state,anim,command,speed in [(20,20,'holdfwd',3.2),(21,21,'holdback',-2.6)]:
    states+=f'''
[Statedef {state}]
type = S
movetype = I
physics = N
anim = {anim}
ctrl = 0
[State {state}, Velocity]
type = VelSet
trigger1 = 1
x = {speed}
y = 0
[State {state}, Release to idle]
type = ChangeState
trigger1 = command != "{command}"
trigger2 = roundstate != 2
value = 0
ctrl = 0
'''
(target/'will-motion.cns').write_text(constants+states,encoding='utf-8')
air='''; Idle uses only the approved PNG: a tiny engine-scale breath, no redraw flicker.
[Begin Action 0]
Interpolate Scale
0,0,0,0,36,,,1,1
Interpolate Scale
0,0,0,0,36,,,1,1.004
'''
for action,sequence in [(20,[0,1,2,3]),(21,[0,3,2,1])]:
    air+=f'\n[Begin Action {action}]\n'
    air+=''.join(f'0,{index},0,0,8\n' for index in sequence)
(target/'will-motion.air').write_text(air,encoding='utf-8')
report={'stage':'Forward/back movement study','frames':frames,'scale':.25,
        'idle':'Approved original PNG only; interpolated y-scale 1 to 1.004, anchored feet',
        'walk_forward_sequence':[0,1,2,3],'walk_backward_sequence':[0,3,2,1],
        'walk_ticks_per_drawing':8,'forward_speed':3.2,'backward_speed':-2.6,
        'sff_roundtrip':'Passed; embedded PNG bytes identical','runtime_validation':'Pending',
        'limitations':['Backward uses reversed forward drawings','Walk garment detail varies',
                       'Foot contact timing needs polish','No jump/crouch/attacks/hit reactions','No portraits'],
        'engine_folder':str(target.relative_to(root))}
(source/'motion-build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('WILL_MOTION_PACKAGE_READY',len(archive),'bytes',flush=True)
