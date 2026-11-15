local cases={{["name"]="Intro - GT Kid Goku greeting",["form"]=0,["direct"]=190,["state"]=190,["expectForm"]=0,["meter"]=3000,["length"]=340,["intro"]=true,["category"]="Intro",["energy"]=false}}
local index,tick,shot=1,0,0
local guardSeen,hurtAnim,guardAnim=false,nil,nil
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["common1.cns"]="df98e370f2797d2854b7214844f703a863e1a644427cd6b3d73b7fe299088d5c",["Especiales.cns"]="4d5f06a95c8bd9fd29614bc2a7766cf31323a2aca047748e476ab2c0796fafd1",["goku-roster.cns"]="7345661fa9acdf3b76113d64d255f9bbc3cea125b65b5b29cb099c70104797df",["GokuGT.air"]="973059c51d4277523b1134ff4ef72db8fc2fd9b1a0a62ffe12a95e625c3042d8",["GokuGT.cmd"]="a95b20c034b920a9e407449d2609c7c98bd98d9d6638f0e90f962c291c4bcea0",["GokuGT.cns"]="5c797b6bcf0a1439cbd090f173179bc61402745c68b0d62ce9cfe2eba79dc173",["GokuGT.def"]="776b6a9939e82ebdec6a229b3bf0e1054bc066b8855533c44065d461a4fc19ce",["GokuGT.sff"]="1c932ab126bf8707dd96945fc8903a560fb1298f77c2a1b8874ad1579227b7a6",["GokuGT.snd"]="0c6942c7d3f237a218d5166c87462d721102c98e0ebc1d7882dd80227aa31769",["gt_goku.def"]="01f15ab9bb6b8f1b489190375b402ad03d2c14e6958d15fd9fbbe502e1467b12",["IA.cns"]="fd8db065b8508ecd1757e5a5941079db40fadefd2d3a35e78706c98915a1b21c",["SS1.cns"]="03158a4bd2e5b932fd664e079ee02c9ce43354dd97d752ef08391f532b585f2e",["SS2.cns"]="e659afeec1b319d6df42bf4016225da18255333384c8c540dafd037ad5d1e3aa",["SS3.cns"]="7d17e37414aa91330a551ab6be76ca608277effbba7fddfabbc1fe3821376e04",["SS4.cns"]="5b9096d7aa2ae25c21f88e8f219a9add6839f8cea4ced7882f3d4bbadbf366af",["Supers.cns"]="e793370fd5b4fd20148cf12b8ad28141fcb4268603f0871fcdeacc38b32cb382"},status='Running',checks={},frames={},capture_directory='gallery-intro-20261019093856-0'}
hook.add('loop','goku-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/gt-goku/runtime-validation.json');print('GOKU_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/gt-goku/replays/gallery-intro-20261019093856-0/GT_Goku_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='GT_Goku_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};guardSeen=false;hurtAnim=nil;guardAnim=nil;caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('goku.form',c.form or 0);mapSet('test.charge',0);mapSet('test.bomb',0);mapSet('test.guard',0);mapSet('test.reaction',(c.hurt or c.defend) and 1 or 0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*55)*4);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
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
 if tick==12 and c.lowHealth then player(1);setLife(400);player(2);setLife(400);minLife=400 end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==39 and c.air and c.category=='Basics' then player(2);mapSet('test.distance',c.pulse==3 and 360 or 160);selfState(9006);player(1) end
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
  table.insert(report.checks,{name=c.name,passed=ok,guarded=guardSeen,hurt_animation=hurtAnim,guard_animation=guardAnim,charge_aura=numExplod(960810),seen=seen,final_state=final,target_final_state=targetFinal,damage=(c.lowHealth and 400 or 1000)-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('goku.form')) or 0})
  print('GOKU '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/gt-goku/runtime-validation.json');index=index+1;tick=0
 end
end)
