"""Independent form movesets with bounded effects and confirmed form ultimates."""
from pathlib import Path
import json,re,hashlib,statistics
from PIL import Image,ImageDraw,ImageFilter
from mugen_sff import Sff
from rimuru_complete import load,frame

NAMES=['Masked human','Demon Lord','Slime']
SPECIALS=[['Water Blade','Gluttony','Ranga Pounce','Black Flame'],['Hellfire Orb','Wing Step','Void Rift','Storm Spike'],['Acid Bubble','Tendril Spear','Predator Pull','Slime Slam']]
SUPERS=[['Tempest Sever','Predator Collapse','Black Lightning'],['Hellfire Wings','Chaos Rift','Draconic Burst'],['Bubble Barrage','Absorption Crush','Corrosive Wave']]
ULTS=['Megiddo','Draconic Storm','Beelzebuth Devour']
OFFSETS=[0,1,2,10,11,12,20,21,22,30,31,32,33,60,61,62,90]

def ctl(state,name,kind,trigger='1',**params):
    return f'[State {state}, {name}]\ntype={kind}\ntrigger1={trigger}\n'+''.join(k.replace('__','.')+'='+str(v)+'\n' for k,v in params.items())

def state(n,anim,kind='S',cost=0):
    return f'\n[Statedef {n}]\ntype={kind}\nmovetype=A\nphysics={"N" if kind=="A" else "C" if kind=="C" else "S"}\nanim={anim}\nctrl=0\nvelset=0,{"-1.5" if kind=="A" else "0"}\npoweradd=-{cost}\n'

def hit(n,t,damage,kind='S',low=False,final=False,p1=None,p2=None):
    p=dict(attr=kind+',HA',damage=f'{damage},4',hitflag='MAF',guardflag='L' if low else 'H' if kind=='A' else 'MA',pausetime='3,5',animtype='Hard',ground__type='Low' if low else 'High',ground__hittime=24,ground__velocity='0,0',air__velocity='0,-1.5',fall=int(final),sparkno=-1,guard__sparkno=-1,hitsound='S1,0',getpower='0,0',givepower='10,5')
    if p1 is not None:p.update(p1stateno=p1,p2stateno=p2)
    elif final:
        p['p2stateno']=879991
        p['snap']='(max(64,min(gamewidth-64,screenpos x+facing*p2dist x))-screenpos x)*facing,-pos y'
    return ctl(n,'Impact','HitDef',f'time={t}',**p)

def fx(n,t,anim,y=0,lifetime=16):
    return ctl(n,'Bounded energy','Explod',f'time={t}',anim=anim,ID=879100,postype='p1',pos=f'map(rimuru.fx_x),{y}',scale='1,1',removetime=lifetime,bindtime=1,sprpriority=3,ownpal=1,removeongethit=1)

def install(out,base=None):
    out=Path(out);source=out.parents[3]/'characters/rimuru';folder=source/'art/forms-v3'
    sff=Sff(out/'Rimuru Demon Lord.sff')
    if (8790,0) in sff.keys:raise RuntimeError('Run on the complete-v2 build or use the saved v2 runtime snapshot')
    slime=load(folder,'slime-combat',3,[11]);demon=load(folder,'demon-combat',3,[0,3,6,8]);walk=load(folder,'slime-walk',2,list(range(8)))
    for f in slime:f['scale']=18/slime[11]['image'].height
    for f in walk:f['scale']=18/statistics.median(t['image'].height for t in walk)
    extras={};sprites={}
    # These are authored gameplay particles, rendered smoothly at 512px.
    bubbles=[]
    for j in range(4):
        im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
        for x,y,r in [(256,270,140+j*3),(100,140,34+j*2),(400,100,28+j*3)]:
            d.ellipse((x-r,y-r,x+r,y+r),fill=(30,195,245,100),outline=(130,245,255,245),width=9)
            d.arc((x-r+20,y-r+20,x+r-20,y+r-20),195,285,fill=(240,255,255,240),width=12)
        bubbles.append(dict(frame(im,(256,512)),scale=.1))
    for group,tiles in [(8790,slime),(8791,demon),(8792,bubbles),(8793,walk)]:
        for i,f in enumerate(tiles):
            # The slime's mass stays on the left of extended fluid attacks.
            if group==8790 and i in (0,1,2,3,4,8,9):f['axis']=(round(f['image'].width*.32),f['image'].height)
            extras[group,i]=f;sprites[f'{group},{i}']=dict(scale=f['scale'],axis=f['axis'],rgba_sha256=f['rgba_sha256'])
    (out/'Rimuru Demon Lord.sff').write_bytes(sff.derive({},extras))
    sff=Sff(out/'Rimuru Demon Lord.sff')
    air=(out/'Rimuru Demon Lord.air').read_text(encoding='utf-8');cns='';moves=[];fxmeta={};bodymeta={}
    # Replace the clipped dash drawing with complete registered walking cycles.
    for number,indices in [(40020,range(4)),(40021,range(4,8)),(40060,range(4)),(40070,range(4,8)),(47930,range(4))]:
        block=f'[Begin Action {number}]\nClsn2Default: 1\nClsn2[0]=-13,-18,13,0\n'
        for i in indices:block+=f'8793,{i},0,0,7,,,{walk[i]["scale"]:.9f},{walk[i]["scale"]:.9f}\n'
        air=re.sub(rf'(?is)\[Begin Action {number}\].*?(?=\[Begin Action|\Z)',lambda _:block+'\n',air,count=1)
    wing_guard=load(source/'art/complete-v2','wings',2,[0,1,2,3])[6]['scale']*1.085
    for number in [20010,20011,20012]:
        match=re.search(rf'(?is)\[Begin Action {number}\].*?(?=\[Begin Action|\Z)',air)
        if not match:continue
        rows=[]
        for line in match[0].splitlines():
            if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
                p=line.split(',');p[:2]=['7951','6']
                while len(p)<9:p.append('')
                p[7]=p[8]=str(wing_guard);line=','.join(p)
            rows.append(line)
        air=air[:match.start()]+'\n'.join(rows)+'\n\n'+air[match.end():]
    oldmeta=json.loads((source/'build-report.json').read_text())['sprites']
    def body(form,pose):
        if form==2:
            return (8790,pose%12,slime[pose%12]['scale'])
        if form==1:return (8791,pose%12,demon[pose%12]['scale'])
        keys=[(1,2),(1,2),(1,9),(0,48),(0,51),(1,10),(0,60),(0,63),(0,59),(0,61),(0,52),(0,55)]
        # Find the already registered masked drawing by its authored pose key.
        wanted=['combat:0','combat:2','combat:5','movement:8','combat:7','combat:8','combat:12','combat:13','combat:14','combat:9','combat:10','combat:11'][pose%12]
        key=next(k for k,m in oldmeta.items() if m['pose']==wanted)
        g,num=map(int,key.split(','));return g,num,oldmeta[key]['scale']
    def action(n,form,poses,kind='S',attack=True,reach=52,durations=None):
        nonlocal air
        rows=[f'\n[Begin Action {n}]','Clsn2Default: 1',f'Clsn2[0]=-12,{-18 if form==2 else -32 if kind=="C" else -50},12,0']
        if attack:rows+=['Clsn1Default: 1',f'Clsn1[0]=0,{-18 if form==2 else -48},{reach},2']
        for j,pose in enumerate(poses):
            g,num,scale=body(form,pose);ticks=durations[j] if durations else 8
            rows.append(f'{g},{num},0,0,{ticks},,,{scale:.9f},{scale:.9f}')
            bodymeta[f'{g},{num}']=dict(scale=scale,axis=list(sff.headers[sff.keys[g,num]][4:6]))
        air+='\n'.join(rows)+'\n'
    def energy(anim,indices,maxw=72,maxh=84,group=7952):
        nonlocal air
        rows=[f'\n[Begin Action {anim}]'];bounds=[]
        for i in indices:
            h=sff.headers[sff.keys[group,i]];scale=min(maxw/h[2],maxh/h[3]);rows.append(f'{group},{i},0,0,4,,,{scale:.9f},{scale:.9f}');bounds.append([h[2]*scale,h[3]*scale])
        air+='\n'.join(rows)+'\n';fxmeta[str(anim)]=dict(max_width=max(x[0] for x in bounds),max_height=max(x[1] for x in bounds))
    for i,indices in enumerate([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,12,13],[13,13,13],[14,14,14],[8,10,11],[0,2,13],[4,6,13]]):energy(879100+i,indices)
    energy(879109,list(range(8)),72,42,7953);energy(879110,list(range(4)),58,58,8792)
    energy(879111,[0,1,2,3],36,32);energy(879112,[4,5,6,7],36,32);energy(879113,list(range(4)),30,30,8792)
    def safety(n,airborne=False):
        text=ctl(n,'Stay in arena','ScreenBound',value=1,movecamera='1,1')
        text+=ctl(n,'Wall-aware recoil','TargetBind','movehit=1 && numtarget && statetype!=A',time=1,pos='(max(64,min(gamewidth-64,screenpos x+facing*p2dist x))-screenpos x)*facing,-pos y')
        text+=ctl(n,'Effect position','MapSet',map='"rimuru.fx_x"',value='(max(40,min(gamewidth-40,screenpos x+facing*34))-screenpos x)*facing')
        if airborne:
            text+=ctl(n,'Air gravity','VelAdd',y=.25)+ctl(n,'Land','ChangeState','vel y>0 && pos y>=0',value=52,ctrl=0)
        return text
    def end(n,t,airborne=False):return ctl(n,'Recover','ChangeState',f'time>={t}',value=50 if airborne else 0,ctrl=1)
    for form in range(3):
        b=870000+form*1000
        for offset in OFFSETS:
            n=b+offset;ult=offset==90
            if ult:continue
            kind='C' if 10<=offset<=12 else 'A' if 20<=offset<=22 else 'S'
            strength=offset%10
            if offset<30:
                poses=([0,1,3] if strength==0 else [0,2,3] if strength==1 else [5,6,3]) if form==0 else ([0,1,3] if strength==0 else [0,2,3] if strength==1 else [6,9,3]) if form==1 else ([11,0,11] if strength==0 else [11,1,11] if strength==1 else [11,2,11])
                if kind=='C':poses=[3,4,3] if form<2 else [6,1,6]
                if kind=='A':poses=[6,7,6] if form==0 else [5,5,3] if form==1 else [4,4,11]
                damage=[38,62,88][strength]+form*3;startup=[8,12,17][strength]+(2 if form==0 else -1 if form==1 else 0);cost=0;total=[29,36,44][strength];reach=[42,50,58][strength]
                label=['Light','Medium','Heavy'][strength]+' '+('crouch' if kind=='C' else 'air' if kind=='A' else 'standing')
                action(n,form,poses,kind,True,reach,[startup,8,total-startup-8]);cns+=state(n,n,kind)+safety(n,kind=='A')+hit(n,startup,damage,kind,kind=='C',strength==2)+fx(n,startup,879100+(11+form if kind=='A' else 0 if form==0 else 1 if form==1 else 10),0,12)+end(n,total,kind=='A')
            elif offset<60:
                index=offset-30;cost=500;total=[52,48,58,56][index];startup=[12,10,18,20][index];damage=[95,110,125,130][index]+form*5;reach=[76,64,78,64][index]
                label=SPECIALS[form][index];poses=([5,11,5] if form==0 else [6,9,3] if form==1 else [11,3 if index==0 else 2 if index==1 else 8 if index==2 else 5,11]);action(n,form,poses,attack=True,reach=reach,durations=[startup,18,total-startup-18]);cns+=state(n,n,cost=cost)+safety(n)
                # Compact signatures use actual hitboxes in front of the body.
                # No target teleport, full-screen projectile or camera helper.
                cns+=hit(n,startup,damage,final=True)+fx(n,startup,879100+([0,2,9,1][index] if form==0 else [1,7,2,3][index] if form==1 else [10,0,6,8][index]))
                if index==1:cns+=ctl(n,'Bounded approach','VelSet',f'time>={startup-5} && time<{startup}',x='min(2,max(0,(p2dist x-36)/5))')+ctl(n,'Brake','VelSet',f'time>={startup}',x=0)
                cns+=end(n,total)
            else:
                index=offset-60;cost=[1000,1500,2000][index];total=[68,84,96][index];startup=[16,22,26][index];damage=[70,80,95][index]+form*5;reach=84
                label=SUPERS[form][index];poses=[0,1,2,3] if form==0 and index==0 else [6,9,10,3] if form==1 else [10,3,8,11] if form==2 else [5,11,10,5]
                action(n,form,poses,attack=True,reach=reach,durations=[startup,16,20,total-startup-36]);cns+=state(n,n,cost=cost)+safety(n)
                cns+=ctl(n,'Super power','SuperPause','!time',time=10,movetime=10,anim=-1,darken=0,sound='S950,2')+ctl(n,'Contrast','BGPalFX','!time',time=total,mul='130,155,190')
                for j,t in enumerate([startup,startup+16,startup+32]):cns+=hit(n,t,damage,final=j==2)+fx(n,t,879100+([0,2,3][index] if form==0 else [1,2,8][index] if form==1 else [10,6,0][index]))+ctl(n,'Impact weight','EnvShake',f'time={t}',time=6,ampl=4 if j<2 else 7)
                cns+=end(n,total)
            moves.append(dict(form=form,form_name=NAMES[form],state=n,offset=offset,name=label,cost=cost,kind=kind,total=total,damage=damage*(3 if offset>=60 else 1)))
        # Form-specific ultimate: only a confirmed opening enters the framed scene.
        n=b+90;confirmed=n+1
        action(n,form,[0,10,10] if form==0 else [8,9,10] if form==1 else [10,8,9],durations=[14,12,24],reach=70)
        action(confirmed,form,[10,10,11,10] if form==0 else [8,9,10,9] if form==1 else [8,9,10,11],durations=[28,48,64,68],reach=0,attack=False)
        cns+=state(n,n,cost=1000)+safety(n)+ctl(n,'Ultimate power','SuperPause','!time',time=12,movetime=12,anim=-1,darken=0,sound='S950,2')+hit(n,24,10,p1=confirmed,p2=879990)+end(n,64)
        cns+=state(confirmed,confirmed,cost=2000)
        cns+=ctl(confirmed,'Camera anchor','MapSet','!time',map='"rimuru.anchor"',value='camerapos x')
        cns+=ctl(confirmed,'Hold framing','ScreenBound',value=0,movecamera='0,0')+ctl(confirmed,'Caster position','PosSet',x='map(rimuru.anchor)-facing*38',y=0)
        cns+=ctl(confirmed,'Effect position','MapSet',map='"rimuru.fx_x"',value=54)
        cns+=ctl(confirmed,'Protected casting','NotHitBy','time<184',value='SCA',time=1)
        cns+=ctl(confirmed,'Keep target in scene','TargetBind','time<184',time=1,pos='58,0')
        cns+=ctl(confirmed,'Darkened arena','BGPalFX','!time',time=208,mul=['70,105,155','80,65,120','55,110,130'][form])
        ticks=[28,46,64,82,100,118,136,154,172] if form==0 else [32,52,72,92,112,132,152,172] if form==1 else [36,60,84,108,132,156]
        dmg=[34,42,50][form]
        for j,t in enumerate(ticks):
            cns+=ctl(confirmed,'Actual sequence damage','TargetLifeAdd',f'time={t}',value=-dmg,kill=0,absolute=1)+ctl(confirmed,'Combo count','HitAdd',f'time={t}',value=1)
            effect=3 if form==0 else (1 if j%2==0 else 7) if form==1 else (6 if j%2==0 else 4)
            cns+=fx(confirmed,t,879100+effect)+ctl(confirmed,'Sequence impact','EnvShake',f'time={t}',time=6,ampl=4)
        finish=[110,134,140][form]
        cns+=ctl(confirmed,'Finishing damage','TargetLifeAdd','time=184',value=-finish,kill=1,absolute=1)+ctl(confirmed,'Finish combo','HitAdd','time=184',value=1)+fx(confirmed,184,879108 if form==1 else 879106,lifetime=20)
        cns+=ctl(confirmed,'Release into knockdown','TargetState','time=184',value=879991)+ctl(confirmed,'Final quake','EnvShake','time=184',time=12,ampl=8)+end(confirmed,210)
        moves.append(dict(form=form,form_name=NAMES[form],state=n,confirmed=confirmed,offset=90,name=ULTS[form],cost=3000,kind='S',total=280,damage=10+len(ticks)*dmg+finish))
    cns+='''
[Statedef 879990]
type=S
movetype=H
physics=N
velset=0,0
[State 879990, Own reaction]
type=ChangeAnim
trigger1=!time
value=5000
[State 879990, Framed victim]
type=ScreenBound
trigger1=1
value=0
movecamera=0,0
[State 879990, Protection]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 879990, Safety release]
type=SelfState
trigger1=time>250
value=0
ctrl=1
[Statedef 879991]
type=L
movetype=H
physics=N
velset=0,0
[State 879991, Own knockdown]
type=ChangeAnim
trigger1=!time
value=ifelse(selfanimexist(5110),5110,5000)
[State 879991, Grounded finish]
type=PosSet
trigger1=1
y=0
[State 879991, Native getup]
type=SelfState
trigger1=time>=18
value=5120
ctrl=0
'''
    (out/'rimuru_forms.cns').write_text(cns,encoding='utf-8');(out/'Rimuru Demon Lord.air').write_text(air,encoding='utf-8')
    # New routes supersede source states for all forms and retain the familiar
    # Jinwoo pattern: standing/crouching/aerial Z/X/C, A skills, S super, D ult.
    command=(out/'Rimuru Demon Lord.cmd').read_text(encoding='utf-8');defs='';routes=''
    controls=[('rf_ult','~z',90,3000),('rf_form','/$D,~y',None,0),('rf_super_back','/$B,~y',61,1500),('rf_super_forward','/$F,~y',62,2000),('rf_super','~y',60,1000),('rf_down','/$D,~x',33,500),('rf_back','/$B,~x',32,500),('rf_forward','/$F,~x',31,500),('rf_special','~x',30,500)]
    for name,key,offset,cost in controls:
        defs+=f'[Command]\nname="{name}"\ncommand={key}\ntime=15\n'
        value='ifelse(map(rimuru.form)=0,7940,ifelse(map(rimuru.form)=1,7941,7942))' if offset is None else f'870000+map(rimuru.form)*1000+{offset}'
        routes+=ctl(-1,name,'ChangeState',f'command="{name}" && ctrl && statetype!=A && power>={cost}',value=value)
    for i,name in enumerate(['a','b','c']):
        for kind,offset in [('A',20+i),('C',10+i),('S',i)]:routes+=ctl(-1,'Form normal','ChangeState',f'command="{name}" && statetype={kind} && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && {i}>stateno%1000))',value=f'870000+map(rimuru.form)*1000+{offset}')
    command=command.replace('[Statedef -1]',defs+'\n[Statedef -1]\n'+routes,1);(out/'Rimuru Demon Lord.cmd').write_text(command,encoding='utf-8')
    ai=(out/'IA.cns').read_text(encoding='utf-8');safe=ctl(-3,'Consistent edge room','Width','!ishelper',edge='ifelse(movetype=A,48,34),ifelse(movetype=A,48,34)')
    # Redirect creator AI and old motion commands to the same bounded movesets.
    for legacy,offset in [(200,0),(220,1),(250,2),(330,10),(340,11),(600,20),(620,21),(650,22),(660,22),(670,21),(1000,30),(1100,33),(1200,32),(1300,33),(1400,62),(1500,61),(7960,60),(7970,61),(4500,90)]:
        safe+=ctl(-3,'Legacy route adapter','ChangeState',f'!ishelper && stateno={legacy}',value=f'870000+map(rimuru.form)*1000+{offset}')
    ai=re.sub(r'(?i)\[statedef -3\]',lambda m:m[0]+'\n'+safe,ai,count=1);(out/'IA.cns').write_text(ai,encoding='utf-8')
    definition=(out/'rimuru.def').read_text(encoding='utf-8');definition=definition.replace('st5=','st6=rimuru_forms.cns\nst5=');(out/'rimuru.def').write_text(definition,encoding='utf-8')
    report=dict(revision=3,forms=NAMES,moves=moves,attacks_per_form=17,controls={'normals':'Z/X/C standing, crouching and airborne','signatures':'A / forward+A / back+A / down+A','supers':'S / back+S / forward+S','ultimate':'D','forms':'W or down+S'},body_sprites=bodymeta,added_sprites=sprites,effects=fxmeta,screen_safety={'effect_margin':40,'max_effect_width':72,'max_effect_height':84,'camera_zoom':False,'ultimate_anchor':'current camera center; fixed actor scale'},art={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.png')})
    (source/'forms-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    # Refresh production fingerprints after the complete adaptation.
    b=json.loads((source/'build-report.json').read_text());b['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ('.def','.air','.cns','.cmd','.sff') and not p.name.startswith(('test-','rimuru_test'))};b['status']='Forms v3 built; native validation pending';(source/'build-report.json').write_text(json.dumps(b,indent=2),encoding='utf-8')
    print('RIMURU_FORM_MOVESETS',len(moves),'attacks;',len(fxmeta),'bounded effect actions')

if __name__=='__main__':
    from rimuru_source import ROOT
    install(ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru')
