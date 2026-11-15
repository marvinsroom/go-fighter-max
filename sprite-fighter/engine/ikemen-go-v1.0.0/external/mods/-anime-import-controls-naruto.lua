local cases=jsonDecode('../../characters/naruto/import-test-cases.json')
local commands=jsonDecode('../../characters/naruto/import-test-commands.json')
local index,tick,total,shot=1,0,0,0
local pending=nil
local seen,forms,damage,air,startx={}, {},0,false,0
local report={status='Running',method='Original command routes through test-only AssertCommand, production data unchanged',capture_directory='import-controls-20261024164301',checks={},frames={}}
local function save() jsonEncode(report,'../../characters/naruto/runtime-validation.json') end
local function command(name,value) for i,n in ipairs(commands) do if n==name then mapSet('import.command'..(i-1),value) end end end
hook.add('loop','anime-import-controls',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local file=io.open('../../characters/naruto/replays/import-controls-20261024164301/Anime_controls'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);shot=shot+1;pending=nil;save() else return end
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 tick=tick+1;total=total+1
 if tick==1 then
  seen={};forms={};damage=0;air=false
  for _,name in ipairs(commands) do command(name,0) end
  mapSet('import.input',0);mapSet('import.close',c.close and 1 or 0);mapSet('import.initialform',c.form or 0);mapSet('import.initialchakra',c.chakra or 1000);changeState(990900);setLife(1200);setPower(c.meter or 3000)
  player(2);setLife(1000);changeState(990901);player(1)
 end
 if tick==19 then startx=posX() end
 if tick==20 then
  for _,name in ipairs(c.commands or {}) do command(name,1) end
  for _,name in ipairs(c.held or {}) do command(name,1) end
  mapSet('import.input',c.input or 0)
 end
 if tick==23 then for _,name in ipairs(c.commands or {}) do command(name,0) end end
 if tick==(c.hold_until or 70) then for _,name in ipairs(c.held or {}) do command(name,0) end;mapSet('import.input',0) end
 if tick>=20 then
  seen[tostring(stateNo())]=true;forms[tostring(var(2))]=true;air=air or posY()<-1
  player(2);damage=math.max(damage,1000-life());player(1)
 end
 if tick==30 or tick==90 or tick==170 or tick==600 or tick==1000 or tick==c.length-1 then
  pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),form=var(2),power=power(),chakra=var(5),damage=damage,file='Anime_controls'..string.format('%03d',shot)..'.png'};screenshot()
 end
 if tick>=c.length then
  local ok=true
  if c.state and not seen[tostring(c.state)] then ok=false end
  if c.forbid and seen[tostring(c.forbid)] then ok=false end
  if c.result_form and not forms[tostring(c.result_form)] then ok=false end
  if c.damage and damage<=0 then ok=false end
  if c.air and not air then ok=false end
  if c.move and math.abs(posX()-startx)<2 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,states_seen=seen,forms_seen=forms,damage=damage,final_state=stateNo(),final_form=var(2),airborne=air});index=index+1;tick=0;save()
 end
end)
