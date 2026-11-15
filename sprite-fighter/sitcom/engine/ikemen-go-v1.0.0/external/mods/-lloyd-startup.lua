local report={runtime_sha256={["lloyd-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["lloyd.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["lloyd.cmd"]="4ecde8e9db7c05f0f8a99da716b108074c7ecd085e10b0e643c8c9ac92fe9b90",["lloyd.cns"]="f5eba1f4dc96f9fd6ba71a5dcac4e0bdb2083005dede5ecd226956d4bb1c8cf2",["lloyd.def"]="450b0e02517c9a1625927125a33fcb456b9be4711d250daa9a32ee80c09e0c4e",["lloyd.sff"]="5cd1799cb3f31c6b0d04faa49004f7d6bef7b8ccd25828762ce918ece0248c2d",["lloyd.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/lloyd/replays/startup-v20261021101938/Lloyd_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='Lloyd_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/lloyd/startup-ai-validation.json');jsonEncode(report,'../../characters/lloyd/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
