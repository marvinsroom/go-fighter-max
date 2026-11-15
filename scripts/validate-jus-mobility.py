"""Exercise common commands in the real engine; test fixtures never ship in config.ini."""
from pathlib import Path
import json,re,subprocess,concurrent.futures,sys,os,hashlib,datetime
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/jus-upgrade'

FIXTURE='''[Statedef -4]
[State -4, Fixture dash input]
type=AssertInput
trigger1=map(justest.dash)=1
flag=d
[State -4, Fixture backward input]
type=AssertInput
trigger1=map(justest.back)=1
flag=B
[State -4, Fixture flight input]
type=AssertInput
trigger1=map(justest.flight)=1
flag=d
[State -4, Fixture up input]
type=AssertInput
trigger1=map(justest.up)=1
trigger2=map(justest.flight)=1
flag=U
[State -4, Fixture walking input]
type=AssertInput
trigger1=map(justest.walk)=1
flag=F
[State -4, Fixture walking command]
type=AssertCommand
trigger1=map(justest.walk)=1
name="holdfwd"
buffer.time=1
[State -4, Fixture jumping input]
type=AssertInput
trigger1=map(justest.jump)=1
flag=U
[State -4, Fixture jumping command]
type=AssertCommand
trigger1=map(justest.jump)=1
name="holdup"
buffer.time=1
[Statedef 8797190]
type=A
movetype=I
physics=N
ctrl=0
anim=41
velset=0,0
[State 8797190, Position]
type=PosSet
trigger1=1
x=const240p(map(justest.worldx))-camerapos x
y=const240p(-80)
[State 8797190, Return own native airborne state]
type=SelfState
trigger1=time>=2
value=50
ctrl=1
[Statedef 8797191]
type=S
movetype=I
physics=N
ctrl=0
anim=0
velset=0,0
[State 8797191, Position]
type=PosSet
trigger1=1
x=const240p(map(justest.worldx))-camerapos x
y=0
[State 8797191, Return own native idle state]
type=SelfState
trigger1=time>=2
value=0
ctrl=1
'''

LUA='''local report={status='Running',slug='SLUG',checks={},samples={}}
local tick,warmup=0,0
local entered,backward,firstdash,second,flightSeen,flightCost,lowSeen=false,false,false,false,false,0,false
local startX,flightStart,flightPower,startFacing=0,0,0,1
local walkKeys,walkStates={},{}
local jumpPeak,jumped,landed=0,false,false
-- posX() is camera-relative; use the world root for displacement checks.
local function worldX() return posX()+cameraPosX() end
local function save() jsonEncode(report,'PROOF') end
local function check(label,ok,actual) table.insert(report.checks,{label=label,passed=ok,actual=actual});save() end
local function clear()
 for _,key in ipairs({'dash','back','flight','up','walk','jump'}) do mapSet('justest.'..key,0) end
end
local function setup(air,meter)
 clear();setPower(meter or 2000);mapSet('jus.airdash_used',0);changeState(air and 8797190 or 8797191)
end
hook.add('loop','jus-mobility-SLUG',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 tick=tick+1
 if (tick>=5 and tick<=24) or (tick>=43 and tick<=60) or (tick>=83 and tick<=100) then table.insert(report.samples,{tick=tick,state=stateNo(),y=posY(),x=posX(),control=ctrl(),facing=facing(),back=commandGetState(1,'jus.back'),up=commandGetState(1,'jus.up'),direction=map('jus.dash_direction'),dash=map('justest.dash'),used=map('jus.airdash_used')}) end
 if tick==1 then
  check('JUS layer enabled',map('jus.enabled')==1,map('jus.enabled'))
  check('Flight policy',map('jus.flight_allowed')==FLIGHT,map('jus.flight_allowed'))
  setup(true)
 end
 if tick==7 then startX=worldX();startFacing=facing();mapSet('justest.dash',1) end
 if tick>=8 and tick<=22 and stateNo()==8797101 then entered=true end
 if tick==10 then clear() end
 if tick==22 then
  check('Air dash follows common command',entered,stateNo())
  check('Air dash moves forward',(worldX()-startX)*startFacing>15*WIDTH/320,(worldX()-startX)*startFacing)
  check('Air dash consumes airborne budget',map('jus.airdash_used')==1,map('jus.airdash_used'))
  mapSet('justest.dash',1)
 end
 if tick>=24 and tick<=32 and stateNo()==8797101 then second=true end
 if tick==32 then
  check('Second dash blocked before landing',not second,stateNo());setup(false)
 end
 if tick==39 then
  check('Landing restores dash budget',map('jus.airdash_used')==0,map('jus.airdash_used'));setup(true)
 end
 -- Hold direction before the button and through state entry, as a player does.
 -- Clearing both after three ticks can drop Back before the dash's time=0.
 if tick==43 then mapSet('justest.back',1) end
 if tick==46 then startX=worldX();startFacing=facing();mapSet('justest.dash',1) end
 if tick>=47 and tick<=56 and stateNo()==8797101 then backward=true end
 if tick==49 then mapSet('justest.dash',0) end
 if tick==60 then
  check('Backward air dash enters',backward,stateNo())
  check('Backward air dash moves back',(worldX()-startX)*startFacing<-15*WIDTH/320,(worldX()-startX)*startFacing)
  setup(true,200)
 end
 if tick==64 then mapSet('justest.up',1) end
 if tick==67 then mapSet('justest.flight',1) end
 if tick>=68 and tick<=76 and stateNo()==8797102 then lowSeen=true end
 if tick==70 then clear() end
 if tick==78 then check('Flight blocked below entry meter',not lowSeen,stateNo());setup(true,2000) end
 if tick==82 then mapSet('justest.up',1) end
 if tick==85 then mapSet('justest.flight',1);flightPower=power() end
 if tick>=86 and tick<=105 and stateNo()==8797102 then flightSeen=true end
 if tick==88 then clear() end
 if tick==106 then
  check('Flight eligibility respected',flightSeen==(FLIGHT==1),flightSeen)
  if FLIGHT==1 then check('Sustained flight spends meter',power()<=flightPower-70,power());mapSet('justest.flight',1) end
 end
 if tick==110 then clear() end
 if tick==115 and FLIGHT==1 then check('Flight toggle returns to native fall',stateNo()~=8797102,stateNo()) end
 if tick==120 then setup(false) end
 if tick==127 then mapSet('justest.dash',1) end
 if tick==129 then check('Air dash never steals grounded input',stateNo()~=8797101,stateNo());clear() end
 if tick==135 then setup(false) end
 if tick==142 then startX=worldX();startFacing=facing();mapSet('justest.walk',1) end
 if tick>=145 and tick<=170 then
  walkKeys[tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))]=true
  walkStates[tostring(stateNo())]=true
 end
 if tick==171 then
  local count=0;for _ in pairs(walkKeys) do count=count+1 end
  check('Native walking moves at compact pace',(worldX()-startX)*startFacing>15*WIDTH/320,(worldX()-startX)*startFacing)
  if WALK_DRAWINGS>0 then check('Eight new walk drawings appear in native animation',count==WALK_DRAWINGS,count) end
  report.walk={distinct_drawings=count,keys=walkKeys,states=walkStates};clear()
 end
 if tick==175 then screenshot() end
 if tick==180 then setup(false) end
 if tick==187 then mapSet('justest.jump',1) end
 if tick==190 then clear() end
 if tick>=188 and tick<=285 then
  jumpPeak=math.min(jumpPeak,posY());if posY()<0 then jumped=true end
  if jumped and posY()>=0 then landed=true end
 end
 if tick==286 then
  check('Native jump clears compact fighter height',jumpPeak<-55*WIDTH/320,jumpPeak)
  check('Jump returns to ground',landed,posY());report.jump_peak=jumpPeak
 end
 if tick==290 then screenshot() end
 if tick==300 then
  report.status='Complete';report.passed=0;report.failed=0
  for _,c in ipairs(report.checks) do if c.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
'''

def q(v):return "'"+str(v).replace("'","''")+"'"
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def runtime(row):
 paths=[E/'data/jus-mobility.cns',E/'data/jus-mobility.cmd',E/'data/jusfx/jusfx.sff',E/'data/jusfx/jusfx.air',E/'data/jusfx/jusfx.def',E/'stages/stage0-720.def']
 for definition in (E/'chars'/row['engine']/row['definition'],E/'chars/naruto/naruto.def'):
  paths.append(definition);text=definition.read_text(encoding='cp1252')
  section=re.search(r'(?ims)^\[Files\](.*?)(?=^\[|\Z)',text)[1]
  for _,value in re.findall(r'(?im)^\s*(cmd|cns|st\d*|stcommon|sprite|anim|sound)\s*=\s*([^;\r\n]+)',section):
   value=value.strip().strip('"');p=definition.parent/value
   if not p.exists():p=E/'data'/value
   if p.exists():paths.append(p)
 return {p.relative_to(E).as_posix():sha(p) for p in paths}
def lua_for(row,suite):
 slug=row['slug']
 return LUA.replace('SLUG',slug).replace('PROOF','../../jus-upgrade/'+suite+'/'+slug+'/current.json').replace('FLIGHT',str(int(row['flight']))).replace('WIDTH',str(row['width'])).replace('WALK_DRAWINGS','8' if (O/'art'/slug/'packing.json').exists() else '0')
def harness(row,suite):
 data=b'manga-roster-v3'+str(row.get('speedtest',4)).encode()+lua_for(row,suite).encode()+(E/'data/jus-test-fixture.cns').read_bytes()
 if (E/'data/jus-test-fixture.air').exists():data+=(E/'data/jus-test-fixture.air').read_bytes()
 for path in row.get('harness_inputs',[]):data+=(E/path).read_bytes()
 return hashlib.sha256(data).hexdigest()
def collect(rows,suite):
 results=[]
 for row in rows:
  p=O/suite/row['slug']/'current.json'
  if not p.exists():continue
  r=json.loads(p.read_text())
  if r.get('status')=='Complete' and r.get('failed')==0 and r.get('harness_sha256')==harness(row,suite) and r.get('runtime_sha256')==runtime(row):results.append(r)
 return results
def run(row,suite='native'):
 slug=row['slug'];out=O/suite/slug;out.mkdir(parents=True,exist_ok=True)
 before=runtime(row);fingerprint=harness(row,suite);proof=out/'current.json'
 if proof.exists():
  saved=json.loads(proof.read_text())
  if saved.get('status')=='Complete' and saved.get('failed')==0 and saved.get('runtime_sha256')==before and saved.get('harness_sha256')==fingerprint and saved.get('screenshots') and all((R/p).exists() for p in saved['screenshots']):
   print(slug,'current native proof',saved['passed'],'passed',flush=True);return saved
 mod='external/mods/-jus-'+suite+'-'+slug+'.lua'
 capture=out/('run-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'));capture.mkdir()
 relative_capture=capture.relative_to(E.parent.parent).as_posix()
 capture_from_engine='../../'+relative_capture
 # relative_capture already starts jus-upgrade; screenshots belong only to
 # this run, never to an older report with the same window title.
 lua=lua_for(row,suite).replace('CAPTURE_DIR',capture_from_engine)
 (E/mod).write_text(lua)
 config=(E/'save/config.ini').read_text()
 config=config.replace('data/jus-mobility.cns','data/jus-test-fixture.cns, data/jus-mobility.cns')
 if (E/'data/jus-test-fixture.air').exists():config=re.sub(r'(?im)^(Air\s*=.*)$',lambda m:m[0]+', data/jus-test-fixture.air',config)
 for key,value in {'Modules':mod,'ScreenshotFolder':capture_from_engine+'/','WindowTitle':'JUS_'+slug,'MasterVolume':'0','GameWidth':'640','GameHeight':'360'}.items():
  config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 cfg='save/jus-'+suite+'-'+slug+'.ini';(E/cfg).write_text(config)
 args=['-config',cfg,'-loadmotif','-p1',row['engine']+'/'+row['definition'],'-p2','naruto','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest',str(row.get('speedtest',4))]
 cmd='$env:GOGC="50"; $env:GOMAXPROCS="2"; $g=Start-Process -FilePath '+q(E/'Ikemen_GO.exe')+' -WorkingDirectory '+q(E)+' -ArgumentList @('+','.join(map(q,args))+') -WindowStyle Hidden -RedirectStandardOutput '+q(out/'stdout.log')+' -RedirectStandardError '+q(out/'stderr.log')+' -PassThru; $null=$g.Handle; if (!$g.WaitForExit(210000)) { Stop-Process -Id $g.Id -Force -ErrorAction SilentlyContinue; exit 124 }; exit $g.ExitCode'
 subprocess.run(['powershell','-NoProfile','-Command',cmd],check=True,timeout=240)
 result=json.loads((out/'current.json').read_text())
 result['runtime_sha256']=runtime(row);result['harness_sha256']=fingerprint
 assert result['runtime_sha256']==before,'Production files changed while native game was running: '+slug
 assert fingerprint==harness(row,suite),'Test fixture changed while native game was running: '+slug
 result['screenshots']=[p.relative_to(R).as_posix() for p in capture.glob('*.png')]
 result['capture_directory']=capture.relative_to(R).as_posix()
 (out/'current.json').write_text(json.dumps(result,indent=2))
 print(slug,result['passed'],'passed',result['failed'],'failed',flush=True)
 return result

if __name__=='__main__':
 (E/'data/jus-test-fixture.cns').write_text(FIXTURE)
 data=json.loads((O/'manifest.json').read_text());selected=[r for r in data['fighters'] if len(sys.argv)==1 or r['slug'] in sys.argv[1:]]
 results=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  jobs={pool.submit(run,r):r['slug'] for r in selected}
  for job in concurrent.futures.as_completed(jobs):
   try:results.append(job.result())
   except Exception as error:errors.append(dict(slug=jobs[job],error=str(error)));print('FAILED',jobs[job],error,flush=True)
 combined=collect(data['fighters'],'native')
 (O/'native-mobility-validation.json').write_text(json.dumps(dict(status='Complete' if len(combined)==len(data['fighters']) and not errors else 'In progress',fighters=combined,errors=errors),indent=2))
 if errors or any(r['failed'] for r in results):raise SystemExit(1)
