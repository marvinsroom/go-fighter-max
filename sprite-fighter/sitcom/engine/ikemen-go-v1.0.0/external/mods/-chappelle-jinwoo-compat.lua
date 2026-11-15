
local cases={{name='Shadow 1 incoming throw',pulse=7,expected=110,form=1},{name='Shadow 2 incoming throw',pulse=7,expected=110,form=2},{name='Shadow 3 incoming throw',pulse=7,expected=110,form=3},{name='Shadow 4 incoming throw',pulse=7,expected=110,form=4}}
local index,tick=1,0
local report={status='Running',checks={}}
local violations={}
hook.add('loop','chappelle-jinwoo-compat',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/chappelle/jinwoo-compat-validation.json');print('CHAPPELLE_COMPAT_COMPLETE jinwoo');os.exit() end
 tick=tick+1
 if tick==1 then
  violations={};for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','down','guard','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(1);mapSet('test.form',1);player(2);mapSet('test.shadowform',c.form);changeState(9010)
 elseif tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 if tick>=24 then
  player(2);local group=spriteVar('group');local image=spriteVar('image')
  local ok=(group==51 and image>=44+(c.form-1)*8 and image<=47+(c.form-1)*8)
  if not ok and time()>1 and #violations<12 then table.insert(violations,{tick=tick,group=group,image=image,state=stateNo()}) end
 end
 if tick>=(c.pulse==6 and 440 or 280) then
  player(2);local received=1000-life();local ok=received==c.expected and stateNo()==0 and #violations==0
  table.insert(report.checks,{name=c.name,passed=ok,received=received,violations=violations});print('CHAPPELLE_COMPAT '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
