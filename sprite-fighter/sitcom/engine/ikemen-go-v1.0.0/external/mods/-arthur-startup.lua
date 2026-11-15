local report={runtime_sha256={["arthur-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["arthur.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["arthur.cmd"]="c099caf74f54138e55087ffc4b15805c46cbf209feb1f167223bbe33200bffe7",["arthur.cns"]="86fe1125f0d4078b27dcde83e8b7e9f3cc98b2dd92af82f27e215696da0df6a3",["arthur.def"]="6ae1c0fbc6f40b3faf51ba9d5743b01d814de731227b93f3c1b062d34845454a",["arthur.sff"]="4214645a785c654e017eee54561e5f6161f9a0d93cded7750fda206d532e8c40",["arthur.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/arthur/replays/startup-v20261021110201/ArthurLeywin_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='ArthurLeywin_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/arthur/startup-ai-validation.json');jsonEncode(report,'../../characters/arthur/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
