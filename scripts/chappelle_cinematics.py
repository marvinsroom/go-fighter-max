"""Illustrated cinematic stages and restrained, animated contact effects.

Scene PNGs are archived unchanged. SFF stores their decoded RGBA pixels;
character art, calibrated AIR poses, damage and capture mechanics stay intact.
"""
import hashlib, math, re, struct
from pathlib import Path
from PIL import Image, ImageDraw

SCENES={'Prince':'prince','Rick James':'rick','Tyrone Biggums':'tyrone','Negan':'negan'}
PALETTES={'Prince':(205,175,255),'Rick James':(255,197,115),
          'Tyrone Biggums':(234,207,154),'Negan':(255,189,127)}


def pack(a,form,number,im,axis):
    im=im.convert('RGBA');w,h=im.size
    # Native true-color blending expects premultiplied channels. Opaque scene
    # pixels remain identical; fading effects must not brighten as alpha drops.
    raw=im.convert('RGBa').tobytes();offset=len(a.payload)
    a.payload.extend(raw)
    a.headers.append(struct.pack('<HHHHhhHBBIIHH',7000+form,number,w,h,*axis,0,0,32,offset,len(raw),0,0))


def effects(a,form,label):
    """Code-native tapered sparks, slashes and angular dust; no ring sprites."""
    color=PALETTES[label];base=20000+form*1000
    for kind,first in [('contact',41),('slash',47),('dust',53)]:
        for frame in range(6):
            im=Image.new('RGBA',(768,768));d=ImageDraw.Draw(im);t=frame/5
            if kind=='contact':
                for j in range(9):
                    angle=j*2.399+.23;reach=(25+50*t)*(1+(j%3)*.25)
                    start=12+48*t;end=start+reach*(1-t*.7);width=5*(1-t*.65)
                    ux,uy=math.cos(angle),math.sin(angle);vx,vy=-uy,ux
                    pts=[(384+ux*start*3,384+uy*start*3),
                         (384+(ux*(start+9)+vx*width)*3,384+(uy*(start+9)+vy*width)*3),
                         (384+ux*end*3,384+uy*end*3),
                         (384+(ux*(start+9)-vx*width)*3,384+(uy*(start+9)-vy*width)*3)]
                    d.polygon(pts,fill=(*color,round(235*(1-t*.9))))
                if frame<3:
                    d.line([(240,460),(525,285)],fill=(255,250,233,230-frame*65),width=9-frame*2)
            elif kind=='slash':
                for j in range(3):
                    points=[]
                    for step in range(31):
                        u=step/30
                        points.append(((1-u)**2*95+2*(1-u)*u*200+u*u*650,
                                       (1-u)**2*590+2*(1-u)*u*150+u*u*180+j*24+frame*9))
                    for step in range(30):
                        width=max(2,round((4+9*math.sin(step/30*math.pi))*(1-j*.2)))
                        d.line(points[step:step+2],fill=(*color,int((160-j*35)*(1-t*.9))),width=width)
            else:
                for j in range(15):
                    side=-1 if j%2 else 1;dx=side*(15+(j*31)%90)*(t+.15)
                    dy=-(15+j%5*13)*math.sin(t*math.pi*.8)
                    x=384+dx*3;y=650+dy*3;s=(5+j%4*3)*(1-t*.65)*3
                    d.polygon([(x-s,y),(x-s*.35,y-s*.7),(x+s*.8,y-s*.4),(x+s,y+s*.3)],
                              fill=(*color,int(150*(1-t))))
            pack(a,form,first+frame,im.resize((256,256),Image.Resampling.LANCZOS),(128,128 if kind!='dust' else 217))
        a.air.append(f'\n[Begin Action {base+first}]')
        for frame in range(6):a.air.append(f'{7000+form},{first+frame},0,0,{2 if kind!="dust" else 3},,,1,1')


def controller(state,label,kind,body):
    return f'\n[State {state}, {label}]\ntype={kind}\n{body}\n'


def rewrite(block,form,label):
    state=int(re.match(r'\s*\[Statedef (\d+)\]',block)[1])
    ult=state in {3210,4510,13210};last=350 if ult else 190;duration=420 if ult else 240
    base=20000+form*1000;parts=re.split(r'(?=\[State\s)',block,flags=re.I);out=parts[0]
    for part in parts[1:]:
        typ=re.search(r'^type\s*=\s*(\w+)',part,re.M|re.I)
        if not typ:out+=part;continue
        kind=typ[1].lower()
        if kind=='explod':
            # Only the authored title remains from the original visual layer.
            if 'ID=6411' in part:
                part=re.sub(r'^pos=.*$', 'pos=640,125',part,flags=re.M)
                part=re.sub(r'^scale=.*$', 'scale=.85,.85',part,flags=re.M)
                out+=part
            continue
        if kind in {'afterimage','afterimagetime'}:continue
        if kind=='envcolor':
            part=re.sub(r'^time=.*$', 'time=2',part,flags=re.M)
            part=re.sub(r'^value=.*$', 'value=245,235,220',part,flags=re.M)
        if kind=='envshake':
            part=re.sub(r'^ampl=.*$', 'ampl=8' if 'Final' in part else 'ampl=2',part,flags=re.M)
        out+=part
    out+=controller(state,'Illustrated setting','Explod',f'trigger1=time=0\nanim={base+40}\nID=6401\npostype=left\npos=0,0\nbindtime=-1\nremovetime={duration}\nsprpriority=-10\nownpal=1')
    targets={
        'Prince':('640+var(44)*210',f'580-230*abs(sin(time*pi/{last}))'),
        'Rick James':('640+var(44)*120','615-120*abs(sin(time*.08))'),
        'Tyrone Biggums':('640+var(44)*60*sin(time*.11)','620-120*abs(sin(time*.16))'),
        'Negan':('640+var(44)*150','620-230*abs(sin(time*.045))')}
    x,y=targets[label]
    for t in list(range(30,last-12,24))+[last]:
        final=t==last
        out+=controller(state,'Contact streaks','Explod',f'trigger1=time={t}\nanim={base+41}\nID=6405\npostype=left\npos={x},({y})-125\nremovetime=12\nscale={1.15 if final else .52},{1.15 if final else .52}\nsprpriority=5\nownpal=1')
        if label=='Negan':
            out+=controller(state,'Lucille motion','Explod',f'trigger1=time={t-2}\nanim={base+47}\nID=6403\npostype=p1\npos=130,-230\nfacing=1\nremovetime=10\nscale=.9,.9\nsprpriority=3\nownpal=1')
    if label=='Prince':
        # Readable basketball-size shots instead of oversized falling ball spam.
        for j,t in enumerate(range(36,last-30,42)):
            out+=controller(state,'Royal cross-court shot','Explod',f'trigger1=time={t}\nanim={base}\nID=6403\npostype=left\npos=640-var(44)*230,{195+j%3*35}\nvelocity=var(44)*11,-7\naccel=0,.65\nremovetime=40\nscale=.38,.38\nsprpriority=2\nownpal=1')
    for t in [last-12,last,last+8]:
        out+=controller(state,'Landing debris','Explod',f'trigger1=time={t}\nanim={base+53}\nID=6406\npostype=left\npos=640+var(44)*100,660\nremovetime=18\nscale=1.5,1.5\nsprpriority=3\nownpal=1')
    return out


def install(a,data):
    result={}
    for form,info in enumerate(data):
        label=info['label'];slug=SCENES[label]
        path=a.root/'sprite-fighter/characters/chappelle/art/cinematics-v5'/f'{slug}-scene.png'
        with Image.open(path) as im:
            w,h=im.size;pack(a,form,40,im,(0,0))
        a.air.extend([f'\n[Begin Action {20040+form*1000}]',f'{7000+form},40,0,0,-1,,,{1280/w:.9f},{720/h:.9f}'])
        effects(a,form,label)
        confirmed={3010,3210,4410,4510} if form==0 else {13010,13210}
        info['positive']=[rewrite(b,form,label) if int(re.match(r'\s*\[Statedef (\d+)\]',b)[1]) in confirmed else b for b in info['positive']]
        result[label]={'scene':str(path.relative_to(a.root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                       'size':[w,h],'sprite':[7000+form,40],'revision':5,'legacy_rings_and_prop_overlays':False}
    return result
