"""Make editable lossless pose templates from the five established native fighters."""
from comic_identity_v3 import *
from mugen_sff import Sff
from PIL import Image
import json,hashlib,math,re
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
requests=[]
for slug,engine,file in [('baam','baam','baam.sff'),('jin-mori','jin_mori','jin_mori.sff'),('vikir','vikir','vikir.sff'),('pyowol','pyowol','pyowol.sff'),('jinwoo','jinwoo','spr.sff')]:
 p=SPECS[slug];art=C/slug/'art/comic-identity-v3';art.mkdir(exist_ok=True);templates=art/'templates';templates.mkdir(exist_ok=True)
 sff=Sff(E/engine/file)
 if slug=='baam':keys=[k for k in sff.keys if k[0] in [62000,62001,62100,62101,62200,62300,62400,62500,62600]]
 elif slug=='jin-mori':keys=[k for k in sff.keys if k[0] in [62000,62001,62002,62300,62301,62302,62304]]
 elif slug=='vikir':
  data=json.loads((C/slug/'build-report.json').read_text());keys=[(v['group'],v['number']) for k,v in data['poses'].items() if re.fullmatch('[mcnkabprs][0-9]+',k)]
 elif slug=='pyowol':keys=[k for k in sff.keys if k[0]==50]
 else:
  data=json.loads((C/slug/'validation/proportions-art.json').read_text());keys=[(v['group'],v['number']) for v in data['entries'] if v['actor']=='Jinwoo']
 frames=[];seen={}
 for key in sorted(set(keys)):
  index=sff.keys[key];im=sff.decode(index);digest=hashlib.sha256(im.tobytes()).hexdigest();h=sff.headers[index]
  if digest in seen:frames[seen[digest]]['keys'].append(list(key));continue
  seen[digest]=len(frames);bound=im.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox();assert bound
  png=templates/('source-'+str(len(frames)).zfill(3)+'.png');im.save(png)
  frames.append(dict(keys=[list(key)],source=str(png),rgba_sha256=digest,size=im.size,axis=h[4:6],bounds=bound))
 pages=[]
 for start in range(0,len(frames),16):
  chunk=frames[start:start+16];rows=math.ceil(len(chunk)/4);cols=min(4,len(chunk));kind='body-'+str(start//16).zfill(2)
  canvas=Image.new('RGBA',(cols*480,rows*560))
  for i,f in enumerate(chunk):
   im=Image.open(f['source']).crop(f['bounds']);im.thumbnail((360,440));canvas.alpha_composite(im,(i%cols*480+(480-im.width)//2,i//cols*560+(560-im.height)//2))
  target=templates/(kind+'.png');canvas.save(target)
  refs=[str(REF/(n+'.png')) for n in p['refs']]
  if slug=='baam':refs.append(str(REF/'viole.png'))
  prompt='Use case: precise-object-edit. First image(s) are the ORIGINAL COMIC likeness references. LAST image is an existing game POSE TEMPLATE ONLY; its generic face is wrong. Correct '+p['name']+' to the ACTUAL COMIC face and hair in EVERY body drawing. '+p['identity']+' Preserve each original pose, weapon, full body anatomy, facing and exact costume/form from the last image. Preserve masks when a form wears a mask; fix all exposed faces. '+('The long-haired black-clothed figures are VIOLE: match the additional SIU Viole panel with eyes concealed by broad black bangs and simple black high-collar top/red-white FUG circles. Short-haired figures are early Baam. Never mix their head/hair between forms. ' if slug=='baam' else '')+('Keep green goggles on base Mori and gold circlet/tiger pelt/staff on Monkey King, in the same cells. Same youthful comic face in both, same anatomy; transition poses must remain gradual. ' if slug=='jin-mori' else '')+'Use the original comic artist\'s specific eye shapes, brows, nose and cheek contours, simple ink contours and flat cel shading. Do NOT beautify into another glossy anime character. EXACTLY '+str(len(chunk))+' isolated COMPLETE FULL BODY drawings, STRICT '+str(cols)+' columns by '+str(rows)+' rows, identical row-major order to template. No added or missing figures. HUGE transparent gutters and margins; hair, weapons, companions, robe and both feet completely inside each cell. No scenery, labels, text or extra VFX. TRUE TRANSPARENT background.'
  (art/(kind+'.prompt.txt')).write_text(prompt,encoding='utf-8')
  page=dict(slug=slug,kind=kind,columns=cols,rows=rows,count=len(chunk),frames=chunk,prompt=prompt,references=refs+[str(target)],destination=str(art/(kind+'.png')))
  pages.append(page);requests.append(page)
 (art/'runtime-templates.json').write_text(json.dumps(dict(engine=engine,sff=file,baseline_sha256=hashlib.sha256((E/engine/file).read_bytes()).hexdigest(),pages=pages),indent=2));print('LEGACY_COMIC',slug,len(frames),'unique bodies',len(pages),'pages',flush=True)
(R/'.tmp/comic-legacy-requests.json').write_text(json.dumps(requests,indent=2))
