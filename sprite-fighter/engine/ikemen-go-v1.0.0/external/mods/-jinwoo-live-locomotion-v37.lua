local cases={{name='idle',state=0,length=42},{name='crouch',state=10,length=42},{name='walk-forward',state=20,length=54},{name='walk-back',state=21,length=54},{name='jump-start',state=40,length=30},{name='jump-rise',state=41,length=30},{name='jump-forward',state=42,length=30},{name='jump-back',state=43,length=30},{name='jump-apex',state=44,length=30},{name='jump-land',state=47,length=30}}
local tick,index,localtick,shot,pending=0,0,0,0,nil
local report={status='RUNNING',runtime='jinwoo/jinwoo.def',frames={}}
local function save()
 jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/live-locomotion-v37.json')
end
hook.add('loop','jinwoo-live-locomotion-v37',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1
 if pending then
  local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/live-locomotion-v37-preview/'..pending.file
  local f=io.open(path,'rb')
  if f then f:close();table.insert(report.frames,pending);pending=nil;save() end
 end
 if localtick==1 then
  index=index+1
  if cases[index] then changeState(cases[index].state) end
 end
 local c=cases[index]
 if c and not pending and (localtick==2 or localtick==8 or localtick==16 or localtick==28 or localtick==40) then
  local file='Jinwoo_Live_Locomotion_v37'..string.format('%03d',shot)..'.png';shot=shot+1
  pending={case=index,name=c.name,target=c.state,tick=localtick,state=stateNo(),animation=anim(),
   group=spriteVar('group'),image=spriteVar('image'),pos_x=posX(),pos_y=posY(),file=file}
  screenshot()
 end
 if c and localtick>=c.length then localtick=0 end
 if index>#cases and localtick>=20 and not pending then
  report.status='PASS';report.frame_count=#report.frames;save();os.exit(0)
 end
 if tick>700 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)