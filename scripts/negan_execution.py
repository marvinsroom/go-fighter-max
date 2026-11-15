"""Negan's grounded execution-style ultimate, with a cut on the single blow."""
import hashlib,re
from PIL import Image


def install(a,data,pack):
    for form,info in enumerate(data):
        if info['label']!='Negan':continue
        assert form==1
        path=a.root/'sprite-fighter/characters/chappelle/art/negan-execution-v1/night-clearing.png'
        with Image.open(path) as im:
            w,h=im.size;pack(a,form,64,im,(0,0))
        pack(a,form,59,Image.new('RGBA',(1280,42),(0,0,0,255)),(0,0))
        a.air.extend(['\n[Begin Action 21064]',f'7001,64,0,0,-1,,,{1280/w:.9f},{720/h:.9f}',
                      '\n[Begin Action 21059]','7001,59,0,0,-1,,,1,1'])
        # Walk up, pause with the bat, long overhead wind-up, then cut on impact.
        frames=[('alt_'+key,18) for _ in range(4) for key in ['walk_a','walk_b']]
        frames += [('alt_idle',106),('alt_special',100),('alt_palm',6),('alt_idle',64)]
        before=len(a.air);a.action(13210,frames)
        replacement='\n'.join(a.air[before:]);del a.air[before:]
        for i,block in enumerate(a.air):
            if re.match(r'\s*\[Begin Action 13210\]',block):a.air[i]=replacement;break
        info['positive']=[ultimate() if re.match(r'\s*\[Statedef 13210\]',b) else b for b in info['positive']]
        info['positive'].extend([victim(8251,10,10010),victim(8262,5170,15170)])
        return {'revision':1,'scene':str(path.relative_to(a.root)),
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':[w,h],
                'sprite':[7001,64],'kneeling_state':8251,'aftermath_state':8262,
                'impact_tick':350,'damage':950,'duration':420}
    return None


def ultimate():
    text='\n[Statedef 13210]\ntype=S\nmovetype=A\nphysics=N\nctrl=0\nanim=13210\nvelset=0,0\n'
    def ctl(name,kind,body):
        nonlocal text
        text+=f'\n[State 13210, {name}]\ntype={kind}\n{body}\n'
    ctl('Entry direction','VarSet','trigger1=time=0\nvar(44)=facing')
    ctl('Remember framing','VarSet','trigger1=time=0\nfvar(38)=camerapos x')
    ctl('Confirmed protection','NotHitBy','trigger1=1\nvalue=SCA\ntime=1')
    ctl('Lock framing','ScreenBound','trigger1=1\nvalue=0\nmovecamera=0,0')
    ctl('Kneeling captive','TargetState','trigger1=time=0\nvalue=8251')
    ctl('Slow approach','PosSet','trigger1=1\nx=fvar(38)-var(44)*(260-180*min(1,time/144.0))\ny=0')
    ctl('Hold the low captive','TargetBind','trigger1=time<350\npos=(fvar(38)+var(44)*110-pos x)*facing,-pos y')
    ctl('Face captive','Turn','trigger1=facing!=var(44)')
    ctl('Night clearing','Explod','trigger1=time=0\nanim=21064\nID=6401\npostype=left\npos=0,0\nbindtime=-1\nremovetime=420\nsprpriority=-10\nownpal=1')
    for name,y,identity in [('Upper framing',0,6412),('Lower framing',678,6413)]:
        ctl(name,'Explod',f'trigger1=time=0\nanim=21059\nID={identity}\npostype=left\npos=0,{y}\nbindtime=-1\nremovetime=420\nsprpriority=9\nownpal=1')
    ctl('Lucille wind-up','PlaySnd','trigger1=time=250\nvalue=0,2')
    ctl('Cut on the blow','EnvColor','trigger1=time=350\nvalue=0,0,0\ntime=12\nunder=0')
    ctl('Single crushing impact','PlaySnd','trigger1=time=350\nvalue=0,1')
    ctl('Heavy impact','EnvShake','trigger1=time=350\ntime=18\nampl=10\nfreq=65')
    ctl('One decisive hit','HitAdd','trigger1=time=350\nvalue=1')
    ctl('Resolve once','TargetLifeAdd','trigger1=time=350\nvalue=-950\nkill=1')
    ctl('Grounded aftermath','TargetState','trigger1=time=350\nvalue=8262')
    ctl('Final title','Explod','trigger1=time=362\nanim=21008\nID=6411\npostype=left\npos=640,125\nscale=.85,.85\nbindtime=-1\nremovetime=45\nsprpriority=8\nownpal=1')
    ctl('Settling dust','Explod','trigger1=time=362\nanim=21053\nID=6406\npostype=p1\npos=190,0\nremovetime=18\nscale=.7,.7\nsprpriority=3\nownpal=1')
    ctl('Recover','ChangeState','trigger1=time>=419\nvalue=10000\nctrl=1')
    return text


def victim(state,base,alt):
    # ChangeAnim selects the victim's own sprite bank, including paired forms.
    animation=f'ifelse((var(45)>0 || var(30)>0) && selfanimexist({alt}),{alt},ifelse(selfanimexist({base}),{base},5000))'
    text=f'\n[Statedef {state}]\ntype={"C" if state==8251 else "L"}\nmovetype=H\nphysics=N\nctrl=0\n'
    text+=f'[State {state}, Own active pose]\ntype=ChangeAnim\ntrigger1=time=0\nvalue={animation}\n'
    text+=f'[State {state}, Stop]\ntype=VelSet\ntrigger1=1\nx=0\ny=0\n'
    text+=f'[State {state}, Ground contact]\ntype=PosSet\ntrigger1=1\ny=0\n'
    text+=f'[State {state}, Hold camera]\ntype=ScreenBound\ntrigger1=1\nvalue=0\nmovecamera=0,0\n'
    text+=f'[State {state}, Capture protection]\ntype=NotHitBy\ntrigger1=1\nvalue=SCA\ntime=1\n'
    if state==8251:
        text+=f'[State {state}, Face captor]\ntype=Turn\ntrigger1=p2dist x<0\n'
        text+=f'[State {state}, Orphan safety]\ntype=SelfState\ntrigger1=time>600\nvalue=0\nctrl=1\n'
    else:text+=f'[State {state}, Own knockdown recovery]\ntype=SelfState\ntrigger1=time>=38\nvalue=5100\nctrl=0\n'
    return text
