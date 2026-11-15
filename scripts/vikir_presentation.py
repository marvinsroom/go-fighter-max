"""Body calibration and cinematic sword presentation, independent of weapon bounds."""
from pathlib import Path
import json,math

# Hair crown to chin spans measured in the original source atlases. Bent knees,
# a raised blade, coat tails and an extended arm must never resize the head.
HEAD_SPANS={
 'm':[58,60,59,61,56,64,65,63,57,61,60,64,61,59,62,61],
 'c':[57,53,62,65,58,61,62,64,64,56,59,58,64,60,65,64],
 'p':[66,58,65,67,67,61,63,70,59,64,64,65,61,58,59,63],
 'a':[60,61,59,61,57,64,64,63,60,62,61,63,61,61,60,61],
 'b':[57,53,62,65,58,61,62,64,64,56,59,58,64,60,65,64],
 's':[66,67,70,66,71,63,63,66,60,61,64,64,59,56,64,63],
 'bo':[76,76,75,76,75,76,76,75],
}

def calibrate(A):
    for prefix,spans in HEAD_SPANS.items():
        for i,span in enumerate(spans):
            key=prefix+str(i)
            if key not in A.meta:continue
            m=A.meta[key];m.update(scale=76/span,head_span=span,head_pixels=76,scale_basis='crown-to-chin anatomy')
    for dst,src in [('n','m'),('k','c'),('r','p')]:
        for i in range(16):
            if dst+str(i) in A.meta:
                base=A.meta[src+str(i)];A.meta[dst+str(i)].update(scale=base['scale'],head_span=base['head_span'],head_pixels=76,scale_basis='matched anatomy of '+src+str(i))
    audit={k:dict(scale=m['scale'],head_span=m['head_span'],head_pixels=m['head_pixels']) for k,m in A.meta.items() if 'head_span' in m}
    (A.source/'anatomy-calibration.json').write_text(json.dumps(dict(method='Measured crown-to-chin spans; weapon and pose bounds excluded',target_head_pixels=76,poses=audit),indent=2))

def load_fx(A,axis):
    from PIL import Image
    art=A.source/'art/presentation-v4';sheet=art/'effects.png'
    assert sheet.exists(),'Generate the presentation-v4 effects atlas first'
    (art/'poses').mkdir(exist_ok=True);im=Image.open(sheet).convert('RGBA');w,h=im.size
    for i in range(16):
        tile=im.crop((i%4*w//4,i//4*h//4,(i%4+1)*w//4,(i//4+1)*h//4))
        box=tile.getchannel('A').getbbox();assert box,(i,'empty VFX cell')
        tile=tile.crop(box);p=art/'poses'/f'vfx{i}.png';tile.save(p)
        A.png(f'vfx{i}',p,tile.height,i,91);root=[tile.width//2,tile.height//2];axis(*root)
        width=180 if i<8 else 620 if i<12 else 860 if i<14 else 760
        A.meta[f'vfx{i}'].update(axis=root,scale=width/tile.width,bank='presentation-v4')
    for n,ids in [(7140,range(4)),(7150,range(4,8)),(8010,range(8,12)),(8020,[12,13]),(8030,[14,15])]:
        A.action(n,[(f'vfx{i}',3) for i in ids],range(len(ids)) if n<8000 else (),attack=(-80,-15,80,15),hurt=False)

def states(state,ctl,end,hit):
    state(4500,4500,move='A',poweradd=-3000,velset='0,0')
    ctl(4500,'Restore human body','MapSet','time=0',map='"vikir.form"',value='ifelse(map(vikir.form)=2,0,map(vikir.form))')
    ctl(4500,'Execution announcement','SuperPause','time=0',time=18,movetime=18,anim=-1,sound='S0,4',darken=1,poweradd=0)
    ctl(4500,'Hound eyes cut in','Explod','time=0',anim=8020,ID=8020,postype='left',pos='640,320',bindtime=-1,removetime=22,supermovetime=22,pausemovetime=22,ownpal=1,sprpriority=5)
    ctl(4500,'Opening dash','VelSet','time=[19,25]',x=18)
    ctl(4500,'Stop opener','VelSet','time=26',x=0)
    hit(4500,24,55,attr='S,HA',pausetime='0,2',ground__hittime=30,ground__velocity=0,air__velocity='0,0',fall=0,getpower='0,0',p2stateno=4515,hitsound='S0,0',sparkno=-1,guard__sparkno=-1,kill=0)
    ctl(4500,'Confirmed execution','ChangeState','movehit',value=4510)
    end(4500)
    state(4510,4510,move='A',velset='0,0')
    ctl(4510,'Cinematic safety','NotHitBy',value='SCA',time=1)
    ctl(4510,'No body push','PlayerPush',value=0)
    ctl(4510,'Hold confirmed target','TargetBind',['time<88','numtarget>0'],time=1,pos='185,0')
    ctl(4510,'Crimson background','BGPalFX','time<104',time=2,color=0,mul='100,30,45')
    ctl(4510,'Blade afterimages','AfterImage','time=0',time=104,length=12,timegap=2,framegap=2,trans='add',palcolor=0,palbright='50,0,0',palmul='.8,.25,.25')
    ctl(4510,'Fang storm','Explod','time=16',anim=8010,ID=8010,postype='p1',pos='180,-220',bindtime=-1,removetime=62,ownpal=1,sprpriority=3)
    for t in range(16,76,3):
        hit(4510,t,14,attr='S,HA',guard='MA',pausetime='0,1',ground__hittime=30,ground__velocity=0,air__velocity='0,0',fall=0,p2stateno=4515,getpower='0,0',hitsound='S0,0',sparkno=-1,guard__sparkno=-1,kill=0)
        ctl(4510,'Fang camera impact','EnvShake',f'time={t}',time=2,freq=100,ampl=3)
    ctl(4510,'Final cleave flash','PalFX','time=88',time=5,add='120,60,60',color=0)
    ctl(4510,'Final shockwave','Explod','time=88',anim=8030,ID=8030,postype='p1',pos='210,-210',bindtime=1,removetime=16,ownpal=1,sprpriority=4)
    ctl(4510,'Final impact sound','PlaySnd','time=88',value='0,3')
    ctl(4510,'Final camera impact','EnvShake','time=88',time=16,freq=65,ampl=10)
    hit(4510,88,220,attr='S,HA',pausetime='0,8',ground__hittime=30,ground__velocity='-10,-8',air__velocity='-10,-8',fall=1,getpower='0,0',hitsound='S0,3',sparkno=-1,guard__sparkno=-1)
    ctl(4510,'Abort without a target','ChangeState',['time<88','numtarget=0'],value=0,ctrl=1)
    end(4510)
    state(4515,None,kind='S',move='H',velset='0,0')
    ctl(4515,'Victim hurt pose','ChangeAnim','time=0',value=5000)
    ctl(4515,'Freeze victim pose','ChangeAnim','animtime=0',value=5000)
    ctl(4515,'Release interrupted victim','SelfState','time>150 || enemynear,stateno!=4510 && enemynear,stateno!=4500',value=0,ctrl=1)

def charge(ctl):
    ctl(500,'Visible charging aura','PalFX',time=2,add='35,5,5',sinadd='30,10,10,16')
    ctl(500,'Charge floor ring','Explod','numexplod(8050)=0',anim=7130,ID=8050,postype='p1',pos='0,-15',bindtime=-1,scale='.5,.12',removetime=-1,ownpal=1,sprpriority=-1)

