"""Authored pancake dunk, five-fingers slap and mist-then-knockout ultimates."""
import hashlib,math,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from negan_execution import victim


def install(a,data,pack):
    result={}
    for form,info in enumerate(data):
        label=info['label']
        if label=='Negan':continue
        base=20000+form*1000;state=13210 if form else 4510 if label=='Tyrone Biggums' else 3210
        prefix='alt_' if form else ''
        def fx(number,im,axis,scale=1):
            pack(a,form,number,im,axis)
            a.air.extend([f'\n[Begin Action {base+number}]',f'{7000+form},{number},0,0,-1,,,{scale},{scale}'])
        def caption(number,text,size=38):
            im=Image.new('RGBA',(1140,100));draw=ImageDraw.Draw(im)
            font=ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',size)
            draw.text((570,50),text,font=font,anchor='mm',fill=(255,237,200,255),stroke_width=3,stroke_fill=(16,11,24,255))
            fx(number,im,(570,50))
        metadata={'revision':6,'state':state,'damage':950,'impact_tick':350,'duration':420}
        if label=='Prince':
            path=a.root/'sprite-fighter/characters/chappelle/art/finishers-v6/pancake-stack.png'
            with Image.open(path) as im:
                assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0
                w,h=im.size;fx(75,im,(w//2,round(h*.9)),.112)
            caption(70,'BREAKFAST IS SERVED')
            frames=[('walk_a',10),('walk_b',10)]*5+[('crouch',80),('special',150),('palm',30),('idle',60)]
            metadata.update(prop=str(path.relative_to(a.root)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sprite=[7000+form,75])
        elif label=='Rick James':
            caption(70,'WHAT DID THE FIVE FINGERS')
            caption(71,'SAY TO THE FACE?')
            caption(72,'SLAP!',68)
            frames=[('idle',60),('walk_a',14),('walk_b',14)]*2+[('idle',134),('walk_b',30),('palm',12),('idle',68)]
        else:
            caption(70,'POCKET MIST');caption(71,'LIGHTS OUT',52)
            frames=[('idle',60),('crouch',36),('palm',114),('walk_b',70),('walk_a',30),('walk_b',30),('palm',20),('idle',60)]
            yy,xx=np.mgrid[0:192,0:384];u=xx/383
            for frame in range(12):
                center=96+8*np.sin(xx*.025+frame*.6)
                width=8+u*64
                noise=np.clip(.62+.19*np.sin(xx*.041+yy*.093-frame*.8)+.12*np.sin(xx*.11-yy*.06+frame),.1,1)
                alpha=np.exp(-((yy-center)/width)**2*2)*np.sin(np.pi*u)**.65*noise*220
                alpha*=min(1,(frame+1)/3)*min(1,(12-frame)/4)
                pixels=np.zeros((192,384,4),dtype=np.uint8);pixels[:,:,:3]=(223,219,206);pixels[:,:,3]=alpha.astype(np.uint8)
                pack(a,form,80+frame,Image.fromarray(pixels),(0,96))
            a.air.append(f'\n[Begin Action {base+80}]')
            a.air.extend(f'{7000+form},{80+j},0,0,4,,,.85,.85' for j in range(12))
        assert sum(t for _,t in frames)==420,(label,frames)
        before=len(a.air);a.action(state,[(prefix+k,t) for k,t in frames])
        replacement='\n'.join(a.air[before:]);del a.air[before:]
        for i,b in enumerate(a.air):
            if re.match(r'\s*\[Begin Action '+str(state)+r'\]',b):a.air[i]=replacement;break
        info['positive']=[ultimate(state,base,label) if re.match(r'\s*\[Statedef '+str(state)+r'\]',b) else b for b in info['positive']]
        result[label]=metadata
    # Shared victim-owned reactions use their own art and stop camera drift.
    existing={int(re.match(r'\s*\[Statedef (\d+)\]',b)[1]) for f in data for b in f['positive']}
    for state in [8252,8253]:data[0]['positive'].append(captive(state))
    if 8262 not in existing:data[0]['positive'].append(victim(8262,5170,15170))
    return result


def captive(state):
    text=f'\n[Statedef {state}]\ntype=S\nmovetype=H\nphysics=N\nctrl=0\n'
    text+=f'[State {state}, Own active reaction]\ntype=ChangeAnim\ntrigger1=time=0\nvalue=ifelse((var(45)>0 || var(30)>0) && selfanimexist(15000),15000,5000)\n'
    for name,kind,body in [('Stop','VelSet','x=0\ny=0'),('Ground contact','PosSet','y=0'),('Hold framing','ScreenBound','value=0\nmovecamera=0,0'),('Capture protection','NotHitBy','value=SCA\ntime=1')]:
        text+=f'[State {state}, {name}]\ntype={kind}\ntrigger1=1\n{body}\n'
    if state==8252:
        text+=f'[State {state}, Dizzy stagger]\ntype=AngleDraw\ntrigger1=1\nvalue=4*sin(time*.14)\nscale=1,1\n'
    text+=f'[State {state}, Orphan safety]\ntype=SelfState\ntrigger1=time>600\nvalue=0\nctrl=1\n'
    return text


def ultimate(state,base,label):
    text=f'\n[Statedef {state}]\ntype=S\nmovetype=A\nphysics=N\nctrl=0\nanim={state}\nvelset=0,0\n'
    def ctl(name,kind,body):
        nonlocal text
        text+=f'\n[State {state}, {name}]\ntype={kind}\n{body}\n'
    def explod(name,t,anim,identity,pos,life,extra=''):
        ctl(name,'Explod',f'trigger1=time={t}\nanim={anim}\nID={identity}\npostype=left\npos={pos}\nremovetime={life}\nsprpriority=5\nownpal=1\n{extra}')
    ctl('Entry direction','VarSet','trigger1=time=0\nvar(44)=facing')
    ctl('Remember framing','VarSet','trigger1=time=0\nfvar(38)=camerapos x')
    ctl('Confirmed protection','NotHitBy','trigger1=1\nvalue=SCA\ntime=1')
    ctl('Lock framing','ScreenBound','trigger1=1\nvalue=0\nmovecamera=0,0')
    ctl('Grounded captive','TargetState','trigger1=time=0\nvalue=8253')
    release=370 if label=='Prince' else 350;distance=180 if label=='Prince' else 150
    ctl('Hold target','TargetBind',f'trigger1=time<{release}\npos=(fvar(38)+var(44)*{distance}-pos x)*facing,-pos y')
    ctl('Face target','Turn','trigger1=facing!=var(44)')
    if label=='Prince':
        x='fvar(38)+var(44)*(-180+220*min(1,max(0,(time-180)/170.0)))'
        y='ifelse(time>=180 && time<350,-150*sin(pi*(time-180)/170.0),0)'
    else:
        x='fvar(38)+var(44)*(-160+120*min(1,max(0,(time-280)/70.0)))';y='0'
    ctl('Authored approach','PosSet',f'trigger1=1\nx={x}\ny={y}')
    ctl('Illustrated setting','Explod',f'trigger1=time=0\nanim={base+40}\nID=6401\npostype=left\npos=0,0\nbindtime=-1\nremovetime=420\nsprpriority=-10\nownpal=1')
    if label=='Rick James':
        explod('Five fingers setup',45,base+70,6410,'640,130',120)
        explod('Question to the face',165,base+71,6410,'640,130',150)
        explod('SLAP',350,base+72,6411,'640,130',65)
    elif label=='Prince':
        ctl('Carry the pancakes','Explod',f'trigger1=time=180\nanim={base+75}\nID=6402\npostype=p1\npos=70,-375\nbindtime=-1\nremovetime=170\nsprpriority=6\nownpal=1')
        ctl('Dunk the plate','ModifyExplod','trigger1=time>=330 && time<350\nID=6402\npostype=p1\npos=70+3*(time-330),-375+2*(time-330)')
        ctl('Pancakes on the head','Explod',f'trigger1=time=350\nanim={base+75}\nID=6407\npostype=p2\npos=0,-335\nbindtime=-1\nremovetime=20\nsprpriority=6\nownpal=1')
        explod('Falling breakfast',370,base+75,6408,'640+var(44)*180,325',17,'velocity=0,12\naccel=0,1.3')
        explod('Breakfast on the floor',387,base+75,6409,'640+var(44)*225,660',33)
        explod('Breakfast served',350,base+70,6411,'640,125',65)
    else:
        explod('Pocket mist',70,base+70,6410,'640,130',160)
        for t in [108,144,180]:
            ctl('Mist into the face','Explod',f'trigger1=time={t}\nanim={base+80}\nID=6403\npostype=p1\npos=135,-320\nbindtime=-1\nremovetime=48\nsprpriority=5\nownpal=1')
        ctl('Dazed opponent','TargetState','trigger1=time=120\nvalue=8252')
        explod('Knockout caption',350,base+71,6411,'640,130',65)
    explod('Decisive contact',350,base+41,6405,f'640+var(44)*{distance},335',12,'scale=1.05,1.05')
    ctl('Impact flash','EnvColor','trigger1=time=350\nvalue=245,235,220\ntime=2\nunder=0')
    ctl('Heavy impact','EnvShake','trigger1=time=350\ntime=16\nampl=10\nfreq=70')
    ctl('Impact cue','PlaySnd','trigger1=time=350\nvalue=0,1')
    ctl('One decisive hit','HitAdd','trigger1=time=350\nvalue=1')
    ctl('Resolve once','TargetLifeAdd','trigger1=time=350\nvalue=-950\nkill=1')
    ctl('Release','TargetState',f'trigger1=time={release}\nvalue={8260 if label=="Rick James" else 8262}')
    ctl('Recover','ChangeState',f'trigger1=time>=419\nvalue={10000 if state>=10000 else 0}\nctrl=1')
    return text
