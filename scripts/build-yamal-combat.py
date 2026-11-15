"""Build the independent Lamine Yamal football fighter and cinematic finishers."""
from pathlib import Path
import json, math
from fighter_assets import FighterAssets

ROOT=Path(__file__).resolve().parents[1]
assets=FighterAssets(ROOT,'yamal'); SOURCE=assets.source; OUT=assets.output
POSES={'idle':365,'walk_a':365,'walk_b':366,'kick':338,'crouch':217,
       'volley':290,'hurt':343,'down':114,'jump':292}
for i,(key,height) in enumerate(POSES.items()):
    assets.png(key,SOURCE/'art/v1'/f'{key}.png',height,i)
# The sheet was drawn at one human scale. Preserve that common pixel scale
# for every pose instead of enlarging lower or airborne silhouettes to fit a
# target rectangle. This also avoids alpha-edge noise changing proportions.
sheet_scale=assets.meta['idle']['scale']
for m in assets.meta.values():m['scale']=sheet_scale
for i,key in enumerate(['idle']*4+['kick','crouch','volley','kick','kick','volley','hurt','down','idle','idle']):
    assets.alias(0,i,key)

# Code-native ball, pitch, goal net, comet and impact sprites. Character artwork
# remains losslessly embedded; effect geometry belongs to the engine.
def ball(x,y):
    dx,dy=x-47.5,y-47.5; r=math.hypot(dx,dy)
    if r>46:return (0,0,0,0)
    edge=r>42; angle=math.atan2(dy,dx)
    panel=r<14 or (20<r<37 and math.cos(angle*5)>.55)
    return (15,25,50,255) if edge or panel else (238,242,250,255)
assets.raw(0,96,96,ball)
def pitch(x,y):
    line=abs(x-640)<2 or abs(y-570)<2 or abs(math.hypot((x-640), (y-570)*2)-180)<3
    crowd=y<340 and (x//14+y//10)%4==0
    return (95,190,210,255) if line else (16,46,65,255) if crowd else (8,20,39,255) if y<340 else (13,65+((x//90)%2)*10,67,255)
assets.raw(1,1280,720,pitch,(0,0))
def net(x,y):
    border=x<9 or x>310 or y<9
    mesh=x%24<2 or y%24<2
    return (210,240,255,245) if border else (95,180,230,150) if mesh else (0,0,0,0)
assets.raw(2,320,280,net,(160,280))
def comet(x,y):
    dx=(x-270)/45;dy=(y-64)/45;r=math.hypot(dx,dy)
    if r<1:return (235,250,255,255) if r<.7 else (70,190,255,255)
    width=max(0,(x+20)/290)*42
    if x<270 and abs(y-64)<width:
        a=int(230*max(0,1-abs(y-64)/max(1,width))*(x+20)/290)
        return (240,45,90,a) if y>64 else (40,130,255,a)
    return (0,0,0,0)
assets.raw(3,320,128,comet,(270,64))
assets.raw(4,192,192,lambda x,y:(155,220,255,int(245*max(0,1-abs(math.hypot(x-95.5,y-95.5)-65)/10))))
assets.raw(5,256,256,lambda x,y:(255,220,160,230) if (abs(x-128)<5 or abs(y-128)<5 or abs(abs(x-128)-abs(y-128))<4) and math.hypot(x-128,y-128)<120 else (0,0,0,0))
glyphs=['01110/10000/10111/10001/10001/10001/01110','01110/10001/10001/10001/10001/10001/01110',
        '01110/10001/10001/11111/10001/10001/10001','10000/10000/10000/10000/10000/10000/11111',
        '00100/00100/00100/00100/00100/00000/00100']
def goal_text(x,y):
    gx=x//14;gy=y//14;letter=gx//6;col=gx%6
    on=letter<5 and col<5 and gy<7 and glyphs[letter].split('/')[gy][col]=='1'
    return (245,230,145,255) if on else (0,0,0,0)
assets.raw(6,420,98,goal_text)
sff_bytes=assets.write_sff('yamal.sff')
action=assets.action;air=assets.air
for n,key in [(0,'idle'),(5,'idle'),(6,'crouch'),(10,'crouch'),(11,'crouch'),(12,'idle'),(47,'crouch')]:action(n,[(key,-1)])
for n,keys in [(20,['walk_a','idle','walk_b','idle']),(21,['walk_b','idle','walk_a','idle'])]:action(n,[(k,7) for k in keys])
action(22,[('walk_a',3),('idle',3)])
for n in [40,41,42,43,52]:action(n,[('crouch',3)] if n==40 else [('jump',-1)] if n!=52 else [('crouch',4),('idle',3)])
for n in list(range(120,123))+list(range(130,133))+list(range(140,143))+list(range(150,156)):
    action(n,[('crouch' if n in (121,131,141,152,153) else 'hurt' if n>=150 else 'idle',8)])
for n in [170,175,180,181,190,191,195]:action(n,[('down' if n in (170,175) else 'idle',30)])
for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:action(n,[('hurt',-1)])
for n in [5100,5110,5140,5150,5160,5170]:action(n,[('down',6 if n in (5100,5160) else -1)],hurt=False)
action(5120,[('down',10),('crouch',10),('idle',5)])
for n in [5200,5210,5220,5300,5500,5510]:action(n,[('crouch',8),('idle',8)])
for n in [820,821,8250,8260,3050,3250,4550]:action(n,[('hurt',-1)],hurt=False)
NORMALS={200:('Inside Tap','kick',6,3,12,30,'S','MA',False),
 210:('Turning Kick','kick',11,4,17,52,'S','MA',False),220:('Left-Foot Drive','kick',18,5,24,82,'S','MA',True),
 400:('Low Toe Poke','crouch',7,3,13,26,'C','L',False),410:('Slide Tackle','crouch',15,4,25,58,'C','L',True),
 420:('Rising Flick','volley',12,5,24,78,'C','MA',True),600:('Air Tap','volley',7,5,15,34,'A','H',False),
 610:('Air Volley','volley',10,6,19,58,'A','H',True),620:('Bicycle Volley','volley',15,7,22,72,'A','H',True)}
for n,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    action(n,[('jump' if kind=='A' else 'crouch' if kind=='C' else 'idle',start),(pose,active),('jump' if kind=='A' else 'crouch' if kind=='C' else 'idle',recovery)],
           active=(1,),kind=kind,attack=(0,-100,220,-5) if guard=='L' else (0,-320,230,-50))
for n in [800,810]:action(n,[('idle',5),('kick',4),('idle',25)],active=(1,),attack=(0,-300,105,-30))
for n in [801,811]:action(n,[('idle',10),('kick',10),('idle',15)])
for n in [1000,1010,1020,1100,1110]:action(n,[('idle',14 if n<1100 else 9),('kick',6),('idle',24)],active=(1,) if n>=1100 else (),attack=(0,-320,230,-50))
action(1120,[('walk_b',10),('kick',5),('idle',18)],active=(1,),attack=(0,-320,230,-50))
action(1130,[('crouch',12),('crouch',8),('idle',24)])
action(1200,[('crouch',10),('volley',8),('idle',25)],active=(1,),attack=(0,-420,170,-50))
for n in [1300,1400]:action(n,[('walk_a',5),('walk_b',5),('walk_a',5),('idle',8)])
for n,start in [(3000,12),(3200,24)]:action(n,[('idle',start),('kick',6),('idle',28)],active=(1,),attack=(-900,-450,1100,0) if n==3200 else (0,-355,470,-30))
for n,total in [(3010,240),(3210,420)]:action(n,[(k,5) for _ in range((total-40)//20) for k in ['walk_a','walk_b','volley','kick']]+[('kick',20),('idle',20)])
for n,sprite,scale in [(6400,0,.64),(6401,1,1),(6402,2,1),(6403,3,1),(6404,4,1),(6405,5,1),(6406,6,1)]:
    air.extend([f'\n[Begin Action {n}]'])
    if n==6400:air.extend(['Clsn1: 1','Clsn1[0]=-28,-28,28,28'])
    air.append(f'7000,{sprite},0,0,-1,,,{scale},{scale}')
assets.write_air('yamal.air')
(OUT/'yamal.def').write_text('''[Info]
name="Lamine Yamal"
displayname="Lamine Yamal"
author="Game1 project"
mugenversion=1.1
localcoord=1280,720
[Files]
cmd=yamal.cmd
cns=yamal.cns
st=yamal.cns
stcommon=common1.cns.zss
sprite=yamal.sff
anim=yamal.air
sound=yamal.snd
''',encoding='utf-8')
commands={'L':'a','M':'b','H':'c','skill':'x','super_short':'y','ultimate_short':'z','throw':'d',
 'curler':'D, DF, F, a','curler_medium':'D, DF, F, b','curler_heavy':'D, DF, F, c',
 'rainbow':'D, DB, B, a','retreat':'D, DB, B, c',
 'holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={20 if len(keys)>2 and not keys.startswith("/") else 1}\n'
cmd+='\n[Statedef -1]\n'
def command(label,target,conditions):
    global cmd
    cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions[:-1])+f'trigger1={conditions[-1]}\nvalue={target}\nctrl=0\n'
g=['roundstate=2','statetype!=A','ctrl']
for name,target,cost in [('ultimate_short',3200,2000),('super_short',3000,1000)]:command(name,target,g+[f'power>={cost}',f'command="{name}"'])
for name,target in [('curler',1000),('curler_medium',1010),('curler_heavy',1020),('rainbow',1200),('retreat',1400)]:
    command(name,target,g+(['numproj=0'] if target<1100 else [])+[f'command="{name}"'])
for target,route in [(1130,'command="holddown"'),(1120,'command="holdback"'),(1110,'command="holdfwd"'),(1100,'1')]:
    command('Dribble route',target,g+(['numproj=0'] if target==1130 else [])+[route,'command="skill"'])
for name,target in [('H',1200),('M',1110),('L',1000)]:
    command('Close Control branch',target,['roundstate=2','stateno=1100','time=[8,22]']+(['numproj=0'] if target==1000 else [])+[f'command="{name}"'])
for target,back in [(810,True),(800,False)]:command('Throw',target,g+['p2bodydist x<75','p2statetype!=A','p2movetype!=H',f'command="throw" && command{"=" if back else "!="}"holdback"'])
for name,target in [('H',620),('M',610),('L',600)]:command('Air '+name,target,['roundstate=2','statetype=A','ctrl',f'command="{name}"'])
for name,target in [('H',420),('M',410),('L',400)]:command('Low '+name,target,g+['command="holddown"',f'command="{name}"'])
for name,target in [('H',220),('M',210),('L',200)]:command(name,target,g+[f'command="{name}"'])
for label,n,conditions in [('Crouch',10,['stateno!=10','command="holddown"']),('Jump',40,['command="holdup"']),('Forward',20,['stateno=0','command="holdfwd"']),('Back',21,['stateno=0','command="holdback"'])]:command(label,n,g+conditions)
command('CPU attack',210,g+['ailevel>0','p2bodydist x<150','random<35'])
command('CPU curler',1000,g+['ailevel>0','p2bodydist x>180','numproj=0','random<25'])
command('CPU approach',20,g+['ailevel>0','stateno=0','p2bodydist x>160'])
(OUT/'yamal.cmd').write_text(cmd,encoding='utf-8')
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
attack.dist=230
proj.attack.dist=280
proj.doscale=1
head.pos=0,-310
mid.pos=0,-170
shadowoffset=0
draw.offset=0,0
[Velocity]
walk.fwd=4.6
walk.back=-3.4
jump.neu=0,-12.5
jump.fwd=4,-12.5
jump.back=-3.4,-12.5
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
    if anim is not None:cns+=f'anim={anim}\n'
    cns+=''.join(f'{k}={v}\n' for k,v in params.items())
def ctl(number,label,kind,triggers='1',**params):
    global cns
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
ctl(-2,'Face opponent','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'No automatic turn','AssertSpecial',flag='noautoturn')
ctl(-2,'Authored movement','AssertSpecial',flag='nowalk',flag2='nobrake')
ctl(-2,'Own proportions in incoming captures','ChangeAnim',
 ['movetype=H','time=1','stateno=820 || stateno=821 || stateno=1420 || stateno=3050 || stateno=3250 || stateno=4550'],value='ifelse(stateno=821 || stateno=1420,5050,5000)')
ctl(-2,'Finish guard recovery','ChangeState',['stateno=140','animtime=0'],value='ifelse(statetype=C,10,0)',ctrl=1)
ctl(-2,'Ball at feet','Explod',['numexplod(6450)=0','numproj=0','stateno<500','movetype!=H'],anim=6400,ID=6450,pos='85,-31',bindtime=-1,removetime=-1,sprpriority=2,ownpal=1)
ctl(-2,'Hide ball during shots or reactions','RemoveExplod','numproj>0 || stateno>=500 || movetype=H',ID=6450)
ctl(-2,'Finisher foreground','SprPriority',value='ifelse(stateno=3010 || stateno=3210,4,0)')
for effect in [6401,6402,6403,6404,6405,6406]:ctl(-2,'Cinematic cleanup','RemoveExplod','stateno!=3210 && stateno!=3010',ID=effect)
state(0,0,velset='0,0');ctl(0,'Control','CtrlSet',value=1);ctl(0,'Ground','PosSet',y=0)
state(10,10,kind='C',velset='0,0');ctl(10,'Control','CtrlSet',value=1);ctl(10,'Stand','ChangeState','command!="holddown"',value=0,ctrl=1)
for number,speed,held in [(20,4.6,'holdfwd'),(21,-3.4,'holdback')]:
    state(number,number);ctl(number,'Control','CtrlSet',value=1)
    ctl(number,'Walk','VelSet',x=f'{speed}*(.35+.65*min(1,time/8.0))',y=0)
    ctl(number,'Stop','ChangeState',f'(ailevel=0 && command!="{held}") || (ailevel>0 && p2bodydist x<140)',value=22,ctrl=1)
state(22,22);ctl(22,'Settle','VelMul',x=.6);ctl(22,'Ground','PosSet',y=0);end(22)
state(40,40);ctl(40,'Direction','VarSet','time=0',**{'var(1)':'ifelse(command="holdfwd",4,ifelse(command="holdback",-3.4,0))'});ctl(40,'Take off','ChangeState','time>=3',value=50,ctrl=1)
state(50,41,kind='A');ctl(50,'Control','CtrlSet',value=1)
ctl(50,'Launch','VelSet',['time=0','prevstateno=40'],x='var(1)',y=-12.5)
ctl(50,'Apex','ChangeAnim',['vel y=[-3,3]','anim!=42'],value=42)
ctl(50,'Descend','ChangeAnim',['vel y>3','anim!=43'],value=43)
ctl(50,'Gravity','VelAdd',y=.65);ctl(50,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
state(52,52,velset='0,0');ctl(52,'Ground','PosSet',y=0);ctl(52,'Recover','ChangeState','time>=5',value=0,ctrl=1)
for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    state(number,number,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}));hit(number,start,damage,kind,guard,fall)
    if kind=='A':ctl(number,'Gravity','VelAdd',y=.65);ctl(number,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
    end(number,kind=='A',kind=='C')
for n,speed,damage in [(1000,9,48),(1010,12,60),(1020,15,72),(1130,10,65)]:
    state(n,n,move='A',velset='0,0');start=12 if n==1130 else 14
    ctl(n,'Football shot','Projectile',f'time={start}',projid=n,projanim=6400,projhitanim=-1,projremanim=-1,projremove=1,projremovetime=110,
      velocity=f'{speed},0',offset='105,-32' if n==1130 else '105,-170',attr='S,SP',damage=f'{damage},2',guardflag='L' if n==1130 else 'MA',
      hitflag='MAF',pausetime='0,8',ground__type='Low' if n==1130 else 'High',ground__hittime=22,
      ground__velocity='-4,-5' if n==1130 else '-3',air__velocity='-4,-5',fall=int(n==1130),getpower='40,10',givepower='20,10',hitsound='S0,1')
    ctl(n,'Kick cue','PlaySnd',f'time={start}',value='0,0');end(n)
state(1100,1100,move='A',velset='0,0');hit(1100,9,45,attr='S,SA');end(1100)
ctl(1100,'Close control ball','Explod','time=0',anim=6400,ID=6460,pos='85,-31',bindtime=-1,removetime=30,sprpriority=2,ownpal=1)
for n,speed,damage,start in [(1110,6,85,9),(1120,-3,70,10),(1200,0,90,10)]:
    state(n,n,move='A',velset='0,0');hit(n,start,damage,guard='MA',fall=True,attr='S,SA')
    ctl(n,'Footwork','VelSet',f'time<{start}',x=speed)
    ctl(n,'Stop','VelSet',f'time>={start}',x=0);end(n)
    if n==1200:ctl(n,'Rainbow arc','Explod','time=10',anim=6400,ID=6461,pos='90,-130',velocity='2,-12',accel='0,.4',removetime=35,sprpriority=3,ownpal=1)
state(1400,1400,velset='0,0');ctl(1400,'Retreat','VelSet','time<15',x=-6);ctl(1400,'Stop','VelSet','time>=15',x=0);end(1400)
for number,nextstate in [(800,801),(810,811)]:
    state(number,number,move='A',velset='0,0')
    ctl(number,'Shoulder challenge','HitDef','time=5',attr='S,NT',hitflag='M-',priority='1,Miss',sparkno=-1,guard__dist=0,
      pausetime='0,0',p1stateno=nextstate,p2stateno=8250,fall=1,numhits=0,getpower='0,0',givepower='0,0',id=number);end(number)
for number,back in [(801,False),(811,True)]:
    state(number,number,move='A',velset='0,0')
    if back:ctl(number,'Back throw','Turn','time=0')
    ctl(number,'Hold','TargetBind','time<18',pos='100,-30');ctl(number,'Throw damage','TargetLifeAdd','time=18',value=-105,kill=1)
    ctl(number,'Release','TargetState','time=18',value=8260);end(number)

# Guardable starters capture only on hit. Cinematic damage resolves exactly
# once, with an orphan timeout and explicit return to the victim's own states.
for n,confirmed,cost,start in [(3000,3010,1000,12),(3200,3210,2000,24)]:
    state(n,n,move='A',velset='0,0',poweradd=-cost)
    ctl(n,'Wind up','SuperPause','time=0',time=16,anim=-1,movetime=0,unhittable=0)
    hit(n,start,0,attr='S,HA',p1stateno=confirmed,p2stateno=8250,getpower='0,0',givepower='0,0');end(n)
for n,total,last,damage in [(3010,240,190,620),(3210,420,350,950)]:
    state(n,n,move='A',velset='0,0')
    ctl(n,'Entry direction','VarSet','time=0',**{'var(44)':'facing'})
    ctl(n,'Confirmed protection','NotHitBy',value='SCA',time=1)
    ctl(n,'Stadium framing','ScreenBound',value=0,movecamera='0,0')
    ctl(n,'Dribble pursuit','PosSet',f'time<{last-30}',x='camerapos x+var(44)*ifelse((time/20)%2=0,-210,210)',y='-40*abs(sin(time*.15))')
    ctl(n,'Shooting position','PosSet',f'time>={last-30}',x='camerapos x-var(44)*290',y=0)
    ctl(n,'Face target','Turn','p2dist x<0')
    ctl(n,'Volley target','TargetBind',f'time<{last}',pos=f'(camerapos x+var(44)*ifelse(time>={last-25},14.4*(time-({last-25})),0)-pos x)*facing,-130-90*abs(sin(time*.08))-pos y')
    ctl(n,'Stadium','Explod','time=0',anim=6401,ID=6401,postype='left',pos='0,0',bindtime=-1,removetime=total,sprpriority=-10,ownpal=1)
    ctl(n,'Giant goal','Explod',f'time={last-70}',anim=6402,ID=6402,postype='left',pos='640+var(44)*360,640',scale='1.6,1.6',bindtime=-1,removetime=100,sprpriority=-3,ownpal=1)
    ctl(n,'Dribble afterimages','AfterImage','time=20',time=last-50,length=16,timegap=1,framegap=3,palcolor=0,palbright='0,0,35',palcontrast='130,160,256',trans='add')
    for tick in range(30,last-30,16 if n==3010 else 12):
        x=350+(tick*19)%550;y=180+(tick*7)%240
        ctl(n,'Ricochet volley','Explod',f'time={tick}',anim=6400,ID=6403,postype='left',pos=f'{x},{y}',velocity=f'{14 if tick%2 else -14},-2',removetime=20,sprpriority=5,ownpal=1,scale='1.4,1.4')
        ctl(n,'Impact star','Explod',f'time={tick}',anim=6405,ID=6405,postype='left',pos='640,390',scale='.35,.35',removetime=7,sprpriority=6,ownpal=1)
        ctl(n,'Volley count','HitAdd',f'time={tick}',value=3)
        ctl(n,'Volley cue','PlaySnd',f'time={tick}',value='0,1')
        ctl(n,'Volley shake','EnvShake',f'time={tick}',time=5,ampl=3,freq=80)
    ctl(n,'Comet shot','Explod',f'time={last-25}',anim=6403,ID=6403,postype='left',pos='640-var(44)*290,410',velocity='26*var(44),0',facing='var(44)',scale='2.6,2.6' if n==3210 else '1.8,1.8',removetime=29,sprpriority=5,ownpal=1)
    ctl(n,'Goal explosion','Explod',f'time={last}',anim=6404,ID=6404,postype='left',pos='640+var(44)*360,400',scale='5,5',removetime=20,sprpriority=6,ownpal=1)
    ctl(n,'GOAL title','Explod',f'time={last}',anim=6406,ID=6406,postype='left',pos='640,180',scale='1.4,1.4',bindtime=-1,removetime=45,sprpriority=8,ownpal=1)
    ctl(n,'Goal flash','EnvColor',f'time={last}',value='180,220,255',time=5,under=0)
    ctl(n,'Final quake','EnvShake',f'time={last}',time=20,ampl=18,freq=75)
    ctl(n,'Goal cue','PlaySnd',f'time={last}',value='0,3')
    ctl(n,'Resolve once','TargetLifeAdd',f'time={last}',value=-damage,kill=1)
    ctl(n,'Release target','TargetState',f'time={last}',value=8260)
    ctl(n,'Recover','ChangeState',f'time>={total-1}',value=0,ctrl=1)
for number,animation in [(8250,5000),(8260,5050)]:
    state(number,kind='A' if number==8260 else 'S',move='H')
    ctl(number,'Own reaction','ChangeAnim','time=0',value=f'ifelse(var(30)=1 && selfanimexist({animation+10000}),{animation+10000},{animation})')
    if number==8250:
        ctl(number,'Captured protection','NotHitBy',value='SCA',time=1)
        ctl(number,'No camera pull','ScreenBound',value=0,movecamera='0,0')
        ctl(number,'Orphan safety','SelfState','time>600',value=0,ctrl=1)
    else:
        ctl(number,'Launch','VelSet','time=0',x=-6,y=-9);ctl(number,'Gravity','VelAdd',y=.65)
        ctl(number,'Land','SelfState',['vel y>0','pos y>=0'],value=5100)
state(9000,0);ctl(9000,'Reset life','LifeSet',value=1000);ctl(9000,'Reset meter','PowerSet',value=3000)
ctl(9000,'Reset form','VarSet',**{'var(30)':0});ctl(9000,'Position','PosSet',x='ifelse(teamside=1,-60,60)',y=0)
ctl(9000,'Speed','VelSet',x=0,y=0);ctl(9000,'Effects','RemoveExplod');ctl(9000,'Ready','ChangeState',value=0,ctrl=1)
(OUT/'yamal.cns').write_text(cns,encoding='utf-8')
assets.sounds('yamal.snd',[(550,.12),(160,.14),(900,.07),(330,.45)])
report={'status':'Built; native validation pending','character':'Lamine Yamal','sprites':assets.meta,
 'sff_bytes':sff_bytes,'source_png_bytes_preserved':True,'revision':1,
 'normals':{str(n):v[0] for n,v in NORMALS.items()},
 'specials':{'1000':'Curler light','1010':'Curler medium','1020':'Curler heavy','1100':'Close Control','1110':'Cut Inside','1120':'Elastico','1130':'Nutmeg','1200':'Rainbow Flick','1400':'Retreat'},
 'super':{'name':'Left-Foot Lightning','cost':1000,'damage':620,'ticks':240},
 'ultimate':{'name':'The World Is My Pitch','cost':2000,'damage':950,'ticks':420},
 'limitations':['First-pass key poses, shared kick and air drawings; additional in-betweens pending','No transformation, portrait or recorded voice; further effects and balance polish pending']}
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('YAMAL_BUILT',sff_bytes,'bytes; 9 original key poses')
