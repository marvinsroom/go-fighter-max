"""Check captures between the new roster fighters, including Tyrone victims."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
for slug in ['prince','negan','rick']:
    victim='negan' if slug=='rick' else 'rick'
    cases="{{name='Cross super',pulse=5,expected=620,length=420},{name='Cross ultimate',pulse=6,expected=950,length=600}"
    if slug=='prince':cases+=",{name='Counter Tyrone',pulse=4,counter=true,expected=100,length=280}"
    cases+='}'
    code='''
local cases=CASES
local index,tick=1,0
local report={status='Running',checks={}}
local violations={}
hook.add('loop','SLUG-cross',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/SLUG/cross-validation.json');print('CHAPPELLE_CROSS_COMPLETE SLUG');os.exit() end
 tick=tick+1
 if tick==1 then
  violations={};for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','form','guard','down','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  if TYRONE then player(1);mapSet('test.form',2) end
  if c.counter then player(2);mapSet('test.walk',-1) end
 elseif tick==20 then player(2);mapSet('test.pulse',c.pulse) end
 if c.counter and tick==30 then player(1);mapSet('test.pulse',1) end
 if tick==90 then player(2);mapSet('test.walk',0) end
 if tick>=24 then
  player(1);local group=spriteVar('group')
  if group~=EXPECTED_GROUP and #violations<12 then table.insert(violations,{tick=tick,state=stateNo(),group=group}) end
 end
 if tick>=c.length then
  player(2);local actorFinal=stateNo();player(1);local damage=1000-life();local targetFinal=stateNo()
  local ok=damage==c.expected and actorFinal==0 and targetFinal==0 and #violations==0
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,violations=violations});print('CHAPPELLE_CROSS '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
'''.replace('CASES',cases).replace('SLUG',slug).replace('TYRONE','false' if slug=='rick' else 'true').replace('EXPECTED_GROUP','50' if slug=='rick' else '51')
    (E/'external/mods'/('-'+slug+'-cross-tests.lua')).write_text(code)
    config=(E/'save'/(slug+'-combat-tests.ini')).read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-cross-tests.lua',config,flags=re.M)
    (E/'save'/(slug+'-cross-tests.ini')).write_text(config)
    print('CHAPPELLE_CROSS_READY',slug,'victim',victim)
