"""Install audited comic sheets, retaining the rejected sources and native files."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
from isolated_sprite_atlas import extract
from PIL import Image
import shutil,json,sys,hashlib,subprocess,re
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
for slug in sys.argv[1:]:
 p=PROFILES[slug];f=C/slug;new=f/'art/comic-identity-v3';old=f/'art/illustrated-v1';backup=f/'archive/before-comic-identity-v3'
 for kind in ('movement','combat','story'):
  layout=p.get('art_layouts',{}).get(kind,{})
  extract(new/(kind+'.png'),layout.get('columns',4),layout.get('rows',4))
 assert Image.open(new/'portrait.png').getextrema()[3][0]==0
 if not backup.exists():
  backup.mkdir(parents=True)
  shutil.copytree(old,backup/'art')
  native=backup/'runtime';native.mkdir()
  for x in (E/p['id']).iterdir():
   if x.suffix in ('.sff','.cns','.cmd','.air','.snd','.zss','.def'):shutil.copy2(x,native/x.name)
  for n in ('review.html','build-report.json','runtime-validation.json','viewer-validation.json','startup-validation.json'):
   if (f/n).exists():shutil.copy2(f/n,backup/n)
 for kind in ('movement','combat','story','portrait'):
  shutil.copy2(new/(kind+'.png'),old/(kind+'.png'))
  meta=json.loads((new/(kind+'.generation.json')).read_text(encoding='utf-8-sig'))
  (old/(kind+'.prompt.txt')).write_text(meta['prompt'],encoding='utf-8')
  shutil.copy2(new/(kind+'.generation.json'),old/(kind+'.generation.json'))
 subprocess.run([sys.executable,str(R/'scripts/build-manhwa-fighter.py'),slug],check=True,cwd=R)
 for x in (backup/'runtime').iterdir():
  if x.suffix in ('.cmd','.cns','.air','.snd','.zss'):
   before=x.read_bytes();after=(E/p['id']/x.name).read_bytes()
   if (R/'sprite-fighter/face-audit/identity-scale-v5/profiles.json').exists() and x.suffix=='.cns':
    # The user explicitly requested roster stature changes. Only native size
    # constants may differ; all state controllers still compare byte-for-byte.
    pattern=rb'(?im)^\s*(?:xscale|yscale)\s*=\s*[-+0-9.eE]+'
    before=re.sub(pattern,b'',before);after=re.sub(pattern,b'',after)
   assert before==after,('Unexpected gameplay change',slug,x.name)
 report=json.loads((f/'build-report.json').read_text());report['revision']='comic-identity-v3';report['comic_identity']=SPECS[slug]
 (f/'build-report.json').write_text(json.dumps(report,indent=2))
 print('COMIC_INSTALLED',slug,flush=True)
