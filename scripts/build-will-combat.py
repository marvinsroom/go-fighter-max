"""Build Will's first full combat prototype. Original PNG payloads stay unchanged."""
from pathlib import Path
from PIL import Image
import struct,json,hashlib,math,wave
import will_agent_j as agent
root=Path(__file__).resolve().parents[1];source=root/'sprite-fighter/characters/will'
engine=root/'sprite-fighter/engine/ikemen-go-v1.0.0';out=engine/'chars/will_full';out.mkdir(exist_ok=True)
sprites=[];payload=bytearray(b''.join(bytes((i,i,i,0 if i==0 else 255)) for i in range(256)));meta={}
def png_sprite(key,path,axis=None,height=None,group=0,number=None):
    raw=path.read_bytes()
    with Image.open(path) as im:
        w,h=im.size;bounds=im.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox() if im.mode=='RGBA' else (0,0,w,h)
        depth=32 if im.mode=='RGBA' else 24
    if axis is None:axis=((bounds[0]+bounds[2])//2,bounds[3])
    scale=height/(bounds[3]-bounds[1]) if height else 1
    number=len(sprites) if number is None else number
    offset=len(payload);block=struct.pack('<I',w*h*(depth//8))+raw;payload.extend(block)
    sprites.append(struct.pack('<HHHHhhHBBIIHH',group,number,w,h,*axis,0,12 if depth==32 else 11,depth,offset,len(block),0,0))
    meta[key]={'group':group,'number':number,'scale':scale,'width':w,'height':h,'axis':axis,
               'file':str(path.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest()}
png_sprite('idle',source/'art/will-stance-v1.png',(512,1520),375)
for key in ['pass','plant','lead']:png_sprite(key,source/('art/will-walk-'+key+'-v1.png'),(512,1520),375)
for key,height,ax in [('jab',375,590),('crouch',235,680),('sweep',230,350),('elbow',375,660),
                      ('palm',375,650),('airkick',320,430),('hurt',375,700),('down',145,650)]:
    path=source/'art/combat-v1'/(key+'.png')
    with Image.open(path) as image:bottom=image.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()[3]
    png_sprite(key,path,(ax,bottom),height)
for key,height,axis in [('whistle',410,510),('shrug',375,510),('taxi',245,None),('luggage',160,None)]:
    path=source/'art/finishers-v2'/(key+'.png')
    with Image.open(path) as image:
        bounds=image.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()
    png_sprite(key,path,(axis or (bounds[0]+bounds[2])//2,bounds[3]),height)
for i,key in enumerate(['street','mansion']):png_sprite(key,source/'art/combat-v1'/(key+'.png'),(0,0),group=6000,number=i)
agent.sprites(png_sprite,source)
# Small code-native impact stars, embedded as raw RGBA sprites (no source art editing).
for n,color in enumerate([(60,235,225),(255,220,55),(175,85,240)]):
    pixels=bytearray()
    for y in range(64):
        for x in range(64):
            dx=x-31.5;dy=y-31.5;r=math.hypot(dx,dy);a=math.atan2(dy,dx)
            inside=r<13+17*abs(math.cos(4*a))**5
            pixels.extend((*color,255 if inside else 0))
    offset=len(payload);payload.extend(pixels)
    sprites.append(struct.pack('<HHHHhhHBBIIHH',7000,n,64,64,32,32,0,0,32,offset,len(pixels),0,0))
# Code-native plasma capsule: bright core and translucent cyan glow.
bolt=bytearray()
for y in range(32):
    for x in range(128):
        dx=max(0,abs(x-63.5)-42);distance=math.hypot(dx,y-15.5)
        alpha=int(255*max(0,1-distance/16)**1.4)
        core=max(0,1-distance/5)
        bolt.extend((int(50+205*core),245,255,alpha))
offset=len(payload);payload.extend(bolt)
sprites.append(struct.pack('<HHHHhhHBBIIHH',7100,0,128,32,64,16,0,0,32,offset,len(bolt),0,0))
def effect_sprite(number,width,height,pixels,axis):
    offset=len(payload);payload.extend(pixels)
    sprites.append(struct.pack('<HHHHhhHBBIIHH',7200,number,width,height,*axis,0,0,32,offset,len(pixels),0,0))
agent.effect_sprites(effect_sprite)
header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2));paloffset=512+28*len(sprites);dataoffset=paloffset+16
struct.pack_into('<IIIIIIII',header,36,512,len(sprites),paloffset,1,dataoffset,len(payload),dataoffset+len(payload),0)
archive=bytes(header)+b''.join(sprites)+struct.pack('<HHHHII',1,1,256,0,0,1024)+payload
(out/'will.sff').write_bytes(archive)
# Container readback verifies original PNG bytes, not just table sizes.
for item in meta.values():
    entry=next(struct.unpack('<HHHHhhHBBIIHH',s) for s in sprites if struct.unpack_from('<HH',s)==(item['group'],item['number']))
    offset,length=entry[9:11]
    assert hashlib.sha256(archive[dataoffset+offset+4:dataoffset+offset+length]).hexdigest()==item['sha256']

air=[];action_records={}
hurt_stand=(-55,-355,65,0);hurt_crouch=(-60,-225,70,0);hurt_air=(-65,-300,75,-30)
def action(number,frames,active=None,hurt=hurt_stand,attack=None):
    action_records[number]=frames
    air.append(f'\n[Begin Action {number}]')
    for i,(key,duration,*extra) in enumerate(frames):
        if hurt:
            air.extend(['Clsn2: 1','Clsn2[0] = '+','.join(map(str,hurt))])
        if active and i in active:
            box=attack or (35,-305,200,-145)
            air.extend(['Clsn1: 1','Clsn1[0] = '+','.join(map(str,box))])
        item=meta[key];sx=item['scale'];sy=sx;angle=extra[0] if extra else 0
        air.append(f"{item['group']},{item['number']},0,0,{duration},,,{sx:.7f},{sy:.7f},{angle}")
action(0,[('idle',36),('idle',36)])
# Insert interpolation directives and a tiny breath on one shared drawing.
start=next(i for i,line in enumerate(air) if line.strip()=='[Begin Action 0]');air.insert(start+1,'Interpolate Scale')
for i in range(start+2,len(air)):
    if air[i].startswith('0,0,'):
        if any(s.startswith('0,0,') for s in air[start+2:i]):
            parts=air[i].split(',');parts[8]=f"{meta['idle']['scale']*1.004:.7f}";air[i]=','.join(parts);air.insert(i,'Interpolate Scale');break
for num,seq in [(20,['idle','pass','plant','lead']),(21,['idle','lead','plant','pass'])]:action(num,[(p,8) for p in seq])
action(10,[('crouch',-1)],hurt=hurt_crouch)
action(40,[('crouch',4)],hurt=hurt_crouch);action(41,[('pass',-1)],hurt=hurt_air);action(52,[('crouch',5)],hurt=hurt_crouch)
for num,pose in [(5,'idle'),(6,'crouch'),(120,'idle'),(121,'crouch'),(122,'pass'),(130,'idle'),(131,'crouch'),(132,'pass'),(140,'idle'),(141,'crouch'),(142,'pass'),(150,'hurt'),(151,'crouch'),(152,'hurt'),(153,'crouch'),(154,'hurt'),(155,'hurt')]:
    action(num,[(pose,8)],hurt=hurt_crouch if pose=='crouch' else hurt_stand)
normals={200:('Fresh Jab','jab',6,3,10,34,'S','MA',False),210:('Philly Straight','jab',10,4,16,58,'S','MA',False),
         220:('Punchline','palm',17,5,22,90,'S','MA',False),400:('Sneaker Tap','sweep',6,3,12,30,'C','L',False),
         410:('Floor Sweep','sweep',12,4,21,65,'C','L',True),420:('High-Top Saver','elbow',11,5,20,80,'C','MA',True),
         280:('High Five','palm',23,4,24,78,'S','H',False),600:('Air Jab','jab',5,4,12,30,'A','H',False),
         610:('Fresh Sole','airkick',8,6,14,60,'A','H',False),620:('Double Take','airkick',11,12,16,38,'A','H',True)}
for num,(_,pose,startup,active,recovery,damage,kind,guard,fall) in normals.items():
    attack=(30,-90,225,-5) if num in [400,410] else ((-10,-400,135,-180) if num==420 else (35,-305,215,-125))
    action(num,[('crouch' if kind=='C' else ('pass' if kind=='A' else 'idle'),startup),(pose,active),('crouch' if kind=='C' else ('pass' if kind=='A' else 'idle'),recovery)],active={1},hurt=hurt_crouch if kind=='C' else hurt_air if kind=='A' else hurt_stand,attack=attack)
specials={1000:('Three-Piece entry','elbow',9,4,19,48,'MA',False),1010:('Three-Piece body punch','jab',8,4,22,44,'MA',False),
          1020:('Three-Piece palm finish','palm',7,4,19,55,'MA',False),1030:('Three-Piece sweep finish','sweep',13,5,24,75,'L',True),
          1040:('Three-Piece heel finish','airkick',23,5,26,85,'H',True),1200:('Fresh Step','airkick',16,8,29,95,'MA',False),
          1300:('Windmill Remix','sweep',15,14,29,48,'MA',True),1400:('Taxi!','elbow',22,6,28,105,'MA',True)}
for num,(_,pose,startup,active,recovery,damage,guard,fall) in specials.items():
    box=(25,-240,245,-5) if num in [1030,1300] else (25,-320,230,-90)
    action(num,[('idle',startup),(pose,active),('idle',recovery)],active={1},attack=box)
action(1050,[('elbow',7),('idle',18)]) # Psyche: zero attack collision.
action(1100,[('palm',8),('idle',14)]) # Run It Back: visible vulnerable recovery.
for num in [800,810]:action(num,[('palm',4),('palm',4),('idle',22)],active={1},attack=(10,-310,105,-70))
for num in [801,811]:action(num,[('palm',8),('elbow',8),('idle',12)])
action(820,[('hurt',-1)],hurt=None);action(821,[('hurt',-1)],hurt=None)
action(3000,[('palm',12),('jab',5),('idle',30)],active={1})
action(3200,[('palm',22),('jab',5),('idle',36)],active={1})
action(3010,[('palm',12),('shrug',8),('elbow',8),('jab',8),('palm',8),('jab',8),('elbow',12),('pass',16),('airkick',20),('shrug',40)])
action(3210,[('whistle',28),('palm',28),('lead',10),('pass',10),('elbow',20),('airkick',14,-12),('airkick',34,18),('shrug',64)])
action(6400,[('taxi',-1)],hurt=None)
action(6401,[('luggage',-1)],hurt=None)
for num in [3050,3250]:action(num,[('hurt',-1)],hurt=None)
for num in [170,180,181,190,191,195]:action(num,[('down' if num==170 else 'palm',30)])
for num in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:action(num,[('hurt',-1)])
for num in [5100,5110,5140,5150,5160,5170]:action(num,[('down',6 if num in [5100,5160] else -1)],hurt=(-120,-120,160,0))
action(5120,[('down',10),('crouch',10),('idle',5)])
for num in [5200,5210,5220,5500,5510]:action(num,[('pass',8),('idle',8)])
for i,key in enumerate(['street','mansion']):
    item=meta[key];air.append(f'\n[Begin Action {6000+i}]\n6000,{i},0,0,-1,,,{1280/item["width"]:.7f},{720/item["height"]:.7f}')
for i in range(3):air.append(f'\n[Begin Action {7000+i}]\n7000,{i},0,0,6,,,1,1\n7000,{i},0,0,5,,,1.5,1.5')
agent.animations(action,air)
agent.animation_variants(air,meta)
(out/'will.air').write_text('\n'.join(air)+'\n',encoding='utf-8')
(out/'will-common.cns.zss').write_text(agent.common_states((engine/'data/common1.cns.zss').read_text(encoding='utf-8')),encoding='utf-8')
(out/'will_full.def').write_text('''[Info]
name = "Will"
displayname = "Will"
author = "Sitcom Fighter project"
mugenversion = 1.1
localcoord = 1280,720
[Files]
cmd = will.cmd
cns = will.cns
st = will.cns
stcommon = will-common.cns.zss
sprite = will.sff
anim = will.air
sound = will.snd
''',encoding='utf-8')

cmd='''[Remap]
a=a
b=b
c=c
x=x
y=y
z=z
s=s
d=d
w=w
[Defaults]
command.time=20
command.buffer.time=3
'''
definitions={'super':'D, DF, F, D, DF, F, c','ultimate':'D, DB, B, D, DB, B, c',
             'three':'D, DF, F, a','feint':'D, DB, B, a','freeze':'D, DB, B, b',
             'windmill':'D, DF, F, c','taxi':'D, DB, B, c',
             'L':'a','M':'b','H':'c','skill':'x','super_short':'y','ultimate_short':'z','throw':'d','transform':'w',
             'holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
for name,keys in definitions.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={32 if name in ["super","ultimate"] else 20 if name in ["three","feint","freeze","windmill","taxi"] else 1}\n'
cmd+='\n[Statedef -1]\n'
def command_state(label,value,conditions):
    global cmd
    if value in list(normals)+list(specials)+[1050,1100,3000,3200]:conditions=['var(30)=0']+conditions
    cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'
    cmd+='\n'.join('triggerall='+c for c in conditions[:-1])+'\ntrigger1='+conditions[-1]+f'\nvalue={value}\nctrl=0\n'
agent.commands(command_state)
base='roundstate=2';ground='statetype!=A';ready='ctrl || ((stateno=[200,420]) && movehit) || ((stateno=1000 || stateno=1010) && movehit)'
for name,st,cost,short in [('ultimate',3200,2000,'ultimate_short'),('super',3000,1000,'super_short')]:
    command_state(name,st,[base,ground,ready,f'power>={cost}',f'command="{name}" || command="{short}"'])
command_state('Run It Back',1100,[base,'stateno=1010','time=[12,28]','power>=1000','command="skill"'])
special_ready='ctrl || ((stateno=[200,420]) && movehit)'
for name,st in [('three',1000),('feint',1050),('freeze',1200),('windmill',1300),('taxi',1400)]:command_state(name,st,[base,ground,special_ready,f'command="{name}"'])
command_state('Three Piece second hit',1010,[base,'stateno=1000','time=[13,27]','command="L" || command="M" || command="H"'])
for button,st in [('L',1020),('M',1030),('H',1040)]:command_state('Three Piece ending '+button,st,[base,'stateno=1010','time=[12,29]',f'command="{button}"'])
for st,back in [(810,True),(800,False)]:command_state('Throw',st,[base,ground,'ctrl','p2bodydist x < 75','p2statetype!=A','p2movetype!=H',f'command="throw" && command{"=" if back else "!="}"holdback"'])
for button,st in [('H',620),('M',610),('L',600)]:command_state('Air '+button,st,[base,'statetype=A','ctrl',f'command="{button}"'])
for button,st in [('H',420),('M',410),('L',400)]:command_state('Crouch '+button,st,[base,ground,'ctrl','command="holddown"',f'command="{button}"'])
command_state('High Five',280,[base,ground,'ctrl','command="holdfwd"','command="M"'])
for button,st,cancel in [('H',220,'stateno=200 || stateno=210'),('M',210,'stateno=200'),('L',200,'0')]:
    command_state('Standing '+button,st,[base,ground,f'ctrl || (({cancel}) && movehit)',f'command="{button}"'])
command_state('Crouch',10,[base,ground,'ctrl','stateno!=10','command="holddown"'])
command_state('Jump',40,[base,ground,'ctrl','command="holdup"'])
command_state('Walk forward',20,[base,'stateno=0','ctrl','command="holdfwd"'])
command_state('Walk back',21,[base,'stateno=0','ctrl','command="holdback"'])
# A modest opponent for optional CPU testing. Full AI strategy is not claimed.
command_state('CPU basic punish',210,[base,'ailevel>0','ctrl','p2bodydist x<150','random<35'])
command_state('CPU approach',20,[base,'ailevel>0','ctrl','stateno=0','p2bodydist x>160'])
(out/'will.cmd').write_text(cmd,encoding='utf-8')

states='''[Data]
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
ground.back=48
ground.front=58
air.back=48
air.front=48
height=360
attack.dist=230
proj.attack.dist=0
head.pos=5,-340
mid.pos=0,-190
shadowoffset=0
draw.offset=0,0
[Velocity]
walk.fwd=3.2
walk.back=-2.6
jump.neu=0,-13
jump.fwd=4,-13
jump.back=-3.5,-13
[Movement]
yaccel=.65
stand.friction=.85
crouch.friction=.82
airjump.num=0
stand.friction.threshold=.1
'''
def state(num,anim=None,kind='S',move='I',physics='N',ctrl=0,**kwargs):
    global states
    states+=f'\n[Statedef {num}]\ntype={kind}\nmovetype={move}\nphysics={physics}\nctrl={ctrl}\n'
    if anim is not None:states+=f'anim={agent.animation_value(anim)}\n'
    for k,v in kwargs.items():states+=k+'='+str(v)+'\n'
def ctl(num,label,typ,triggers='1',**params):
    global states
    if typ in ('ChangeAnim','ChangeAnim2') and num in (820,821,1420,3050,3250,4550) and 'value' in params:
        typ='ChangeAnim'
        params['value']=agent.victim_animation_value(num)
    elif typ in ('ChangeAnim','ChangeAnim2') and 'value' in params:
        params['value']=agent.animation_value(params['value'])
    states+=f'\n[State {num}, {label}]\ntype={typ}\n'
    if num in (3010,3210) and typ=='Explod':
        states+='triggerall=var(30)=0\n'
    for trigger in triggers if isinstance(triggers,list) else [triggers]:states+='trigger1='+trigger+'\n'
    states+=''.join(k.replace('__','.')+'='+str(v)+'\n' for k,v in params.items())
def finish(num,air=False,crouch=False):
    ctl(num,'End','ChangeState','animtime=0',value=50 if air else 10 if crouch else 0,ctrl=1)
def hit(num,time,damage,kind='S',guard='MA',fall=False,attr='NA',**extra):
    params=dict(attr=f'{kind},{attr}',damage=f'{damage},{max(0,int(damage*.04))}',guardflag=guard,hitflag='MAF',priority='4,Hit',
      pausetime='6,8',sparkno=2,sparkxy='-12,-200',hitsound='S0,1',guardsound='S0,2',
      animtype='Hard' if fall else 'Medium',ground__type='Low' if fall else 'High',ground__slidetime=12,
      ground__hittime=24 if attr=='SA' else 19,ground__velocity='-4,-5' if fall else '-2.5',
      air__velocity='-4,-5',fall=1 if fall else 0,getpower='75,25',givepower='35,15',id=num)
    params.update(extra);ctl(num,'Contact','HitDef',f'time={time}',**params)
    ctl(num,'Swing','PlaySnd',f'time={max(0,time-1)}',value='0,0')
state(5900);ctl(5900,'Fresh Prince at round start','VarSet',**{'var(30)':0});ctl(5900,'Enter','ChangeState',value=0,ctrl=1)
state(-2)
agent.global_states(ctl,meta,action_records)
ctl(-2,'Turn','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'Reset wall bounce budget','VarSet','enemynear,movetype!=H',**{'var(20)':0})
ctl(-2,'Landing remains real','AssertSpecial','1',flag='noautoturn')
state(0,0,ctrl=1,velset='0,0');ctl(0,'Ground','PosSet',y=0)
state(10,10,kind='C',ctrl=1,velset='0,0');ctl(10,'Stand','ChangeState','command!="holddown"',value=0,ctrl=1)
for num,speed,held in [(20,3.2,'holdfwd'),(21,-2.6,'holdback')]:
    state(num,num,ctrl=1);ctl(num,'Step','VelSet',x=speed,y=0)
    ctl(num,'Stop','ChangeState',f'(ailevel=0 && command!="{held}") || (ailevel>0 && p2bodydist x<140)',value=0,ctrl=1)
state(40,40);ctl(40,'Choose jump','VarSet','time=0',**{'var(1)':'ifelse(command="holdfwd",4,ifelse(command="holdback",-3.5,0))'})
ctl(40,'Lift','ChangeState','time>=3',value=50,ctrl=1)
state(50,41,kind='A',ctrl=1)
ctl(50,'Launch','VelSet',['time=0','prevstateno=40'],x='var(1)',y=-13)
ctl(50,'Gravity','VelAdd',y=.65);ctl(50,'Land','ChangeState',['vel y>0','pos y>=0'],value=52,ctrl=0)
state(52,52,velset='0,0');ctl(52,'Ground','PosSet',y=0);ctl(52,'Recover','ChangeState','time>=4',value=0,ctrl=1)
for num,(_,pose,startup,active,recovery,damage,kind,guard,fall) in normals.items():
    state(num,num,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}))
    hit(num,startup,damage,kind,guard,fall)
    if num==620:hit(num,startup+7,damage,kind,guard,True)
    if kind=='A':
        ctl(num,'Gravity','VelAdd',y=.65);ctl(num,'Land','ChangeState',['vel y>0','pos y>=0'],value=52,ctrl=0)
    finish(num,kind=='A',kind=='C')
for num,(_,pose,startup,active,recovery,damage,guard,fall) in specials.items():
    state(num,num,move='A',velset='0,0',poweradd=25)
    hit(num,startup,damage,guard=guard,fall=fall,attr='SA')
    if num==1300:hit(num,startup+8,damage,guard=guard,fall=True,attr='SA')
    if num in [1000,1010,1400]:
        ctl(num,'Committed entry','VelSet',f'time<{startup+active}',x=5.5 if num==1400 else 2.2)
        ctl(num,'Stop entry','VelSet',f'time>={startup+active}',x=0)
    if num==1400:
        ctl(num,'One clean corner bounce','TargetState',['movehit','numtarget>0','target,backedgedist<45','var(20)=0'],value=1420)
        ctl(num,'Spend corner bounce','VarSet',['movehit','numtarget>0','target,backedgedist<45'],**{'var(20)':1})
    finish(num)
state(1050,1050,velset='0,0');finish(1050)
state(1100,1100,velset='0,0',poweradd=-1000);finish(1100)
# A corner bounce returns the victim toward center exactly once in the combo.
state(1420,5050,kind='A',move='H')
ctl(1420,'Own hurt art','ChangeAnim2','time=0',value=5050)
ctl(1420,'Bounce','VelSet','time=0',x=7,y=-9);ctl(1420,'Gravity','VelAdd',y=.65)
ctl(1420,'Return to own floor state','SelfState',['vel y>0','pos y>=0'],value=5100)
for num,success in [(800,801),(810,811)]:
    state(num,num,move='A',velset='0,0')
    hit(num,4,0,attr='NT',guard='',hitflag='M-',priority='1,Miss',sparkno=-1,
        p1stateno=success,p2stateno=820,p1facing=1,p2facing=1,guard__dist=0,fall=1,numhits=0)
    finish(num)
for num in [801,811]:
    state(num,num,move='A',velset='0,0')
    if num==811:ctl(num,'After You side switch','Turn','time=0')
    ctl(num,'Keep captured','TargetBind','time<14',pos='90,-20')
    ctl(num,'Throw damage once','TargetLifeAdd','time=14',value=-110,kill=1)
    ctl(num,'Release','TargetState','time=14',value=821)
    finish(num)
state(820,move='H');ctl(820,'Captured pose','ChangeAnim2','time=0',value=820)
ctl(820,'Escape orphan capture','SelfState','time>160',value=0,ctrl=1)
state(821,kind='A',move='H');ctl(821,'Falling pose','ChangeAnim2','time=0',value=821)
ctl(821,'Throw velocity','VelSet','time=0',x=-7,y=-8);ctl(821,'Gravity','VelAdd',y=.65)
ctl(821,'Hit floor','SelfState',['vel y>0','pos y>=0'],value=5100)
# Starters spend meter on entry. HitDef redirects only on unguarded hit.
for num,nextstate,victim,cost,startup in [(3000,3010,3050,1000,12),(3200,3210,3250,2000,22)]:
    state(num,num,move='A',velset='0,0',poweradd=-cost)
    ctl(num,'Super flash','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0,darken=1)
    ctl(num,'Original super cue','PlaySnd','time=0',value='0,3')
    hit(num,startup,20 if num==3000 else 0,attr='HA',p1stateno=nextstate,p2stateno=victim,
        getpower='0,0',givepower='0,0',ground__hittime=180,fall=0)
    finish(num)
for num,victim,total,final in [(3010,3050,140,100),(3210,3250,208,144)]:
    state(num,num,move='A',velset='0,0')
    ctl(num,'Confirmed sequence protection','NotHitBy',value='SCA',time=1)
    ctl(num,'Keep cinematic in view','ScreenBound',value=0,movecamera='0,0')
    if num==3010:
        ctl(num,'Handshake and shoulder pop','TargetBind','time<56',pos='120+18*sin(time*.45),-abs(sin(time*.18))*24')
        ctl(num,'Launch into the air','TargetBind','time=[56,83]',pos='160,-(time-56)*5')
        ctl(num,'Meet the falling target','TargetBind',f'time=[84,{final-1}]',pos='160,-140+(time-84)*6')
        ctl(num,'Dance step forward','PosAdd','time=[16,47]',x=2.4)
        ctl(num,'Jump after the launch','VelSet','time=56',y=-7)
        ctl(num,'Air chase gravity','VelAdd','time=[56,79]',y=.65)
        ctl(num,'Plant feet for kick','PosSet','time>=80',y=0)
        ctl(num,'Stop jump','VelSet','time>=80',y=0)
        ctl(num,'Chase afterimages','AfterImage','time=20',time=80,length=8,timegap=2,framegap=2,trans='add')
        for t in [20,28,36,44,52]:
            ctl(num,'Dance string damage','TargetLifeAdd',f'time={t}',value=-28,kill=0)
            ctl(num,'Dance combo count','HitAdd',f'time={t}',value=1)
        ctl(num,'Final kick damage','TargetLifeAdd',f'time={final}',value=-125,kill=1)
        ctl(num,'Final kick count','HitAdd',f'time={final}',value=1)
    else:
        ctl(num,'Frame Will and chase the cab','PosSet',x='camerapos x+facing*(-200+ifelse(time=[56,95],(time-56)*3,0))',y=0)
        ctl(num,'Whistle call','PlaySnd','time=4',value='0,4')
        ctl(num,'Cab horn','PlaySnd','time=38',value='0,5')
        ctl(num,'Cab approaches','Explod','time=20',anim=6400,ID=6400,postype='left',
            pos='ifelse(facing=1,-450,1730),630',velocity='22*facing,0',facing='facing',bindtime=0,
            removetime=100,sprpriority=5,ownpal=1)
        ctl(num,'Before the cab arrives','TargetBind','time<44',pos='130,0')
        ctl(num,'Cab scoops opponent upward','TargetBind','time=[44,75]',pos='130+(time-44)*5,-abs(sin((time-44)*pi/32))*110')
        ctl(num,'Chase and catch','TargetBind','time=[76,109]',pos='290-(time-76)*4,-80')
        ctl(num,'Wind up the finishing kick','TargetBind',f'time=[110,{final-1}]',pos='155,-80+25*sin((time-110)*pi/34)')
        ctl(num,'Luggage landing spot','Explod','time=96',anim=6401,ID=6401,postype='p1',pos='420,0',
            bindtime=-1,removetime=112,sprpriority=2,ownpal=1)
        ctl(num,'Dash trails','AfterImage','time=56',time=88,length=10,timegap=2,framegap=2,trans='add')
        ctl(num,'Ultimate damage resolves once','TargetLifeAdd',f'time={final}',value=-420,kill=1)
        for t,bg,duration in [(0,6000,96),(96,6001,112)]:
            ctl(num,'Cinematic location','Explod',f'time={t}',anim=bg,ID=bg,postype='left',pos='0,0',bindtime=-1,
                removetime=duration,sprpriority=-10,ownpal=1,supermovetime=999,pausemovetime=999)
    for t in ([20,28,36,44,52,final] if num==3010 else [44,76,96,final]):
        ctl(num,'Impact accent','Explod',f'time={t}',anim=7000+(t//12)%3,postype='p1',pos='120,-210',
            removetime=-2,sprpriority=6,ownpal=1,scale='1.8,1.8')
        ctl(num,'Impact cue','PlaySnd',f'time={t}',value='0,1')
        ctl(num,'Impact shake','EnvShake',f'time={t}',time=5 if t!=final else 14,ampl=3 if t!=final else 10,freq=90)
    ctl(num,'Final impact flash','PalFX',f'time={final}',time=7,add='130,100,25',mul='256,256,256')
    ctl(num,'Release opponent','TargetState',f'time={final}',value=821)
    ctl(num,'End confirmed sequence','ChangeState',f'time>={total-1}',value=0,ctrl=1)
for num in [3050,3250]:
    state(num,move='H');ctl(num,'Captured reaction','ChangeAnim2','time=0',value=num)
    ctl(num,'Stay vulnerable only to sequence','NotHitBy',value='SCA',time=1)
    ctl(num,'Keep cinematic camera still','ScreenBound',value=0,movecamera='0,0')
    ctl(num,'Comic tumble','AngleDraw','time=[44,143]',value='12*sin(time*.3)')
    ctl(num,'Escape interrupted sequence','SelfState','time>260',value=0,ctrl=1)
for num in [180,181,190,191,195]:
    state(num,num);ctl(num,'Pose then recover','ChangeState','time>=25',value=0,ctrl=1)
# Test setup state has no input mapping and is not used by the playable launchers.
state(9000,0);ctl(9000,'Test life','LifeSet',value=1000);ctl(9000,'Test meter','PowerSet',value=3000)
for var in [30,31,32]:ctl(9000,'Test reset form','VarSet',**{f'var({var})':0})
ctl(9000,'Test location','PosSet',x='ifelse(teamside=1,-60,60)',y=0);ctl(9000,'Test stop','VelSet',x=0,y=0)
ctl(9000,'Clear previous effects','RemoveExplod')
ctl(9000,'Test start','ChangeState',value=0,ctrl=1)
agent.states(state,ctl,finish,hit)
(out/'will.cns').write_text(states,encoding='utf-8')
# Original synthesized cues, no music or sampled celebrity dialogue.
sounds=[]
for number,(frequency,duration) in enumerate([(550,.10),(140,.13),(850,.07),(330,.40),(1800,.35),(410,.30)]):
    rate=22050;pcm=bytearray()
    for i in range(int(rate*duration)):
        t=i/rate;envelope=(1-t/duration)**2
        sample=int(11000*envelope*(math.sin(2*math.pi*frequency*t)+.25*math.sin(2*math.pi*frequency*2.3*t)))
        pcm.extend(struct.pack('<h',max(-32768,min(32767,sample))))
    import io
    stream=io.BytesIO()
    with wave.open(stream,'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(pcm)
    sounds.append((0,number,stream.getvalue()))
sndheader=bytearray(512);sndheader[:12]=b'ElecbyteSnd\0';sndheader[12:16]=bytes((0,0,0,1));struct.pack_into('<II',sndheader,16,len(sounds),512)
sounddata=bytearray();position=512
for i,(group,number,wav) in enumerate(sounds):
    nxt=position+16+len(wav) if i<len(sounds)-1 else 0
    sounddata.extend(struct.pack('<IIII',nxt,len(wav),group,number)+wav);position+=16+len(wav)
(out/'will.snd').write_bytes(sndheader+sounddata)
report={'status':'Built; runtime checks pending','character':'will_full','source_design':'concepts/will-moveset.md',
        'forms':{'0':'Fresh Prince','1':'Agent J'},'transform_cost':1000,'transform_commit_tick':24,
        'transform_duration_ticks':48,'transform_cooldown_ticks':120,
        'agent_source':'scripts/will_agent_j.py','agent_controls':'AGENT_J_CONTROLS.md',
        'agent_outfit_revision':3,'agent_outfit_bank_offset':10000,
        'agent_ultimate_revision':2,'agent_ultimate_duration_ticks':240,
        'agent_ultimate_beats':['Neural capture','Tractor beam lift','Orbital deatomizer','Ground slam','Memory wipe'],
        'sprites':meta,'normals':{n:v[0] for n,v in normals.items()},'specials':{n:v[0] for n,v in specials.items()},
        'super_cost':1000,'ultimate_cost':2000,'meter_reset_cost':1000,'meter_max':3000,
        'super_cinematic_state':3010,'ultimate_cinematic_state':3210,'cinematic_on_hit_only':True,
        'sff_png_readback':'Passed byte comparison','audio':'Original synthesized cues',
        'limitations':['First-pass key-pose animation; drawings reused across some moves',
                       'Agent J uses seven poses, a shared walk drawing and shared throw mechanics',
                       'Backward walk is reversed forward art','No HUD portraits yet',
                       'Sprite-based cinematic with moving cab, luggage and shared combat key poses; no 3D camera',
                       'Balance, competitive frame data and polished animation pending']}
(source/'combat-build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('WILL_COMBAT_BUILT',len(archive),'sprite bytes',len(states),'state bytes',flush=True)
