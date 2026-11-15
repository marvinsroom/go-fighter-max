"""Observe actual forward/back walk cadence and pace; never capture images."""
from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/walk-fix-v11';(O/'validation').mkdir(exist_ok=True)
fixture='[Statedef -4]\n'
for value,flag,command in [(1,'F','holdfwd'),(-1,'B','holdback')]:
 fixture+=f'''[State -4, Walk test input {flag}]
type=AssertInput
triggerall=!ishelper
trigger1=map(walktest.direction)={value}
flag={flag}
[State -4, Walk test command {flag}]
type=AssertCommand
triggerall=!ishelper
trigger1=map(walktest.direction)={value}
name="{command}"
buffer.time=1
'''
(E/'data/walk-v11-test.cns').write_text(fixture)
lua='''local ticks=0
local report={status='Running',recording=false,forward_keys={},backward_keys={},samples={}}
local function worldX() return posX()+cameraPosX() end
local function keysCount(keys) local n=0;for k,v in pairs(keys) do n=n+1 end;return n end
hook.add('loop','walk-cadence-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 mapSet('walktest.direction',ticks>=10 and ticks<=99 and 1 or (ticks>=120 and ticks<=229 and -1 or 0))
 if ticks==30 then report.forward_start=worldX() end
 if ticks==90 then report.forward_speed=(worldX()-report.forward_start)/60 end
 if ticks==150 then report.backward_start=worldX() end
 if ticks==210 then report.backward_speed=(worldX()-report.backward_start)/60 end
 if ticks>=30 and ticks<=90 then report.forward_keys[tostring(animElemNo(0))]=true end
 if ticks>=150 and ticks<=210 then report.backward_keys[tostring(animElemNo(0))]=true end
 if ticks%10==0 then table.insert(report.samples,{tick=ticks,state=stateNo(),animation=anim(),element=animElemNo(0),velocity=velX()}) end
 if ticks>=240 then
  report.forward_elements=keysCount(report.forward_keys);report.backward_elements=keysCount(report.backward_keys)
  report.passed=math.abs(report.forward_speed-.95)<.03 and math.abs(report.backward_speed+.72)<.03 and report.forward_elements==8 and report.backward_elements==8
  report.status=report.passed and 'PASS' or 'FAIL'
  jsonEncode(report,'../../walk-fix-v11/validation/SLUG.json');os.exit(report.passed and 0 or 1)
 end
end)
'''
def quote(v):return "'"+str(v).replace("'","''")+"'"
for slug in sys.argv[1:] or ['lloyd','baam','jin_mori']:
 mod='external/mods/-walk-v11-'+slug+'.lua';(E/mod).write_text(lua.replace('SLUG',slug));config=(E/'save/config.ini').read_text()
 for key,value in {'Modules':mod,'MasterVolume':'0'}.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 config=re.sub(r'(?im)^(States\s*=.*)$',r'\1, data/walk-v11-test.cns',config);ini='save/walk-v11-'+slug+'.ini';(E/ini).write_text(config)
 args=['-config',ini,'-loadmotif','-p1',slug,'-p2','baam','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest','4'];out=O/'validation'
 cmd='$p=Start-Process -FilePath '+quote(E/'Ikemen_GO.exe')+' -WorkingDirectory '+quote(E)+' -ArgumentList @('+','.join(map(quote,args))+') -WindowStyle Hidden -RedirectStandardOutput '+quote(out/(slug+'-stdout.log'))+' -RedirectStandardError '+quote(out/(slug+'-stderr.log'))+' -PassThru; $null=$p.Handle; if(!$p.WaitForExit(45000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode'
 run=subprocess.run(['powershell','-NoProfile','-Command',cmd],timeout=55);path=out/(slug+'.json')
 report=None
 if path.exists():
  report=json.loads(path.read_text());print(slug,report['status'],'forward',round(report['forward_speed'],4),'backward',round(report['backward_speed'],4),'elements',report['forward_elements'],report['backward_elements'],flush=True)
 # Windows can report Ikemen's forced Lua os.exit as nonzero after the report is
 # flushed. The machine-readable assertions are the authoritative result.
 assert report and report.get('passed'),slug+' native check failed; see stderr'
