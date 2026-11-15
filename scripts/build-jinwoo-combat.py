"""Build Sung Jinwoo: independent art, daggers and screen-framed shadow army."""
from pathlib import Path
import json, math
from fighter_assets import FighterAssets
import jinwoo_motion as motion
import jinwoo_finishers as monarch
import jinwoo_proportions as proportions
import jinwoo_transform as transformation
ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
assets=FighterAssets(ROOT,'jinwoo'); SOURCE=assets.source; OUT=assets.output
POSES={'idle':375,'slash':375,'lunge':340,'kick':340,'crouch':235,'summon':375,'hurt':360,'down':145}
for i,(key,height) in enumerate(POSES.items()):assets.png(key,SOURCE/'art/v1'/f'{key}.png',height,i)
calibration=proportions.calibrate(assets)
sheets=motion.load(assets)
for i,key in enumerate(['idle','idle','idle','idle','slash','crouch','kick','lunge','slash','kick','hurt','down','idle','idle']):assets.alias(0,i,key)
def dagger(x,y):
    if 4<y<20 and 12<x<115 and abs(y-12)<(115-x)*.09:return (190,125,255,255)
    return (50,30,80,255) if 0<x<28 and 7<y<17 else (0,0,0,0)
assets.raw(0,128,24,dagger)
assets.raw(1,640,360,lambda x,y:(21 if x%48<2 or y%48<2 else 9,8,42 if x%48<2 or y%48<2 else 23,255),(0,0))
assets.raw(2,128,128,lambda x,y:(175,85,255,int(255*max(0,1-abs(math.hypot(x-63.5,y-63.5)-45)/8))))
assets.raw(3,256,96,lambda x,y:(210,165,255,220) if abs((y-48)-(x-128)*.25)<5 and 8<x<248 else (0,0,0,0))
monarch.effects(assets)
sff_bytes=assets.write_sff('jinwoo.sff')
air=assets.air;meta=assets.meta;action=assets.action
for number,key in [(0,'idle'),(5,'idle'),(6,'crouch'),(10,'crouch'),(11,'crouch'),(12,'idle'),(47,'crouch')]:
    action(number,[(key,36 if number in (0,20,21) else -1)])
action(20,[(f'walk_{i}',4) for i in range(8)])
action(21,[(f'walk_{i}',5) for i in reversed(range(8))])
action(22,[('walk_6',2),('walk_7',2),('idle',2)])
action(40,[('jump_0',2),('jump_1',1)])
action(41,[('jump_2',5),('jump_3',-1)])
action(42,[('jump_3',4),('jump_4',-1)])
action(43,[('jump_4',-1)])
action(52,[('jump_5',2),('jump_6',3),('jump_7',1)])
for number in list(range(120,123))+list(range(130,133))+list(range(140,143))+list(range(150,156)):
    action(number,[('crouch' if number in (121,131,141,152,153) else 'hurt' if number>=150 else 'idle',8)])
for number in [170,175,180,181,190,191,195]:action(number,[('down' if number in (170,175) else 'idle',30)])
for number in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:action(number,[('hurt',-1)])
for number in [5100,5110,5140,5150,5160,5170]:action(number,[('down',6 if number in (5100,5160) else -1)],hurt=False)
action(5120,[('down',10),('crouch',10),('idle',5)])
for number in [5200,5210,5220,5300,5500,5510]:action(number,[('crouch',8),('idle',8)])
for number in [820,821,8250,8260,3050,3250,4550]:action(number,[('hurt',-1)],hurt=False)
NORMALS={200:('Dagger Check','slash',6,3,12,30,'S','MA',False),
         210:('Twin Cut','lunge',11,4,17,52,'S','MA',False),
         220:('Monarch Heel','kick',18,5,24,82,'S','MA',True),
         400:('Low Dagger','crouch',7,3,13,26,'C','L',False),
         410:('Low Sweep','kick',15,4,25,58,'C','L',True),
         420:('Rising Dagger','slash',12,5,24,78,'C','MA',True),
         600:('Air Cut','slash',7,5,15,34,'A','H',False),
         610:('Air Heel','kick',10,6,19,58,'A','H',True),
         620:('Diving Cut','lunge',15,7,22,72,'A','H',True)}
for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    box=(15,-85,205,-5) if kind=='C' and guard=='L' else (15,-300,205,-95)
    motion.normal(assets,number,start,active,recovery,kind,guard,pose,box)
for number in [800,810]:action(number,[('slash',5),('slash',4),('idle',25)],active=(1,),attack=(0,-300,105,-60))
for number in [801,811]:action(number,[('slash',10),('lunge',10),('idle',15)])

action(1000,[('idle',18),('slash',6),('idle',25)])
for move in monarch.SHADOW_MOVES:action(move['state'],[('summon',move['startup']),('summon',12),('idle',66-move['startup']-12)])
action(1200,[('dagger-cycle_0',4),('dagger-cycle_1',6),('dagger-cycle_2',12),('lunge',5),
    ('dagger-cycle_5',6),('dagger-cycle_6',8),('dagger-cycle_7',12)],active=(3,),attack=(20,-340,240,-100))
action(1300,[('jump_0',3)]+[(f'walk_{i}',2) for i in range(8)]+[('walk_6',3),('walk_7',3),('idle',5)])
action(1400,[(f'walk_{i}',3) for i in reversed(range(8))]+[('idle',6)])
monarch.animations(assets)
air.extend(['\n[Begin Action 6400]','Clsn1: 1','Clsn1[0] = -45,-12,45,12','7000,0,0,0,-1'])
air.extend(['\n[Begin Action 6401]','7000,1,0,0,-1,,,2,2'])
motion.shadow_actions(assets)
air.extend(['\n[Begin Action 6405]','7000,2,0,0,6,,,1,1','7000,2,0,0,6,,,3,3','7000,2,0,0,6,,,6,6'])
air.extend(['\n[Begin Action 6407]','7000,3,0,0,5,,,1,1','7000,3,0,0,5,,,1.8,1.8'])
transformation.animations(assets)
assets.write_air('jinwoo.air')
(OUT/'jinwoo.def').write_text('''[Info]
name="Sung Jinwoo"
displayname="Sung Jinwoo"
author="Game1 project"
mugenversion=1.1
localcoord=1280,720
[Files]
cmd=jinwoo.cmd
cns=jinwoo.cns
st=jinwoo.cns
stcommon=common1.cns.zss
sprite=jinwoo.sff
anim=jinwoo.air
sound=jinwoo.snd
''',encoding='utf-8')
commands={'L':'a','M':'b','H':'c','skill':'x','super_short':'y','ultimate_short':'z','throw':'d','transform':'w',
          'dagger':'D, DF, F, a','knight':'D, DB, B, b','lunge':'D, DF, F, c','retreat':'D, DB, B, c',
          'holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
commands['step']='D, DF, F, b'
commands.update({'igris':'D, DB, B, a','beru':'D, DB, B, b','iron':'B, B, x','tank':'D, D, x'})
cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={20 if len(keys)>2 and not keys.startswith("/") else 1}\n'
cmd+='\n[Statedef -1]\n'
def command(label,target,conditions):
    global cmd
    cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions[:-1])+f'trigger1={conditions[-1]}\nvalue={target}\nctrl=0\n'
g=['roundstate=2','statetype!=A','ctrl']
command('Random shadow transformation',2000,g+['command="transform"'])
for name,target,cost in [('ultimate_short',3200,2000),('super_short',3000,1000)]:command(name,target,g+[f'power>={cost}',f'command="{name}"'])
for name,target in [('dagger',1000),('igris',1100),('knight',1110),('beru',1110),('iron',1120),('tank',1130),('lunge',1200),('retreat',1400),('step',1300)]:
    command(name,target,g+(['power>=250','var(31)=0'] if target in (1100,1110,1120,1130) else [])+[f'command="{name}"'])
for target,direction in [(1130,'command="holddown"'),(1120,'command="holdback"'),(1110,'command="holdfwd"'),(1100,'1')]:
    command('Choose named shadow',target,g+['power>=250','var(31)=0',direction,'command="skill"'])
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
(OUT/'jinwoo.cmd').write_text(cmd,encoding='utf-8')
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
walk.fwd=3.8
walk.back=-3
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
    if anim is not None:cns+=f'anim=ifelse(var(45)>0,{anim}+var(45)*10000,{anim})\n' if anim<6000 else f'anim={anim}\n'
    cns+=''.join(f'{k}={v}\n' for k,v in params.items())
def ctl(number,label,kind,triggers='1',**params):
    global cns
    if kind=='ChangeAnim' and label not in ('Random shadow form drawing','Restore Monarch drawing') and 'value' in params:
        value=params['value']
        params['value']=f'ifelse(var(45)>0 && selfanimexist(({value})+var(45)*10000),({value})+var(45)*10000,({value}))'
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
ctl(-2,'Summon cooldown','VarAdd','var(31)>0',**{'var(31)':-1})
ctl(-2,'Face opponent','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'No automatic turn','AssertSpecial',flag='noautoturn')
ctl(-2,'Use authored walk control','AssertSpecial',flag='nowalk',flag2='nobrake')
ctl(-2,'Keep own proportions in incoming captures','ChangeAnim',
    ['movetype=H','time=1','stateno=820 || stateno=821 || stateno=1420 || stateno=3050 || stateno=3250 || stateno=4550'],
    value='ifelse(stateno=821 || stateno=1420,5050,5000)')
transformation.states(state,ctl,end)
ctl(-2,'Keep Jinwoo visible during finishers','SprPriority',value='ifelse(stateno=3010 || stateno=3210,4,0)')
ctl(-2,'Finish guard recovery','ChangeState',['stateno=140','animtime=0'],value='ifelse(statetype=C,10,0)',ctrl=1)
for effect in [6401,6402,6403,6405,6407,6700,6701,6702,6703,6800,6801,6802,6803,6804]:ctl(-2,'Cinematic cleanup','RemoveExplod','stateno!=3210 && stateno!=3010',ID=effect)
transformation.move(state,ctl,end)
state(0,0,velset='0,0');ctl(0,'Control','CtrlSet',value=1);ctl(0,'Ground','PosSet',y=0)
state(10,10,kind='C',velset='0,0');ctl(10,'Control','CtrlSet',value=1);ctl(10,'Stand','ChangeState','command!="holddown"',value=0,ctrl=1)
for number,speed,held in [(20,3.8,'holdfwd'),(21,-3,'holdback')]:
    state(number,number);ctl(number,'Control','CtrlSet',value=1)
    ctl(number,'Ease into walk','VelSet',x=f'{speed}*(.35+.65*min(1,time/8.0))',y=0)
    ctl(number,'Stop','ChangeState',f'(ailevel=0 && command!="{held}") || (ailevel>0 && p2bodydist x<140)',value=22,ctrl=1)
state(22,22);ctl(22,'Settle','VelMul',x=.6);ctl(22,'Ground','PosSet',y=0);end(22)
state(40,40);ctl(40,'Direction','VarSet','time=0',**{'var(1)':'ifelse(command="holdfwd",3.5,ifelse(command="holdback",-3,0))'})
ctl(40,'Take off','ChangeState','time>=3',value=50,ctrl=1)
state(50,41,kind='A');ctl(50,'Control','CtrlSet',value=1)
ctl(50,'Launch','VelSet',['time=0','prevstateno=40'],x='var(1)',y=-12.5)
ctl(50,'Apex pose','ChangeAnim',['vel y=[-3,3]','anim!=42'],value=42)
ctl(50,'Descending pose','ChangeAnim',['vel y>3','anim!=43'],value=43)
ctl(50,'Gravity','VelAdd',y=.65);ctl(50,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
state(52,52,velset='0,0');ctl(52,'Ground','PosSet',y=0);ctl(52,'Recover','ChangeState','time>=5',value=0,ctrl=1)
for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
    state(number,number,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}))
    hit(number,start,damage,kind,guard,fall)
    if kind=='A':ctl(number,'Gravity','VelAdd',y=.65);ctl(number,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
    end(number,kind=='A',kind=='C')

state(1000,1000,move='A',velset='0,0')
ctl(1000,'Thrown dagger','Projectile','time=18',projid=1000,projanim=6400,projhitanim=-1,projremanim=-1,
    projremove=1,projremovetime=120,velocity='11,0',offset='120,-280',attr='S,SP',damage='48,2',
    guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=22,
    ground__velocity=-3,air__velocity='-4,-5',getpower='40,10',givepower='20,10',hitsound='S0,1')
ctl(1000,'Dagger cue','PlaySnd','time=18',value='0,0');end(1000)
for move in monarch.SHADOW_MOVES:
    n,i=move['state'],move['selection']
    state(n,n,move='A',velset='0,0',poweradd=-250)
    ctl(n,'Assigned named shadow','VarSet','time=0',**{'var(35)':i})
    ctl(n,'Summon cooldown','VarSet','time=0',**{'var(31)':90})
    ctl(n,move['name']+' attack','Projectile',f'time={move["startup"]}',projid=1100+i,projanim=6500+i,projhitanim=-1,projremanim=-1,
        projremove=0,projremovetime=30,velocity=f'{move["speed"]},0',offset='110,0',attr='S,SP',damage=f'{move["damage"]},2',
        guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=24,
        ground__velocity=move['launch'],air__velocity=move['launch'],fall=1,getpower='0,0',givepower='20,10',hitsound='S0,3')
    ctl(n,'Shadow cue','PlaySnd',f'time={move["startup"]}',value='0,3');end(n)
state(1200,1200,move='A',velset='0,0');hit(1200,22,90,guard='H',fall=True,attr='S,SA')
ctl(1200,'Fatal lunge','VelSet','time=[10,26]',x=4)
ctl(1200,'Stop','VelSet','time>=27',x=0);end(1200)
for n,speed in [(1300,8),(1400,-6)]:
    state(n,n,velset='0,0');ctl(n,'Shadow step','VelSet','time<16',x=speed)
    ctl(n,'Recover step','VelSet','time>=16',x=0);end(n)
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

army_framing=[]
def army_scale(key,x,facing,desired):
    limits=[desired]
    for frame in range(4):
        m=meta[f'{key}_{frame}'];x0,y0,x1,y1=m['bounds'];ax,ay=m['axis'];s=m['scale']
        left,right=sorted([(x0-ax)*s*facing,(x1-ax)*s*facing])
        limits.extend([(x-50)/max(1,-left),(1230-x)/max(1,right),610/max(1,(ay-y0)*s)])
    return min(limits)
def army_bounds(key,x,facing,scale):
    m=meta[key];x0,y0,x1,y1=m['bounds'];ax,ay=m['axis'];s=m['scale']*scale
    left,right=sorted([x+(x0-ax)*s*facing,x+(x1-ax)*s*facing])
    bounds=[left,660+(y0-ay)*s,right,660+(y1-ay)*s]
    assert left>=40 and right<=1240 and bounds[1]>=40 and bounds[3]<=680,(key,bounds)
    army_framing.append({'pose':key,'x':x,'facing':facing,'scale':scale,'bounds':bounds})
monarch.states(state,ctl,hit,end,army_scale,army_bounds,motion.SHADOWS)
# These victim states select the victim's own reaction sprites, including the
# suited bank when Will is Agent J.
for number,animation in [(8250,5000),(8260,5050)]:
    state(number,kind='A' if number==8260 else 'S',move='H')
    ctl(number,'Own character reaction','ChangeAnim','time=0',value=f'ifelse(var(30)=1 && selfanimexist({animation+10000}),{animation+10000},{animation})')
    if number==8250:
        ctl(number,'Captured protection','NotHitBy',value='SCA',time=1)
        ctl(number,'No camera pull','ScreenBound',value=0,movecamera='0,0')
        ctl(number,'Orphan safety','SelfState','time>600',value=0,ctrl=1)
    else:
        ctl(number,'Launch','VelSet','time=0',x=-6,y=-9)
        ctl(number,'Gravity','VelAdd',y=.65)
        ctl(number,'Land','SelfState',['vel y>0','pos y>=0'],value=5100)
state(9000,0);ctl(9000,'Reset life','LifeSet',value=1000);ctl(9000,'Reset meter','PowerSet',value=3000)
ctl(9000,'Reset form','VarSet',**{'var(30)':0})
ctl(9000,'Reset cooldown','VarSet',**{'var(31)':0})
ctl(9000,'Reset shadow form','VarSet',**{'var(45)':0})
ctl(9000,'Reset position','PosSet',x='ifelse(teamside=1,-60,60)',y=0)
ctl(9000,'Reset speed','VelSet',x=0,y=0);ctl(9000,'Clear effects','RemoveExplod');ctl(9000,'Ready','ChangeState',value=0,ctrl=1)

(OUT/'jinwoo.cns').write_text(cns,encoding='utf-8')
assets.sounds('jinwoo.snd',[(700,.1),(160,.14),(900,.07),(280,.32)])
report={'status':'Built; native validation pending','character':'jinwoo','sprites':meta,
        'source_png_bytes_preserved':True,'sff_bytes':sff_bytes,'army_framing':army_framing,
        'revision':3,'visual_revision':5,'transformation':{'key':']','forms':list(transformation.SHADOWS),'selection':'random on activation; press again to return','cost':0},'proportion_calibration':calibration,'motion_sheets':sheets,'named_shadows':list(motion.SHADOWS),
        'summon_selection':{'R':'Igris','toward+R':'Beru','away+R':'Iron','down+R':'Tank'},
        'army_choreography':'Tank charge, Iron launch, Igris cuts, Beru pursuit, full-army finale',
        'normals':{str(n):v[0] for n,v in NORMALS.items()},
        'specials':{'1000':'Dagger Throw','1100':'Igris Blade Command','1110':'Beru Predator Rush','1120':'Iron Bulwark Smash','1130':'Tank Avalanche',
                    '1200':'Fatal Lunge','1300':'Shadow Step','1400':'Retreat'},
        'super':{'name':'Dagger Tempest: Monarch Storm','cost':1000,'damage':monarch.SUPER['damage'],'confirmed_ticks':monarch.SUPER['total']},
        'ultimate':{'name':"Monarch's Decree: Arise",'cost':2000,'damage':monarch.ULTIMATE['damage'],'confirmed_ticks':monarch.ULTIMATE['total'],'hit_confirm_only':True,'screen_wide_starter':True},
        'limitations':['Eight-frame walk, dagger and jump cycles; four poses per shadow; some low/kick/reaction drawings shared',
                        'No portraits or voices; further in-betweens and balance polish pending']}
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
preview={}
for name,info in sheets.items():
    preview[name]=[dict(meta[f'{name}_{i}'],file=str(Path(meta[f'{name}_{i}']['file']).relative_to(SOURCE.relative_to(ROOT))).replace('\\','/')) for i in range(info['frames'])]
preview['proportions']=[dict(meta[key],file=f'art/v1/{key}.png') for key in
    ('idle','crouch','hurt','down','crouch','idle','kick','lunge','slash','idle')]
(SOURCE/'motion-data.js').write_text('window.JINWOO_MOTION='+json.dumps(preview)+';\n',encoding='utf-8')
print('JINWOO_BUILT',sff_bytes,'sprite bytes; 15 original PNG sources + 40 lossless cells; army framing verified')
