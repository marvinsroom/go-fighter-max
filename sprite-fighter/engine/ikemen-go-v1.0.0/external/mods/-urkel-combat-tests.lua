-- Explicitly loaded through urkel-combat-tests.ini; never auto-loaded in play.
local cases={
 {name='Stefan transformation',pulse=12,state=3900,form=1,power=2000,noDamage=true},
 {name='Stefan return',stefan=true,pulse=12,state=3901,form=0,power=3000,noDamage=true},
 {name='Stefan switch needs meter',pulse=12,meter=0,notState=3900,form=0,noDamage=true},
 {name='Stefan switch preserves health',pulse=12,startLife=600,life=600,state=3900,form=1,noDamage=true},
 {name='Stefan switch interrupted early',pulse=12,enemyAt=30,state=3900,form=0,noDamage=true},
 {name='Stefan switch interrupted late',pulse=12,enemyAt=52,state=3900,form=1,noDamage=true},
 {name='Stefan cooldown',pulse=12,probeAt=90,state=3900,notState=3901,form=1,noDamage=true},
 {name='Stefan palm',stefan=true,pulse=1,state=4100,exact=34},
 {name='Stefan straight',stefan=true,pulse=2,state=4110,exact=56},
 {name='Stefan heel',stefan=true,pulse=3,state=4120,exact=90},
 {name='Stefan low check',stefan=true,pulse=1,down=true,state=4140,exact=30},
 {name='Stefan sweep',stefan=true,pulse=2,down=true,state=4150,exact=60},
 {name='Stefan air',stefan=true,pulse=3,jump=true,state=4180,damage=true},
 {name='Stefan smooth step',stefan=true,pulse=4,state=4300,exact=60},
 {name='Stefan throw',stefan=true,pulse=7,state=801,exact=105},
 {name='Stefan super',stefan=true,pulse=5,state=4410,exact=245,power=2000},
 {name='Stefan ultimate',stefan=true,pulse=6,state=4510,exact=390,power=1000},
 {name='Stefan ultimate misses',stefan=true,pulse=6,far=true,notState=4510,noDamage=true,power=1000},
 {name='Stefan ultimate blocked',stefan=true,pulse=6,guard=true,notState=4510,noDamage=true,power=1000},
 {name='Stefan captured by Will ultimate',stefan=true,actor=1,pulse=6,state=3210,exact=420},
 {name='Urkel palm',pulse=1,state=200,exact=30},
 {name='Urkel elbow',pulse=2,state=210,exact=52},
 {name='Urkel heavy kick',pulse=3,state=220,exact=82},
 {name='Urkel low poke',pulse=1,down=true,state=400,exact=26},
 {name='Urkel sweep',pulse=2,down=true,state=410,exact=58},
 {name='Urkel anti-air',pulse=3,down=true,state=420,exact=78},
 {name='Urkel air palm',pulse=1,jump=true,state=600,damage=true},
 {name='Urkel air kick',pulse=2,jump=true,state=610,damage=true},
 {name='Urkel air accident',pulse=3,jump=true,state=620,damage=true},
 {name='Urkel jump landing',jump=true},
 {name='Urkel forward walk',walk=1,state=20,noDamage=true},
 {name='Urkel backward walk',walk=-1,state=21,noDamage=true},
 {name='Urkel forward throw',pulse=7,state=801,exact=105},
 {name='Urkel back throw',pulse=7,back=true,state=811,exact=105},
 {name='Urkel Cheese Please',pulse=8,state=1000,exact=48},
 {name='Urkel stumble skill',pulse=4,state=1100,exact=85},
 {name='Urkel stumble motion',pulse=9,state=1100,exact=85},
 {name='Urkel suspender snap',pulse=10,state=1200,exact=90},
 {name='Urkel safety retreat',pulse=11,state=1300,noDamage=true},
 {name='Urkel Gadget Malfunction',pulse=5,state=3000,exact=210,power=2000},
 {name='Urkel super requires meter',pulse=5,meter=0,notState=3000,noDamage=true,power=0},
 {name='Urkel invention ultimate',pulse=6,state=3210,exact=400,power=1000},
 {name='Urkel ultimate misses',pulse=6,far=true,notState=3210,noDamage=true,power=1000},
 {name='Urkel ultimate blocked',pulse=6,guard=true,notState=3210,noDamage=true,power=1000},
 {name='Urkel ultimate requires meter',pulse=6,meter=1000,notState=3200,noDamage=true,power=1000},
 {name='Urkel standing guard',defend=true,state=150,noDamage=true},
 {name='Urkel crouch guard',defend=true,down=true,state=152,noDamage=true},
 {name='Urkel thrown by Will',actor=1,pulse=7,state=801,exact=110},
 {name='Urkel captured by Fresh Prince ultimate',actor=1,pulse=6,state=3210,exact=420},
 {name='Urkel captured by Agent ultimate',actor=1,agentWill=true,pulse=6,state=4510,exact=390},
 {name='Agent captured by Urkel throw',agentWill=true,pulse=7,state=801,exact=105},
 {name='Agent captured by Urkel invention',agentWill=true,pulse=6,state=3210,exact=400},
}
local filter=os.getenv('URKEL_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,c in ipairs(cases) do if c.name==filter then table.insert(selected,c) end end
 assert(#selected>0,'Unknown filter');cases=selected
end
local report={status='Running',method='Native engine with Will P1 and Urkel P2',checks={}}
local index,tick=1,0
local seen,violations,minTarget,minPower,minActorY={}, {},1000,3000,0
local function save() jsonEncode(report,'../../characters/urkel/runtime-validation.json') end
hook.add('loop','urkel-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('URKEL_TESTS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
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
  if c.guard then mapSet('test.guard',1) end
  if c.far then changeState(9001) end
 elseif tick==20 then
  player(actor)
  if c.jump then changeState(40) elseif c.pulse then mapSet('test.pulse',c.pulse) end
  if c.back then mapSet('test.backthrow',1) end
  if c.defend then player(target);mapSet('test.pulse',1) end
 end
 if c.jump and c.pulse and tick==32 then player(actor);mapSet('test.pulse',c.pulse) end
 if c.enemyAt and tick==c.enemyAt then player(target);mapSet('test.pulse',1) end
 if c.probeAt and tick==c.probeAt then player(actor);mapSet('test.pulse',12) end
 if c.walk and tick==90 then player(actor);mapSet('test.walk',0) end
 if tick>=20 then
  player(actor);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());minActorY=math.min(minActorY,posY())
  player(target);minTarget=math.min(minTarget,life())
  player(2);local group=spriteVar('group');local form=_G['var'](30)
  local correct=form==1 and (group==30 or group==10) or form==0 and (group==0 or group==20)
  if stateNo()~=3900 and stateNo()~=3901 and not correct and #violations<12 then table.insert(violations,{player=2,tick=tick,group=group,state=stateNo()}) end
  player(1)
  if _G['var'](30)==1 and stateNo()~=3900 and stateNo()~=3901 and spriteVar('group')~=10 and #violations<12 then
   table.insert(violations,{player=1,tick=tick,group=spriteVar('group'),state=stateNo(),animation=anim()})
  end
 end
 if tick>=((c.pulse==6 or c.pulse==5) and 440 or 280) then
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
  if c.name=='Urkel invention ultimate' and robotSeen~=1 then ok=false end
  player(target);local targetFinal=stateNo()
  if c.exact or c.damage then if targetFinal~=0 and targetFinal~=10 and targetFinal~=130 and targetFinal~=131 and targetFinal~=140 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,minPower=minPower,actorLife=actorLife,actorFinal=actorFinal,
       targetFinal=targetFinal,states=seen,outfitViolations=violations,robotSeen=robotSeen,robotMissing=robotMissing,robotLeak=robotLeak})
  report.current=index;save();print('URKEL_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
