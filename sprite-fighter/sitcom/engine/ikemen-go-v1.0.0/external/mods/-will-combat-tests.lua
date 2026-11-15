-- Opt-in native engine integration tests. No autoload: leading '-' filename.
local cases = {
 {name='Agent chained moves outfit',agent=true,pulse=1,chain=true,damage=true},
 {name='Agent mirror hurt outfit',agent=true,enemyAgent=true,enemyAttackAt=30,hitP1=true,noDamage=true},
 {name='Agent forward throw outfit',agent=true,pulse=7,state=801,damage=true},
 {name='Agent back throw outfit',agent=true,pulse=7,back=true,state=811,damage=true},
 {name='Agent jump landing outfit',agent=true,jump=true},
 {name='Agent forward walk outfit',agent=true,walk=1,state=20,noDamage=true},
 {name='Agent backward walk outfit',agent=true,walk=-1,state=21,noDamage=true},
 {name='Agent hurt outfit',agent=true,enemyAttackAt=30,hitP1=true,noDamage=true},
 {name='Agent knockdown outfit',agent=true,enemyAttackAt=30,enemyPulse=12,hitP1=true,noDamage=true},
 {name='Agent standing guard outfit',agent=true,ownGuard=true,enemyAttackAt=30,state=150,noDamage=true},
 {name='Agent crouch guard outfit',agent=true,ownGuard=true,ownDown=true,enemyAttackAt=30,state=152,noDamage=true},
 {name='Agent transformation',pulse=14,state=3900,form=1,power=2000,noDamage=true},
 {name='Agent return to Fresh Prince',agent=true,pulse=14,state=3901,form=0,power=3000,noDamage=true},
 {name='Transformation requires meter',pulse=14,meter=0,notState=3900,form=0,noDamage=true},
 {name='Suit up can be interrupted before switch',pulse=14,enemyAttackAt=30,state=3900,form=0,hitP1=true,noDamage=true,power=2000},
 {name='Suit up stays Agent after late interruption',pulse=14,enemyAttackAt=52,state=3900,form=1,hitP1=true,noDamage=true,power=2000},
 {name='Transformation preserves health',pulse=14,startLife=600,state=3900,form=1,lifeP1=600,noDamage=true},
 {name='Transformation cooldown prevents immediate revert',pulse=14,probeAt=90,state=3900,notState=3901,form=1,noDamage=true},
 {name='Agent Agency Check',agent=true,pulse=1,state=4100,damage=true},
 {name='Agent Standard Issue shot',agent=true,pulse=2,state=4110,damage=true},
 {name='Agent Black Tie Kick',agent=true,pulse=3,state=4120,damage=true},
 {name='Agent Cuff Check',agent=true,pulse=1,down=true,state=4140,damage=true},
 {name='Agent kneeling shot',agent=true,pulse=2,down=true,state=4150,damage=true},
 {name='Agent Sweep Protocol',agent=true,pulse=3,down=true,state=4160,damage=true},
 {name='Agent Air Intercept',agent=true,pulse=3,jump=true,state=4180,damage=true},
 {name='Agent Neuralyzer',agent=true,pulse=4,state=4320,exactDamage=20,power=2750},
 {name='Agent Noisy Cricket',agent=true,pulse=8,state=4300,damage=true},
 {name='Agent Deatomizer',agent=true,pulse=11,state=4310,damage=true},
 {name='Agent Evasive Protocol',agent=true,pulse=12,state=4330,noDamage=true},
 {name='Agent Overload super',agent=true,pulse=5,state=4400,exactDamage=220,power=2000},
 {name='Agent Galaxy Protocol hit',agent=true,pulse=6,state=4510,exactDamage=390,power=1000},
 {name='Agent Galaxy Protocol whiff',agent=true,pulse=6,far=true,notState=4510,noDamage=true,power=1000},
 {name='Agent Galaxy Protocol blocked',agent=true,pulse=6,guard=true,notState=4510,noDamage=true,power=1000},
 {name='Agent super requires meter',agent=true,pulse=5,meter=0,notState=4400,noDamage=true},
 {name='Agent low blocked crouching',agent=true,pulse=1,down=true,guard=true,guardDown=true,state=4140,noDamage=true},
 {name='Fresh Jab',pulse=1,damage=true,state=200},
 {name='Philly Straight',pulse=2,damage=true,state=210},
 {name='Punchline',pulse=3,damage=true,state=220},
 {name='Sneaker Tap',pulse=1,down=true,damage=true,state=400},
 {name='Floor Sweep knockdown',pulse=2,down=true,damage=true,state=410,fall=true},
 {name='High-Top Saver',pulse=3,down=true,damage=true,state=420},
 {name='Jump and landing',jump=true},
 {name='Fresh Sole air kick',pulse=2,jump=true,damage=true,state=610},
 {name='Double Take air kicks',pulse=3,jump=true,damage=true,state=620},
 {name='Forward throw',pulse=7,damage=true,state=801},
 {name='Back throw',pulse=7,back=true,damage=true,state=811},
 {name='Three-Piece palm branch',pulse=8,follow=1,damage=true,state=1020},
 {name='Three-Piece sweep branch',pulse=8,follow=2,damage=true,state=1030},
 {name='Three-Piece heel branch',pulse=8,follow=3,damage=true,state=1040},
 {name='Psyche has no hitbox',pulse=9,noDamage=true,state=1050},
 {name='Fresh Step upright kick',pulse=10,damage=true,state=1200},
 {name='Windmill Remix',pulse=11,damage=true,state=1300},
 {name='Taxi',pulse=12,damage=true,state=1400},
 {name='Run It Back meter reset',pulse=8,reset=true,state=1100,power=2000},
 {name='Standing guard blocks jab',pulse=1,guard=true,noDamage=true,state=200},
 {name='Standing guard loses to low',pulse=1,down=true,guard=true,damage=true,state=400},
 {name='Crouch guard blocks sweep',pulse=2,down=true,guard=true,guardDown=true,noDamage=true,state=410},
 {name='Super hit confirms',pulse=5,exactDamage=285,state=3010,power=2000},
 {name='Super whiff does not confirm',pulse=5,far=true,noDamage=true,notState=3010,power=2000},
 {name='Super blocked does not confirm',pulse=5,guard=true,noDamage=true,notState=3010,power=2000},
 {name='Ultimate hit confirms once',pulse=6,exactDamage=420,state=3210,power=1000},
 {name='Ultimate whiff does not confirm',pulse=6,far=true,noDamage=true,notState=3210,power=1000},
 {name='Ultimate blocked does not confirm',pulse=6,guard=true,noDamage=true,notState=3210,power=1000},
 {name='Super requires meter',pulse=5,meter=0,noDamage=true,notState=3000,power=0},
 {name='Ultimate requires meter',pulse=6,meter=1000,noDamage=true,notState=3200,power=1000},
 {name='Normal builds meter',pulse=1,meter=0,damage=true,state=200,gain=true},
 {name='Air Jab',pulse=1,jump=true,damage=true,state=600},
 {name='High Five overhead hits crouch guard',pulse=13,guard=true,guardDown=true,damage=true,state=280},
 {name='High Five overhead blocked standing',pulse=13,guard=true,noDamage=true,state=280},
}
local filter=os.getenv('WILL_TEST_FILTER')
if filter and filter~='' then
 local selected={};for _,case in ipairs(cases) do if case.name==filter or (filter:sub(-1)=='*' and case.name:sub(1,#filter-1)==filter:sub(1,-2)) then table.insert(selected,case) end end
 assert(#selected>0,'Unknown native test filter: '..filter);cases=selected
end
local index,tick,phase=1,0,0
local result={status='Running',method='Native engine command injection via opt-in AssertCommand states',checks={}}
local seen,enemySeen,minLife,minPower,minY={}, {},1000,3000,0
local outfitViolations={}
local reportPath='../../characters/will/'..(filter=='Agent *' and 'combat-runtime-agent-recheck.json' or ((filter and filter~='') and 'combat-runtime-recheck.json' or 'combat-runtime-validation.json'))
local function save()
 jsonEncode(result,reportPath)
end
local function pulse(code) player(1);mapSet('test.pulse',code) end
hook.add('loop','will-combat-suite',function()
 if not player(1) or roundState()~=2 then return end
 local case=cases[index]
 if not case then
  result.status='Complete';result.passed=0;result.failed=0
  for _,r in ipairs(result.checks) do if r.passed then result.passed=result.passed+1 else result.failed=result.failed+1 end end
  save();print('WILL_COMBAT_TESTS_COMPLETE '..result.passed..' passed '..result.failed..' failed');os.exit()
 end
 tick=tick+1
 if tick==1 then
  seen={};enemySeen={};minLife=1000;minPower=3000;minY=0;phase=0;outfitViolations={}
  for p=1,2 do player(p);mapSet('test.pulse',0);mapSet('test.guard',0);mapSet('test.down',0);mapSet('test.backthrow',0);mapSet('test.foreignCinematic',0);mapSet('test.agentBackdrop',0);mapSet('test.agentBeam',0);changeState(9000) end
 elseif tick==8 then
  player(1);setLife(case.startLife or 1000);setPower(case.meter or 3000);mapSet('test.form',case.agent and 2 or 1);if case.down then mapSet('test.down',1) end
  mapSet('test.walk',case.walk or 0)
  if case.ownGuard then mapSet('test.guard',1) end
  if case.ownDown then mapSet('test.down',1) end
  player(2);setLife(1000);mapSet('test.form',1);if case.far then changeState(9001) end
  if case.enemyAgent then mapSet('test.form',2) end
  if case.guard then mapSet('test.guard',1) end
  if case.guardDown then mapSet('test.down',1) end
 elseif tick==20 then
  player(1)
  if case.back then mapSet('test.guard',0);mapSet('test.pulse',7);mapSet('test.backthrow',1)
  elseif case.jump then changeState(40)
  elseif case.pulse then pulse(case.pulse) end
 end
 player(1)
 if case.enemyAttackAt and tick==case.enemyAttackAt then player(2);mapSet('test.pulse',case.enemyPulse or 1);player(1) end
 if case.walk and tick==90 then mapSet('test.walk',0) end
 if case.chain then
  if tick==60 then pulse(2) elseif tick==105 then pulse(3) elseif tick==165 then pulse(4) end
 end
 if case.probeAt and tick==case.probeAt then pulse(14) end
 if case.jump and case.pulse and tick==32 then pulse(case.pulse) end
 if (case.follow or case.reset) and stateNo()==1000 and time()>=15 and phase==0 then pulse(2);phase=1 end
 if stateNo()==1010 and time()>=14 and phase==1 then pulse(case.reset and 4 or case.follow);phase=2 end
 if tick>=20 then
  seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());minY=math.min(minY,posY())
  if _G['var'](30)==1 and stateNo()~=3900 and stateNo()~=3901 and spriteVar('group')~=10 and #outfitViolations<12 then
   table.insert(outfitViolations,{tick=tick,state=stateNo(),animation=anim(),element=animElemNo(0),group=spriteVar('group'),image=spriteVar('image')})
  end
  player(2);enemySeen[tostring(stateNo())]=true;minLife=math.min(minLife,life())
 end
 if tick>=((case.agent and case.pulse==6) and 420 or ((case.pulse==5 or case.pulse==6) and 330 or 240)) then
  player(1)
  local damage=1000-minLife;local ok=true
  if case.state and not seen[tostring(case.state)] then ok=false end
  if case.notState and seen[tostring(case.notState)] then ok=false end
  if case.damage and damage<20 then ok=false end
  if case.noDamage and damage>6 then ok=false end
  if case.exactDamage and damage~=case.exactDamage then ok=false end
  if case.power and minPower~=case.power then ok=false end
  local finalForm=_G['var'](30)
  if #outfitViolations>0 then ok=false end
  local foreignCinematic=map('test.foreignCinematic')
  local agentBackdrop=map('test.agentBackdrop')
  local agentBeam=map('test.agentBeam')
  if case.agent and (foreignCinematic~=0 or seen['3210'] or seen['3010']) then ok=false end
  if case.name=='Agent Galaxy Protocol hit' and (agentBackdrop~=1 or agentBeam~=1) then ok=false end
  if (not case.agent or case.name=='Agent Galaxy Protocol whiff' or case.name=='Agent Galaxy Protocol blocked') and (agentBackdrop~=0 or agentBeam~=0) then ok=false end
  if case.form and finalForm~=case.form then ok=false end
  if case.hitP1 and life()>980 then ok=false end
  if case.lifeP1 and life()~=case.lifeP1 then ok=false end
  if case.gain and power()<=0 then ok=false end
  if case.jump and minY>=-30 then ok=false end
  if case.fall and not (enemySeen['5050'] or enemySeen['5100'] or enemySeen['5110']) then ok=false end
  player(2);local finalEnemyState=stateNo();player(1)
  if case.damage or case.exactDamage then
   if finalEnemyState~=0 and finalEnemyState~=10 and finalEnemyState~=130 and finalEnemyState~=131 and finalEnemyState~=140 then ok=false end
  end
  local row={name=case.name,passed=ok,damage=damage,minPower=minPower,finalPower=power(),minY=minY,states=seen,enemyStates=enemySeen,finalEnemyState=finalEnemyState,finalForm=finalForm,foreignCinematic=foreignCinematic,agentBackdrop=agentBackdrop,agentBeam=agentBeam,outfitViolations=outfitViolations}
  table.insert(result.checks,row);result.current=index;save();print('WILL_TEST '..index..' '..case.name..' '..tostring(ok)..' damage='..damage)
  index=index+1;tick=0
 end
end)
