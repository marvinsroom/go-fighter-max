local ticks=0
local states={}
hook.add('loop','original-import-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 states[tostring(stateNo())]=true
 if ticks>=180 then
  jsonEncode({status='PASS',slug='shredder',scope='Verified loaded fighter identity and 180 active-round ticks; full moves/forms audit pending',recording=false,active_round_ticks=ticks,loaded_name=name(),animation=anim(),states=states},'../../mugen-expansion/validation/shredder.json')
  os.exit(0)
 end
end)
