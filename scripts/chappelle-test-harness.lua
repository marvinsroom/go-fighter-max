-- Explicitly loaded through CHAR_SLUG-combat-tests.ini; never auto-loaded in play.
local cases=CASE_DATA
local filter=os.getenv('CHAR_UPPER_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,c in ipairs(cases) do if c.name==filter then table.insert(selected,c) end end
 assert(#selected>0,'Unknown filter');cases=selected
end
local report={status='Running',method='Native engine with Will P1 and CHAR_NAME P2',checks={}}
local index,tick=1,0
local seen,violations,minTarget,minPower,minActorY={}, {},1000,3000,0
local function save() jsonEncode(report,'../../characters/CHAR_SLUG/runtime-validation.json') end
hook.add('loop','CHAR_SLUG-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('CHAR_UPPER_TESTS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 local actor=c.actor or 2;local target=3-actor
 tick=tick+1
 if tick==1 then
  seen={};violations={};minTarget=1000;minPower=3000;minActorY=0
  for p=1,2 do player(p);for _,key in ipairs({'pulse','down','guard','backthrow','walk','robotSeen','robotMissing','robotLeak'}) do mapSet('test.'..key,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',c.agentWill and 2 or 1)
  player(2);mapSet('test.form',c.stefan and 2 or 1)
  player(actor);setPower(c.meter or 3000)
  if c.startLife then setLife(c.startLife) end
  if c.down then mapSet('test.down',1) end
  if c.walk then mapSet('test.walk',c.walk) end
  if c.defend then mapSet('test.guard',1) end
  player(target)
  if c.guard then mapSet('test.guard',1);if c.targetDown then mapSet('test.down',1) end end
  if c.far then changeState(9001);player(actor);changeState(9001) end
 elseif tick==20 then
  player(actor)
  if c.jump then changeState(40) elseif c.pulse then mapSet('test.pulse',c.pulse) end
  if c.back then mapSet('test.backthrow',1) end
  if c.defend then player(target);mapSet('test.pulse',1) end
 end
 if c.jump and c.pulse and tick==32 then player(actor);mapSet('test.pulse',c.pulse) end
 if c.branch and tick==43 then player(actor);mapSet('test.pulse',c.branch) end
 if c.enemyAt and tick==c.enemyAt then player(target);mapSet('test.pulse',1) end
 if c.probeAt and tick==c.probeAt then player(actor);mapSet('test.pulse',12) end
 if c.walk and tick==90 then player(actor);mapSet('test.walk',0) end
 if tick>=20 then
  player(actor);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());minActorY=math.min(minActorY,posY())
  player(target);minTarget=math.min(minTarget,life())
  player(2);local group=spriteVar('group');local form=_G['var'](30)
  local correct=group==0 or group==50
  if stateNo()~=3900 and stateNo()~=3901 and not correct and #violations<12 then table.insert(violations,{player=2,tick=tick,group=group,state=stateNo()}) end
  player(1)
  if _G['var'](30)==1 and stateNo()~=3900 and stateNo()~=3901 and spriteVar('group')~=10 and #violations<12 then
   table.insert(violations,{player=1,tick=tick,group=spriteVar('group'),state=stateNo(),animation=anim()})
  end
 end
 if tick>=(c.pulse==6 and 600 or c.pulse==5 and 420 or 280) then
  player(actor);local actorLife=life();local actorFinal=stateNo();local damage=1000-minTarget;local ok=#violations==0
  if c.state and not seen[tostring(c.state)] then ok=false end
  if c.notState and seen[tostring(c.notState)] then ok=false end
  if c.exact and damage~=c.exact then ok=false end
  if c.damage and damage<20 then ok=false end
  if c.noDamage and damage>6 then ok=false end
  if c.power and minPower~=c.power then ok=false end
  if c.jump and minActorY>=-30 then ok=false end
  if c.defend and actorLife<994 then ok=false end
  if c.form and _G['var'](30)~=c.form then ok=false end
  if c.life and actorLife~=c.life then ok=false end
  player(2);local robotSeen=map('test.robotSeen');local robotMissing=map('test.robotMissing');local robotLeak=map('test.robotLeak')
  if robotMissing~=0 or robotLeak~=0 then ok=false end

  player(target);local targetFinal=stateNo()
  if actorFinal~=0 and actorFinal~=10 and actorFinal~=130 and actorFinal~=131 and actorFinal~=140 then ok=false end
  if c.exact or c.damage then if targetFinal~=0 and targetFinal~=10 and targetFinal~=130 and targetFinal~=131 and targetFinal~=140 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,minPower=minPower,actorLife=actorLife,actorFinal=actorFinal,
       targetFinal=targetFinal,states=seen,outfitViolations=violations,robotSeen=robotSeen,robotMissing=robotMissing,robotLeak=robotLeak})
  report.current=index;save();print('CHAR_UPPER_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
