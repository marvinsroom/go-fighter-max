"""Three arena-scale ultimates; ordinary combat and body scales stay separate."""
import hashlib,json,re
from pathlib import Path
from mugen_sff import Sff
from rimuru_source import ROOT,SOURCE
from rimuru_complete import frame
from rimuru_forms import ctl,state
from isolated_sprite_atlas import extract

def block(text,number,new,air=False):
    pattern=rf'(?ims)^\[{"Begin Action" if air else "statedef"}\s+{number}\].*?(?=^\[{"Begin Action" if air else "statedef"}|\Z)'
    assert re.search(pattern,text),number
    return re.sub(pattern,lambda _:new+'\n',text,count=1)

def install(out):
    out=Path(out);folder=SOURCE/'art/ultimates-v5';sff=Sff(out/'Rimuru Demon Lord.sff')
    assert (8795,0) not in sff.keys,'Cinematic art already installed'
    art=extract(folder/'cinematics.png',4,3);slime=extract(folder/'slime-combat.png',4,3)
    extra={(8795,i):frame(im,(im.width//2,im.height)) for i,(im,_) in enumerate(art)}
    replacements={};slime_scale=18/slime[11][0].height
    for i,(im,_) in enumerate(slime):
        axis=(round(im.width*(.32 if i in (0,2,3,8,9) else .5)),im.height)
        replacements[8790,i]=frame(im,axis)
    (out/'Rimuru Demon Lord.sff').write_bytes(sff.derive(replacements,extra))
    air=(out/'Rimuru Demon Lord.air').read_text();rows=[]
    for line in air.splitlines():
        if re.match(r'^8790,\d+,',line):
            p=line.split(',');p+=['']*max(0,9-len(p));p[7]=p[8]=f'{slime_scale:.9f}';line=','.join(p)
        rows.append(line)
    air='\n'.join(rows)+'\n';cns=(out/'rimuru_forms.cns').read_text();manifest={}
    # FX use the full arena; root fighters always keep their calibrated size.
    effect_sizes=[(160,130),(160,145),(180,145),(270,150),(170,140),(230,145),(270,145),(260,145),(160,140),(210,145),(250,145),(260,145)]
    for i,((im,_),(width,height)) in enumerate(zip(art,effect_sizes)):
        scale=min(width/im.width,height/im.height);anim=879500+i
        air+=f'\n[Begin Action {anim}]\n8795,{i},0,0,-1,,,{scale:.9f},{scale:.9f}\n'
        manifest[str(anim)]=dict(width=im.width*scale,height=im.height*scale,anchor=[160,165])
    def visual(n,t,index,life=30,priority=-2):
        return ctl(n,'Cinematic spell','Explod',f'time={t}',anim=879500+index,ID=879100,postype='left',pos='160,165',facing='facing',bindtime=-1,removetime=life,scale='1,1',sprpriority=priority,ownpal=1,removeongethit=1,supermovetime=999,pausemovetime=999)
    def flash(n,t,color='150,205,255',length=2):return ctl(n,'Impact flash','EnvColor',f'time={t}',time=length,color=color,under=1)
    for form in range(3):
        n=870091+form*1000;finish=[220,250,248][form];end=[270,310,300][form]
        body=[]
        poses=[(8794,2,40),(8794,2,110),(8794,3,60),(8794,2,60)] if form==0 else [(8794,4,50),(8794,5,100),(8794,6,100),(8794,7,60)] if form==1 else [(8790,11,48),(8790,8,80),(8790,9,100),(8790,8,72)]
        forms=json.loads((SOURCE/'forms-build.json').read_text())
        for g,i,duration in poses:
            scale=slime_scale if g==8790 else forms['body_sprites'][f'{g},{i}']['scale']
            body.append(f'{g},{i},0,0,{duration},,,{scale:.9f},{scale:.9f}')
        air=block(air,n,f'[Begin Action {n}]\nClsn2Default: 1\nClsn2[0]=-12,{-18 if form==2 else -50},12,0\n'+'\n'.join(body),True)
        text=state(n,n,cost=2000)
        text+=ctl(n,'Camera anchor','MapSet','!time',map='"rimuru.anchor"',value='camerapos x')
        text+=ctl(n,'Keep cinematic framing','ScreenBound',value=0,movecamera='0,0')
        text+=ctl(n,'Caster position','PosSet',x='map(rimuru.anchor)-facing*52',y=0)
        text+=ctl(n,'Effect evidence anchor','MapSet',map='"rimuru.fx_x"',value=0)
        text+=ctl(n,'Living spell field','ModifyExplod',ID=879100,postype='left',pos='160+4*sin(time*.06),165',scale='1+.025*sin(time*.12),1+.025*sin(time*.12)')
        text+=ctl(n,'Protected caster','NotHitBy',f'time<{finish}',value='SCA',time=1)
        target_pos='82,0' if form==0 else f'82,-18*sin(time*3.14159265/{finish})' if form==1 else '82-min(26,time*.1),0'
        text+=ctl(n,'Hold victim in scene','TargetBind',f'time<{finish}',time=1,pos=target_pos)
        text+=ctl(n,'Cinematic lighting','BGPalFX','!time',time=end,mul=['35,50,85','25,20,55','10,45,45'][form])
        text+=ctl(n,'Ultimate charge pause','SuperPause','!time',time=18,movetime=18,anim=-1,darken=0,sound='S950,2')
        if form==0:
            for t,idx,life in [(0,0,44),(32,1,42),(64,2,36),(92,1,35),(122,2,36),(152,1,36),(184,2,40),(220,3,28)]:text+=visual(n,t,idx,life,-2 if idx<2 else 3)
            ticks=[54,68,82,96,110,124,138,152,166]
        elif form==1:
            for t,idx,life in [(0,4,58),(42,5,45),(78,6,44),(114,5,44),(150,6,45),(188,5,50),(224,6,40),(250,7,32)]:text+=visual(n,t,idx,life,-2 if t<78 else 2)
            ticks=[70,90,110,130,150,170,190,210]
        else:
            for t,idx,life in [(0,8,58),(42,9,60),(92,10,58),(140,9,62),(190,10,45),(230,9,18),(248,11,34)]:text+=visual(n,t,idx,life,-2 if idx!=11 else 2)
            text+=ctl(n,'Abyss closes','EnvColor','time=232',time=12,color='0,0,0',under=0)
            ticks=[80,104,128,152,176,200]
        for t in ticks:
            text+=ctl(n,'Sequence damage','TargetLifeAdd',f'time={t}',value=-[34,42,50][form],kill=0,absolute=1)
            text+=ctl(n,'Sequence combo','HitAdd',f'time={t}',value=1)
            text+=ctl(n,'Sequence weight','EnvShake',f'time={t}',time=7,ampl=4)
            text+=ctl(n,'Sequence sound','PlaySnd',f'time={t}',value='S1,0',volumescale=110)
        text+=ctl(n,'Finisher anticipation','SuperPause',f'time={finish-12}',time=10,movetime=10,anim=-1,darken=0)
        text+=ctl(n,'Final damage','TargetLifeAdd',f'time={finish}',value=-[110,134,140][form],kill=1,absolute=1)
        text+=ctl(n,'Final combo','HitAdd',f'time={finish}',value=1)+flash(n,finish,'230,240,255' if form==0 else '90,170,255' if form==1 else '90,240,220',3)
        text+=ctl(n,'Finishing quake','EnvShake',f'time={finish}',time=18,ampl=10)
        text+=ctl(n,'Finishing sound','PlaySnd',f'time={finish}',value='S950,2',volumescale=140)
        text+=ctl(n,'Release knockdown','TargetState',f'time={finish}',value=879991)
        text+=ctl(n,'Recover','ChangeState',f'time>={end}',value=0,ctrl=1)
        cns=block(cns,n,text)
        for move in forms['moves']:
            if move['form']==form and move['offset']==90:move.update(total=end+70,cinematic_finish=finish,cinematic_duration=end)
        (SOURCE/'forms-build.json').write_text(json.dumps(forms,indent=2),encoding='utf-8')
    # The victim's safety timeout must cover the longer dragon sequence.
    cns=cns.replace('trigger1=time>250','trigger1=time>370')
    (out/'rimuru_forms.cns').write_text(cns,encoding='utf-8');(out/'Rimuru Demon Lord.air').write_text(air,encoding='utf-8')
    forms=json.loads((SOURCE/'forms-build.json').read_text())
    for key,f in replacements.items():
        k=','.join(map(str,key));meta=dict(scale=slime_scale,axis=list(f['axis']),rgba_sha256=f['rgba_sha256'])
        forms['added_sprites'][k]=meta;forms['body_sprites'][k]={k:v for k,v in meta.items() if k!='rgba_sha256'}
    forms['cinematic_effects']=manifest;forms['cinematic_art']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.png')}
    forms['cinematic_sprites']={','.join(map(str,key)):dict(axis=list(f['axis']),rgba_sha256=f['rgba_sha256']) for key,f in extra.items()}
    forms['cinematic_revision']=5
    (SOURCE/'forms-build.json').write_text(json.dumps(forms,indent=2),encoding='utf-8')
    report=json.loads((SOURCE/'build-report.json').read_text());report['status']='Cinematic ultimates v5 built; validation pending'
    report['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ('.def','.air','.cns','.cmd','.sff') and not p.name.startswith(('test-','rimuru_test'))}
    (SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('RIMURU_CINEMATICS three distinct arena ultimates; 12 cinematic effects; 12 complete slime drawings')

if __name__=='__main__':install(ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru')
