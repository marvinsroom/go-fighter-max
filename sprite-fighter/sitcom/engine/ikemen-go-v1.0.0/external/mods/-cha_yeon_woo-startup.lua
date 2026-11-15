local report={runtime_sha256={["cha_yeon_woo-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["cha_yeon_woo.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["cha_yeon_woo.cmd"]="af5bdacbbd09fa89b7fbd9a227b45c94f85d067b70858c694e7e0c4f46db911b",["cha_yeon_woo.cns"]="5e27d4407b01f11c57a1ac87dfd535e447c76ceec01a8da34bf8e4ec4b2e141c",["cha_yeon_woo.def"]="8951cec68418ca2de98871319db8760eb62b2965d9526f9f4f59971e8d29de9c",["cha_yeon_woo.sff"]="df376842ec0225ab5c3f750ad8f53de54bb8f204d5d46930fa9968b6eadacd27",["cha_yeon_woo.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/cha-yeon-woo/replays/startup-v20261021112001/ChaYeonWoo_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='ChaYeonWoo_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/cha-yeon-woo/startup-ai-validation.json');jsonEncode(report,'../../characters/cha-yeon-woo/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
