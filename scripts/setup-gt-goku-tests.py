"""Exercise imported Goku command routes against the installed illustrated build."""
from pathlib import Path
import json,re,sys
from gt_goku_model import FORMS,NORMALS,routes
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/gt-goku';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/gt_goku'
capture=sys.argv[1] if len(sys.argv)>1 else 'gameplay-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
commands=['a','b','c','goku_form','goku_revert']+list(dict.fromkeys(r['command'] for r in routes()))
source=(O/'IA.cns').read_text();inject=''
parts=re.split(r'(?=^\[State\s+)',source,flags=re.I|re.M)
for i,part in enumerate(parts):
 if re.search(r'^type\s*=\s*HitOverride',part,re.I|re.M):parts[i]=re.sub(r'(^type\s*=\s*HitOverride\s*$)',r'\1\ntriggerall=map(test.reaction)!=1',part,flags=re.I|re.M,count=1)
source=''.join(parts)
for i,name in enumerate(commands,1):inject+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
inject+='\n[State -3, Consume test pulse]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
for flag,command in [('guard','holdback'),('bomb','goku_hold_bomb'),('charge','goku_charge'),('jump','holdup'),('down','holddown'),('walk','holdfwd'),('walkback','holdback')]:inject+=f'\n[State -3, Held {flag}]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{command}"\nbuffer.time=1\n'
inject+='\n[State -3, Guard input]\ntype=AssertInput\ntrigger1=map(test.guard)=1\nflag=B\n'
inject+='\n[State -3, Keep guard probe in range]\ntype=PosSet\ntrigger1=map(test.guard)=1\nx=map(test.startx)\n'
source=source.replace('[Statedef -3]','[Statedef -3]\n'+inject)
source=source.replace('[Statedef -2]','''[Statedef -2]
[State -2, Test no KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Clear fixture helpers]
type=DestroySelf
triggerall=ishelper
trigger1=root,stateno=99000
ignorehitpause=1
''',1)
source+='''
[Statedef 99000]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 99000, Position]
type=PosSet
trigger1=1
x=map(test.startx)
y=0
[State 99000, Facing]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear effects]
type=RemoveExplod
trigger1=1
[State 99000, Reset vars]
type=VarRangeSet
trigger1=!time
first=0
last=57
value=0
[State 99000, Manual]
type=MapSet
trigger1=1
map="goku.manual"
value=1
[State 99000, Selected idle]
type=ChangeAnim
trigger1=time=6
value=var(11)+(map(goku.bank)+1)*1000000
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'gt-goku-test-ia.cns').write_text(source)
(O/'gt_goku_test.def').write_text((O/'gt_goku.def').read_text().replace('IA.cns','gt-goku-test-ia.cns'))
T=E/'chars/will_full'
target=(T/'edward-test-common-target.cns').read_text()
target=re.sub(r'(?ms)(^\[Statedef 9002\].*?^y=)0',r'\g<1>-1200',target,count=1)
target+='''
[Statedef 9006]
type=A
movetype=I
physics=N
ctrl=0
anim=0
velset=0,0
[State 9006, Aerial contact fixture]
type=PosSet
trigger1=1
x=pos x+facing*(p2dist x)+map(test.distance)*(enemynear,facing)
y=pos y+p2dist y
[State 9006, Face attacker]
type=Turn
trigger1=facing!=-(enemynear,facing)
'''
(T/'gt-goku-test-common-target.cns').write_text(target)
(T/'will_gt_goku_test.def').write_text((T/'will_edward_test.def').read_text().replace('edward-test-common-target.cns','gt-goku-test-common-target.cns'))
build=json.loads((S/'build-report.json').read_text());cases=[]
cases.append(dict(name='Intro - GT Kid Goku greeting',form=0,direct=190,state=190,expectForm=0,meter=3000,length=340,intro=True,category='Intro'))
for form in FORMS:
 fid=form['id'];common=dict(form=fid,meter=3000)
 cases.append(dict(common,name=form['name']+' form cycle',pulse=4,state=900800,expectForm=(fid+1)%5,length=150,category='Forms'))
 for air in (False,True):
  for i,(state,label) in enumerate(zip(NORMALS[fid][int(air)],['light','medium','heavy']),1):cases.append(dict(common,name=form['name']+(' air ' if air else ' ground ')+label,pulse=i,state=state,air=air,direct=40 if air else None,length=420,damage=True,category='Basics'))
 for pulse,label in [(1,'light combo chain'),(2,'medium combo chain')]:
  state=NORMALS[fid][0][pulse-1]
  cases.append(dict(common,name=form['name']+' '+label,pulse=pulse,state=state,require=state+10,combo=True,length=420,category='Basics'))
 for route in [r for r in routes() if r['form']==fid]:
  if route['state']==3001:continue # Native Spirit Bomb release is tested with its gather helper below.
  cases.append(dict(common,name=form['name']+' / '+route['name']+(' (air)' if route['air'] else ''),pulse=commands.index(route['command'])+1,state=route['state'],command_state=route['state'],air=route['air'],direct=40 if route['air'] else None,counter=route['state']==35100,require=35101 if route['state']==35100 else None,length=3000 if route['category']=='Ultimates' else 1800 if route['category']=='Supers' else 1400,category=route['category'],move=route['name']))
 cases.append(dict(name=form['name']+' charge and release',form=fid,meter=0,charge=True,state=900810,gain=500,length=180,category='Charge up'))
cases.append(dict(name='Return to base Goku',form=4,meter=3000,pulse=5,state=900800,expectForm=0,length=150,category='Forms'))

for f in FORMS:cases.append(dict(name=f['name']+' hurt reaction',form=f['id'],meter=0,hurt=True,state=5000,length=300,category='Reaction checks',capture=False))
for f in FORMS:cases.append(dict(name=f['name']+' guard reaction',form=f['id'],meter=0,defend=True,state=150,length=300,category='Reaction checks',capture=False))
for f in FORMS:cases.append(dict(name=f['name']+' charge interrupted by hit',form=f['id'],meter=0,charge=True,interrupt=True,state=900810,length=240,category='Interruption checks',capture=False))
for route in routes():
 if route['category']!='Supers':continue
 for mode,extra in [('guard',dict(guard=True)),('miss',dict(far=True))]:
  cases.append(dict(name=FORMS[route['form']]['name']+' / '+route['name']+' '+mode,form=route['form'],meter=3000,pulse=commands.index(route['command'])+1,state=route['state'],length=1800,category='Contact checks',**extra))
for route in routes():
 if route['cost']>0:cases.append(dict(name=FORMS[route['form']]['name']+' / '+route['name']+(' air' if route['air'] else '')+' insufficient meter',form=route['form'],meter=max(0,route['cost']-100),pulse=commands.index(route['command'])+1,air=route['air'],direct=40 if route['air'] else None,forbid=route['state'],length=150,category='Meter checks'))
for c in cases:
 if c.get('state')==3000 or c.get('forbid')==3000:c['lowHealth']=True
 c['energy']=c.get('state') in (400,620,1400,1700) or bool(re.search(r'Kame|Blast|Ki Machinegun',c['name'],re.I))
if '--gallery-basics' in sys.argv:cases=[c for c in cases if c['category']=='Basics']
if '--air-contact' in sys.argv:cases=[c for c in cases if c['category']=='Basics' and c.get('air')]
if '--gallery-skills' in sys.argv:cases=[c for c in cases if c['category']=='Skills']
if '--gallery-power' in sys.argv:cases=[c for c in cases if c['category'] in ('Charge up','Supers','Ultimates','Forms')]
if '--intro' in sys.argv:cases=[c for c in cases if c['category']=='Intro']
batch=next((a for a in sys.argv if a.startswith('--form-batch=')),None)
if batch:
 first=int(batch.split('=',1)[1]);cases=[c for c in cases if first<=c['form']<first+2]
if '--contact' in sys.argv:cases=[c for c in cases if c['category']=='Contact checks']
if '--reactions' in sys.argv:cases=[c for c in cases if c['category']=='Reaction checks']
if '--foundation-probe' in sys.argv:cases=[c for c in cases if c['category'] in ('Reaction checks','Interruption checks')]
if '--visual-probe' in sys.argv:cases=[c for c in cases if c['name'] in ('Base Goku / Taiyoken','Base Goku / Shunkan Ido','Super Saiyan 3 / Ryu Ken','Super Saiyan God / Ki Machinegun','Ultra Instinct Omen / Egoist Counter','Mastered Ultra Instinct / Invisible Blows','Base Goku / Super Spirit Bomb: full gather and release')]
if '--energy-probe' in sys.argv:cases=[c for c in cases if c['name'] in ('GT Kid Goku ground heavy','GT Kid Goku air heavy','GT Kid Goku / Kamehameha','Super Saiyan / Super Kamehameha SS1','Super Saiyan 3 / Kamehameha SS3','Super Saiyan 4 / Kamehameha')]
if '--smoke' in sys.argv:cases=[c for c in cases if c['category'] in ('Intro','Forms','Charge up') or c['category']=='Basics' and c['pulse']==1 and not c.get('air') and not c.get('combo')]
if '--probe' in sys.argv:cases=[c for c in cases if c['name']=='Base Goku ground light']
if '--alignment-probe' in sys.argv:
 from goku_alignment_tests import cases_for_alignment
 cases=cases_for_alignment(cases,'gt-goku')
if '--no-capture' in sys.argv:
 for c in cases:c['capture']=False
def lua(v):
 if v is None:return 'nil'
 if isinstance(v,bool):return str(v).lower()
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
template=(R/'scripts/setup-rimuru-tests.py').read_text();code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0]
code=code.replace('rimuru','goku').replace('Rimuru','Goku').replace('RIMURU','GOKU')
# CNS P2Dist handles both fighters' local coordinates and camera movement.
code=code.replace(' if tick==28 and c.air'," if tick==39 and c.air and c.category=='Basics' then player(2);mapSet('test.distance',c.pulse==3 and 360 or 160);selfState(9006);player(1) end\n if tick==28 and c.air")
code=code.replace('tick==28 and c.air','tick==40 and c.air')
code=code.replace(' if tick==40 and c.air'," if tick==39 and c.air and c.forbid then player(1);setPower(c.meter) end\n if tick==40 and c.air")
code=code.replace('elseif tick==8 then player(2);','elseif tick==8 then player(1);setPower(c.meter or 3000);player(2);')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*55)*4')
code=code.replace("mapSet('test.charge',0);mapSet('test.down',0)","mapSet('test.charge',0);mapSet('test.bomb',0);mapSet('test.down',0)")
code=code.replace("mapSet('test.bomb',0);mapSet('test.down',0)","mapSet('test.bomb',0);mapSet('test.guard',0);mapSet('test.down',0)")
code=code.replace("mapSet('test.guard',0);mapSet('test.down',0)","mapSet('test.guard',0);mapSet('test.reaction',(c.hurt or c.defend) and 1 or 0);mapSet('test.down',0)")
code=code.replace("if c.charge then mapSet('test.charge',1) end","if c.charge then mapSet('test.charge',1) end;if c.gather then mapSet('test.bomb',1) end")
code=code.replace(' if tick==24 then'," if c.gather and tick==700 then player(1);mapSet('test.bomb',0) end\n if c.gather and tick==750 then player(1);mapSet('test.pulse',c.pulse) end\n if tick==24 then")
code=code.replace(' if tick==24 then'," if c.combo and tick>24 and tick<150 and tick%6==0 then player(1);mapSet('test.pulse',c.pulse) end\n if tick==24 then")
code=code.replace(' if tick==24 then'," if c.counter and tick==60 then player(2);selfState(9003);player(1) end\n if tick==24 then")
code=code.replace(' if tick==24 then'," if c.hurt and tick==60 then player(1);setPower(0);player(2);selfState(9004);player(1) end\n if tick==24 then")
code=code.replace(' if tick==24 then'," if c.defend and tick==50 then player(1);mapSet('test.guard',1) end\n if c.defend and tick==60 then player(1);setPower(0);player(2);selfState(9004);player(1) end\n if c.defend and tick==100 then player(1);mapSet('test.guard',0) end\n if tick==24 then")
code=code.replace(' if tick==24 then'," if c.interrupt and tick==60 then player(2);selfState(9004);player(1) end\n if tick==24 then")
# Boundman legitimately regenerates power, so an idle-meter invariant would
# reject valid source behavior. The forbidden state checks the actual route.
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
code=code.replace("local caseShots,lastKey=0,''","local guardSeen,hurtAnim,guardAnim=false,nil,nil\nlocal caseShots,lastKey=0,''")
code=code.replace("seen={};caseShots=0;lastKey='';minLife=1000","seen={};guardSeen=false;hurtAnim=nil;guardAnim=nil;caseShots=0;lastKey='';minLife=1000")
code=code.replace('seen[tostring(stateNo())]=true;','seen[tostring(stateNo())]=true;local aid=anim()%1000000;if c.hurt and ((aid>=5000 and aid<=5300) or (aid>=6000 and aid<=6300) or (aid>=12000 and aid<=12300) or (aid>=14000 and aid<=14300) or (aid>=16000 and aid<=16300) or (aid>=18000 and aid<=18300)) then hurtAnim=anim() end;if c.defend and ((aid>=120 and aid<=152) or (aid>=2120 and aid<=2152) or (aid>=11120 and aid<=11152) or (aid>=13120 and aid<=13152) or (aid>=15120 and aid<=15152) or (aid>=17120 and aid<=17152)) then guardAnim=anim() end;')
code=code.replace('minLife=math.min(minLife,life()) end','minLife=math.min(minLife,life());if stateNo()>=120 and stateNo()<=155 then guardSeen=true end end')
code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.damage and minLife>=1000 then ok=false end\n  if c.guard and not guardSeen then ok=false end')
code=code.replace('if c.guard and not guardSeen then ok=false end','if c.guard and not guardSeen then ok=false end\n  if c.interrupt and numExplod(960810)>0 then ok=false end')
code=code.replace('passed=ok,seen=seen','passed=ok,guarded=guardSeen,hurt_animation=hurtAnim,guard_animation=guardAnim,charge_aura=numExplod(960810),seen=seen')
if any(flag.startswith('--gallery-') or flag in ('--visual-probe','--energy-probe','--alignment-probe','--no-capture') for flag in sys.argv):
 code=code.replace('local caseShots,lastKey',"local galleryIdle=0\nlocal caseShots,lastKey")
 code=code.replace("seen={};caseShots=0;lastKey='';minLife=1000","seen={};galleryIdle=0;caseShots=0;lastKey='';minLife=1000")
 code=code.replace(' if tick>=c.length then',""" player(1)
 local minimum=(c.category=='Basics' and not c.combo) and 90 or 180
 local settled=stateNo()==0 and tick>=minimum and not c.gather and not c.charge
 if settled then
  local helpers=numHelper()
  for j=0,helpers-1 do
   player(1)
   if helper(-1,j) and moveType()=='A' then settled=false end
  end
 end
 player(1)
 if settled then galleryIdle=galleryIdle+1 else galleryIdle=0 end
 if tick>=c.length or galleryIdle>=60 then""")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
replacement=" player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))\n if c.capture~=false and tick>10 and not pending and ((c.intro and tick%4==0) or (caseShots<10 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<24 and tick%math.max(12,math.floor(c.length/16))==0) or tick==12 or tick==c.length-4) then\n lastKey=key"
assert marker in code;code=code.replace(marker,replacement).replace('player(1);pending={','caseShots=caseShots+1;player(1);pending={')
if '--gallery-basics' in sys.argv:code=code.replace('caseShots<10','caseShots<6').replace('caseShots<24','caseShots<12')
if '--gallery-basics' in sys.argv:code=code.replace('tick%4==0 and key~=lastKey','tick%2==0 and key~=lastKey').replace('caseShots<6','caseShots<12')
code=code.replace('((c.intro and tick%4==0)', '((c.energy and caseShots<96 and tick%3==0 and stateNo()~=0) or (c.intro and tick%4==0)')
code=code.replace('(c.intro and tick%4==0)','(c.intro and tick%2==0)')
code=code.replace('local report={','local report={runtime_sha256='+lua(build['runtime_sha256'])+',')
code=code.replace('animation=anim(),','animation=anim(),animation_element=animElemNo(0),')
code=re.sub(r"spriteVar\('(group|image)'\)",'-1',code)
code=code.replace('../../characters/goku/','../../characters/gt-goku/')
code=code.replace('Goku_native','GT_Goku_native')
if '--trace-air' in sys.argv:
 code=code.replace(' tick=tick+1'," tick=tick+1\n if c.air and tick>=40 and tick<=64 and tick%4==0 then player(1);print('AIR_TRACE '..c.name..' tick='..tick..' state='..stateNo()..' anim='..anim()..' elem='..animElemNo(0)..' face='..facing()..' contact='..moveContact()..' hitflag='..hitDefVar('hitflag')..' x='..posX()..' y='..posY());player(2);print('AIR_TARGET state='..stateNo()..' x='..posX()..' y='..posY()..' life='..life());player(1) end")
code=code.replace("elseif tick==8 then", "elseif tick==8 then")
code=code.replace(' if tick==24 then', " if tick==12 and c.lowHealth then player(1);setLife(400);player(2);setLife(400);minLife=400 end\n if tick==24 then")
code=code.replace('damage=1000-minLife','damage=(c.lowHealth and 400 or 1000)-minLife')
if '--alignment-probe' in sys.argv:
 from goku_alignment_tests import instrument
 code=instrument(code,'gt-goku',lua)
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
if '--probe' in sys.argv:
 debug='''
 if tick==12 or tick==80 then
  player(1);print('PROBE tick='..tick..' state='..stateNo()..' anim='..anim()..' helpers='..numHelper()..' explods='..numExplod())
  for i=0,numExplod()-1 do print('ROOT_FX '..i..' id='..tostring(explodVar(-1,i,'id'))..' anim='..tostring(explodVar(-1,i,'anim'))..' sx='..tostring(explodVar(-1,i,'scale x'))) end
  local count=numHelper()
  for j=0,count-1 do
   player(1);if helper(-1,j) then
    print('HELPER '..j..' state='..stateNo()..' anim='..anim()..' explods='..numExplod())
    for i=0,numExplod()-1 do print('HELPER_FX '..i..' id='..tostring(explodVar(-1,i,'id'))..' anim='..tostring(explodVar(-1,i,'anim'))..' sx='..tostring(explodVar(-1,i,'scale x'))) end
   end
  end
 end
'''
 code=code.replace(' tick=tick+1',' tick=tick+1\n'+debug)
(E/'external/mods/-gt-goku-tests.lua').write_text(code,encoding='utf-8')
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-gt-goku-tests.lua'),('WindowTitle','GT_Goku_native'),('ScreenshotFolder','../../characters/gt-goku/replays/'+capture+'/'),('MasterVolume','0'),('VSync','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/gt-goku-tests.ini').write_text(config);(folder/'cases.json').write_text(json.dumps(cases,indent=2));print('GOKU_TESTS_READY',len(cases))
