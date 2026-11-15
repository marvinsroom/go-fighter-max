
local moves={{name="movement",length=220},{name="special",pulse=8,length=120},{name="super",pulse=5,length=330},{name="ultimate",pulse=6,length=530}}
local index,tick,shot=1,0,0
local pending=nil
local report={method='Actual native screenshot API with acknowledged image files',frames={}}
hook.add('loop','prince-native-replay',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/prince/replays/native-v1/Chappelle_prince'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=moves[index]
 if not c then jsonEncode(report,'../../characters/prince/native-preview-report.json');print('CHAPPELLE_PREVIEW_COMPLETE prince '..shot);os.exit() end
 tick=tick+1
 if tick==1 then
  for p=1,2 do player(p);for _,k in ipairs({'pulse','down','guard','walk','backthrow','form'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  if c.tyrone then player(2);mapSet('test.form',2) end
 elseif tick==20 then player(2);if c.pulse then mapSet('test.pulse',c.pulse) end end
 if c.name=='movement' then
  player(2)
  if tick==20 then mapSet('test.walk',-1) end
  if tick==45 then mapSet('test.walk',0) end
  if tick==60 then mapSet('test.down',1) end
  if tick==85 then mapSet('test.down',0) end
  if tick==95 then changeState(40) end
  if tick==160 then mapSet('test.pulse',3) end
 elseif c.name=='transformation' then
  player(2)
  if tick==20 or tick==150 then mapSet('test.pulse',13) end
  if tick==85 then mapSet('test.pulse',4) end
 end
 if not pending and tick>=14 and tick<c.length-4 and tick%8==6 then
  player(2);screenshot();pending={index=shot+1,move=c.name,tick=tick,state=stateNo(),animation=anim(),group=spriteVar('group'),form=_G['var'](45)}
 end
 if tick>=c.length then index=index+1;tick=0 end
end)
