"""Authored Baam adaptation. Common movement comes from the bundled engine."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'sprite-fighter/characters/baam'
E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
FORM='map(baam.form)'
MOVES=[('palm','x',1000,500,'Shinsu Palm'),('piercer','/$F,x',1100,700,'Flow Piercer'),('stop','/$B,x',1200,600,'Reverse Flow Control'),('orb','/$D,x',1300,500,'Shinsu Baang'),('butterfly','y',2000,1500,'Floral Butterfly'),('shield','/$B,y',2100,1000,'Blue Thryssa Guard'),('wave','/$F,y',2200,2000,'Thorn Wave'),('ultimate','z',3000,3000,'Shinwonryu')]
NORMALS={200:(35,6,24,[1,2,2]),210:(45,7,24,[3,4,4]),220:(60,8,28,[5,6,7]),230:(45,7,24,[5,6,6]),240:(55,7,26,[5,6,6]),250:(70,9,30,[5,6,7]),260:(80,10,30,[5,6,7]),400:(30,6,24,[12,12,12]),410:(50,8,28,[12,12,12]),420:(70,10,30,[13,13,13]),600:(35,6,24,[14,14,14]),610:(50,8,26,[14,14,14]),620:(70,10,30,[14,14,14])}
LINKS={200:{1:210,2:230,3:260},210:{1:220,2:220,3:260},230:{1:240,2:240,3:260},240:{1:250,2:250,3:260}}

class Author:
    def __init__(self):self.cns='';self.animations={}
    def state(self,n,anim=None,kind='S',move='I',physics=None,bank=True,**params):
        if n<0:
            self.cns+=f'\n[Statedef {n}]\n'
            return
        self.cns+=f'\n[Statedef {n}]\ntype={kind}\nmovetype={move}\nphysics={physics or ("A" if kind=="A" else "S" if kind=="S" else "C" if kind=="C" else "N")}\nctrl=0\n'
        if anim is not None:self.cns+=f'anim={anim}'+(f'+1000000*{FORM}' if bank else '')+'\n'
        self.cns+=''.join(f'{k}={v}\n' for k,v in params.items())
    def ctl(self,n,label,kind,triggers='1',**params):
        self.cns+=f'\n[State {n}, {label}]\ntype={kind}\n'
        self.cns+=''.join(f'trigger1={t}\n' for t in (triggers if isinstance(triggers,list) else [triggers]))
        self.cns+=''.join(f'{k.replace("__",".")}={v}\n' for k,v in params.items())
    def end(self,n,kind='S'):
        self.ctl(n,'Recover','ChangeState','animtime=0',value=50 if kind=='A' else 11 if kind=='C' else 0,ctrl=1)
        if kind=='A':self.ctl(n,'Land','ChangeState',['vel y>0','pos y>=0'],value=52,ctrl=1)
    def hit(self,n,t,amount,kind='S',guard='MA',fall=False,**params):
        b=dict(attr=kind+',NA',damage=f'{amount},4',guardflag=guard,hitflag='MAF',pausetime='4,6',animtype='Hard' if fall else 'Medium',ground__type='Low' if kind=='C' else 'High',ground__hittime=26,ground__slidetime=10,ground__velocity='3,-3' if fall else '.25',air__velocity='2,-3',fall=int(fall),sparkno='S9120',guard__sparkno='S9121',hitsound='S0,6',guardsound='S0,1',getpower='20,5',givepower='10,5')
        b['sparkxy']='0,-16' if kind=='C' else '0,-32'
        b.update(params);self.ctl(n,'Contact','HitDef',f'time={t}',**b)
    def action(self,n,frames,active=(),box=(9,-44,48,-9),kind='S',hurt=True):
        text=f'\n[Begin Action {n}]\n'
        if hurt:text+='Clsn2Default: 1\nClsn2[0]='+('-11,-29,12,0' if kind=='C' else '-11,-51,12,0')+'\n'
        for i,(g,p,t,*offset) in enumerate(frames):
            if i in active:text+='Clsn1: 1\nClsn1[0]='+','.join(map(str,box))+'\n'
            x,y=offset if offset else (0,0)
            text+=f'{g},{p},{x},{y},{t},,,.125,.125\n'
        self.animations[n]=text
    def fx(self,n,pose,t,pos='28,-31',scale='.05,.05',duration=16):
        self.ctl(n,'Localized Shinsu','Explod',f'time={t}',anim=9000+pose,ID=9000+pose,pos=pos,postype='p1',bindtime=1,removetime=duration,scale=scale,sprpriority=-1,ownpal=1,removeongethit=1)

def author_moves(a):
    st,ct=a.state,a.ctl
    st(20,20,velset='0,0')
    ct(20,'Walking control','CtrlSet',value=1)
    ct(20,'Walk direction','VelSet',x='ifelse(AILevel>0,1.5,ifelse(command="holdback",-1.2,ifelse(command="holdfwd",1.5,0)))',y=0)
    ct(20,'Forward stride','ChangeAnim','vel x>0 && anim%1000000!=20',value='20+1000000*map(baam.form)')
    ct(20,'Backward stride','ChangeAnim','vel x<0 && anim%1000000!=21',value='21+1000000*map(baam.form)')
    ct(20,'Stop walking','ChangeState','(AILevel=0 && command!="holdfwd" && command!="holdback") || (AILevel>0 && p2bodydist x<30)',value=0,ctrl=1)
    # Standard movement and reaction animations stay in the current form bank.
    for n in (170,175,180,181,190,191,195):
        st(n,190 if n in (190,191) else 181 if n in (180,181,195) else 170,velset='0,0')
        if n in (190,191):
            ct(n,'Reset form','MapSet','!time',map='"baam.form"',value=1)
            ct(n,'Real round entrance','AssertSpecial','roundstate<2 && time<72',flag='intro')
            a.end(n)
        elif n in (180,181,195):ct(n,'Victory hold','NotHitBy',value='SCA',time=1)
    st(-3,bank=False,physics='N')
    for i,key in enumerate(('a','b','c'),1):
        ct(-3,'Buffer '+key,'MapSet',f'!ishelper && time>1 && (stateno=200 || stateno=210 || stateno=220 || stateno=230 || stateno=240 || stateno=250 || stateno=260) && command="{key}"',map='"baam.buffer"',value=i)
    ct(-3,'Buffer window','MapSet','!ishelper && (command="a" || command="b" || command="c")',map='"baam.buffer_ticks"',value=12)
    ct(-3,'Buffer decay','MapAdd','!ishelper && map(baam.buffer_ticks)>0',map='"baam.buffer_ticks"',value=-1)
    ct(-3,'Thorn appears after awakening','Explod',['!ishelper',FORM+'=1','numexplod(9090)=0'],anim=9090,ID=9090,pos='-14,-39',postype='p1',bindtime=-1,removetime=-1,scale='.045,.045',sprpriority=-1,ownpal=1)
    ct(-3,'Dismiss thorn','RemoveExplod',['!ishelper',FORM+'=0'],ID=9090)
    for n,(damage,active,duration,poses) in NORMALS.items():
        k='A' if n>=600 else 'C' if n>=400 else 'S'
        st(n,n,kind=k,move='A',**({} if k=='A' else dict(velset='0,0')),poweradd=20)
        ct(n,'Consume buffer','MapSet','!time',map='"baam.buffer"',value=0)
        if k=='S':
            ct(n,'Step','VelSet','time<4',x=1.5)
            ct(n,'Plant feet','VelSet','time>=4',x=0)
        ct(n,'Strike wind','PlaySnd',f'time={max(0,active-3)}',value='0,5',volumescale=65)
        if n in (220,250,260,620):
            ct(n,'Finisher motion trail','AfterImage','!time',time=12,length=3,timegap=2,framegap=2,palcolor=0,palbright='0,15,25',palcontrast='160,200,220',trans='add1')
            ct(n,'Finisher impact','EnvShake','MoveHit && time<18',time=3,ampl=-2,freq=75,persistent=0)
        a.hit(n,active,damage,k,guard='H' if k=='A' else 'L' if k=='C' else 'MA',fall=n in (220,250,260,410,420,620))
        for button,destination in LINKS.get(n,{}).items():ct(n,'Confirmed chain','ChangeState',f'MoveContact && time>={active+1} && time<={duration-2} && ((map(baam.buffer)={button} && map(baam.buffer_ticks)>0) || (AILevel>0 && time>={active+3} && {button}=1))',value=destination)
        a.end(n,k)
    from baam_combat_v3 import author_techniques,author_ultimate
    author_techniques(a,MOVES)
    # A free, interruptible transformation, with the same eight drawings reversed.
    st(800,'800+map(baam.form)',bank=False,velset='0,0')
    ct(800,'Destination form','MapSet','!time',map='"baam.next_form"',value='1-map(baam.form)')
    ct(800,'Commit complete ignition','MapSet','time=64',map='"baam.form"',value='map(baam.next_form)')
    ct(800,'Ignition tone','PlaySnd','time=40',value='0,4')
    a.fx(800,14,16,pos='0,-2',scale='.08,.025',duration=55)
    a.end(800)
    st(700,700,velset='0,0');ct(700,'Gather Shinsu','PowerAdd',value=15)
    a.fx(700,0,0,pos='8,-29',scale='.035,.035',duration=18)
    ct(700,'Release charge','ChangeState','command!="hold_s" || power>=3000',value=0,ctrl=1)
    st(900,900,physics='N',velset='-2,0')
    ct(900,'Evade window','NotHitBy','time=[3,12]',value='SCA',time=1)
    ct(900,'Settle','VelSet','time=14',x=0);a.end(900)
    author_ultimate(a)

def author_commands():
    commands={'a':'a','b':'b','c':'c','hold_s':'/s','form':'w','evade':'d','FF':'F,F','BB':'B,B','holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
    commands.update({name:key for name,key,*_ in MOVES})
    cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=15\ncommand.buffer.time=1\n'
    for name,key in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={key}\ntime={15 if key in ("F,F","B,B") else 1}\n'
    cmd+='\n[Statedef -1]\n'
    def route(label,n,conditions):
        nonlocal cmd
        cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions[:-1])+f'trigger1={conditions[-1]}\nvalue={n}\nctrl=0\n'
    g=['AILevel=0','roundstate=2','statetype!=A']
    chain='(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))'
    for name,key,n,cost,label in sorted(MOVES,key=lambda m:-len(m[1])):
        exclude=['command!="holdfwd"','command!="holdback"','command!="holddown"'] if name=='palm' else ['command!="holdfwd"','command!="holdback"'] if name=='butterfly' else []
        route(label,n,g+[chain if n not in (1200,2100) else 'ctrl',f'power>={cost}']+exclude+[f'command="{name}"'])
    for name,n in [('form',800),('evade',900),('hold_s',700),('FF',100),('BB',105)]:route(name,n,g+['ctrl']+(['power<3000'] if n==700 else [])+[f'command="{name}"'])
    for key,n in [('a',600),('b',610),('c',620)]:route('Air '+key,n,['AILevel=0','roundstate=2','statetype=A','ctrl',f'command="{key}"'])
    for key,n in [('a',400),('b',410),('c',420)]:route('Low '+key,n,g+['ctrl','command="holddown"',f'command="{key}"'])
    for key,n in [('a',200),('b',230),('c',260)]:route('Normal '+key,n,g+['ctrl',f'command="{key}"'])
    ai=['AILevel>0','roundstate=2','ctrl','statetype!=A']
    route('CPU Shinwonryu',3000,ai+['power>=3000','p2bodydist x<40','random<25'])
    route('CPU ignition',800,ai+[FORM+'=0','life<700','p2bodydist x>45','random<10'])
    route('CPU palm',1000,ai+['power>=500','p2bodydist x<38','random<35'])
    route('CPU baang',1300,ai+['power>=500','numhelper(10001)=0','p2bodydist x>50','random<18'])
    route('CPU strike',200,ai+['p2bodydist x<35','random<65'])
    route('CPU approach',20,ai+['stateno!=20','p2bodydist x>=35','random<60'])
    return cmd
