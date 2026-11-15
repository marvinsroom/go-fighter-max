local previous=-999
hook.add('loop','chappelle-keyboard-trace',function()
 if not player(1) or roundState()~=2 then return end
 if stateNo()~=previous then previous=stateNo();print('P1_KEYBOARD_STATE '..previous..' power='..power()) end
end)
