"""Drive original command routes in test copies; preserve all production files."""
from pathlib import Path
import json,re,subprocess,datetime,concurrent.futures,hashlib,sys,shutil
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';stamp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
def q(s):return "'"+str(s).replace("'","''")+"'"
def run(slug):
 f=R/'sprite-fighter/characters'/slug;n=E/'chars'/slug;capture='import-controls-'+stamp;folder=f/'replays'/capture;folder.mkdir(parents=True)
 cases=[dict(name='Walk forward',input=2,move=True,length=130),dict(name='Jump',input=1,air=True,length=160)]
 if slug=='naruto':
  for form,name,state in [(0,'Base',200),(1,'Sage',11200),(2,'Ashura',2200),(3,'KCM1',13200),(4,'KCM2',15200),(5,'Four tails',17200),(6,'Six tails',19200)]:cases.append(dict(name=name+' normal attack',form=form,commands=['a'],state=state,damage=True,length=200))
  cases += [dict(name='Sage transformation',commands=['y'],held=['hold_y'],hold_until=160,state=811,result_form=1,length=340),dict(name='KCM1 transformation',commands=['x'],state=830,result_form=3,length=220),dict(name='KCM2 transformation',commands=['x'],held=['holddown'],state=840,result_form=4,length=220),dict(name='Kurama avatar transformation',form=3,commands=['y'],state=10001,length=480),dict(name='Return from KCM2 to base',form=4,commands=['s'],held=['holddown'],state=815,result_form=0,length=220),dict(name='KCM1 blocked without chakra',chakra=0,commands=['x'],forbid=830,result_form=0,length=160),dict(name='Rasengan',commands=['SPECIAL 1'],held=['hold_a'],hold_until=65,state=1000,damage=True,close=True,length=400),dict(name='Rasengan blocked without meter',meter=0,commands=['SPECIAL 1'],forbid=1000,length=160)]
  source='IA.cns';main='Naruto.cns'
 else:
  cases += [dict(name='Normal punch',commands=['x'],state=200,damage=True,length=180),dict(name='Consecutive normal punches',commands=['Two-Handed Consecutive Punches'],state=1100,damage=True,length=650),dict(name='Serious punch',commands=['Serious Punch'],state=1500,damage=True,length=1500),dict(name='Serious table flip',commands=['Serious Table Flip'],state=1200,length=500),dict(name='Genos summon',commands=['Genos'],state=300,length=240),dict(name='Forward teleport',commands=['Teleport Forward'],state=1600,length=200)]
  source=main='Saitama.cns'
 names=sorted({name for c in cases for name in c.get('commands',[])+c.get('held',[])})
 fixture=''
 for i,name in enumerate(names):fixture+=f'\n[State -3, Original command {i}]\ntype=AssertCommand\ntriggerall=!ishelper\ntrigger1=map(import.command{i})>0\nname="{name}"\nbuffer.time=1\nignorehitpause=1\n'
 for i,flag in [(1,'U'),(2,'F'),(3,'B'),(4,'D')]:fixture+=f'\n[State -3, Original input {flag}]\ntype=AssertInput\ntriggerall=!ishelper\ntrigger1=map(import.input)={i}\nflag={flag}\n'
 fixture+='''
[State -3, Keep observation running]
type=AssertSpecial
triggerall=!ishelper
trigger1=1
flag=globalnoko
ignorehitpause=1
[State -3, Reset old helpers between cases]
type=DestroySelf
triggerall=ishelper
triggerall=!ishelper(999999)
trigger1=root,stateno=990900
ignorehitpause=1
'''
 if slug=='naruto':fixture+='''
[State -3, Initial test form]
type=VarSet
triggerall=!ishelper
trigger1=stateno=990900
v=2
value=map(import.initialform)
[State -3, Initial test chakra]
type=VarSet
triggerall=!ishelper
trigger1=stateno=990900
v=5
value=map(import.initialchakra)
'''
 text=(n/source).read_text(encoding='cp1252');text,count=re.subn(r'(?im)^(\[statedef\s+-3\])',lambda m:m[0]+'\n'+fixture,text,count=1);assert count==1
 (n/'import-controls-source.cns').write_text(text,encoding='utf-8')
 extra='''[Statedef 990900]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 990900, Grounded reset]
type=PosSet
trigger1=1
x=-15
y=0
[State 990900, Clear effects]
type=RemoveExplod
trigger1=1
[State 990900, Face opponent]
type=Turn
trigger1=facing!=1
[State 990900, Return to original idle]
type=ChangeState
trigger1=time>=5
value=0
ctrl=1
''';(n/'import-controls-reset.cns').write_text(extra)
 de=(n/(slug+'.def')).read_text(encoding='cp1252');de,swaps=re.subn(r'(?im)^(\s*(?:cns|st\d*)\s*=\s*)'+re.escape(source)+r'(?=\s*(?:;[^\r\n]*)?$)',r'\1import-controls-source.cns',de);assert swaps==(2 if slug=='saitama' else 1),(slug,swaps)
 nums=[int(x) for x in re.findall(r'(?im)^\s*st(\d+)\s*=',de)];de=re.sub(r'(?im)^\[Files\]',lambda m:m[0]+f'\nst{max(nums+[4])+1}=import-controls-reset.cns',de,count=1);(n/'import-controls.def').write_text(de,encoding='utf-8')
 # Use the engine's bundled KFM as the inert test target.  The earlier
 # harness used will_full, which is no longer part of the active roster.
 target=E/'chars/kfm';targetbase='kfm';targetname='import-controls-target-'+slug
 target_fixture='''[Statedef 990901]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 990901, Ground target]
type=PosSet
trigger1=1
x=cond(root,map(import.close),-10,15)
y=0
[State 990901, Do not push]
type=PlayerPush
trigger1=1
value=0
'''
 (target/(targetname+'.cns')).write_text(target_fixture)
 targetdef=(target/(targetbase+'.def')).read_text();targetdef=re.sub(r'(?im)^\[Files\]',lambda m:m[0]+'\nst99='+targetname+'.cns',targetdef,count=1);(target/(targetname+'.def')).write_text(targetdef)
 (f/'import-test-cases.json').write_text(json.dumps(cases,indent=2));(f/'import-test-commands.json').write_text(json.dumps(names))
 lua='''local cases=jsonDecode('../../characters/SLUG/import-test-cases.json')
local commands=jsonDecode('../../characters/SLUG/import-test-commands.json')
local index,tick,total,shot=1,0,0,0
local pending=nil
local seen,forms,damage,air,startx={}, {},0,false,0
local report={status='Running',method='Original command routes through test-only AssertCommand, production data unchanged',capture_directory='CAPTURE',checks={},frames={}}
local function save() jsonEncode(report,'../../characters/SLUG/runtime-validation.json') end
local function command(name,value) for i,n in ipairs(commands) do if n==name then mapSet('import.command'..(i-1),value) end end end
hook.add('loop','anime-import-controls',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local file=io.open('../../characters/SLUG/replays/CAPTURE/Anime_controls'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);shot=shot+1;pending=nil;save() else return end
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 tick=tick+1;total=total+1
 if tick==1 then
  seen={};forms={};damage=0;air=false
  for _,name in ipairs(commands) do command(name,0) end
  mapSet('import.input',0);mapSet('import.close',c.close and 1 or 0);mapSet('import.initialform',c.form or 0);mapSet('import.initialchakra',c.chakra or 1000);changeState(990900);setLife(1200);setPower(c.meter or 3000)
  player(2);setLife(1000);changeState(990901);player(1)
 end
 if tick==19 then startx=posX() end
 if tick==20 then
  for _,name in ipairs(c.commands or {}) do command(name,1) end
  for _,name in ipairs(c.held or {}) do command(name,1) end
  mapSet('import.input',c.input or 0)
 end
 if tick==23 then for _,name in ipairs(c.commands or {}) do command(name,0) end end
 if tick==(c.hold_until or 70) then for _,name in ipairs(c.held or {}) do command(name,0) end;mapSet('import.input',0) end
 if tick>=20 then
  seen[tostring(stateNo())]=true;forms[tostring(var(2))]=true;air=air or posY()<-1
  player(2);damage=math.max(damage,1000-life());player(1)
 end
 if tick==30 or tick==90 or tick==170 or tick==600 or tick==1000 or tick==c.length-1 then
  pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),form=var(2),power=power(),chakra=var(5),damage=damage,file='Anime_controls'..string.format('%03d',shot)..'.png'};screenshot()
 end
 if tick>=c.length then
  local ok=true
  if c.state and not seen[tostring(c.state)] then ok=false end
  if c.forbid and seen[tostring(c.forbid)] then ok=false end
  if c.result_form and not forms[tostring(c.result_form)] then ok=false end
  if c.damage and damage<=0 then ok=false end
  if c.air and not air then ok=false end
  if c.move and math.abs(posX()-startx)<2 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,states_seen=seen,forms_seen=forms,damage=damage,final_state=stateNo(),final_form=var(2),airborne=air});index=index+1;tick=0;save()
 end
end)
'''.replace('SLUG',slug).replace('CAPTURE',capture)
 mod='external/mods/-anime-import-controls-'+slug+'.lua';(E/mod).write_text(lua)
 config=(E/'save/config.ini').read_text()
 for key,value in {'Modules':mod,'ScreenshotFolder':'../../characters/'+slug+'/replays/'+capture+'/','WindowTitle':'Anime_controls','MasterVolume':'0'}.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 ini='save/anime-import-controls-'+slug+'.ini';(E/ini).write_text(config)
 args=['-config',ini,'-loadmotif','-p1',slug+'/import-controls.def','-p2','kfm/'+targetname+'.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
 cmd='$g=Start-Process -FilePath '+q(E/'Ikemen_GO.exe')+' -WorkingDirectory '+q(E)+' -ArgumentList @('+','.join(map(q,args))+') -WindowStyle Hidden -RedirectStandardOutput '+q(f/'controls-stdout.log')+' -RedirectStandardError '+q(f/'controls-stderr.log')+' -PassThru; $null=$g.Handle; $g.WaitForExit(); exit $g.ExitCode'
 result=subprocess.run(['powershell','-NoProfile','-Command',cmd],cwd=R,timeout=300)
 if result.returncode:raise RuntimeError(slug+' engine error: '+(f/'controls-stderr.log').read_text(errors='replace')[-3000:])
 d=json.loads((f/'runtime-validation.json').read_text());manifest=json.loads((f/'import-report.json').read_text());d['runtime_sha256']={name:hashlib.sha256((n/name).read_bytes()).hexdigest() for name in manifest['source_files_sha256']};(f/'runtime-validation.json').write_text(json.dumps(d,indent=2))
 for frame in d['frames']:assert (folder/frame['file']).exists()
 print('ANIME_CONTROLS_RESULT',slug,d.get('passed'),d.get('failed'),flush=True)
 for case in d['checks']:
  if not case['passed']:print('FAILED',slug,case,flush=True)
 return d.get('failed',1)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 failures=sum(pool.map(run,sys.argv[1:] or ['naruto','saitama']))
if failures:raise RuntimeError(str(failures)+' native checks failed')
