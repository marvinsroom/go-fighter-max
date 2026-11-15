"""Install Soulfire's preserved combat base with illustrated key poses."""
from jin_mori_assets import *
from edward_assets import write_v2
from isolated_sprite_atlas import extract
import re, hashlib, shutil

O=E/'chars/jin_mori_build'; O.mkdir(exist_ok=True)
R=E/'chars/jin_mori_reference'; R.mkdir(exist_ok=True)
originals={}
for p in U.iterdir():
    if p.is_file():
        originals[p.name]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        shutil.copy2(p,R/p.name)
        if p.suffix.lower() not in ('.sff','.air','.cmd','.def'):
            if p.suffix.lower()=='.cns':
                cns=p.read_text(encoding='latin1')
                if p.name=='Jin Mori.cns':
                    cns=re.sub(r'(?i)type\s*=\s*ChangeAnim2(\s*\ntrigger1\s*=\s*time\s*=\s*(?:0|16)\s*\nvalue\s*=\s*(?:5000|5060)\b)',r'type = ChangeAnim\1',cns)
                    marker='[StateDef 4503]'
                    start=cns.index(marker);end=cns.index('[StateDef 4504]',start)
                    cyclone=cns[start:end]
                    cyclone+='''
[State 4503, Confirmed cyclone contact]
type=VarSet
trigger1=MoveHit
v=58
value=1
[State 4503, Hold confirmed target inside cyclone]
type=TargetBind
triggerall=NumTarget>0 && var(58)
trigger1=Time<92
pos=0,120
time=1
'''
                    cns=cns[:start]+cyclone+cns[end:]
                (O/p.name).write_text(cns,encoding='utf-8')
            else:shutil.copy2(p,O/p.name)
definition=(U/'Jin Mori.def').read_text(encoding='latin1')
definition=definition.replace('[Files]','localcoord=320,240\n\n[Files]').replace('pal2=',';pal2=')
(R/'jin_mori_reference.def').write_text(definition,encoding='utf-8')
(O/'jin_mori.def').write_text(definition.replace('localcoord=320,240','localcoord=192,144\nportraitscale=0.125').replace('sprite=Jin Mori.sff','sprite=jin_mori.sff').replace('anim=Jin Mori.air','anim=jin_mori.air').replace('cmd=Jin Mori.cmd','cmd=jin_mori.cmd'),encoding='utf-8')

# Convenient roster shortcuts; all source motions and combo routes survive.
routes=[('mori_ultimate','z',4500,3000),('mori_tempest','/$B,y',3000,2000),('mori_twin','/$F,y',2500,2000),('mori_triple','/$D,y',3500,1500),('mori_azure','y',2000,1500),('mori_tortoise','/$B,x',1500,1000),('mori_sword','x',1000,1000),('mori_transform','w',980500,0),('mori_dodge','d',340,0)]
commands=''
controllers=''
for name,keys,state,cost in sorted(routes,key=lambda r:-len(r[1])):
    commands+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime=1\n'
    controllers+=f'\n[State -1, {name}]\ntype=ChangeState\ntriggerall=AILevel=0 && command="{name}"\ntriggerall=StateType!=A && RoundState=2\ntriggerall=Power>={cost}\ntrigger1=ctrl\nvalue={state}\n'
    if name=='mori_azure':
        controllers=controllers.removesuffix(f'value={state}\n')+'triggerall=command!="holdback" && command!="holdfwd" && command!="holddown"\n'+f'value={state}\n'
cmd=(U/'Jin Mori.cmd').read_text(encoding='latin1')
cmd=cmd.replace('[Statedef -1]',commands+'\n[Statedef -1]\n'+controllers,1)
# Identity remap keeps Z/X/C on source a/b/c; A/S/D use free x/y/z.
(O/'jin_mori.cmd').write_text(cmd,encoding='utf-8')

art=S/'art/illustrated-v1'; poses=art/'poses';poses.mkdir(parents=True,exist_ok=True)
sprites=read_source();body_groups={s['key'][0] for s in sprites if s['key'][0]<6000 and s['key'][0]!=9000}
body_groups.discard(500) # 500 is also an actor, restored below for clarity.
body_groups.add(500)
new=[];library={};registration=[]
for bank,slug in enumerate(('movement','combat','specials')):
    tiles=extract(art/(slug+'.png'),4,4)
    # The first drawing is upright in every bank, all poses retain that scale.
    factor=424/tiles[0][0].height
    for i,(im,bounds) in enumerate(tiles):
        im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
        anchor=({2:.34,4:.45,6:.37,9:.36,12:.34,15:.30}.get(i,.5) if bank==1 else {2:.35,4:.35,6:.34,11:.35,14:.38}.get(i,.5) if bank==2 else .5)
        axis=(round(im.width*anchor),im.height)
        entry=dict(key=(62000+bank,i),axis=axis,image=im)
        new.append(entry);library[bank,i]=entry
        im.save(poses/f'{slug}-{i}.png')
        registration.append(dict(bank=slug,pose=i,bounds=bounds,size=im.size,axis=axis))

def pose(g,n):
    if g in (0,5):return 0,0
    if g==10:return 0,4
    if g==20:return 0,2+n%2
    if g==40:return 0,6 if n<3 else 7
    if g==100:return 0,5
    if g==120:return 0,8
    if g in (170,5060,5061,5062):return 0,13
    if g in (180,190):return 0,15
    if g==5300:return 0,14
    if 5000<=g<=5072:return 0,12 if 5030<=g<=5042 else 10 if n<2 else 11
    if g==4500:return 2,0 if n<4 else min(15,n+4)
    if g==3000:return 2,[0,5,6,7,7,0][min(n,5)]
    if g==1500:return 2,[0,3,4,4,0][min(n,4)]
    if g==1000:return 2,[0,1,2][min(n,2)]
    if g==500:return 2,0
    sequences={230:[0,1,2,0],240:[0,3,4,0],250:[0,5,6,7,0],260:[0,8,9,0],270:[0,8,9,10,0],280:[0,5,6,7,0],290:[0,11,12,13,0],300:[0,11,12,0],310:[0,8,9,10,11,12,13,14,0],320:[0,14,15],630:[0,11,12,0],640:[0,11,12,0],650:[0,8,9],660:[12]}
    seq=sequences.get(g,[0,1,2,0]);return 1,seq[min(n,len(seq)-1)]

# Replace body raster references while keeping AIR durations and collision boxes.
source_air=(U/'Jin Mori.air').read_text(encoding='latin1');out=[];actor_rows=0
for line in source_air.splitlines():
    m=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
    if m and int(m[1]) in body_groups:
        f=[v.strip() for v in line.split(';',1)[0].split(',')]
        g,n=int(f[0]),int(f[1]);bank,index=pose(g,n)
        f=f[:7]
        while len(f)<7:f.append('')
        f[0]=str(62000+bank);f[1]=str(index)
        f+=['.125','.125']
        line=','.join(f);actor_rows+=1
    out.append(line)
(O/'jin_mori.air').write_text('\n'.join(out)+'\n',encoding='utf-8')
# Retain smooth source VFX, replacing the chibi portrait and Monkey King cut-in.
portrait=Image.open(art/'portrait.png').convert('RGBA')
for s in sprites:
    g,n=s['key']
    if g in body_groups:continue
    if g==9000:
        size=(200,200) if n==0 else (960,1120)
        im=portrait.copy();im.thumbnail(size,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',size);canvas.alpha_composite(im,((size[0]-im.width)//2,0))
        s=dict(key=s['key'],axis=(0,0),image=canvas)
    if g==17000:
        im=library[2,8]['image'].copy(); im.thumbnail(s['image'].size,Image.Resampling.LANCZOS)
        s=dict(key=s['key'],axis=s['axis'],image=im)
    new.append(s)
from jin_mori_upgrade import install as upgrade
new=upgrade(O,new)
write_v2(O/'jin_mori.sff',new)
(S/'pose-registration.json').write_text(json.dumps(registration,indent=2))
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix.lower() in ('.def','.cmd','.cns','.sff','.snd','.air','.act') and 'test' not in p.name.lower()}
report=dict(creator='Soulfire',source=json.loads((S/'source/source-report.json').read_text()),original_files=originals,runtime_sha256=runtime,source_sprites=len(sprites),source_actions=len(re.findall(r'\[Begin Action',source_air,re.I)),actor_rows=actor_rows,illustrated_poses=104,revision='awakening-v3',notes=['Source preserved; original AIR actions retained alongside new authored actions.','Buffered ground chains, dedicated entrance, free persistent Monkey King toggle.','Eight registered transformation in-betweens; equal 424px planted body height in both forms.','Readable guardable staff ultimate replaces screen-covering source cyclone; 540 confirmed damage.','Original counter, dragon supers, sound and AI routes retained.'],routes=[dict(name=n,input=k,state=s,cost=c) for n,k,s,c in routes])
(S/'build-report.json').write_text(json.dumps(report,indent=2))
installed=E/'chars/jin_mori';installed.mkdir(exist_ok=True)
for p in O.iterdir():
    if p.suffix.lower() in ('.def','.cmd','.cns','.sff','.snd','.air','.act'):shutil.copy2(p,installed/p.name)
select=E/'data/select.def';text=select.read_text(encoding='utf-8')
if not re.search(r'^jin_mori\s*,',text,re.M):select.write_text(text.replace('[Characters]','[Characters]\njin_mori, stages/stage0-720.def, order=1',1),encoding='utf-8')
print('JIN_MORI_IMPORTED',len(new),'sprites',actor_rows,'illustrated actor frames')

