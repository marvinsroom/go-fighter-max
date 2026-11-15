-- Jinwoo JUS playstyle v71 smoke: intro, weapon lock, escort, chase, physics.
local OUT='../../characters/jinwoo-mugen/jus-playstyle-v71/'
local report={status='RUNNING',intro_frames={},checks={},weapons_seen={},states={},escort_states={}}
local tick,itick,phase,ptick,shot,pending=0,0,1,0,0,nil
local function save() jsonEncode(report,OUT..'engine-smoke-v71.json') end
local function snap(label)
 local file='Jinwoo_JUS_v71'..string.format('%03d',shot)..'.png'
 shot=shot+1
 pending={label=label,state=stateNo(),anim=anim(),weapon=var(10),file=file}
 screenshot()
end
local function check(name,ok,detail)
 table.insert(report.checks,{name=name,passed=ok and true or false,detail=detail});save()
end
local function dist() local x1=posX();player(2);local x2=posX();player(1);return math.abs(x2-x1) end
local escorts=0
-- phase: {name, ticks, action(t)}
local phases={
 {'settle',30,function(t) if t==20 then check('round starts holding the longsword',var(10)==20000,{weapon=var(10)}) end end},
 {'swap to daggers',50,function(t) if t==1 then changeState(870220) end if t==12 then snap('sword-to-daggers') end if t==45 then check('swap 1 -> daggers',var(10)==10000,{weapon=var(10)}) end end},
 {'swap to sword',50,function(t) if t==1 then changeState(870220) end if t==45 then check('swap 2 -> longsword (no bare hands)',var(10)==20000,{weapon=var(10)}) end end},
 {'approach',150,function(t) if dist()>70 and (stateNo()==0 or stateNo()==52) then changeState(879960) end if t==150 then report.approach_distance=dist() end end},
 {'summon escort',70,function(t) if t==1 then setPower(3000);changeState(870100) end if t==40 then escorts=numHelper(870790);snap('escort-arrives');check('summon leaves an Igris escort on the field',escorts==1,{escorts=escorts}) end end},
 {'tandem light',40,function(t) if t==1 then changeState(200) end if t==10 or t==22 then snap('tandem-strike') end end},
 {'tandem medium',40,function(t) if t==1 then changeState(300) end if t==14 then snap('tandem-strike-2') end end},
 {'launcher',40,function(t) if t==1 then changeState(340) end if t==10 then snap('launcher') end end},
 {'air chase',50,function(t) if t==1 then changeState(879960) end if t==6 then snap('air-chase');check('air chase rises and hands control to air state',posY()<-10,{y=posY(),state=stateNo()}) end end},
 {'escort persists',60,function(t) if t==50 then check('escort still fighting after the combo',numHelper(870790)==1,{escorts=numHelper(870790)});check('escort struck in tandem with Jinwoo',report.escort_states['870791'] or report.escort_states['870792'] or report.escort_states['870793'],report.escort_states) end end},
}
hook.add('loop','jinwoo-jus-v71-smoke',function()
 if not player(1) then return end
 if pending then
  local f=io.open(OUT..'smoke/'..pending.file,'rb')
  if f then f:close();table.insert(report.intro_frames,pending);pending=nil;save() end
 end
 tick=tick+1
 if tick>2400 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
 if roundState()==1 or (roundState()<2 and stateNo()==191) then
  itick=itick+1
  if (stateNo()==191 or itick<=40) and (itick==4 or itick==12 or itick==20 or itick==30 or itick==40 or itick==70 or itick==108 or itick==150) and not pending then snap('intro-'..itick) end
  return
 end
 if roundState()~=2 then return end
 report.states[tostring(stateNo())]=true
 local count=numHelper()
 for j=0,count-1 do
  player(1);if helper(-1,j) then report.escort_states[tostring(stateNo())]=true end
 end
 player(1)
 report.weapons_seen[tostring(var(10))]=true
 setLife(1000)
 player(2);setLife(1000);player(1)
 local p=phases[phase]
 if not p then
  if pending then return end
  local ok=report.weapons_seen['0']==nil
  check('never in bare-hand mode during the run',ok,report.weapons_seen)
  local all=true
  for _,c in ipairs(report.checks) do if not c.passed then all=false end end
  report.status=all and 'PASS' or 'FAIL';report.intro_ticks=itick;save();os.exit(all and 0 or 1)
 end
 ptick=ptick+1
 p[3](ptick)
 if ptick>=p[2] then phase=phase+1;ptick=0 end
end)
