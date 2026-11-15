-- Screenshot every super / ultimate at fixed ticks, in both weapon modes.
local OUT='../../characters/jinwoo-mugen/consistency-v72/'
local states={1900,2000,2200,2400,2600,2620,2700,2800,2850,2900,2950,3000,3100,3200,876300,876310,1500}
local ticks={[6]=1,[20]=1,[40]=1,[65]=1,[95]=1,[130]=1,[170]=1,[220]=1}
local report={status='RUNNING',shots={}}
local idx,t,shot,pending,pass,approach=0,0,0,nil,1,0
local function dist() local x1=posX();player(2);local x2=posX();player(1);return math.abs(x2-x1) end
local function save() jsonEncode(report,OUT..'supers-shots-v73.json') end
hook.add('loop','jinwoo-supers-shots-v73',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open(OUT..'supers/'..pending.file,'rb')
  if f then f:close();table.insert(report.shots,pending);pending=nil;save() else return end
 end
 setLife(1000);setPower(3000);player(2);setLife(1000);player(1)
 t=t+1
 if idx==0 or t>240 or (t>10 and stateNo()==0) then
  idx=idx+1;t=0
  if idx>#states then
   if pass==1 then pass=2;idx=0;changeState(870220);t=-45;return end
   report.status='DONE';save();os.exit(0)
  end
  approach=1;return
 end
 if approach>0 then
  approach=approach+1
  if dist()>45 and approach<200 then
   if stateNo()==0 or stateNo()==52 then changeState(879960) end
   t=0;return
  end
  if stateNo()~=0 and approach<200 then t=0;return end
  approach=0;t=0
  player(2);changeState(0);player(1)
  changeState(states[idx]);return
 end
 if t>0 and ticks[t] then
  local file='Super'..string.format('%03d',shot)..'.png';shot=shot+1
  pending={pass=pass,state=states[idx],tick=t,cur=stateNo(),anim=anim(),weapon=var(10),file=file}
  screenshot()
 end
end)
