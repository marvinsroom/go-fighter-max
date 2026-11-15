"""Inventory imported artwork and form banks before illustrated conversion."""
from pathlib import Path
from collections import Counter,defaultdict
import json,re,hashlib,math
from PIL import Image,ImageDraw
from mugen_sff import Sff
from edward_assets import read_v1
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
for slug in ['naruto','saitama']:
 n=E/slug;a=R/'sprite-fighter/characters'/slug/'art/comic-style-v10';a.mkdir(parents=True,exist_ok=True);o=a/'audit';o.mkdir(exist_ok=True)
 sf=next(n.glob('*.sff'));raw=sf.read_bytes();version=raw[15]
 if version==1:sprites=read_v1(sf)
 else:
  source=Sff(sf);sprites=[dict(key=k,axis=source.headers[i][4:6],image=source.decode(i)) for k,i in source.keys.items()]
 groups=defaultdict(list)
 for s in sprites:groups[s['key'][0]].append(s)
 summary=[]
 for group,ss in sorted(groups.items()):
  ss.sort(key=lambda x:x['key'][1]);entry=dict(group=group,count=len(ss),sizes=Counter(str(s['image'].size) for s in ss).most_common(3),first_keys=[s['key'] for s in ss[:3]],unique=len(set(hashlib.sha256(s['image'].tobytes()).hexdigest() for s in ss)));summary.append(entry)
 sample=[(g,ss[i]) for g,ss in sorted(groups.items()) for i in sorted(set([0,len(ss)//2,len(ss)-1]))]
 for start in range(0,len(sample),64):
  page=sample[start:start+64];board=Image.new('RGB',(1600,math.ceil(len(page)/8)*150),'#25313f');d=ImageDraw.Draw(board)
  for i,(g,s) in enumerate(page):
   im=s['image'].copy();b=im.getbbox()
   if b:im=im.crop(b)
   im.thumbnail((185,120));x=(i%8)*200+(200-im.width)//2;y=(i//8)*150+122-im.height;board.paste(im,(x,y),im);d.text(((i%8)*200+5,(i//8)*150+126),str(s['key'])+' '+str(s['image'].size),fill='white')
  board.save(o/f'groups-{start//64:02d}.png')
 air=next(n.glob('*.air')).read_text(encoding='cp1252',errors='replace');actions=[]
 for m in re.finditer(r'(?ims)^\s*\[Begin Action\s+(\d+)\](.*?)(?=^\s*\[Begin Action|\Z)',air):
  keys=[]
  for ln in m[2].splitlines():
   f=re.match(r'^\s*(\d+)\s*,\s*(\d+)\s*,',ln)
   if f:keys.append(tuple(map(int,f.groups())))
  actions.append(dict(action=int(m[1]),keys=keys))
 report=dict(slug=slug,sff=str(sf.relative_to(R)),version=version,sprite_count=len(sprites),groups=summary,actions=actions)
 (o/'inventory.json').write_text(json.dumps(report,indent=2));print(slug,version,len(sprites),'sprites;',len(groups),'groups;',len(actions),'actions; contact pages',math.ceil(len(sample)/64),flush=True)
