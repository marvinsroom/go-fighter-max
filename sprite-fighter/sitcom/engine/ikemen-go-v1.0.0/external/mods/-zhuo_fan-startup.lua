local report={runtime_sha256={["zhuo_fan-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["zhuo_fan.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["zhuo_fan.cmd"]="5e1ce624b473c07366606ce36008faaeb680ae523aa5e35e24eaadf04693fd62",["zhuo_fan.cns"]="216fc53ecf550f34e896662624dadb5006d0c5eb2005d375197cb34e0fb69ecd",["zhuo_fan.def"]="1492db4074620fb26edea2520c7141b9ce308e05fd070b55f86c4bf0ff3e5e15",["zhuo_fan.sff"]="1a24b03ac683ffdace5f956536a86906033121abce88e1477126461e316e4c4c",["zhuo_fan.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/zhuo-fan/replays/startup-v20261021104301/ZhuoFan_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='ZhuoFan_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/zhuo-fan/startup-ai-validation.json');jsonEncode(report,'../../characters/zhuo-fan/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
