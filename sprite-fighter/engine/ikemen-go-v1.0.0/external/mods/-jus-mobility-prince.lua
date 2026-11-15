local report={status='Running',slug='prince',checks={},samples={}}
local tick,warmup=0,0
local entered,backward,firstdash,second,flightSeen,flightCost,lowSeen=false,false,false,false,false,0,false
local startX,flightStart,flightPower=0,0,0
local function save() jsonEncode(report,'../../jus-upgrade/native/prince/current.json') end
local function check(label,ok,actual) table.insert(report.checks,{label=label,passed=ok,actual=actual});save() end
local function clear()
 for _,key in ipairs({'dash','back','flight','up'}) do mapSet('justest.'..key,0) end
end
local function setup(air,meter)
 clear();setPower(meter or 2000);mapSet('jus.airdash_used',0);changeState(air and 8797190 or 8797191)
end
hook.add('loop','jus-mobility-prince',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 tick=tick+1
 if tick>=5 and tick<=24 then table.insert(report.samples,{tick=tick,state=stateNo(),y=posY(),x=posX(),control=ctrl(),dash=map('justest.dash'),used=map('jus.airdash_used')}) end
 if tick==1 then
  check('JUS layer enabled',map('jus.enabled')==1,map('jus.enabled'))
  check('Flight policy',map('jus.flight_allowed')==0,map('jus.flight_allowed'))
  setup(true)
 end
 if tick==7 then startX=posX();mapSet('justest.dash',1) end
 if tick>=8 and tick<=22 and stateNo()==8797101 then entered=true end
 if tick==10 then clear() end
 if tick==22 then
  check('Air dash follows common command',entered,stateNo())
  check('Air dash moves forward',posX()>startX+15*2133/320,posX()-startX)
  check('Air dash consumes airborne budget',map('jus.airdash_used')==1,map('jus.airdash_used'))
  mapSet('justest.dash',1)
 end
 if tick>=24 and tick<=32 and stateNo()==8797101 then second=true end
 if tick==32 then
  check('Second dash blocked before landing',not second,stateNo());setup(false)
 end
 if tick==39 then
  check('Landing restores dash budget',map('jus.airdash_used')==0,map('jus.airdash_used'));setup(true)
 end
 if tick==46 then startX=posX();mapSet('justest.back',1);mapSet('justest.dash',1) end
 if tick>=47 and tick<=56 and stateNo()==8797101 then backward=true end
 if tick==49 then clear() end
 if tick==60 then
  check('Backward air dash enters',backward,stateNo())
  check('Backward air dash moves back',posX()<startX-15*2133/320,posX()-startX)
  setup(true,200)
 end
 if tick==67 then mapSet('justest.flight',1) end
 if tick>=68 and tick<=76 and stateNo()==8797102 then lowSeen=true end
 if tick==70 then clear() end
 if tick==78 then check('Flight blocked below entry meter',not lowSeen,stateNo());setup(true,2000) end
 if tick==85 then mapSet('justest.flight',1);flightPower=power() end
 if tick>=86 and tick<=105 and stateNo()==8797102 then flightSeen=true end
 if tick==88 then clear() end
 if tick==106 then
  check('Flight eligibility respected',flightSeen==(0==1),flightSeen)
  if 0==1 then check('Sustained flight spends meter',power()<=flightPower-70,power());mapSet('justest.flight',1) end
 end
 if tick==110 then clear() end
 if tick==115 and 0==1 then check('Flight toggle returns to native fall',stateNo()~=8797102,stateNo()) end
 if tick==120 then setup(false) end
 if tick==127 then mapSet('justest.dash',1) end
 if tick==129 then check('Air dash never steals grounded input',stateNo()~=8797101,stateNo());clear() end
 if tick==135 then
  screenshot();report.status='Complete';report.passed=0;report.failed=0
  for _,c in ipairs(report.checks) do if c.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
