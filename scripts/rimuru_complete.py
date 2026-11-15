"""Complete charge/forms/supers and replace every imported visual effect."""
from pathlib import Path
import io,json,re,hashlib,statistics,math
from PIL import Image,ImageOps
import numpy as np
from scipy import ndimage
from mugen_sff import Sff
from jinwoo_motion import atlas_rects

def frame(im,axis):
    b=io.BytesIO();im.save(b,format='PNG',compress_level=1)
    return dict(image=im,png=b.getvalue(),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())

def load(folder,name,rows,refs):
    im=Image.open(folder/(name+'.png')).convert('RGBA');tiles=[]
    if name in ('effects-v4','clean-casters'):
        # Slice complete isolated drawings before assigning grid order. A tall
        # beam can cross an imagined equal-height row without being cropped.
        labels,_=ndimage.label(np.array(im.getchannel('A'))>48)
        areas=np.bincount(labels.ravel());areas[0]=0;objects=ndimage.find_objects(labels)
        boxes=[objects[i-1] for i in np.argsort(areas)[-4*rows:]]
        chosen=sorted(areas[1:])[-4*rows:]
        assert min(chosen)>max(chosen)*.12,('Expected isolated complete drawings',name,chosen)
        boxes.sort(key=lambda b:(b[0].start+b[0].stop)/2)
        ordered=[]
        for row in range(rows):ordered+=sorted(boxes[row*4:row*4+4],key=lambda b:(b[1].start+b[1].stop)/2)
        for yy,xx in ordered:
            assert min(xx.start,yy.start,im.width-xx.stop,im.height-yy.stop)>0,('Drawing touches sheet edge',name,xx,yy)
            tiles.append(im.crop((xx.start,yy.start,xx.stop,yy.stop)))
        scale=50/statistics.median(tiles[i].height for i in refs)
        return [dict(frame(t,(t.width//2,t.height)),scale=scale) for t in tiles]
    rects=atlas_rects(im,4,rows)
    for rect in rects:
        tile=im.crop(rect);labels,_=ndimage.label(np.array(tile.getchannel('A'))>48);areas=np.bincount(labels.ravel());areas[0]=0
        yy,xx=ndimage.find_objects(labels)[areas.argmax()-1]
        tiles.append(tile.crop((xx.start,yy.start,xx.stop,yy.stop)))
    scale=50/statistics.median(tiles[i].height for i in refs)
    return [dict(frame(t,(t.width//2,t.height)),scale=scale) for t in tiles]

def block_replace(text,state,new):
    pattern=rf'(?is)\[statedef\s+{state}\s*\].*?(?=\[statedef|\Z)'
    assert re.search(pattern,text),state
    return re.sub(pattern,lambda _:new+'\n\n',text,count=1)

def action(number,rows,group=7950,hurt=True,attack=False,loop=False):
    out=[f'\n[Begin Action {number}]']
    if hurt:out+=['Clsn2Default: 1','Clsn2[0]=-12,-50,12,0']
    if attack:out+=['Clsn1Default: 1','Clsn1[0]=0,-58,90,0']
    if loop:out+=['LoopStart']
    for n,ticks,s in rows:out.append(f'{group},{n},0,0,{ticks},,,{s:.9f},{s:.9f}')
    return '\n'.join(out)+'\n'

def install(out,base):
    source=out.parents[3]/'characters/rimuru';folder=source/'art/complete-v2'
    forms=load(folder,'forms',4,[0,1,4,5,6,7,8]);wings=load(folder,'wings',2,[0,1,2,3]);fx=load(folder,'effects-v4' if (folder/'effects-v4.png').exists() else 'effects',4,[0]);wolf=load(folder,'ranga',2,[0,3,4,7])
    # Walking wings extend above the head: calibrate to head-to-sole height.
    for f in wings:f['scale']*=1.085
    for i in range(12,16):forms[i]['scale']=18/forms[12]['image'].height
    sff=Sff(out/'Rimuru Demon Lord.sff');replace={};extra={};factors={};metadata={}
    # Re-author effects rather than enlarging source pixels. Original geometry,
    # AIR timing, helper anchors and blend modes retain their world-space size.
    fire={6880,7200,7250,7340,7400};vortex={6250,6260,6270,6800,6840,6860,6900,7050,7070,7150,7160,7170,8000,8050,8900}
    for (g,n),index in sff.keys.items():
        if g<6000 or g in (7900,9000,17000):continue
        old=sff.headers[index];ow,oh=old[2:4];factor=max(1,min(4,math.ceil(640/max(ow,oh))))
        if g==7300:tile=wolf[n%8]['image']
        else:
            k=(4+n%4) if g in fire else (8+n%4) if g in vortex else 15 if g in (8600,8700) else 12 if g in (8740,8741,16000,16020,16040) else 14 if g in (6700,7350) else n%4 if g in (6000,6001,6002,6003,6004,6005,6008,6009,6780) else 13
            tile=fx[k]['image']
        canvas=Image.new('RGBA',(ow*factor,oh*factor));fit=ImageOps.contain(tile,canvas.size,Image.Resampling.LANCZOS);canvas.alpha_composite(fit,((canvas.width-fit.width)//2,(canvas.height-fit.height)//2))
        replace[g,n]=frame(canvas,(old[4]*factor,old[5]*factor));factors[g,n]=factor
        metadata[f'{g},{n}']=dict(factor=factor,rgba_sha256=replace[g,n]['rgba_sha256'],kind='illustrated Ranga' if g==7300 else 'painted effect')
    for i,f in enumerate(forms):extra[7950,i]=f
    for i,f in enumerate(wings):extra[7951,i]=f
    for i,f in enumerate(fx):extra[7952,i]=f
    for i,f in enumerate(wolf):extra[7953,i]=f
    (out/'Rimuru Demon Lord.sff').write_bytes(sff.derive(replace,extra))
    air=(out/'Rimuru Demon Lord.air').read_text(encoding='utf-8');lines=[]
    for line in air.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            p=line.split(';')[0].split(',');key=tuple(int(v.strip()) for v in p[:2]);factor=factors.get(key)
            if factor:
                while len(p)<9:p.append('')
                for j in (7,8):p[j]=f'{(float(p[j]) if p[j].strip() else 1)/factor:.9f}'
                line=','.join(p)
        lines.append(line)
    air='\n'.join(lines)+'\n'
    def authored(number,indices,group=7950,hurt=True,attack=False,loop=False,duration=8):
        nonlocal air
        table=forms if group==7950 else wings if group==7951 else fx
        rows=[(i,duration,table[i]['scale']) for i in indices]
        air+=action(number,rows,group,hurt,attack,loop)
    authored(7930,range(4),loop=True);authored(7931,[1,0],duration=5)
    authored(7940,[4,5,6,7,8],duration=9);authored(7941,[11,12,13,15],duration=8);authored(7942,[15,12,4,0],duration=8)
    # Ground aura, slashes, vortex and beams use explicit world-space dimensions.
    for number,indices,height in [(7965,[0,1,2,3],65),(7975,[8,9,10,11],90),(7985,[12,12,13],125),(7935,[14,14,14],65)]:
        air+=action(number,[(i,5,height/fx[i]['image'].height) for i in indices],7952,False)
    for number,keys in [(7960,['combat:0','combat:1','combat:2','combat:5','combat:6','combat:3']),(7970,['combat:8','combat:9','combat:11','combat:8']),(7980,['combat:0','combat:8','combat:10']),(7981,['combat:10','combat:10','combat:10','combat:10'])]:
        # Reuse already authored, registered body entries, preserving their scale.
        s=Sff(out/'Rimuru Demon Lord.sff');group=7961+number-7960
        for i,key in enumerate(keys):extra_frame=base[key];extra[group,i]=extra_frame
        air+=action(number,[(i,10 if number!=7981 else 54,base[key]['scale']) for i,key in enumerate(keys)],group,True,True)
    # Add body rows created after the first container write.
    latest=Sff(out/'Rimuru Demon Lord.sff');new={k:v for k,v in extra.items() if k not in latest.keys}
    (out/'Rimuru Demon Lord.sff').write_bytes(latest.derive({},new))
    # Each gameplay body action gets a complete form variant, keeping its timing
    # and attack boxes. Form selection changes the animation once on entry.
    body_keys={tuple(map(int,k.split(','))) for k in json.loads((source/'build-report.json').read_text()).get('sprites',{})} if (source/'build-report.json').exists() else set()
    body_keys.update(k for k in sff.keys if k[0]<6000);body_keys.update(k for k in new)
    variants=[];supported=[]
    for block in re.split(r'(?=\[Begin Action\s+)',air,flags=re.I):
        match=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
        if not match:continue
        number=int(match[1]);body_rows=[l for l in block.splitlines() if re.match(r'^\s*\d+\s*,\s*\d+\s*,',l)]
        if number in (190,7900,7940,7941,7942) or not any(tuple(map(int,l.split(',')[:2])) in body_keys or l.startswith('7950,') for l in body_rows):continue
        supported.append(number)
        for form,offset in [(1,20000),(2,40000)]:
            variant=re.sub(r'\[Begin Action\s+\d+\]',f'[Begin Action {number+offset}]',block,count=1,flags=re.I);converted=[]
            for line in variant.splitlines():
                if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
                    p=line.split(';')[0].split(',');g,n=map(int,p[:2]);isbody=(g,n) in body_keys or g==7950
                    if isbody:
                        if form==2:idx=13 if number in (20,21,60,70) else 14 if number in (40,50) else 15 if number in (10,11,12,52) else 12+(n%2 if number==7930 else 0);f=forms[idx];group=7950
                        elif number in (20,21,60,70):idx=n%4;f=wings[idx];group=7951
                        elif number in (40,50,52,120,121,122) or 5000<=number<=5300:idx=4 if number in (40,50) else 6 if number==121 else 7;f=wings[idx];group=7951
                        else:idx=11 if number in (7980,7981,1400,1500) else 10 if number>=1000 or number==7930 else 9 if 200<=number<700 else 8;f=forms[idx];group=7950
                        while len(p)<9:p.append('')
                        p[0:2]=[str(group),str(idx)];p[7]=p[8]=str(f['scale']);line=','.join(p)
                elif form==2 and re.match(r'\s*Clsn2\[',line,re.I):line=re.sub(r'=.*','= -13,-18,13,0',line)
                converted.append(line)
            variants.append('\n'.join(converted))
    (out/'Rimuru Demon Lord.air').write_text(air+'\n'+'\n'.join(variants),encoding='utf-8')
    main=(out/'Rimuru Demon Lord.cns').read_text(encoding='utf-8');main=block_replace(main,500,charge());main=block_replace(main,501,recover(501,7931,10))
    (out/'Rimuru Demon Lord.cns').write_text(main,encoding='utf-8')
    supers=(out/'Supers.cns').read_text(encoding='utf-8');supers=block_replace(supers,4500,ultimate_start());supers=block_replace(supers,4501,ultimate_finish())
    (out/'Supers.cns').write_text(supers,encoding='utf-8')
    ai=(out/'IA.cns').read_text(encoding='utf-8');controllers=''
    for form,offset in [(1,20000),(2,40000)]:
        controllers+=f'[State -3, Persistent form {form}]\ntype=ChangeAnim\ntriggerall=!ishelper\ntriggerall=map(rimuru.form)={form}\ntriggerall=anim<20000\ntrigger1='+ ' || '.join(f'anim={n}' for n in supported)+f'\nvalue=anim+{offset}\nelem=animelemno(0)\nignorehitpause=1\n'
    ai=re.sub(r'(?i)\[statedef -3\]',lambda m:m[0]+'\n'+controllers,ai,count=1);(out/'IA.cns').write_text(ai,encoding='utf-8')
    common=(out/'common1.cns').read_text(encoding='utf-8')
    common='\n'.join(re.sub(r'\banim\s*(!=|=)\s*(\d+)',lambda m:f'anim%20000 {m[1]} {m[2]}' if int(m[2])<20000 else m[0],line,flags=re.I) if re.match(r'\s*trigger',line,re.I) else line for line in common.splitlines())
    (out/'common1.cns').write_text(common+'\n',encoding='utf-8')
    cmds=(out/'Rimuru Demon Lord.cmd').read_text(encoding='utf-8');defs='';routes=''
    for name,command,state,meter in [('rimuru_form','w',7940,0),('rimuru_slash','/$F,~x',7960,1000),('rimuru_predator','/$B,~x',7970,2000),('rimuru_blackflame','/$D,~x',1300,1500),('rimuru_ranga','/$B,~y',1200,1500),('rimuru_timestop','/$F,~y',1500,2000)]:
        defs+=f'[Command]\nname="{name}"\ncommand={command}\ntime=15\n'
        value='ifelse(map(rimuru.form)=0,7940,ifelse(map(rimuru.form)=1,7941,7942))' if name=='rimuru_form' else str(state)
        routes+=f'[State -1, {name}]\ntype=ChangeState\ntriggerall=command="{name}"\ntriggerall=power>={meter}\ntriggerall=statetype!=A\ntrigger1=ctrl\nvalue={value}\n'
    cmds=cmds.replace('[Statedef -1]',defs+'\n[Statedef -1]\n'+routes,1)
    cmds=cmds.replace('triggerall = command = "s"','triggerall = command = "hold_s"')
    (out/'Rimuru Demon Lord.cmd').write_text(cmds,encoding='utf-8')
    (out/'rimuru_complete.cns').write_text(transformations()+super_state(7960,1000,7965,70)+super_state(7970,2000,7975,100),encoding='utf-8')
    definition=(out/'rimuru.def').read_text(encoding='utf-8');definition=definition.replace('st4=','st4=rimuru_complete.cns\nst5=');(out/'rimuru.def').write_text(definition,encoding='utf-8')
    report=dict(revision=2,replaced_effects=len(replace),effect_sprites=metadata,form_actions=supported,forms=['Masked human','Demon Lord','Slime'],new_supers={'Tempest Sever':7960,'Predator Collapse':7970},ultimate='Completed Megiddo: visible caster, nine beam hits and finishing knockdown',source_art={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.png')})
    (source/'complete-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('RIMURU_COMPLETE_ART',len(replace),'painted effect/summon sprites;',len(supported),'actions in both forms')

def recover(state,anim,ticks):return f'[Statedef {state}]\ntype=S\nmovetype=I\nphysics=S\nctrl=0\nanim={anim}\nvelset=0,0\n[State {state}, Ready]\ntype=ChangeState\ntrigger1=time>={ticks}\nvalue=0\nctrl=1\n'

def charge():return '''[Statedef 500]
type=S
movetype=I
physics=S
anim=7930
ctrl=0
velset=0,0
[State 500, Power]
type=PowerAdd
trigger1=time>=8
value=12
[State 500, Voice]
type=PlaySnd
trigger1=time=0
value=S500,13
[State 500, Aura]
type=Explod
trigger1=time%15=0
anim=7935
ID=7935
pos=0,0
postype=p1
bindtime=-1
removetime=15
scale=1.65,1.65
sprpriority=-1
removeongethit=1
[State 500, End]
type=ChangeState
triggerall=time>=8
trigger1=command!="hold_s"
trigger2=power>=3000
value=501
'''

def transformations():
    result=''
    for state,form in [(7940,1),(7941,2),(7942,0)]:
        result+=recover(state,state,46 if state==7940 else 33)
        result+=f'[State {state}, Form]\ntype=MapSet\ntrigger1=time=30\nmap="rimuru.form"\nvalue={form}\n'
    return result

def flash(state,ticks):return f'[State {state}, Pause]\ntype=SuperPause\ntrigger1=time=0\ntime=18\nmovetime=18\nanim=-1\ndarken=0\nsound=S950,2\n[State {state}, Darken]\ntype=BGPalFX\ntrigger1=time=0\ntime={ticks}\nmul=100,120,155\n[State {state}, Voice]\ntype=PlaySnd\ntrigger1=time=0\nvalue=S500,15\n'

def hit(state,trigger,damage,fall=0):return f'[State {state}, Strike]\ntype=HitDef\ntrigger1={trigger}\nattr=S,HA\ndamage={damage},4\nanimtype=Hard\nhitflag=MAF\nguardflag=MA\npausetime=2,4\nground.type=High\nground.hittime=20\nground.velocity={"-5,-5" if fall else "0,0"}\nair.velocity=-3,-4\nfall={fall}\nsparkno=-1\nguard.sparkno=-1\nhitsound=S1,0\ngetpower=0,0\ngivepower=0,0\nkill=1\n'

def effect(state,trigger,anim,pos='35,0',scale='1.65,1.65'):return f'[State {state}, Painted effect]\ntype=Explod\ntrigger1={trigger}\nanim={anim}\nID={anim}\npostype=p1\npos={pos}\nscale={scale}\nremovetime=15\nsprpriority=4\nremoveongethit=1\n'

def super_state(state,cost,fx,damage):
    text=f'[Statedef {state}]\ntype=S\nmovetype=A\nphysics=S\nanim={state}\nctrl=0\nvelset=0,0\npoweradd=-{cost}\n'+flash(state,70)
    text+=hit(state,'time=22 || time=34',damage)+hit(state,'time=46',damage,1)
    text+=effect(state,'time=22 || time=34 || time=46',fx)
    text+=f'[State {state}, Shake]\ntype=EnvShake\ntrigger1=movehit=1\ntime=8\nampl=5\n[State {state}, End]\ntype=ChangeState\ntrigger1=time>=70\nvalue=0\nctrl=1\n'
    return text

def ultimate_start():return '''[Statedef 4500]
type=S
movetype=A
physics=S
anim=7980
ctrl=0
velset=0,0
poweradd=-1000
'''+flash(4500,50)+hit(4500,'time=24',10)+'''[State 4500, Confirm]
type=ChangeState
trigger1=movehit
value=4501
[State 4500, Whiff recovery]
type=ChangeState
trigger1=time>=60
value=0
ctrl=1
'''

def ultimate_finish():return '''[Statedef 4501]
type=S
movetype=A
physics=S
anim=7981
ctrl=0
velset=0,0
poweradd=-2000
[State 4501, Cinematic protection]
type=NotHitBy
trigger1=time<190
value=SCA
time=1
[State 4501, Storm]
type=BGPalFX
trigger1=time=0
time=216
mul=65,85,120
'''+hit(4501,'time>=28 && time<=172 && time%18=10',34)+hit(4501,'time=190',110,1)+effect(4501,'time>=28 && time<=172 && time%18=10',7985,'40,0')+effect(4501,'time=190',7975,'40,0','2.5,2.5')+'''[State 4501, Impacts]
type=EnvShake
trigger1=time>=28 && time<=190 && time%18=10
time=8
ampl=6
[State 4501, Finish shake]
type=EnvShake
trigger1=time=190
time=16
ampl=10
[State 4501, Recover]
type=ChangeState
trigger1=time>=218
value=0
ctrl=1
'''
