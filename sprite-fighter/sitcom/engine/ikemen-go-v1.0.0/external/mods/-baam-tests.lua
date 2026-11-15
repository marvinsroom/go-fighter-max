local cases={{["name"]="Return to base",["pulse"]=12,["state"]=800,["form"]=1,["expectForm"]=0,["length"]=190}}
local index,tick,shot=1,0,0
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["baam-common.zss"]="eb98787e00a476023b94e2b7d815971b7d2d941e5e990c5cf077188b2174047f",["baam.air"]="7547882778599b212e931d71995e897175016aeafdc5999d355d11d6e65ae3e9",["baam.cmd"]="1f60d3574ebdb3e3539fd507300b5a20d1e6fba7536c47cc6bd3a412dc741eac",["baam.cns"]="92a8bd36eb89bdf1e11ca5af53ef1cb823326d6c775eabae6568638d4156881c",["baam.def"]="7cdf7b4f809065757185070d1dd067f41d7da7ebac62545f5abda666addbd882",["baam.sff"]="c81ae74085584f2fcee41fc79a7217530e2eae2ca7bc960ee5d72d55b1d3228d",["baam.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',checks={},frames={},capture_directory='comic-20261021111723-return-retake'}
hook.add('loop','baam-tests',function()
 if not player(1) then return end
 if roundState()<2 and (stateNo()==190 or stateNo()==191) then report.natural_intro_seen=true;if spriteVar('group')==62200 and spriteVar('image')==2 then report.cuff_adjustment_seen=true end end
 if roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  os.remove('../../characters/baam/runtime-validation.json');jsonEncode(report,'../../characters/baam/runtime-validation.json');print('BAAM_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/baam/replays/comic-20261021111723-return-retake/Baam_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Baam_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('baam.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.inputdir',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*40)*(1280/192));mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if c.inputs then for _,input in ipairs(c.inputs) do if tick==input.tick then player(1);mapSet('test.pulse',input.pulse) end end end
 if c.probe and tick==c.probe then player(2);selfState(9004) end
 if tick==18 then player(1);mapSet('test.inputdir',c.rawdir or 0) end
 if tick==24 then player(1);mapSet('test.inputdir',0) end
 if tick==36 and c.counter then player(2);selfState(9004) end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==28 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(minLife)
 if c.capture~=false and tick>10 and caseShots<40 and not pending and ((stateNo()~=0 and tick%4==0 and (stateNo()==800 or key~=lastKey or tick%16==0)) or tick==12 or tick==c.length-4) then
 lastKey=key;caseShots=caseShots+1
  player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),power=power(),form=tonumber(map('baam.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=spriteVar('group'),drawing=spriteVar('image'),facing=facing(),cinematic_tick=time(),fx_count=numExplod(9108)+numExplod(9109)+numExplod(9110)+numExplod(9111)+numExplod(9112)+numExplod(9113)+numExplod(9114)+numExplod(9115),beam_count=numExplod(9112)+numExplod(9113),fx_x=tonumber(map('baam.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=spriteVar('group');pending.target_drawing=spriteVar('image');pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  if c.forbid and c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('baam.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.minDamage and 1000-minLife<c.minDamage then ok=false end
  if c.maxDamage and 1000-minLife>c.maxDamage then ok=false end
  for _,s in ipairs(c.requireStates or {}) do if not seen[tostring(s)] then ok=false end end
  if c.hurt and life()>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if (targetFinal==3050 or targetFinal==3051 or targetFinal==3052) then ok=false end
  table.insert(report.checks,{name=c.name,passed=not not ok,seen=seen,final_life=life(),final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('baam.form')) or 0})
  print('BAAM '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));os.remove('../../characters/baam/runtime-validation.json');jsonEncode(report,'../../characters/baam/runtime-validation.json');index=index+1;tick=0
 end
end)
