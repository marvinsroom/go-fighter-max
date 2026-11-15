"""Shared native movement/reaction authoring for the Chappelle fighters.
Core controllers follow the validated project fighter convention.
"""
FORMS=False
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
    if anim is not None:cns+=f'anim=ifelse(var(45)>0 && selfanimexist({anim}+10000),{anim}+10000,{anim})\n' if FORMS else f'anim={anim}\n'
    cns+=''.join(f'{k}={v}\n' for k,v in params.items())
def ctl(number,label,kind,triggers='1',**params):
    global cns
    if FORMS and kind=='ChangeAnim' and label not in ('Keep Tyrone drawing','Restore Rick drawing','Same-frame reveal','Own reaction') and 'value' in params:
        value=params['value']
        params['value']=f'ifelse(var(45)>0 && selfanimexist(({value})+10000),({value})+10000,({value}))'
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

DATA=cns
def reset(forms=False):
    global cns,FORMS
    cns=DATA;FORMS=forms

def basic_states(NORMALS,walk_speed=3.8,globals_hook=None):
    state(-2)
    ctl(-2,'Face opponent','Turn',['ctrl','statetype!=A','p2dist x<0'])
    ctl(-2,'No automatic turn','AssertSpecial',flag='noautoturn')
    ctl(-2,'Authored movement','AssertSpecial',flag='nowalk',flag2='nobrake')
    ctl(-2,'Own proportions in incoming captures','ChangeAnim',
     ['movetype=H','time=1','stateno=820 || stateno=821 || stateno=1420 || stateno=3050 || stateno=3250 || stateno=4550'],value='ifelse(stateno=821 || stateno=1420,5050,5000)')
    ctl(-2,'Finish guard recovery','ChangeState',['stateno=140','animtime=0'],value='ifelse(statetype=C,10,0)',ctrl=1)
    ctl(-2,'Finisher foreground','SprPriority',value='ifelse(stateno=3010 || stateno=3210 || stateno=4410 || stateno=4510,4,0)')
    for effect in range(6401,6421):ctl(-2,'Cinematic cleanup','RemoveExplod','stateno!=3210 && stateno!=3010 && stateno!=4410 && stateno!=4510',ID=effect)
    if globals_hook:globals_hook()
    state(0,0,velset='0,0');ctl(0,'Control','CtrlSet',value=1);ctl(0,'Ground','PosSet',y=0)
    state(10,10,kind='C',velset='0,0');ctl(10,'Control','CtrlSet',value=1);ctl(10,'Stand','ChangeState','command!="holddown"',value=0,ctrl=1)
    for number,speed,held in [(20,walk_speed,'holdfwd'),(21,-walk_speed*.74,'holdback')]:
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
    for number,nextstate in [(800,801),(810,811)]:
        state(number,number,move='A',velset='0,0')
        ctl(number,'Shoulder challenge','HitDef','time=5',attr='S,NT',hitflag='M-',priority='1,Miss',sparkno=-1,guard__dist=0,
          pausetime='0,0',p1stateno=nextstate,p2stateno=8250,fall=1,numhits=0,getpower='0,0',givepower='0,0',id=number);end(number)
    for number,back in [(801,False),(811,True)]:
        state(number,number,move='A',velset='0,0')
        if back:ctl(number,'Back throw','Turn','time=0')
        ctl(number,'Hold','TargetBind','time<18',pos='100,-30');ctl(number,'Throw damage','TargetLifeAdd','time=18',value=-105,kill=1)
        ctl(number,'Release','TargetState','time=18',value=8260);end(number)
    
    for number,animation in [(8250,5000),(8260,5050)]:
        state(number,kind='A' if number==8260 else 'S',move='H')
        ctl(number,'Own reaction','ChangeAnim','time=0',value=f'ifelse(var(45)>0 && selfanimexist({animation}+var(45)*10000),{animation}+var(45)*10000,ifelse(var(30)=1 && selfanimexist({animation+10000}),{animation+10000},{animation}))')
        if number==8250:
            ctl(number,'Captured protection','NotHitBy',value='SCA',time=1)
            ctl(number,'No camera pull','ScreenBound',value=0,movecamera='0,0')
            ctl(number,'Orphan safety','SelfState','time>600',value=0,ctrl=1)
        else:
            ctl(number,'Launch','VelSet','time=0',x=-6,y=-9);ctl(number,'Gravity','VelAdd',y=.65)
            ctl(number,'Land','SelfState',['vel y>0','pos y>=0'],value=5100)
    state(9000,0);ctl(9000,'Reset life','LifeSet',value=1000);ctl(9000,'Reset meter','PowerSet',value=3000)
    ctl(9000,'Reset form','VarSet',**{'var(30)':0});ctl(9000,'Reset transformation','VarSet',**{'var(45)':0});ctl(9000,'Reset transform cooldown','VarSet',**{'var(47)':0});ctl(9000,'Position','PosSet',x='ifelse(teamside=1,-60,60)',y=0)
    ctl(9000,'Speed','VelSet',x=0,y=0);ctl(9000,'Effects','RemoveExplod');ctl(9000,'Ready','ChangeState',value=0,ctrl=1)

def basic_animations(assets,NORMALS,reach=230):
    action=assets.action
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
    
    for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
        action(number,[('jump' if kind=='A' else 'crouch' if kind=='C' else 'idle',start),(pose,active),('jump' if kind=='A' else 'crouch' if kind=='C' else 'idle',recovery)],active=(1,),kind=kind,attack=(0,-100,220,-5) if guard=='L' else (0,-320,reach,-50))
    for n in [800,810]:action(n,[('idle',5),('palm',4),('idle',25)],active=(1,),attack=(0,-300,105,-30))
    for n in [801,811]:action(n,[('idle',10),('palm',10),('idle',15)])
