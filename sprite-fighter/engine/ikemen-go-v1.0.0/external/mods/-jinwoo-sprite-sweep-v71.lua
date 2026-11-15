-- Jinwoo v71 sprite sweep: which body sprites each reachable move shows.
local OUT='../../characters/jinwoo-mugen/jus-playstyle-v71/'
local states={200,210,220,230,240,241,242,260,270,300,310,320,330,340,350,400,403,405,406,407,409,410,411,412,413,414,415,416,417,420,421,422,423,424,425,426,427,428,440,450,451,452,453,454,455,456,457,458,460,461,462,463,465,466,467,468,469,500,501,510,600,601,602,610,620,630,640,650,660,700,1000,1010,1011,1012,1013,1014,1020,1021,1022,1023,1024,1025,1030,1090,1100,1110,1120,1130,1140,1150,1160,1170,1200,1260,1290,1300,1400,1500,1600,1601,1602,1605,1610,1620,1621,1630,1631,1700,1740,1800,1900,1930,2000,2001,2200,2201,2270,2370,2400,2600,2620,2700,2800,2850,2900,2950,3000,3010,3020,3030,3100,3110,3120,3130,3200,3210,3220,3900,870100,870101,870102,876300,876310,879920,879960}
local report={status='RUNNING',moves={},helpers={}}
local pass,idx,t=1,0,0
local function save() jsonEncode(report,OUT..'sprite-sweep-v71.json') end
hook.add('loop','jinwoo-sweep-v71',function()
 if not player(1) or roundState()~=2 then return end
 setLife(1000);setPower(3000);player(2);setLife(1000);player(1)
 t=t+1
 if idx==0 or t>140 or (t>8 and (stateNo()==0 or stateNo()==11 or stateNo()==52) ) then
  idx=idx+1;t=0
  if idx>#states then
   if pass==1 then pass=2;idx=0;changeState(870220);t=-40;return end
   report.status='DONE';save();os.exit(0)
  end
  changeState(states[idx]);return
 end
 if t<0 then return end
 local key=(pass==1 and 'sword:' or 'dagger:')..states[idx]
 local m=report.moves[key] or {}
 local k=tostring(stateNo() or -1)..'|'..tostring(anim() or -1)..'|'..tostring(animElemNo(0) or -1)..'|'..tostring(var(10) or -1)..'|'..tostring(var(48) or -1)..'|'..tostring((posY() or 0)>-0.5 and 1 or 0)
 m[k]=(m[k] or 0)+1
 report.moves[key]=m
 local hk=report.helpers[key] or {}
 local count=numHelper()
 for j=0,count-1 do
  player(1)
  if helper(-1,j) then local okid,hid=pcall(id);local h=tostring(okid and hid or -1)..'|'..tostring(stateNo())..'|'..tostring(anim() or -1)..'|'..tostring(animElemNo(0) or -1);hk[h]=(hk[h] or 0)+1 end
 end
 player(1)
 report.helpers[key]=hk
 if t%40==0 then save() end
end)
