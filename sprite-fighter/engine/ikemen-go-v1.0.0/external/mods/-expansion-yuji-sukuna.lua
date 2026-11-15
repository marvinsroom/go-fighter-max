local ticks=0
local report={status='Running',recording=false,scope='Original y command enters Sukuna, changes form bank, and returns to Yuji; no video or screenshots',states_seen={},forms_seen={}}
hook.add('loop','yuji-sukuna-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 if ticks==1 then setPower(3000) end
 mapSet('expansion.transform',ticks>=20 and ticks<=24 and 1 or 0)
 report.states_seen[tostring(stateNo())]=true
 report.forms_seen[tostring(var(11))]=true
 if var(11)==10000 then
  report.sukuna_seen=true
  report.sukuna_idle=report.sukuna_idle or stateNo()==0
 end
 if ticks>=200 and ticks<=204 then mapSet('expansion.transform',1) end
 if ticks>=300 then
  report.final_form=var(11)
  report.passed=report.sukuna_seen and report.sukuna_idle and report.states_seen['1300'] and report.states_seen['1310'] and var(11)==0
  report.status=report.passed and 'PASS' or 'FAIL'
  jsonEncode(report,'../../mugen-expansion/validation/yuji-sukuna.json')
  os.exit(report.passed and 0 or 1)
 end
end)
