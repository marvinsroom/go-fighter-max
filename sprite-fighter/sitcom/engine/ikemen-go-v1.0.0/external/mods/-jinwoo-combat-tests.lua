if os.getenv('JINWOO_TRANSFORM_TESTS')=='1' then dofile('../../../scripts/jinwoo-transform-tests.lua');return end
-- Explicitly loaded through jinwoo-combat-tests.ini; never auto-loaded in play.
local cases={
 {name='Dagger check',pulse=1,state=200,exact=30},
 {name='Twin cut',pulse=2,state=210,exact=52},
 {name='Monarch heel',pulse=3,state=220,exact=82},
 {name='Low dagger',pulse=1,down=true,state=400,exact=26},
 {name='Low sweep',pulse=2,down=true,state=410,exact=58},
 {name='Rising dagger',pulse=3,down=true,state=420,exact=78},
 {name='Air cut',pulse=1,jump=true,state=600,damage=true},
 {name='Air heel',pulse=2,jump=true,state=610,damage=true},
 {name='Diving cut',pulse=3,jump=true,state=620,damage=true},
 {name='Jump landing',jump=true},
 {name='Walk forward',walk=1,state=20,noDamage=true},
 {name='Walk backward',walk=-1,state=21,noDamage=true},
 {name='Forward throw',pulse=7,state=801,exact=105},
 {name='Back throw',pulse=7,back=true,state=811,exact=105},
 {name='Dagger throw',pulse=8,state=1000,exact=48},
 {name='Shadow Knight',pulse=4,state=1100,exact=100,power=2750},
 {name='Knight motion',pulse=9,state=1110,exact=110,power=2750},
 {name='Knight needs meter',pulse=4,meter=0,notState=1100,noDamage=true,power=0},
 {name='Knight cooldown',pulse=4,probeKnight=true,state=1100,exact=100,power=2750},
 {name='Fatal lunge',pulse=10,state=1200,exact=90},
 {name='Shadow retreat',pulse=11,state=1400,noDamage=true},
 {name='Shadow step',pulse=12,state=1300,noDamage=true},
 {name='Dagger Tempest',pulse=5,state=3010,exact=620,power=2000},
 {name='Tempest long-range catch',pulse=5,far=true,state=3010,exact=620,power=2000},
 {name='Tempest blocked',pulse=5,guard=true,notState=3010,noDamage=true,power=2000},
 {name='Tempest needs meter',pulse=5,meter=0,notState=3000,noDamage=true,power=0},
 {name='Arise army ultimate',pulse=6,state=3210,exact=950,power=1000},
 {name='Arise full-screen catch',pulse=6,far=true,state=3210,exact=950,power=1000},
 {name='Arise blocked',pulse=6,guard=true,notState=3210,noDamage=true,power=1000},
 {name='Arise needs meter',pulse=6,meter=1000,notState=3200,noDamage=true,power=1000},
 {name='Standing guard',defend=true,state=150,noDamage=true},
 {name='Crouch guard',defend=true,down=true,state=152,noDamage=true},
 {name='Thrown by Will',actor=1,pulse=7,state=801,exact=110},
 {name='Captured by Fresh Prince',actor=1,pulse=6,state=3210,exact=420},
 {name='Captured by Agent J',actor=1,agentWill=true,pulse=6,state=4510,exact=390},
 {name='Agent captured by Jinwoo throw',agentWill=true,pulse=7,state=801,exact=105},
 {name='Agent captured by Arise',agentWill=true,pulse=6,state=3210,exact=950},
}
for _,c in ipairs({ {name='Igris summon',summon=1,pulse=13,state=1100,exact=100,power=2750}, {name='Beru summon',summon=2,pulse=14,state=1110,exact=110,power=2750}, {name='Iron summon',summon=3,pulse=15,state=1120,exact=125,power=2750}, {name='Tank summon',summon=4,pulse=16,state=1130,exact=115,power=2750}, {name='Igris assigned repeat 1',summon=1,pulse=13,state=1100,exact=100,power=2750}, {name='Beru assigned repeat 1',summon=2,pulse=14,state=1110,exact=110,power=2750}, {name='Iron assigned repeat 1',summon=3,pulse=15,state=1120,exact=125,power=2750}, {name='Tank assigned repeat 1',summon=4,pulse=16,state=1130,exact=115,power=2750}, {name='Igris assigned repeat 2',summon=1,pulse=13,state=1100,exact=100,power=2750}, {name='Beru assigned repeat 2',summon=2,pulse=14,state=1110,exact=110,power=2750}, {name='Iron assigned repeat 2',summon=3,pulse=15,state=1120,exact=125,power=2750}, {name='Tank assigned repeat 2',summon=4,pulse=16,state=1130,exact=115,power=2750}, {name='Igris assigned repeat 3',summon=1,pulse=13,state=1100,exact=100,power=2750}, {name='Beru assigned repeat 3',summon=2,pulse=14,state=1110,exact=110,power=2750}, {name='Iron assigned repeat 3',summon=3,pulse=15,state=1120,exact=125,power=2750}, {name='Tank assigned repeat 3',summon=4,pulse=16,state=1130,exact=115,power=2750}, {name='Toward R selects Beru',summon=2,pulse=4,walk=1,state=1110,exact=110,power=2750}, {name='Away R selects Iron',summon=3,pulse=4,walk=-1,state=1120,exact=125,power=2750}, {name='Down R selects Tank',summon=4,pulse=4,down=true,state=1130,exact=115,power=2750}}) do table.insert(cases,c) end
local filter=os.getenv('JINWOO_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,c in ipairs(cases) do if c.name==filter then table.insert(selected,c) end end
 assert(#selected>0,'Unknown filter');cases=selected
end
local report={status='Running',method='Native engine with Will P1 and Jinwoo P2',checks={}}
local index,tick=1,0
local motionFrames,currentSummon={},nil
local assignedSeen={}
local seen,violations,minTarget,minPower,minActorY={}, {},1000,3000,0
local function save() jsonEncode(report,'../../characters/jinwoo/runtime-validation.json') end
hook.add('loop','jinwoo-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  report.assignedSummons=assignedSeen;save();print('JINWOO_TESTS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 local actor=c.actor or 2;local target=3-actor
 tick=tick+1
 if tick==1 then
  seen={};violations={};motionFrames={};currentSummon=nil;minTarget=1000;minPower=3000;minActorY=0
  for p=1,2 do player(p);for _,key in ipairs({'pulse','down','guard','backthrow','walk','armySeen','armyMissing','armyLeak','summon','shadow0','shadow1','shadow2','shadow3'}) do mapSet('test.'..key,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',c.agentWill and 2 or 1)
  player(2);mapSet('test.form',c.stefan and 2 or 1)
  player(2);mapSet('test.summon',c.summon or 0)
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
 if c.probeKnight and tick==100 then player(actor);mapSet('test.pulse',4) end
 if c.enemyAt and tick==c.enemyAt then player(target);mapSet('test.pulse',1) end
 if c.probeAt and tick==c.probeAt then player(actor);mapSet('test.pulse',12) end
 if c.walk and tick==90 then player(actor);mapSet('test.walk',0) end
 if tick>=20 then
  player(actor);seen[tostring(stateNo())]=true;motionFrames[tostring(spriteVar('image'))]=true;
  if actor==2 and stateNo()>=1100 and stateNo()<=1130 and time()>=2 then currentSummon=_G['var'](35) end;minPower=math.min(minPower,power());minActorY=math.min(minActorY,posY())
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
  player(2);local armySeen=map('test.armySeen');local armyMissing=map('test.armyMissing');local armyLeak=map('test.armyLeak')
  if armyMissing~=0 or armyLeak~=0 then ok=false end
  if (c.name=='Arise army ultimate' or c.name=='Agent captured by Arise') and armySeen~=1 then ok=false end
  local namedWaves={}
  for i=0,3 do namedWaves[tostring(i)]=map('test.shadow'..i) end
  if actor==2 and c.state==3210 then for i=0,3 do if namedWaves[tostring(i)]~=1 then ok=false end end end
  local frameCount=0;for _ in pairs(motionFrames) do frameCount=frameCount+1 end
  if actor==2 and ((c.walk and not c.pulse) or c.name=='Dagger check') and frameCount<6 then ok=false end
  if c.summon then if currentSummon~=c.summon-1 then ok=false end;assignedSeen[tostring(currentSummon)]=true end
  player(target);local targetFinal=stateNo()
  if actorFinal~=0 and actorFinal~=10 and actorFinal~=130 and actorFinal~=131 and actorFinal~=140 then ok=false end
  if c.exact or c.damage then if targetFinal~=0 and targetFinal~=10 and targetFinal~=130 and targetFinal~=131 and targetFinal~=140 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,minPower=minPower,actorLife=actorLife,actorFinal=actorFinal,
       targetFinal=targetFinal,states=seen,outfitViolations=violations,armySeen=armySeen,armyMissing=armyMissing,armyLeak=armyLeak,namedWaves=namedWaves,summon=currentSummon,motionFrameCount=frameCount})
  report.current=index;save();print('JINWOO_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
