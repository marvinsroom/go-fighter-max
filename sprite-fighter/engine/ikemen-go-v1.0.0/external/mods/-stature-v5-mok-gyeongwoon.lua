local cases=jsonDecode('../../face-audit/identity-scale-v5/native/mok-gyeongwoon/cases.json')
local report={status='Running',checks={},frames={},runtime_sha256=jsonDecode('../../face-audit/identity-scale-v5/native/mok-gyeongwoon/runtime.json'),method='Current native packed body samples, both facings, actual CNS and AIR scales'}
local index,tick,shot,pending,warmup=1,0,0,nil,0
local function save() jsonEncode(report,'../../face-audit/identity-scale-v5/native/mok-gyeongwoon/current.json') end
hook.add('loop','stature-v5',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if pending then
  local file=io.open('../../face-audit/identity-scale-v5/native/mok-gyeongwoon/run-20261021141452/Stature_v5'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);table.insert(report.checks,{label=pending.label,facing=pending.facing,passed=pending.passed});index=index+1;tick=0;shot=shot+1;pending=nil;save() end
  return
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 if c.combat then
  tick=tick+1
  if tick==1 then
   mapSet('stature.pose',0);mapSet('stature.facing',1);mapSet('stature.combat',1);changeState(879650)
   player(2);setLife(1000);changeState(879651);player(1)
  end
  if tick==8 then changeState(200) end
  if tick>=12 then
   player(2);local hp=life();player(1)
   if hp<1000 or tick>=240 then
    pending={label=c.label,facing=facing(),group=spriteVar('group'),drawing=spriteVar('image'),target_life=hp,passed=hp<1000,file='../../face-audit/identity-scale-v5/native/mok-gyeongwoon/run-20261021141452/Stature_v5'..string.format('%03d',shot)..'.png'};screenshot()
   end
  end
  return
 end
 tick=tick+1
 if tick==1 then mapSet('stature.pose',c.id);mapSet('stature.facing',c.facing);changeState(879650) end
 if tick>=24 then
  local g=tonumber(spriteVar('group'));local d=tonumber(spriteVar('image'));local sx=tonumber(animElemVar('xscale'));local sy=tonumber(animElemVar('yscale'));local native=tonumber(map('stature.native_scale')) or -1
  local ok=g==c.group and d==c.drawing and facing()==c.facing and math.abs(sx-c.xscale)<.00001 and math.abs(sy-c.yscale)<.00001 and math.abs(native-c.native_scale)<.00001 and posY()==0
  pending={label=c.label,facing=facing(),group=g,drawing=d,xscale=sx,yscale=sy,native_scale=native,screen_x=screenPosX(),screen_y=screenPosY(),passed=ok,file='../../face-audit/identity-scale-v5/native/mok-gyeongwoon/run-20261021141452/Stature_v5'..string.format('%03d',shot)..'.png'}
  screenshot()
 end
end)
