local tick,index,localtick,shot,pending=0,0,0,0,nil
local targets={870220,870220,870220,876290,876300,876310}
local shotmap={[870220]={5,15,23,31},[876290]={8,16,25},[876300]={10,19,28},[876310]={10,22,29,38}}
local report={status='RUNNING',targets=targets,entered={},frames={},states={},runtime='jinwoo/jinwoo.def'}
local function save() jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/arsenal-engine-smoke-v35.json') end
local function wants(state,t)
 local times=shotmap[state] or {}
 for _,v in ipairs(times) do if v==t then return true end end
 return false
end
hook.add('loop','jinwoo-arsenal-v35-smoke',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1;report.states[tostring(stateNo())]=true
 if pending then
  local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/arsenal-v35-preview/'..pending.file
  local f=io.open(path,'rb')
  if f then f:close();table.insert(report.frames,pending);pending=nil;save() end
 end
 if localtick==1 then
  index=index+1
  if targets[index] then setPower(3000);changeState(targets[index]);report.entered[tostring(index)..':'..tostring(targets[index])]=true end
 end
 if targets[index] and wants(targets[index],localtick) and not pending then
  local file='Jinwoo_Arsenal_v35'..string.format('%03d',shot)..'.png'
  pending={target=targets[index],tick=localtick,state=stateNo(),animation=anim(),file=file}
  shot=shot+1
  screenshot()
 end
 if localtick>=72 then localtick=0 end
 if index>#targets and localtick>=50 and not pending then report.status='PASS';report.active_round_ticks=tick;report.frame_count=#report.frames;save();os.exit(0) end
 if tick>900 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)
