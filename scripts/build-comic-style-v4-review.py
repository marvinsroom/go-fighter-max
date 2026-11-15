"""Publish honest visual progress separately from mechanical game validation."""
from comic_identity_v3 import *
import json,html,hashlib
from PIL import Image

root=R/'sprite-fighter/face-audit'
requests=json.loads((R/'.tmp/comic-style-v4-requests.json').read_text())
progress=json.loads((REF/'style-v4-progress.json').read_text())
cards=[]
def rel(p):return '../'+p.relative_to(root.parent).as_posix()
for slug,spec in SPECS.items():
 f=C/slug;a=f/'art/comic-style-v4';old=f/'archive/before-comic-style-v4/art'
 relevant=[q for q in requests if q['slug']==slug]
 generated=[]
 for q in relevant:
  p=Path(q['destination']);meta=p.with_suffix('.generation.json')
  if p.exists() and meta.exists() and json.loads(meta.read_text()).get('layout_validation',{}).get('status')=='PASS':generated.append(q)
 record=progress['fighters'][slug];record['generated']=len(generated)
 if record['status']=='pending' and generated:record['status']='candidate artwork; visual and native checks pending'
 selected=next((q for q in generated if q['kind'] in ('movement','body-00')),None)
 images=[(REF/(spec['refs'][0]+'.png'),'Comic reference')]
 if selected:
  k=selected['kind'];preview=a/'extracted'/(k+'-00.png');prior=old/'extracted'/(k+'-00.png')
  if prior.exists():images.append((prior,'Previous first pose'))
  if preview.exists():images.append((preview,'New first pose'))
 figures=''.join(f'<figure><img src="{rel(p)}" alt="{html.escape(label)}"><figcaption>{html.escape(label)}</figcaption></figure>' for p,label in images)
 sections=[]
 native_review=a/'native-contact.jpg'
 if record['status']=='Complete' and native_review.exists():
  sections.append('<section><h2>Installed game captures</h2><img class="atlas" src="native-contact.jpg" alt="Current installed sprites captured in the game"><p><a href="native-contact.json">Capture provenance</a> · <a href="visual-review.json">Visual review record</a></p></section>')
 for q in generated:
  p=Path(q['destination']);sections.append(f'<section><h2>{html.escape(q["kind"])}</h2><img class="atlas" src="{p.name}" alt="Full {html.escape(q["kind"])} sheet"><p><a href="{p.stem}.prompt.txt">Exact prompt</a> · <a href="{p.stem}.generation.json">Generation record</a></p></section>')
 if selected:
  gallery=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{spec["name"]} artwork correction</title><style>body{{max-width:1400px;margin:auto;padding:24px;background:#151b27;color:#eef1f7;font:17px/1.6 system-ui}}a{{color:#b4d9ff}}.atlas{{width:100%;background:#414855}}section{{margin:32px 0}}</style><h1>{spec["name"]} artwork correction</h1><p>{record["status"]}. {len(generated)}/{len(relevant)} body sheets saved. Generated artwork is shown for visual judgment; layout and gameplay checks do not prove comic likeness.</p><p><a href="../../../../face-audit/style-v4-review.html#{slug}">Roster comparison</a> · <a href="../../review.html">Installed animation review</a></p>'+''.join(sections)+'</html>'
  (a/'design-review.html').write_text(gallery,encoding='utf-8')
 link=f'<a href="{rel(a/"design-review.html")}">New complete body sheets</a>' if selected else 'New sheets pending'
 cards.append(f'<article id="{slug}"><h2>{spec["name"]}</h2><p>{html.escape(record["status"])} · {len(generated)}/{len(relevant)} sheets saved</p><div class="images">{figures}</div><p>{link} · <a href="{rel(f/"review.html")}">Installed animation review</a></p></article>')
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roster artwork correction</title><style>body{margin:0;background:#111824;color:#eef2fa;font:17px/1.6 system-ui}main{max-width:1450px;margin:auto;padding:24px}a{color:#b3d8ff}article{padding:20px;margin:24px 0;background:#202c3c;border-radius:12px}.images{display:flex;gap:16px;flex-wrap:wrap}figure{margin:0;flex:1 1 250px}img{width:100%;height:340px;object-fit:contain;background:#414855}figcaption{color:#c6d1e0}</style><main><h1>Roster artwork correction</h1><p>Reworking the body sprites to restore each comic’s face and proportions, reduce glossy rendering and keep forms distinct. The stronger portraits are preserved. Current progress is shown below; saved candidates are separate from installed gameplay artwork.</p><p><a href="review.html">Previous comic comparison and game checks</a></p>'+''.join(cards)+'</main></html>'
if progress.get('status')=='Complete':
 start=page.index('<p>Reworking the body sprites')
 end=page.index('</p>',start)+4
 page=page[:start]+'<p>All fourteen fighters now use the revised body artwork: flatter shadows, simpler folds and distinct comic faces and forms. All 64 sheets are installed and visually reviewed, with fresh game captures and browser checks. The stronger portraits and gameplay are preserved. Compare the previous and current sprites below.</p>'+page[end:]
(root/'style-v4-review.html').write_text(page,encoding='utf-8')
from stature_review_banner import update as update_stature_banner
update_stature_banner(root/'style-v4-review.html')
(REF/'style-v4-progress.json').write_text(json.dumps(progress,indent=2))
print('V4_REVIEW',sum(v['generated'] for v in progress['fighters'].values()),'of',len(requests),'sheets')
