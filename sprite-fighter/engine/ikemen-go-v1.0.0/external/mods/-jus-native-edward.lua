local report={status='Running',slug='edward',checks={},samples={}}
local tick,warmup=0,0
local entered,backward,firstdash,second,flightSeen,flightCost,lowSeen=false,false,false,false,false,0,false
local startX,flightStart,flightPower,startFacing=0,0,0,1
local walkKeys,walkStates={},{}
local jumpPeak,jumped,landed=0,false,false
-- posX() is camera-relative; use the world root for displacement checks.
local function worldX() return posX()+cameraPosX() end
local function save() jsonEncode(report,'../../jus-upgrade/native/edward/current.json') end
local function check(label,ok,actual) table.insert(report.checks,{label=label,passed=ok,actual=actual});save() end
local function clear()
 for _,key in ipairs({'dash','back','flight','up','walk','jump'}) do mapSet('justest.'..key,0) end
end
local function setup(air,meter)
 clear();setPower(meter or 2000);mapSet('jus.airdash_used',0);changeState(air and 8797190 or 8797191)
end
hook.add('loop','jus-mobility-edward',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 tick=tick+1
 if (tick>=5 and tick<=24) or (tick>=43 and tick<=60) or (tick>=83 and tick<=100) then table.insert(report.samples,{tick=tick,state=stateNo(),y=posY(),x=posX(),control=ctrl(),facing=facing(),back=commandGetState(1,'jus.back'),up=commandGetState(1,'jus.up'),direction=map('jus.dash_direction'),dash=map('justest.dash'),used=map('jus.airdash_used')}) end
 if tick==1 then
  check('JUS layer enabled',map('jus.enabled')==1,map('jus.enabled'))
  check('Flight policy',map('jus.flight_allowed')==0,map('jus.flight_allowed'))
  setup(true)
 end
 if tick==7 then startX=worldX();startFacing=facing();mapSet('justest.dash',1) end
 if tick>=8 and tick<=22 and stateNo()==8797101 then entered=true end
 if tick==10 then clear() end
 if tick==22 then
  check('Air dash follows common command',entered,stateNo())
  check('Air dash moves forward',(worldX()-startX)*startFacing>15*533/320,(worldX()-startX)*startFacing)
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
 -- Hold direction before the button and through state entry, as a player does.
 -- Clearing both after three ticks can drop Back before the dash's time=0.
 if tick==43 then mapSet('justest.back',1) end
 if tick==46 then startX=worldX();startFacing=facing();mapSet('justest.dash',1) end
 if tick>=47 and tick<=56 and stateNo()==8797101 then backward=true end
 if tick==49 then mapSet('justest.dash',0) end
 if tick==60 then
  check('Backward air dash enters',backward,stateNo())
  check('Backward air dash moves back',(worldX()-startX)*startFacing<-15*533/320,(worldX()-startX)*startFacing)
  setup(true,200)
 end
 if tick==64 then mapSet('justest.up',1) end
 if tick==67 then mapSet('justest.flight',1) end
 if tick>=68 and tick<=76 and stateNo()==8797102 then lowSeen=true end
 if tick==70 then clear() end
 if tick==78 then check('Flight blocked below entry meter',not lowSeen,stateNo());setup(true,2000) end
 if tick==82 then mapSet('justest.up',1) end
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
 if tick==135 then setup(false) end
 if tick==142 then startX=worldX();startFacing=facing();mapSet('justest.walk',1) end
 if tick>=145 and tick<=170 then
  walkKeys[tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))]=true
  walkStates[tostring(stateNo())]=true
 end
 if tick==171 then
  local count=0;for _ in pairs(walkKeys) do count=count+1 end
  check('Native walking moves at compact pace',(worldX()-startX)*startFacing>15*533/320,(worldX()-startX)*startFacing)
  if 0>0 then check('Eight new walk drawings appear in native animation',count==0,count) end
  report.walk={distinct_drawings=count,keys=walkKeys,states=walkStates};clear()
 end
 if tick==175 then screenshot() end
 if tick==180 then setup(false) end
 if tick==187 then mapSet('justest.jump',1) end
 if tick==190 then clear() end
 if tick>=188 and tick<=285 then
  jumpPeak=math.min(jumpPeak,posY());if posY()<0 then jumped=true end
  if jumped and posY()>=0 then landed=true end
 end
 if tick==286 then
  check('Native jump clears compact fighter height',jumpPeak<-55*533/320,jumpPeak)
  check('Jump returns to ground',landed,posY());report.jump_peak=jumpPeak
 end
 if tick==290 then screenshot() end
 if tick==300 then
  report.status='Complete';report.passed=0;report.failed=0
  for _,c in ipairs(report.checks) do if c.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
