local report={runtime_sha256={["mok_gyeongwoon-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["mok_gyeongwoon.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["mok_gyeongwoon.cmd"]="57c54e6d91d3b11ab40cfa67a8e6d8df2658da0e3c4bd759d8b9f6396422181c",["mok_gyeongwoon.cns"]="58c9f1e7bed9fe7f6069fc48244caa6de3f978cb23abcc51d4b0a9290a1693ba",["mok_gyeongwoon.def"]="eab4d4aa1f83b9551f39edd6da34d27358de4e82f63074ea53be6fd838f6b722",["mok_gyeongwoon.sff"]="bba16af0fe9c000efcb2f8aa120b4c758dbb1ebb65577a1218d7438a2acbf1d0",["mok_gyeongwoon.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/mok-gyeongwoon/replays/startup-v20261021103501/MokGyeongwoon_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='MokGyeongwoon_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/mok-gyeongwoon/startup-ai-validation.json');jsonEncode(report,'../../characters/mok-gyeongwoon/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
