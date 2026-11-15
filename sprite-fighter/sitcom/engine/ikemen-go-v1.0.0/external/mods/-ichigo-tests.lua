local cases={{["name"]="Intro - school uniform into Bankai",["form"]=0,["direct"]=190,["state"]=191,["expectForm"]=2,["meter"]=10000,["length"]=280,["intro"]=true}}
local index,tick,shot=1,0,0
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["Bankai.cns"]="fa91c6e437eaa1f10983d05ba7fd7613378252b1519c54d62063f5de0ffd714d",["Clash.cns"]="f31165a2ba5fe2ca61909bc84776d5a0d441322beab718208ed0c1a78664c19d",["common1.cns"]="5679f44a2fbd546c92b98edebcd1aaf0f2e6845ebd10202317ffc9e8e09a31aa",["Especiales.cns"]="c5ec8c9d5e9aeadff1c6d96ddc9d0326c786bb198f6391356dc53cb8978403aa",["HalfMask.cns"]="6f461b26139e56213fdc8fb95be72bbb59657a404cd4b2b95d660ddbb7a3b382",["IA.cns"]="dfdb90553c7dacb9bcfa2c6c5d03409f20a0d20f03fab9b4b6a948f28373e71c",["ichigo-main.cns"]="00393ab0a915b1a1bd4de17e29871d5a37e31af29662df2ee068526ab99ba7b1",["ichigo-roster.cns"]="5ec76f5079b01e28bc133f360684bfae1b64588add0ff5bbb327c73b23a78c03",["Ichigo.air"]="18d70b31b75f189e98800b8c660202abfc1f1ee7db0789f5d0bdb884c22759a3",["Ichigo.cmd"]="19d082af2c65be88fb41c75ad06d049386dd4cfe4cb655ab63174724bfdd131c",["Ichigo.cns"]="741ebcebc83b2f9447ddaff93c65746657b7c7eca3b23d0034c691f8e03e5965",["Ichigo.def"]="7cad5c013fdbaa6002a2c92af91123aa9726459720949068cc8cf660d6748a8c",["Ichigo.sff"]="b51dab4f4d3762bb405f8de7f8894d11003b53b9c37f75955d57c558983919cd",["Ichigo.snd"]="a5deb5014b88d130e06698d255cbadb212569e55769f40ccbe4bbd052463cd49",["Mask.cns"]="b6c3961d4b8fe80afb61aa33bfd5f79e72836f28ff6c78397b9d8e383cd7d2ca",["Mugetsu.cns"]="dcc1960fe48e566d9d5247fb3933ebb2a8e32ce90e4c5a7184b3ce42ce142355",["Supers.cns"]="d8959ba3f010cdad2ca170802673874756c80256f220cac82bd6fd87ea08e43a",["TYBW.cns"]="7841cb44808d4f3fd2a5956a6aeb67754ff5ddbf18d39a7d9349f48a2ac0f7b8",["Vaste Lord.cns"]="7bdb17f5d137adbb6402d6839e3f3c1ce3176132d3faaa5627b74aed747e7ee7",["Vasto Lorde.cns"]="49a3a99132d136d8220094d79b70e629d699725472f60abeecd350fbaae44519"},status='Running',checks={},frames={},capture_directory='intro-school-v4'}
hook.add('loop','ichigo-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/ichigo/runtime-validation.json');print('ICHIGO_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/ichigo/replays/intro-school-v4/Ichigo_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Ichigo_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 10000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('ichigo.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 10000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*55)*4);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(1);setPower(c.meter or 10000);player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==40 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))
 if c.capture~=false and tick>10 and not pending and ((c.intro and tick%4==0) or (caseShots<8 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<18 and tick%math.max(12,math.floor(c.length/12))==0) or tick==12 or tick==c.length-4) then
 lastKey=key
  caseShots=caseShots+1;player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),animation_element=animElemNo(0),power=power(),form=tonumber(map('ichigo.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=-1,drawing=-1,facing=facing(),fx_count=numExplod(879100),fx_x=tonumber(map('ichigo.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=-1;pending.target_drawing=-1;pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  if c.forbid and c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('ichigo.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,seen=seen,final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('ichigo.form')) or 0})
  print('ICHIGO '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/ichigo/runtime-validation.json');index=index+1;tick=0
 end
end)
