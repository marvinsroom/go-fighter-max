local cases=jsonDecode('../../characters/jinwoo/validation/proportions-cases.json')
local report={checks={},frames={},runtime=jsonDecode('../../characters/jinwoo/validation/proportions-runtime.json'),method='Every authored drawing, both facings, actual engine sprite and AIR scale',capture_directory='comic-20261021113425-proportions'}
local index,tick,shot,pending,warmup=1,0,0,nil,0
local function save() jsonEncode(report,'../../characters/jinwoo/validation/proportions-native.json') end
hook.add('loop','jinwoo-proportion-audit',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<90 then warmup=warmup+1;return end
 if pending then
  local file=io.open('../../characters/jinwoo/replays/comic-20261021113425-proportions/Jinwoo_hybrid'..string.format('%03d',shot)..'.png','rb')
  if file then
   file:close();table.insert(report.frames,pending);table.insert(report.checks,{key=pending.key,facing=pending.facing,passed=pending.passed})
   index=index+1;tick=0;shot=shot+1;pending=nil;save()
  end
  return
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,check in ipairs(report.checks) do if check.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('PROPORTIONS_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 tick=tick+1
 if tick==1 then mapSet('pose.id',c.id);mapSet('pose.facing',c.facing);changeState(879650) end
 if tick>=24 then
  local group=tonumber(spriteVar('group'));local image=tonumber(spriteVar('image'));local sx=tonumber(animElemVar('xscale'));local sy=tonumber(animElemVar('yscale'))
  local ok=group==c.group and image==c.number and facing()==c.facing and math.abs(sx-c.scale)<.00001 and math.abs(sy-c.scale)<.00001 and posY()==0
  pending={key=c.key,facing=facing(),group=group,drawing=image,xscale=sx,yscale=sy,passed=ok,src='replays/comic-20261021113425-proportions/Jinwoo_hybrid'..string.format('%03d',shot)..'.png'}
  screenshot();if index%24==0 then print('PROPORTION_POSE '..index..'/'..#cases..' '..c.key..' '..tostring(ok)) end
 end
end)
