local ticks=0
local report={status='Running',recording=false,forward_keys={},backward_keys={},samples={}}
local function worldX() return posX()+cameraPosX() end
local function keysCount(keys) local n=0;for k,v in pairs(keys) do n=n+1 end;return n end
hook.add('loop','walk-cadence-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 mapSet('walktest.direction',ticks>=10 and ticks<=99 and 1 or (ticks>=120 and ticks<=229 and -1 or 0))
 if ticks==30 then report.forward_start=worldX() end
 if ticks==90 then report.forward_speed=(worldX()-report.forward_start)/60 end
 if ticks==150 then report.backward_start=worldX() end
 if ticks==210 then report.backward_speed=(worldX()-report.backward_start)/60 end
 if ticks>=30 and ticks<=90 then report.forward_keys[tostring(animElemNo(0))]=true end
 if ticks>=150 and ticks<=210 then report.backward_keys[tostring(animElemNo(0))]=true end
 if ticks%10==0 then table.insert(report.samples,{tick=ticks,state=stateNo(),animation=anim(),element=animElemNo(0),velocity=velX()}) end
 if ticks>=240 then
  report.forward_elements=keysCount(report.forward_keys);report.backward_elements=keysCount(report.backward_keys)
  report.passed=math.abs(report.forward_speed-.95)<.03 and math.abs(report.backward_speed+.72)<.03 and report.forward_elements==8 and report.backward_elements==8
  report.status=report.passed and 'PASS' or 'FAIL'
  jsonEncode(report,'../../walk-fix-v11/validation/jin_mori.json');os.exit(report.passed and 0 or 1)
 end
end)
