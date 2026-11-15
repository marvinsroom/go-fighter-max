local tick,shot=0,0;local report={frames={}};local pending=nil
hook.add('loop','intro-audit',function()
 if not player(1) then return end
 tick=tick+1
 if pending then local f=io.open('../../characters/jinwoo/replays/intro-audit/Jinwoo_intro_audit'..string.format('%03d',shot)..'.png','rb');if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end end
 if tick%8==0 and not pending then screenshot();pending={index=shot+1,tick=tick,state=stateNo(),animation=anim(),time=time(),round=roundState()} end
 if tick>=500 then jsonEncode(report,'../../characters/jinwoo/intro-audit.json');os.exit() end
end)
