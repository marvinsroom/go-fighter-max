local report={runtime_sha256={["baam-common.zss"]="eb98787e00a476023b94e2b7d815971b7d2d941e5e990c5cf077188b2174047f",["baam.air"]="7547882778599b212e931d71995e897175016aeafdc5999d355d11d6e65ae3e9",["baam.cmd"]="1f60d3574ebdb3e3539fd507300b5a20d1e6fba7536c47cc6bd3a412dc741eac",["baam.cns"]="92a8bd36eb89bdf1e11ca5af53ef1cb823326d6c775eabae6568638d4156881c",["baam.def"]="7cdf7b4f809065757185070d1dd067f41d7da7ebac62545f5abda666addbd882",["baam.sff"]="c81ae74085584f2fcee41fc79a7217530e2eae2ca7bc960ee5d72d55b1d3228d",["baam.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',intro_seen=false,cuff_seen=false,attack_seen=false,frames={}}
local tick,shot,pending=0,0,nil
hook.add('loop','baam-production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true;if spriteVar('group')==62200 and spriteVar('image')==2 then report.cuff_seen=true end end
 if roundState()==2 then tick=tick+1;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/baam/replays/comic-20261021111723-startup/Baam_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='Baam_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190) or (tick>0 and tick%20==0)) then
  pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};screenshot()
 end
 player(2);report.target_life=life();player(1)
 if tick>=200 or (tick>100 and roundState()>2) then
  report.status='Complete';report.passed=report.intro_seen and report.cuff_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/baam/startup-ai-validation.json');jsonEncode(report,'../../characters/baam/startup-ai-validation.json');print('BAAM_STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
