"""Identify actor drawings through root state routes, retaining helper effects."""
import re,json
from collections import defaultdict,Counter
from ichigo_model import FORMS,actions,source_folder

def build(root):
 u=source_folder(root);air=actions((u/'Ichigo.air').read_text(encoding='cp1252',errors='replace'))
 states={}
 files=['add004basic.reb1','common1.cns','IA.cns','Clash.cns','Especiales.cns','Supers.cns','Bankai.cns','Mask.cns','Vasto Lorde.cns','Mugetsu.cns','TYBW.cns']
 for file in files:
  for block in re.split(r'(?=^\[Statedef\s+)',(u/file).read_text(encoding='cp1252',errors='replace'),flags=re.I|re.M):
   m=re.match(r'\[Statedef\s+(-?\d+)\]',block,re.I)
   if m:states[int(m[1])]=block
 def number(text):
  m=re.match(r'\s*(\d+)\s*(?:;.*)?$',text)
  return int(m[1]) if m else None
 seed={0,5,10,11,12,20,21,40,41,45,50,51,52,100,105,120,130,140,150,170,180,190,195,5000,5010,5020,5030,5040,5050,5060,5070,5080,5100,5110,5120,5200,5210,5300,5500}
 cmd=(u/'Ichigo.cmd').read_text(encoding='cp1252',errors='replace')
 for block in re.split(r'(?=^\[State\s)',cmd,flags=re.I|re.M):
  if re.search(r'^type\s*=\s*ChangeState',block,re.I|re.M):
   m=re.search(r'^value\s*=\s*(\d+)\s*$',block,re.M|re.I)
   if m:seed.add(int(m[1]))
 reachable=set();queue=list(seed)
 while queue:
  n=queue.pop()
  if n in reachable:continue
  reachable.add(n)
  for block in re.split(r'(?=^\[State\s)',states.get(n,''),flags=re.I|re.M)[1:]:
   if re.search(r'^type\s*=\s*ChangeState',block,re.I|re.M):
    m=re.search(r'^value\s*=([^\n]+)',block,re.M|re.I)
    if m and number(m[1]) is not None:queue.append(number(m[1]))
   for m in re.finditer(r'^p1stateno\s*=([^\n]+)',block,re.M|re.I):
    if number(m[1]) is not None:queue.append(number(m[1]))
 root_actions=set()
 for n in reachable:
  chunks=re.split(r'(?=^\[State\s)',states.get(n,''),flags=re.I|re.M)
  for i,block in enumerate(chunks):
   key='anim' if i==0 else 'value'
   if i and not re.search(r'^type\s*=\s*ChangeAnim\s*$',block,re.I|re.M):continue
   for m in re.finditer(r'^'+key+r'\s*=([^\n]+)',block,re.M|re.I):
    if number(m[1]) is not None:root_actions.add(number(m[1]))
 # Shared state animations use variable offsets. Each form's entire locomotion,
 # normals, and hurt bands are explicit root actions even without literal refs.
 for f in FORMS:
  base=f['base'];root_actions.update(a for a in air if base<=a<base+1000)
  hurt=0 if not base else base+1000
  root_actions.update(a for a in air if hurt+5000<=a<hurt+6000) if not base else root_actions.update(a for a in air if hurt<=a<hurt+1000)
 def formof(a):
  if 60000<=a<60020:return a-60000
  if a>=100000:a//=10
  for f in reversed(FORMS):
   if f['base'] and f['base']<=a<f['base']+2000:return f['id']
  return 0
 votes=defaultdict(Counter);posevotes=defaultdict(Counter);record=[]
 for a in sorted(root_actions):
  rows=air.get(a,[]);form=formof(a);base=next(f['base'] for f in FORMS if f['id']==form)
  off=a-base
  for i,row in enumerate(rows):
   key=row['key']
   if key[0]<0 or key==(9999,0):continue
   weight=10 if off<200 and off>=0 else 1
   votes[key][form]+=weight
   t=i/max(1,len(rows)-1)
   if off in (0,5):pose=i%2
   elif off in (10,11,12):pose=4
   elif off in (20,21):pose=2+i%2
   elif off in (40,41,45,50,51):pose=5
   elif off in (52,100,105):pose=6 if off!=52 else 7
   elif (5000<=a<6000) or (base and base+1000<=a<base+2000):pose=15 if a%1000>=100 else 14
   elif a in (195,196,197) or off in (950,951):pose=12
   elif off<200 and off>=0:pose=0
   else:pose=[8,9,10,11][min(3,int(t*4))]
   posevotes[key][pose]+=weight
  record.append(dict(action=a,form=form,frames=len(rows)))
 mapping={key:(v.most_common(1)[0][0],posevotes[key].most_common(1)[0][0]) for key,v in votes.items()}
 return mapping,dict(reachable_states=sorted(reachable),root_actions=record)
