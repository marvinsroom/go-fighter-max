
local cases={{["name"]="Seven Shadows ultimate hit",["pulse"]=18,["state"]=7920,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["damage"]=true,["require"]=7921},{["name"]="Seven Shadows ultimate blocked",["pulse"]=18,["state"]=7920,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["guard"]=true,["forbid"]=7921},{["name"]="Seven Shadows ultimate misses",["pulse"]=18,["state"]=7920,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["far"]=true,["forbid"]=7921},{["name"]="Seven Shadows ultimate insufficient meter",["pulse"]=18,["state"]=nil,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["meter"]=2999,["forbid"]=7920},{["name"]="Seven Shadows ultimate empty meter",["pulse"]=18,["state"]=nil,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["meter"]=0,["forbid"]=7920},{["name"]="Seven Shadows ultimate interrupted",["pulse"]=18,["state"]=7920,["length"]=460,["capture"]=true,["recover"]=true,["garden"]=true,["interrupt"]=true,["forbid"]=7921}}
local index,tick,total,shot=1,0,0,0
local seen,minLife,pending={},1000,nil
local seenAnimations={}
local minPower,maxPower,sufferedHit=3000,0,false
local report={runtime={["AI.cns"]="6f1a9cb8241d0df07df0bf6b2aa93892f8562d223ad0f0a299b000e655d8dced",["Atomic.cns"]="d10469f6c85c62af0593d4f7e995724fb556bb887951967ba66694d1e568d8c6",["Cid.air"]="7ce6bf9cc1a5dd0de626deb7a04c18d984e8f0e872dabdbbbe273235ab054cbb",["Cid.cmd"]="ef3ef54d23689a53b708db8e108afa1e60bb0099254615c54dc4bcdac432bebe",["Cid.cns"]="fc5f2eccd683c3d6a5d842f98a0b231bfcc98854b189fcc0e9ca6336615e49e3",["Cid.sff"]="a3361f149aa2597c1ba9f42c8a45f3636c75293e0237decec37d3f413984e9f9",["cid_garden.cns"]="d751378daa48d271cfdb60cbbbf3a8a5857d348fe9d119a0848330a81a1faf75",["cid_shadow.def"]="782a3c129dcddc4f683b7cf2bf55dc2641f879f21e1181ca68796d835cc2e07e",["cid_summons.cns"]="470ec9da2e6900eed5eae9265951fadeb8929ee270b924d26842d33088c88885",["cid_taunt.cns"]="9c11839174f54c856dc5fefd27ffa78fc117933e7ae632eb183cb3d7668a9fd8",["Fx.cns"]="447b89aaabd7742eabf39e2e8fc715a5cbd1754e62f955843983e29e64e4035a",["Normal Skill.cns"]="d99afa1475dfb20ca38ace292f1aa883e992acd5a79300370a861d1aa140a2b7",["Skills.cns"]="b6b2e436438ca93e65eead4a1a6756faa02d68babe3cb0008277d62fb66f4556"},method='Native engine; creator command routes through AssertCommand',capture_directory='garden-v1-final-checked',checks={},frames={}}
hook.add('loop','cid-reference-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/cid/runtime-garden.json');print('CID_REFERENCE_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local path='../../characters/cid/replays/garden-v1-final-checked/Cid_reference'..string.format('%03d',shot)..'.png'
  local f=io.open(path,'rb');if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1;total=total+1
 if tick==1 then
  seen={};seenAnimations={};minLife=c.targetLow and 250 or 1000;minPower=3000;maxPower=0;sufferedHit=false
  player(1);mapSet('cid.pulse',0);mapSet('cid.walk',0);mapSet('cid.walkback',0);mapSet('cid.down',0);mapSet('cid.jump',0);mapSet('cid.jumpdir',c.jumpdir or 0);changeState(99000);setLife(c.lowLife and 400 or 1000);setPower(c.meter or 3000)
  if c.garden then for a=0,6 do mapSet('garden.actor'..a,0) end;mapSet('garden.blackout',0);mapSet('garden.finish',0) end
  player(2);mapSet('test.guard',0);mapSet('test.down',0);changeState(9000)
 elseif tick==8 then player(2);setLife(c.targetLow and 250 or 1000);mapSet('test.guard',c.guard and 1 or 0)
  if c.far then changeState(9002) end
 elseif tick==20 then
  player(1);if c.pulse then mapSet('cid.pulse',c.pulse) end
  if c.walk then mapSet('cid.walk',1) end
  if c.walkback then mapSet('cid.walkback',1) end
  if c.down then mapSet('cid.down',1) end
  if c.jump then mapSet('cid.jump',1) end
 end
 if tick==24 then player(1);mapSet('cid.jump',0) end
 if tick==((c.summon or c.garden) and 32 or 70) and c.interrupt then player(2);changeState(200) end
 if tick==(c.release or 110) then player(1);mapSet('cid.walk',0);mapSet('cid.walkback',0);mapSet('cid.down',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;seenAnimations[tostring(anim())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());if life()<1000 then sufferedHit=true end;player(2);minLife=math.min(minLife,life()) end
 if c.capture and tick>10 and not pending and tick%(c.length>1000 and 24 or 12)==0 then
  player(1);local state,animation,powerNow=stateNo(),anim(),power()
  screenshot();player(2)
  pending={index=shot+1,tick=total,case_tick=tick,case_name=c.name,state=state,animation=animation,power=powerNow,target_life=life()}
  if c.garden then pending.target_state=stateNo();player(1);pending.blackout=numExplod(7940);pending.actors={};for a=0,6 do table.insert(pending.actors,tonumber(map('garden.actor'..a)) or 0) end;pending.finish=tonumber(map('garden.finish')) or 0 end
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=true
  if c.state and not seen[tostring(c.state)] then ok=false end
  if c.requireAnimation and not seenAnimations[tostring(c.requireAnimation)] then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.forbid and seen[tostring(c.forbid)] then ok=false end
  if c.recover and final~=0 then ok=false end
  if c.keepPower and (minPower~=c.keepPower or maxPower~=c.keepPower) then ok=false end
  if c.interrupt and (not sufferedHit or not seen['5000']) then ok=false end
  local damage=(c.targetLow and 250 or 1000)-minLife
  player(2);local targetFinal=stateNo();player(1)
  if c.damage and damage<=0 then ok=false end
  if c.summon and not c.forbid and minPower>2000 then ok=false end
  if c.summon and c.forbid and minPower~=(c.meter or 3000) then ok=false end
  if c.guard and c.summon and (damage<=0 or damage>=100) then ok=false end
  if c.far and damage~=0 then ok=false end
  local actors={};if c.garden then
   for a=0,6 do table.insert(actors,tonumber(map('garden.actor'..a)) or 0) end
   if c.damage then
    if damage~=520 or minPower~=0 or map('garden.blackout')~=1 or map('garden.finish')~=1 then ok=false end
    for _,v in ipairs(actors) do if v~=1 then ok=false end end
   end
   if c.guard and damage~=2 then ok=false end
   if c.meter and minPower~=c.meter then ok=false end
   if numExplod(7940)~=0 then ok=false end
   if targetFinal==7929 or targetFinal==7949 then ok=false end
   if map('garden.helpers')~=0 then ok=false end
  end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,final_state=final,target_final_state=targetFinal,seen=seen,animations=seenAnimations,min_power=minPower,max_power=maxPower,suffered_hit=sufferedHit,garden_actors=actors,blackout=tonumber(map('garden.blackout')) or 0,finish=tonumber(map('garden.finish')) or 0})
  print('CID_REFERENCE '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  jsonEncode(report,'../../characters/cid/runtime-garden.json');index=index+1;tick=0
 end
end)
