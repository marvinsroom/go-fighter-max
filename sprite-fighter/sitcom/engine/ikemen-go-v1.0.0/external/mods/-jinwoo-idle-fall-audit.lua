local n=0
local r={trace={}}
hook.add('loop','jinwoo-idle-audit',function()
 if not player(1) or roundState()~=2 then return end
 n=n+1
 local t={tick=n,state=stateNo(),animation=anim(),x=posX(),y=posY(),form=_G['var'](45),weapon=_G['var'](10)}
 if anim()~=6 then t.group=spriteVar('group') end
 table.insert(r.trace,t)
 if n%120==0 then screenshot();print('IDLE '..n..' state='..stateNo()..' anim='..anim()..' y='..posY()) end
 if n>=1200 then jsonEncode(r,'../../characters/jinwoo/idle-fall-audit.json');os.exit() end
end)
