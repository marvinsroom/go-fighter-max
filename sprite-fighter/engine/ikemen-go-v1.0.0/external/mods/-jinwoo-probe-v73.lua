local OUT='../../characters/jinwoo-mugen/proportions-v73/'
local r={}
local t=0
hook.add('loop','probe',function()
 if not player(1) or roundState()~=2 then return end
 t=t+1
 if t==5 then
  r.setPosX=tostring(type(setPosX)); r.setPos=tostring(type(setPos)); r.setFacing=tostring(type(setFacing)); r.assertInput=tostring(type(assertInput)); r.setAILevel=tostring(type(setAILevel)); r.velSet=tostring(type(velSet)); r.posSet=tostring(type(posSet))
  r.x0=posX()
  local ok,err=pcall(function() setPosX(-60) end); r.setPosX_call=tostring(ok)..' '..tostring(err)
 end
 if t==8 then r.x1=posX(); jsonEncode(r,OUT..'probe.json'); os.exit(0) end
end)
