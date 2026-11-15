local cases={{["name"]="Intro - funny meat gag (base Luffy)",["form"]=0,["direct"]=190,["state"]=190,["expectForm"]=0,["meter"]=3000,["length"]=340,["intro"]=true,["category"]="Intro"}}
local index,tick,shot=1,0,0
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["common1.cns"]="005b32af1a74eca1e1a57545f0482794db1eff43aa2cf97054e5900f99524d30",["Especiales.cns"]="971d62e36e86322ca72f6c49b5dc543d5546aeb306921a391b39215c971d4b89",["Gear 5.cns"]="807fb0f8a5346dcc7ba05306142bb787e30f2de6af9450dc3ebe2ea1fbee755e",["IA.cns"]="ee07da50fcec791da9f459d54908f1993f728dce95e070c4c0cfd98e57c76159",["luffy-roster.cns"]="6c9ad9f032fa75f36b6a5e82f9866ed346500e455b285f359b62b6590ecf1f5c",["luffy.def"]="596e0ac9e951d8ac44db29bcdeecd1acea98c8ab1f580e26cb7bb1196c37531d",["Luffy.sff"]="8a101dd39ba1db99f4b21aab9dd7f271f247a921d9222ba5196341e1b0b7da2c",["Nightmare.cns"]="92c1201f8fd20d1d94b9d51428df990d6565beb57cbc3789295a8d02ce7420a2",["SnakeMan.cns"]="38fe49e9dd06ed38471346aa433e17cc5ec17b745c88544d1162cd863abcd000",["Supers.cns"]="99805b94237fbc66c3daa60db29c452f17475e26cea8917d74837fe16be35c7f",["TC_Luffy_All_Forms.air"]="58c86f80c937e4f70142dd28df0899943c501154f30f9048326fe3bac530cdf6",["TC_Luffy_All_Forms.cmd"]="9b5249b843b73d5ef990a8b3f9ff75fd97d56c2d8a2881eedbf4299f4f1927f2",["TC_Luffy_All_Forms.cns"]="14177199fcf64515a618cb6179872e1ce96b96b07b7e4f61449e1b41121e546e",["TC_Luffy_All_Forms.def"]="6b71c82da3e5986c7ec7ffbc7869710d2a88e7054b94f3966a762f2482f63d1c",["TC_Luffy_All_Forms.sff"]="7b409b85ccdcaf9af54f49f65bc910804fb67c969e1cad947fd786bf52cf4130",["TC_Luffy_All_Forms.snd"]="5539d24025913be4558d0f5bc8fe107253bb4f7545c92610b7449074fefadb6c"},status='Running',checks={},frames={},capture_directory='gallery-intro-20261018205445'}
hook.add('loop','luffy-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/luffy/runtime-validation.json');print('LUFFY_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/luffy/replays/gallery-intro-20261018205445/Luffy_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Luffy_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('luffy.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*85)*4);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(1);setPower(c.meter or 3000);player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==40 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))
 if c.capture~=false and tick>10 and not pending and ((c.intro and tick%4==0) or (caseShots<10 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<24 and tick%math.max(12,math.floor(c.length/16))==0) or tick==12 or tick==c.length-4) then
 lastKey=key
  caseShots=caseShots+1;player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),animation_element=animElemNo(0),power=power(),form=tonumber(map('luffy.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=-1,drawing=-1,facing=facing(),fx_count=numExplod(879100),fx_x=tonumber(map('luffy.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=-1;pending.target_drawing=-1;pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('luffy.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,seen=seen,final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('luffy.form')) or 0})
  print('LUFFY '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/luffy/runtime-validation.json');index=index+1;tick=0
 end
end)
