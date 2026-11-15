-- AI vs AI: per Jinwoo attack state, how often it connects (hit or guarded).
local OUT='../../characters/jinwoo-mugen/proportions-v73/'
local report={status='RUNNING',states={},ticks=0,whiffs=0,connects=0}
local t,cur,contact=0,nil,false
local function save() jsonEncode(report,OUT..(os.getenv('JW_TAG') or 'aimatch')..'.json') end
hook.add('loop','jinwoo-aimatch-v73',function()
 if not player(1) or roundState()~=2 then return end
 t=t+1
 if t==1 then setAILevel(1,8);setAILevel(2,8) end
 setLife(1000);player(2);setLife(1000)
 local p2mv=moveType()
 player(1)
 local st=stateNo();local mv=moveType()
 if mv=='A' and st~=cur then
  if cur then local s=report.states[tostring(cur)];s.n=s.n+1;if contact then s.c=s.c+1;report.connects=report.connects+1 else report.whiffs=report.whiffs+1 end end
  cur=st;contact=false;report.states[tostring(st)]=report.states[tostring(st)] or {n=0,c=0}
 elseif mv~='A' and cur then
  local s=report.states[tostring(cur)];s.n=s.n+1;if contact then s.c=s.c+1;report.connects=report.connects+1 else report.whiffs=report.whiffs+1 end
  cur=nil;contact=false
 end
 if cur and p2mv=='H' then contact=true end
 if t%300==0 then save() end
 if t>=3600 then report.ticks=t;report.status='DONE';save();os.exit(0) end
end)
