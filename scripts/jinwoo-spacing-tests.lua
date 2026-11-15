local cases=jsonDecode('../../characters/jinwoo/spacing-test-cases.json')
local report={checks={},frames={},status='Running',capture_directory='spacing-v8-contact',scope='Ordinary attack body separation; native target-bound grab and nonattacking dissolve frames excluded'}
report.runtime_sha256=jsonDecode('../../characters/jinwoo/spacing-test-build.json')
local index,tick,shot=1,0,0
local samples,minGap,minLife,pending
hook.add('loop','shadow-contact',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/jinwoo/replays/spacing-v8/Jinwoo_hybrid'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=cases[index]
 if not c then
  if pending then return end
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/jinwoo/spacing-native-validation.json');print('SPACING_COMPLETE '..report.passed..'/'..#report.checks);os.exit()
 end
 tick=tick+1
 if tick==1 then
  samples={};minGap=10000;minLife=1000
  player(1);mapSet('jw.setup',1);mapSet('jw.form',0);mapSet('contact.seen',0);mapSet('contact.side',c.side);changeState(879000);setPower(3000)
  player(2);setLife(1000);mapSet('test.guard',0);mapSet('contact.wide',c.mode=='wide' and 1 or 0);mapSet('contact.side',c.side);mapSet('contact.distance',c.distance);changeState(9010)
 elseif tick==8 then player(1);changeState(879110)
 elseif tick==18 then player(2);if c.mode=='guard' then mapSet('test.guard',1) end
 elseif tick==20 then player(1);changeState(c.native and 879100+c.shadow or 870100+c.shadow)
 end
 player(1)
 if tick>21 and map('contact.seen')>0 and map('contact.attacking')>0 and map('contact.state')~=1340 and map('contact.age')>0 and map('contact.distance')>=0 and math.abs(map('contact.height'))<60 then
  local gap=map('contact.gap');minGap=math.min(minGap,gap)
  table.insert(samples,{tick=tick,gap=gap,state=map('contact.state')})
 end
 mapSet('contact.seen',0)
 if tick>21 and tick%20==0 and not pending then screenshot();pending={case=c.name,index=shot+1} end
 player(2);minLife=math.min(minLife,life())
 if tick>=170 then
  local damage=1000-minLife
  local ok=#samples>0 and minGap>=-0.1
  -- A wide push bar may extend beyond the damageable torso. Check separation
  -- there without lengthening a short claw attack to force an artificial hit.
  if not c.native and (c.mode=='near' or c.mode=='approach') and damage<=0 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,min_gap=minGap,damage=damage,samples=samples})
  print('SPACING '..c.name..' '..tostring(ok)..' gap='..minGap..' damage='..damage)
  jsonEncode(report,'../../characters/jinwoo/spacing-native-validation.json');index=index+1;tick=0
 end
end)
