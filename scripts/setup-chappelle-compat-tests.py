"""Regression checks for existing transformed victims of Will's capture moves."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
for slug in ['urkel','jinwoo']:
    cases="{{name='Stefan incoming throw',pulse=7,expected=110,form=1},{name='Stefan incoming ultimate',pulse=6,expected=420,form=1}}" if slug=='urkel' else '{'+','.join("{name='Shadow "+str(i)+" incoming throw',pulse=7,expected=110,form="+str(i)+'}' for i in range(1,5))+'}'
    code='''
local cases=CASES
local index,tick=1,0
local report={status='Running',checks={}}
local violations={}
hook.add('loop','chappelle-SLUG-compat',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/chappelle/SLUG-compat-validation.json');print('CHAPPELLE_COMPAT_COMPLETE SLUG');os.exit() end
 tick=tick+1
 if tick==1 then
  violations={};for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','down','guard','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',1);player(2);SET_FORM
 elseif tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 if tick>=24 then
  player(2);local group=spriteVar('group');local image=spriteVar('image')
  local ok=GROUP_OK
  if not ok and time()>1 and #violations<12 then table.insert(violations,{tick=tick,group=group,image=image,state=stateNo()}) end
 end
 if tick>=(c.pulse==6 and 440 or 280) then
  player(2);local received=1000-life();local ok=received==c.expected and stateNo()==0 and #violations==0
  table.insert(report.checks,{name=c.name,passed=ok,received=received,violations=violations});print('CHAPPELLE_COMPAT '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
'''.replace('CASES',cases).replace('SLUG',slug)
    code=code.replace('SET_FORM',"mapSet('test.form',2)" if slug=='urkel' else "mapSet('test.shadowform',c.form);changeState(9010)")
    code=code.replace('GROUP_OK','(group==30 or group==10)' if slug=='urkel' else '(group==51 and image>=44+(c.form-1)*8 and image<=47+(c.form-1)*8)')
    (E/'external/mods'/('-chappelle-'+slug+'-compat.lua')).write_text(code)
    config=(E/'save'/(slug+'-combat-tests.ini')).read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-chappelle-'+slug+'-compat.lua',config,flags=re.M)
    (E/'save'/('chappelle-'+slug+'-compat.ini')).write_text(config)
print('CHAPPELLE_COMPAT_READY 6 checks')
