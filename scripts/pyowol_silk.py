"""Fine animated silk with hand-to-target registration; quiet execution art."""
from pathlib import Path
import json,math,re,struct
from PIL import Image,ImageDraw,ImageOps

THREAD_STATES=(210,410,610,1120,1121,3000,3200,3201,4000,4001)

def _register(A,key,path,number,axis):
    A.png(key,path,720,number,7200);A.meta[key]['scale']=1;A.meta[key]['axis']=axis
    h=list(struct.unpack('<HHHHhhHBBIIHH',A.headers[-1]));h[4:6]=axis
    A.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*h)

def load_silk(A):
    folder=A.source/'art/thread-v6';folder.mkdir(exist_ok=True)
    # Supersampling gives one soft filament, not several thick glowing beams.
    for phase,sag in enumerate((18,11,4,0,-1,0)):
        im=Image.new('RGBA',(1024,256));d=ImageDraw.Draw(im)
        points=[((8+240*t/120)*4,(32+sag*math.sin(math.pi*t/120))*4) for t in range(121)]
        d.line(points,fill=(210,221,235,195),width=4)
        glint=.18+phase*.13
        fragment=[((8+240*t/120)*4,(32+sag*math.sin(math.pi*t/120))*4) for t in range(max(0,round(glint*120)-3),min(121,round(glint*120)+4))]
        d.line(fragment,fill=(249,250,255,245),width=5)
        path=folder/f'silk-{phase}.png';im.resize((256,64),Image.Resampling.LANCZOS).save(path)
        _register(A,f'silk{phase}',path,phase,[8,32])
    for phase in range(3):
        im=Image.new('RGBA',(1024,256));d=ImageDraw.Draw(im);gap=(8+phase*32)*4
        for left,right,sign in ((8*4,128*4-gap,-1),(128*4+gap,248*4,1)):
            pts=[]
            for j in range(61):
                x=left+(right-left)*j/60;y=128+math.sin(j/60*math.pi)*sign*(4+phase*6)
                pts.append((x,y))
            d.line(pts,fill=(224,232,244,255),width=5)
        path=folder/f'snap-{phase}.png';im.resize((256,64),Image.Resampling.LANCZOS).save(path)
        _register(A,f'snap{phase}',path,6+phase,[8,32])
    for name,num in [('backdrop',9),('eye-cutin',10)]:
        source=Image.open(folder/f'{name}-source.png').convert('RGBA')
        if name=='backdrop':
            im=ImageOps.fit(source,(1280,720),method=Image.Resampling.LANCZOS)
            # A transparent corner keeps the shared PNG container's alpha contract.
            im.putpixel((0,0),(0,0,0,0))
        else:
            source.thumbnail((1280,720),Image.Resampling.LANCZOS)
            im=Image.new('RGBA',(1280,720));im.alpha_composite(source,((1280-source.width)//2,0))
        path=folder/f'{name}.png';im.save(path);_register(A,name,path,num,[0,0])
    # Restrained closing cut. Only a local diagonal flick, never a screen-wide X.
    for phase in range(3):
        im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im)
        d.line([(570+phase*22,405-phase*14),(710-phase*20,315+phase*15)],fill=(246,246,250,245),width=1)
        path=folder/f'cut-{phase}.png';im.save(path);_register(A,f'cut{phase}',path,11+phase,[640,360])
    # The ground snare has a fine loose coil, with no teeth or red markers.
    im=Image.new('RGBA',(2560,1440));d=ImageDraw.Draw(im)
    pts=[((380+520*j/160)*2,(650-4*math.sin(j/160*math.pi*4))*2) for j in range(161)]
    d.line(pts,fill=(222,230,242,245),width=3)
    d.arc((560*2,642*2,720*2,655*2),0,330,fill=(226,233,244,160),width=2)
    path=folder/'ground-silk.png';im.resize((1280,720),Image.Resampling.LANCZOS).save(path)
    _register(A,'ground-silk',path,14,[640,360])

def author_silk(A):
    A.action(7100,[(f'silk{i}',1 if i<3 else 2) for i in range(6)],hurt=False)
    A.action(7101,[('silk3',5),('silk4',2),('silk5',5)],hurt=False)
    A.action(7102,[('snap0',1),('snap1',2),('snap2',2)],hurt=False)
    A.action(7006,[('backdrop',-1)],hurt=False)
    A.action(7110,[('eye-cutin',8)],hurt=False)
    A.action(7111,[('cut0',1),('cut1',1),('cut2',2)],hurt=False)
    # HitDef sparks are not ordinary timed Explods. An infinite last frame
    # leaves them on screen across attacks (and across native test cases).
    A.action(7011,[('cut0',1),('cut1',1),('cut2',2)],hurt=False)
    A.action(7010,[('ground-silk',-1)],hurt=False,active=(0,),attack=(-260,-20,260,15))
    # Quiet choreography: one pass, stillness, and one decisive finishing pull.
    A.action(4001,[('u0',20),('u9',12),('u8',20),('u4',8),('u5',4),('u6',6),('u7',8),('u8',30),('u9',20),('u10',4),('u11',24)])

def _rig(A):
    lookup={(v['group'],v['number']):k for k,v in A.meta.items()}
    actions={};current=None
    for line in A.air:
        m=re.match(r'\s*\[Begin Action (\d+)\]',line)
        if m:current=int(m[1]);actions[current]=[]
        elif re.match(r'^\d+,\d+,',line) and current is not None:
            values=line.split(',');actions[current].append(lookup[int(values[0]),int(values[1])])
    hands={'a4':(15,-280),'a6':(45,-230),'a7':(35,-185),'a8':(0,-70),'a10':(40,-70),'a11':(45,-60),'a12':(50,-250),'a14':(100,-75),
           'u0':(20,-245),'u2':(30,-240),'u3':(50,-170),'u4':(-60,-150),'u7':(80,-130),'u8':(25,-245),'u10':(30,-170),'u11':(35,-170),'q0':(58,-160)}
    # Extended fingertips / dagger tips are the rightmost opaque edge, measured
    # in the registered image rather than guessed from a screen-space rectangle.
    for key in ('a5','a9','u1','u5','u6','u9'):
        m=A.meta[key];im=Image.open(A.root/m['file']);alpha=im.getchannel('A')
        edge=m['bounds'][2]-1
        ys=[y for y in range(im.height) if alpha.getpixel((edge,y))>200]
        if not ys:ys=[y for y in range(im.height) if alpha.getpixel((edge-1,y))>48]
        y=sum(ys)/max(1,len(ys))
        hands[key]=((edge-m['axis'][0])*m['scale'],(y-m['axis'][1])*m['scale'])
    expressions=[]
    for component in (0,1):
        expr='25' if component==0 else '-230'
        for number in reversed(THREAD_STATES):
            values=[hands.get(key,(25,-230))[component] for key in actions[number]]
            inner=f'{values[-1]:.3f}'
            for i in range(len(values)-2,-1,-1):inner=f'ifelse((root,animelemno(0))={i+1},{values[i]:.3f},{inner})'
            expr=f'ifelse((root,anim)={number},{inner},{expr})'
        expressions.append(expr)
    (A.source/'art/thread-v6/hand-registration.json').write_text(json.dumps(hands,indent=2))
    return expressions

def write_silk_states(A,state,ctl):
    hand_x,hand_y=_rig(A)
    for strand in range(3):
        n=8600+strand;state(n,7100,move='I',velset='0,0')
        valid=' || '.join(f'(root,stateno)={s}' for s in THREAD_STATES)
        ctl(n,'End with owner action','DestroySelf',f'!({valid}) || (root,life)<=0')
        ctl(n,'Normal filament fades','DestroySelf',f'time>=12 && ((root,stateno)=210 || (root,stateno)=410 || (root,stateno)=610)')
        ctl(n,'Strand index','VarSet','time=0',**{'var(0)':strand})
        ctl(n,'Follow facing','Turn','facing!=(root,facing)')
        ctl(n,'Registered fingertip X','VarSet',**{'fvar(2)':hand_x})
        ctl(n,'Registered fingertip Y','VarSet',**{'fvar(3)':hand_y})
        ctl(n,'Attach at hand','BindToRoot',time=1,pos='fvar(2),fvar(3)')
        ctl(n,'Hand to victim X','VarSet',**{'fvar(0)':'(root,p2dist x)-fvar(2)'})
        ctl(n,'Hand to victim Y','VarSet',**{'fvar(1)':'(root,p2dist y)-fvar(3)-ifelse((root,stateno)=410,30,205-var(0)*35)'})
        ctl(n,'Aim filament','AngleSet',value='ifelse(fvar(0)<0,180+atan(fvar(1)/max(1,abs(fvar(0))))*57.29578,-atan(fvar(1)/max(1,abs(fvar(0))))*57.29578)')
        ctl(n,'Reach victim','AngleDraw',scale='max(.01,(fvar(0)*fvar(0)+fvar(1)*fvar(1))**.5/240),1')
        ctl(n,'Taut shimmer','ChangeAnim',['time>=8','anim=7100'],value=7101)
        ctl(n,'Final snap','ChangeAnim',['(root,stateno)=4001','(root,time)>=128','anim!=7102'],value=7102)
        ctl(n,'Snap vanishes','DestroySelf',['anim=7102','animtime=0'])
        ctl(n,'Subtle opacity','VarSet',**{'var(1)':'ifelse((root,stateno)=4001,ifelse((root,time)<108,65,180),180)'})
        ctl(n,'Silk transparency','Trans',trans='addalpha',alpha='var(1),256-var(1)')
        ctl(n,'No body collision','PlayerPush',value=0)
        ctl(n,'Draw over sleeves','SprPriority',value=3)

def spawn_silk(ctl,n,t,strands=1):
    for strand in range(strands):
        ctl(n,'Silk from fingertips','Helper',[f'time={t}',f'numhelper({8600+strand})=0'],name='Silk filament',ID=8600+strand,stateno=8600+strand,postype='p1',pos='0,0',ownpal=1,keyctrl=0)

def write_silk_review(folder,report):
    from html import escape
    root=Path(folder);dest=root/'art/thread-v6'
    shots=[]
    choices=[('Silk Finger',34,'A fine cast from the hand'),('Ankle Thread',34,'Low silk at the ankle'),('Thread Reel',42,'Drawing the filament taut'),('Heavenly Silk Prison',65,'Three strands, without the radial web'),('Reaper of the Drifting Moon',36,'A momentary glance'),('Reaper of the Drifting Moon',98,'One unseen pass'),('Reaper of the Drifting Moon',151,'Stillness before the cut'),('Reaper of the Drifting Moon',165,'The finishing cut')]
    for case,tick,caption in choices:
        frames=[f for f in report['frames'] if f['case_name']==case]
        if not frames:continue
        frame=min(frames,key=lambda f:abs(f['case_tick']-tick))
        src='../../replays/'+frame.get('capture_directory',report['capture_directory'])+'/'+frame['file']
        shots.append('<figure><img src="'+escape(src)+'" alt="'+escape(caption)+'"><figcaption>'+escape(caption)+'</figcaption></figure>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pyo Wol — subtle silk and quiet execution</title>
<style>body{margin:0;background:#090d14;color:#f1f1f8;font:16px/1.6 system-ui}main{max-width:1280px;margin:auto;padding:28px 18px}a{color:#c9b8ff}p{max-width:850px;color:#b9c3d5}figure{margin:28px 0}img{display:block;width:100%;height:auto}figcaption{padding:8px 0;color:#bbc4d8}</style>
<main><a href="../../review.html">Play the in-game captures</a><h1>Subtle silk. One finishing cut.</h1><p>The quiet direction uses thin hand-anchored filaments, one unseen pass and a final pull. The red disk, radial web and persistent star marks are gone. These are actual engine captures; use the combat review to see them moving.</p>'''+''.join(shots)+'''<p><a href="notes.md">Changes and artwork prompts</a> · <a href="provenance.json">Art provenance</a></p></main></html>'''
    (dest/'review.html').write_text(page,encoding='utf-8')
