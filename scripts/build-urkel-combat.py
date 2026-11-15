"""Build Steve Urkel's standalone first playable kit. Source PNGs stay intact."""
from pathlib import Path
from PIL import Image
import hashlib, io, json, math, re, struct, wave
import will_agent_j as bank
import urkel_stefan as stefan

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sprite-fighter/characters/urkel'
ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
OUT=ENGINE/'chars/urkel'; OUT.mkdir(parents=True,exist_ok=True)
POSES={'idle':350,'palm':350,'kick':320,'crouch':225,'gadget':350,'stumble':310,'hurt':350,'down':135}
payload=bytearray(b''.join(bytes((i,i,i,0 if i==0 else 255)) for i in range(256)))
headers=[]; meta={}
def png(key,number,group=20,path=None,height=None,name=None):
    path=path or SOURCE/'art/v1'/f'{key}.png'; raw=path.read_bytes()
    with Image.open(path) as im:
        assert im.mode=='RGBA', path
        w,h=im.size; bounds=im.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()
        assert bounds and im.getchannel('A').getextrema()[0]==0, path
    axis=((bounds[0]+bounds[2])//2 if key=='down' else w//2,bounds[3])
    offset=len(payload); block=struct.pack('<I',w*h*4)+raw; payload.extend(block)
    headers.append(struct.pack('<HHHHhhHBBIIHH',group,number,w,h,*axis,0,12,32,offset,len(block),0,0))
    if group in (20,30,40):meta[name or key]={'group':group,'number':number,'axis':axis,'bounds':bounds,'scale':(height or POSES[key])/(bounds[3]-bounds[1]),
                          'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest()}
for i,key in enumerate(POSES):png(key,i)
for i,(key,height) in enumerate(stefan.POSES.items()):
    png(key,i,30,path=SOURCE/'art/stefan-v1'/f'{key}.png',height=height,name='stefan_'+key)
for i,key in enumerate(['idle','punch']):png('robot-'+key,i,40,height=460,name='robot_'+key)
def alias(group,number,key):
    m=meta[key]
    index=next(i for i,h in enumerate(headers) if struct.unpack_from('<HH',h)==(m['group'],m['number']))
    fields=list(struct.unpack('<HHHHhhHBBIIHH',headers[index]))
    fields[0]=group;fields[1]=number;fields[6]=index;fields[9]=0;fields[10]=0
    headers.append(struct.pack('<HHHHhhHBBIIHH',*fields))
# Opponent-owned ChangeAnim2 actions can request Will's reaction indices. These
# compatibility sprites still contain only Urkel artwork, never Will's PNGs.
for i,key in enumerate(['idle','idle','idle','idle','palm','crouch','kick','palm','palm','kick','hurt','down','idle','idle']):alias(0,i,key)
for i,key in enumerate(['idle','palm','palm','kick','crouch','hurt','down']):alias(10,i,'stefan_'+key)
def raw_sprite(number,width,height,fn,axis=None):
    pixels=bytearray()
    for y in range(height):
        for x in range(width):pixels.extend(fn(x,y))
    offset=len(payload);payload.extend(pixels)
    headers.append(struct.pack('<HHHHhhHBBIIHH',7000,number,width,height,*(axis or (width//2,height//2)),0,0,32,offset,len(pixels),0,0))
def cheese(x,y):
    inside=6<x<74 and 6<y<54 and y>52-(x-6)*.65
    hole=any((x-a)**2+(y-b)**2<r*r for a,b,r in [(30,40,5),(57,32,6),(61,47,3)])
    return (170,98,12,255) if inside and hole else (255,211,50,255) if inside else (0,0,0,0)
raw_sprite(0,80,60,cheese)
raw_sprite(1,640,360,lambda x,y:(7,40 if x%40==0 or y%40==0 else 15,41 if x%40==0 or y%40==0 else 27,255),(0,0))
def machine(x,y):
    if 25<x<231 and 135<y<345:
        if 40<x<213 and 155<y<225:return (40,225,176,255) if x%18<3 or y%18<3 else (8,45,45,255)
        if 45<x<210 and 253<y<270:return (244,192,60,255)
        if 40<x<220 and 290<y<320:return (35,45,60,255)
        return (85,105,118,255)
    if 115<x<141 and 28<y<138:return (234,185,56,255) if y%20<10 else (92,115,125,255)
    if ((x-128)/80)**2+((y-110)/25)**2<1:return (48,230,190,255)
    if (x-128)**2+(y-25)**2<18**2:return (255,218,80,255)
    if 10<x<246 and 340<y<358:return (45,56,70,255)
    return (0,0,0,0)
raw_sprite(2,256,360,machine,(128,360))
def gear(x,y):
    dx=x-63.5;dy=y-63.5;r=math.hypot(dx,dy);a=math.atan2(dy,dx)
    inside=22<r<45+(12 if math.cos(a*12)>.2 else 0)
    return (255,201,65,255) if inside else (0,0,0,0)
raw_sprite(3,128,128,gear)
raw_sprite(4,128,128,lambda x,y:(65,255,195,int(255*max(0,1-abs(math.hypot(x-63.5,y-63.5)-45)/7))))
raw_sprite(5,128,128,lambda x,y:(255,215,90,int(255*max(0,1-abs(math.hypot(x-63.5,y-63.5)-45)/7))))
header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2))
pal=512+28*len(headers);data=pal+16
struct.pack_into('<IIIIIIII',header,36,512,len(headers),pal,1,data,len(payload),data+len(payload),0)
archive=bytes(header)+b''.join(headers)+struct.pack('<HHHHII',1,1,256,0,0,1024)+payload
(OUT/'urkel.sff').write_bytes(archive)
for item in meta.values():
    entry=next(struct.unpack('<HHHHhhHBBIIHH',h) for h in headers if struct.unpack_from('<HH',h)==(item['group'],item['number']))
    offset,length=entry[9:11]
    assert hashlib.sha256(archive[data+offset+4:data+offset+length]).hexdigest()==item['sha256']

air=[]
def action(number,frames,active=(),kind='S',attack=(20,-285,200,-110),hurt=True):
    air.append(f'\n[Begin Action {number}]')
    for i,(key,duration,*extra) in enumerate(frames):
        if hurt:
            box=(-60,-215,65,0) if kind=='C' else (-55,-330,60,0)
            air.extend(['Clsn2: 1','Clsn2[0] = '+','.join(map(str,box))])
        if i in active:air.extend(['Clsn1: 1','Clsn1[0] = '+','.join(map(str,attack))])
        m=meta[key]; scale=m['scale']
        air.append(f'{m["group"]},{m["number"]},0,0,{duration},,,{scale:.7f},{scale:.7f},{extra[0] if extra else 0}')
for number,key in [(0,'idle'),(5,'idle'),(6,'crouch'),(10,'crouch'),(11,'crouch'),(12,'idle'),(20,'stumble'),(21,'idle'),
                   (40,'crouch'),(41,'kick'),(42,'kick'),(43,'kick'),(47,'crouch'),(52,'crouch')]:
    action(number,[(key,36 if number in (0,20,21) else -1)])
for number in list(range(120,123))+list(range(130,133))+list(range(140,143))+list(range(150,156)):
    action(number,[('crouch' if number in (121,131,141,152,153) else 'hurt' if number>=150 else 'idle',8)])
for number in [170,175,180,181,190,191,195]:action(number,[('down' if number in (170,175) else 'idle',30)])
for number in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:action(number,[('hurt',-1)])
for number in [5100,5110,5140,5150,5160,5170]:action(number,[('down',6 if number in (5100,5160) else -1)],hurt=False)
action(5120,[('down',10),('crouch',10),('idle',5)])
for number in [5200,5210,5220,5300,5500,5510]:action(number,[('crouch',8),('idle',8)])
for number in [820,821,8250,8260,3050,3250,4550]:action(number,[('hurt',-1)],hurt=False)
NORMALS={200:('Nervous Palm','palm',6,3,12,30,'S','MA',False),
         210:('Elbow Oops','stumble',11,4,17,52,'S','MA',False),
         220:('High-Waist Heel','kick',18,5,24,82,'S','MA',True),
         400:('Ankle Tap','crouch',7,3,13,26,'C','L',False),
         410:('Trouser Sweep','kick',15,4,25,58,'C','L',True),
         420:('Panic Button','palm',12,5,24,78,'C','MA',True),
         600:('Air Flail','palm',7,5,15,34,'A','H',False),
         610:('Saddle-Shoe Kick','kick',10,6,19,58,'A','H',True),
         620:('Falling Accident','stumble',15,7,22,72,'A','H',True)}
for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    box=(15,-85,205,-5) if kind=='C' and guard=='L' else (15,-300,205,-95)
    action(number,[('crouch' if kind=='C' else 'kick' if kind=='A' else 'idle',start),(pose,active),
                   ('crouch' if kind=='C' else 'kick' if kind=='A' else 'idle',recovery)],active=(1,),kind=kind,attack=box)
for number in [800,810]:action(number,[('palm',5),('palm',4),('idle',25)],active=(1,),attack=(0,-300,105,-60))
for number in [801,811]:action(number,[('palm',10),('stumble',10),('idle',15)])
action(1000,[('idle',18),('gadget',6),('idle',25)])
action(1100,[('idle',20),('stumble',8),('idle',30)],active=(1,),attack=(0,-275,225,-30))
action(1200,[('idle',24),('palm',5),('idle',28)],active=(1,),attack=(20,-340,230,-130))
action(1300,[('idle',36)])
action(3000,[('gadget',16),('stumble',12),('gadget',12),('stumble',18),('idle',42)])
action(3200,[('idle',24),('gadget',6),('idle',35)],active=(1,),attack=(15,-320,225,-90))
action(3210,[('gadget',36),('stumble',36),('gadget',60),('crouch',48),('idle',60)])
air.extend(['\n[Begin Action 6400]','Clsn1: 1','Clsn1[0] = -32,-22,32,22','7000,0,0,0,-1'])
air.extend(['\n[Begin Action 6401]','7000,1,0,0,-1,,,2,2'])
action(6402,[('robot_idle',-1)],hurt=False)
action(6403,[('robot_punch',-1)],hurt=False)
air.extend(['\n[Begin Action 6404]']+[f'7000,3,0,0,4,,,1.8,1.8,{angle}' for angle in [0,90,180,270]])
air.extend(['\n[Begin Action 6405]','7000,4,0,0,8,,,1,1','7000,4,0,0,8,,,3,3','7000,4,0,0,8,,,5,5'])
air.extend(['\n[Begin Action 6406]','Clsn1Default: 1','Clsn1[0] = -64,-64,64,64','7000,3,0,0,4,,,2,2,0','7000,3,0,0,4,,,2,2,90'])
air.extend(['\n[Begin Action 6407]','7000,5,0,0,8,,,1,1','7000,5,0,0,8,,,3,3','7000,5,0,0,8,,,5,5'])
stefan.animations(action)
stefan.variants(air,meta)
(OUT/'urkel.air').write_text('\n'.join(air)+'\n',encoding='utf-8')
(OUT/'urkel-common.cns.zss').write_text(bank.common_states((ENGINE/'data/common1.cns.zss').read_text(encoding='utf-8')),encoding='utf-8')
(OUT/'urkel.def').write_text('''[Info]
name="Steve Urkel"
displayname="Steve Urkel"
author="Sitcom Fighter project"
mugenversion=1.1
localcoord=1280,720
[Files]
cmd=urkel.cmd
cns=urkel.cns
st=urkel.cns
stcommon=urkel-common.cns.zss
sprite=urkel.sff
anim=urkel.air
sound=urkel.snd
''',encoding='utf-8')
commands={'L':'a','M':'b','H':'c','skill':'x','super_short':'y','ultimate_short':'z','throw':'d',
          'cheese':'D, DF, F, a','stumble':'D, DB, B, b','snap':'D, DF, F, c','retreat':'D, DB, B, c',
          'holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
commands['transform']='w'
cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={20 if len(keys)>2 and not keys.startswith("/") else 1}\n'
cmd+='\n[Statedef -1]\n'
def command(label,target,conditions):
    global cmd
    if target in NORMALS or target in (1000,1100,1200,1300,3000,3200):conditions=['var(30)=0']+conditions
    cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions[:-1])+f'trigger1={conditions[-1]}\nvalue={target}\nctrl=0\n'
stefan.commands(command)
g=['roundstate=2','statetype!=A','ctrl']
for name,target,cost in [('ultimate_short',3200,2000),('super_short',3000,1000)]:command(name,target,g+[f'power>={cost}',f'command="{name}"'])
for name,target in [('cheese',1000),('stumble',1100),('snap',1200),('retreat',1300),('skill',1100)]:command(name,target,g+[f'command="{name}"'])
for target,back in [(810,True),(800,False)]:command('Throw',target,g+['p2bodydist x<75','p2statetype!=A','p2movetype!=H',f'command="throw" && command{"=" if back else "!="}"holdback"'])
for name,target in [('H',620),('M',610),('L',600)]:command('Air '+name,target,['roundstate=2','statetype=A','ctrl',f'command="{name}"'])
for name,target in [('H',420),('M',410),('L',400)]:command('Low '+name,target,g+['command="holddown"',f'command="{name}"'])
for name,target in [('H',220),('M',210),('L',200)]:command(name,target,g+[f'command="{name}"'])
command('Crouch',10,g+['stateno!=10','command="holddown"'])
command('Jump',40,g+['command="holdup"'])
command('Forward',20,g+['stateno=0','command="holdfwd"'])
command('Back',21,g+['stateno=0','command="holdback"'])
command('CPU attack',210,g+['ailevel>0','p2bodydist x<150','random<35'])
command('CPU approach',20,g+['ailevel>0','stateno=0','p2bodydist x>160'])
(OUT/'urkel.cmd').write_text(cmd,encoding='utf-8')
cns='''[Data]
life=1000
power=3000
attack=100
defence=100
fall.defence_up=50
liedown.time=40
airjuggle=15
sparkno=2
guard.sparkno=40
KO.echo=0
volume=0
[Size]
xscale=1
yscale=1
ground.back=45
ground.front=45
air.back=45
air.front=45
height=345
attack.dist=210
proj.attack.dist=280
proj.doscale=1
head.pos=0,-310
mid.pos=0,-170
shadowoffset=0
draw.offset=0,0
[Velocity]
walk.fwd=2.8
walk.back=-2.1
jump.neu=0,-12.5
jump.fwd=3.5,-12.5
jump.back=-3,-12.5
[Movement]
yaccel=.65
stand.friction=.85
crouch.friction=.82
airjump.num=0
stand.friction.threshold=.1
'''
def state(number,anim=None,kind='S',move='I',**params):
    global cns
    cns+=f'\n[Statedef {number}]\ntype={kind}\nmovetype={move}\nphysics=N\nctrl=0\n'
    if anim is not None:cns+=f'anim={bank.animation_value(anim)}\n'
    cns+=''.join(f'{k}={v}\n' for k,v in params.items())
def ctl(number,label,kind,triggers='1',**params):
    global cns
    if kind in ('ChangeAnim','ChangeAnim2') and 'value' in params:params['value']=bank.animation_value(params['value'])
    cns+=f'\n[State {number}, {label}]\ntype={kind}\n'
    cns+=''.join(f'trigger1={t}\n' for t in (triggers if isinstance(triggers,list) else [triggers]))
    cns+=''.join(f'{k.replace("__",".")}={v}\n' for k,v in params.items())
def end(number,air=False,crouch=False):ctl(number,'Recover','ChangeState','animtime=0',value=50 if air else 10 if crouch else 0,ctrl=1)
def hit(number,start,damage,kind='S',guard='MA',fall=False,**params):
    base=dict(attr=kind+',NA',damage=f'{damage},{int(damage*.03)}',guardflag=guard,hitflag='MAF',priority='4,Hit',
              pausetime='6,8',sparkno=2,sparkxy='-10,-180',hitsound='S0,1',guardsound='S0,2',animtype='Hard' if fall else 'Medium',
              ground__type='Low' if fall else 'High',ground__hittime=20,ground__slidetime=12,
              ground__velocity='-4,-5' if fall else '-3',air__velocity='-4,-5',fall=int(fall),getpower='45,10',givepower='25,10',id=number)
    base.update(params);ctl(number,'Contact','HitDef',f'time={start}',**base)
state(-2)
stefan.globals(ctl)
ctl(-2,'Face opponent','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'No automatic turn','AssertSpecial',flag='noautoturn')
for effect in [6401,6402,6403,6404,6405]:ctl(-2,'Cinematic cleanup','RemoveExplod','stateno!=3210',ID=effect)
state(0,0,velset='0,0');ctl(0,'Control','CtrlSet',value=1);ctl(0,'Ground','PosSet',y=0)
state(10,10,kind='C',velset='0,0');ctl(10,'Control','CtrlSet',value=1);ctl(10,'Stand','ChangeState','command!="holddown"',value=0,ctrl=1)
for number,speed,held in [(20,2.8,'holdfwd'),(21,-2.1,'holdback')]:
    state(number,number);ctl(number,'Control','CtrlSet',value=1);ctl(number,'Walk','VelSet',x=speed,y=0)
    ctl(number,'Stop','ChangeState',f'(ailevel=0 && command!="{held}") || (ailevel>0 && p2bodydist x<140)',value=0,ctrl=1)
state(40,40);ctl(40,'Direction','VarSet','time=0',**{'var(1)':'ifelse(command="holdfwd",3.5,ifelse(command="holdback",-3,0))'})
ctl(40,'Take off','ChangeState','time>=3',value=50,ctrl=1)
state(50,41,kind='A');ctl(50,'Control','CtrlSet',value=1)
ctl(50,'Launch','VelSet',['time=0','prevstateno=40'],x='var(1)',y=-12.5)
ctl(50,'Gravity','VelAdd',y=.65);ctl(50,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
state(52,52,velset='0,0');ctl(52,'Ground','PosSet',y=0);ctl(52,'Recover','ChangeState','time>=5',value=0,ctrl=1)
for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    state(number,number,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}))
    hit(number,start,damage,kind,guard,fall)
    if kind=='A':ctl(number,'Gravity','VelAdd',y=.65);ctl(number,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
    end(number,kind=='A',kind=='C')
for number,cost,start,damage,speed,anim,offset in [(1000,0,18,48,8,6400,'120,-275'),(3000,1000,40,210,15,6406,'120,-275')]:
    state(number,number,move='A',velset='0,0',poweradd=-cost)
    if cost:ctl(number,'Overcharge pause','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0)
    ctl(number,'Invention shot','Projectile',f'time={start}',projid=number,projanim=anim,projhitanim=-1,projremanim=-1,
        projremove=1,projremovetime=140,velocity=f'{speed},0',offset=offset,attr='S,HP' if cost else 'S,SP',damage=f'{damage},2',
        guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=22,
        ground__velocity='-5,-5' if cost else '-3',air__velocity='-5,-5',fall=int(bool(cost)),getpower='0,0' if cost else '50,10',givepower='20,10',hitsound='S0,1')
    ctl(number,'Scientific cue','PlaySnd',f'time={start}',value='0,3')
    if cost:
        for tick in [16,28,40]:
            ctl(number,'Malfunction sparks','Explod',f'time={tick}',anim=6405,postype='p1',pos='120,-275',scale='.4,.4',removetime=-2,sprpriority=6,ownpal=1)
            ctl(number,'Sputter recoil','VelSet',f'time={tick}',x=-3 if tick<40 else -7)
            ctl(number,'Sputter cue','PlaySnd',f'time={tick}',value='0,3')
        ctl(number,'Recoil drag','VelMul','time>16',x=.84)
    end(number)
state(1100,1100,move='A',velset='0,0');hit(1100,20,85,fall=True,attr='S,SA')
ctl(1100,'Trip forward','VelSet','time=[14,27]',x=5)
ctl(1100,'Stop stumble','VelSet','time>=28',x=0);end(1100)
state(1200,1200,move='A',velset='0,0');hit(1200,24,90,guard='H',attr='S,SA');end(1200)
state(1300,1300,velset='0,0');ctl(1300,'Back off','VelSet','time<18',x=-5)
ctl(1300,'Stop','VelSet','time>=18',x=0);end(1300)
for number,nextstate in [(800,801),(810,811)]:
    state(number,number,move='A',velset='0,0')
    ctl(number,'Grab','HitDef','time=5',attr='S,NT',hitflag='M-',priority='1,Miss',sparkno=-1,guard__dist=0,
        pausetime='0,0',p1stateno=nextstate,p2stateno=8250,fall=1,numhits=0,getpower='0,0',givepower='0,0',id=number)
    end(number)
for number,back in [(801,False),(811,True)]:
    state(number,number,move='A',velset='0,0')
    if back:ctl(number,'Back throw','Turn','time=0')
    ctl(number,'Hold','TargetBind','time<18',pos='100,-30')
    ctl(number,'Throw damage','TargetLifeAdd','time=18',value=-105,kill=1)
    ctl(number,'Let go','TargetState','time=18',value=8260);end(number)
state(3200,3200,move='A',velset='0,0',poweradd=-2000)
ctl(3200,'Invention pause','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0)
hit(3200,24,0,attr='S,HA',p1stateno=3210,p2stateno=8250,getpower='0,0',givepower='0,0');end(3200)
state(3210,3210,move='A',velset='0,0')
ctl(3210,'Sequence protection','NotHitBy',value='SCA',time=1)
ctl(3210,'Frame laboratory','ScreenBound',value=0,movecamera='0,0')
ctl(3210,'Frame inventor','PosSet',x='camerapos x-facing*260',y=0)
ctl(3210,'Blueprint laboratory','Explod','time=0',anim=6401,ID=6401,postype='left',pos='0,0',bindtime=-1,removetime=240,sprpriority=-10,ownpal=1)
ctl(3210,'Urkelbot arrives','Explod','time=0',anim=6402,ID=6402,postype='left',pos='640-facing*70,660',facing='facing',bindtime=-1,removetime=48,sprpriority=2,ownpal=1)
ctl(3210,'Start experiment','TargetBind','time<48',pos='180,-time*2')
ctl(3210,'Robot juggle','TargetBind','time=[48,149]',pos='260+40*sin(time*.15),-130-100*abs(sin(time*.08))')
ctl(3210,'Uppercut windup','TargetBind','time=[150,179]',pos='260,-60-(time-150)*3')
for tick in [48,96,150]:
    ctl(3210,'Robot piston punch','Explod',f'time={tick}',anim=6403,ID=6403,postype='left',pos='640-facing*70,660',facing='facing',bindtime=-1,
        removetime=(48 if tick==48 else 54 if tick==96 else 90),sprpriority=3,ownpal=1)
for tick in [24,48,72,96,120,150,180]:
    ctl(3210,'Flying gears','Explod',f'time={tick}',anim=6404,ID=6404,postype='p1',pos='220,-240',velocity='-2,-1',
        removetime=24,sprpriority=5,ownpal=1)
    ctl(3210,'Science shock','Explod',f'time={tick}',anim=6405,ID=6405,postype='p1',pos='220,-170',removetime=-2,sprpriority=6,ownpal=1)
    ctl(3210,'Malfunction cue','PlaySnd',f'time={tick}',value='0,3')
    ctl(3210,'Machine shakes','EnvShake',f'time={tick}',time=10,ampl=14 if tick==180 else 5,freq=85)
ctl(3210,'Robot impact flash','EnvColor','time=180',value='255,239,135',time=6,under=0)
ctl(3210,'Resolve once','TargetLifeAdd','time=180',value=-400,kill=1)
ctl(3210,'Release','TargetState','time=180',value=8260)
ctl(3210,'Recover','ChangeState','time>=239',value=0,ctrl=1)
# These victim states select the victim's own reaction sprites, including the
# suited bank when Will is Agent J. No opponent ever inherits Urkel's costume.
for number,animation in [(8250,5000),(8260,5050)]:
    state(number,kind='A' if number==8260 else 'S',move='H')
    ctl(number,'Own character reaction','ChangeAnim','time=0',value=f'ifelse(var(30)=1 && selfanimexist({animation+10000}),{animation+10000},{animation})')
    if number==8250:
        ctl(number,'Captured protection','NotHitBy',value='SCA',time=1)
        ctl(number,'No camera pull','ScreenBound',value=0,movecamera='0,0')
        ctl(number,'Orphan safety','SelfState','time>300',value=0,ctrl=1)
    else:
        ctl(number,'Launch','VelSet','time=0',x=-6,y=-9)
        ctl(number,'Gravity','VelAdd',y=.65)
        ctl(number,'Land','SelfState',['vel y>0','pos y>=0'],value=5100)
state(9000,0);ctl(9000,'Reset life','LifeSet',value=1000);ctl(9000,'Reset meter','PowerSet',value=3000)
ctl(9000,'Reset form','VarSet',**{'var(30)':0})
ctl(9000,'Reset cooldown','VarSet',**{'var(31)':0})
ctl(9000,'Reset position','PosSet',x='ifelse(teamside=1,-60,60)',y=0)
ctl(9000,'Reset speed','VelSet',x=0,y=0);ctl(9000,'Clear effects','RemoveExplod');ctl(9000,'Ready','ChangeState',value=0,ctrl=1)
stefan.states(state,ctl,end,hit)
(OUT/'urkel.cns').write_text(cns,encoding='utf-8')
sounds=[]
for number,(frequency,duration) in enumerate([(420,.1),(125,.14),(900,.07),(650,.42)]):
    rate=22050;pcm=bytearray()
    for i in range(int(rate*duration)):
        t=i/rate;sample=int(11000*(1-t/duration)**2*math.sin(2*math.pi*(frequency*t+180*t*t)))
        pcm.extend(struct.pack('<h',sample))
    stream=io.BytesIO()
    with wave.open(stream,'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(pcm)
    sounds.append(stream.getvalue())
snd=bytearray(512);snd[:12]=b'ElecbyteSnd\0';snd[12:16]=bytes((0,0,0,1));struct.pack_into('<II',snd,16,len(sounds),512)
for i,sound in enumerate(sounds):
    offset=len(snd);nxt=offset+16+len(sound) if i<len(sounds)-1 else 0
    snd.extend(struct.pack('<IIII',nxt,len(sound),0,i)+sound)
(OUT/'urkel.snd').write_bytes(snd)
robot_framing=[]
for key in ['robot_idle','robot_punch']:
    item=meta[key];x0,y0,x1,y1=item['bounds'];ax,ay=item['axis'];scale=item['scale']
    for facing in (-1,1):
        center=640-facing*70
        left,right=sorted([center+(x0-ax)*scale*facing,center+(x1-ax)*scale*facing])
        top,bottom=660+(y0-ay)*scale,660+(y1-ay)*scale
        assert left>=40 and right<=1240 and top>=40 and bottom<=680, (key,facing,left,top,right,bottom)
        robot_framing.append({'pose':key,'facing':facing,'bounds':[left,top,right,bottom]})
report={'status':'Built; native validation pending','character':'urkel','sprites':meta,'source_png_bytes_preserved':True,
        'robot_framing_revision':2,'robot_framing':robot_framing,'robot_anchor':'Screen space; independent of stage position and camera movement',
        'sff_bytes':len(archive),'normals':{str(n):v[0] for n,v in NORMALS.items()},
        'specials':{'1000':'Cheese Please','1100':'Did I Do That?','1200':'Suspender Snap','1300':'Safety First'},
        'forms':{'0':'Steve Urkel','1':'Stefan Urquelle'},'transform':{'cost':1000,'commit_tick':24,'duration':48,'cooldown':120,'free_return':True},
        'super':{'name':'Gadget Malfunction','cost':1000,'damage':210},
        'ultimate':{'name':'Urkelbot Unleashed','cost':2000,'damage':400,'confirmed_ticks':240,'hit_confirm_only':True},
        'stefan':{'super':'Smooth Operator','super_damage':245,'ultimate':'Perfect Finish','ultimate_damage':390},
        'limitations':['Eight Steve poses, six Stefan poses and two robot drawings; shared movement/attack drawings','No portraits, authored walk cycle or voice lines','Balance and animation polish pending']}
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('URKEL_BUILT',len(archive),'sprite bytes;',len(meta),'original PNG poses preserved')
