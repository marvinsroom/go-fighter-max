local cases=jsonDecode('../../characters/jinwoo/hybrid-test-cases.json')
local report={checks={},frames={},method='Native command routes and rendered form identities',randomForms={}}
local index,tick,shot=1,0,0
local previousShadow=0
local seen,animations,violations,minLife,minPower,chosen,returned,army,images,ownLife,maxPower,trace
local function save()jsonEncode(report,'../../characters/jinwoo/hybrid-native-validation.json')end
hook.add('loop','jinwoo-hybrid-suite',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();print('HYBRID_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 tick=tick+1
 if tick==1 then
  seen={};animations={};violations={};minLife=1000;minPower=3000;chosen=nil;returned=false;army={};images={};ownLife=1000;maxPower=0;trace={}
  player(1);for _,k in ipairs({'pulse','walk','back','down','jump','charge'}) do mapSet('jw.'..k,0) end
  for i=0,3 do mapSet('jw.army'..i,0) end
  mapSet('jw.form',c.form);mapSet('jw.setup',1);changeState(879000);setLife(1000);setPower((c.mode=='empty' or c.charge) and 0 or 3000)
  player(2);for _,k in ipairs({'pulse','walk','down','guard'}) do mapSet('test.'..k,0) end;changeState(9000);setLife(1000)
 elseif tick==9 then
  player(2);setLife(1000)
  if c.mode=='block' then mapSet('test.guard',1) end
  if c.mode=='whiff' then changeState(9002) end
 elseif tick==20 then
  player(1)
  if c.hold then mapSet('jw.'..c.hold,1) end
  if c.air then mapSet('jw.jump',1) end
  if c.summon==1 then mapSet('jw.walk',1) elseif c.summon==2 then mapSet('jw.back',1) elseif c.summon==3 then mapSet('jw.down',1) end
  if c.pulse and not c.air then mapSet('jw.pulse',c.pulse) end
  if c.incoming then player(2);changeState(c.incoming) end
 elseif tick==25 then player(1);mapSet('jw.jump',0)
 elseif tick==31 then player(1);if c.air then mapSet('jw.pulse',c.pulse) end
 end
 if tick==34 and c.summon then player(1);mapSet('jw.walk',0);mapSet('jw.back',0);mapSet('jw.down',0) end
 if tick==85 then
  player(1);mapSet('jw.walk',0);mapSet('jw.back',0);mapSet('jw.down',0);mapSet('jw.charge',0)
  if c.toggle then chosen=_G['var'](45);report.randomForms[tostring(chosen)]=true;mapSet('jw.pulse',7) end
 end
 if tick>=22 then
  player(1);seen[tostring(stateNo())]=true;animations[tostring(anim())]=true;images[tostring(spriteVar('group'))..','..tostring(spriteVar('image'))]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());ownLife=math.min(ownLife,life())
  local form=_G['var'](45);local group=spriteVar('group')
  if form>0 and group~=61000+form and time()>1 and #violations<8 then table.insert(violations,{tick=tick,state=stateNo(),animation=anim(),group=group,form=form}) end
  if c.toggle and tick>130 and form==0 then returned=true end
  for i=0,3 do if map('jw.army'..i)>0 then army[tostring(i)]=true end end
  player(2);minLife=math.min(minLife,life())
  if c.air and c.pulse==4 and tick<80 then
   local enemyx,enemyy=posX(),posY();player(1);table.insert(trace,{tick=tick,state=stateNo(),time=time(),x=posX(),y=posY(),enemyx=enemyx,enemyy=enemyy,animation=anim()})
  end
 end
 if c.capture and (tick==45 or tick==70 or tick==110 or (c.length>300 and tick==180)) then
  shot=shot+1;player(1);screenshot();table.insert(report.frames,{index=shot,name=c.name,tick=tick,state=stateNo(),animation=anim(),form=_G['var'](45)})
 end
 if tick>=c.length then
  player(1);local damage=1000-minLife;local ok=#violations==0;local count=0;for _ in pairs(images) do count=count+1 end
  if c.damage and damage<=0 then ok=false end
  if c.exact and damage~=c.exact then ok=false end
  if c.expected then
   if c.mode=='hit' and not seen[tostring(c.expected)] then ok=false end
   if c.mode~='hit' and seen[tostring(c.expected)] then ok=false end
   if minPower~=(c.mode=='empty' and 0 or 3000-c.cost) then ok=false end
  end
  if c.toggle then
   if not chosen or chosen<1 or chosen>4 or not returned or chosen==previousShadow then ok=false end
   previousShadow=chosen
  end
  if c.received and 1000-ownLife~=c.received then ok=false end
  if c.charge and (maxPower<=0 or stateNo()~=0) then ok=false end
  if c.form==0 and c.mode=='hit' and c.pulse==6 then for i=0,3 do if not army[tostring(i)] then ok=false end end end
  if c.hold=='walk' or c.hold=='back' then if count<4 then ok=false end end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,received=1000-ownLife,min_power=minPower,max_power=maxPower,states=seen,animations=animations,violations=violations,drawings=count,chosen=chosen,returned=returned,army=army,trace=trace,final_state=stateNo()})
  print('HYBRID_TEST '..index..' '..c.name..' '..tostring(ok)..' damage='..damage);save();index=index+1;tick=0
 end
end)
