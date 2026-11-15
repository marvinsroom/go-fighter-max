"""Character-specific profiles and native combat for the new manhwa fighters."""
from pathlib import Path
import json
from baam_model import Author as BaseAuthor,NORMALS,LINKS
from baam_combat_v3 import author_techniques,powerfx

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
PROFILES={
 'jin-mu-won':dict(id='jin_mu_won',name='Jin Mu-Won',capture='JinMuWon',series='The Legend of the Northern Blade',credits='Woogack / HAE MIN / Seoul Media',source='https://www.tappytoon.com/en/book/legend-of-northern-blade',moves=['Drawing Cut','Silent Step','Snow Flower Reversal','Shadow Crescent','Northern Threefold','Iron Wall','Black Horizon','Ten Thousand Shadows'],ultimate=600,taunt='Quiet Resolve',description='Snow Flower swordsmanship, decisive draw cuts, shadow crescents and the Ten Thousand Shadows cinematic.'),
 'lloyd':dict(id='lloyd',name='Lloyd Frontera',capture='Lloyd',series='The Greatest Estate Developer',credits='BK_Moon / Lee Hyun Min / Kim Hyunsoo',source='https://www.webtoons.com/en/fantasy/the-greatest-estate-developer/list?title_no=3596',moves=['Shovel Drive','Earthbreaker','Worksite Reversal','Rubble Shot','Overtime Barrage','Safety First','Fault Line','Grand Excavation'],ultimate=640,taunt='Nightmare Grin',description='Shovel combinations, excavation shockwaves, rubble, worksite counters and a giant-hamster Grand Excavation finisher.')}

from manhwa_expansion import BATCH
PROFILES.update(BATCH)

# The v5 Jin Mu-Won combat atlas uses wider cells to keep sword silhouettes apart.
_jin_v5=ROOT/'sprite-fighter/characters/jin-mu-won/art/identity-scale-v5/combat.generation.json'
if _jin_v5.exists():
    _layout=json.loads(_jin_v5.read_text())
    if _layout.get('layout_validation',{}).get('status')=='PASS':
        PROFILES['jin-mu-won'].setdefault('art_layouts',{})['combat']={k:_layout[k] for k in ('columns','rows')}

def profile(slug):
    p=PROFILES[slug].copy();p['slug']=slug;p['folder']=ROOT/'sprite-fighter/characters'/slug
    p['movespec']=[(key,command,state,cost,label) for (key,command,state,cost),label in zip([('palm','x',1000,500),('piercer','/$F,x',1100,700),('stop','/$B,x',1200,600),('orb','/$D,x',1300,500),('butterfly','y',2000,1500),('shield','/$B,y',2100,1000),('wave','/$F,y',2200,2000),('ultimate','z',3000,3000)],p['moves'])]
    return p

class Author(BaseAuthor):
    def state(self,n,anim=None,kind='S',move='I',physics=None,bank=False,**params):super().state(n,anim,kind,move,physics,False,**params)

def animations(a):
    act=a.action
    act(0,[(62000,0,8),(62000,1,8)]);act(5,[(62000,0,4)])
    for n,p,t in [(6,4,6),(10,4,4),(11,4,-1),(12,0,4),(40,4,3),(41,6,-1),(42,6,-1),(43,7,-1),(47,4,3),(52,4,5),(100,5,24),(105,5,20),(170,13,-1),(181,0,-1)]:act(n,[(62000,p,t)])
    for n,poses in [(20,[2,3]),(21,[3,2])]:act(n,[(62000,p,8) for p in poses])
    for n in range(120,156):act(n,[(62000,9 if n in (121,131,141,152,153) else 8,6)])
    for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:act(n,[(62000,12 if n>=5030 else 10 if n%10==0 else 11,-1)])
    for n in [5100,5110,5140,5150,5160,5170]:act(n,[(62000,13,6 if n in (5100,5160) else -1)],hurt=n!=5110)
    act(5120,[(62000,13,8),(62000,14,8),(62000,0,5)])
    for n in [5200,5210,5220,5300,5500,5510]:act(n,[(62000,14,6),(62000,0,6)])
    act(190,[(62600,0,12),(62600,1,18),(62600,2,18),(62600,3,18),(62000,0,6)])
    act(800,[(62600,p,12) for p in range(12,16)])
    for n,(damage,start,duration,poses) in NORMALS.items():
        k='A' if n>=600 else 'C' if n>=400 else 'S'
        act(n,[(62400,poses[0],start),(62400,poses[1],5),(62400,poses[2],5),(62000,7 if k=='A' else 4 if k=='C' else 0,duration-start-10)],active=(1,),kind=k,box=(6,-24,58,0) if k=='C' else (8,-48,64,-8))
    for n,frames,active,box in [
        (1000,[(8,14),(9,6),(15,8)],(1,),(8,-44,68,-10)),(1100,[(5,12),(6,6),(15,12)],(1,),(8,-44,68,-10)),
        (1200,[(11,32),(0,10)],(0,),(-11,-52,38,0)),(1201,[(11,6),(13,8),(15,10)],(),(0,0,0,0)),
        (1300,[(3,16),(10,8),(15,12)],(),(0,0,0,0)),(2000,[(1,12),(2,6),(3,6),(4,6),(5,6),(6,6),(15,14)],(1,3,5),(8,-45,80,-8)),
        (2100,[(11,32),(0,12)],(0,),(-11,-52,38,0)),(2101,[(13,8),(15,12)],(),(0,0,0,0)),
        (2200,[(5,20),(6,6),(8,8),(7,6),(15,14)],(1,3),(8,-46,92,-7))]:act(n,[(62400,p,t) for p,t in frames],active=active,box=box)
    act(700,[(62400,0,8),(62400,8,8)]);act(900,[(62000,4,8),(62000,5,10),(62000,0,6)])
    act(3000,[(62600,4,12),(62600,5,12),(62600,6,8),(62600,11,10)],active=(2,),box=(8,-47,80,-6))
    act(3001,[(62600,p,t) for p,t in [(5,24),(6,24),(7,32),(8,24),(9,36),(10,12),(11,12)]])
    for i in range(16):a.animations[9100+i]=f'\n[Begin Action {9100+i}]\n63100,{i},0,0,-1\n'
    for n,p in [(9120,6),(9121,2)]:a.animations[n]=f'\n[Begin Action {n}]\n63100,{p},0,0,2,,,0.045,0.045\n63100,{p},0,0,3,,,0.075,0.075\n'
    a.animations[9010]='\n[Begin Action 9010]\nClsn1Default: 1\nClsn1[0]=-7,-7,7,7\n63100,3,0,0,-1\n'

def core(a,p):
    st,ct=a.state,a.ctl
    st(20,20,velset='0,0');ct(20,'Walk control','CtrlSet',value=1)
    ct(20,'Walk','VelSet',x='ifelse(AILevel>0,1.5,ifelse(command="holdback",-1.2,ifelse(command="holdfwd",1.5,0)))',y=0)
    for value,condition in [(20,'vel x>0'),(21,'vel x<0')]:ct(20,'Stride','ChangeAnim',condition+f' && anim!={value}',value=value)
    ct(20,'Stop','ChangeState','(AILevel=0 && command!="holdfwd" && command!="holdback") || (AILevel>0 && p2bodydist x<30)',value=0,ctrl=1)
    for n in (170,175,180,181,190,191,195):
        st(n,190 if n in (190,191) else 181 if n in (180,181,195) else 170,velset='0,0')
        if n in (190,191):ct(n,'Entrance','AssertSpecial','roundstate<2 && time<72',flag='intro');a.end(n)
        elif n in (180,181,195):ct(n,'Victory','NotHitBy',value='SCA',time=1)
    st(-3)
    for i,key in enumerate(('a','b','c'),1):ct(-3,'Buffer strike','MapSet',f'!ishelper && time>1 && (stateno=200 || stateno=210 || stateno=220 || stateno=230 || stateno=240 || stateno=250 || stateno=260) && command="{key}"',map='"fighter.buffer"',value=i)
    ct(-3,'Buffer window','MapSet','!ishelper && (command="a" || command="b" || command="c")',map='"fighter.buffer_ticks"',value=12)
    ct(-3,'Buffer decay','MapAdd','!ishelper && map(fighter.buffer_ticks)>0',map='"fighter.buffer_ticks"',value=-1)
    for n,(damage,active,duration,poses) in NORMALS.items():
        k='A' if n>=600 else 'C' if n>=400 else 'S';st(n,n,kind=k,move='A',**({} if k=='A' else dict(velset='0,0')),poweradd=20)
        ct(n,'Consume strike','MapSet','!time',map='"fighter.buffer"',value=0)
        if k=='S':ct(n,'Step','VelSet','time<4',x=1.5);ct(n,'Plant','VelSet','time>=4',x=0)
        ct(n,'Weapon wind','PlaySnd',f'time={max(0,active-3)}',value='0,5',volumescale=75)
        a.hit(n,active,damage,k,guard='H' if k=='A' else 'L' if k=='C' else 'MA',fall=n in (220,250,260,410,420,620))
        for button,dest in LINKS.get(n,{}).items():ct(n,'Confirmed chain','ChangeState',f'MoveContact && time>={active+1} && time<={duration-2} && ((map(fighter.buffer)={button} && map(fighter.buffer_ticks)>0) || (AILevel>0 && time>={active+3} && {button}=1))',value=dest)
        a.end(n,k)
    author_techniques(a,p['movespec'])
    for n,anim in [(800,800),(700,700),(900,900)]:
        st(n,anim,velset='0,0')
        if n==700:
            ct(n,'Gather strength','PowerAdd',value=15);powerfx(a,n,7,0,pos='0,-2',scale='.16,.04',duration=20)
            ct(n,'Finish charging','ChangeState','command!="hold_s" || power>=3000',value=0,ctrl=1)
        elif n==900:
            ct(n,'Evade','VelSet','time<12',x=-2);ct(n,'Settle','VelSet','time>=12',x=0)
            ct(n,'Evade window','NotHitBy','time=[3,12]',value='SCA',time=1);a.end(n)
        else:
            if p['slug']=='arthur':powerfx(a,n,13,24,pos='-13,-44',scale='.075,.075',duration=24,bindtime=-1,sprpriority=5)
            a.end(n)
    for n,vel in [(100,4),(105,-3)]:st(n,n,physics='N',velset=f'{vel},0');ct(n,'Dash recovery','ChangeState','time>=18',value=0,ctrl=1)
    ultimate(a,p)

def ultimate(a,p):
    st,ct=a.state,a.ctl;lloyd=p['slug']=='lloyd'
    st(3001,3001,move='A',physics='N',velset='0,0')
    ct(3001,'Cinematic room','PosAdd','!time && frontedgebodydist<88',x='-(88-frontedgebodydist)')
    ct(3001,'Visible attacker','SprPriority',value=3)
    ct(3001,'Captured opponent','TargetBind','time<140 && NumTarget>0',pos='48+ifelse(time>=92,10,0),ifelse(time<24,0,ifelse(time<60,-10,ifelse(time<128,-22,-10)))',time=1)
    ct(3001,'Protection','NotHitBy',value='SCA',time=1)
    ct(3001,'Contrast','BGPalFX','!time',time=148,mul='125,110,90' if lloyd else '95,95,135')
    ct(3001,'Anticipation','SuperPause','!time',time=8,movetime=0,anim=-1,darken=0,p2defmul=1,poweradd=0)
    for pose,t,pos,scale,duration in [(8,0,'10,-42','.24,.25',96),(7,0,'0,-2','.30,.075',144),(9,24,'48,-37','.17,.23',70),(10,56,'48,-42','.14,.34',28),(11 if lloyd else 15,88,'28,-37','.27,.30',40),(12,112,'23,-32','.48,.32',34),(14,128,'58,-33','.24,.30',24)]:powerfx(a,3001,pose,t,pos,scale,duration)
    if lloyd:powerfx(a,3001,13,36,pos='-10,-26',scale='.22,.25',duration=50)
    if p['slug'] in BATCH:
        # Distinct character motifs, kept behind both actors and localized to
        # the corresponding phase of the confirmed hit sequence.
        if p['slug']=='gang-ryong':
            powerfx(a,3001,13,40,pos='48,-56',scale='.19,.19',duration=40)
            powerfx(a,3001,11,88,pos='35,-38',scale='.30,.26',duration=40)
        elif p['slug']=='mok-gyeongwoon':
            powerfx(a,3001,13,12,pos='-15,-35',scale='.15,.20',duration=84)
            powerfx(a,3001,11,88,pos='48,-40',scale='.28,.30',duration=40)
        elif p['slug']=='arthur':
            powerfx(a,3001,11,88,pos='36,-38',scale='.28,.26',duration=40)
            powerfx(a,3001,4,28,pos='48,-36',scale='.13,.13',duration=20)
        elif p['slug'] in ('cha-yeon-woo','kim-dokja'):
            powerfx(a,3001,11,60,pos='0,-35',scale='.28,.26',duration=68)
        elif p['slug']=='eugene':
            powerfx(a,3001,13,24,pos='-15,-30',scale='.19,.22',duration=96)
            powerfx(a,3001,11,88,pos='40,-40',scale='.26,.28',duration=40)
        elif p['slug']=='zhuo-fan':
            powerfx(a,3001,13,12,pos='-15,-35',scale='.19,.22',duration=76)
            powerfx(a,3001,11,88,pos='40,-40',scale='.28,.26',duration=40)
    for t,damage,shake in [(28,80,3),(60,100,4),(92,120,5),(128,p['ultimate']-340,8)]:
        ct(3001,'Cinematic contact','TargetLifeAdd',f'time={t} && NumTarget>0',value=-damage,kill=int(t==128))
        ct(3001,'Impact','EnvShake',f'time={t}',time=5 if t<128 else 12,ampl=-shake,freq=75)
        ct(3001,'Impact sound','PlaySnd',f'time={t}',value='0,6' if t<128 else '0,8')
        if t<128:powerfx(a,3001,14,t,pos='48,-35',scale='.10,.13',duration=14)
    ct(3001,'Flash','BGPalFX','time=128',time=5,add='105,100,100',mul='225,220,255')
    ct(3001,'Settle contrast','BGPalFX','time=144',time=20,mul='240,240,250')
    ct(3001,'Release','TargetState','time=140 && NumTarget>0',value=3052);a.end(3001)
    st(3050,kind='S',move='H',physics='N',velset='0,0')
    ct(3050,'Own hurt art','ChangeAnim','!time',value=5000);ct(3050,'Victim visible','SprPriority',value=4)
    ct(3050,'Camera','ScreenBound',value=1,movecamera='1,1');ct(3050,'Emergency release','SelfState','time>=220',value=5050,ctrl=0)
    for n,v in [(3051,'2,-3'),(3052,'6,-5')]:st(n,kind='A',move='H',physics='N',velset=v);ct(n,'Own physics','SelfState',value=5050,ctrl=0)

def commands(p):
    import baam_model,re
    previous=baam_model.MOVES
    try:baam_model.MOVES=p['movespec'];cmd=baam_model.author_commands()
    finally:baam_model.MOVES=previous
    cmd=re.sub(r'\n\[State -1, CPU ignition\].*?(?=\n\[State|\Z)','',cmd,flags=re.S)
    return cmd.replace('baam.','fighter.').replace('name="form"','name="taunt"').replace('command="form"','command="taunt"')
