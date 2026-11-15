local report={runtime_sha256={["kim_dokja-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["kim_dokja.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["kim_dokja.cmd"]="35434cac1960fdd666fcce2735f7c8393266f5f21c17b412d8439ae014ad3793",["kim_dokja.cns"]="f5ffb35b0646cf58985b4841b6573cecef04d9511085afcc322e12bbe16621fc",["kim_dokja.def"]="d5dd114fb6ecc07110c822e7b06715f4a47b98e708bab486a58739d794e1ba04",["kim_dokja.sff"]="9288dd57a254454351f1b74cdd0e553faac47c494d85695e92a2198a423b15e2",["kim_dokja.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/kim-dokja/replays/startup-v20261021095528/KimDokja_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='KimDokja_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/kim-dokja/startup-ai-validation.json');jsonEncode(report,'../../characters/kim-dokja/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
