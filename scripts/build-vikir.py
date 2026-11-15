"""Original manhwa-only Vikir adaptation. Common locomotion, authored sword combat."""
from pathlib import Path
import hashlib,json,struct,shutil,re
from PIL import Image,ImageDraw
from fighter_assets import FighterAssets
from isolated_sprite_atlas import extract
ROOT=Path(__file__).resolve().parents[1]
A=FighterAssets(ROOT,'vikir');S=A.source;O=A.output;ART=next(S/('art/'+v) for v in ['v3','v2','v1'] if v=='v1' or (S/('art/'+v+'/ready.json')).exists())
layout=json.loads((ART/'ready.json').read_text()) if (ART/'ready.json').exists() else {}
(ART/'poses').mkdir(exist_ok=True)
# Foot roots are registered to the body, never to the centre of a long sword.
anchors_m=[(205,292),(605,291),(1010,289),(1405,289),(190,506),(565,514),(974,511),(1360,510),(185,752),(555,739),(952,724),(1350,716),(210,998),(565,1015),(960,1017),(1350,1017)]
anchors_c=[(185,273),(535,267),(953,275),(1315,280),(205,519),(595,542),(970,536),(1350,528),(185,723),(560,734),(966,716),(1360,739),(168,1008),(580,976),(954,1006),(1325,1009)]
def axis(x,y):
    h=list(struct.unpack('<HHHHhhHBBIIHH',A.headers[-1]));h[4:6]=[int(x),int(y)];A.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*h)
banks=[(0,'movement','m',0,anchors_m),(0,'combat','c',3,anchors_c),(1,'night-movement','n',0,anchors_m),(1,'night-combat-v2','k',3,anchors_c),(2,'choco','d',0,None)]
if ART.name=='v3':banks += [(3,'school-movement','a',0,None),(3,'school-combat','b',3,None),(4,'power','p',7,None),(5,'night-power','r',7,None),(6,'school-power','s',7,None)]
for bank,sheet,prefix,ref,roots in banks:
    source=ART/f'{sheet}.png'
    if not source.exists():source=S/'art/v1'/f'{sheet}.png'
    tiles=extract(source,4,3 if bank==2 else 4,layout.get('separation_threshold',{}).get(sheet,48))
    scale=(110 if bank==2 else 375)/tiles[ref][0].height
    for i,(im,bounds) in enumerate(tiles):
        p=ART/f'poses/{prefix}{i}.png';im.save(p);key=f'{prefix}{i}'
        A.png(key,p,110 if bank==2 else 375,i+(16 if prefix in ('c','k','b') else 0),50+bank)
        if roots or sheet in layout:
            # Night edits preserve pose placements; use the exact foot baseline
            # from each extracted drawing (weapon tips are hand-traced below).
            rootx,rooty=layout.get(sheet,roots)[i]
            if prefix=='n':rooty=bounds[3]
            if prefix=='k':rooty=bounds[3]
            root=(rootx-bounds[0],rooty-bounds[1])
        else:root=(im.width*.56,im.height)
        axis(*root);A.meta[key].update(axis=list(map(int,root)),scale=scale,bank=sheet,source_bounds=bounds)
# Padded square portraits are compiled at the HUD's native source size.
portrait=Image.open(ART/'portrait.png').convert('RGBA');portrait=portrait.crop(portrait.getchannel('A').getbbox())
for number,size in [(0,200),(1,900)]:
    p=ART/f'portrait-{size}.png';im=Image.new('RGBA',(size,size));fit=portrait.copy()
    if number==0 and layout:
        # The small HUD needs a face crop; the selection portrait keeps the art.
        w,h=fit.size;fit=fit.crop((int(w*.13),0,int(w*.74),int(h*.40)))
    fit.thumbnail((int(size*.80),int(size*.80)),Image.Resampling.LANCZOS);im.alpha_composite(fit,((size-fit.width)//2,(size-fit.height)//2));im.save(p)
    A.png('portrait'+str(number),p,size,number,9000);axis(0,0);A.meta['portrait'+str(number)]['axis']=[0,0]
A.alias(0,0,'m0');A.alias(0,3,'m0')
clips={}
import vikir_guests as guests
has_guests=guests.load_art(A,axis,clips)
import vikir_presentation as presentation
presentation.calibrate(A)
presentation.load_fx(A,axis)
for clip in clips.values():
    for frame in clip["frames"]:frame.update(A.meta[frame["key"]])
def action(n,frames,active=(),kind='S',attack=(20,-300,260,-100),hurt=True,name=None):
    for bank in ([0,1,3] if ART.name=='v3' else [0,1]):
        remap={0:{},1:{'m':'n','c':'k','p':'r'},3:{'m':'a','c':'b','p':'s'}}[bank]
        frames=[('m0' if k in ('c3','p7','p11') else k,t) for k,t in frames]
        fs=[(remap.get(k[0],k[0])+k[1:],t) for k,t in frames]
        A.action(n+bank*10000,fs,active,kind,attack,hurt)
        clips[str(n+bank*10000)]=dict(name=name or str(n),form=bank,frames=[dict(key=k,ticks=t,**A.meta[k]) for k,t in fs])
common={0:[('m0',-1)],5:[('m0',-1)],10:[('m4',-1)],11:[('m4',5)],12:[('m0',5)],20:[('m2',6),('m3',6)],21:[('m3',7),('m2',7)],22:[('m2',4),('m0',4)],40:[('m5',4)],41:[('m6',5)],42:[('m6',5)],43:[('m7',5)],47:[('m4',5)],52:[('m4',5)]}
for n,fs in common.items():action(n,fs,kind='C' if n in (10,11) else 'A' if n in (41,42,43) else 'S')
for n in list(range(120,123))+list(range(130,134))+list(range(140,144))+list(range(150,157)):action(n,[('m8',6)])
for n in [170,175,5100,5110,5140,5150,5160,5170]:action(n,[('m11',-1)],hurt=False)
for n in [180,181,195]:action(n,[('m15',50)])
action(190,[('m14',24),('m13',18),('m0',18)])
action(191,[('m0',1)])
for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090,820,821]:action(n,[('m9' if n<5030 else 'm10',-1)])
action(5120,[('m11',6),('m12',12),('m0',6)])
for n in [5200,5210,5220,5300,5500,5510]:action(n,[('m7',8),('m0',8)])
NORMALS=[(200,'Fang Thrust','S',6,34,1),(210,'Cross Fang','S',9,55,2),(220,'Descending Fang','S',13,82,7),(400,'Low Fang','C',6,30,8),(410,'Low Lunge','C',9,50,9),(420,'Rising Fang','C',12,76,5),(600,'Air Fang','A',6,34,10),(610,'Air Cross','A',9,52,10),(620,'Descending Bite','A',12,75,11)]
for n,name,kind,start,damage,pose in NORMALS:
    rest='m7' if kind=='A' else 'm4' if kind=='C' else 'm0'
    prep='m7' if kind=='A' else 'c4' if kind=='C' else 'c6' if n==220 else 'c0' if n==210 else 'c3'
    box=(15,-140,265,-15) if kind=='C' and n!=420 else (15,-345,285,-70)
    follow='c11' if kind=='A' else 'c8' if kind=='C' and n!=420 else 'c3' if n in (220,420) else 'c2' if n==200 else 'c3'
    action(n,[(prep,start),(f'c{pose}',5),(follow,7),(rest,9 if n%100<20 else 16)],(1,),kind,box,name=name)
power_clips={
 3000:([('p0',10),('p1',4),('p2',4),('p3',4),('p4',4),('p5',4),('p6',4),('p7',16)],(1,3,6)),
 3100:([('p8',12),('p9',8),('p10',12),('p11',20)],(1,)),
 4000:([('p0',20),('p1',4),('p2',4),('p3',4),('p4',4),('p6',4),('p2',4),('p12',4),('p14',4),('p13',4),('p4',4),('p14',4),('p2',4),('p15',6),('p11',24)],(1,3,5,7,9,11,13))
} if ART.name=='v3' else {}
for n,name,frames,active,box in [
 (500,'Charge',[('m13',12),('c12',12)],(),(0,0,0,0)),
 (700,'Change appearance',[('m14',8),('m13',6),('m0',10)],(),(0,0,0,0)),
 (710,'Return to Vikir',[('m14',8),('m0',12)],(),(0,0,0,0)),
 (800,'Sword Aura',[('c12',16),('m13',16),('m0',12)],(),(0,0,0,0)),
 (1000,'Hound Lunge',[('c4',8),('c9',7),('c2',6),('c3',14)],(1,2),(15,-300,320,-90)),
 (1100,'Rising Hunt',[('c4',10),('c5',7),('c6',7),('m0',18)],(1,2),(0,-400,270,-35)),
 (1200,'Silent Retreat',[('m8',4),('c13',8),('m0',14)],(),(0,0,0,0)),
 (3000,'Three Fangs',[('c0',10),('c1',6),('c2',6),('c6',7),('c7',8),('m0',18)],(1,2,3),(15,-340,330,-60)),
 (3100,'Beelzebub Blood Draw',[('c12',12),('c9',8),('c2',7),('c15',20)],(1,2),(15,-300,340,-80)),
 (4000,'Seven Fangs',[('c12',20),('c9',6),('c2',6),('c5',6),('c6',6),('c10',6),('c14',6),('c1',7),('c15',24)],tuple(range(1,8)),(10,-350,380,-40)),
 (1300,'Quickstep',[('c4',4),('c13',9),('m0',13)],(),(0,0,0,0))]:
    if n in power_clips:frames,active=power_clips[n]
    action(n,frames,active,attack=box,name=name)
action(4500,[('p0',24),('p1',6),('p2',6),('p0',16)],(1,),attack=(0,-355,400,0),name='Night Hound: Crimson Execution - opening')
execution=[('p0',16)]+[(k,3) for k in ['p1','p3','p6','p12','p13']*4]+[('p12',12),('p15',8),('m0',28)]
action(4510,execution,tuple(range(1,21))+(22,),attack=(0,-355,420,0),name='Night Hound: Crimson Execution')
if has_guests:
    for n,name in zip(guests.STATES,guests.NAMES):action(n,[('m13',18),('m0',46)],name=name+' Guest')
# Choco has a real small collision body. Sword inputs return to human first.
dogmap={0:[(0,10),(1,10)],5:[(0,10),(1,10)],10:[(4,-1)],11:[(4,5)],12:[(0,5)],20:[(2,5),(3,5)],21:[(3,6),(2,6)],22:[(0,6)],40:[(4,4)],41:[(5,6)],42:[(5,6)],43:[(6,6)],47:[(4,5)],52:[(4,5)],500:[(10,10),(1,10)],700:[(11,10),(0,14)],710:[(11,8),(0,12)],1200:[(4,4),(7,10),(0,12)],1300:[(4,4),(7,9),(0,13)]}
dogmap[0]=dogmap[5]=[(0,-1)]
if has_guests:
    for n in guests.STATES:dogmap[n]=[(10,18),(1,34),(0,12)]
for n in list(range(120,123))+list(range(130,134))+list(range(140,144))+list(range(150,157)):dogmap[n]=[(4,6)]
for n in [170,175,180,181,190,191,195,5100,5110,5140,5150,5160,5170]:dogmap[n]=[(9,-1 if n>=5000 or n in (170,175) else 60)]
for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090,820,821]:dogmap[n]=[(8,-1)]
dogmap[5120]=[(9,6),(10,12),(0,6)]
for n in [5200,5210,5220,5300,5500,5510]:dogmap[n]=[(6,8),(0,8)]
for n,frames in dogmap.items():
    A.air.append(f'\n[Begin Action {20000+n}]')
    for pose,t in frames:
        m=A.meta[f'd{pose}'];sc=m['scale'];A.air.extend(['Clsn2: 1','Clsn2[0] = -55,-100,60,0',f'52,{pose},0,0,{t},,,{sc:.7f},{sc:.7f}'])
    clips[str(20000+n)]=dict(name=str(n),form=2,frames=[dict(key=f'd{i}',ticks=t,**A.meta[f'd{i}']) for i,t in frames])
A.write_sff('vikir.sff');A.write_air('vikir.air')
# Original procedural sword/impact audio only; no borrowed character voices.
from pyowol_animation import write_audio
write_audio(O/'vikir.snd')
(O/'vikir.def').write_text('[Info]\nname="Vikir van Baskerville"\ndisplayname="Vikir"\nauthor="Game1 original fan adaptation"\nmugenversion=1.1\nlocalcoord=1280,720\nportraitscale=.125\n[Files]\ncmd=vikir.cmd\ncns=vikir.cns\nst=vikir.cns\nstcommon=common1.cns.zss\nsprite=vikir.sff\nanim=vikir.air\nsound=vikir.snd\n[Arcade]\n',encoding='utf-8')
template=(ROOT/'scripts/build-yamal-combat.py').read_text(encoding='utf-8');ns={}
exec(template[template.index("cns='''[Data]"):template.index('state(-2)')],ns)
state,ctl,end,hit=[ns[k] for k in ('state','ctl','end','hit')]
base_state=state
ns['base_state']=base_state
def state(number,anim=None,**params):
    if anim is not None:
        # Select the outfit on entry, before the first frame is drawn. A -2
        # remap alone runs too early and flashes the base outfit for one tick.
        anim=f'{anim}+10000*ifelse(map(vikir.form)=2 && !selfanimexist({anim+20000}),0,map(vikir.form))'
    base_state(number,anim,**params)
ns['state']=state
state(-2)
ctl(-2,'Face opponent','Turn',['ctrl','statetype!=A','p2dist x<0'])
ctl(-2,'Authored movement','AssertSpecial',flag='nowalk',flag2='nobrake',flag3='noautoturn')
ctl(-2,'Aura duration','VarAdd','var(20)>0',**{'var(20)':-1})
ctl(-2,'Aura bonus','AttackMulSet',value='ifelse(var(20)>0,1.12,1)')
ctl(-2,'Clear aura on KO','VarSet','life<=0',**{'var(20)':0})
ctl(-2,'Reset disguise each round','MapSet','roundstate=0',map='"vikir.form"',value=0)
ctl(-2,'Reset aura each round','VarSet','roundstate=0',**{'var(20)':0})
ctl(-2,'Night Hound art','ChangeAnim',['map(vikir.form)=1','anim<10000','selfanimexist(anim+10000)'],value='anim+10000',elem='animelemno(0)')
ctl(-2,'Choco art','ChangeAnim',['map(vikir.form)=2','anim<20000','selfanimexist((anim%10000)+20000)'],value='(anim%10000)+20000',elem='animelemno(0)')
ctl(-2,'Unmasked art','ChangeAnim',['map(vikir.form)=0','anim>=10000','selfanimexist(anim%10000)'],value='anim%10000',elem='animelemno(0)')
ctl(-2,'Disguise from Choco','ChangeAnim',['map(vikir.form)=1','anim>=20000','selfanimexist((anim%10000)+10000)'],value='(anim%10000)+10000',elem='animelemno(0)')
if ART.name=='v3':ctl(-2,'Academy art','ChangeAnim',['map(vikir.form)=3','anim<30000','selfanimexist((anim%10000)+30000)'],value='(anim%10000)+30000',elem='animelemno(0)')
ctl(-2,'Size matches form','Width',edge='ifelse(map(vikir.form)=2,38,45),ifelse(map(vikir.form)=2,38,45)',player='ifelse(map(vikir.form)=2,38,45),ifelse(map(vikir.form)=2,38,45)')
if has_guests:guests.tick(ctl)
ctl(-2,'Release charge ring','RemoveExplod','stateno!=500',ID=8050)
for effect in [8010,8020,8030]:ctl(-2,'Clean interrupted cinematic','RemoveExplod','stateno!=4500 && stateno!=4510',ID=effect)
movement=template[template.index('state(0,0,velset='):template.index('for number,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():')]
movement=movement.replace("'anim!=42'","'anim%10000!=42'").replace("'anim!=43'","'anim%10000!=43'")
movement=movement.replace('value=42)',"value='42+10000*map(vikir.form)')").replace('value=43)',"value='43+10000*map(vikir.form)')")
exec(movement,ns)
for n,name,kind,start,damage,pose in NORMALS:
    state(n,n,kind=kind,move='A',**({} if kind=='A' else {'velset':'0,0'}))
    ctl(n,'Human sword body','MapSet','time=0',map='"vikir.form"',value='ifelse(map(vikir.form)=2,0,map(vikir.form))')
    hit(n,start,damage,kind,guard='H' if kind=='A' else 'L' if kind=='C' and n!=420 else 'MA',fall=n in (220,420,620),hitsound='S0,0',pausetime='4,7',sparkxy='-10,-190')
    ctl(n,'Sword whoosh','PlaySnd',f'time={start-1}',value='0,0')
    if kind=='A':ctl(n,'Gravity','VelAdd',y=.65);ctl(n,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
    else:
        ctl(n,'Sword step','VelSet',f'time=[{start-2},{start+2}]',x=3 if n%100<20 else 5)
        ctl(n,'Plant feet','VelSet',f'time={start+3}',x=0)
    end(n,kind=='A',kind=='C')
state(190,190,velset='0,0');ctl(190,'Intro','AssertSpecial','time<52',flag='intro');end(190)
state(191,191);end(191)
state(500,500,velset='0,0');presentation.charge(ctl);ctl(500,'Gather power','PowerAdd',value=10);ctl(500,'Release','ChangeState','command!="hold_charge" || power>=3000',value=0,ctrl=1)
for n in (700,710):
    state(n,n,velset='0,0');ctl(n,'Change form','MapSet','time=8',map='"vikir.form"',value=f'(map(vikir.form)+1)%{4 if ART.name=="v3" else 3}' if n==700 else 0);ctl(n,'Mask sound','PlaySnd','time=8',value='0,4',volumescale=40);end(n)
state(800,800,velset='0,0',poweradd=-1000);ctl(800,'Return to swordsman','MapSet','time=0',map='"vikir.form"',value='ifelse(map(vikir.form)=2,0,map(vikir.form))');ctl(800,'Sword aura','VarSet','time=16',**{'var(20)':600});end(800)
for n,cost,starts,damage in [(1000,250,[8],75),(1100,500,[10],100),(3000,1000,[10,16,22],62),(3100,1500,[12],165),(4000,2000,[20,26,32,38,44,50,56],44)]:
    if n in power_clips:
        fs,active=power_clips[n];starts=[sum(t for _,t in fs[:i]) for i in active]
    state(n,n,move='A',poweradd=-cost,velset='0,0')
    ctl(n,'Human sword body','MapSet','time=0',map='"vikir.form"',value='ifelse(map(vikir.form)=2,0,map(vikir.form))')
    if n>=3000:ctl(n,'Super pause','SuperPause','time=0',time=10,movetime=10,anim=-1,sound='S0,4',darken=1,poweradd=0)
    for t in starts:
        hit(n,t,damage,attr='S,HA' if n>=3000 else 'S,SA',pausetime='0,5' if n>=3000 else '4,7',ground__hittime=28,ground__velocity='-2,-4' if n==1100 or n==4000 and t==starts[-1] else 0,air__velocity='-2,-3',fall=int(n==1100 or n==4000 and t==starts[-1]),getpower='0,0',hitsound='S0,0')
        ctl(n,'Blade sound','PlaySnd',f'time={t}',value='0,0')
    if n in (1000,4000):
        ctl(n,'Drive forward','VelSet',f'time=[{starts[0]-3},{starts[-1]+3}]',x=13 if n==1000 else 4)
        ctl(n,'Stop','VelSet',f'time={starts[-1]+4}',x=0)
    if n==3100:
        ctl(n,'Blood draw on confirmed contact','LifeAdd','movehit=1',value=55,absolute=1)
    ctl(n,'Cut impact','EnvShake','movehit=1',time=4,freq=90,ampl=2 if n<3000 else 3)
    end(n)
for n,speed in [(1200,-13),(1300,15)]:
    state(n,n,velset='0,0');ctl(n,'Step','VelSet','time=[4,12]',x=speed);ctl(n,'Plant','VelSet','time=13',x=0)
    ctl(n,'Brief evasion','NotHitBy','time=[5,8]',value='SCA',time=1);ctl(n,'Pass through','PlayerPush','time=[4,12]',value=0);end(n)
if has_guests:guests.states(ns,state,ctl,end)
presentation.states(state,ctl,end,hit)
(O/'vikir.cns').write_text(ns['cns'],encoding='utf-8')
commands={'L':'a','M':'b','H':'c','skill':'x','rise':'x','retreat':'x','super':'y','drain':'y','aura':'y','ultimate':'z','seven':'y+z','form':'d','base':'d','step':'w','hold_charge':'/s','holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
if has_guests:commands.update(guest_dolores='y',guest_camu='z',guest_aiyen='z',guest_sinclair='z',bow='x')
cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=15\ncommand.buffer.time=4\n'
for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=1\n'
cmd+='\n[Statedef -1]\n'
def route(name,n,conditions):
    global cmd
    cmd+=f'\n[State -1, {name}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions)+f'trigger1=command="{name}"\nvalue={n}\nctrl=0\n'
g=['roundstate=2','ctrl','statetype!=A','ailevel=0']
route('seven',4000,g+['power>=2000','command!="holddown"','command!="holdback"','command!="holdfwd"'])
if has_guests:guests.routes(route,g)
for name,n,cost in [('base',710,0),('form',700,0),('ultimate',4500,3000),('aura',800,1000),('drain',3100,1500),('super',3000,1000),('rise',1100,500),('retreat',1200,0),('skill',1000,250),('step',1300,0),('hold_charge',500,0)]:
    permission='(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))' if n in (1000,1100,3000,3100,4000,4500) else 'ctrl'
    modifiers={'base':['command="holddown"'],'form':['command!="holddown"'],'rise':['command="holddown"'],'retreat':['command="holdback"','command!="holddown"'],'skill':['command!="holddown"','command!="holdback"'],'aura':['command="holddown"'],'drain':['command="holdback"','command!="holddown"'],'super':['command!="holddown"','command!="holdback"']}
    if has_guests:
        modifiers['super']+=['command!="holdfwd"']
        modifiers['ultimate']=['command!="holdfwd"','command!="holdback"','command!="holddown"']
        modifiers['skill']+=['map(vikir.form)!=3 || command!="holdfwd"']
    # Direct command assertions in native tests also supply their real modifiers.
    route(name,n,[g[0],permission,*g[2:],f'power>={cost}',*modifiers.get(name,[])]+(['power<3000'] if n==500 else ['var(20)=0'] if n==800 else []))
for name,n in [('H',620),('M',610),('L',600)]:route(name,n,['roundstate=2','ctrl','statetype=A','ailevel=0'])
for crouch in [True,False]:
    for name,n in [('H',420 if crouch else 220),('M',410 if crouch else 210),('L',400 if crouch else 200)]:
        prev=n-10;permission='ctrl' if name=='L' else f'(ctrl || (movecontact && time>=8 && stateno={prev}))'
        route(name,n,[g[0],permission,*g[2:]]+(['command="holddown"'] if crouch else []))
for name,n,extra in [('holddown',10,'stateno!=10'),('holdup',40,'1'),('holdfwd',20,'stateno=0'),('holdback',21,'stateno=0')]:route(name,n,g+[extra])
for n,conditions in [(4500,['power>=3000','p2bodydist x<260','random<14']),(3000,['power>=1000','p2bodydist x<200','random<24']),(1000,['power>=250','p2bodydist x=[160,350]','random<35']),(210,['p2bodydist x<150','random<60']),(20,['stateno=0','p2bodydist x>150'])]:
    cmd+='\n[State -1, CPU]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in ['roundstate=2','ctrl','statetype!=A','ailevel>0',*conditions])+f'trigger1=1\nvalue={n}\nctrl=0\n'
(O/'vikir.cmd').write_text(cmd,encoding='utf-8')
for path in O.glob('vikir.*'):
    if path.suffix in ('.cmd','.cns','.def','.air'):shutil.copy2(path,S/path.name)
report=dict(character='Vikir van Baskerville',forms=['Vikir','Night Hound disguise','Choco']+(['Academy'] if ART.name=='v3' else []),scope='Manhwa appearances; attacks and balance are a fan game adaptation',poses=A.meta,power_clips={str(n):dict(hit_ticks=[sum(t for _,t in fs[:i]) for i in active],active_frames=list(active)) for n,(fs,active) in power_clips.items()},normal_moves=[dict(state=n,name=name,kind=kind) for n,name,kind,*_ in NORMALS],moves={n:clips[str(n)]['name'] for n in (500,700,710,800,1000,1100,1200,1300,3000,3100,4000,4500,4510)},runtime_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.glob('vikir.*')})
report.update(ultimate=dict(name='Night Hound: Crimson Execution',opener=4500,confirmed=4510,cost=3000,hit_count=22),super_seven_fangs=dict(state=4000,cost=2000,command='S+D'))
if has_guests:report.update(guests=[dict(name=name,state=n,cost=cost,cooldown=360) for name,n,cost in zip(guests.NAMES,guests.STATES,guests.COSTS)],archery=dict(state=1400,form=3,release_tick=28,damage=82,projectile=7140,frames=4,color='crimson'))
(S/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(S/'animation-data.js').write_text('window.VIKIR_ANIMATION='+json.dumps(clips)+';',encoding='utf-8')
provenance={p.name:dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),prompt=p.with_suffix('.prompt.txt').name) for p in ART.glob('*.png') if p.with_suffix('.prompt.txt').exists()}
(ART/'provenance.json').write_text(json.dumps(dict(generator='Built-in imagegen',assets=provenance),indent=2),encoding='utf-8')
print('VIKIR_BUILT',len(A.meta),'sprites;',len(clips),'actions')
