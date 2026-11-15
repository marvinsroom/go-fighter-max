
local cases={{name="P1 form 0 super",actor=1,form=0,pulse=5,damage=620,length=420},{name="P1 form 0 ultimate",actor=1,form=0,pulse=6,damage=950,length=620},{name="P1 form 1 super",actor=1,form=1,pulse=5,damage=620,length=420},{name="P1 form 1 ultimate",actor=1,form=1,pulse=6,damage=950,length=620},{name="P2 form 0 super",actor=2,form=0,pulse=5,damage=620,length=420},{name="P2 form 0 ultimate",actor=2,form=0,pulse=6,damage=950,length=620},{name="P2 form 1 super",actor=2,form=1,pulse=5,damage=620,length=420},{name="P2 form 1 ultimate",actor=2,form=1,pulse=6,damage=950,length=620},{name="P1 actual toggle and return",actor=1,toggle=true,length=250},{name="P2 actual toggle and return",actor=2,toggle=true,length=250},{name="Independent simultaneous toggles",actor=1,toggle=true,both=true,length=250},{name="P1 Rick slap against alternate form",actor=1,form=1,targetForm=1,pulse=6,damage=950,length=620},{name="P2 Negan execution against alternate form",actor=2,form=1,targetForm=1,pulse=6,damage=950,length=620}}
local index,tick=1,0
local seen,violations={},{}
local revealed,returned=false,false
local kneeling,aftermath,badPose,early,changes,previousLife=false,false,false,false,0,1000
local held,dazed=false,false
local report={status='Running',method='Actual paired matchup with both player sides',checks={}}
hook.add('loop','chappelle-two-pair-match',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/chappelle/paired-match-validation.json');print('PAIRED_MATCH_COMPLETE');os.exit() end
 tick=tick+1
 local actor=c.actor;local target=3-actor
 if tick==1 then
  seen={};violations={};revealed=false;returned=false
  kneeling=false;aftermath=false;badPose=false;early=false;changes=0;previousLife=1000
  held=false;dazed=false
  for p=1,2 do player(p);for _,k in ipairs({'pulse','form','guard','down','walk','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  if c.toggle then
   player(actor);setLife(600);setPower(1234)
  else
   player(actor);mapSet('test.form',c.form+1);player(target);mapSet('test.form',c.targetForm and c.targetForm+1 or 2-c.form)
  end
 elseif tick==20 then
  player(actor);mapSet('test.pulse',c.toggle and 13 or c.pulse)
  if c.both then player(target);mapSet('test.pulse',13) end
 end
 if c.toggle and tick==150 then player(actor);mapSet('test.pulse',13);if c.both then player(target);mapSet('test.pulse',13) end end
 if c.toggle and tick==85 then
  player(actor);revealed=_G['var'](45)==1 and spriteVar('group')==51 and life()==600 and power()==1234
  if c.both then player(target);revealed=revealed and _G['var'](45)==1 and spriteVar('group')==51 end
  screenshot()
 end
 if c.toggle and tick==220 then
  player(actor);returned=_G['var'](45)==0 and spriteVar('group')==50 and life()==600 and power()==1234
  if c.both then player(target);returned=returned and _G['var'](45)==0 and spriteVar('group')==50 end
  screenshot()
 end
 if not c.toggle and tick>=24 then
  for p=1,2 do
   player(p);local form=_G['var'](45);local group=spriteVar('group')
   if group~=50+form and #violations<12 then table.insert(violations,{player=p,tick=tick,group=group,state=stateNo(),form=form}) end
  end
  player(actor);seen[tostring(stateNo())]=true
  if c.pulse==6 then
   local executing=stateNo()==13210 or stateNo()==3210 or stateNo()==4510;local actorTime=time()
   player(target)
   if stateNo()==8253 then held=true;if math.abs(posY())>.1 then badPose=true end end
   if stateNo()==8252 then dazed=true;if math.abs(posY())>.1 then badPose=true end end
   if stateNo()==8251 then
    kneeling=true
    if time()>1 and (anim()~=(_G['var'](45)==1 and 10010 or 10) or math.abs(posY())>.1) then badPose=true end
   end
   if stateNo()==8262 then aftermath=true;if math.abs(posY())>.1 then badPose=true end end
   if life()~=previousLife then changes=changes+1;previousLife=life() end
   if executing and actorTime<350 and life()~=1000 then early=true end
  end
 end
 if tick==14 and index==1 then screenshot() end
 if tick>=c.length then
  player(actor);local actorFinal=stateNo();local af=_G['var'](45)
  player(target);local targetFinal=stateNo();local damage=1000-life();local tf=_G['var'](45)
  local ok
  if c.toggle then ok=revealed and returned
  else
   local base=actor==2 and c.form==0 and (c.pulse==5 and 4410 or 4510) or (c.pulse==5 and 3010 or 3210)+c.form*10000
   ok=#violations==0 and damage==c.damage and seen[tostring(base)] and actorFinal==(af==1 and 10000 or 0) and targetFinal==(tf==1 and 10000 or 0)
   if c.pulse==6 then
    ok=ok and not badPose and not early and changes==1
    if c.actor==2 and c.form==1 then ok=ok and kneeling and aftermath else ok=ok and held end
    if c.actor==2 and c.form==0 then ok=ok and dazed and aftermath end
   end
  end
  table.insert(report.checks,{name=c.name,passed=ok==true,damage=damage,actorFinal=actorFinal,targetFinal=targetFinal,violations=violations,revealed=revealed,returned=returned,kneeling=kneeling,aftermath=aftermath,badPose=badPose,earlyDamage=early,damageChanges=changes,held=held,dazed=dazed})
  print('PAIRED_MATCH '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
