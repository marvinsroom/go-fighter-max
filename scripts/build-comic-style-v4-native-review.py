"""Make diagnostic contact sheets from current native captures, never artwork substitutes."""
from comic_identity_v3 import *
from PIL import Image,ImageDraw
import json,sys,hashlib

for slug in sys.argv[1:]:
 f=C/slug;a=f/'art/comic-style-v4';proofpath=f/('validation/current.json' if slug=='jinwoo' else 'runtime-validation.json');proof=json.loads(proofpath.read_text())
 assert proof['status']=='Complete' and proof['failed']==0
 frames=proof['frames']
 if slug=='jin-mori':wanted=['Idle','Transform into Monkey King','Monkey King idle','Monkey King walking','Monkey King Azure Dragon','Monkey King ultimate','Return to Jin Mori','Entrance']
 elif slug=='baam':wanted=['Base / Idle','Viole / Idle','Transform into Viole','Base / Shinwonryu','Viole / Shinwonryu','Entrance']
 elif slug=='vikir':wanted=['Vikir idle','Night Hound idle','Academy idle','Night Hound walk','Academy walk','Night Hound / Night Hound: Crimson Execution','Academy / Night Hound: Crimson Execution','Intro']
 elif slug=='jinwoo':wanted=['Daggers stance','Greatsword stance','Greatsword walk','Mutilate ultimate','Greatsword King Domain ultimate','Greatsword Antares ultimate']
 elif slug=='pyowol':wanted=['Idle','Forward walk','Thread arrival intro','Soul-Reaping Thread','Heavenly Silk Prison','Reaper of the Drifting Moon']
 else:wanted=[]
 names=list(dict.fromkeys(x.get('case_name',x.get('case','Unknown')) for x in frames))
 selected=[]
 for title in wanted:
  name=next((n for n in names if n==title),next((n for n in names if title.lower() in n.lower()),None))
  if name and name not in selected:selected.append(name)
 if not selected:
  for keyword in ('idle','walk','intro','transform','prison','execution','ultimate','super','hound','academy','greatsword'):
   for n in names:
    if keyword in n.lower() and n not in selected:selected.append(n)
  selected=selected[:10]
 entries=[]
 for name in selected:
  candidates=[x for x in frames if x.get('case_name',x.get('case','Unknown'))==name]
  active=[x for x in candidates if x.get('state',0) not in (0,99000)] or candidates
  chosen=active[len(active)//2]
  if 'src' in chosen:p=f/chosen['src']
  elif 'file' in chosen:p=f/'replays'/chosen.get('capture_directory',proof['capture_directory'])/chosen['file']
  else:p=f/'replays'/proof['capture_directory']/('Jinwoo_hybrid%03d.png'%(chosen['index']-1))
  assert p.exists(),p
  entries.append(dict(case=name,file=str(p.relative_to(f)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),group=chosen.get('group'),drawing=chosen.get('drawing'),state=chosen.get('state')))
 page=Image.new('RGB',(1280,385*((len(entries)+1)//2)),(24,32,44));draw=ImageDraw.Draw(page)
 for i,entry in enumerate(entries):
  im=Image.open(f/entry['file']).convert('RGB');im.thumbnail((640,360));x=i%2*640;y=i//2*385;page.paste(im,(x,y+25));draw.text((x+10,y+5),entry['case'],fill='white')
 page.save(a/'native-contact.jpg')
 (a/'native-contact.json').write_text(json.dumps(dict(source=str(proofpath.relative_to(R)),runtime_sha256=proof.get('runtime_sha256',proof.get('runtime')),frames=entries),indent=2))
 print(slug,'NATIVE_CONTACT',len(entries),selected,flush=True)
