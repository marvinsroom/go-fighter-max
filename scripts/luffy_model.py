"""TheCube Luffy source forms and explicit imported command routes."""
from pathlib import Path
from ichigo_model import actions

FORMS=[dict(id=0,slug='base',name='Base Luffy',base=0,height=66),dict(id=1,slug='boundman',name='Gear 4 Boundman',base=2000,height=76),dict(id=2,slug='snakeman',name='Gear 4 Snakeman',base=4000,height=78),dict(id=3,slug='nightmare',name='Nightmare',base=6000,height=86),dict(id=4,slug='gear-five',name='Gear 5 Nika',base=70000,height=72)]
FLAGS={0:(0,0,0,0),1:(2,0,0,0),2:(0,1,0,0),3:(0,0,1,0),4:(0,0,0,1)}
NORMALS={0:([200,300,400],[600,610,800]),1:([2200,2300,2400],[2600,2610,2620]),2:([4200,4300,4400],[4600,4610,4630]),3:([6200,6300,6400],[6600,6605,6610]),4:([70200,70220,70235],[70200,70220,70236])}
MOVES={
0:[('Red Hawk',1000,1000),('Jet Rifle',1100,1000),('Conqueror Haki',1200,1000),('Observation Haki',1300,1000),('Eagle Bazooka',1400,1500)],
1:[('Kong Gun',41000,1000),('Rhino Schneider',42000,1000),('Culverin',44000,1000),('Boundman Taunt',45000,1000),('Leo Bazooka',43000,2000)],
2:[('Jet Culverin',4999,1000),('Leg Culverin',41499,1000),('Double Culverins',41649,1500),('Jet Python',41849,1000),('Jet Python Barrage',42500,2500),('Left Arm Python',41950,2000),('Culverin Gatling',43550,1500),('Deformed Python',43500,2500)],
3:[('Nightmare Arrow',641000,1000),('Nightmare Fireball',644000,1000),('Nightmare Dash Cut',61204,1000),('Nightmare Gatling',64998,1850),('Nightmare Storm',64300,2000),('Nightmare Elephant Gun',640000,2000),('Nightmare Sword',6920,2300),('Nightmare Giant Rifle',6925,2300),('Nightmare Ultra Slash',66315,3000)],
4:[('Rubber Ray',71000,1000),('Giant Stomp',71150,1000),('Rolling the World',71170,1000),('Giant Assault',71682,1000),('Giant Hand',71350,2000),('Giant Throw',71550,1000),('Giant Head',71560,1000),('Se Desconocieron',71570,1000),('Giant Lift',71615,1000)]}
SUPERS={0:('Hawk Gatling',1500,1500),1:('Kong Organ',46000,1500),2:('Black Mamba',42950,2000),3:('Nightmare Giant Gatling',66345,3000),4:('Sky Fury',71500,2000)}
ULTIMATES={0:('Tankman Cannonball',13600,1000),1:('King Kong Gun',3300,3000),2:('King Cobra',43005,3000),3:('Nightmare Elephant Gatling',66300,3000),4:('Bajrang Gun',73000,3000)}
INPUTS=['x','/$B,x','/$F,x','/$D,x','/$D,/$F,x','/$D,/$B,x','d','/$B,d','/$F,d','/$D,d']
def routes():
 result=[]
 for form in FORMS:
  fid=form['id']
  for i,(name,state,cost) in enumerate(MOVES[fid],1):result.append(dict(form=fid,name=name,state=state,cost=cost,command=f'luffy_skill{i}',input=INPUTS[i-1],category='Skills'))
  for category,table,command,button in [('Supers',SUPERS,'luffy_super','y'),('Ultimates',ULTIMATES,'luffy_ultimate','z')]:
   name,state,cost=table[fid];result.append(dict(form=fid,name=name,state=state,cost=cost,command=command,input=button,category=category))
 return result
def source_folder(root):return Path(root)/'sprite-fighter/characters/luffy/source/upstream/TC_Luffy_All_Forms'
