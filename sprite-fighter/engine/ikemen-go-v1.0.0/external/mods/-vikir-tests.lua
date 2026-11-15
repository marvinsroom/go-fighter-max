local cases={{["name"]="Vikir / Guest Dolores",["form"]=0,["expectForm"]=0,["pulse"]=14,["state"]=2000,["length"]=210,["damage"]=false,["expectSelf"]=920,["guest"]=true},{["name"]="Vikir / Guest Camu",["form"]=0,["expectForm"]=0,["pulse"]=15,["state"]=2010,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Vikir / Guest Aiyen",["form"]=0,["expectForm"]=0,["pulse"]=16,["state"]=2020,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Vikir / Guest Sinclair",["form"]=0,["expectForm"]=0,["pulse"]=17,["state"]=2030,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Night Hound / Guest Dolores",["form"]=1,["expectForm"]=1,["pulse"]=14,["state"]=2000,["length"]=210,["damage"]=false,["expectSelf"]=920,["guest"]=true},{["name"]="Night Hound / Guest Camu",["form"]=1,["expectForm"]=1,["pulse"]=15,["state"]=2010,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Night Hound / Guest Aiyen",["form"]=1,["expectForm"]=1,["pulse"]=16,["state"]=2020,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Night Hound / Guest Sinclair",["form"]=1,["expectForm"]=1,["pulse"]=17,["state"]=2030,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Choco / Guest Dolores",["form"]=2,["expectForm"]=2,["pulse"]=14,["state"]=2000,["length"]=210,["damage"]=false,["expectSelf"]=920,["guest"]=true},{["name"]="Choco / Guest Camu",["form"]=2,["expectForm"]=2,["pulse"]=15,["state"]=2010,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Choco / Guest Aiyen",["form"]=2,["expectForm"]=2,["pulse"]=16,["state"]=2020,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Choco / Guest Sinclair",["form"]=2,["expectForm"]=2,["pulse"]=17,["state"]=2030,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Academy / Guest Dolores",["form"]=3,["expectForm"]=3,["pulse"]=14,["state"]=2000,["length"]=210,["damage"]=false,["expectSelf"]=920,["guest"]=true},{["name"]="Academy / Guest Camu",["form"]=3,["expectForm"]=3,["pulse"]=15,["state"]=2010,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Academy / Guest Aiyen",["form"]=3,["expectForm"]=3,["pulse"]=16,["state"]=2020,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Academy / Guest Sinclair",["form"]=3,["expectForm"]=3,["pulse"]=17,["state"]=2030,["length"]=210,["damage"]=true,["expectSelf"]=800,["guest"]=true},{["name"]="Guest Camu ranged facing left",["pulse"]=15,["state"]=2010,["range"]=true,["facing"]=-1,["damage"]=true,["length"]=220,["guest"]=true},{["name"]="Guest Aiyen ranged facing left",["pulse"]=16,["state"]=2020,["range"]=true,["facing"]=-1,["damage"]=true,["length"]=220,["guest"]=true},{["name"]="Guest Sinclair ranged facing left",["pulse"]=17,["state"]=2030,["range"]=true,["facing"]=-1,["damage"]=true,["length"]=220,["guest"]=true},{["name"]="Academy / Anubis shot",["form"]=3,["expectForm"]=3,["pulse"]=18,["state"]=1400,["damage"]=true,["length"]=220,["arrow"]=true},{["name"]="Academy / Anubis long range",["form"]=3,["expectForm"]=3,["pulse"]=18,["state"]=1400,["damage"]=true,["length"]=220,["arrow"]=true,["range"]=true},{["name"]="Academy / Anubis facing left",["form"]=3,["expectForm"]=3,["pulse"]=18,["state"]=1400,["damage"]=true,["length"]=220,["arrow"]=true,["facing"]=-1},{["name"]="Academy / Anubis blocked",["form"]=3,["expectForm"]=3,["pulse"]=18,["state"]=1400,["damage"]=false,["length"]=220,["arrow"]=true,["guard"]=true,["max_damage"]=6}}
local index,tick,shot=1,0,0
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["vikir.air"]="32c8fabe0c9af0f088ab1f1e1dfd3bfb8083b231f139b72eaa688fa9eb065a95",["vikir.cmd"]="b3665061501164c0f76cc9adff2fa70b0cb6a1bdf6b2ddd61e4c322f9646bf35",["vikir.cns"]="35c3f37821be747b9eb08504efd455f62ad1f2c18c18a04bd81ae4829ed4963d",["vikir.def"]="7ea4514e34dbdfcf30992d2fc9e3c87cf009abe1cd4a397f2281d311cc6e0c96",["vikir.sff"]="7574852d1275cba0bd48af7f0dbc24b8472b0fbbb101d136b62e3cef5f97414c",["vikir.snd"]="cc7b837e62e64851877d316ad454bfaccb754457fe2d6206f439033b737fd3a4"},status='Running',checks={},frames={},capture_directory='guests-20261021112201'}
hook.add('loop','vikir-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/vikir/runtime-validation.json');print('VIKIR_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/vikir/replays/guests-20261021112201/Vikir_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Vikir_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};firstSeen={};shots=0;lastKey="";maxAura=0;maxGuest=0;maxArrows=0;minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -120);mapSet('test.facing',c.facing or 1);mapSet('vikir.form',c.form or 0);mapSet('test.cooldown',c.cooldown or 0);mapSet('test.key',0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(c.life or 800);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',(c.cornerX or -120)*4+(c.facing or 1)*160);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) elseif c.range then selfState(9006) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if tick==20 and c.key then player(1);mapSet('test.key',c.key);if c.walkback then mapSet('test.walkback',1) end end
 if tick==23 then player(1);mapSet('test.key',0) end
 if tick==25 and c.probe then player(2);changeState(c.probe) end
 for _,event in ipairs(c.chain or {}) do if tick==event.tick then player(1);mapSet('test.pulse',event.pulse) end end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==28 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;if not firstSeen[tostring(stateNo())] then firstSeen[tostring(stateNo())]=tick end;maxAura=math.max(maxAura,var(20));maxGuest=math.max(maxGuest,numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230));maxArrows=math.max(maxArrows,map('guest.projectiles'));minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(life())..':'..tostring(math.floor(tick/4))
 if c.capture~=false and tick>18 and tick%3==0 and shots<((c.walk or c.walkback or c.jump or c.charge or not c.state) and 40 or 40) and tick<175 and key~=lastKey and not pending then
  shots=shots+1;lastKey=key
  player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),power=power(),form=tonumber(map('vikir.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=spriteVar('group'),drawing=spriteVar('image'),facing=facing(),guest_count=numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230),projectiles=map('guest.projectiles'),fx_count=numExplod(8010)+numExplod(8020)+numExplod(8030),fx_x=tonumber(map('vikir.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=spriteVar('group');pending.target_drawing=spriteVar('image');pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local actorOK=not c.guest or (maxGuest>0 and numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230)==0)
 local arrowOK=not c.arrow or maxArrows>0 or minLife<1000
 local final=stateNo();local selfLife=life();local ok=actorOK and arrowOK and (not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and final==0
  if c.forbid and c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
 if c.max_gain and maxPower>(c.meter or 0)+c.max_gain then ok=false end
  if c.expectForm and map('vikir.form')~=c.expectForm then ok=false end
  if c.cinematic and numExplod(8010)+numExplod(8020)+numExplod(8030)>0 then ok=false end
 if c.damage and minLife>=1000 then ok=false end
 if c.max_damage and 1000-minLife>c.max_damage then ok=false end
 if c.min_damage and 1000-minLife<c.min_damage then ok=false end
 if c.requireAura and maxAura==0 then ok=false end
 if c.expectAura and var(20)~=c.expectAura then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
 for _,required in ipairs(c.require_states or {}) do if not seen[tostring(required)] then ok=false end end
 if c.expectSelf and selfLife~=c.expectSelf then ok=false end
 if c.state==3100 and not c.guard and not c.far and selfLife~=855 then ok=false end
 if c.state==3100 and (c.guard or c.far) and selfLife~=800 then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,seen=seen,final_state=final,target_final_state=targetFinal,max_guest=maxGuest,max_projectiles=maxArrows,guest_cleanup=numHelper(7200)+numHelper(7210)+numHelper(7220)+numHelper(7230),state_ticks=firstSeen,self_life=selfLife,aura=var(20),damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('vikir.form')) or 0})
  print('VIKIR '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/vikir/runtime-validation.json');index=index+1;tick=0
 end
end)
