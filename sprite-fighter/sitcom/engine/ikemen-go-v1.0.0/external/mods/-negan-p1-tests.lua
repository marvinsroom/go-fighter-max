
local cases={{name='P1 super',pulse=5,damage=620,length=420},{name='P1 ultimate',pulse=6,damage=950,length=600}}
local index,tick=1,0
local report={checks={},status='Running'}
hook.add('loop','negan-player-one-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/negan/player-one-validation.json');print('CHAPPELLE_P1_COMPLETE negan');os.exit() end
 tick=tick+1
 if tick==1 then for p=1,2 do player(p);mapSet('test.form',0);changeState(9000) end end
 if tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(2);mapSet('test.form',1)
  if c.tyrone then player(1);mapSet('test.form',2) end
 end
 if tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 player(1)
 if (stateNo()==3010 or stateNo()==4410) and (time()==175 or time()==195) or (stateNo()==3210 or stateNo()==4510) and (time()==335 or time()==355) then screenshot() end
 if tick>=c.length then
  local actorFinal=stateNo();player(2);local damage=1000-life();local targetFinal=stateNo()
  local ok=damage==c.damage and actorFinal==0 and targetFinal==0
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,actorFinal=actorFinal,targetFinal=targetFinal})
  print('CHAPPELLE_P1 '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
