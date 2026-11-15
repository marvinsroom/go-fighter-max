"""Publish native engine evidence in the shared character review."""
from baam_model import *
from fighter_review import write_review
from PIL import Image,ImageDraw
import hashlib,re

r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and r['failed']==0
assert r['runtime_sha256']==json.loads((S/'build-report.json').read_text())['runtime_sha256']
cases={}
for f in r['frames']:
    # Earlier fixtures set the form map before entering a forced base idle.
    # Keep those historical samples in the proof, but omit that invalid pre-roll
    # from ignition move previews. The real W transition and all active moves
    # used the correct appearance; idle/return/damage were explicitly retaken.
    if f['case_name'].startswith('Viole / ') and f['case_tick']<=20 and f['group']==62000:continue
    p=S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']
    with Image.open(p) as im:im.verify()
    cases.setdefault(f['case_name'],[]).append(dict(f,src=p.relative_to(S).as_posix()))
groups={k:[] for k in ['Ultimates','Entrance and forms','Combos','Base techniques','Viole techniques','Basics and movement']}
for name in cases:
    k='Ultimates' if 'Shinwonryu' in name else 'Entrance and forms' if name in ('Entrance','Transform into Viole','Return to base','Viole facing left','Interrupted awakening') else 'Combos' if any(x in name for x in ('Z Z Z','X X X','Z X C','Chain','chain')) else 'Base techniques' if name.startswith('Base / ') and any(m[4] in name for m in MOVES) else 'Viole techniques' if name.startswith('Viole / ') and any(m[4] in name for m in MOVES) else 'Basics and movement'
    groups[k].append(name)
art=S/'art/canonical-v2'
comparison=Image.new('RGB',(2500,1030),(20,29,43));pen=ImageDraw.Draw(comparison)
samples=[('Original Baam','movement-0'),('Viole','ignited-movement-0')]+[(f'Stage {i+1}',f'transition-spaced-{i}') for i in range(8)]
for j,(label,slug) in enumerate(samples):
    im=Image.open(art/'poses'/(slug+'.png')).convert('RGBA');assert im.height==424
    col,row=j%5,j//5;comparison.paste(im,(col*500+(500-im.width)//2,row*510+55),im)
    pen.text((col*500+15,row*510+15),label,fill='white');pen.line((col*500,row*510+479,col*500+499,row*510+479),fill=(130,172,200))
comparison.save(art/'scale-comparison.png')
style='<style>body{max-width:1200px;margin:35px auto;padding:20px;background:#111925;color:#edf2f8;font:17px/1.6 system-ui}img{max-width:100%;background:#253143}a{color:#9cdbff}section{margin:30px 0}</style>'
page='<!doctype html><html lang="en"><meta charset="utf-8"><title>Baam artwork</title>'+style+'<a href="../../review.html">Back to combat review</a><h1>Baam / Jue Viole Grace</h1><p>Built-in image generation. Original sheets, repair drafts and exact prompts are retained. Both requested appearances follow the official anime references: original short-haired Baam in the red waistcoat and long-haired Viole in the black FUG robe. Eight actual stages connect their hair and costume changes. Two cropped victory cells are excluded from gameplay and use full-body neutral drawings.</p><p><a href="https://tog-anime.com/1st/character/">Official original Baam reference</a> ? <a href="https://tog-anime.com/chara/">Official Viole reference</a></p>'
for slug in ['movement','combat','ignited-movement','ignited-combat','story-spaced','transition-spaced','effects','portrait']:
    page+=f'<section><h2>{slug}</h2><a href="{slug}.prompt.txt">Exact prompt</a><img src="{slug}.png" alt="Baam {slug}"></section>'
(art/'design-review.html').write_text(page+'</html>',encoding='utf-8')
assets={p.stem:dict(file=p.name,prompt=p.stem+'.prompt.txt',sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in art.glob('*.png') if (art/(p.stem+'.prompt.txt')).exists()}
(art/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen.imagegen',assets=assets,accepted_story='story-spaced.png',accepted_transition='transition-spaced.png',forms=['Original Baam','Jue Viole Grace'],identity_sources=['https://tog-anime.com/1st/character/','https://tog-anime.com/chara/'],reused_effects='../illustrated-v1/effects.png'),indent=2))
(S/'proportion-audit.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Baam proportions</title>'+style+'<a href="review.html">Back to combat review</a><h1>Consistent form scale</h1><img src="art/canonical-v2/scale-comparison.png" alt="Both forms and planted transition poses share the same registered height"><p>Both neutral form drawings and all eight planted awakening frames use424px body height at AIR scale0.125 with192x144 coordinates. Each bank preserves its anatomical scale for crouches, jumps and attacks.</p><img src="art/canonical-v2/transition-spaced.png" alt="Eight connected awakening stages"><p><a href="pose-registration.json">Compiled pose registrations</a></p></html>',encoding='utf-8')
combat=S/'art/combat-v3'
combat_page='<!doctype html><html lang="en"><meta charset="utf-8"><title>Baam combat and Endless Sky</title>'+style+'<a href="../../review.html">Back to native combat review</a><h1>Baam / Viole: Endless Sky</h1><p>Dedicated palm, piercer, counter, baang, butterfly and Thorn Wave choreography. The ultimate opens a Shinsu field, suspends its confirmed opponent, collapses the baang into a gravity well and erupts into a giant final discharge. Both characters remain in front of the effects. Blue-white for original Baam, crimson-black Thorn amplification for Viole.</p><p>48 additional full-body poses and16 new layered effects, generated with built-in imagegen. <a href="../canonical-v2/design-review.html">Original likeness and transformation art</a>.</p>'
if (combat/'native-ultimate-preview.png').exists():combat_page+='<img src="native-ultimate-preview.png" alt="Native game captures of the Shinsu field, suspension, amplification and final discharge in both appearances">'
for slug in ('techniques','viole-techniques','ultimate','effects'):
    combat_page+=f'<section><h2>{slug}</h2><a href="{slug}.prompt.txt">Exact prompt</a><img src="{slug}.png" alt="Baam {slug}"></section>'
(combat/'design-review.html').write_text(combat_page+'</html>',encoding='utf-8')
(combat/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen.imagegen',reference='../canonical-v2/likeness-comparison.png',requests='generation-requests.json',assets={p.stem:dict(file=p.name,prompt=p.stem+'.prompt.txt',sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in combat.glob('*.png') if (combat/(p.stem+'.prompt.txt')).exists()}),indent=2))
data=dict(passed=r['passed'],cases=cases,groups={k:v for k,v in groups.items() if v},revision=hashlib.sha256(json.dumps(r).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.BAAM_REVIEW='+json.dumps(data)+';')
write_review('baam',data=data)
for slug in ('jin-mori','vikir'):
    p=S.parent/slug/'review.html';text=p.read_text(encoding='utf-8')
    if '../baam/review.html' not in text:p.write_text(text.replace('</nav>','<a href="../baam/review.html">Baam</a></nav>',1),encoding='utf-8')
print('BAAM_PACKAGE',len(cases),'clips;',len(r['frames']),'captures')
