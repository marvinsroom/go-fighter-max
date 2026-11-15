"""Three explicit human loadouts and dedicated meter supers for the illustrated port."""
import re,json
from PIL import Image
import numpy as np
from scipy import ndimage
from jinwoo_hybrid_art import drawing
import jinwoo_super_power as super_power

WEAPON_BANK = 500000
DAGGER_BANK = 700000
TOGGLE = 870220
BARE_SUPER = 876290
DAGGER_SUPER = 876300
SWORD_SUPER = 876310
SHOCKWAVE = 876311


def load(root, art):
    folder=root/'sprite-fighter/characters/jinwoo/art/greatsword'
    registration=json.loads((folder/'registration.json').read_text())
    for name,sheet in registration['sheets'].items():
        path=folder/sheet['file']
        with Image.open(path) as im:
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,path
            pixels=np.array(im)
        labels,_=ndimage.label(pixels[:,:,3]>sheet['alpha_min'])
        for i,frame in enumerate(sheet['frames']):
            x1,y1,x2,y2=frame['rect'];tile=pixels[y1:y2,x1:x2].copy()
            tile[:,:,3]=np.where(np.isin(labels[y1:y2,x1:x2],frame['components']),tile[:,:,3],0)
            axis=frame['axis'];key=f'sword:{name}:{i}'
            art[key]=drawing(Image.fromarray(tile),axis,62.5/sheet['body_height'],str(path.relative_to(root)),frame['rect'])
            art[key]['component_alpha_min']=sheet['alpha_min']


def commands(cmd):
    # Directional variants win before the neutral super. Release commands avoid
    # firing a super while entering the weapon toggle or domain input.
    cmd = re.sub(r'(name\s*=\s*"Mornach Domain"\s*\n\s*command\s*=)[^\n]*', r'\1/$B, ~y', cmd)
    # var(10): 0=barehand, 10000=daggers, 20000=greatsword.
    definitions = '''
[Command]
name="arsenal_super"
command=c
time=1
[Command]
name="arsenal_weapon"
command=/$D, y
time=1
'''
    # D-pad transforms MUST win before A/B/X (bridge sends d+a etc.).
    routes = '''
[State -1, Transform Igris]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="our_tf_igris"
value=870201
ctrl=0
[State -1, Transform Beru]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="our_tf_beru"
value=870202
ctrl=0
[State -1, Transform Iron]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="our_tf_iron"
value=870203
ctrl=0
[State -1, Transform Tank]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="our_tf_tank"
value=870204
ctrl=0
[State -1, Human light A]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=ctrl
triggerall=var(10)<=20000
trigger1=command="a" || command="our_light"
value=cond(var(10)=0,cond(statetype=A,875600,cond(command="holddown",875400,875200)),cond(statetype=A,600,cond(command="holddown",410,200)))
ctrl=0
[State -1, Human medium B]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=ctrl
triggerall=var(10)<=20000
trigger1=command="b" || command="our_medium"
value=cond(var(10)=0,cond(statetype=A,875610,cond(command="holddown",875410,875210)),cond(statetype=A,610,cond(command="holddown",420,300)))
ctrl=0
[State -1, Human heavy Y]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=ctrl
triggerall=!command="holddown"
trigger1=command="y" || command="our_heavy"
value=cond(var(10)=0,cond(statetype=A,875620,875220),cond(statetype=A,630,400))
ctrl=0
[State -1, Human grab X]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=statetype!=A && ctrl
triggerall=!command="our_ultimate"
triggerall=p2bodydist x<140
triggerall=p2statetype!=A
triggerall=p2movetype!=H
trigger1=command="x" || command="our_grab"
value=879920
ctrl=0
[State -1, Visible weapon toggle]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=statetype!=A && ctrl
trigger1=command="arsenal_weapon"
value=870220
[State -1, Human meter super]
type=ChangeState
triggerall=!AILevel && var(45)=0 && roundstate=2
triggerall=statetype!=A && ctrl && power>=1000
triggerall=!command="holddown" && !command="holdback"
trigger1=command="arsenal_super"
; Bare hands, Antares daggers, and greatsword each keep their own super.
value=cond(var(10)=0,876290,cond(var(10)>=20000,876310,876300))
'''
    # Native Dagger change command remains defined for source tooling, but its
    # physical input is intercepted by the two-way toggle above.
    return re.sub(r'(?im)(\[statedef\s+-1\])', lambda m:definitions+m[0]+routes, cmd, count=1)


def states():
    # Never use native 800/801 — those are helper FX states with blank anim 6
    # and unconditional DestroySelf (player vanishes). Dedicated high IDs only.
    out = '''
[Statedef 879810]
type=S
movetype=I
physics=N
anim=6
velset=0,0
ctrl=0
[State 879810, Helpers only]
type=DestroySelf
triggerall=ishelper
trigger1=time>=1
[State 879810, Player safety]
type=ChangeState
triggerall=!ishelper
trigger1=1
value=0
ctrl=1

[Statedef 879920]
type=S
movetype=A
physics=S
anim=879920
ctrl=0
velset=0,0
[State 879920, Grab]
type=HitDef
trigger1=time=3
attr=S,NT
hitflag=M-
priority=1,Miss
sparkno=-1
hitsound=-1
guardsound=-1
guard.dist=0
pausetime=0,0
p1stateno=879921
p2stateno=879922
p2getp1state=1
fall=1
numhits=0
getpower=0,0
givepower=0,0
id=879920
[State 879920, Miss]
type=ChangeState
trigger1=animtime=0
value=0
ctrl=1

[Statedef 879921]
type=S
movetype=A
physics=N
anim=879921
ctrl=0
velset=0,0
[State 879921, Hold]
type=TargetBind
trigger1=time<22
pos=36,-8
[State 879921, Damage]
type=TargetLifeAdd
trigger1=time=22
value=-110
kill=1
[State 879921, Release]
type=TargetState
trigger1=time=22
value=879923
[State 879921, Done]
type=ChangeState
trigger1=time>=40
value=0
ctrl=1

[Statedef 879922]
type=A
movetype=H
physics=N
ctrl=0
velset=0,0
sprpriority=0
[State 879922, Pose]
type=ChangeAnim
trigger1=time=0
value=5030
[State 879922, Safe pose]
type=ChangeAnim
trigger1=time=0 && !selfanimexist(5030)
value=5000
[State 879922, Armor]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 879922, Orphan]
type=SelfState
trigger1=time>90
value=5050

[Statedef 879923]
type=A
movetype=H
physics=N
ctrl=0
anim=5050
velset=-5.5,-8.5
[State 879923, Pose]
type=ChangeAnim
trigger1=time=0 && !selfanimexist(5050)
value=5030
[State 879923, Gravity]
type=VelAdd
trigger1=1
y=.55
[State 879923, Land]
type=SelfState
trigger1=vel y>0 && pos y>=0
value=5110

[Statedef 870220]
type=S
movetype=I
physics=S
anim=-1
ctrl=0
velset=0,0
[State 870220, Choose visible transition]
type=ChangeAnim
trigger1=time=0
value=cond(var(10)=0,876322,cond(var(10)<20000,876323,876324))
[State 870220, Equip]
type=VarSet
trigger1=time=20
var(10)=cond(var(10)=0,10000,cond(var(10)<20000,20000,0))
[State 870220, Reset domain]
type=VarSet
trigger1=time=20
var(11)=0
[State 870220, Reset source selector]
type=VarSet
trigger1=time=20
var(12)=0
[State 870220, Flash]
type=PalFX
trigger1=time=20
time=10
add=35,0,65
[State 870220, Weapon handoff sound]
type=PlaySnd
trigger1=time=20
value=S5,52
volumescale=70
persistent=0
[State 870220, Ready]
type=ChangeState
trigger1=time>=38
value=0
ctrl=1
'''
    # Barehand attacks have their own state/animation bank. They never borrow
    # a dagger action, so changing stance cannot make a weapon appear mid-hit.
    for n, anim, damage, startup, recovery, kind in (
        (875200,875200,42,7,24,'S'), (875210,875210,62,10,30,'S'),
        (875220,875220,88,14,38,'S'), (875400,875400,38,7,24,'C'),
        (875410,875410,58,10,30,'C'), (875600,875600,40,7,24,'A'),
        (875610,875610,60,10,30,'A'), (875620,875620,82,13,36,'A')):
        out += f'''\n[Statedef {n}]\ntype={kind}\nmovetype=A\nphysics={'N' if kind=='A' else 'S'}\nanim={anim}\nctrl=0\n[State {n}, Barehand contact]\ntype=HitDef\ntrigger1=time={startup}\nattr={kind},NA\ndamage={damage},4\nhitflag=MAF\nguardflag={'H' if kind=='A' else 'MA'}\npriority=4,Hit\npausetime=4,8\nsparkno=2\nsparkxy=0,-35\nground.type=High\nground.hittime=18\nground.velocity=-3,-3\nair.velocity=-3,-4\nfall={1 if damage>=80 else 0}\n[State {n}, Air gravity]\ntype=VelAdd\ntriggerall=statetype=A\ntrigger1=1\ny=.44\n[State {n}, Land]\ntype=ChangeState\ntriggerall=statetype=A\ntrigger1=vel y>0 && pos y>=0\nvalue=52\n[State {n}, Recover]\ntype=ChangeState\ntrigger1=time>={recovery}\nvalue={50 if kind=='A' else 0}\nctrl=1\n'''
    for n, hits, damage, recovery in ((DAGGER_SUPER, (10,18,26), 60, 48),):
        out += f'''
[Statedef {n}]
type=S
movetype=A
physics=S
anim={n}
velset=0,0
ctrl=0
poweradd=-1000
[State {n}, Step into the attack]
type=VelSet
trigger1=1
x={'cond(time>=4 && time<10,3.5,cond(time>=18 && time<26,2,0))' if n==DAGGER_SUPER else 'cond(time>=12 && time<22,1.4,0)'}
'''
        out+=super_power.start(n)
        for t in hits:
            out += f'''
[State {n}, Strike {t}]
type=HitDef
trigger1=time={t}
attr=S,HA
damage={damage},8
hitflag=MAF
guardflag=MA
priority=5,Hit
pausetime={7 if t==hits[-1] else 4},{12 if t==hits[-1] else 8}
sparkno=-1
guard.sparkno=-1
sparkxy=0,-35
ground.type=High
ground.hittime=24
ground.velocity={'-5,-4' if t==hits[-1] else '-2,0'}
air.velocity={'-5,-5' if t==hits[-1] else '-3,-4'}
fall={1 if t==hits[-1] else 0}
getpower=0,0
givepower=12,5
[State {n}, Compact weapon trail {t}]
type=Explod
trigger1=time={t}
anim={879860 if n==DAGGER_SUPER else 879861}
ID={879820 if n==DAGGER_SUPER else 879821}
postype=p1
pos=32,-32
scale={'.85,.85' if n==DAGGER_SUPER else '1,1'}
sprpriority=3
ownpal=1
removetime=-2
persistent=0
[State {n}, Weapon sound {t}]
type=PlaySnd
trigger1=time={t}
value=S5,52
volumescale=80
'''
            out+=super_power.impact(n,t,t==hits[-1])
        out += f'''
[State {n}, Recover]
type=ChangeState
trigger1=time>={recovery}
value=0
ctrl=1
'''
    out += '''
[Statedef 876290]
type=S
movetype=A
physics=S
anim=876290
velset=0,0
ctrl=0
poweradd=-1000
[State 876290, Shadow reinforcement]
type=SuperPause
trigger1=!time
time=7
movetime=0
anim=-1
sound=-1
darken=0
unhittable=0
persistent=0
[State 876290, Bare rush]
type=VelSet
trigger1=time>=5 && time<25
x=2.4
[State 876290, First impact]
type=HitDef
trigger1=time=8
attr=S,HA
damage=55,4
hitflag=MAF
guardflag=MA
priority=5,Hit
pausetime=4,7
sparkno=2
sparkxy=0,-35
ground.hittime=18
ground.velocity=-2.5,-1
air.velocity=-2.5,-3
[State 876290, Second impact]
type=HitDef
trigger1=time=15
attr=S,HA
damage=65,4
hitflag=MAF
guardflag=MA
priority=5,Hit
pausetime=4,7
sparkno=2
sparkxy=0,-35
ground.hittime=18
ground.velocity=-3,-2
air.velocity=-3,-3
[State 876290, Finisher]
type=HitDef
trigger1=time=24
attr=S,HA
damage=105,8
hitflag=MAF
guardflag=MA
priority=5,Hit
pausetime=7,11
sparkno=-1
guard.sparkno=-1
sparkxy=0,-35
ground.hittime=24
ground.velocity=-6,-4
air.velocity=-6,-5
fall=1
[State 876290, Finisher effect]
type=Explod
trigger1=time=24
anim=879837
ID=876290
postype=p1
pos=42,-34
scale=.75,.75
sprpriority=5
ownpal=1
removetime=-2
persistent=0
[State 876290, Recover]
type=ChangeState
trigger1=time>=44
value=0
ctrl=1

[Statedef 876310]
type=S
movetype=A
physics=S
anim=876310
velset=0,0
ctrl=0
poweradd=-1000
[State 876310, Step into the attack]
type=VelSet
trigger1=1
x=cond(time>=12 && time<22,1.4,0)
'''
    out += super_power.start(SWORD_SUPER)
    out += '''
[State 876310, Sword contact]
type=HitDef
trigger1=time=22
attr=S,HA
damage=70,8
hitflag=MAF
guardflag=MA
priority=5,Hit
pausetime=7,12
sparkno=-1
guard.sparkno=-1
sparkxy=0,-35
ground.type=High
ground.hittime=24
ground.velocity=-5,-4
air.velocity=-5,-5
fall=1
getpower=0,0
givepower=12,5
[State 876310, Launch greatsword shockwave]
type=Helper
trigger1=time=22
name="Greatsword Shockwave"
ID=876311
stateno=876311
postype=p1
pos=44,-30
facing=1
ownpal=1
supermovetime=0
pausemovetime=0
persistent=0
[State 876310, Weapon sound]
type=PlaySnd
trigger1=time=22
value=S5,52
volumescale=80
'''
    out += super_power.impact(SWORD_SUPER,22,True).replace(
        'anim=879837', 'anim=879861').replace(
        'pos=44,-33', 'pos=48,-20').replace(
        'scale=.85,.85', 'scale=.35,.22')
    out += '''
[State 876310, Recover]
type=ChangeState
trigger1=time>=58
value=0
ctrl=1

[Statedef 876311]
type=A
movetype=A
physics=N
anim=876311
velset=8.5,0
ctrl=0
[State 876311, Shockwave transparency]
type=Trans
trigger1=1
trans=addalpha
alpha=220,36
[State 876311, Keep wave traveling parallel to the floor]
type=AngleDraw
trigger1=1
value=0
scale=1,1
[State 876311, Traveling shockwave]
type=HitDef
trigger1=time=0
attr=S,HP
damage=165,10
hitflag=MAF
guardflag=MA
priority=6,Hit
pausetime=0,10
sparkno=-1
guard.sparkno=-1
sparkxy=0,0
ground.type=High
ground.hittime=28
ground.velocity=-8,-4
air.velocity=-8,-5
fall=1
fall.recover=0
getpower=0,0
givepower=10,5
[State 876311, Impact shake]
type=EnvShake
trigger1=movehit
time=10
ampl=-4
freq=70
persistent=0
[State 876311, End]
type=DestroySelf
trigger1=movecontact
trigger2=time>=48
trigger3=frontedgedist<-80
'''
    return out


def controllers():
    return '''
[State -2, Equipped dagger artwork]
type=ChangeAnim
triggerall=!ishelper && var(45)=0 && var(10)=10000
triggerall=anim<500000
trigger1=selfanimexist(anim+700000)
value=anim+700000
elem=animelemno(0)
ignorehitpause=1
[State -2, Human greatsword artwork]
type=ChangeAnim
triggerall=!ishelper && var(45)=0 && var(10)>=20000
triggerall=anim<500000
trigger1=selfanimexist(anim+500000)
value=anim+500000
elem=animelemno(0)
ignorehitpause=1
[State -2, Sword throw artwork]
type=ChangeAnim
triggerall=!ishelper && var(45)=0 && var(10)>=20000
trigger1=anim=879920 && selfanimexist(507920)
value=507920
elem=animelemno(0)
ignorehitpause=1
[State -2, Sword throw slam artwork]
type=ChangeAnim
triggerall=!ishelper && var(45)=0 && var(10)>=20000
trigger1=anim=879921 && selfanimexist(507921)
value=507921
elem=animelemno(0)
ignorehitpause=1
'''


def air(source, mapping, art):
    """Clone human actions with sword drawings, retaining collision/timing."""
    out=[]
    jump_actions={40,41,42,43,44,45,47,50,52}
    crouch_actions={10,11,12}
    for block in re.split(r'(?=^\[Begin Action )', source, flags=re.M|re.I):
        match=re.match(r'\[Begin Action (\d+)\]',block,re.I)
        if not match or int(match[1])>=WEAPON_BANK: continue
        n=int(match[1]); rows=block.splitlines(); changed=False
        # Source jump actions contain crouch/downed body rows. Author every
        # greatsword airborne action below so these can never win by AIR order.
        if n%10000 in jump_actions or n%10000 in crouch_actions: continue
        body_rows=[];active_rows=[];pending=None;default=False
        for j,line in enumerate(rows):
            collision=re.match(r'\s*Clsn1(Default)?\s*:\s*(\d+)',line,re.I)
            if collision:
                if collision[1]:default=int(collision[2])>0
                else:pending=int(collision[2])>0
            if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
                fields=line.split(';')[0].split(',');pose=mapping.get(tuple(map(int,fields[:2])))
                if pose and pose.startswith('base:'):
                    if (pending if pending is not None else default):active_rows.append(len(body_rows))
                    body_rows.append(j)
                pending=None
        if n%10000 in (20,21) and body_rows:
            # Walking has no attack element triggers. Eight drawings fit the
            # original 48-tick loop, with its original default hurt boxes.
            prefix=rows[:body_rows[0]];prefix[0]=f'[Begin Action {WEAPON_BANK+n}]'
            # Two upright weapon-ready drawings; attack poses made walking
            # look like skating and changed apparent height every few ticks.
            sequence=(0,1,2,3)
            if n%10000==21: sequence=tuple(reversed(sequence))
            for i in sequence:
                m=art[f'combat:locomotion-sword:{i}']
                prefix.append(f"{m['group']},{m['number']},0,0,6,,,{m['scale']},{m['scale']}")
            out.append('\n'.join(prefix));continue
        positions={line:i for i,line in enumerate(body_rows)}
        for i,line in enumerate(rows):
            if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
            p=[v.strip() for v in line.split(';')[0].split(',')]
            pose=mapping.get(tuple(map(int,p[:2])))
            if not pose or not pose.startswith('base:'):continue
            key=pose_for(n,positions[i],len(body_rows),pose[5:],active_rows)
            m=art[key]
            p[:2]=[str(m['group']),str(m['number'])]
            while len(p)<9:p.append('')
            # One AIR scale for the whole sword bank (charge/idle-unified).
            lock=art.get('base:idle',m)['scale']
            p[7]=p[8]=f'{lock:.9f}'
            rows[i]=','.join(p);changed=True
        if changed:
            rows[0]=f'[Begin Action {WEAPON_BANK+n}]'
            out.append('\n'.join(rows))
    def action(n,frames,sword=False):
        # Clsn in character units (Size-scaled). Sword reach slightly longer.
        lock=art['base:idle']['scale'] if 'base:idle' in art else None
        lines=[f'[Begin Action {n}]','Clsn2Default: 1','Clsn2[0] = -12,-59,12,0']
        for key,t,active in frames:
            if active:lines+=['Clsn1: 1','Clsn1[0] = 0,-65,'+('100' if sword else '72')+',-5']
            m=art[key]
            # Combat-v2 frames are normalized as one bank and must keep their
            # registered scale.  Applying the tiny source-idle scale here made
            # dagger supers collapse into miniature Jinwoos.
            # Greatsword sheets have their own measured body heights. Reusing
            # the source-idle scale makes the sword frames visibly grow.
            sc=m['scale'] if key.startswith(('combat:','sword:')) else (lock if lock is not None else m['scale'])
            lines.append(f"{m['group']},{m['number']},0,0,{t},,,{sc:.9f},{sc:.9f}")
        out.append('\n'.join(lines))
    special_keys = [f'combat:special:{i}' for i in (8,9,9,10,9,10,10,11)]
    action(DAGGER_SUPER,[(key,t,i in (2,4,6)) for i,(key,t) in enumerate(zip(special_keys,(4,6,4,4,4,4,6,16)))])
    action(SWORD_SUPER,[(f'sword:super:{i}',t,i in (4,5)) for i,t in enumerate((6,6,6,4,5,5,10,17))],True)
    action(876320,[('sword:stance:6',7,False),('sword:stance:7',8,False)])
    action(876321,[('combat:ground:0',7,False),('combat:ground:1',8,False)])
    action(BARE_SUPER,[
        ('combat:normal-reactions:0',5,False),('combat:normal-reactions:1',5,True),
        ('combat:normal-reactions:2',3,False),('combat:normal-reactions:1',5,True),
        ('combat:normal-reactions:2',4,False),('combat:normal-reactions:3',7,True),
        ('combat:normal-reactions:2',15,False)])
    action(876322,[
        ('combat:normal-reactions:0',5,False),('combat:normal-reactions:1',5,False),
        ('combat:normal-reactions:2',5,False),('combat:ground:0',5,False),
        ('combat:ground:1',5,False),('combat:ground:2',6,False),
        ('combat:ground:3',8,False)])
    action(876323,[
        ('combat:ground:0',4,False),('combat:ground:1',4,False),
        ('sword:super:0',4,False),('sword:super:1',4,False),
        ('sword:super:2',4,False),('sword:super:3',4,False),
        ('sword:super:4',4,False),('sword:super:5',4,False),
        ('sword:super:6',4,False),('sword:super:7',6,False)])
    action(876324,[
        ('sword:super:7',4,False),('sword:super:6',4,False),
        ('sword:super:5',4,False),('sword:super:4',4,False),
        ('combat:normal-reactions:3',4,False),('combat:normal-reactions:2',5,False),
        ('combat:normal-reactions:0',9,False)])
    out.append('''[Begin Action 876311]
Clsn1Default: 1
Clsn1[0] = -12,-18,90,18
LoopStart
61013,7,0,0,3,,A,.45,.30
61013,7,0,0,3,,A,.45,.30
61013,7,0,0,3,,A,.45,.30
61013,7,0,0,3,,A,.45,.30''')
    # Weapon-free punches and kicks use only the normal reaction/locomotion
    # sheet. These action IDs are unreachable from dagger/sword routing.
    bare = {
        875200: (('combat:normal-reactions:0',6),('combat:normal-reactions:1',5),('combat:normal-reactions:0',13)),
        875210: (('combat:normal-reactions:0',8),('combat:normal-reactions:1',7),('combat:normal-reactions:2',15)),
        875220: (('combat:normal-reactions:2',10),('combat:normal-reactions:3',8),('combat:normal-reactions:2',20)),
        875400: (('combat:normal-locomotion:6',5),('combat:normal-reactions:1',6),('combat:normal-locomotion:7',13)),
        875410: (('combat:normal-locomotion:7',7),('combat:normal-reactions:3',8),('combat:normal-locomotion:6',15)),
        875600: (('combat:normal-locomotion:9',5),('combat:normal-reactions:1',6),('combat:normal-locomotion:10',13)),
        875610: (('combat:normal-locomotion:9',7),('combat:normal-reactions:3',8),('combat:normal-locomotion:11',15)),
        875620: (('combat:normal-locomotion:8',9),('combat:normal-reactions:3',8),('combat:normal-locomotion:11',19)),
    }
    for n, seq in bare.items():
        action(n,[(key,t,i==1) for i,(key,t) in enumerate(seq)])
    # Equipped dagger locomotion: the blades stay in hand outside attacks.
    dagger_moves = {
        0: tuple((f'combat:ground:{i}',6) for i in (0,1)),
        5: (('combat:ground:0',16),), 6: (('combat:ground:0',20),),
        10: (('combat:air-low:0',4),('combat:air-low:3',7)),
        11: (('combat:air-low:3',20),), 12: (('combat:air-low:3',4),('combat:ground:0',7)),
        20: tuple((f'combat:locomotion-dagger:{i}',6) for i in (0,1,2,3)),
        21: tuple((f'combat:locomotion-dagger:{i}',6) for i in (3,2,1,0)),
        100: tuple((f'combat:locomotion-dagger:{i}',4) for i in (4,5,6,7)),
        105: (('combat:air-low:4',4),('combat:air-low:5',8)),
    }
    for n in jump_actions:
        dagger_moves[n] = tuple((f'combat:air-low:{i}',3 if i<7 else 8) for i in range(4,12))
    for n, seq in dagger_moves.items(): action(DAGGER_BANK+n,[(key,t,False) for key,t in seq])
    # Guarantee a sword body for every common airborne state. Several source
    # actions contain no mapped body row, so the automatic clone skipped them.
    existing={int(m.group(1)) for block in out if (m:=re.match(r'\[Begin Action (\d+)\]',block))}
    sword_crouch={10:((11,3),(10,5)),11:((10,-1),),12:((10,3),(11,5))}
    for n,frames in sword_crouch.items():
        action(WEAPON_BANK+n,[(f'combat:sword-ground:{i}',t,False) for i,t in frames])
    # Use the genuine locomotion flight/contact drawings. The sword-air attack
    # sheet contains tucked knees and a hand-on-ground finisher, so it is not a
    # neutral jump cycle.
    sword_jump={
        40:((4,3),(5,5)), 41:((5,-1),), 42:((4,3),(5,-1)),
        43:((4,3),(5,-1)), 44:((6,-1),), 45:((5,-1),),
        47:((7,4),(0,5)), 50:((5,-1),), 52:((7,4),(0,5)),
    }
    for n,frames in sword_jump.items():
        action(WEAPON_BANK+n,[(f'combat:locomotion-sword:{i}',t,False) for i,t in frames])
    for n, seq in ((100,(4,5,6,7)), (105,(5,6,7))):
        if WEAPON_BANK+n not in existing:
            action(WEAPON_BANK+n,[(f'combat:locomotion-sword:{i}',4 if n==100 else 5,False) for i in seq])
    # Throw attempt / slam — dagger atlas frames (survives rebuild; native Action 6 is blank).
    lock = art['base:idle']['scale'] if 'base:idle' in art else None
    def throw_action(n, keys, times, grab_box=False):
        lines = [f'[Begin Action {n}]', 'Clsn2Default: 1', 'Clsn2[0] = -14,-57,14,0']
        for i, (key, t) in enumerate(zip(keys, times)):
            if key not in art:
                continue
            if grab_box and i == 1:
                lines += ['Clsn1: 1', 'Clsn1[0] = 0,-55,55,-4']
            m = art[key]
            sc = m['scale'] if key.startswith('combat:') else (lock if lock is not None else m['scale'])
            lines.append(f"{m['group']},{m['number']},0,0,{t},,,{sc:.9f},{sc:.9f}")
        if len(lines) > 3:
            out.append('\n'.join(lines))
    dagger = lambda i: f'combat:ground:{min(11,4+i)}' if f'combat:ground:{min(11,4+i)}' in art else f'base:idle'
    sword = lambda i: f'sword:light:{i}' if f'sword:light:{i}' in art else 'base:idle'
    # Prefer dagger throw visuals; sword bank still plays when var(10) remaps via ChangeAnim controller.
    throw_action(879920, [dagger(0), dagger(1), dagger(2)], (4, 6, 8), grab_box=True)
    throw_action(879921, [dagger(3), dagger(4), dagger(5), dagger(6)], (6, 8, 10, 12))
    throw_action(507920, [sword(0), sword(1), sword(2)], (4, 6, 8), grab_box=True)
    throw_action(507921, [sword(3), sword(4), sword(5), sword(6)], (6, 8, 10, 12))
    return '\n'+'\n\n'.join(out)+'\n'


def pose_for(action,index,total,fallback,active):
    """Choose by action and phase, avoiding shared source-key pose collisions."""
    n=action%10000
    sample=lambda start,end:start+min(end-start,index*(end-start+1)//max(1,total))
    sheet='stance';frame=0
    if n in (0,5,180,181,182,183,190,191,192,193,194,195):frame=index%2
    elif n in (10,11,12,121,131,141,151,153):frame=2+min(1,index*2//max(1,total))
    elif n in (120,122,130,132,140,142):frame=0
    elif n in (403,404):frame=6+index%2
    elif n in (500,501,2600,2620):frame=4+index%2
    elif n in (60,65):sheet='movement';frame=(index*2+(0 if n==60 else 1))%8
    elif n in (40,41,42,43,44,45,47,50,52):
        sheet='aerial';frame=sample(0,1) if n==40 else sample(6,7) if n in (47,52) else sample(2,5)
    elif 5000<=n<=5090:sheet='reactions';frame=2 if n>=5050 else (n//10)%2
    elif n in (170,175,5100,5110,5140,5150,5160,5170):sheet='reactions';frame=3
    elif n==5120:sheet='reactions';frame=sample(4,7)
    elif n in (3200,3210,3220):
        # Antares is commanded from one planted pose. Cycling jumping and
        # crouched finisher drawings made the monarch appear to resize.
        sheet='stance';frame=4
    elif 3000<=n<3400:sheet='finisher';frame=(sample(0,7)+(n//10)%3)%8
    elif 1000<=n<3000 or n in (200,210,220,260,300,310,320,350,400,410,415,416,420,426,430,440,450,460,465,600,610,620,630,650):
        # Idle A (200) = light horizontal. Idle B (300) = heavy horizontal on the
        # same slash sheet (the dedicated heavy sheet is an overhead cleave for Y).
        # Idle Y (400) = heavy overhead. Never use (n//100)%2 — it made 300 look
        # like whatever filled the medium clone and broke sword routing.
        if 600<=n<700:sheet='aerial'
        elif n in (200,210,220,260):sheet='light'
        elif n in (300,310,320,350):sheet='light'
        elif n in (400,410,415,416,420,426,430,440,450,460,465):sheet='heavy'
        else:sheet='heavy' if (n//100)%2 else 'light'
        heavy_feel=n in (300,310,320,350) or sheet=='heavy'
        frame=sample(2,5) if sheet=='aerial' else sample(0,7)
        if active and sheet in ('light','heavy'):
            first,last=active[0],active[-1]
            if index<first:frame=min(4 if heavy_feel else 2,index*(5 if heavy_feel else 3)//max(1,first))
            elif index<=last:frame=(5 if heavy_feel else 3)+min(1 if heavy_feel else 2,(index-first)*(2 if heavy_feel else 3)//max(1,last-first+1))
            else:frame=7 if heavy_feel else 6+min(1,(index-last-1)*2//max(1,total-last-1))
    elif fallback=='hurt':sheet='reactions';frame=0
    elif fallback=='down':sheet='reactions';frame=3
    elif fallback=='summon':frame=4+index%2
    elif fallback=='crouch':frame=3
    elif fallback.startswith('jump_'):sheet='aerial';frame=2+index%4
    elif fallback.startswith('dagger-cycle_'):sheet='light';frame=sample(0,7)
    return f'sword:{sheet}:{frame}'
