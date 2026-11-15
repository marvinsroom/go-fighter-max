"""Compose the four existing kits into the user's two explicit fighter pairs.

Prince <-> Rick James; Tyrone Biggums <-> Negan. Component packages are frozen
before composing so rebuilding a pair never accidentally consumes its own output.
"""
from pathlib import Path
import hashlib,json,re,shutil,struct
from fighter_assets import FighterAssets
import will_agent_j as bank
import chappelle_signature_moves as signature
import chappelle_proportions as proportions
import chappelle_cinematics as cinematics
import negan_execution
import chappelle_finishers

ROOT=Path(__file__).resolve().parents[1];CH=ROOT/'sprite-fighter/characters';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
ARCHIVE=CH/'chappelle/components-v1'
KEYS=['idle','walk_a','walk_b','palm','kick','special','crouch','hurt','down']
PAIRS={'prince':[('prince',0,'Prince'),('rick',0,'Rick James')],
       'tyrone':[('rick',1,'Tyrone Biggums'),('negan',0,'Negan')]}
FORM_STATES={4100,4110,4120,4130,4200,4400,4410,4500,4510}
RICK_STATES={1000,1010,1020,1100,1110,1120,1121,1130,1200,1400,3000,3010,3200,3210}

def snapshot():
    for slug in ['prince','rick','negan']:
        dest=ARCHIVE/slug
        if (dest/'component.json').exists():continue
        dest.mkdir(parents=True,exist_ok=True)
        for suffix in ['def','cmd','cns','air','sff','snd']:
            shutil.copy2(E/'chars'/slug/(slug+'.'+suffix),dest/(slug+'.'+suffix))
        shutil.copy2(CH/slug/'build-report.json',dest/'component.json')
    # Existing validation refers to the previous three-slot layout. Preserve it
    # separately; new pairing results must never be mislabeled as that old run.
    for slug in ['prince','rick','negan']:
        old=CH/slug/'verification.json'
        if old.exists() and not (ARCHIVE/slug/'verification.json').exists():shutil.copy2(old,ARCHIVE/slug/'verification.json')

def blocks(text,kind):
    return re.split(r'(?=\['+kind+r'\b)',text,flags=re.I)

def number(block,kind):
    m=re.match(r'\['+kind+r'\s+(-?\d+)\]',block,re.I);return int(m[1]) if m else None

def split_args(text):
    parts=[];depth=0;start=0
    for i,c in enumerate(text):
        if c=='(':depth+=1
        elif c==')':depth-=1
        elif c==',' and depth==0:parts.append(text[start:i]);start=i+1
    parts.append(text[start:]);return parts

def strip_form(expression):
    """Remove the former Rick/Tyrone animation choice, preserving other logic."""
    s=expression.strip()
    while s.startswith('(') and s.endswith(')'):
        depth=0;whole=True
        for i,c in enumerate(s):
            if c=='(':depth+=1
            elif c==')':depth-=1
            if depth==0 and i<len(s)-1:whole=False;break
        if not whole:break
        s=s[1:-1].strip()
    if s.lower().startswith('ifelse(') and s.endswith(')'):
        args=split_args(s[7:-1])
        if len(args)==3:
            if 'var(45)' in args[0]:return strip_form(args[2])
            return 'ifelse('+args[0]+','+strip_form(args[1])+','+strip_form(args[2])+')'
    return s

def map_expression(expression,lookup):
    s=strip_form(expression)
    if re.fullmatch(r'-?\d+',s):return str(lookup.get(int(s),int(s)))
    if s.lower().startswith('ifelse(') and s.endswith(')'):
        args=split_args(s[7:-1])
        if len(args)==3:return 'ifelse('+args[0]+','+map_expression(args[1],lookup)+','+map_expression(args[2],lookup)+')'
    return s

def state_tests(text,lookup):
    # Only comparisons of state numbers are translated. Time, damage, meter,
    # variables and animation element indices keep their original values.
    return re.sub(r'\b(stateno|prevstateno)\s*(!=|>=|<=|=|>|<)\s*(-?\d+)',
      lambda m:m[1]+m[2]+str(lookup.get(int(m[3]),int(m[3]))),text,flags=re.I)

def controller(block,states,anims,form,selected,global_controller=False):
    typ=re.search(r'^type\s*=\s*(\w+)',block,re.M|re.I)
    if not typ:return block
    kind=typ[1].lower()
    if any(label in block for label in ['Keep Tyrone drawing','Restore Rick drawing','Form cooldown']):return ''
    out=state_tests(block,states)
    if global_controller:
        pos=out.index('\n',out.index('type='))+1
        out=out[:pos]+f'triggerall=var(45)={form}\n'+out[pos:]
    for field in ['anim','projanim','projhitanim','projremanim']:
        out=re.sub(r'^('+field+r'\s*=)([^\n]+)',lambda m:m[1]+map_expression(m[2],anims),out,flags=re.M|re.I)
    if kind in ['changestate','selfstate']:
        out=re.sub(r'^(value\s*=)([^\n]+)',lambda m:m[1]+map_expression(m[2],states),out,flags=re.M|re.I)
    elif kind in ['changeanim','changeanim2']:
        out=re.sub(r'^(value\s*=)([^\n]+)',lambda m:m[1]+map_expression(m[2],anims),out,flags=re.M|re.I)
    elif kind=='explod':pass
    for field in ['p1stateno','p2stateno']:
        out=re.sub(r'^('+field+r'\s*=)([^\n]+)',lambda m:m[1]+map_expression(m[2],states),out,flags=re.M|re.I)
    return out

def build_pair(slug,forms):
    assets=FighterAssets(ROOT,slug);out=assets.output;source=assets.source
    source.mkdir(parents=True,exist_ok=True)
    data=[]
    for i,(component,selected,label) in enumerate(forms):
        directory=ARCHIVE/component;meta=json.loads((directory/'component.json').read_text())
        cns=(directory/(component+'.cns')).read_text();cmd=(directory/(component+'.cmd')).read_text()
        original_air={number(b,'Begin Action'):b for b in blocks((directory/(component+'.air')).read_text(),'Begin Action') if number(b,'Begin Action') is not None}
        for j,key in enumerate(KEYS):
            m=meta['sprites'][('tyrone_' if selected else '')+key]
            assets.png(('alt_' if i else '')+key,ROOT/m['file'],365,j,group=50+i)
        scale=assets.meta[('alt_' if i else '')+'idle']['scale']
        for key in KEYS:assets.meta[('alt_' if i else '')+key]['scale']=scale
        calibration=proportions.calibrate(assets,'alt_' if i else '',label)
        own={n:b for b in blocks(cns,'Statedef') if (n:=number(b,'Statedef')) is not None and n>=0 and n not in {2000,8250,8260,9000}}
        if component=='rick':
            own={n:b for n,b in own.items() if n not in (RICK_STATES if selected else FORM_STATES)}
        states={n:n+i*10000 for n in own}
        # Canonical AIR actions are baked from the selected source look. Tyrone's
        # old +10000 drawing bank becomes this pair's base animation bank.
        chosen={}
        for n,b in original_air.items():
            if n>=6000:continue
            candidate=original_air.get(n+10000,b) if selected else b
            rows=[line for line in candidate.splitlines() if re.match(r'^\d+,',line)]
            group=51 if selected else 50
            if rows and all(int(line.split(',')[0])==group for line in rows):chosen[n]=candidate
        for n,b in original_air.items():
            if 6400<=n<6500:chosen[n]=b
        anims={n:(21000 if i else 20000)+(n-6400) if n>=6400 else n+i*10000 for n in chosen}
        for n,b in chosen.items():
            lines=b.strip().splitlines();lines[0]=f'[Begin Action {anims[n]}]'
            for k,line in enumerate(lines[1:],1):
                if not re.match(r'^\d+,',line):continue
                p=line.split(',')
                if int(p[0])==7000:p[0]=str(7000+i)
                else:
                    p[0]=str(50+i)
                    m=assets.meta[('alt_' if i else '')+KEYS[int(p[1])]]
                    p[7]=p[8]=f'{m["scale"]:.7f}'
                lines[k]=','.join(p)
            assets.air.append('\n'+'\n'.join(lines))
        # Copy the component's code-native effects without raster alteration.
        archive=(directory/(component+'.sff')).read_bytes();header,count=struct.unpack_from('<II',archive,36);start=struct.unpack_from('<I',archive,52)[0]
        for k in range(count):
            h=list(struct.unpack_from('<HHHHhhHBBIIHH',archive,header+k*28))
            if h[0]!=7000:continue
            raw=archive[start+h[9]:start+h[9]+h[10]];h[0]=7000+i;h[9]=len(assets.payload);assets.payload.extend(raw)
            assets.headers.append(struct.pack('<HHHHhhHBBIIHH',*h))
        source_cmd=cmd[cmd.lower().index('[statedef -1]')+len('[statedef -1]'):]
        input_defs=cmd[:cmd.lower().index('[statedef -1]')]
        commands=[]
        for b in blocks(source_cmd,'State'):
            if not b.lstrip().startswith('[State'):continue
            if 'command="transform"' in b or re.search(r'^value=2000\s*$',b,re.M):continue
            requirement=re.search(r'^triggerall=var\(45\)=(\d+)',b,re.M)
            if requirement and int(requirement[1])!=selected:continue
            b=re.sub(r'^triggerall=var\(45\)=\d+\s*\n','',b,flags=re.M)
            b=controller(b,states,anims,i,selected,global_controller=True)
            commands.append(b)
        globals=[]
        for b in blocks(cns,'Statedef'):
            if number(b,'Statedef')!=-2:continue
            for c in blocks(b[b.index(']')+1:],'State'):
                if c.lstrip().startswith('[State'):globals.append(controller(c,states,anims,i,selected,True))
        positive=[]
        for n,b in own.items():
            chunks=blocks(b[b.index(']')+1:],'State');params=chunks[0]
            params=state_tests(params,states)
            params=re.sub(r'^(anim=)([^\n]+)',lambda m:m[1]+map_expression(m[2],anims),params,flags=re.M)
            # Common-state recovery can enter base state 0 before routing to the
            # alternate movement bank. Select the correct idle immediately.
            if n==0 and i==0:params=re.sub(r'^anim=0$', 'anim=ifelse(var(45)>0,10000,0)',params,flags=re.M)
            positive.append(f'\n[Statedef {states[n]}]'+params+''.join(controller(c,states,anims,i,selected) for c in chunks[1:]))
        data.append(dict(label=label,component=component,selected=selected,calibration=calibration,meta=meta,states=states,anims=anims,commands=commands,globals=globals,positive=positive,input_defs=input_defs))
    # Compatibility aliases support legacy opponent-owned AIR before own art is
    # selected. Active reaction code uses this pair's canonical form banks.
    for group,prefix in [(0,''),(10,'alt_')]:
        for j,key in enumerate(['idle']*4+['palm','crouch','kick','palm','palm','kick','hurt','down','idle','idle']):assets.alias(group,j,prefix+key)
    for n,frames in [(3900,[('idle',18),('alt_idle',12),('alt_idle',12)]),(13900,[('alt_idle',18),('idle',12),('idle',12)])]:assets.action(n,frames)
    signature_moves=signature.install(assets,data)
    cinematic_art=cinematics.install(assets,data)
    execution=negan_execution.install(assets,data,cinematics.pack)
    if execution:cinematic_art['Negan']['execution']=execution
    authored_finishers=chappelle_finishers.install(assets,data,cinematics.pack)
    assets.write_sff(slug+'.sff');assets.write_air(slug+'.air')
    shutil.copy2(ARCHIVE/forms[0][0]/(forms[0][0]+'.snd'),out/(slug+'.snd'))
    title=forms[0][2]+' / '+forms[1][2]
    (out/(slug+'.def')).write_text(f'[Info]\nname="Chappelle: {title}"\ndisplayname="{title}"\nauthor="Game1 project"\nmugenversion=1.1\nlocalcoord=1280,720\n[Files]\ncmd={slug}.cmd\ncns={slug}.cns\nst={slug}.cns\nstcommon={slug}-common.cns.zss\nsprite={slug}.sff\nanim={slug}.air\nsound={slug}.snd\n')
    common=bank.common_states((E/'data/common1.cns.zss').read_text()).replace('var(30)','var(45)').replace('Local Will copy','Local paired Chappelle copy')
    (out/(slug+'-common.cns.zss')).write_text(common)
    signature_defs,signature_routes=signature.command_routes(data)
    cmd=data[0]['input_defs']+signature_defs+'\n[Statedef -1]\n'+'''\n[State -1, Toggle paired form]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(47)=0
trigger1=command="transform"
value=3900
ctrl=0
'''+signature_routes+''.join(''.join(f['commands']) for f in data)
    (out/(slug+'.cmd')).write_text(cmd)
    original=(ARCHIVE/forms[0][0]/(forms[0][0]+'.cns')).read_text();cns=original[:original.lower().index('[statedef')]
    cns+='\n[Statedef -2]\n'+'''[State -2, Paired transformation cooldown]
type=VarAdd
trigger1=var(47)>0
var(47)=-1
[State -2, Return to alternate movement after common recovery]
type=ChangeState
triggerall=var(45)=1
trigger1=stateno=0
value=10000
ctrl=1
'''+''.join(''.join(f['globals']) for f in data)
    cns+='\n[State -2, Dismount interrupted couch]\ntype=RemoveExplod\ntrigger1=stateno!=11500\nID=6901\n'
    cns+=''.join(''.join(f['positive']) for f in data)
    cns+=''.join(signature.states(i,f['label']) for i,f in enumerate(data))
    cns+='''
[Statedef 3900]
type=S
movetype=I
physics=N
ctrl=0
anim=ifelse(var(45)>0,13900,3900)
velset=0,0
[State 3900, Clear previous form trails]
type=AfterImageTime
trigger1=time=0
time=0
[State 3900, Remember starting form]
type=VarSet
trigger1=time=0
var(46)=var(45)
[State 3900, Toggle paired form]
type=VarSet
trigger1=time=18
var(45)=1-var(46)
[State 3900, Immediate paired drawing]
type=ChangeAnim
trigger1=time=18
value=ifelse(var(45)>0,3900,13900)
elem=2
[State 3900, Shared cooldown]
type=VarSet
trigger1=time=18
var(47)=90
[State 3900, Transform flash]
type=PalFX
trigger1=time=18
time=10
add=110,80,30
mul=256,256,256
[State 3900, Recover in selected kit]
type=ChangeState
trigger1=time>=41
value=ifelse(var(45)>0,10000,0)
ctrl=1
'''
    # Captured states run on the victim, so these expressions select that
    # victim's active form rather than the attacking fighter's animation bank.
    for n,anim in [(8250,5000),(8260,5050)]:
        cns+=f'\n[Statedef {n}]\ntype={"S" if n==8250 else "A"}\nmovetype=H\nphysics=N\nctrl=0\n[State {n}, Own active reaction]\ntype=ChangeAnim\ntrigger1=time=0\nvalue=ifelse(var(45)>0 && selfanimexist({anim}+var(45)*10000),{anim}+var(45)*10000,ifelse(var(30)=1 && selfanimexist({anim+10000}),{anim+10000},{anim}))\n'
        if n==8250:cns+='[State 8250, Capture protection]\ntype=NotHitBy\ntrigger1=1\nvalue=SCA\ntime=1\n[State 8250, Orphan safety]\ntype=SelfState\ntrigger1=time>600\nvalue=0\nctrl=1\n'
        else:cns+='[State 8260, Throw launch]\ntype=VelSet\ntrigger1=time=0\nx=-6\ny=-9\n[State 8260, Gravity]\ntype=VelAdd\ntrigger1=1\ny=.65\n[State 8260, Land]\ntype=SelfState\ntrigger1=vel y>0\ntrigger1=pos y>=0\nvalue=5100\n'
    cns+='''
[Statedef 9000]
type=S
movetype=I
physics=N
ctrl=0
anim=0
[State 9000, Clear replay trails]
type=AfterImageTime
trigger1=1
time=0
[State 9000, Reset form]
type=VarSet
trigger1=1
var(45)=0
[State 9000, Reset cooldown]
type=VarSet
trigger1=1
var(47)=0
[State 9000, Reset legacy form]
type=VarSet
trigger1=1
var(30)=0
[State 9000, Health]
type=LifeSet
trigger1=1
value=1000
[State 9000, Meter]
type=PowerSet
trigger1=1
value=3000
[State 9000, Position]
type=PosSet
trigger1=1
x=ifelse(teamside=1,-60,60)
y=0
[State 9000, Stop]
type=VelSet
trigger1=1
x=0
y=0
[State 9000, Clear effects]
type=RemoveExplod
trigger1=1
[State 9000, Ready]
type=ChangeState
trigger1=1
value=0
ctrl=1
'''
    (out/(slug+'.cns')).write_text(cns)
    report={'slug':slug,'layout_revision':2,'moves_revision':3,'visual_revision':6,'authored_finishers':authored_finishers,'cinematic_art':cinematic_art,'proportion_calibration':{f['label']:f['calibration'] for f in data},'signature_moves':signature_moves,'status':'Built; cinematic validation pending','forms':[f[2] for f in forms],
      'transformation':{'key_p1':'W','key_p2':']','cost':0,'ticks':42,'reveal_tick':18,'cooldown':90,'shared_health_meter':True},
      'sprites':assets.meta,'form_sources':[{'component':f['component'],'selected_source_form':f['selected'],'label':f['label'],'state_map':f['states'],'animation_map':f['anims']} for f in data],
      'super_damage':620,'ultimate_damage':950,'limitations':['Existing first-pass key poses and shared animation drawings retained']}
    (source/'paired-build-report.json').write_text(json.dumps(report,indent=2))
    print('CHAPPELLE_PAIR_BUILT',slug,report['forms'],flush=True)

if __name__=='__main__':
    snapshot()
    for slug,forms in PAIRS.items():build_pair(slug,forms)
