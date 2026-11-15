"""Package native captures and illustrated originals in the shared review UI."""
from jin_mori_assets import *
from fighter_review import write_review
import hashlib,re

report=json.loads((S/'runtime-validation.json').read_text())
assert report['status']=='Complete' and report['failed']==0,report.get('checks')
cases={}
for f in report['frames']:
    p=S/'replays'/f.get('capture_directory',report['capture_directory'])/f['file']
    with Image.open(p) as im:im.verify()
    cases.setdefault(f['case_name'],[]).append(dict(f,src=p.relative_to(S).as_posix()))
groups={}
for n in cases:
    group='Ultimates' if n in ('Monkey King','Monkey King facing left','Monkey King ultimate') else 'Entrance and forms' if n=='Entrance' or any(t in n.lower() for t in ('transform','return to jin')) else 'Combos' if any(t in n for t in ('Z Z Z','X X X','Z X C','Normal to Azure','Chain on guard','Chain whiff')) else 'Monkey King form' if n.startswith('Monkey King ') else 'Supers and counter' if any(n.startswith(t) for t in ('Moonlight','Black Tortoise','Azure','Triple','Twin','Blue Dragon')) else 'Normals' if any(t in n for t in ('chain','sweep')) else 'Movement and charge'
    groups.setdefault(group,[]).append(n)
groups={k:groups[k] for k in ('Ultimates','Entrance and forms','Combos','Monkey King form','Supers and counter','Normals','Movement and charge') if k in groups}
data=dict(passed=report['passed'],cases=cases,groups=groups,revision=hashlib.sha256(json.dumps(report).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.MORI_REVIEW='+json.dumps(data)+';',encoding='utf-8')
art=S/'art/illustrated-v1'
design='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jin Mori artwork</title><style>body{margin:30px auto;max-width:1100px;padding:20px;background:#101722;color:#edf1f5;font:17px/1.6 system-ui}a{color:#bfa1fa}img{max-width:100%;background:#202a37;border-radius:12px}section{margin:36px 0}</style><a href="../../review.html">Back to combat review</a><h1>Jin Mori illustrated artwork</h1><p>Built-in image generation: 48 registered key poses and a dedicated portrait. Some imported in-betweens share drawings; source timing remains. Original prompts are linked below.</p>'
for n in ('portrait','movement','combat','specials'):
    design+=f'<section><h2>{n.title()}</h2><p><a href="{n}.prompt.txt">Exact generation prompt</a></p><img src="{n}.png" alt="Jin Mori {n} artwork"></section>'
(art/'design-review.html').write_text(design+'</html>',encoding='utf-8')
(S/'proportion-audit.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Jin Mori proportions</title><style>body{background:#101722;color:white;font:17px system-ui;padding:25px}a{color:#bfa1fa}img{max-width:100%;background:#202a37}</style><a href="review.html">Back to combat review</a><h1>Jin Mori proportions</h1><p>Body drawings retain their aspect ratio. Base and King story rows use separate neutral references; planted awakening drawings register crown and soles to a shared height. AIR body scale is uniformly 0.125 with 192x144 local coordinates to match roster height. Attack origins use registered body anchors.</p>'+''.join(f'<h2>{n.title()}</h2><img src="art/illustrated-v1/{n}.png" alt="{n} atlas">' for n in ('movement','combat','specials'))+'</html>',encoding='utf-8')
provenance=dict(tool='built-in image_gen.imagegen',assets={n:dict(file=n+'.png',prompt=n+'.prompt.txt',sha256=hashlib.sha256((art/(n+'.png')).read_bytes()).hexdigest()) for n in ('portrait','movement','combat','specials')})
(art/'provenance.json').write_text(json.dumps(provenance,indent=2))
v2=S/'art/combat-v2'
design2='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jin Mori combat v2 artwork</title><style>body{margin:30px auto;max-width:1100px;padding:20px;background:#101722;color:#edf1f5;font:17px/1.6 system-ui}a{color:#bfa1fa}img{max-width:100%;background:#202a37;border-radius:12px}section{margin:36px 0}</style><a href="../../review.html">Back to combat review</a><h1>Entrance, Monkey King and staff choreography</h1><p>48 additional body drawings and 16 localized effect tiles, created with built-in image generation. The compiler uses the original circlet staff-ready drawing for story cell 11 because the generated cell retained goggles. Exact source drawings and prompts remain preserved.</p>'
for n in ('story','monkey-movement','monkey-combat','effects'):
    correction=f' · <a href="{n}-correction.prompt.txt">Correction prompt</a>' if n in ('story','effects') else ''
    design2+=f'<section><h2>{n.title()}</h2><p><a href="{n}.prompt.txt">Generation prompt</a>{correction}</p><img src="{n}.png" alt="{n} drawings"></section>'
(v2/'design-review.html').write_text(design2+'</html>',encoding='utf-8')
v3=S/'art/awakening-v3'
(v3/'design-review.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Jin Mori awakening</title><style>body{margin:30px auto;max-width:1200px;padding:20px;background:#101722;color:#edf1f5;font:17px/1.6 system-ui}a{color:#bfa1fa}img{max-width:100%;background:#202a37}</style><a href="../../review.html">Back to combat review</a><h1>Awakening transition</h1><p>Eight consecutive drawings show the goggles changing to a circlet, red wraps appearing and the tiger pelt forming. The 92-tick sequence plays forward and backward. Each planted drawing is registered to the same 424px crown-to-sole height as both idle forms. Base and King story rows now have separate neutral size references.</p><p><a href="transition.prompt.txt">Exact built-in image generation prompt</a></p><img src="transition.png" alt="Eight stages from Jin Mori to Monkey King"></html>',encoding='utf-8')
p=S/'proportion-audit.html';old=p.read_text(encoding='utf-8');p.write_text(old.replace('</html>',''.join(f'<h2>Monkey King {n}</h2><img src="art/combat-v2/monkey-{n}.png" alt="Monkey King {n}">' for n in ('movement','combat'))+'</html>'),encoding='utf-8')
p=S/'proportion-audit.html';p.write_text(p.read_text(encoding='utf-8').replace('</html>','<h2>Awakening scale correction</h2><img src="art/awakening-v3/scale-comparison.png" alt="Base idle, King idle and King story neutral share a common height"><p>Both idle forms and all eight planted transition drawings use the same 424px body height. King story poses use their own neutral reference to prevent the smaller story drawings from shrinking the form.</p><p><a href="art/awakening-v3/design-review.html">Transition artwork and exact prompt</a></p><img src="art/awakening-v3/transition.png" alt="Eight transformation stages"></html>'),encoding='utf-8')
write_review('jin-mori',data=data)
# Make the new review reachable from the user's open Vikir page.
v=S.parent/'vikir/review.html';page=v.read_text(encoding='utf-8')
if '../jin-mori/review.html' not in page:
    page=page.replace('</nav>','<a href="../jin-mori/review.html">Jin Mori</a></nav>',1)
    v.write_text(page,encoding='utf-8')
print('MORI_PACKAGE',len(cases),'clips')
