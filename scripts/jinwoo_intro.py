"""Igris enters first; Shadow Exchange replaces him with a composed Jinwoo."""
import math,re
from PIL import Image
from jinwoo_hybrid_art import drawing


def portal():
    # A code-drawn floor ellipse, independent of the old pixel effect artwork.
    im=Image.new('RGBA',(512,160));pixels=im.load()
    for y in range(160):
        for x in range(512):
            r=math.hypot((x-255.5)/222,(y-79.5)/48)
            glow=math.exp(-((r-1)/.13)**2)
            inside=max(0,min(1,(1-r)*32))
            a=round(max(inside*.97,glow*.72)*255)
            pixels[x,y]=(round(9+100*glow),round(4+44*glow),round(22+170*glow),a)
    return drawing(im,(256,80),.20,'procedural shadow portal: scripts/jinwoo_intro.py')


def air(art):
    out=['\n[Begin Action 878510]','61006,0,0,0,-1,,,0.20,0.20','\n[Begin Action 878500]']
    for name,ticks in (('idle',-1),):
        m=art['base:'+name]
        out.append(f"{m['group']},{m['number']},0,0,{ticks},,,{m['scale']},{m['scale']}")
    for action,poses in ((878511,(1,2,3,4,5,6)),(878512,(0,))):
        out.append(f'[Begin Action {action}]')
        for pose in poses:
            m=art[f'igris:movement:{pose}']
            out.append(f"{m['group']},{m['number']},0,0,{5 if action==878511 else -1},,,{m['scale']},{m['scale']}")
    return '\n'.join(out)+'\n'


def adapt(text,filename):
    if filename=='-2.cns':
        # The source's independent pre-round pillar obscures the exchange.
        # Disable only that decorative intro helper, retaining gameplay helpers.
        blocks=re.split(r'(?=^\[state\s)',text,flags=re.I|re.M)
        return ''.join(re.sub(r'(?im)^(\s*type\s*=\s*)helper\s*$',r'\1Null',b) if re.search(r'(?im)^\s*stateno\s*=\s*99015\s*$',b) else b for b in blocks)
    if filename!='cns.cns':return text
    return re.sub(r'(?im)^\[statedef 190\][\s\S]*?(?=^\[statedef (?!191\b))',intro(),text,count=1)


def intro():
    return '''[Statedef 190]
type=S
physics=N
movetype=I
ctrl=0
velset=0,0
anim=6
[State 190, Begin shadow arrival]
type=ChangeState
trigger1=1
value=191

[Statedef 191]
type=S
physics=N
movetype=I
ctrl=0
velset=0,0
anim=6
sprpriority=1
[State 191, Hold the introduction]
type=AssertSpecial
trigger1=1
flag=intro
flag2=noshadow
[State 191, Feet on the floor]
type=PosSet
trigger1=1
y=0
[State 191, Open the shadow]
type=Helper
trigger1=!time
name="Shadow arrival pool"
ID=878510
stateno=878510
postype=p1
pos=0,0
ownpal=1
keyctrl=0
size.xscale=1.8
size.yscale=1.8
[State 191, Arrival sound]
type=PlaySnd
trigger1=time=48
value=S5,54
[State 191, Shadow scout enters first]
type=Helper
trigger1=!time
name="Igris shadow exchange"
ID=878511
stateno=878511
postype=p1
pos=-30,0
ownpal=1
keyctrl=0
size.xscale=1.5
size.yscale=1.5
[State 191, Exchange places]
type=ChangeAnim
trigger1=time=48
value=878500
[State 191, Keep Jinwoo hidden until the exchange]
type=Trans
trigger1=time<48
trans=addalpha
alpha=0,256
[State 191, Brief exchange flash]
type=PalFX
trigger1=time>=48 && time<54
time=1
mul=180,150,256
add=20,0,40
[State 191, Finish arrival]
type=ChangeState
trigger1=time>=108
value=0
ctrl=1

'''


def states():
    return '''
[Statedef 878511]
type=S
physics=N
movetype=I
ctrl=0
anim=878511
velset=1,0
sprpriority=1
[State 878511, No collision]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 878511, No floor shadow]
type=AssertSpecial
trigger1=1
flag=noshadow
[State 878511, Arrive at exchange point]
type=VelSet
trigger1=time>=30
x=0
[State 878511, Stand guard]
type=ChangeAnim
trigger1=time=30
value=878512
[State 878511, Purple exchange silhouette]
type=PalFX
trigger1=time>=42
time=1
mul=100,50,180
add=20,0,50
[State 878511, Swap instantly and clean up on skip]
type=DestroySelf
trigger1=parent,time>=48
trigger2=parent,stateno!=191

[Statedef 878510]
type=S
physics=N
movetype=I
ctrl=0
anim=878510
velset=0,0
sprpriority=-2
[State 878510, No hit collision]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 878510, No extra floor shadow]
type=AssertSpecial
trigger1=1
flag=noshadow
[State 878510, Follow arrival position]
type=BindToParent
trigger1=1
pos=0,0
[State 878510, Open and close]
type=AngleDraw
trigger1=1
scale=1.8*min(1,(time+1)/20.0)*max(0,min(1,(108-time)/28.0)),1.8*min(1,(time+1)/20.0)*max(0,min(1,(108-time)/28.0))
[State 878510, Leave no portal after an intro skip]
type=DestroySelf
trigger1=parent,stateno!=191
trigger2=time>=108
'''
