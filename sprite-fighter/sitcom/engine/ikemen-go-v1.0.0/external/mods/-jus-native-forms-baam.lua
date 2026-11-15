local cases=jsonDecode('../../jus-upgrade/native-forms/baam/cases.json')
local report={status='Running',slug='baam',method='Production AIR cycles replayed in isolated observation IDs, both facings, short per-pose capture holds; physical movement tested separately',checks={},frames={}}
local index,tick,shot,warmup=1,0,0,0
local seen,pending={},nil
local function save() jsonEncode(report,'../../jus-upgrade/native-forms/baam/current.json') end
local function finishCase(ok,why)
 table.insert(report.checks,{label=cases[index].label,facing=cases[index].facing,passed=ok,detail=why})
 index=index+1;tick=0;seen={};mapSet('jusform.hold',0);mapSet('jusform.natural',0);mapSet('jusform.urkel',0);save()
end
hook.add('loop','jus-form-cycles-baam',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if pending then
  -- Speed-test physics can advance several times between displayed frames.
  -- Hold the exact drawing long enough for fresh render buffers, then capture.
  if pending.settle<24 then pending.settle=pending.settle+1;return end
  if not pending.requested then screenshot();pending.requested=true;return end
  local f=io.open(pending.file,'rb')
  if f then
   f:close();pending.passed=spriteVar('group')==pending.group and spriteVar('image')==pending.drawing and facing()==pending.facing
   table.insert(report.frames,pending);seen[pending.drawing]=pending.passed;pending=nil;shot=shot+1;mapSet('jusform.hold',0);save()
  end
  return
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 tick=tick+1
 if c.natural then
  if tick==1 then
   mapSet('jusform.hold',0);mapSet('jusform.natural',1);mapSet('jusform.urkel',c.urkel and 1 or 0);mapSet('jusform.form_value',c.form_value)
   if c.form_map then mapSet(c.form_map,c.form_value) end
   mapSet('ichigo.manual',1);mapSet('luffy.manual',1);mapSet('goku.manual',1)
   setPower(3000);changeState(8797199)
  end
  if tick<10 then return end
  if spriteVar('group')~=c.group then finishCase(false,'Natural walk used wrong body group '..tostring(spriteVar('group')));return end
  seen[spriteVar('image')]=true
  local count=0;for _ in pairs(seen) do count=count+1 end
  if count==8 then finishCase(true,'Original forward controls played all eight form drawings; native state '..tostring(stateNo()));return end
  if tick>60 then finishCase(false,'Natural forward input did not play eight form drawings') end
  return
 end
 if tick==1 then
  mapSet('jusform.natural',0);mapSet('jusform.urkel',0)
  mapSet('jusform.action',c.action);mapSet('jusform.facing',c.facing);mapSet('jusform.hold',0);changeState(8797198)
 end
 if tick<3 then return end
 local count=0;for _,v in pairs(seen) do if v then count=count+1 end end
 if count==8 then finishCase(true,'All eight native drawings and scales captured');return end
 if tick>100 then finishCase(false,'Did not observe all eight drawings');return end
 local g,d=spriteVar('group'),spriteVar('image')
 if g~=c.group then finishCase(false,'Unexpected body group '..tostring(g));return end
 local sx,sy=animElemVar('xscale'),animElemVar('yscale')
 if math.abs(sx-c.xscale)>.000001 or math.abs(sy-c.yscale)>.000001 or facing()~=c.facing or posY()~=0 then finishCase(false,'Native scale/facing/root mismatch');return end
 if d>=0 and d<8 and seen[d]==nil then
  mapSet('jusform.elem',c.backward and 8-d or d+1);mapSet('jusform.hold',1)
  pending={label=c.label,facing=c.facing,group=g,drawing=d,xscale=sx,yscale=sy,settle=0,file='../../jus-upgrade/native-forms/baam/run-20261021-224713-983071/JUS_baam'..string.format('%03d',shot)..'.png'}
 end
end)
