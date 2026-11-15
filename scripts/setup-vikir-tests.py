"""Native integration fixture: commands, meter, guard/miss, forms and captures."""
from pathlib import Path
import re,json,sys
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/vikir';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';C=E/'chars/vikir'
capture=sys.argv[1];assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('*.png'))
commands=['L','M','H','skill','rise','retreat','super','drain','seven','form','base','aura','step']
commands+=['guest_dolores','guest_camu','guest_aiyen','guest_sinclair','bow','ultimate']
# Reuse only a proven test harness, independently asserting Vikir's commands.
old=(R/'scripts/setup-pyowol-tests.py').read_text(encoding='utf-8')
fixture=old[old.index("fixture='[Statedef -3]"):old.index("(C/'pyowol-tests.cns')")]
ns=dict(commands=commands);exec(fixture,ns);fixture=ns['fixture']
fixture=fixture.replace('[Statedef -3]','''[Statedef -3]
[State -3, Directional skill down]
type=AssertCommand
trigger1=map(test.pulse)=5 || map(test.pulse)=11 || map(test.pulse)=12 || map(test.pulse)=17
name="holddown"
[State -3, Directional skill back]
type=AssertCommand
trigger1=map(test.pulse)=6 || map(test.pulse)=8 || map(test.pulse)=16
name="holdback"
[State -3, Directional guest forward]
type=AssertCommand
trigger1=map(test.pulse)=14 || map(test.pulse)=15 || map(test.pulse)=18
name="holdfwd"
''',1)
fixture=fixture.replace('[State 99000, Ready]','[State 99000, Clear aura]\ntype=VarSet\ntrigger1=1\nvar(20)=0\n[State 99000, Ready]')
fixture=fixture.replace('[State 99000, Ready]','[State 99000, Reset guest cooldown]\ntype=VarSet\ntrigger1=1\nvar(21)=map(test.cooldown)\n[State 99000, Ready]')
for i,button in enumerate(['a','b','c','x','y','z','d','w'],1):
    fixture=fixture.replace('[Statedef 99000]',f'[State -3, Real button input]\ntype=AssertInput\ntrigger1=map(test.key)={i}\nflag={button}\n[Statedef 99000]')
(C/'vikir-tests.cns').write_text(fixture,encoding='utf-8')
(C/'vikir_test.def').write_text((C/'vikir.def').read_text(encoding='utf-8').replace('[Arcade]','st1=vikir-tests.cns\n[Arcade]'),encoding='utf-8')
target=E/'chars/will_full'
targetcode='''[Statedef 9005]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 9005, Position]
type=PosSet
trigger1=1
x=pos x+facing*(p2dist x)+240*(enemynear,facing)
y=pos y+p2dist y
[State 9005, Direction]
type=Turn
trigger1=facing!=-map(test.facing)
[State 9005, Ready]
type=ChangeState
trigger1=time>=5
value=0
ctrl=1
'''
(target/'vikir-test-target.cns').write_text(targetcode+targetcode.replace('[Statedef 9005]','[Statedef 9006]').replace('+240*','+650*'),encoding='utf-8')
(target/'will_vikir_test.def').write_text((target/'will_hybrid_test.def').read_text(encoding='utf-8')+'\nst3=vikir-test-target.cns\n',encoding='utf-8')
cases=[]
forms=['Vikir','Night Hound','Choco','Academy']
for form,title in enumerate(forms):
    for name,extra in [('idle',{}),('walk',dict(walk=True,state=20)),('backward walk',dict(walkback=True,state=21)),('jump',dict(jump=True,state=40))]:cases.append(dict(name=title+' '+name,form=form,expectForm=form,length=150,**extra))
    cases.append(dict(name=title+' next appearance',form=form,expectForm=(form+1)%len(forms),pulse=10,state=700,length=100))
    cases.append(dict(name=title+' return to Vikir',form=form,expectForm=0,pulse=11,state=710,length=100))
    for m in json.loads((S/'build-report.json').read_text(encoding='utf-8'))['normal_moves']:
        cases.append(dict(name=title+' / '+m['name'],form=form,expectForm=0 if form==2 else form,pulse=1+(m['state']%100)//10,state=m['state'],down=m['kind']=='C',air=m['kind']=='A',damage=True,length=150))
    for pulse,n,name,cost in [(4,1000,'Hound Lunge',250),(5,1100,'Rising Hunt',500),(7,3000,'Three Fangs',1000),(8,3100,'Beelzebub Blood Draw',1500),(9,4000,'Seven Fangs',2000)]:
        cases.append(dict(name=title+' / '+name,form=form,expectForm=0 if form==2 else form,pulse=pulse,state=n,damage=True,length=210))
        if form==0:
            for suffix,extra in [('blocked',dict(guard=True,damage=False,max_damage=35)),('miss',dict(far=True,damage=False)),('insufficient meter',dict(meter=cost-1,state=None,forbid=n,damage=False))]:cases.append(dict(cases[-1] if False else dict(name=title+' / '+name,form=form,expectForm=form,pulse=pulse,state=n,length=210),**dict(extra,name=name+' '+suffix,capture=False)))
    for pulse,n,name in [(6,1200,'Silent Retreat'),(13,1300,'Quickstep')]:cases.append(dict(name=title+' / '+name,form=form,expectForm=form,pulse=pulse,state=n,length=120))
cases += [dict(name='Charge empty meter',charge=True,meter=0,state=500,gain=500,length=150),dict(name='Charge full meter',charge=True,meter=3000,forbid=500,length=150),dict(name='Sword Aura',pulse=12,state=800,requireAura=True,length=120),dict(name='Aura insufficient meter',pulse=12,meter=999,forbid=800,length=120,capture=False),dict(name='Sword Aura expires',pulse=12,state=800,expectAura=0,length=700,capture=False),dict(name='Intro',direct=190,state=190,length=150),dict(name='Seven Fangs facing left',pulse=9,state=4000,facing=-1,damage=True,length=220),dict(name='Choco sword restores human facing left',form=2,expectForm=0,pulse=4,state=1000,facing=-1,damage=True,length=180)]
extra=[]
for key,n,name,conditions in [(1,200,'Z light',{}),(2,210,'X medium',{}),(3,220,'C heavy',{}),(4,1000,'A lunge',{}),(4,1100,'down+A rising hunt',dict(down=True)),(4,1200,'back+A retreat',dict(walkback=True)),(5,3000,'S three fangs',{}),(5,3100,'back+S blood draw',dict(walkback=True)),(5,800,'down+S aura',dict(down=True)),(6,4500,'D crimson execution',{}),(7,700,'Q changes appearance',dict(expectForm=1)),(7,710,'down+Q restores Vikir',dict(form=2,down=True,expectForm=0)),(8,1300,'W quickstep',{})]:extra.append(dict(name='Keyboard / '+name,key=key,state=n,length=300,capture=False,**conditions))
for form,title in enumerate(forms):
    extra += [dict(name=title+' high strike hurtbox',form=form,expectForm=form,probe=9003,expectSelf=800 if form==2 else 775,length=150,capture=False),dict(name=title+' low strike hurtbox',form=form,expectForm=form,probe=9004,expectSelf=775,length=150,capture=False)]
extra += [dict(name='Light medium heavy combo',pulse=1,state=200,damage=True,chain=[dict(tick=32,pulse=2),dict(tick=47,pulse=3)],require_states=[200,210,220],length=160,capture=False),dict(name='Normal cancels into lunge',pulse=1,state=200,damage=True,chain=[dict(tick=32,pulse=4)],require_states=[200,1000],length=180,capture=False)]
cases+=extra
ultimate_cases=[]
for form,title in enumerate(forms):
    ultimate_cases.append(dict(name=title+' / Night Hound: Crimson Execution',form=form,expectForm=0 if form==2 else form,pulse=19,state=4500,require_states=[4500,4510],damage=True,min_damage=500,length=320,cinematic=True))
for suffix,options in [('blocked',dict(guard=True,forbid=4510,max_damage=10)),('miss',dict(far=True,forbid=4510)),('insufficient meter',dict(meter=2999,state=None,forbid=4500)),('empty meter',dict(meter=0,state=None,forbid=4500)),('facing left',dict(facing=-1,damage=True,require_states=[4510],min_damage=500)),('interrupted opener',dict(probe=9003,forbid=4510,max_damage=0,expectSelf=775))]:
    ultimate_cases.append(dict(dict(name='Crimson Execution '+suffix,pulse=19,state=4500,length=320,cinematic=True,capture=suffix=='facing left'),**options))
for side in [-1,1]:ultimate_cases.append(dict(name='Crimson Execution corner '+str(side),pulse=19,state=4500,require_states=[4510],damage=True,min_damage=500,cornerX=side*400,facing=-side,length=340,cinematic=True,capture=False))
ultimate_cases += [dict(name='Seven Fangs two-bar keyboard super',key=9,state=4000,meter=2000,damage=True,length=230,capture=False),dict(name='Charge release stops power gain',charge=True,meter=0,state=500,gain=500,max_gain=750,length=170,capture=False),dict(name='Charge reaches full and stops',charge=True,meter=2950,state=500,gain=50,max_gain=50,length=150,capture=False)]
cases+=ultimate_cases
fixture=fixture.replace('[Statedef 99000]','[State -3, Chord S]\ntype=AssertInput\ntrigger1=map(test.key)=9\nflag=y\n[State -3, Chord D]\ntype=AssertInput\ntrigger1=map(test.key)=9\nflag=z\n[Statedef 99000]')
(C/'vikir-tests.cns').write_text(fixture,encoding='utf-8')
guest_cases=[]
for form,title in enumerate(forms):
    for pulse,n,name,cost in [(14,2000,'Dolores',1250),(15,2010,'Camu',1250),(16,2020,'Aiyen',1000),(17,2030,'Sinclair',1250)]:
        guest_cases.append(dict(name=title+' / Guest '+name,form=form,expectForm=form,pulse=pulse,state=n,length=210,damage=name!='Dolores',expectSelf=920 if name=='Dolores' else 800,guest=True))
for pulse,n,name,cost in [(14,2000,'Dolores',1250),(15,2010,'Camu',1250),(16,2020,'Aiyen',1000),(17,2030,'Sinclair',1250)]:
    guest_cases.append(dict(name='Guest '+name+' insufficient meter',pulse=pulse,meter=cost-1,forbid=n,length=160,capture=False))
    if name!='Dolores':
        guest_cases += [dict(name='Guest '+name+' blocked',pulse=pulse,state=n,guard=True,max_damage=12,length=210,guest=True,capture=False),dict(name='Guest '+name+' ranged facing left',pulse=pulse,state=n,range=True,facing=-1,damage=True,length=220,guest=True)]
guest_cases += [dict(name='Dolores healing cap',pulse=14,state=2000,life=980,expectSelf=1000,length=180,guest=True,capture=False),dict(name='Dolores interrupted before heal',pulse=14,state=2000,probe=9003,expectSelf=775,length=180,guest=True,capture=False),dict(name='Shared guest cooldown',pulse=14,state=2000,forbid=2010,chain=[dict(tick=100,pulse=15)],expectSelf=920,length=240,guest=True,capture=False),dict(name='Guest cooldown blocks ultimate fallback',key=6,walk=True,cooldown=360,meter=3000,forbid=2010,max_damage=0,length=210,capture=False)]
for suffix,options in [('shot',{}),('long range',dict(range=True)),('facing left',dict(facing=-1)),('blocked',dict(guard=True,max_damage=6,damage=False))]:
    guest_cases.append(dict(dict(name='Academy / Anubis '+suffix,form=3,expectForm=3,pulse=18,state=1400,damage=True,length=220,arrow=True),**options))
guest_cases += [dict(name='Guest cooldown expires',pulse=14,state=2000,chain=[dict(tick=420,pulse=15)],require_states=[2000,2010],expectSelf=920,damage=True,length=650,guest=True,capture=False),dict(name='Camu interrupted before fire',pulse=15,state=2010,probe=9003,expectSelf=775,max_damage=0,length=180,guest=True,capture=False),dict(name='Anubis interrupted before release',form=3,expectForm=3,pulse=18,state=1400,probe=9003,expectSelf=775,max_damage=0,length=180,capture=False)]
guest_cases += [dict(name='Anubis requires academy outfit',pulse=18,form=0,expectForm=0,forbid=1400,length=160,capture=False)]
for key,n,name,conditions in [(5,2000,'forward+S Dolores',dict(walk=True)),(6,2010,'forward+D Camu',dict(walk=True)),(6,2020,'back+D Aiyen',dict(walkback=True)),(6,2030,'down+D Sinclair',dict(down=True)),(4,1400,'academy forward+A Anubis',dict(form=3,expectForm=3,walk=True))]:
    guest_cases.append(dict(name='Keyboard / '+name,key=key,state=n,length=220,capture=False,**conditions))
cases+=guest_cases
if '--ultimate' in sys.argv:cases=ultimate_cases
if '--extra' in sys.argv:cases=extra
if '--guests' in sys.argv:cases=guest_cases
if '--guest-gallery' in sys.argv:cases=[c for c in guest_cases if c.get('capture') is not False]
if '--power-gallery' in sys.argv:cases=[c for c in cases if c.get('state') in (3000,3100,4000,4500) and c.get('capture') is not False]
if '--case' in sys.argv:
    selected=sys.argv[sys.argv.index('--case')+1];cases=[c for c in cases if c['name']==selected];assert cases,selected
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Vikir / Fang Thrust','Night Hound / Hound Lunge','Choco next appearance','Vikir / Seven Fangs','Seven Fangs facing left')]
if '--portrait' in sys.argv:cases=[dict(name='HUD portrait fit',length=50)]
if '--no-capture' in sys.argv:
    for c in cases:c['capture']=False
if '--gallery' in sys.argv:
    cases=[c for c in cases if c.get('capture') is not False]
    bank=int(sys.argv[sys.argv.index('--gallery')+1]);cases=[c for i,c in enumerate(cases) if i%3==bank]
(S/'test-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
if '--no-capture' in sys.argv:(S/'gameplay-test-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
template=(R/'scripts/setup-rimuru-tests.py').read_text(encoding='utf-8')
code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0].replace('rimuru','vikir').replace('Rimuru','Vikir').replace('RIMURU','VIKIR')
code=code.replace('c.cornerX or -25','c.cornerX or -120')
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','if c.forbid and c.meter and minPower~=c.meter then ok=false end')
code=code.replace('seen={};minLife=1000','seen={};firstSeen={};shots=0;lastKey="";maxAura=0;maxGuest=0;maxArrows=0;minLife=1000')
code=code.replace("mapSet('test.charge',0)","mapSet('test.key',0);mapSet('test.charge',0)",1)
code=code.replace("mapSet('test.key',0);mapSet('test.charge',0)","mapSet('test.cooldown',c.cooldown or 0);mapSet('test.key',0);mapSet('test.charge',0)",1)
code=code.replace('if c.far then selfState(9002) end','if c.far then selfState(9002) elseif c.range then selfState(9006) end')
code=code.replace('if tick==24 then',"if tick==20 and c.key then player(1);mapSet('test.key',c.key);if c.walkback then mapSet('test.walkback',1) end end\n if tick==23 then player(1);mapSet('test.key',0) end\n if tick==25 and c.probe then player(2);changeState(c.probe) end\n for _,event in ipairs(c.chain or {}) do if tick==event.tick then player(1);mapSet('test.pulse',event.pulse) end end\n if tick==24 then")
code=code.replace('seen[tostring(stateNo())]=true;','seen[tostring(stateNo())]=true;if not firstSeen[tostring(stateNo())] then firstSeen[tostring(stateNo())]=tick end;maxAura=math.max(maxAura,var(20));')
code=code.replace('maxAura=math.max(maxAura,var(20));','maxAura=math.max(maxAura,var(20));maxGuest=math.max(maxGuest,numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230));maxArrows=math.max(maxArrows,map(\'guest.projectiles\'));')
code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.damage and minLife>=1000 then ok=false end\n if c.max_damage and 1000-minLife>c.max_damage then ok=false end\n if c.min_damage and 1000-minLife<c.min_damage then ok=false end\n if c.requireAura and maxAura==0 then ok=false end\n if c.expectAura and var(20)~=c.expectAura then ok=false end')
code=code.replace('setLife(1000);setPower(c.meter or 3000)','setLife(c.life or 800);setPower(c.meter or 3000)')
code=code.replace("local final=stateNo();", "local final=stateNo();local selfLife=life();")
code=code.replace('if c.require and not seen[tostring(c.require)] then ok=false end','if c.require and not seen[tostring(c.require)] then ok=false end\n for _,required in ipairs(c.require_states or {}) do if not seen[tostring(required)] then ok=false end end\n if c.expectSelf and selfLife~=c.expectSelf then ok=false end\n if c.state==3100 and not c.guard and not c.far and selfLife~=855 then ok=false end\n if c.state==3100 and (c.guard or c.far) and selfLife~=800 then ok=false end')
code=code.replace('damage=1000-minLife,min_power=', 'state_ticks=firstSeen,self_life=selfLife,aura=var(20),damage=1000-minLife,min_power=')
code=code.replace('state_ticks=firstSeen,','max_guest=maxGuest,max_projectiles=maxArrows,guest_cleanup=numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230),state_ticks=firstSeen,')
code=code.replace('local final=stateNo();','local actorOK=not c.guest or (maxGuest>0 and numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230)==0)\n local arrowOK=not c.arrow or maxArrows>0 or minLife<1000\n local final=stateNo();')
code=code.replace('if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end','if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end\n if c.max_gain and maxPower>(c.meter or 0)+c.max_gain then ok=false end')
code=code.replace('local ok=(not c.state','local ok=actorOK and arrowOK and (not c.state')
code=code.replace('fx_count=numExplod(879100),','guest_count=numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230),projectiles=map(\'guest.projectiles\'),fx_count=numExplod(879100),')
# A strict capture budget avoids the engine's 999-screenshot limit.
code=code.replace(' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then', ''' player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(life())
 if c.capture~=false and tick>18 and tick%3==0 and shots<((c.walk or c.walkback or c.jump or c.charge or not c.state) and 8 or 16) and tick<130 and key~=lastKey and not pending then
  shots=shots+1;lastKey=key''')
code=code.replace('fx_count=numExplod(879100)', 'fx_count=numExplod(8010)+numExplod(8020)+numExplod(8030)')
code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.cinematic and numExplod(8010)+numExplod(8020)+numExplod(8030)>0 then ok=false end\n if c.damage and minLife>=1000 then ok=false end')
build=json.loads((S/'build-report.json').read_text(encoding='utf-8'))
if '--guest-gallery' in sys.argv:
    code=code.replace("..':'..tostring(life())", "..':'..tostring(life())..':'..tostring(math.floor(tick/4))")
    code=code.replace('and 8 or 16','and 40 or 40').replace('tick<130','tick<175')
if '--power-gallery' in sys.argv:code=code.replace("..':'..tostring(life())","..':'..tostring(life())..':'..(c.cinematic and tostring(math.floor(tick/4)) or '')");code=code.replace('tick%3==0','tick%1==0').replace('and 8 or 16','and 40 or 64').replace('tick<130','tick<205')
code=code.replace('local report={','local report={runtime_sha256='+lua(build['runtime_sha256'])+',',1).replace('CASES',lua(cases)).replace('CAPTURE',capture)
(E/'external/mods/-vikir-tests.lua').write_text(code,encoding='utf-8')
config=(E/'save/prince-paired-tests.ini').read_text(encoding='utf-8')
for key,value in [('Modules','external/mods/-vikir-tests.lua'),('WindowTitle','Vikir_native'),('ScreenshotFolder','../../characters/vikir/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/vikir-tests.ini').write_text(config,encoding='utf-8');print('VIKIR_TESTS_READY',len(cases))
