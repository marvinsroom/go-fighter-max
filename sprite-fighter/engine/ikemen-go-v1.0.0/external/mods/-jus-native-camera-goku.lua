local report={status='Running',slug='goku',checks={},samples={}}
local tick,warmup=0,0
local function save() jsonEncode(report,'../../jus-upgrade/native-camera/goku/current.json') end
local function check(label,passed,actual) table.insert(report.checks,{label=label,passed=passed,actual=actual});save() end
hook.add('loop','jus-camera-goku',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 tick=tick+1
 if tick==1 then setPower(3000);changeState(8797190) end
 if tick==7 then mapSet('justest.flight',1) end
 if tick==10 then mapSet('justest.flight',0);mapSet('justest.up',1) end
 if tick==70 then
  local zoom=cameraZoom();local py=posY()*320/533;local feet=screenPosY()*zoom;local x=screenPosX()*zoom
  -- The engine's widescreen viewport is 426.67x240 at this 16:9 resolution.
  -- Character 320-unit coordinates gain the same 4/3 aspect factor.
  local top=feet-55*(4/3)*zoom
  player(2);local otherFeet=screenPosY()*zoom;local otherX=screenPosX()*zoom;player(1)
  check('Real flight reaches bounded ceiling',stateNo()==8797102 and math.abs(py+180)<2,{state=stateNo(),world_y=py})
  check('Camera zooms out for vertical separation',zoom<.95 and zoom>=.49,zoom)
  check('Flying fighter stays below HUD and in frame',top>=46 and feet<235 and x>0 and x<427,{top=top,feet=feet,x=x})
  check('Grounded opponent remains in frame',otherFeet>70 and otherFeet<=240 and otherX>0 and otherX<427,{feet=otherFeet,x=otherX})
  table.insert(report.samples,{label='Flight ceiling',zoom=zoom,world_y=py,top=top,feet=feet,opponent_feet=otherFeet});screenshot()
 end
 if tick==95 then mapSet('justest.up',0);mapSet('justest.flight',1) end
 if tick==98 then mapSet('justest.flight',0) end
 if tick==270 then
  check('Flight exit lands normally',posY()==0,posY())
  check('Camera returns to ground combat zoom',cameraZoom()>.95,cameraZoom());screenshot()
 end
 if tick==285 then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
