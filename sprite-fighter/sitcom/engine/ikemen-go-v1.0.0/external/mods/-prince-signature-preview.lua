
local tick,shot=0,0
local pending=nil
local selectAt,selectedForm=nil,nil
local report={method='Native renderer; real command routes for signature moves and finishers',capture_directory='cinematics-v6-final',frames={}}
local function reset(form)
 for p=1,2 do player(p);for _,key in ipairs({'pulse','walk','guard','down','charge'}) do mapSet('test.'..key,0) end;changeState(9000) end
 selectAt=tick+7;selectedForm=form+1
end
hook.add('loop','prince-signature-preview',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local path='../../characters/prince/replays/cinematics-v6-final/Chappelle_signature_prince'..string.format('%03d',shot)..'.png'
  local f=io.open(path,'rb');if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if selectAt and tick==selectAt then player(2);mapSet('test.form',selectedForm);selectAt=nil end
 for form=0,1 do
  local t=tick-form*1400
  if t==1 or t==220 or t==300 or t==440 or t==800 then reset(form) end
  if t==20 then player(2);mapSet('test.pulse',18);if 'prince'=='tyrone' and form==1 then mapSet('test.charge',1) end end
  if t==150 then player(2);mapSet('test.charge',0) end
  if t==90 then player(2);mapSet('test.down',1) end
  if t==130 then player(2);mapSet('test.down',0) end
  if t==145 then player(2);mapSet('test.walk',1) end
  if t==180 then player(2);mapSet('test.walk',0) end
  if t==240 then player(2);mapSet('test.pulse',17) end
  if t==255 then player(2);mapSet('test.pulse',4) end
  if t==320 then player(1);mapSet('test.pulse',7) end
  if t==460 then player(2);mapSet('test.pulse',5) end
  if t==820 then player(2);mapSet('test.pulse',6) end
 end
 if not pending and tick>=14 and tick<2780 and tick%8==6 then
  player(2);screenshot();pending={index=shot+1,tick=tick,state=stateNo(),animation=anim(),form=_G['var'](45),group=spriteVar('group')}
 end
 if tick>=2800 then jsonEncode(report,'../../characters/prince/signature-preview-report.json');print('SIGNATURE_PREVIEW_COMPLETE prince '..shot);os.exit() end
end)
