"""Imported Goku DBS V3.5 forms, source routes and illustrated asset banks."""
from pathlib import Path
import re
from ichigo_model import actions
R=Path(__file__).resolve().parents[1]
S=R/'sprite-fighter/characters/goku'
U=S/'source/candidates/lora/upstream/Goku'
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
O=E/'chars/goku'
FORMS=[dict(id=i,name=name,slug=slug,bank=bank,flags=flags) for i,(name,slug,bank,flags) in enumerate([
 ('Base Goku','base',0,(0,0)),('Kaioken','kaioken',0,(0,1)),
 ('Super Saiyan','ss1',1,(1,0)),('Super Saiyan 2','ss2',2,(2,0)),
 ('Super Saiyan 3','ss3',3,(3,0)),('Super Saiyan God','god',4,(4,0)),
 ('Super Saiyan Blue','blue',5,(5,0)),('Blue Kaioken','blue-kaioken',5,(5,1)),
 ('Blue Kaioken x10','blue-kaioken-x10',5,(5,2)),
 ('Ultra Instinct Omen','omen',6,(6,0)),('Mastered Ultra Instinct','mui',7,(7,0))])]
BANKS=['base','ss1','ss2','ss3','god','blue','omen','mui']
NORMALS={f['id']:([200,300,400],[600,610,620]) for f in FORMS}
INPUTS={'SPECIAL 1':'x','SPECIAL 2':'/$B,x','SPECIAL 3':'/$F,x','SPECIAL 4':'/$D,x','SPECIAL 5':'y','SPECIAL 6':'/$D,/$F,x','SPECIAL 7':'d','SUPER1':'z','SUPER2':'/$D,z'}

def valid(expression,form,power):
 expression=re.sub(r'var\(2\)',str(form),expression,flags=re.I)
 expression=re.sub(r'var\(3\)',str(power),expression,flags=re.I)
 expression=re.sub(r'(\d+)\s*=\s*\[(\d+),(\d+)\]',r'(\2 <= \1 <= \3)',expression)
 expression=expression.replace('||',' or ').replace('&&',' and ')
 expression=re.sub(r'(?<=[\d )])=(?!=)', '==',expression)
 return bool(eval(expression,{'__builtins__':{}},{}))

def routes():
 source=(U/'Goku.cmd').read_text(encoding='cp1252')
 source='\n'.join(l.split(';',1)[0] for l in source.splitlines())
 result=[]
 for block in re.split(r'(?=^\[State\s+)',source,flags=re.I|re.M):
  if not re.search(r'type\s*=\s*ChangeState',block,re.I):continue
  command=re.search(r'command\s*=\s*"(SPECIAL [1-7]|SUPER[12])"',block,re.I)
  if not command:continue
  state=re.search(r'^value\s*=\s*(\d+)',block,re.I|re.M)
  if not state:continue
  state=int(state[1]);native=command[1].upper()
  name=re.match(r'\[State[^,]*,\s*([^\]]+)',block,re.I)[1].strip()
  constraints=re.findall(r'^triggerall\s*=\s*([^\n]*var\([23]\)[^\n]*)',block,re.I|re.M)
  cost=re.search(r'power\s*>=\s*(\d+)',block,re.I)
  cost=int(cost[1]) if cost else 0
  airborne=bool(re.search(r'statetype\s*=\s*A',block,re.I))
  extra='numhelper(3054)=1' if state==3001 else ''
  for f in FORMS:
   if not all(valid(c,*f['flags']) for c in constraints):continue
   command='goku_'+native.lower().replace(' ','_');buttons=INPUTS[native]
   if state==33700 and f['id']==7:command='goku_meteor_rush';buttons='/$B,d'
   result.append(dict(form=f['id'],name=name,state=state,cost=cost,command=command,input=buttons,air=airborne,extra=extra,category='Ultimates' if native=='SUPER1' else 'Supers' if native in ('SUPER2','SPECIAL 5') else 'Skills'))
 # Preserve the source's two-stage Spirit Bomb: Z prepares, Z releases.
 result.insert(0,dict(form=0,name='Super Spirit Bomb: gather energy',state=3000,cost=500,command='goku_super1',input='z',air=False,extra='numhelper(3054)=0',category='Ultimates'))
 return result

if __name__=='__main__':
 import json
 print(json.dumps(routes(),indent=2))
