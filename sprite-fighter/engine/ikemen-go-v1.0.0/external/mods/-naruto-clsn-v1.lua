-- Hurtbox probe: show collision boxes and screenshot Jinwoo's missing moves frame by frame.
local OUT='../../characters/naruto-hurtbox-v1/'
local moves={240,300,1800,1900}
local t,i,start=0,0,0
local log={}
hook.add('loop','naruto-clsn-v1',function()
 if not player(1) or roundState()~=2 then return end
 t=t+1
 if t==2 then toggleClsnDisplay() end
 if t<10 then return end
 if start==0 then
  i=i+1
  if i>#moves then jsonEncode(log,OUT..'probe.json');os.exit(0) end
  player(2);setLife(1000);player(1);changeState(879990);start=t;return
 end
 local e=t-start
 if e==150 then changeState(moves[i]) end
 if e>150 then
  player(2);local mv=moveType();local st2=stateNo();local x2=posX();local y2=posY();local an2=anim();player(1)
  table.insert(log,{m=moves[i],e=e-150,anim=anim(),elem=animElemNo(0),st=stateNo(),p2=mv,st2=st2,an2=an2,dx=x2-posX(),y2=y2})
  if moves[i]==300 and (e-150)%3==0 and e-150<=24 then screenshot() end
 end
 if e>=210 then changeState(0);start=0 end
end)
