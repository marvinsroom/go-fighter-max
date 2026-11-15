
local tick,shot=0,0
local pending=nil
local report={method='Actual native engine; command asserted for each transform and move',capture_directory='paired-v2',frames={}}
hook.add('loop','prince-pair-preview',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/prince/replays/paired-v2/Chappelle_pair_prince'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','form','down','guard','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end end
 if tick==20 or tick==540 then player(2);mapSet('test.pulse',13) end
 if tick==90 or tick==610 then player(2);mapSet('test.pulse',8) end
 if tick==150 or tick==520 or tick==700 then player(1);changeState(9000);player(2);changeState(9012) end
 if tick==170 then player(2);mapSet('test.pulse',5) end
 if tick==720 then player(2);mapSet('test.pulse',6) end
 if not pending and tick>=14 and tick<1310 and tick%8==6 then
  player(2);screenshot();pending={index=shot+1,tick=tick,state=stateNo(),animation=anim(),form=_G['var'](45),group=spriteVar('group')}
 end
 if tick>=1320 then jsonEncode(report,'../../characters/prince/paired-preview-report.json');print('PAIRED_PREVIEW_COMPLETE prince '..shot);os.exit() end
end)
