
local cases={{name='Cross super',pulse=5,expected=620,length=420},{name='Cross ultimate',pulse=6,expected=950,length=600}}
local index,tick=1,0
local report={status='Running',checks={}}
local violations={}
hook.add('loop','rick-cross',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/rick/cross-validation.json');print('CHAPPELLE_CROSS_COMPLETE rick');os.exit() end
 tick=tick+1
 if tick==1 then
  violations={};for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','form','guard','down','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  if false then player(1);mapSet('test.form',2) end
  if c.counter then player(2);mapSet('test.walk',-1) end
 elseif tick==20 then player(2);mapSet('test.pulse',c.pulse) end
 if c.counter and tick==30 then player(1);mapSet('test.pulse',1) end
 if tick==90 then player(2);mapSet('test.walk',0) end
 if tick>=24 then
  player(1);local group=spriteVar('group')
  if group~=50 and #violations<12 then table.insert(violations,{tick=tick,state=stateNo(),group=group}) end
 end
 if tick>=c.length then
  player(2);local actorFinal=stateNo();player(1);local damage=1000-life();local targetFinal=stateNo()
  local ok=damage==c.expected and actorFinal==0 and targetFinal==0 and #violations==0
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,violations=violations});print('CHAPPELLE_CROSS '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
