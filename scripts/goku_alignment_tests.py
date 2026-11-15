"""Native helper-position telemetry for hand and trajectory regression checks."""
from goku_alignment import BEAMS, FLIGHTS

def cases_for_alignment(cases,kind):
 selected=[c for c in cases if c['category']=='Basics' and c.get('state') in (400,620) or c['category'] in ('Skills','Supers','Ultimates') and ('Kame' in c['name'] or 'Energy Blast' in c['name'] or 'Ki Machinegun' in c['name'])]
 result=[]
 for c in selected:
  for direction in (1,-1):
   result.append(dict(c,name=c['name']+(' facing right' if direction==1 else ' facing left'),facing=direction,cornerX=-25*direction,length=min(c['length'],1600)))
 return result

def instrument(code,kind,lua):
 body='''
 player(1)
 local rx,ry=screenPosX(),screenPosY()
 local mx,my=tonumber(map('goku.muzzle_x')) or 0,tonumber(map('goku.muzzle_y')) or 0
 local rf=facing()
 local emitting=tonumber(map('goku.emitting')) or 0
 local helpers=numHelper()
 for j=0,helpers-1 do
  player(1)
  if helper(-1,j) and (beamStates[stateNo()] or flightStates[stateNo()]) and (time()<=4 or time()%6==0) and alignmentCount<128 then
   alignmentCount=alignmentCount+1
   table.insert(report.shots,{case_name=c.name,tick=tick,id=id(),state=stateNo(),age=time(),x=screenPosX(),y=screenPosY(),px=posX()+cameraPosX(),py=posY(),vx=velX(),vy=velY(),root_x=rx,root_y=ry,muzzle_x=mx,muzzle_y=my,facing=rf,shot_facing=facing(),emitting=emitting,angle=angle(),beam=beamStates[stateNo()] or false})
  end
 end
 player(1)
'''
 code=code.replace('local report={','local beamStates='+lua({s:True for s in BEAMS[kind]})+'\nlocal flightStates='+lua({s:True for s in FLIGHTS[kind]})+'\nlocal report={shots={},',1)
 code=code.replace('local index,tick,shot=','local alignmentCount=0\nlocal index,tick,shot=',1)
 code=code.replace(' if tick==1 then',' if tick==1 then\n alignmentCount=0',1)
 marker=' if tick>=c.length or galleryIdle>=60 then' if ' if tick>=c.length or galleryIdle>=60 then' in code else ' if tick>=c.length then'
 assert marker in code
 return code.replace(marker,body+'\n'+marker,1)
