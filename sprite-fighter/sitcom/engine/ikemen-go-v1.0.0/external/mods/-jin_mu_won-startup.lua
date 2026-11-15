local report={runtime_sha256={["jin_mu_won-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["jin_mu_won.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["jin_mu_won.cmd"]="f95305a9e11d6526d914772a9551b5a24f589b58e6dbaf05c273de72c034cc05",["jin_mu_won.cns"]="5d512b3144aed6ea76a8bdfeece4b423b15e80a3e1b35c13cc8cecc6dc79083e",["jin_mu_won.def"]="19b3098714bfb06dfcc2ef595f0f88936cb6cd4f6a3c6e9c24ad504240cca63a",["jin_mu_won.sff"]="57f3e5241fe21adcb5e1ff49e3c5f36928d28766598d11d9461f6c188544dfdb",["jin_mu_won.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/jin-mu-won/replays/startup-v20261021160000/JinMuWon_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='JinMuWon_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/jin-mu-won/startup-ai-validation.json');jsonEncode(report,'../../characters/jin-mu-won/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
