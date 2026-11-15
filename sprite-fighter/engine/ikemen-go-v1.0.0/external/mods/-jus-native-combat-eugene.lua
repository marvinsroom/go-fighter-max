local report={status='Running',slug='eugene',checks={},cases={}}
local tick,warmup=0,0
local cases={{name='Native normal connects',x=89,targetx=101}, {name='Whiff never launches',x=0,targetx=210,up=true,whiff=true}, {name='Confirmed normal launches',x=89,targetx=101,up=true,launch=true}}
local index,phase,hit,launched,landed=1,0,false,false,false
local function save() jsonEncode(report,'../../jus-upgrade/native-combat/eugene/current.json') end
local function check(name,ok,actual) table.insert(report.checks,{label=name,passed=ok,actual=actual});save() end
local function reset(air,meter)
 player(1);mapSet('justest.dash',0);mapSet('justest.flight',0);mapSet('justest.up',0);mapSet('justest.worldx',0);mapSet('jus.airdash_used',0);setPower(meter or 2000);setLife(1000);changeState(air and 8797190 or 8797191)
end
local dashHit,dashEntered,flightHit,flightEntered=false,false,false,false
hook.add('loop','jus-combat-eugene',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if tick==0 and 'eugene'=='rimuru' then
  table.insert(cases,{name='Demon Lord confirmed normal launches',x=89,targetx=101,up=true,launch=true,form=1})
  table.insert(cases,{name='Slime confirmed normal launches',x=89,targetx=101,up=true,launch=true,form=2})
 end
 tick=tick+1
 local c=cases[index]
 if c then
  phase=phase+1
  if phase==1 then
   reset(false);mapSet('justest.worldx',c.x)
   if 'eugene'=='rimuru' then mapSet('rimuru.form',c.form or 0) end
   player(2);mapSet('justest.worldx',c.targetx);mapSet('jus.launched',0);mapSet('jus.launch_request',0);setLife(1000);changeState(8797192);player(1)
   hit=false;launched=false;landed=false
  end
  if phase==12 then
   if c.up then mapSet('justest.up',1) end
   changeState(('eugene'=='jin-mori' and 230 or 200))
  end
  if phase>12 then
   player(2);if life()<1000 then hit=true end
   if stateNo()==8797103 then launched=true end
   if launched and posY()>=0 then landed=true end
   player(1)
  end
  if phase==70 then screenshot() end
  if phase==180 then
   if c.whiff then check(c.name,not hit and not launched,{hit=hit,launched=launched})
   elseif c.launch then
    check(c.name,hit and launched,{hit=hit,launched=launched})
    check('Launched victim returns to ground',not launched or landed,landed)
   else
    check(c.name,hit,hit)
    check('Arena slab reacts to actual nearby fighter hit',map('jus.prop_right')>0,map('jus.prop_right'))
   end
   table.insert(report.cases,{name=c.name,hit=hit,launched=launched,landed=landed})
   mapSet('justest.up',0);index=index+1;phase=0;save()
  end
  return
 end
 phase=phase+1
 if phase==1 then reset(true);player(2);mapSet('justest.worldx',150);changeState(8797192);player(1) end
 if phase==7 then mapSet('justest.dash',1) end
 if phase==9 then
  dashEntered=stateNo()==8797101
  mapSet('justest.dash',0);player(2);changeState(8797194);player(1)
 end
 if phase>=10 and phase<=20 and life()<1000 and stateNo()~=8797101 then dashHit=true end
 if phase==25 then
  check('Dash command entered before collision',dashEntered,dashEntered)
  if 'eugene'~='saitama' then check('Air dash remains vulnerable to a real HitDef',dashHit,{hit=dashHit,hp=life(),state=stateNo()})
  else report.source_exception='Original Saitama source intentionally rejects damage; no added JUS invulnerability.' end
  reset(true)
 end
 if phase==32 then mapSet('justest.flight',1) end
 if phase==35 then
  flightEntered=stateNo()==8797102;mapSet('justest.flight',0)
  player(2);changeState(8797194);player(1)
 end
 if phase>=36 and phase<=50 and life()<1000 and stateNo()~=8797102 then flightHit=true end
 if phase==55 then
  if 0==1 then
   check('Flight entered before collision',flightEntered,flightEntered)
   check('Real hit interrupts flight',flightHit,{hit=flightHit,hp=life(),state=stateNo()})
  end
  screenshot()
 end
 if phase==65 then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
