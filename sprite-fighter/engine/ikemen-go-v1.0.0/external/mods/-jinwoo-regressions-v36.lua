local cases={{state=0,length=110},{state=500,length=45},{state=870100,length=70},{state=870101,length=70},{state=870102,length=70},{state=870103,length=70},{state=876310,length=75}}
local tick,index,localtick,shot,pending=0,0,0,0,nil
local report={status='RUNNING',frames={},helpers={},runtime='jinwoo/jinwoo.def'}
local function save() jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/regressions-v36.json') end
local function traceHelpers()
 local out={};player(1);local count=numHelper()
 for j=0,count-1 do
  player(1);if helper(-1,j) then table.insert(out,{state=stateNo(),anim=anim(),group=spriteVar('group'),image=spriteVar('image')}) end
 end
 player(1);return out
end
hook.add('loop','jinwoo-regressions-v36',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1
 if pending then local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/regressions-v36-preview/'..pending.file;local f=io.open(path,'rb');if f then f:close();table.insert(report.frames,pending);pending=nil;save() end end
 if localtick==1 then index=index+1;if cases[index] then setPower(3000);changeState(cases[index].state) end end
 local c=cases[index]
 if c and not pending and (localtick==2 or localtick==8 or localtick==16 or localtick==28 or localtick==44 or localtick==60 or localtick==90) then
  local file='Jinwoo_Regressions_v36'..string.format('%03d',shot)..'.png';shot=shot+1
  pending={case=index,target=c.state,tick=localtick,state=stateNo(),animation=anim(),group=spriteVar('group'),image=spriteVar('image'),file=file,helper_count=numHelper()}
  report.helpers[tostring(index)..':'..tostring(localtick)]=traceHelpers();screenshot()
 end
 if c and localtick>=c.length then localtick=0 end
 if index>#cases and localtick>=30 and not pending then report.status='PASS';report.frame_count=#report.frames;save();os.exit(0) end
 if tick>750 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)