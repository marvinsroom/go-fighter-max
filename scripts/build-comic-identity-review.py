"""Publish source panels beside complete replacement sprites and current native proof."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
from PIL import Image,ImageDraw
import json,html,hashlib,shutil
O=R/'sprite-fighter/face-audit';S=O.parent;archive=O/'before-comic-identity-v3';archive.mkdir(exist_ok=True)
for n in ('review.html','audit.json','completion.json','viewer-validation.json'):
 if (O/n).exists() and not (archive/n).exists():shutil.copy2(O/n,archive/n)
cards=[];records=[]
def rel(path):return '../'+path.relative_to(S).as_posix()
for slug,p in SPECS.items():
 f=C/slug;a=f/'art/comic-identity-v3';ref=REF/(p['refs'][0]+'.png');portrait=a/'portrait.png'
 if not portrait.exists():continue
 sheets=sorted(x for x in a.glob('*.png') if '.rejected-' not in x.name)
 gallery='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(p['name'])+' comic redraws</title><style>body{max-width:1300px;margin:30px auto;padding:20px;background:#101825;color:#eef4ff;font:17px/1.6 system-ui}a{color:#a9dbff}img{max-width:100%;background:#28364a}section{margin:35px 0}</style><a href="../../review.html">Combat review</a> · <a href="../../../../face-audit/review.html">Comic comparisons</a><h1>'+html.escape(p['name'])+' comic redraws</h1><p>Current replacement artwork. Original generations, rejected drafts, exact prompts and the previous runtime are retained in the project.</p>'
 for sheet in sheets:
  prompt=a/(sheet.stem+'.prompt.txt');generation=a/(sheet.stem+'.generation.json')
  links=('<a href="'+prompt.name+'">Exact prompt</a> ' if prompt.exists() else '')+('<a href="'+generation.name+'">Generation record</a>' if generation.exists() else '')
  gallery+='<section><h2>'+html.escape(sheet.stem)+'</h2><p>'+links+'</p><img loading="lazy" src="'+sheet.name+'" alt="'+html.escape(p['name']+' '+sheet.stem)+'"></section>'
 (a/'design-review.html').write_text(gallery+'</html>',encoding='utf-8')
 (a/'provenance.json').write_text(json.dumps(dict(revision='comic-identity-v3',assets={x.stem:dict(file=x.name,sha256=hashlib.sha256(x.read_bytes()).hexdigest(),prompt=x.stem+'.prompt.txt',generation=x.stem+'.generation.json') for x in sheets if (a/(x.stem+'.generation.json')).exists()}),indent=2))
 source=json.loads((REF/(p['refs'][0]+'.source.json')).read_text())
 body=a/'extracted/movement-00.png'
 if not body.exists():body=a/'extracted/body-00-00.png'
 images=[(ref,'Original comic reference'),(portrait,'New portrait adaptation')]
 if body.exists():images.append((body,'Complete replacement body sprite'))
 runtime=f/'runtime-validation.json';installed=(a/'installed.json').exists() or (f/'build-report.json').exists() and json.loads((f/'build-report.json').read_text()).get('revision')=='comic-identity-v3'
 state='Installed; current native checks pending' if installed else 'New artwork; installation pending'
 proof=None
 if runtime.exists():
  proof=json.loads(runtime.read_text());build=json.loads((a/'installed.json').read_text()) if (a/'installed.json').exists() else json.loads((f/'build-report.json').read_text())
  if installed and proof.get('status')=='Complete' and proof.get('runtime_sha256')==build.get('runtime_sha256'):
   state=str(proof['passed'])+' native checks passed on this artwork'
   frames=proof.get('frames',[]);idle=next((v for v in frames if v.get('case_name')=='Idle'),next(iter(frames),None))
   if idle:
    capture=f/'replays'/idle.get('capture_directory',proof.get('capture_directory',''))/idle['file']
    if capture.exists():images.append((capture,'Current native game capture'))
 if slug=='jinwoo' and (a/'verification.json').exists():
  verified=json.loads((a/'verification.json').read_text());installed_report=json.loads((a/'installed.json').read_text())
  if verified['runtime_sha256']==installed_report['runtime_sha256']:
   state=str(verified['native_checks'])+' native checks passed on this artwork'
   current=json.loads((f/'validation/current.json').read_text())
   frame=next(iter(current['frames']),None)
   if frame:
    capture=f/frame.get('src',f"replays/{current['capture_directory']}/Jinwoo_hybrid{frame['index']-1:03d}.png")
    if capture.exists():images.append((capture,'Current native game capture'))
 figures=''.join('<figure><img loading="lazy" src="'+rel(im)+'" alt="'+label+'"><figcaption>'+label+'</figcaption></figure>' for im,label in images)
 promptlinks='<a href="'+rel(a/'design-review.html')+'">All current sprite sheets and generation records</a> '+' '.join('<a href="'+rel(x)+'">'+x.stem+'</a>' for x in sorted(a.glob('*.prompt.txt')))
 sourceurl=source.get('page') or source.get('image_url') or PROFILES.get(slug,{}).get('source','')
 sourcehtml=('<a href="'+html.escape(sourceurl)+'">Panel source</a> · ') if sourceurl else ''
 cards.append('<article id="'+slug+'"><h2>'+p['name']+'</h2><p class="state">'+state+'</p><div class="images">'+figures+'</div><p>'+html.escape(p['identity'])+'</p><p>'+sourcehtml+'<a href="../characters/'+slug+'/review.html">Combat review</a></p><details><summary>Exact artwork prompts</summary>'+promptlinks+'</details></article>')
 records.append(dict(slug=slug,name=p['name'],reference=str(ref.relative_to(S)),portrait_sha256=hashlib.sha256(portrait.read_bytes()).hexdigest(),status=state,source=source))
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Comic Sprite Redraws</title><style>body{margin:0;background:#101825;color:#eef4ff;font:17px/1.6 system-ui}main{max-width:1500px;margin:auto;padding:24px}a{color:#a9dbff}article{background:#1b293b;border:1px solid #3b4a60;padding:20px;margin:24px 0;border-radius:12px}.images{display:flex;flex-wrap:wrap;gap:16px}figure{flex:1 1 230px;margin:0;min-width:0}img{width:100%;height:340px;object-fit:contain;background:#28364a}figcaption{color:#bbcee5}.state{color:#c5dca5}details a{display:inline-block;margin:8px}</style><main><a href="../manhwa-roster.html">Fighter roster</a><h1>Comic sprite redraws</h1><p>The previous likeness pass was rejected. This pass uses actual comic panels to remake complete body sprites, clothing, hair and faces. Original panels are shown beside generated adaptations so you can judge the likeness. Publicly reposted panels are secondary references; publisher-posted images and official WEBTOON strips are identified in the source records. These adaptations are not extracted original animation frames.</p>'+''.join(cards)+'</main></html>'
if (REF/'style-v4-progress.json').exists():
 progress=json.loads((REF/'style-v4-progress.json').read_text())
 if progress.get('status')=='Complete':
  page=page.replace('<h1>Comic sprite redraws</h1>','<h1>Comic sprite redraws</h1><p><a href="style-v4-review.html">Current flatter comic artwork: before/after comparisons and full sheets</a></p>')
 if progress.get('status')!='Complete':
  page=page.replace('<h1>Comic sprite redraws</h1>','<h1>Comic sprite redraws</h1><p><strong>Body artwork correction in progress.</strong> Native checks below describe gameplay evidence; visual likeness is being reviewed separately. <a href="style-v4-review.html">See the new roster artwork and progress</a>.</p>')
(O/'review.html').write_text(page,encoding='utf-8');(O/'audit.json').write_text(json.dumps(dict(date='2026-10-21',revision='comic-identity-v3',fighters=records),indent=2));print('COMIC_REVIEW',len(records))
