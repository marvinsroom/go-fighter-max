local r={frames={},checks={},method="Real pre-fight intro, then interrupted arrival",runtime=jsonDecode('../../characters/jinwoo/validation/intro-runtime.json')}
local shot,pending,seen,finished,skipTick=0,nil,false,false,nil
local scoutSeen,swapped=false,false
local function save() jsonEncode(r,'../../characters/jinwoo/validation/shadow-intro.json') end
hook.add('loop','jinwoo-shadow-intro',function()
 if not player(1) then return end
 if pending then
  local f=io.open('../../characters/jinwoo/replays/comic-20261021113425-intro/Jinwoo_hybrid'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();table.insert(r.frames,pending);pending=nil;shot=shot+1 end
 end
 local state=stateNo()
 if not finished and state==191 then
  seen=true
  if time()<48 and numHelper(878511)>0 and anim()==6 then scoutSeen=true end
  if time()>49 and numHelper(878511)==0 and anim()==878500 then swapped=true end
  if time()%6==0 and not pending then
   pending={case_name='Shadow arrival intro',case_tick=time(),state=state,animation=anim(),scouts=numHelper(878511),group=tonumber(spriteVar('group')) or -1,x=posX(),y=posY(),src='replays/comic-20261021113425-intro/Jinwoo_hybrid'..string.format('%03d',shot)..'.png'}
   screenshot()
  end
 end
 if seen and not finished and state==0 and roundState()==2 and not pending then
  table.insert(r.checks,{name='Actual pre-fight intro finishes grounded in idle',passed=posY()==0 and anim()==0 and spriteVar('group')==0})
  table.insert(r.checks,{name='Shadow enters before Jinwoo exchanges places',passed=scoutSeen and swapped})
  finished=true;changeState(191)
 elseif finished then
  if state==191 and time()>=45 then changeState(0);skipTick=0 end
  if skipTick then
   skipTick=skipTick+1
   if skipTick==12 and not pending then
    table.insert(r.checks,{name='Interrupted arrival returns to normal idle',passed=stateNo()==0 and posY()==0 and anim()==0 and spriteVar('group')==0})
    table.insert(r.checks,{name='Interrupted exchange removes scout and portal',passed=numHelper(878511)==0 and numHelper(878510)==0})
    screenshot();pending={case_name='Interrupted intro cleanup',case_tick=12,state=stateNo(),animation=anim(),group=spriteVar('group'),x=posX(),y=posY(),src='replays/comic-20261021113425-intro/Jinwoo_hybrid'..string.format('%03d',shot)..'.png'}
   elseif skipTick>12 and not pending then
    r.status='Complete';r.passed=0;r.failed=0
    for _,c in ipairs(r.checks) do if c.passed then r.passed=r.passed+1 else r.failed=r.failed+1 end end
    save();print('INTRO_COMPLETE '..r.passed..' passed '..r.failed..' failed');os.exit()
   end
  end
 end
end)
