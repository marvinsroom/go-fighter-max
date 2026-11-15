"""GT Goku source forms, native routes and illustrated banks."""
from pathlib import Path
import re
from goku_model import valid, actions
R=Path(__file__).resolve().parents[1]
S=R/'sprite-fighter/characters/gt-goku'
U=S/'source/upstream/GokuGT'
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
O=E/'chars/gt_goku'
BANKS=['base-tail-v3','ss1-tail-v2','ss2','ss3-tail-v2','ss4']
FORMS=[dict(id=i,name=name,slug=slug,bank=i,flags=(i,0)) for i,(name,slug) in enumerate(zip(['GT Kid Goku','Super Saiyan','Super Saiyan 2','Super Saiyan 3','Super Saiyan 4'],BANKS))]
NORMALS={i:([offset+200,offset+300,400],[offset+600,offset+610,620]) for i,offset in enumerate([0,2000,11000,13000,15000])}
INPUTS={'SPECIAL 1':'x','SPECIAL 2':'/$B,x','SPECIAL 3':'/$F,x','SPECIAL 4':'/$D,x','SPECIAL 5':'y','SPECIAL 6':'/$D,/$F,x','SPECIAL 7':'d','SPECIAL 8':'/$B,d','SPECIAL 9':'/$F,d','SPECIAL 10':'/$D,d','SPECIAL 11':'/$F,y','SPECIAL 12':'/$B,y','SUPER1':'z'}

def routes():
 source='\n'.join(l.split(';',1)[0] for l in (U/'GokuGT.cmd').read_text(encoding='cp1252').splitlines())
 result=[]
 for block in re.split(r'(?=^\[State\s+)',source,flags=re.I|re.M):
  if not re.search(r'type\s*=\s*ChangeState',block,re.I):continue
  command=re.search(r'command\s*=\s*"(SPECIAL \d+|SUPER1)"',block,re.I)
  state=re.search(r'^value\s*=\s*(\d+)',block,re.I|re.M)
  if not command or not state:continue
  state=int(state[1]);native=command[1].upper()
  name=re.match(r'\[State[^,]*,\s*([^\]]+)',block,re.I)[1].strip()
  constraints=re.findall(r'^triggerall\s*=\s*([^\n]*var\([23]\)[^\n]*)',block,re.I|re.M)
  cost=re.search(r'power\s*>=\s*(\d+)',block,re.I);cost=int(cost[1]) if cost else 0
  air=bool(re.search(r'statetype\s*=\s*A',block,re.I))
  for f in FORMS:
   if all(valid(c,*f['flags']) for c in constraints):
    extra='life<=lifemax/2 && enemynear,life<=enemynear,lifemax/2' if state==3000 else ''
    if state==4000:extra='life>lifemax/2 || enemynear,life>enemynear,lifemax/2'
    result.append(dict(form=f['id'],name=name,state=state,cost=cost,command='goku_'+native.lower().replace(' ','_'),input=INPUTS[native],air=air,extra=extra,category='Ultimates' if native=='SUPER1' else 'Supers' if native=='SPECIAL 5' else 'Skills'))
 result.append(dict(form=4,name='Full Power',state=31600,cost=1500,command='goku_full_power',input='/$D,d',air=False,extra='var(3)=0',category='Skills'))
 return result
