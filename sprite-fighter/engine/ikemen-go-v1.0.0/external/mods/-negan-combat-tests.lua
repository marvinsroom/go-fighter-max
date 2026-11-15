-- Explicitly loaded through negan-combat-tests.ini; never auto-loaded in play.
local cases={{name="Standing light",pulse=1,state=200,exact=30},{name="Standing medium",pulse=2,state=210,exact=52},{name="Standing heavy",pulse=3,state=220,exact=82},{name="Crouch light",pulse=1,state=400,exact=26,down=true},{name="Crouch medium",pulse=2,state=410,exact=58,down=true},{name="Crouch heavy",pulse=3,state=420,exact=78,down=true},{name="Air 1",pulse=1,jump=true,state=600,damage=true},{name="Air 2",pulse=2,jump=true,state=610,damage=true},{name="Air 3",pulse=3,jump=true,state=620,damage=true},{name="Jump landing",jump=true},{name="Walk forward",walk=1,state=20,noDamage=true},{name="Walk backward",walk=-1,state=21,noDamage=true},{name="Forward throw",pulse=7,state=801,exact=105},{name="Back throw",pulse=7,back=true,state=811,exact=105},{name="Meet Lucille 0",pulse=8,state=1000,exact=72},{name="Meet Lucille 1",pulse=9,state=1010,exact=100},{name="Meet Lucille 2",pulse=10,state=1020,exact=125},{name="Whistle stance",pulse=4,state=1100,noDamage=true},{name="Take a Knee",pulse=4,walk=1,state=1110,exact=85},{name="Swing and a Miss",pulse=4,walk=-1,state=1120,noDamage=true},{name="Business Meeting",pulse=4,down=true,state=801,exact=105},{name="Back Off",pulse=11,state=1200,exact=90},{name="Whistle light branch",pulse=4,branch=1,state=1000,exact=72},{name="Whistle medium branch",pulse=4,branch=2,state=1110,exact=85},{name="Whistle heavy branch",pulse=4,branch=3,state=1200,exact=90},{name="Super confirmed",pulse=5,state=3010,exact=620,power=2000},{name="Super blocked",pulse=5,guard=true,notState=3010,noDamage=true,power=2000},{name="Super needs meter",pulse=5,meter=0,notState=3000,noDamage=true,power=0},{name="Super whiff",pulse=5,far=true,notState=3010,noDamage=true,power=2000},{name="Ultimate confirmed",pulse=6,state=3210,exact=950,power=1000},{name="Ultimate blocked",pulse=6,guard=true,notState=3210,noDamage=true,power=1000},{name="Ultimate needs meter",pulse=6,meter=1000,notState=3200,noDamage=true,power=1000},{name="Ultimate whiff",pulse=6,far=true,notState=3210,noDamage=true,power=1000},{name="Standing guard",defend=true,state=150,noDamage=true},{name="Crouch guard",defend=true,down=true,state=152,noDamage=true},{name="Thrown by Will",actor=1,pulse=7,state=801,exact=110},{name="Fresh Prince captures",actor=1,pulse=6,state=3210,exact=420},{name="Agent J captures",actor=1,agentWill=true,pulse=6,state=4510,exact=390},{name="Throw Agent J",agentWill=true,pulse=7,state=801,exact=105},{name="Ultimate captures Agent J",agentWill=true,pulse=6,state=3210,exact=950}}
local filter=os.getenv('NEGAN_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,c in ipairs(cases) do if c.name==filter then table.insert(selected,c) end end
 assert(#selected>0,'Unknown filter');cases=selected
end
local report={status='Running',method='Native engine with Will P1 and Negan P2',checks={}}
local index,tick=1,0
local seen,violations,minTarget,minPower,minActorY={}, {},1000,3000,0
local function save() jsonEncode(report,'../../characters/negan/runtime-validation.json') end
hook.add('loop','negan-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('NEGAN_TESTS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 local actor=c.actor or 2;local target=3-actor
 tick=tick+1
 if tick==1 then
  seen={};violations={};minTarget=1000;minPower=3000;minActorY=0
  for p=1,2 do player(p);for _,key in ipairs({'pulse','down','guard','backthrow','walk','robotSeen','robotMissing','robotLeak'}) do mapSet('test.'..key,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',c.agentWill and 2 or 1)
  player(2);mapSet('test.form',c.tyrone and 2 or 1)
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
 if c.branch and tick==36 then player(actor);mapSet('test.pulse',c.branch) end
 if c.enemyAt and tick==c.enemyAt then player(target);mapSet('test.pulse',1) end
 if c.probeAt and tick==c.probeAt then player(actor);mapSet('test.pulse',13) end
 if c.walk and tick==90 then player(actor);mapSet('test.walk',0) end
 if tick>=20 then
  player(actor);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());minActorY=math.min(minActorY,posY())
  player(target);minTarget=math.min(minTarget,life())
  player(2);local group=spriteVar('group');local form=_G['var'](45)
  local correct=form==1 and (group==51 or group==10) or form==0 and (group==0 or group==50)
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
  if c.form~=nil and _G['var'](45)~=c.form then ok=false end
  if c.life and actorLife~=c.life then ok=false end
  player(2);local robotSeen=map('test.robotSeen');local robotMissing=map('test.robotMissing');local robotLeak=map('test.robotLeak')
  if robotMissing~=0 or robotLeak~=0 then ok=false end

  player(target);local targetFinal=stateNo()
  if actorFinal~=0 and actorFinal~=10 and actorFinal~=130 and actorFinal~=131 and actorFinal~=140 then ok=false end
  if c.exact or c.damage then if targetFinal~=0 and targetFinal~=10 and targetFinal~=130 and targetFinal~=131 and targetFinal~=140 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,minPower=minPower,actorLife=actorLife,actorFinal=actorFinal,
       targetFinal=targetFinal,states=seen,outfitViolations=violations,robotSeen=robotSeen,robotMissing=robotMissing,robotLeak=robotLeak})
  report.current=index;save();print('NEGAN_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
