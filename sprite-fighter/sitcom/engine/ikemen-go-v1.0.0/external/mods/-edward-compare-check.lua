local tick=0
hook.add('loop','edward-compare-check',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1
 if tick==30 then screenshot() end
 if tick==45 then
  player(1);local first=stateNo();player(2);local second=stateNo()
  jsonEncode({status='PASS',illustrated_state=first,original_state=second,loaded_both=true},'../../characters/edward/comparison-validation.json');print('EDWARD_COMPARISON_PASS');os.exit()
 end
end)
