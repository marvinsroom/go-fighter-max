local report={runtime_sha256={["gang_ryong-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["gang_ryong.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["gang_ryong.cmd"]="e26742831c99e5936b7b9b053ddedc9a6305ba5a6298a120536f379f5fe41e21",["gang_ryong.cns"]="12eefa5a090b287b72afe3c2d566cfc5189fc33f8e9edd30728f8678220edf23",["gang_ryong.def"]="8a1baebf4ebec134831af739b9c38a93be81d8aef1e8453505472b10e6d8c87a",["gang_ryong.sff"]="15f08ee466b0c4ef04386c306b1572ffee1dc452cf682ee7d3679e805f53a8a1",["gang_ryong.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/gang-ryong/replays/startup-v20261021100808/GangRyong_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='GangRyong_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/gang-ryong/startup-ai-validation.json');jsonEncode(report,'../../characters/gang-ryong/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
