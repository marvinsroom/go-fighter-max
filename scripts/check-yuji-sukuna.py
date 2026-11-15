"""Exercise the imported transformation command without capturing footage."""
from pathlib import Path
import re,subprocess,json
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';N=E/'chars/yuji'
fixture='''
[State -3, Test transformation input]
type=AssertCommand
triggerall=!ishelper
trigger1=map(expansion.transform)>0
name="y"
buffer.time=1
ignorehitpause=1
'''
text=(N/'IA.cns').read_text(encoding='cp1252')
text,count=re.subn(r'(?im)^(\[statedef\s+-3\])',lambda m:m[0]+'\n'+fixture,text,count=1);assert count==1
(N/'expansion-test-ai.cns').write_text(text,encoding='cp1252')
definition=(N/'yuji.def').read_text(encoding='cp1252')
definition,count=re.subn(r'(?im)^(st\d*\s*=\s*)IA.cns',r'\1expansion-test-ai.cns',definition);assert count==1
(N/'expansion-test.def').write_text(definition,encoding='cp1252')
lua='''local ticks=0
local report={status='Running',recording=false,scope='Original y command enters Sukuna, changes form bank, and returns to Yuji; no video or screenshots',states_seen={},forms_seen={}}
hook.add('loop','yuji-sukuna-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 if ticks==1 then setPower(3000) end
 mapSet('expansion.transform',ticks>=20 and ticks<=24 and 1 or 0)
 report.states_seen[tostring(stateNo())]=true
 report.forms_seen[tostring(var(11))]=true
 if var(11)==10000 then
  report.sukuna_seen=true
  report.sukuna_idle=report.sukuna_idle or stateNo()==0
 end
 if ticks>=200 and ticks<=204 then mapSet('expansion.transform',1) end
 if ticks>=300 then
  report.final_form=var(11)
  report.passed=report.sukuna_seen and report.sukuna_idle and report.states_seen['1300'] and report.states_seen['1310'] and var(11)==0
  report.status=report.passed and 'PASS' or 'FAIL'
  jsonEncode(report,'../../mugen-expansion/validation/yuji-sukuna.json')
  os.exit(report.passed and 0 or 1)
 end
end)
'''
mod='external/mods/-expansion-yuji-sukuna.lua';(E/mod).write_text(lua)
config=(E/'save/config.ini').read_text()
for key,value in {'Modules':mod,'MasterVolume':'0'}.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
(E/'save/expansion-yuji-sukuna.ini').write_text(config)
def quote(v):return "'"+str(v).replace("'","''")+"'"
args=['-config','save/expansion-yuji-sukuna.ini','-loadmotif','-p1','yuji/expansion-test.def','-p2','baam','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
logs=R/'sprite-fighter/mugen-expansion/validation'
cmd='$p=Start-Process -FilePath '+quote(E/'Ikemen_GO.exe')+' -WorkingDirectory '+quote(E)+' -ArgumentList @('+','.join(map(quote,args))+') -WindowStyle Hidden -RedirectStandardOutput '+quote(logs/'yuji-sukuna-stdout.log')+' -RedirectStandardError '+quote(logs/'yuji-sukuna-stderr.log')+' -PassThru; $null=$p.Handle; if(!$p.WaitForExit(45000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode'
result=subprocess.run(['powershell','-NoProfile','-Command',cmd],timeout=55)
report=logs/'yuji-sukuna.json'
if report.exists():print(report.read_text())
assert result.returncode==0,'See yuji-sukuna-stderr.log'
