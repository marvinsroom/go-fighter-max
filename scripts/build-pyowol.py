"""Independent illustrated Pyo Wol fighter; authored thread combat, no reskin states."""
from pathlib import Path
import hashlib,json,math,shutil
from PIL import Image,ImageDraw,ImageFilter
from fighter_assets import FighterAssets
from isolated_sprite_atlas import extract
from pyowol_animation import load_sequences,author_sequences,write_audio,export_player
from pyowol_silk import load_silk,author_silk,write_silk_states,spawn_silk

ROOT=Path(__file__).resolve().parents[1]
A=FighterAssets(ROOT,'pyowol'); S=A.source; O=A.output
ART=S/'art/v4'
(ART/'poses').mkdir(parents=True,exist_ok=True)
for sheet,cols,rows,ref,prefix in [('movement',4,4,0,'m'),('combat',4,3,10,'c')]:
    tiles=extract(ART/f'{sheet}.png',cols,rows)
    scale=375/tiles[ref][0].height
    for i,(im,bounds) in enumerate(tiles):
        path=ART/f'poses/{prefix}{i}.png';im.save(path)
        A.png(f'{prefix}{i}',path,375,i+(0 if prefix=='m' else 16))
        A.meta[f'{prefix}{i}']['scale']=scale
        A.meta[f'{prefix}{i}']['bank']='legacy-'+sheet
A.alias(0,0,'m0');A.alias(0,3,'m0')
portrait=Image.open(S/'art/animation-v5/profile-portrait.png').convert('RGBA')
portrait.resize((120,120),Image.Resampling.LANCZOS).save(S/'art/animation-v5/portrait-small.png')
A.png('portrait',S/'art/animation-v5/portrait-small.png',120,0,9000)
import struct
h=list(struct.unpack('<HHHHhhHBBIIHH',A.headers[-1]));h[4:6]=[0,0];A.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*h)
portrait.resize((320,320),Image.Resampling.LANCZOS).save(S/'art/animation-v5/portrait-large.png')
A.png('portrait-large',S/'art/animation-v5/portrait-large.png',320,1,9000)
h=list(struct.unpack('<HHHHhhHBBIIHH',A.headers[-1]));h[4:6]=[0,0];A.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*h)
load_sequences(A)
# Smooth code-native threads, daggers and moon. No character paint or AI edits.
for i in range(12):
    im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im)
    if i<5:
        # Thin, local cuts anchored at the impact; no arena-wide laser lattice.
        for j in range(1+i):
            y=325+j*18
            d.line([(440,y+60),(640,y),(840,y-40)],fill=(111,22,54,95),width=6)
            d.line([(440,y+60),(640,y),(840,y-40)],fill=(236,239,255,230),width=2)
    elif i==5:
        d.polygon([(535,356),(715,349),(750,360),(715,370)],fill=(240,246,255,255))
        d.line([(480,360),(540,360)],fill=(160,30,60,255),width=8)
    elif i==6:
        d.rectangle((0,0,1280,720),fill=(5,7,18,215))
        d.ellipse((450,95,830,475),fill=(77,17,39,235),outline=(183,72,93,220),width=2)
        d.ellipse((475,105,820,445),fill=(90,22,42,210))
    elif i==7:
        for j in range(7):
            angle=j*math.pi/3.5
            d.line((640,360,640+230*math.cos(angle),360+210*math.sin(angle)),fill=(229,231,255,220),width=2)
        for r in [95,165,225]:d.ellipse((640-r,360-r*.8,640+r,360+r*.8),outline=(175,63,91,155),width=1)
    elif i==8:
        d.rectangle((0,0,1280,720),fill=(0,0,0,255))
        d.line((150,500,1130,220),fill=(255,239,246,255),width=4)
        d.line((350,110,940,610),fill=(216,75,110,255),width=2)
    elif i==9:
        d.arc((475,235,805,470),190,330,fill=(211,222,255,230),width=3)
        d.arc((495,250,780,445),195,320,fill=(239,242,255,160),width=2)
    elif i==10:
        d.line((340,650,940,650),fill=(240,215,230,245),width=3)
        for x in range(380,940,70):d.line((x,650,x+45,620),fill=(220,55,100,220),width=2)
    else:
        for j in range(8):
            a=j*math.pi/4;r=48 if j%2 else 74
            d.line((640+10*math.cos(a),360+10*math.sin(a),640+r*math.cos(a),360+r*math.sin(a)),fill=(255,238,249,240),width=2)
    im.putpixel((0,0),(0,0,0,0))
    path=S/f'art/animation-v5/fx-{i}.png';im.save(path);A.png(f'fx{i}',path,720,i,7000);A.meta[f'fx{i}']['scale']=1
    # All FX share arena center, independent of alpha bounds.
    import struct
    h=list(struct.unpack('<HHHHhhHBBIIHH',A.headers[-1]));h[4:6]=[640,360];A.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*h)
load_silk(A)
act=A.action
for n,key in [(0,'m0'),(5,'m0'),(6,'m8'),(10,'m8'),(11,'m8'),(12,'m0'),(47,'m8')]:act(n,[(key,6 if n==12 else -1)])
for n,keys in [(20,[1,2,3,4]),(21,[4,3,2,1])]:act(n,[(f'm{i}',7) for i in keys])
act(22,[('m1',4),('m0',3)])
for n,key in [(40,'m8'),(41,'m6'),(42,'m7'),(43,'m7'),(52,'m8')]:act(n,[(key,5)])
for n in list(range(120,123))+list(range(130,134))+list(range(140,144))+list(range(150,157)):act(n,[('m9',8)])
for n in [170,175,5100,5110,5140,5150,5160,5170]:act(n,[('m11',-1)],hurt=False)
for n in [180,181,195]:act(n,[('m15',45)])
act(190,[('m14',35),('m13',30),('m0',25)])
act(191,[('m0',1)])
for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090,820,821,8250]:act(n,[('m10',-1)])
act(5120,[('m11',10),('m12',12),('m0',5)])
for n in [5200,5210,5220,5300,5500,5510]:act(n,[('m7',8),('m0',8)])
NORMALS=[(200,'Hidden Fang',0,6,34,'S'),(210,'Silk Finger',1,9,55,'S'),(220,'Crescent Dagger',2,13,82,'S'),(400,'Low Fang',4,6,30,'C'),(410,'Ankle Thread',5,9,52,'C'),(420,'Rising Fang',6,12,76,'C'),(600,'Falling Fang',7,6,35,'A'),(610,'Air Silk',1,9,52,'A'),(620,'Descending Reaper',7,12,74,'A')]
for n,name,pose,start,damage,kind in NORMALS:
    act(n,[('m7' if kind=='A' else 'm8' if kind=='C' else 'm0',start),(f'c{pose}',5),('m7' if kind=='A' else 'm8' if kind=='C' else 'm0',15 if n%100<20 else 24)],active=(1,),kind=kind,attack=(0,-150,280,0) if kind=='C' and n!=420 else (0,-340,300,-40))
for n,pose in [(1000,8),(1100,1),(1120,10),(1200,3),(1300,9),(3000,11),(3100,1),(3200,11),(4000,10)]:act(n,[('m13',16),(f'c{pose}',7),('m0',27)],active=(1,) if n in (1120,3200,4000) else (),attack=(0,-360,380,-10))
act(500,[('m13',8),('c10',8)])
for n,total in [(1121,60),(3201,135),(4001,265)]:act(n,[(f'c{i}',12) for i in ([10,11,1,2]*6)][:total//12]+[('m0',15)])
for n in range(12):
    act(7000+n,[(f'fx{n}',-1)],hurt=False,active=(0,) if n in (5,10) else (),attack=(-75,-15,75,15) if n==5 else (-260,-20,260,15))
    # Projectile collision is anchored at the actual central dagger / snare.
    if n==10:pass
A.write_sff('pyowol.sff');A.write_air('pyowol.air');A.sounds('pyowol.snd',[(1300,.12),(700,.12),(190,.2),(75,.7),(1800,.25)])
(O/'pyowol.def').write_text('[Info]\nname="Pyo Wol"\ndisplayname="Pyo Wol"\nauthor="Game1 fan adaptation"\nmugenversion=1.1\nlocalcoord=1280,720\n[Files]\ncmd=pyowol.cmd\ncns=pyowol.cns\nst=pyowol.cns\nstcommon=common1.cns.zss\nsprite=pyowol.sff\nanim=pyowol.air\nsound=pyowol.snd\n',encoding='utf-8')
# Reuse only the common movement/state writer functions from the standalone
# fighter template. No Yamal attacks, ball effects or cinematics are imported.
template=(ROOT/'scripts/build-yamal-combat.py').read_text(encoding='utf-8')
namespace={};start=template.index("cns='''[Data]");end=template.index('state(-2)',start)
exec(template[start:end],namespace)
state=namespace['state'];ctl=namespace['ctl'];end=namespace['end'];hit=namespace['hit']
state(-2)
ctl(-2,'Face','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'Own movement','AssertSpecial',flag='nowalk',flag2='nobrake',flag3='noautoturn')
ctl(-2,'Veil cooldown','VarAdd','var(10)>0',**{'var(10)':-1})
ctl(-2,'Snare cooldown','VarAdd','var(11)>0',**{'var(11)':-1})
for fx in [7006,7007,7008]:ctl(-2,'Clear cinematic','RemoveExplod','stateno!=4001 && stateno!=3201',ID=fx)
movement=template[template.index('state(0,0,velset='):template.index('for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():')]
exec(movement,namespace)
for n,name,pose,start,damage,kind in NORMALS:
    state(n,n,kind=kind,move='A',**({} if kind=='A' else {'velset':'0,0'}))
    weight=(n%100)//10
    hit(n,start,damage,kind,guard='H' if kind=='A' else 'L' if kind=='C' and n!=420 else 'MA',fall=n in (220,420,620),
        pausetime=['3,6','5,8','7,11'][weight],sparkno='S7111' if n in (210,410,610) else 'S7011',ground__hittime=27,
        ground__velocity='-3,-5' if n in (220,420,620) else '-1.8')
    ctl(n,'Cut sound','PlaySnd',f'time={start-1}',value='0,0')
    ctl(n,'Contact weight','EnvShake','movehit=1',time=4+weight*2,freq=90,ampl=1+weight)
    if kind!='A':
        ctl(n,'Step into cut','VelSet',f'time=[{start-2},{start+2}]',x=1.6+weight*1.8)
        ctl(n,'Plant feet','VelSet',f'time={start+3}',x=0)
    if kind=='A':ctl(n,'Gravity','VelAdd',y=.65);ctl(n,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
    if n in (210,410,610):spawn_silk(ctl,n,start)
    else:ctl(n,'Cut trail','Explod',f'time={start}',anim=7009,ID=7009,pos='160,-190',scale='.85,.65',removetime=5,sprpriority=3,ownpal=1)
    end(n,kind=='A',kind=='C')
state(190,190,velset='0,0');ctl(190,'Intro','AssertSpecial','time<60',flag='intro');ctl(190,'Reveal','Trans','time<12',trans='addalpha',alpha='min(256,time*24),256-min(256,time*24)');ctl(190,'Arrival step','VelSet','time=[0,12]',x=5);ctl(190,'Settle','VelSet','time=13',x=0);end(190)
state(191,191);end(191)
state(500,500,velset='0,0');ctl(500,'Gather','PowerAdd',value=10);ctl(500,'Charge threads','Explod','time%16=0',anim=7009,pos='0,-190',scale='.22,.35',removetime=15,sprpriority=2,ownpal=1);ctl(500,'Release','ChangeState','command!="hold_charge" || power>=3000',value=0,ctrl=1)
state(1000,1000,move='A',velset='0,0',poweradd=-250)
ctl(1000,'Cooldown','VarSet','time=0',**{'var(11)':90})
ctl(1000,'Snare','Helper','time=6',name='Silk snare',ID=8100,stateno=8100,postype='p1',pos='200,0',ownpal=1,keyctrl=0);end(1000)
state(8100,7010,move='A',velset='0,0')
ctl(8100,'Thread footprint','AngleDraw',scale='1,1')
# Ground strip is centered at y=650 in its 720px image.
ctl(8100,'Trap drawing','Offset',y=-290)
hit(8100,1,35,guard='L',attr='S,SP',pausetime='0,0',ground__hittime=45,ground__velocity=0,getpower='0,0',givepower='0,0')
ctl(8100,'Expire','DestroySelf','time>=160 || movecontact || root,stateno=99000 || root,life<=0')
def projectile(n,t,damage,offset='110,-180',speed=17):
    ctl(n,'Hidden dagger','Projectile',f'time={t}',projid=n,projanim=7005,projhitanim=-1,projremanim=-1,projremove=1,projremovetime=65,velocity=f'{speed},0',offset=offset,attr='S,SP',damage=f'{damage},3',guardflag='MA',hitflag='MAF',pausetime='0,5',ground__type='High',ground__hittime=18,ground__velocity=-2,air__velocity='-3,-3',getpower='0,0',givepower='10,0',hitsound='S0,0')
state(1100,1100,move='A',poweradd=-500,velset='0,0')
for t,y in [(8,-240),(16,-180),(24,-120)]:
    projectile(1100,t,35,f'100,{y}')
    ctl(1100,'Release whistle','PlaySnd',f'time={t}',value='0,0')
end(1100)
for n,cost,duration,speed in [(1200,500,24,15),(1300,0,28,-10)]:
    state(n,n,velset='0,0',poweradd=-cost)
    ctl(n,'Cooldown','VarSet','time=0',**{'var(10)':60})
    ctl(n,'Silent motion','VelSet',f'time=[4,{duration-9}]',x=speed)
    ctl(n,'Stop','VelSet',f'time>={duration-8}',x=0)
    ctl(n,'Brief evasion','NotHitBy','time=[6,12]',value='SCA',time=1)
    ctl(n,'Fade','Trans','time=[4,17]',trans='addalpha',alpha='100,156')
    ctl(n,'Pass through','PlayerPush','time=[4,17]',value=0)
    ctl(n,'Motion trail','AfterImage','time=4',time=15,length=6,timegap=2,framegap=2,palcolor=0,palbright='16,20,30',palcontrast='160,170,200',trans='add')
    ctl(n,'Recover','ChangeState',f'time>={duration}',value=0,ctrl=1)
for n,cost,nextstate in [(1120,500,1121),(3200,2000,3201),(4000,3000,4001)]:
    state(n,n,move='A',velset='0,0',poweradd=-cost)
    hit(n,10,10,attr='S,HA' if n>=3000 else 'S,SA',pausetime='0,0',sparkno='S7111',p1stateno=nextstate,p2stateno=8250,getpower='0,0',givepower='0,0',ground__velocity=0,fall=0)
    spawn_silk(ctl,n,10,3 if n==3200 else 1);end(n)
state(3000,3000,move='A',poweradd=-1000,velset='0,0')
ctl(3000,'Super beat','SuperPause','time=0',time=10,movetime=10,anim=-1,sound='S0,4',darken=1,poweradd=0)
for t in [10,19,28]:
    hit(3000,t,65,attr='S,HA',pausetime='0,5',sparkno='S7111',ground__velocity=0,getpower='0,0',givepower='10,0')
    ctl(3000,'Cut snap','PlaySnd',f'time={t}',value='0,0')
ctl(3000,'Contact weight','EnvShake','movehit=1',time=5,freq=90,ampl=3)
spawn_silk(ctl,3000,10)
# active collision for all three plucks
act(3000,[('m13',16),('c11',8),('c1',10),('c2',10),('m0',20)],active=(1,2,3),attack=(0,-360,550,-10))
ctl(3000,'Recover','ChangeState','time>=48',value=0,ctrl=1)
state(3100,3100,move='A',poweradd=-1500,velset='0,0')
ctl(3100,'Super beat','SuperPause','time=0',time=10,movetime=10,anim=-1,sound='S0,4',darken=1,poweradd=0)
for i,t in enumerate([10,12,13,18,20]):
    projectile(3100,t,50,f'100,{-280+i*35}',24)
    ctl(3100,'Dagger rush','PlaySnd',f'time={t}',value='0,0')
ctl(3100,'Recover','ChangeState','time>=52',value=0,ctrl=1)
for n,duration,total in [(1121,48,110),(3201,100,290),(4001,156,470)]:
    state(n,n,move='A',velset='0,0')
    if n==4001:ctl(n,'Center composition','PosSet','time=0',x='-120*facing',y=0)
    ctl(n,'Scene root','VarSet','time=0',**{'var(21)':'pos x'})
    ctl(n,'Scene facing','VarSet','time=0',**{'var(22)':'facing'})
    # Keep the opponent fixed in world space while the assassin passes behind.
    impact_x='((var(21)+240*var(22))-pos x)*facing'
    ctl(n,'Protected choreography','NotHitBy','1',value='SCA',time=1)
    spawn_silk(ctl,n,0,3 if n==3201 else 1)
    if n==4001:
        ctl(n,'Ink silence','Explod','time=0',anim=7006,ID=7006,postype='left',pos='0,0',bindtime=-1,removetime=duration-8,sprpriority=-2,ownpal=1)
        ctl(n,'Cold glance','Explod','time=0',anim=7110,ID=7110,postype='left',pos='0,0',bindtime=-1,removetime=8,sprpriority=6,ownpal=1)
        ctl(n,'Single unseen pass','PosSet','time=60',x='var(21)+360*var(22)')
        ctl(n,'Face victim','Turn','time=60')
        ctl(n,'Unseen step','Trans','time=[60,62]',trans='addalpha',alpha='0,256')
        ctl(n,'Cloth pass','PlaySnd','time=60',value='0,4',volumescale=45)
    ctl(n,'Hold opponent','TargetBind',f'time<{duration-10}',time=1,pos=impact_x+',0')
    pulses=[8,18] if n==1121 else [20,28,40,48,74] if n==3201 else []
    amount=40 if n==1121 else 40 if n==3201 else 50
    for t in pulses:
        ctl(n,'Thread damage','TargetLifeAdd',f'time={t}',value=-amount,kill=0,absolute=1)
        ctl(n,'Fine cut','Explod',f'time={t}',anim=7111,pos=impact_x+',-180',removetime=4,sprpriority=4,ownpal=1)
        ctl(n,'Cut sound','PlaySnd',f'time={t}',value='0,0')
        ctl(n,'Cut impact','EnvShake',f'time={t}',time=4,freq=95,ampl=3)
    finish=132 if n==4001 else duration-20
    ctl(n,'Final thread','TargetLifeAdd',f'time={finish}',value=-(total-amount*len(pulses)),kill=1,absolute=1)
    ctl(n,'Closing cut','Explod',f'time={finish}',anim=7111,pos=impact_x+',-190',removetime=4,sprpriority=4,ownpal=1)
    ctl(n,'Final weight','EnvShake',f'time={finish}',time=2 if n==4001 else 5,freq=80,ampl=1 if n==4001 else 3)
    ctl(n,'Final impact','PlaySnd',f'time={finish}',value='0,0' if n==4001 else '0,3',volumescale=60 if n==4001 else 100)
    ctl(n,'Release','TargetState',f'time={138 if n==4001 else duration-10}',value=8260)
    ctl(n,'Recover','ChangeState',f'time>={duration}',value=0,ctrl=1)
state(8250,move='H',velset='0,0')
ctl(8250,'Victim own proportions','ChangeAnim','time=0',value=5000)
ctl(8250,'Quiet stillness','ChangeAnim',['(enemynear,stateno)=4001','(enemynear,time)<132','anim!=0'],value=0)
ctl(8250,'Finish reaction','ChangeAnim',['(enemynear,stateno)=4001','(enemynear,time)>=132','anim!=5000'],value=5000)
ctl(8250,'Protected','NotHitBy',value='SCA',time=1)
ctl(8250,'Escape safety','SelfState','time>=340',value=0,ctrl=1)
state(8260,kind='L',move='H',velset='0,0');ctl(8260,'Own knockdown','ChangeAnim','time=0',value='ifelse(selfanimexist(5110),5110,5000)');ctl(8260,'Ground','PosSet',y=0);ctl(8260,'Get up','SelfState','time>=18',value=5120)
author_sequences(A,NORMALS)
author_silk(A)
write_silk_states(A,state,ctl)
(O/'pyowol.cns').write_text(namespace['cns'],encoding='utf-8')
write_audio(O/'pyowol.snd')
# Replace the earlier duplicate super action with its final collision sequence.
import re
air='\n'.join(A.air)+'\n';blocks=re.split(r'(?=\[Begin Action )',air);seen=set();kept=[]
for b in reversed(blocks):
    m=re.match(r'\[Begin Action (\d+)\]',b)
    if m and m[1] in seen:continue
    if m:seen.add(m[1])
    kept.append(b)
final_air=''.join(reversed(kept))
(O/'pyowol.air').write_text(final_air,encoding='utf-8')
export_player(A,final_air)
commands={'L':'a','M':'b','H':'c','snare':'~x','daggers':'/$F, ~x','reel':'/$B, ~x','step':'/$D, ~x','super':'~y','rain':'/$B, ~y','prison':'/$F, ~y','ultimate':'~z','veil':'~w','hold_charge':'/s','holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=15\ncommand.buffer.time=6\n'
for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={15 if "," in keys else 1}\n'
cmd+='\n[Statedef -1]\n'
def route(name,n,conditions):
    global cmd
    cmd+=f'\n[State -1, {name}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions)+f'\ntrigger1=command="{name}"\nvalue={n}\nctrl=0\n'
g=['roundstate=2','ctrl','statetype!=A','ailevel=0']
cancel='(movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420]))'
for name,n,cost in [('ultimate',4000,3000),('prison',3200,2000),('rain',3100,1500),('super',3000,1000),('step',1200,500),('daggers',1100,500),('reel',1120,500),('snare',1000,250),('veil',1300,0),('hold_charge',500,0)]:
    special_g=[g[0],f'(ctrl || {cancel})',*g[2:]] if n!=500 else g
    route(name,n,special_g+[f'power>={cost}']+(['numhelper(8100)=0','var(11)=0'] if n==1000 else ['var(10)=0'] if n in (1200,1300) else ['power<3000'] if n==500 else []))
for name,n in [('H',620),('M',610),('L',600)]:route(name,n,['roundstate=2','ctrl','statetype=A','ailevel=0'])
for name,n in [('H',420),('M',410),('L',400)]:
    permission='ctrl' if n==400 else f'(ctrl || (movecontact && time>=8 && stateno={400 if n==410 else 410}))'
    route(name,n,[g[0],permission,*g[2:],'command="holddown"'])
for name,n in [('H',220),('M',210),('L',200)]:
    permission='ctrl' if n==200 else f'(ctrl || (movecontact && time>=8 && stateno={200 if n==210 else 210}))'
    route(name,n,[g[0],permission,*g[2:]])
for name,n,extra in [('holddown',10,'stateno!=10'),('holdup',40,'1'),('holdfwd',20,'stateno=0'),('holdback',21,'stateno=0')]:route(name,n,g+[extra])
for n,conditions in [(4000,['power>=3000','p2bodydist x<230','random<15']),(3000,['power>=1000','p2bodydist x<330','random<30']),(210,['p2bodydist x<200','random<65']),(1100,['power>=500','p2bodydist x>220','numproj=0','random<25']),(20,['stateno=0','p2bodydist x>160'])]:
    cmd+=f'\n[State -1, CPU]\ntype=ChangeState\ntriggerall=roundstate=2\ntriggerall=ctrl\ntriggerall=statetype!=A\ntriggerall=ailevel>0\n'+''.join(f'triggerall={x}\n' for x in conditions)+'trigger1=1\n'+f'value={n}\nctrl=0\n'
(O/'pyowol.cmd').write_text(cmd,encoding='utf-8')
# Publish editable sources alongside the installed runtime.
for path in O.glob('pyowol.*'):
    if path.suffix!='.sff' and path.suffix!='.snd':shutil.copy2(path,S/path.name)
report={'character':'Pyo Wol','poses':A.meta,'normal_moves':[dict(state=n,name=name,kind=kind) for n,name,p,start,d,kind in NORMALS],'animation_version':5,'effects_version':6,'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.glob('pyowol.*')}}
(S/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('PYO_WOL_BUILT',len(A.meta),'original PNG sprites')
