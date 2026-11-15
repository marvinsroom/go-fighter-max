-- Explicitly loaded through tyrone-combat-tests.ini; never auto-loaded in play.
local cases={{name="Tyrone Biggums / Standing light",pulse=1,state=200,exact=30,pairAlt=false},{name="Tyrone Biggums / Standing medium",pulse=2,state=210,exact=52,pairAlt=false},{name="Tyrone Biggums / Standing heavy",pulse=3,state=220,exact=82,pairAlt=false},{name="Tyrone Biggums / Crouch light",pulse=1,state=400,exact=26,down=true,pairAlt=false},{name="Tyrone Biggums / Crouch medium",pulse=2,state=410,exact=58,down=true,pairAlt=false},{name="Tyrone Biggums / Crouch heavy",pulse=3,state=420,exact=78,down=true,pairAlt=false},{name="Tyrone Biggums / Air 1",pulse=1,jump=true,state=600,damage=true,pairAlt=false},{name="Tyrone Biggums / Air 2",pulse=2,jump=true,state=610,damage=true,pairAlt=false},{name="Tyrone Biggums / Air 3",pulse=3,jump=true,state=620,damage=true,pairAlt=false},{name="Tyrone Biggums / Jump landing",jump=true,pairAlt=false},{name="Tyrone Biggums / Walk forward",walk=1,state=20,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Walk backward",walk=-1,state=21,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Forward throw",pulse=7,state=801,exact=105,pairAlt=false},{name="Tyrone Biggums / Back throw",pulse=7,back=true,state=811,exact=105,pairAlt=false},{name="Tyrone Biggums / Tyrone light",pulse=1,state=200,exact=30,pairAlt=false},{name="Tyrone Biggums / Tyrone low",pulse=1,down=true,state=400,exact=26,pairAlt=false},{name="Tyrone Biggums / Tyrone heavy",pulse=3,state=220,exact=82,pairAlt=false},{name="Tyrone Biggums / Tyrone air",pulse=3,jump=true,state=620,damage=true,pairAlt=false},{name="Tyrone Biggums / Tyrone walk",walk=1,state=20,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Tyrone throw",pulse=7,state=801,exact=105,pairAlt=false},{name="Tyrone Biggums / Tyrone incoming throw",actor=1,pulse=7,state=801,exact=110,pairAlt=false},{name="Tyrone Biggums / Tyrone incoming cinematic",actor=1,pulse=6,state=3210,exact=420,pairAlt=false},{name="Tyrone Biggums / Quick Rush",pulse=4,state=4100,exact=75,pairAlt=false},{name="Tyrone Biggums / Panic Lunge",pulse=4,walk=1,state=4110,exact=90,pairAlt=false},{name="Tyrone Biggums / Backpedal",pulse=4,walk=-1,state=4120,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Floor Scramble",pulse=4,down=true,state=4130,exact=65,pairAlt=false},{name="Tyrone Biggums / Rising Flail",pulse=11,state=4200,exact=90,pairAlt=false},{name="Tyrone Biggums / Tyrone super",pulse=5,state=4410,exact=620,power=2000,pairAlt=false},{name="Tyrone Biggums / Tyrone super blocked",pulse=5,guard=true,notState=4410,noDamage=true,power=2000,pairAlt=false},{name="Tyrone Biggums / Tyrone super needs meter",pulse=5,meter=0,notState=4400,noDamage=true,power=0,pairAlt=false},{name="Tyrone Biggums / Tyrone ultimate",pulse=6,state=4510,exact=950,power=1000,pairAlt=false},{name="Tyrone Biggums / Tyrone ultimate blocked",pulse=6,guard=true,notState=4510,noDamage=true,power=1000,pairAlt=false},{name="Tyrone Biggums / Tyrone ultimate needs meter",pulse=6,meter=1000,notState=4500,noDamage=true,power=1000,pairAlt=false},{name="Tyrone Biggums / Tyrone normal hit reaction",enemyAt=30,state=5000,noDamage=true,life=966,pairAlt=false},{name="Tyrone Biggums / Tyrone captured by Agent J",actor=1,agentWill=true,pulse=6,state=4510,exact=390,pairAlt=false},{name="Tyrone Biggums / Super confirmed",pulse=5,state=4410,exact=620,power=2000,pairAlt=false},{name="Tyrone Biggums / Super blocked",pulse=5,guard=true,notState=4410,noDamage=true,power=2000,pairAlt=false},{name="Tyrone Biggums / Super needs meter",pulse=5,meter=0,notState=4400,noDamage=true,power=0,pairAlt=false},{name="Tyrone Biggums / Super whiff",pulse=5,far=true,notState=4410,noDamage=true,power=2000,pairAlt=false},{name="Tyrone Biggums / Ultimate confirmed",pulse=6,state=4510,exact=950,power=1000,pairAlt=false},{name="Tyrone Biggums / Ultimate blocked",pulse=6,guard=true,notState=4510,noDamage=true,power=1000,pairAlt=false},{name="Tyrone Biggums / Ultimate needs meter",pulse=6,meter=1000,notState=4500,noDamage=true,power=1000,pairAlt=false},{name="Tyrone Biggums / Ultimate whiff",pulse=6,far=true,notState=4510,noDamage=true,power=1000,pairAlt=false},{name="Tyrone Biggums / Standing guard",defend=true,state=150,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Crouch guard",defend=true,down=true,state=152,noDamage=true,pairAlt=false},{name="Tyrone Biggums / Thrown by Will",actor=1,pulse=7,state=801,exact=110,pairAlt=false},{name="Tyrone Biggums / Fresh Prince captures",actor=1,pulse=6,state=3210,exact=420,pairAlt=false},{name="Tyrone Biggums / Agent J captures",actor=1,agentWill=true,pulse=6,state=4510,exact=390,pairAlt=false},{name="Tyrone Biggums / Throw Agent J",agentWill=true,pulse=7,state=801,exact=105,pairAlt=false},{name="Tyrone Biggums / Ultimate captures Agent J",agentWill=true,pulse=6,state=4510,exact=950,pairAlt=false},{name="Negan / Standing light",pulse=1,state=10200,exact=30,pairAlt=true},{name="Negan / Standing medium",pulse=2,state=10210,exact=52,pairAlt=true},{name="Negan / Standing heavy",pulse=3,state=10220,exact=82,pairAlt=true},{name="Negan / Crouch light",pulse=1,state=10400,exact=26,down=true,pairAlt=true},{name="Negan / Crouch medium",pulse=2,state=10410,exact=58,down=true,pairAlt=true},{name="Negan / Crouch heavy",pulse=3,state=10420,exact=78,down=true,pairAlt=true},{name="Negan / Air 1",pulse=1,jump=true,state=10600,damage=true,pairAlt=true},{name="Negan / Air 2",pulse=2,jump=true,state=10610,damage=true,pairAlt=true},{name="Negan / Air 3",pulse=3,jump=true,state=10620,damage=true,pairAlt=true},{name="Negan / Jump landing",jump=true,pairAlt=true},{name="Negan / Walk forward",walk=1,state=10020,noDamage=true,pairAlt=true},{name="Negan / Walk backward",walk=-1,state=10021,noDamage=true,pairAlt=true},{name="Negan / Forward throw",pulse=7,state=10801,exact=105,pairAlt=true},{name="Negan / Back throw",pulse=7,back=true,state=10811,exact=105,pairAlt=true},{name="Negan / Meet Lucille 0",pulse=8,state=11000,exact=72,pairAlt=true},{name="Negan / Meet Lucille 1",pulse=9,state=11010,exact=100,pairAlt=true},{name="Negan / Meet Lucille 2",pulse=10,state=11020,exact=125,pairAlt=true},{name="Negan / Whistle stance",pulse=4,state=11100,noDamage=true,pairAlt=true},{name="Negan / Take a Knee",pulse=4,walk=1,state=11110,exact=85,pairAlt=true},{name="Negan / Swing and a Miss",pulse=4,walk=-1,state=11120,noDamage=true,pairAlt=true},{name="Negan / Business Meeting",pulse=4,down=true,state=10801,exact=105,pairAlt=true},{name="Negan / Back Off",pulse=11,state=11200,exact=90,pairAlt=true},{name="Negan / Whistle light branch",pulse=4,branch=1,state=11000,exact=72,pairAlt=true},{name="Negan / Whistle medium branch",pulse=4,branch=2,state=11110,exact=85,pairAlt=true},{name="Negan / Whistle heavy branch",pulse=4,branch=3,state=11200,exact=90,pairAlt=true},{name="Negan / Super confirmed",pulse=5,state=13010,exact=620,power=2000,pairAlt=true},{name="Negan / Super blocked",pulse=5,guard=true,notState=13010,noDamage=true,power=2000,pairAlt=true},{name="Negan / Super needs meter",pulse=5,meter=0,notState=13000,noDamage=true,power=0,pairAlt=true},{name="Negan / Super whiff",pulse=5,far=true,notState=13010,noDamage=true,power=2000,pairAlt=true},{name="Negan / Ultimate confirmed",pulse=6,state=13210,exact=950,power=1000,pairAlt=true},{name="Negan / Ultimate blocked",pulse=6,guard=true,notState=13210,noDamage=true,power=1000,pairAlt=true},{name="Negan / Ultimate needs meter",pulse=6,meter=1000,notState=13200,noDamage=true,power=1000,pairAlt=true},{name="Negan / Ultimate whiff",pulse=6,far=true,notState=13210,noDamage=true,power=1000,pairAlt=true},{name="Negan / Standing guard",defend=true,state=150,noDamage=true,pairAlt=true},{name="Negan / Crouch guard",defend=true,down=true,state=152,noDamage=true,pairAlt=true},{name="Negan / Thrown by Will",actor=1,pulse=7,state=801,exact=110,pairAlt=true},{name="Negan / Fresh Prince captures",actor=1,pulse=6,state=3210,exact=420,pairAlt=true},{name="Negan / Agent J captures",actor=1,agentWill=true,pulse=6,state=4510,exact=390,pairAlt=true},{name="Negan / Throw Agent J",agentWill=true,pulse=7,state=10801,exact=105,pairAlt=true},{name="Negan / Ultimate captures Agent J",agentWill=true,pulse=6,state=13210,exact=950,pairAlt=true},{name="Actual toggle activation",pairAlt=false,pulse=13,state=3900,form=1,noDamage=true,power=3000},{name="Toggle preserves health False",pairAlt=false,pulse=13,startLife=600,life=600,state=3900,form=1,noDamage=true},{name="Actual toggle return",pairAlt=true,pulse=13,state=3900,form=0,noDamage=true,power=3000},{name="Toggle preserves health True",pairAlt=true,pulse=13,startLife=600,life=600,state=3900,form=0,noDamage=true},{name="Transformation free at zero meter",pulse=13,meter=0,state=3900,form=1,noDamage=true,power=0},{name="Transformation cooldown",pulse=13,probeAt=90,state=3900,form=1,noDamage=true},{name="Alternate incoming normal",pairAlt=true,enemyAt=30,state=5000,noDamage=true,life=966},{name="Tyrone Biggums / Signature ground hit",pairAlt=false,pulse=18,state=1500,exact=55},{name="Tyrone Biggums / Signature air hit",pairAlt=false,pulse=4,jump=true,state=1510,exact=90},{name="Tyrone Biggums / Signature ground blocked",pairAlt=false,pulse=18,state=1500,noDamage=true,guard=true,far=false,targetDown=false},{name="Tyrone Biggums / Signature air blocked",pairAlt=false,pulse=4,jump=true,state=1510,noDamage=true,guard=true,far=false},{name="Tyrone Biggums / Signature ground whiff",pairAlt=false,pulse=18,state=1500,noDamage=true,guard=false,far=true,targetDown=false},{name="Tyrone Biggums / Signature air whiff",pairAlt=false,pulse=4,jump=true,state=1510,noDamage=true,guard=false,far=true},{name="Negan / Signature ground hit",pairAlt=true,pulse=18,state=11500,exact=90},{name="Negan / Signature air hit",pairAlt=true,pulse=4,jump=true,state=11510,exact=130},{name="Negan / Signature ground blocked",pairAlt=true,pulse=18,state=11500,noDamage=true,guard=true,far=false,targetDown=false},{name="Negan / Signature air blocked",pairAlt=true,pulse=4,jump=true,state=11510,noDamage=true,guard=true,far=false},{name="Negan / Signature ground whiff",pairAlt=true,pulse=18,state=11500,noDamage=true,guard=false,far=true,targetDown=false},{name="Negan / Signature air whiff",pairAlt=true,pulse=4,jump=true,state=11510,noDamage=true,guard=false,far=true},{name="Negan / Full charge signature",pairAlt=true,pulse=18,state=11501,exact=145,holdSignature=true}}
local filter=os.getenv('TYRONE_PAIR_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,c in ipairs(cases) do if c.name==filter then table.insert(selected,c) end end
 assert(#selected>0,'Unknown filter');cases=selected
end
local report={status='Running',method='Native engine with Will P1 and Tyrone pair P2',checks={}}
local index,tick=1,0
local seen,violations,minTarget,minPower,minActorY={}, {},1000,3000,0
local function save() jsonEncode(report,'../../characters/tyrone/paired-runtime-validation.json') end
hook.add('loop','tyrone-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('TYRONE_PAIR_TESTS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 local actor=c.actor or 2;local target=3-actor
 tick=tick+1
 if tick==1 then
  seen={};violations={};minTarget=1000;minPower=3000;minActorY=0
  for p=1,2 do player(p);for _,key in ipairs({'pulse','down','guard','backthrow','walk','robotSeen','robotMissing','robotLeak','charge','bounced'}) do mapSet('test.'..key,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',c.agentWill and 2 or 1)
  player(2);mapSet('test.form',c.pairAlt and 2 or 1)
  player(actor);mapSet('test.charge',c.holdSignature and 1 or 0);setPower(c.meter or 3000)
  if c.startLife then setLife(c.startLife) end
  if c.down then mapSet('test.down',1) end
  if c.walk then mapSet('test.walk',c.walk) end
  if c.defend then mapSet('test.guard',1) end
  player(target)
  if c.guard then mapSet('test.guard',1);if c.targetDown then mapSet('test.down',1) end end
  if c.far then changeState(9001);player(actor);changeState(9001) end
 elseif tick==20 then
  player(actor)
  if c.jump then mapSet('test.pulse',17) elseif c.pulse then mapSet('test.pulse',c.pulse) end
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
  if c.requireState and not seen[tostring(c.requireState)] then ok=false end
  if c.needBounce and map('test.bounced')~=1 then ok=false end
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
  if actorFinal~=0 and actorFinal~=10 and actorFinal~=10000 and actorFinal~=10010 and actorFinal~=130 and actorFinal~=131 and actorFinal~=140 then ok=false end
  if c.exact or c.damage then if targetFinal~=0 and targetFinal~=10 and targetFinal~=10000 and targetFinal~=10010 and targetFinal~=130 and targetFinal~=131 and targetFinal~=140 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,minPower=minPower,actorLife=actorLife,actorFinal=actorFinal,
       targetFinal=targetFinal,states=seen,outfitViolations=violations,robotSeen=robotSeen,robotMissing=robotMissing,robotLeak=robotLeak})
  report.current=index;save();print('TYRONE_PAIR_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
