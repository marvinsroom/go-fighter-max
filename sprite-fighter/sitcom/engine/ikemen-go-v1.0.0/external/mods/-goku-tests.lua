local cases={{["name"]="Intro - base Goku greeting",["form"]=0,["direct"]=190,["state"]=190,["expectForm"]=0,["meter"]=3000,["length"]=340,["intro"]=true,["category"]="Intro",["energy"]=false}}
local index,tick,shot=1,0,0
local guardSeen,hurtAnim,guardAnim=false,nil,nil
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["common1.cns"]="dabc9da15fbf1d63f11caa728753dc97b94d3e4be1c8f5e7afa6d4270e72810f",["goku-roster.cns"]="3b955475dc0254aa4a84afa5ea1b18de534fb04a1b077c372ce570e386da34e4",["Goku.air"]="685494c4ae400eda628a950c8809d8ed1f46419a0c22f0617ee25dd8551deccf",["Goku.cmd"]="c642ac3a2987096b181d3ef717d15a8650e1235e3448fbfe0bd705857932ce98",["Goku.cns"]="352b233d704f5ff1134e12913321e2772943576732544f6251afc24ebc684651",["Goku.def"]="cb669fa248f6ac5117116d4343a92bcf1099224369cf5452371c1b1c7f1ddcea",["Goku.sff"]="a213cecc2d80f09fda99dcbe3e43eb12beddedb46bcdbe21e05da417ed2726cd",["Goku.snd"]="d963a5b078c85f36bf65e21e5960047bf7de532300d93267ea442bfebcbe2c29",["IA.cns"]="27c38ce0a90a48be1fcedc983bb88229b2c51edbdeca0dd60688d66ecf16309f",["MG.cns"]="bb538240797467868ee301c2314232ffd8d5a7d65963cad5d3cea0e7cb9fba6b",["Specials.cns"]="91cd029202837c25af3edaf71e2220d5d36f8b33c1d4582f29738c70e74295f8",["SS.cns"]="c9b0cca7e2c1c507ac8574b8c72705000f3848fb47dee326e41251cb6dde1568",["SS2.cns"]="655e058f356a842c45a30270e41aff4fe6f22e8c24a607ffd0c7fdd5392164c0",["SS3.cns"]="312dc3014fd55f455e5a4f68608ba33af2c7ce98b4bb885e5e35e72c29c6c858",["SSG.cns"]="cdfb663793fdeea4e3e9e1ac77ce210c87203d57a7f0b1eb078a1fa66ccfbd1e",["SSGSS.cns"]="4fe24925a7a632d9dc5c89b4b544f5103d6fa1cc9bff999009a6a3ea06efd0e2",["Supers.cns"]="a045ba24c996ccb7b7daa2bbb4df26bbbc45e650ca5b1ae0133d3bc26c111a85"},status='Running',checks={},frames={},capture_directory='gallery-intro-20261019102143-0'}
hook.add('loop','goku-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/goku/runtime-validation.json');print('GOKU_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/goku/replays/gallery-intro-20261019102143-0/Goku_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Goku_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};guardSeen=false;hurtAnim=nil;guardAnim=nil;caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('goku.form',c.form or 0);mapSet('test.charge',0);mapSet('test.bomb',0);mapSet('test.guard',0);mapSet('test.reaction',(c.hurt or c.defend) and 1 or 0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*(c.targetDistance or 55))*4);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(1);setPower(c.meter or 3000);player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end;if c.gather then mapSet('test.bomb',1) end
 end
 if c.gather and tick==700 then player(1);mapSet('test.bomb',0) end
 if c.gather and tick==750 then player(1);mapSet('test.pulse',c.pulse) end
 if c.combo and tick>24 and tick<150 and tick%6==0 then player(1);mapSet('test.pulse',c.pulse) end
 if c.counter and tick==60 then player(2);selfState(9003);player(1) end
 if c.hurt and tick==60 then player(1);setPower(0);player(2);selfState(9004);player(1) end
 if c.defend and tick==50 then player(1);mapSet('test.guard',1) end
 if c.defend and tick==60 then player(1);setPower(0);player(2);selfState(9004);player(1) end
 if c.defend and tick==100 then player(1);mapSet('test.guard',0) end
 if c.interrupt and tick==60 then player(2);selfState(9004);player(1) end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==39 and c.air and c.forbid then player(1);setPower(c.meter) end
 if tick==40 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;local aid=anim()%1000000;if c.hurt and ((aid>=5000 and aid<=5300) or (aid>=6000 and aid<=6300) or (aid>=12000 and aid<=12300) or (aid>=14000 and aid<=14300) or (aid>=16000 and aid<=16300) or (aid>=18000 and aid<=18300)) then hurtAnim=anim() end;if c.defend and ((aid>=120 and aid<=152) or (aid>=2120 and aid<=2152) or (aid>=11120 and aid<=11152) or (aid>=13120 and aid<=13152) or (aid>=15120 and aid<=15152) or (aid>=17120 and aid<=17152)) then guardAnim=anim() end;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life());if stateNo()>=120 and stateNo()<=155 then guardSeen=true end end
 player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))
 if c.capture~=false and tick>10 and not pending and ((c.energy and caseShots<96 and tick%3==0 and stateNo()~=0) or (c.intro and tick%2==0) or (caseShots<10 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<24 and tick%math.max(12,math.floor(c.length/16))==0) or tick==12 or tick==c.length-4) then
 lastKey=key
  caseShots=caseShots+1;player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),animation_element=animElemNo(0),power=power(),form=tonumber(map('goku.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=-1,drawing=-1,facing=facing(),fx_count=numExplod(879100),fx_x=tonumber(map('goku.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=-1;pending.target_drawing=-1;pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('goku.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.guard and not guardSeen then ok=false end
  if c.interrupt and numExplod(960810)>0 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,guarded=guardSeen,hurt_animation=hurtAnim,guard_animation=guardAnim,charge_aura=numExplod(960810),seen=seen,final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('goku.form')) or 0})
  print('GOKU '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/goku/runtime-validation.json');index=index+1;tick=0
 end
end)
