"""Readable entrance, persistent Monkey King, buffered chains and staged ultimate."""
from jin_mori_assets import *
from isolated_sprite_atlas import extract
import re,hashlib

FORM='map(mori.form)'
BODY_HEIGHT=424
NORMALS={230:(35,6,24,[0,1,2,0],False),240:(45,7,24,[3,4,4,0],False),250:(60,8,28,[5,6,7,0],True),260:(45,7,24,[8,9,10,0],False),270:(55,7,26,[5,6,7,0],False),280:(60,8,28,[8,9,10,0],False),290:(75,9,30,[11,12,13,0],True),310:(80,10,30,[8,9,10,0],True)}
LINKS={230:{1:240,2:260,3:310},240:{1:250,2:250,3:310},260:{1:250,2:270,3:310},270:{1:280,2:280,3:310},280:{1:290,2:290,3:310}}

def replace_state(text,number,block):
    pattern=rf'(?ims)^\[statedef\s+{number}\s*\].*?(?=^\[statedef\b|\Z)'
    assert re.search(pattern,text),number
    return re.sub(pattern,lambda _:block+'\n\n',text,count=1)

def bank_controller_animations(text,roots):
    """Bank actor animations at assignment, so loops don't restart every tick."""
    result=[]
    for block in re.split(r'(?=^\[statedef\b)',text,flags=re.I|re.M):
        h=re.match(r'\[statedef\s+(-?\d+)',block,re.I)
        if not h or int(h[1]) not in roots:result.append(block);continue
        chunks=re.split(r'(?=^\[state\b)',block,flags=re.I|re.M)
        chunks[0]=re.sub(r'(?im)^(anim\s*=\s*)([^;\n]+)',lambda m:m[1]+f'({m[2].strip()})+1000000*{FORM}',chunks[0])
        for i in range(1,len(chunks)):
            if re.search(r'(?im)^type\s*=\s*ChangeAnim\s*$',chunks[i]):
                chunks[i]=re.sub(r'(?im)^(value\s*=\s*)([^;\n]+)',lambda m:m[1]+f'({re.sub(r"(?i)\banim\b","(anim%1000000)",m[2].strip())})+1000000*{FORM}',chunks[i])
            chunks[i]=re.sub(r'(?im)^(trigger[^=]*=)([^\n]+)',lambda m:m[1]+re.sub(r'(?i)\banim\b','(anim%1000000)',m[2]),chunks[i])
        result.append(''.join(chunks))
    return ''.join(result)

def action(number,frames,boxes=True):
    a=f'\n[Begin Action {number}]\n'
    if boxes:a+='Clsn2Default: 1\nClsn2[0]=-12,-53,12,0\n'
    for group,pose,ticks in frames:a+=f'{group},{pose},0,0,{ticks},,,.125,.125\n'
    return a

def normal_state(number,damage,active,duration,poses,finish):
    s=f'''[Statedef {number}]
type=S
movetype=A
physics=S
anim={980000+number}
ctrl=0
velset=0,0
poweradd=20
[State {number}, Consume buffered input]
type=MapSet
trigger1=!time
map="mori.buffer"
value=0
[State {number}, Advance]
type=VelSet
trigger1=time<4
x=1.5
[State {number}, Plant feet]
type=VelSet
trigger1=time>=4
x=0
[State {number}, Contact]
type=HitDef
trigger1=time={active}
attr=S,NA
damage={damage},4
guardflag=MA
hitflag=MAF
pausetime=4,6
animtype={'Hard' if finish else 'Medium'}
ground.type=High
ground.slidetime=10
ground.hittime=24
ground.velocity={3 if finish else .25},{-3 if finish else 0}
air.velocity=2,-2
air.hittime=24
fall={int(finish)}
sparkno=-1
guard.sparkno=-1
hitsound=S200,1
guardsound=S200,40
getpower=20,5
givepower=10,5
'''
    for button,destination in LINKS.get(number,{}).items():
        s+=f'''[State {number}, Buffered chain {button}]
type=ChangeState
triggerall=MoveContact && time>={active+1} && time<={duration-2}
trigger1=map(mori.buffer)={button} && map(mori.buffer_ticks)>0
trigger2=AILevel>0 && time={active+3} && {button}=1
value={destination}
ctrl=0
'''
    s+=f'''[State {number}, Recover]
type=ChangeState
trigger1=AnimTime=0
value=0
ctrl=1
'''
    return s

INTRO='''[Statedef 190]
type=S
movetype=I
physics=S
anim=980190
ctrl=0
velset=0,0
[State 190, Base appearance]
type=MapSet
trigger1=!time
map="mori.form"
value=0
[State 190, Entrance voice]
type=PlaySnd
trigger1=time=16
value=S500,23
volumescale=65
[State 190, Hold entrance]
type=AssertSpecial
trigger1=roundstate<2 && time<72
flag=intro
[State 190, Ready]
type=ChangeState
trigger1=AnimTime=0
value=0
ctrl=ifelse(roundstate=2,1,0)
'''

TRANSFORM='''
[Statedef 980500]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=980500+map(mori.form)
[State 980500, Target appearance]
type=MapSet
trigger1=!time
map="mori.next_form"
value=1-map(mori.form)
[State 980500, Awakening]
type=MapSet
trigger1=time=56
map="mori.form"
value=map(mori.next_form)
[State 980500, Circlet light]
type=PalFX
trigger1=time=56
time=10
add=22,15,0
mul=256,256,256
[State 980500, Foot energy]
type=Explod
trigger1=time=16
anim=980913
ID=980913
pos=0,0
postype=p1
bindtime=-1
removetime=52
scale=.12,.06
sprpriority=-1
ownpal=1
removeongethit=1
[State 980500, Awakening sound]
type=PlaySnd
trigger1=time=36
value=S200,8
volumescale=65
[State 980500, Return]
type=ChangeState
trigger1=AnimTime=0
value=0
ctrl=1
'''

ULTIMATE='''[Statedef 4500]
type=S
movetype=A
physics=S
anim=980450
ctrl=0
velset=0,0
poweradd=-3000
[State 4500, Summon staff]
type=PlaySnd
trigger1=time=10
value=S500,21
volumescale=60
[State 4500, Opening sweep]
type=HitDef
trigger1=time=24
attr=S,HA
damage=40,12
guardflag=MA
hitflag=MAF
pausetime=4,8
animtype=Hard
ground.type=High
ground.hittime=30
ground.velocity=0,0
air.velocity=0,0
getpower=0,0
givepower=20,10
sparkno=-1
guard.sparkno=-1
hitsound=S200,4
guardsound=S200,40
p1stateno=4501
p2stateno=9804512
fall=0
[State 4500, Miss or block recovery]
type=ChangeState
trigger1=AnimTime=0
value=0
ctrl=1

[Statedef 4501]
type=S
movetype=A
physics=N
anim=980451
ctrl=0
velset=0,0
[State 4501, Keep confirmed sequence stable]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 4501, Background contrast]
type=BGPalFX
trigger1=!time
time=98
mul=170,185,210
[State 4501, Keep victim in shot]
type=TargetBind
triggerall=NumTarget>0
trigger1=time<70
pos=48,0
time=1
[State 4501, Sweep contact]
type=TargetLifeAdd
trigger1=time=18
value=-100
kill=0
[State 4501, Rising contact]
type=TargetLifeAdd
trigger1=time=42
value=-120
kill=0
[State 4501, Staff finisher]
type=TargetLifeAdd
trigger1=time=64
value=-280
kill=1
[State 4501, Wind trail]
type=Explod
trigger1=time=12
anim=980900
ID=980900
pos=32,-30
postype=p1
removetime=20
scale=.14,.10
sprpriority=-1
ownpal=1
removeongethit=1
[State 4501, Overhead trail]
type=Explod
trigger1=time=42
anim=980904
ID=980904
pos=42,-38
postype=p1
removetime=20
scale=.10,.12
sprpriority=-1
ownpal=1
removeongethit=1
[State 4501, Ground impact]
type=Explod
trigger1=time=64
anim=980908
ID=980908
pos=48,0
postype=p1
removetime=24
scale=.18,.08
sprpriority=-1
ownpal=1
removeongethit=1
[State 4501, Contact sounds]
type=PlaySnd
trigger1=time=18
trigger2=time=42
trigger3=time=64
value=S200,4
volumescale=75
[State 4501, Small impact]
type=EnvShake
trigger1=time=18
trigger2=time=42
time=3
ampl=-1
freq=75
[State 4501, Final impact]
type=EnvShake
trigger1=time=64
time=6
ampl=-2
freq=90
[State 4501, Release victim]
type=TargetState
trigger1=time=70 && NumTarget>0
value=9804513
[State 4501, Finish]
type=ChangeState
trigger1=AnimTime=0
value=0
ctrl=1

[Statedef 9804512]
type=S
movetype=H
physics=N
ctrl=0
velset=0,0
[State 9804512, Victim own hurt pose]
type=ChangeAnim
trigger1=!time
value=5000+1000000*map(mori.form)
[State 9804512, Emergency release]
type=SelfState
trigger1=time>=90
value=5050
ctrl=0

[Statedef 9804513]
type=A
movetype=H
physics=N
ctrl=0
velset=2.5,-3
[State 9804513, Return to victim physics]
type=SelfState
trigger1=1
value=5050
ctrl=0
'''

def install(folder,sprites):
    art=S/'art/combat-v2';out=art/'poses';out.mkdir(parents=True,exist_ok=True)
    registration=[]
    for group,slug in [(62300,'monkey-movement'),(62301,'monkey-combat'),(62302,'story')]:
        tiles=extract(art/(slug+'.png'),4,4)
        for i,(im,bounds) in enumerate(tiles):
            # The story atlas contains two independently drawn form rows. Its
            # King neutral was shorter than base: using base's factor shrank
            # the whole King sequence. Calibrate each form's neutral separately.
            reference=8 if group==62302 and i>=8 else 0
            factor=BODY_HEIGHT/tiles[reference][0].height
            im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
            anchor={2:.34,4:.45,6:.37,9:.36,12:.34,15:.30}.get(i,.5) if group==62301 else {9:.4,10:.42,11:.35,12:.5,13:.45,14:.4,15:.45}.get(i,.5) if group==62302 else .5
            axis=(round(im.width*anchor),im.height)
            if group==62302 and i==10:
                # The generated ready pose retained green goggles; use the
                # established golden-circlet staff grip instead of flashing base.
                approved=next(s for s in sprites if s['key']==(62002,10))
                im=approved['image'].copy();axis=approved['axis']
                factor=BODY_HEIGHT/im.height
                im=im.resize((round(im.width*factor),BODY_HEIGHT),Image.Resampling.LANCZOS)
                axis=(round(axis[0]*factor),BODY_HEIGHT)
            sprites.append(dict(key=(group,i),axis=axis,image=im));im.save(out/f'{slug}-{i}.png')
            registration.append(dict(group=group,pose=i,bounds=bounds,size=im.size,axis=axis))
    awakening=S/'art/awakening-v3'
    transition=[]
    for i,(im,bounds) in enumerate(extract(awakening/'transition.png',4,2)):
        # These are all planted, near-identical stances. Register crown and
        # soles explicitly so minor atlas drawing drift never becomes shrinkage.
        factor=BODY_HEIGHT/im.height
        im=im.resize((round(im.width*factor),BODY_HEIGHT),Image.Resampling.LANCZOS)
        axis=(im.width//2,BODY_HEIGHT)
        sprites.append(dict(key=(62304,i),axis=axis,image=im))
        transition.append(dict(group=62304,pose=i,bounds=bounds,size=im.size,axis=axis))
    (S/'awakening-registration.json').write_text(json.dumps(transition,indent=2))
    (awakening/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen.imagegen',file='transition.png',prompt='transition.prompt.txt',sha256=hashlib.sha256((awakening/'transition.png').read_bytes()).hexdigest()),indent=2))
    # FX remain their own independent transparent layers; sparse trails stay behind bodies.
    sheet=Image.open(art/'effects.png').convert('RGBA')
    for i in range(16):
        x=i%4;y=i//4
        im=sheet.crop((x*sheet.width//4,y*sheet.height//4,(x+1)*sheet.width//4,(y+1)*sheet.height//4))
        sprites.append(dict(key=(62303,i),axis=(im.width//2,im.height//2),image=im))
    air=(folder/'jin_mori.air').read_text()
    extra=''
    for n,(damage,active,duration,poses,finish) in NORMALS.items():
        extra+=f'\n[Begin Action {980000+n}]\nClsn2Default: 1\nClsn2[0]=-12,-53,12,0\n'
        extra+=f'62001,{poses[0]},0,0,{active},,,.125,.125\n'
        extra+='Clsn1: 1\nClsn1[0]=8,-52,'+str(48 if n in (230,240) else 60)+',-9\n'
        extra+=f'62001,{poses[1]},0,0,5,,,.125,.125\n62001,{poses[2]},0,0,5,,,.125,.125\n62000,0,0,0,{duration-active-10},,,.125,.125\n'
    extra+=action(980190,[(62302,0,12),(62302,1,12),(62302,2,12),(62302,3,18),(62000,0,18)])
    transition_ticks=[8,10,10,10,10,10,8,8]
    extra+=action(980500,[(62000,0,8)]+[(62304,i,t) for i,t in enumerate(transition_ticks)]+[(62300,0,10)])
    extra+=action(980501,[(62300,0,8)]+[(62304,i,t) for i,t in zip(range(7,-1,-1),transition_ticks)]+[(62000,0,10)])
    extra+='\n[Begin Action 980450]\nClsn2Default: 1\nClsn2[0]=-12,-53,12,0\n62302,8,0,0,12,,,.125,.125\n62302,9,0,0,10,,,.125,.125\nClsn1: 1\nClsn1[0]=10,-52,78,-6\n62302,11,0,0,8,,,.125,.125\n62302,10,0,0,12,,,.125,.125\n'
    extra+=action(980451,[(62302,10,12),(62302,11,12),(62302,12,14),(62302,13,14),(62302,14,14),(62302,15,24),(62302,8,18)])
    for start in (0,4,8,12):
        extra+=f'\n[Begin Action {980900+start}]\n'+''.join(f'62303,{i},0,0,5\n' for i in range(start,start+4))
    extra+=f'\n[Begin Action 980913]\n'+''.join(f'62303,{i},0,0,6\n' for i in range(12,16))
    # Clone actor actions for the persistent form; the source effect bank is shared.
    all_air=air+extra;bank=''
    movement={0:0,1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:3,10:14,11:14,12:15,13:15,14:3,15:0}
    for block in re.split(r'(?=^\[Begin Action\s+)',all_air,flags=re.I|re.M):
        h=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
        if not h:continue
        lines=[]
        for line in block.splitlines():
            if re.match(r'\[Begin Action',line,re.I):line=f'[Begin Action {int(h[1])+1000000}]'
            m=re.match(r'^\s*(6200[012])\s*,\s*(\d+)\s*,',line)
            if m:
                f=line.split(',');g,n=int(m[1]),int(m[2])
                if g==62000:f[0]='62300';f[1]=str(movement[n])
                elif g==62001:f[0]='62301'
                elif n<8:f[0]='62300' if n in (0,3) else '62301';f[1]=str({0:0,1:1,2:2,3:7,4:2,5:5,6:6,7:13}[n])
                line=','.join(f)
            lines.append(line)
        bank+='\n'+'\n'.join(lines)+'\n'
    (folder/'jin_mori.air').write_text(all_air+bank)
    cns=(folder/'Jin Mori.cns').read_text(encoding='utf-8')
    for n,args in NORMALS.items():cns=replace_state(cns,n,normal_state(n,*args))
    cns=replace_state(cns,190,INTRO);cns=replace_state(cns,191,INTRO.replace('[Statedef 190]','[Statedef 191]'))
    cns=replace_state(cns,4500,ULTIMATE.split('\n[Statedef 4501]')[0])
    cns=replace_state(cns,4501,'[Statedef 4501]'+ULTIMATE.split('\n[Statedef 4501]',1)[1])
    cns+=TRANSFORM
    buffer=''
    for i,key in enumerate(('a','b','c'),1):
        buffer+=f'\n[State -3, Buffer {key}]\ntype=MapSet\ntriggerall=!ishelper && time>1\ntriggerall=StateNo=230 || StateNo=240 || StateNo=250 || StateNo=260 || StateNo=270 || StateNo=280 || StateNo=290 || StateNo=310\ntrigger1=command="{key}"\nmap="mori.buffer"\nvalue={i}\n'
    buffer+='''
[State -3, Buffer lifespan]
type=MapSet
triggerall=!ishelper && time>1
trigger1=command="a" || command="b" || command="c"
map="mori.buffer_ticks"
value=12
[State -3, Buffer decay]
type=MapAdd
trigger1=map(mori.buffer_ticks)>0
map="mori.buffer_ticks"
value=-1
'''
    cns=cns.replace('[Statedef -3]','[Statedef -3]\n'+buffer)
    # Exclude helpers and foreign victim states from actor animation banking.
    helper_states=set()
    for b in re.split(r'(?=^\[State\b)',cns,flags=re.I|re.M):
        if re.search(r'(?im)^type\s*=\s*helper\s*$',b):
            m=re.search(r'(?im)^stateno\s*=\s*(\d+)',b)
            if m:helper_states.add(int(m[1]))
    roots=set(map(int,re.findall(r'(?im)^\[statedef\s+(\d+)',cns)))-helper_states-{190,191,315,820,821,4500,4501,4512,9804512,9804513,980500}
    cns=bank_controller_animations(cns,roots)
    (folder/'Jin Mori.cns').write_text(cns,encoding='utf-8')
    common=(folder/'common1.cns').read_text(encoding='utf-8')
    common=common.replace('[Statedef 0]','[Statedef 0]\nanim=0',1)
    common=bank_controller_animations(common,set(map(int,re.findall(r'(?im)^\[statedef\s+(\d+)',common))))
    (folder/'common1.cns').write_text(common,encoding='utf-8')
    cmd=(folder/'jin_mori.cmd').read_text(encoding='utf-8')
    cmd=cmd.replace('trigger1=ctrl\n','trigger1=ctrl\ntrigger2=(StateNo=230 || StateNo=240 || StateNo=250 || StateNo=260 || StateNo=270 || StateNo=280 || StateNo=290 || StateNo=310) && MoveContact && time>=8\n')
    # Transform/evade require neutral control, while skills can cancel a confirmed normal.
    for name in ('mori_transform','mori_dodge'):
        pattern=r'(?ms)(\[State -1, '+name+r'\].*?)(?=\[State |\Z)'
        cmd=re.sub(pattern,lambda m:re.sub(r'(?m)^trigger2=.*\n','',m[0]),cmd)
    (folder/'jin_mori.cmd').write_text(cmd,encoding='utf-8')
    (S/'upgrade-registration.json').write_text(json.dumps(registration,indent=2))
    (art/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen.imagegen',assets={n:dict(file=n+'.png',prompt=n+'.prompt.txt',sha256=hashlib.sha256((art/(n+'.png')).read_bytes()).hexdigest()) for n in ('monkey-movement','monkey-combat','story','effects')}),indent=2))
    return sprites
