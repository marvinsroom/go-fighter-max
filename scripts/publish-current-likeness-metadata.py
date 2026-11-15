"""Keep current artwork galleries, extracted poses and provenance in sync."""
from pathlib import Path
import json,hashlib,shutil,sys,html
from comic_identity_v3 import SPECS
R=Path(__file__).resolve().parents[1]
for slug in sys.argv[1:]:
 f=R/'sprite-fighter/characters'/slug;build=json.loads((f/'build-report.json').read_text());review=R/build['visual_review'];a=review.parent;active=f/'art/comic-identity-v3';record=json.loads(review.read_text());assert record['status']=='Reviewed'
 build['comic_identity']=SPECS[slug];(f/'build-report.json').write_text(json.dumps(build,indent=2))
 extracted=active/'extracted';extracted.mkdir(exist_ok=True)
 for p in (a/'extracted').glob('*.png'):shutil.copy2(p,extracted/p.name)
 assets={}
 for kind in ('movement','combat','story','portrait'):
  p=active/(kind+'.png');digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest==record['assets'][p.name]
  assets[kind]=dict(file=p.name,sha256=digest,prompt=kind+'.prompt.txt',generation=kind+'.generation.json')
 (active/'provenance.json').write_text(json.dumps(dict(revision=a.name,tool='built-in image_gen.imagegen',visual_review=str(review.relative_to(R)),assets=assets),indent=2))
 reference='jin-mu-won-panel.jpg' if slug=='jin-mu-won' else 'eugene-adult-comic.jpg'
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Current comic faces</title><style>body{max-width:1300px;margin:auto;padding:24px;background:#111824;color:#eef4ff;font:17px/1.6 system-ui}a{color:#b6d9ff}img{display:block;max-width:100%;background:#354352}section{margin:32px 0}.reference{max-height:500px}</style><a href="../../review.html">Current moves</a> | <a href="../../../../face-audit/identity-scale-v5/review.html#'+slug+'">Comic reference comparison</a><h1>'+html.escape(slug.replace('-',' ').title())+' comic face correction</h1><p>Original comic facial construction guides the revised portraits and all body poses. Built-in image generation; exact prompts and original tool records are retained below.</p><img class="reference" src="../../../../face-audit/identity-scale-v5/references/'+reference+'" alt="Original comic facial reference">'
 for kind in assets:
  page+='<section><h2>'+kind+'</h2><a href="'+kind+'.prompt.txt">Exact prompt</a> | <a href="'+kind+'.generation.json">Generation record</a><img src="'+kind+'.png" alt="Corrected '+kind+'"></section>'
 page+='</html>'
 for folder in (a,active):(folder/'design-review.html').write_text(page,encoding='utf-8')
 print('CURRENT_LIKENESS_METADATA',slug,a.name)
