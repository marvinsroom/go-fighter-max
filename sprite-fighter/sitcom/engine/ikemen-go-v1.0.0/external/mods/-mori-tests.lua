local function encode(v)
 local t=type(v)
 if t=='nil' then return 'null' end
 if t=='boolean' or t=='number' then return tostring(v) end
 if t=='string' then return '"'..v:gsub('\\','\\\\'):gsub('"','\\"'):gsub('\n','\\n'):gsub('\r','\\r')..'"' end
 if t=='table' then
  local r={};local array=#v>0
  if array then for i=1,#v do r[#r+1]=encode(v[i]) end
  else for k,item in pairs(v) do r[#r+1]=encode(tostring(k))..':'..encode(item) end end
  return (array and '[' or '{')..table.concat(r,',')..(array and ']' or '}')
 end
 error('Unsupported report value '..t)
end
local function saveReport(v,path) os.remove(path);local f=assert(io.open(path,'w'));f:write(encode(v));f:close() end
local cases={{["name"]="Monkey King",["pulse"]=10,["state"]=4500,["length"]=240,["damage"]=true,["counter"]=false,["require"]=4501,["minDamage"]=500,["rawdir"]=0},{["name"]="Monkey King facing left",["pulse"]=10,["state"]=4500,["length"]=240,["damage"]=true,["counter"]=false,["require"]=4501,["minDamage"]=500,["facing"]=-1,["rawdir"]=0},{["name"]="Entrance",["direct"]=190,["state"]=190,["length"]=180,["rawdir"]=0},{["name"]="Transform into Monkey King",["pulse"]=15,["state"]=980500,["expectForm"]=1,["length"]=180,["rawdir"]=0},{["name"]="Return to Jin Mori",["pulse"]=15,["state"]=980500,["form"]=1,["expectForm"]=0,["length"]=180,["rawdir"]=0},{["name"]="Z Z Z chain",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=1},{["tick"]=52,["pulse"]=1}},["requireStates"]={230,240,250},["minDamage"]=140,["damage"]=true,["length"]=240,["rawdir"]=0},{["name"]="X X X chain",["pulse"]=2,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=53,["pulse"]=2}},["requireStates"]={270,280,290},["minDamage"]=190,["damage"]=true,["length"]=240,["rawdir"]=0},{["name"]="Z X C chain",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=52,["pulse"]=3}},["requireStates"]={230,260,310},["minDamage"]=160,["damage"]=true,["length"]=240,["rawdir"]=0},{["name"]="Normal to Azure Dragon",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=52,["pulse"]=6}},["requireStates"]={230,260,2000},["minDamage"]=350,["damage"]=true,["length"]=300,["rawdir"]=0},{["name"]="Monkey King Z X C chain",["pulse"]=1,["inputs"]={{["tick"]=36,["pulse"]=2},{["tick"]=52,["pulse"]=3}},["requireStates"]={230,260,310},["minDamage"]=160,["length"]=240,["form"]=1,["expectForm"]=1,["rawdir"]=0},{["name"]="Monkey King ultimate",["pulse"]=10,["state"]=4500,["require"]=4501,["minDamage"]=500,["length"]=240,["form"]=1,["expectForm"]=1,["rawdir"]=0}}
local index,tick,shot=1,0,0
local caseShots,lastKey=0,''
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={runtime_sha256={["1.act"]="4a10e2a4d6de9fc9d25a82e1d30f763e0c6724f6975ff2744729223a020213fd",["common1.cns"]="88f45a78e99c7f2aeab3cc0bbce76384fd8d766ece864422f87a95540be63107",["Jin Mori.cns"]="ed204ef1c66b8fa4065f7bc2b8248054d19157e25107bf9b9280abb4ebba5c60",["Jin Mori.snd"]="2b0e2f8009cee53a727cf40c560b311d32092e6e46bee2b543609ae1b6301d8d",["jin_mori.air"]="f38246d31ce2744917277e334a66c11cc335e4e8ea0c9ddde8b76ddeb3858e45",["jin_mori.cmd"]="e492b924711c7574b5c8924a7568b25107511e7d897fd5b39521a5641c995a05",["jin_mori.def"]="06d1f79910e76e68d612838cb9949933caaf52c9d8472c0b82d9b06ce1ff6d46",["jin_mori.sff"]="abb6e0f54f356d36a78b4855b6faccd0b3e5be5c05c76b33d3b9a8a14a55dc4d"},status='Running',checks={},frames={},capture_directory='comic-20261021105435-presentation'}
hook.add('loop','jin-mori-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  saveReport(report,'../../characters/jin-mori/runtime-validation.json');print('MORI_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/jin-mori/replays/comic-20261021105435-presentation/Mori_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Mori_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};caseShots=0;lastKey='';minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('mori.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.inputdir',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',((c.cornerX or -25)+(c.facing or 1)*40)*(1280/192));mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if c.inputs then for _,input in ipairs(c.inputs) do if tick==input.tick then player(1);mapSet('test.pulse',input.pulse) end end end
 if c.probe and tick==c.probe then player(2);selfState(9004) end
 if tick==18 then player(1);mapSet('test.inputdir',c.rawdir or 0) end
 if tick==60 and c.counter then player(2);selfState(9004) end
 if tick==24 then player(1);mapSet('test.inputdir',0) end
 if tick==60 and c.counter then player(2);selfState(9004) end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==28 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(minLife)
 if c.capture~=false and tick>10 and caseShots<(c.pulse==10 and 60 or 32) and not pending and ((stateNo()~=0 and tick%4==0 and (stateNo()==980500 or key~=lastKey or tick%16==0)) or tick==12 or tick==c.length-4) then
 lastKey=key;caseShots=caseShots+1
  player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),power=power(),form=tonumber(map('mori.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=spriteVar('group'),drawing=spriteVar('image'),facing=facing(),fx_count=numExplod(879100),fx_x=tonumber(map('jin-mori.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=spriteVar('group');pending.target_drawing=spriteVar('image');pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and (final==0 or final==11)
  if c.forbid and c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('mori.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.minDamage and 1000-minLife<c.minDamage then ok=false end
  if c.maxDamage and 1000-minLife>c.maxDamage then ok=false end
  for _,s in ipairs(c.requireStates or {}) do if not seen[tostring(s)] then ok=false end end
  if c.hurt and life()>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=not not ok,seen=seen,final_life=life(),final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('mori.form')) or 0})
  print('MORI '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));saveReport(report,'../../characters/jin-mori/runtime-validation.json');index=index+1;tick=0
 end
end)
