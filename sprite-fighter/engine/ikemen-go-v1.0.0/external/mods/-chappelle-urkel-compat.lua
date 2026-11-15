
local cases={{name='Stefan incoming throw',pulse=7,expected=110,form=1},{name='Stefan incoming ultimate',pulse=6,expected=420,form=1}}
local index,tick=1,0
local report={status='Running',checks={}}
local violations={}
hook.add('loop','chappelle-urkel-compat',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/chappelle/urkel-compat-validation.json');print('CHAPPELLE_COMPAT_COMPLETE urkel');os.exit() end
 tick=tick+1
 if tick==1 then
  violations={};for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','down','guard','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',1);player(2);mapSet('test.form',2)
 elseif tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 if tick>=24 then
  player(2);local group=spriteVar('group');local image=spriteVar('image')
  local ok=(group==30 or group==10)
  if not ok and time()>1 and #violations<12 then table.insert(violations,{tick=tick,group=group,image=image,state=stateNo()}) end
 end
 if tick>=(c.pulse==6 and 440 or 280) then
  player(2);local received=1000-life();local ok=received==c.expected and stateNo()==0 and #violations==0
  table.insert(report.checks,{name=c.name,passed=ok,received=received,violations=violations});print('CHAPPELLE_COMPAT '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
