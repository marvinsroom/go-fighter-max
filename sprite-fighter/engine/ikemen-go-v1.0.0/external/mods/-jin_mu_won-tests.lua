local cases={{["name"]="Z Z Z",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=1},{["tick"]=52,["pulse"]=1}},["requireStates"]={200,210,220},["minDamage"]=140,["facing"]=1,["length"]=220},{["name"]="Z Z Z facing left",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=1},{["tick"]=52,["pulse"]=1}},["requireStates"]={200,210,220},["minDamage"]=140,["facing"]=-1,["length"]=220},{["name"]="X X X",["pulse"]=2,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=53,["pulse"]=2}},["requireStates"]={230,240,250},["minDamage"]=170,["facing"]=1,["length"]=220},{["name"]="X X X facing left",["pulse"]=2,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=53,["pulse"]=2}},["requireStates"]={230,240,250},["minDamage"]=170,["facing"]=-1,["length"]=220},{["name"]="Z X C",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=52,["pulse"]=3}},["requireStates"]={200,230,260},["minDamage"]=160,["facing"]=1,["length"]=220},{["name"]="Z X C facing left",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=52,["pulse"]=3}},["requireStates"]={200,230,260},["minDamage"]=160,["facing"]=-1,["length"]=220},{["pulse"]=4,["state"]=1000,["rawdir"]=0,["length"]=250,["counter"]=false,["name"]="Drawing Cut",["facing"]=1,["damage"]=true,["require"]=nil,["minDamage"]=1,["capture"]=true},{["pulse"]=5,["state"]=1100,["rawdir"]=3,["length"]=250,["counter"]=false,["name"]="Silent Step",["facing"]=1,["damage"]=true,["require"]=nil,["minDamage"]=1,["capture"]=true},{["pulse"]=6,["state"]=1200,["rawdir"]=1,["length"]=250,["counter"]=true,["name"]="Snow Flower Reversal",["facing"]=1,["damage"]=true,["require"]=1201,["minDamage"]=1,["capture"]=true},{["pulse"]=7,["state"]=1300,["rawdir"]=2,["length"]=250,["counter"]=false,["name"]="Shadow Crescent",["facing"]=1,["damage"]=true,["require"]=nil,["minDamage"]=1,["capture"]=true},{["pulse"]=8,["state"]=2000,["rawdir"]=0,["length"]=250,["counter"]=false,["name"]="Northern Threefold",["facing"]=1,["damage"]=true,["require"]=nil,["minDamage"]=1,["capture"]=true},{["pulse"]=9,["state"]=2100,["rawdir"]=1,["length"]=250,["counter"]=true,["name"]="Iron Wall",["facing"]=1,["damage"]=true,["require"]=2101,["minDamage"]=1,["capture"]=true},{["pulse"]=10,["state"]=2200,["rawdir"]=3,["length"]=250,["counter"]=false,["name"]="Black Horizon",["facing"]=1,["damage"]=true,["require"]=nil,["minDamage"]=1,["capture"]=true},{["pulse"]=11,["state"]=3000,["rawdir"]=0,["length"]=360,["counter"]=false,["name"]="Ten Thousand Shadows",["facing"]=1,["damage"]=true,["require"]=3001,["minDamage"]=600,["capture"]=true},{["pulse"]=11,["state"]=3000,["rawdir"]=0,["length"]=360,["counter"]=false,["name"]="Ten Thousand Shadows facing left",["facing"]=-1,["damage"]=true,["require"]=3001,["minDamage"]=600,["capture"]=true},{["name"]="Entrance",["direct"]=190,["state"]=190,["length"]=170},{["name"]="Quiet Resolve",["pulse"]=12,["state"]=800,["length"]=140},{["name"]="Chain on guard",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=1},{["tick"]=52,["pulse"]=1}},["guard"]=true,["requireStates"]={200,210,220},["maxDamage"]=20,["length"]=220},{["name"]="Ten Thousand Shadows left wall",["pulse"]=11,["state"]=3000,["require"]=3001,["damage"]=true,["minDamage"]=600,["cornerX"]=-50,["facing"]=-1,["length"]=360},{["name"]="Light into ultimate facing left",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=11}},["requireStates"]={200,3000,3001},["minDamage"]=635,["facing"]=-1,["length"]=400},{["name"]="Ten Thousand Shadows right wall",["pulse"]=11,["state"]=3000,["require"]=3001,["damage"]=true,["minDamage"]=600,["cornerX"]=50,["facing"]=1,["length"]=360},{["name"]="Light into ultimate",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=11}},["requireStates"]={200,3000,3001},["minDamage"]=635,["facing"]=1,["length"]=400}}
local index,tick,shot=1,0,0
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["jin_mu_won-common.zss"]="57c9841096b29c39d1f7489ad14a7c094c5ac21adcd31c3f5a36a619ebb98f0a",["jin_mu_won.air"]="07b435c1ac90dee3814e9d0be4d4db705c7787c7cd0fdd54c29a9a52db814d43",["jin_mu_won.cmd"]="f95305a9e11d6526d914772a9551b5a24f589b58e6dbaf05c273de72c034cc05",["jin_mu_won.cns"]="5d512b3144aed6ea76a8bdfeece4b423b15e80a3e1b35c13cc8cecc6dc79083e",["jin_mu_won.def"]="19b3098714bfb06dfcc2ef595f0f88936cb6cd4f6a3c6e9c24ad504240cca63a",["jin_mu_won.sff"]="57f3e5241fe21adcb5e1ff49e3c5f36928d28766598d11d9461f6c188544dfdb",["jin_mu_won.snd"]="87ebac912614ad0c3242667f828f12087acb42e40d371eb329ef8a014e83f858"},status='Running',checks={},frames={},capture_directory='presentation-v20261021160000'}
hook.add('loop','jin-mu-won-tests',function()
 if not player(1) then return end
 if roundState()<2 and (stateNo()==190 or stateNo()==191) then report.natural_intro_seen=true end
 if roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  os.remove('../../characters/jin-mu-won/runtime-validation.json');jsonEncode(report,'../../characters/jin-mu-won/runtime-validation.json');print('JIN_MU_WON_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/jin-mu-won/replays/presentation-v20261021160000/JinMuWon_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='JinMuWon_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('jin-mu-won.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.inputdir',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
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
 if c.capture~=false and tick>10 and caseShots<40 and not pending and ((stateNo()~=0 and tick%4==0 and (key~=lastKey or tick%16==0)) or tick==12 or tick==c.length-4) then
 lastKey=key;caseShots=caseShots+1
  player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),power=power(),form=tonumber(map('jin-mu-won.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=spriteVar('group'),drawing=spriteVar('image'),facing=facing(),cinematic_tick=time(),companion_count=numExplod(9113),beam_count=numExplod(9112),fx_count=numExplod(9108)+numExplod(9109)+numExplod(9110)+numExplod(9111)+numExplod(9112)+numExplod(9113)+numExplod(9114)+numExplod(9115),fx_x=tonumber(map('jin-mu-won.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=spriteVar('group');pending.target_drawing=spriteVar('image');pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  if c.forbid and c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('jin-mu-won.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
 if c.minDamage and 1000-minLife<c.minDamage then ok=false end
 if c.maxDamage and 1000-minLife>c.maxDamage then ok=false end
 for _,s in ipairs(c.requireStates or {}) do if not seen[tostring(s)] then ok=false end end
 if c.hurt and life()>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if (targetFinal==3050 or targetFinal==3051 or targetFinal==3052) then ok=false end
  table.insert(report.checks,{name=c.name,passed=not not ok,seen=seen,final_life=life(),final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('jin-mu-won.form')) or 0})
  print('JIN_MU_WON '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));os.remove('../../characters/jin-mu-won/runtime-validation.json');jsonEncode(report,'../../characters/jin-mu-won/runtime-validation.json');index=index+1;tick=0
 end
end)
