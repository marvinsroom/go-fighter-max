local cases=jsonDecode('../../characters/jinwoo/validation/a-button-record-cases.json')
local report={checks={},frames={},method='A-button size and double-sprite audit',capture_directory='a-button-record'}
local index,tick,shot=1,0,0
local pending=nil
local seen,violations,minEnemy,minOwn,minPower,images,ready,chosen,returned
local previous=0
local started=nil
local chargedAt=nil
local function save()jsonEncode(report,'../../characters/jinwoo/validation/a-button-record.json')end
hook.add('loop','jinwoo-ported-suite',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local file=io.open('../../characters/jinwoo/replays/a-button-record/Jinwoo_hybrid'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=cases[index]
 if not c then
  if pending then return end
  report.status='Complete';report.passed=0;report.failed=0
  for _,row in ipairs(report.checks) do if row.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('PORTED_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 tick=tick+1
 local actionTick=started or (c.ready and 100000 or 20)
 local caseLength=c.length+((started or (c.ready and 1200 or 20))-20)
 if tick==1 then
  seen={};violations={};minEnemy=1000;minOwn=1000;minPower=3000;images={};ready=false;chosen=nil;returned=false;started=nil;chargedAt=nil
  player(1);for _,k in ipairs({'pulse','walk','back','down','jump','charge'}) do mapSet('jw.'..k,0) end
  mapSet('jw.weapon',c.weapon or 0);mapSet('jw.ready',c.ready and 1 or 0);mapSet('jw.form',c.form or 0);mapSet('jw.setup',1);changeState(879000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.guard',0);mapSet('test.down',0);changeState(9000);setLife(1000)
 elseif tick==9 then
  player(2);if c.guard then mapSet('test.guard',1) end;if c.far then changeState(9002) elseif c.close then changeState(9005) end
 elseif tick==20 and c.ready then player(1);mapSet('jw.charge',1)
 end
 player(1)
 if c.ready and not chargedAt and tick>=45 and map('jw.energyReady')>0 then mapSet('jw.charge',0);chargedAt=tick end
 if c.ready and chargedAt and not started and tick>=chargedAt+20 and stateNo()==0 then started=tick;actionTick=tick end
 if tick==actionTick then
  player(1);if c.hold then mapSet('jw.'..c.hold,1) end
  if c.ready and c.meter then setPower(c.meter) end
  if c.direct then changeState(c.direct) elseif c.air then mapSet('jw.jump',1) elseif c.pulse then mapSet('jw.pulse',c.pulse) end
 end
 if tick==25 then player(1);mapSet('jw.jump',0) end
 if tick==31 then player(1);if c.air then mapSet('jw.pulse',c.pulse) end end
 if c.phases then for _,phase in ipairs(c.phases) do if (not c.ready or started) and tick==phase.tick+(c.ready and started-20 or 0) then player(1);mapSet('jw.pulse',phase.pulse) end end end
 if (not c.ready or started) and tick==(c.release or 85)+(c.ready and started-20 or 0) then
  player(1);mapSet('jw.walk',0);mapSet('jw.back',0);mapSet('jw.down',0);mapSet('jw.charge',0)
  if c.toggle then chosen=_G['var'](45);mapSet('jw.pulse',7) end
 end
 if tick>=22 then
  player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());minOwn=math.min(minOwn,life());if map('jw.energyReady')>0 then ready=true end
  local form=_G['var'](45)
  if form>0 and anim()~=6 and spriteVar('group')~=61000+form and time()>1 and #violations<8 then table.insert(violations,{tick=tick,state=stateNo(),animation=anim(),group=spriteVar('group')}) end
  if c.toggle and tick>140 and form==0 then returned=true end
  player(2);minEnemy=math.min(minEnemy,life())
 end
 if c.capture and tick>20 and tick%(c.every_frame and 1 or 12)==0 and not pending then
  player(1);local actor={index=shot+1,case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),x=posX(),y=posY(),form=_G['var'](45),drawing=tonumber(spriteVar('image')) or -1,group=tonumber(spriteVar('group')) or -1,body_scale_x=tonumber(animElemVar('xscale')) or 1,body_scale_y=tonumber(animElemVar('yscale')) or 1,screen_x=tonumber(screenPosX()) or -1,screen_y=tonumber(screenPosY()) or -1}
  player(2);actor.target_state=stateNo();actor.target_animation=anim();actor.target_life=life();screenshot();pending=actor
 end
 if tick>=caseLength then
  player(1);local ok=#violations==0;local damage=1000-minEnemy
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.forbid and seen[tostring(c.forbid)] then ok=false end
  if c.damage and damage<=0 then ok=false end
  if c.domain and _G['var'](11)~=1 then ok=false end
  if c.charge and (power()<=0 or not ready or stateNo()~=0) then ok=false end
  if c.toggle then if not chosen or chosen==previous or chosen<1 or chosen>4 or not returned then ok=false end;previous=chosen end
  table.insert(report.checks,{name=c.name,passed=ok,states=seen,violations=violations,damage=damage,min_power=minPower,final_power=power(),final_state=stateNo(),weapon=_G['var'](10),domain=_G['var'](11),energy_ready=ready,chosen=chosen,returned=returned})
  print('PORTED_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage);save();index=index+1;tick=0
 end
end)
