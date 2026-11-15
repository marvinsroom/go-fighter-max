"""Meter-move anticipation, distinct weapon energy and confirmed impact accents."""
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
from jinwoo_hybrid_art import drawing

COLORS=((180,75,255),(180,75,255),(40,170,255),(255,45,105),
        (100,190,255),(55,235,255),(150,235,255),(225,205,255))
MODERN_ACTIONS=(879860,879861,879862)


def modern_effects(root):
    """Pack the illustrated dagger, greatsword and Monarch VFX atlas."""
    path=Path(root)/'sprite-fighter/characters/jinwoo/art/effects/super-ultimate-v4.png'
    with Image.open(path) as source:
        source=source.convert('RGBA')
        assert source.size==(1536,1024),source.size
        out={}
        ys=(0,341,683,1024)
        for row in range(3):
            for col in range(4):
                rect=(col*384,ys[row],(col+1)*384,ys[row+1])
                tile=source.crop(rect)
                out[61013,row*4+col]=drawing(tile,(192,tile.height-20),.5,
                    str(path.relative_to(root)),rect)
    return out


def modern_air():
    out=[]
    for row,action in enumerate(MODERN_ACTIONS):
        out.append(f'[Begin Action {action}]')
        for col,t in enumerate((3,3,5,9)):
            out.append(f'61013,{row*4+col},0,0,{t},,A,.5,.5')
    return '\n'+'\n'.join(out)+'\n'


def effects():
    art={}
    for kind,color in enumerate(COLORS):
        for frame in range(8):
            im=Image.new('RGBA',(640,480));d=ImageDraw.Draw(im);a=max(150,255-frame*16)
            def line(points,width=12):
                d.line(points,fill=(*color,a),width=width,joint='curve')
                d.line(points,fill=(235,245,255,a),width=max(2,width//4),joint='curve')
            if kind==0:
                radius=55+frame*22
                d.ellipse((320-radius,360-radius*.24,320+radius,360+radius*.24),outline=(*color,a),width=8)
                for i in range(9):
                    x=160+i*38;line((x,350,x+12,290-frame*12),5)
            elif kind in (1,4):
                for i in range(3 if kind==1 else 4):
                    y=80+i*72+frame*3
                    line((45,y+100,250,y+20,570,y-20),18 if kind==1 else 14)
                if kind==1:line((100,390,540,60),14)
            elif kind in (2,3):
                for offset in ((0,) if kind==2 else (-35,35)):
                    box=(65,20+offset,575,450+offset)
                    d.arc(box,-125+frame*8,115+frame*8,fill=(*color,a),width=32)
                    d.arc(box,-115+frame*8,105+frame*8,fill=(235,250,255,a),width=7)
                if kind==3:line((80,60,560,410),14)
            elif kind==5:
                line((280,20,350,350),36)
                for i in range(7):
                    x=90+i*75;line((320,365,x,290-abs(i-3)*25),10)
                d.ellipse((75,325,590,425),outline=(*color,a),width=14)
            elif kind==6:
                for i in range(7):
                    x=75+i*75;h=90+(i%3)*55
                    d.polygon((x-18,385,x+12,385-h,x+27,385),fill=(*color,a),outline=(235,250,255,a))
                d.arc((50,100,590,450),-100,105,fill=(*color,a),width=18)
            else:
                radius=35+frame*22
                d.ellipse((320-radius,240-radius,320+radius,240+radius),outline=(*color,a),width=max(2,14-frame))
                for i in range(12):
                    angle=i*math.pi/6;near=25+frame*9;far=85+frame*13
                    line((320+math.cos(angle)*near,240+math.sin(angle)*near,320+math.cos(angle)*far,240+math.sin(angle)*far),7)
            im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(10)),im)
            art[61008,kind*8+frame]=drawing(im,(240,240),.20,'procedural super energy: scripts/jinwoo_super_power.py')
    return art


def air():
    out=[]
    for kind in range(8):
        out.append(f'[Begin Action {879830+kind}]')
        for frame in range(8):out.append(f'61008,{kind*8+frame},0,0,2,,A,.20,.20')
    return '\n'+'\n'.join(out)+'\n'


def start(n):
    return f'''
[State {n}, Super energy gathers]
type=Explod
trigger1=!time
anim=879862
ID=879840
postype=p1
pos=0,-22
scale=.85,.85
sprpriority=-1
ownpal=1
supermovetime=12
removetime=-2
persistent=0
[State {n}, Super anticipation]
type=SuperPause
trigger1=!time
time=8
movetime=0
anim=-1
sound=-1
darken=0
unhittable=0
persistent=0
[State {n}, Arena contrast]
type=BGPalFX
trigger1=!time
time=14
mul=150,135,185
add=0,0,0
persistent=0
[State {n}, Power release sound]
type=PlaySnd
trigger1=!time
value=S5,54
volumescale=90
persistent=0
'''


def impact(n,t,last=False):
    return f'''
[State {n}, Confirmed super impact]
type=Explod
trigger1=time={t+1} && movehit
anim=879837
ID=879842
postype=p1
pos=44,-33
scale={'.85,.85' if last else '.5,.5'}
sprpriority=5
ownpal=1
removetime=-2
persistent=0
[State {n}, Super impact weight]
type=EnvShake
trigger1=time={t+1} && movehit
time={10 if last else 5}
ampl={-3 if last else -1}
freq=65
persistent=0
[State {n}, Heavy hit sound]
type=PlaySnd
trigger1=time={t+1} && movehit
value=S5,47
volumescale={100 if last else 65}
persistent=0
'''
