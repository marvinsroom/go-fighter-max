local report={runtime_sha256={["eugene-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["eugene.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["eugene.cmd"]="e09d90a6b9192b746ecdea9e77da14d626d847f9a1085485a81c6715a5e8862d",["eugene.cns"]="85d40e94b02e952ffc313977e90f0eb8b24ba6cabab363a8876b793506703f03",["eugene.def"]="6a45875b55a7a1c25deaa215a3d1c6b00b9426d6d22ae8200bb25af0bd1d501a",["eugene.sff"]="fa1cb6713f4e9b86b2634dd5776803e406557b0e87114d03eae6280618ad140f",["eugene.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/eugene/replays/startup-v20261021160001/EugeneLionheart_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='EugeneLionheart_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/eugene/startup-ai-validation.json');jsonEncode(report,'../../characters/eugene/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
