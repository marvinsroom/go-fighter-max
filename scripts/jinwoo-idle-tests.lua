local poses=jsonDecode('../../characters/jinwoo/idle-test-sprites.json')
local cases={{name='Base idle',weapon=0},{name='First weapon idle',weapon=10000},{name='Second weapon idle',weapon=20000},{name='Knockdown and return to idle',weapon=0,hit=true}}
local report={status='Running',checks={},frames={},capture_directory='idle-v10',runtime_sha256=jsonDecode('../../characters/jinwoo/idle-test-build.json')}
local index,tick,shot=1,0,0
local seen,keys,violations,minLife,pending,trace
hook.add('loop','idle-frame-regression',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/jinwoo/replays/idle-v10/Jinwoo_hybrid'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=cases[index]
 if not c then
  if pending then return end
  report.status='Complete';report.passed=0;report.failed=0
  for _,row in ipairs(report.checks) do if row.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/jinwoo/idle-native-validation.json');print('IDLE_COMPLETE '..report.passed..'/4');os.exit()
 end
 tick=tick+1
 if tick==1 then
  seen={};keys={};violations={};trace={};minLife=1000
  player(1);mapSet('jw.form',0);mapSet('jw.setup',1);mapSet('idle.weapon',c.weapon);changeState(879120);setLife(1000)
  player(2);mapSet('test.guard',0);mapSet('test.pulse',0);changeState(9000);setLife(1000)
 elseif tick==40 and c.hit then player(2);changeState(9014) end
 player(1)
 if tick>8 then
  seen[tostring(stateNo())]=true;minLife=math.min(minLife,life())
  if stateNo()==0 then
   local key=spriteVar('group')..','..spriteVar('image');keys[key]=true
   local pose=poses[key]
   table.insert(trace,{tick=tick,key=key,pose=pose,y=posY()})
   if pose~='base:idle' or math.abs(posY())>.01 then table.insert(violations,{tick=tick,key=key,pose=pose,y=posY()}) end
  elseif not c.hit then table.insert(violations,{tick=tick,state=stateNo()}) end
 end
 if tick>8 and tick<=240 and tick%11==0 and not pending then
  screenshot();pending={index=shot+1,case_name=c.name,case_tick=tick,state=stateNo(),animation=anim()}
 end
 if tick>=600 then
  local count=0;for _ in pairs(keys) do count=count+1 end
  local ok=#violations==0 and count>=5 and stateNo()==0
  if c.hit then ok=ok and minLife<1000 and seen['5050'] and seen['5110'] and seen['5120'] end
  table.insert(report.checks,{name=c.name,passed=ok,states=seen,idle_sprites=count,violations=violations,received=1000-minLife,trace=trace})
  print('IDLE_TEST '..c.name..' '..tostring(ok)..' sprites='..count..' received='..(1000-minLife))
  jsonEncode(report,'../../characters/jinwoo/idle-native-validation.json');index=index+1;tick=0
 end
end)
