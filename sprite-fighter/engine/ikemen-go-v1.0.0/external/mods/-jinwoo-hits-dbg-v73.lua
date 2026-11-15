-- Jinwoo v73: does every attack hit at close range, do movement anims animate.
local OUT='../../characters/jinwoo-mugen/proportions-v73/'
local attacks={200,200,210,220,300,310,320,340,1000,1400,1700,1900,240,350,210,220,230,240,300,310,320,330,340,350,400,410,415,420,450,1000,1010,1100,1200,1300,1400,1600,1700,1800,1900,2000,2200,2700,2800,2900,876300,876310}
local report={status='RUNNING',hits={},anim_progress={},shots={}}
local phase,idx,t,shot,pending,wpass='attacks',0,0,0,nil,1
local seen={}
local function save() jsonEncode(report,OUT..'hits-debug-v73.json') end
local function dist() local x1=posX();player(2);local x2=posX();player(1);return math.abs(x2-x1) end
local function snap(label) local f='Hits'..string.format('%03d',shot)..'.png';shot=shot+1;pending={label=label,file=f};screenshot() end
local p2life=0
local progress={}
hook.add('loop','jinwoo-hits-dbg',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open(OUT..'shots/'..pending.file,'rb')
  if f then f:close();table.insert(report.shots,pending);pending=nil;save() else return end
 end
 setPower(3000);setLife(1000)
 t=t+1
 if phase=='idle' then
  -- idle animation must advance through its elements
  local k='idle:'..tostring(var(10))
  progress[k]=progress[k] or {}
  progress[k][tostring(animElemNo(0))]=true
  if t==20 then snap('side-by-side-idle') end
  if t==30 then changeState(870220) end
  if t>=75 and t<110 then local k2='idle:'..tostring(var(10));progress[k2]=progress[k2] or {};progress[k2][tostring(animElemNo(0))]=true end
  if t==90 then snap('side-by-side-idle-daggers') end
  if t==110 then changeState(870220) end
  if t==150 then phase='walk';t=0 end
  return
 end
 if phase=='walk' then
  -- force walk/run states repeatedly and record element progression
  local st=(t<80) and 20 or 100
  if stateNo()~=st then changeState(st) end
  local k=tostring(st)..':'..tostring(anim())
  progress[k]=progress[k] or {}
  progress[k][tostring(animElemNo(0))]=true
  if t==40 then snap('walk') end
  if t==120 then snap('run') end
  if t==160 then changeState(0);phase='jump';t=0 end
  return
 end
 if phase=='jump' then
  if t==1 then changeState(40) end
  local k='jump:'..tostring(anim())
  progress[k]=progress[k] or {}
  progress[k][tostring(animElemNo(0))]=true
  if t==12 then snap('jump-rise') end
  if t==28 then snap('jump-fall') end
  if t>=70 then phase='attacks';t=0;report.anim_progress=progress;save() end
  return
 end
 if phase=='ai' then
  local k='ai:'..tostring(stateNo())..':'..tostring(anim())
  progress[k]=progress[k] or {}
  progress[k][tostring(animElemNo(0))]=true
  if t%150==75 then snap('ai-'..t) end
  player(2);if moveType()=='H' then report.ai_hits=(report.ai_hits or 0)+1 end;setLife(1000);player(1)
  if t>=1500 then report.status='DONE';report.anim_progress=progress;save();os.exit(0) end
  return
 end
 -- attacks
 if t==1 then
  idx=idx+1
  if idx>#attacks then report.status='DONE';save();os.exit(0) end
 end
 local st=attacks[idx]
 if t==2 then player(2);changeState(0);player(1);changeState(879990);return end
 if t<6 then return end
 if not report.hits[tostring(idx)..':'..tostring(st)] then
  player(2);setLife(1000);changeState(0);player(1)
  changeState(st);report.hits[tostring(idx)..':'..tostring(st)]={hit=false,dist=dist(),start=t}
  return
 end
 local h=report.hits[tostring(idx)..':'..tostring(st)]
 player(2);local mv=moveType();local life2=life();player(1)
 if mv=='H' or life2<1000 then h.hit=true end
 if t-h.start==6 or t-h.start==10 then snap('atk-'..st..'-'..(t-h.start)..'-d'..math.floor(dist())) end
 if t-h.start>=150 or (t-h.start>12 and stateNo()==0) then
  h.ended=stateNo();save()
  player(2);changeState(0);setLife(1000);player(1)
  changeState(0);t=0
 end
end)
