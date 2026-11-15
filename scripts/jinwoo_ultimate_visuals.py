"""Illustrated ultimate armies and purple Mutilate effects; native hits stay intact."""
import re

FORMS=('igris','beru','iron','tank')
ACTOR=878400
ANIM=878420


def set_parameter(block,name,value):
    pattern=r'(?im)^\s*'+re.escape(name)+r'\s*=.*$'
    if re.search(pattern,block):return re.sub(pattern,name+'='+value,block)
    return block.rstrip()+'\n'+name+'='+value+'\n'


def adapt(text,filename):
    out=[]
    for block in re.split(r'(?=^\[statedef\s+)',text,flags=re.I|re.M):
        match=re.match(r'\[statedef\s+(\d+)\]',block,re.I)
        if not match:out.append(block);continue
        state=int(match[1]);parts=[]
        for controller in re.split(r'(?=^\[state\s)',block,flags=re.I|re.M):
            kind=re.search(r'(?im)^\s*type\s*=\s*(\w+)',controller)
            animation=re.search(r'(?im)^\s*anim\s*=\s*(.*)',controller)
            value=animation[1].split(';')[0].strip() if animation else ''
            if filename=='cns.cns' and state in (3000,3010,3020,3030) and kind:
                # Native ultimate presentation helpers inherit remapped human
                # body animations and accumulate as duplicate mini Jinwoos.
                # State 3000 only needs its timing; its helpers are decorative.
                if state==3000 and kind[1].lower()=='helper':
                    controller=set_parameter(controller,'type','Null')
                if kind[1].lower()=='explod':
                    # All native ultimate Explods are low-resolution imported
                    # effects. Modern 879860-879862 layers are injected below.
                    controller=set_parameter(controller,'type','Null')
                if kind[1].lower()=='helper' and re.search(r'(?im)^\s*stateno\s*=\s*30[45]0\s*$',controller):
                    controller=set_parameter(controller,'ownpal','1')
            if filename=='Mode.cns' and state==3210 and kind and kind[1].lower()=='explod':
                if value in ('3274','3275','6221'):
                    # Extra native Tusk/Kaisel pictures are not our four actors.
                    controller=set_parameter(controller,'type','Null')
                elif value in ('3050','3230'):
                    controller=set_parameter(controller,'type','Null')
                elif value in ('3270','3271','3272','3273'):
                    i=int(value)-3270
                    controller=set_parameter(controller,'anim',str(ANIM+i))
                    # Match transform actor size; plant beside Jinwoo, not screen-left.
                    size=1.8 if i==3 else 1.5
                    controller=set_parameter(controller,'scale',f'{size},{size}')
                    controller=set_parameter(controller,'postype','p1')
                    controller=set_parameter(controller,'pos',f'{(i-1.5)*48:.1f},0')
                    controller=set_parameter(controller,'vel','0,0')
                    controller=set_parameter(controller,'bindtime','-1')
                    controller=set_parameter(controller,'sprpriority',str(-4+i))
                    controller=set_parameter(controller,'removetime','100')
                elif re.fullmatch(r'3260\s*\+\s*\(random\s*%\s*3\)',value):
                    controller=set_parameter(controller,'anim',f'{ANIM}+(floor(time/6)%4)')
                    controller=set_parameter(controller,'postype','p1')
                    controller=set_parameter(controller,'pos','p2dist x-40+random%20,-pos y')
                    controller=set_parameter(controller,'scale','1.5,1.5')
                    controller=set_parameter(controller,'removetime','24')
                elif not value.startswith('87842'):
                    # Retire the old pixel aura, rocks, wipes and slashes.
                    controller=set_parameter(controller,'type','Null')
            if filename=='Mode.cns' and state==3210 and kind and kind[1].lower()=='helper':
                # Native Antares helpers inherit player animation banks and
                # render a vertical stack of Jinwoo bodies. Approved shadow
                # actors are supplied separately as 878420-878423 Explods.
                controller=set_parameter(controller,'type','Null')
            parts.append(controller)
        block=''.join(parts)
        if filename=='cns.cns' and state in (3080,3090):
            # Some opponents inherit a blank common 5300. A shadow assault
            # needs their actual own hit-reaction drawing to remain visible.
            own='cond(var(45)>0 && selfanimexist(var(45)*1000000+5000),var(45)*1000000+5000,cond(var(30)=1 && selfanimexist(15000),15000,cond(selfanimexist(5000),5000,0)))'
            if state==3080:
                block=re.sub(r'(?im)^anim\s*=.*$','anim='+own,block,count=1)
            else:
                block=re.sub(r'(?im)^value\s*=\s*cond\([^\n]+$','value='+own,block,count=1)
        addition=''
        if filename=='cns.cns' and state==3000:
            for i in range(4):
                addition+=f'\n[State 3000, Reset ultimate shadow evidence]\ntype=MapSet\ntrigger1=!time\nmap="ultimate.shadow{i}"\nvalue=0\n'
        if filename=='cns.cns' and state==3030:
            for i in range(4):
                # Match playable transform body scale (1.5; Tank 1.8).
                size=1.8 if i==3 else 1.5
                addition+=f'''
[State 3030, {FORMS[i]} coordinated strike]
type=Helper
trigger1=time={35+i*50}
trigger2=time={207+i*2}
helpertype=normal
name="{FORMS[i]} ultimate strike"
ID={ACTOR+i}
stateno={ACTOR+i}
postype=p1
pos=p2dist x-{90 if i==3 else 66},-pos y
ownpal=1
keyctrl=0
size.xscale={size}
size.yscale={size}
[State 3030, Observe {FORMS[i]} strike]
type=MapSet
trigger1=numhelper({ACTOR+i})>0
map="ultimate.shadow{i}"
value=1
'''
            # Dedicated violet slash trails while Jinwoo's assault runs.
            for t in (12,28,44,60,76,92,108,124):
                addition+=f'''
[State 3030, Violet dagger trail]
type=Explod
trigger1=time={t}
                anim=879860
ID=879850
postype=p1
pos=42,-34
facing=1
scale=.85,.55
sprpriority=5
ownpal=1
remappal=3,19
removetime=-2
persistent=0
'''
        if filename=='cns.cns' and state in (3040,3050):
            for palette in (0,2,3,4,20):
                addition+=f'\n[State {state}, Violet impact palette]\ntype=RemapPal\ntrigger1=1\nsource=3,{palette}\ndest=3,19\n'
        if filename=='cns.cns' and state in (3000,3010,3020,3030):
            action=879862 if state==3000 else 879860
            times=(0,18,36) if state==3030 else (0,)
            for t in times:
                addition+=f'''\n[State {state}, Modern illustrated ultimate effect]
type=Explod
trigger1=time={t}
anim={action}
ID=879860
postype=p1
pos=0,-24
scale={1.25 if state==3000 else .95},{1.25 if state==3000 else .95}
sprpriority={-2 if state==3000 else 5}
ownpal=1
removetime=-2
persistent=0
'''
        if filename=='Mode.cns' and state==3210:
            for t in (0,36,72):
                addition+=f'''\n[State 3210, Modern Shadow Monarch eruption]
type=Explod
trigger1=time={t}
anim=879862
ID=879862
postype=p1
pos=0,-18
scale=1.15,1.15
sprpriority={-3 if t==0 else 4}
ownpal=1
removetime=-2
persistent=0
'''
        if addition:
            first=re.search(r'(?im)^\[state\s',block)
            assert first,state
            block=block[:first.start()]+addition+block[first.start():]
        out.append(block)
    return ''.join(out)


def states():
    out=[]
    for i,name in enumerate(FORMS):
        n=ACTOR+i
        out.append(f'''
[Statedef {n}]
type=S
movetype=I
physics=N
anim={ANIM+i}
velset=0,0
ctrl=0
[State {n}, No unrelated collision]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State {n}, No ground shadow]
type=AssertSpecial
trigger1=1
flag=noshadow
[State {n}, Face the captured target]
type=Turn
trigger1=p2dist x<0
[State {n}, Approach]
type=VelSet
trigger1=time<22
x=4.5
[State {n}, Plant for the strike]
type=VelSet
trigger1=time>=22
x=0
[State {n}, Fade]
type=Trans
trigger1=1
trans=addalpha
alpha=cond(time<4,time*64,cond(time>40,(48-time)*32,256)),cond(time<4,256-time*64,cond(time>40,256-(48-time)*32,0))
[State {n}, End visual assault]
type=DestroySelf
trigger1=time>=48
trigger2=parent,stateno!=3030
''')
    return '\n'.join(out)


def air(art):
    out=[]
    poses=((9,9,10,10,2,3,4,11),(0,1,2,3,4,5,6,7),(9,9,10,10,6,7,11,11),(5,5,6,6,7,7,4,11))
    for i,name in enumerate(FORMS):
        out.append(f'[Begin Action {ANIM+i}]')
        for pose,ticks in zip(poses[i],(6,4,6,4,4,4,6,8)):
            m=art[f'{name}:combat:{pose}']
            out.append(f"{m['group']},{m['number']},0,0,{ticks},,,{m['scale']},{m['scale']}")
    return '\n'+'\n'.join(out)+'\n'
