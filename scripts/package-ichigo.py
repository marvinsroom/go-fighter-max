"""Package Ichigo's completed checks and native engine captures for local review."""
from pathlib import Path
import hashlib, html, json,os
from PIL import Image

R=Path(__file__).resolve().parents[1]
S=R/'sprite-fighter/characters/ichigo'
O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/ichigo'
build=json.loads((S/'build-report.json').read_text())
assert build['art']=='illustrated', 'Package the illustrated roster build, not the source-sprite comparison'
art_audit=json.loads((S/'illustrated-build.json').read_text())
assert art_audit['referenced_original_sprites']==0 and art_audit['drawings']==192
suite_files=('gameplay-validation.json','basics-validation.json','skills-validation.json','power-validation.json')
reports=[json.loads((S/name).read_text()) for name in suite_files]
for result in reports:
    assert result['status']=='Complete' and result['failed']==0, 'Runtime checks must pass before packaging'
    assert result['runtime_sha256']==build['runtime_sha256'], 'Validation does not match the build'
    assert result['passed']==len(result['checks']) and all(c['passed'] for c in result['checks'])
report=dict(status='Complete',passed=sum(r['passed'] for r in reports),failed=0,
            checks=[c for r in reports for c in r['checks']],
            frames=[dict(f,capture_directory=r['capture_directory']) for r in reports for f in r.get('frames',[])],
            capture_directory=reports[-1]['capture_directory'],runtime_sha256=build['runtime_sha256'],
            suites=[dict(file=name,passed=r['passed']) for name,r in zip(suite_files,reports)])
for name,digest in build['runtime_sha256'].items():
    assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest, name
escape=html.escape
art=S/'art/illustrated-v2'
design='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ichigo — illustrated artwork</title><style>body{max-width:1100px;margin:30px auto;padding:20px;background:#10141c;color:#edf0f5;font:16px/1.6 system-ui}a{color:#ffbb77}img{max-width:100%;background:#202633;border-radius:10px}section{margin:40px 0}</style><a href="../../review.html">Combat review</a><h1>Ichigo — illustrated roster artwork</h1><p>192 drawings across 11 selectable forms and the Mugetsu finisher bank. Sixteen painted effects replace the source slashes, Getsuga projectiles, Cero beams, impacts and spiritual pressure. Animation retains the imported combat timing and hit boxes, with action-specific wind-up, release, follow-through and recovery poses.</p>'
for form in build['forms']+[dict(slug='mugetsu',name='Mugetsu')]:
    source=art/(form['slug']+'.png')
    if not source.exists():source=S/'art/illustrated-v1'/(form['slug']+'.png')
    relative=os.path.relpath(source,art).replace('\\','/')
    design+=f'<section><h2>{escape(form["name"])}</h2><p><a href="{relative.replace(".png",".prompt.txt")}">Generation prompt</a></p><img loading="lazy" src="{relative}" alt="{escape(form["name"])} illustrated animation drawings"></section>'
design+='<section><h2>Getsuga, Cero and combat effects</h2><p><a href="effects.prompt.txt">Generation prompt</a> · <a href="gutters.prompt.txt">Atlas spacing correction prompt</a> · <a href="provenance.json">Provenance</a></p><img loading="lazy" src="effects.png" alt="Illustrated sword, Getsuga and Cero effects"></section></html>'
(art/'design-review.html').write_text(design,encoding='utf-8')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ichigo Kurosaki — combat review</title><style>
body{max-width:1120px;margin:32px auto;padding:0 22px;background:#10141c;color:#edf0f5;font:16px/1.6 system-ui}a{color:#ffbb77}h1,h2{line-height:1.2}section{margin:36px 0}img{max-width:100%;background:#202633;border-radius:8px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:10px;border-bottom:1px solid #394252}.scroll{overflow:auto}.forms{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}.forms img{width:100%;height:280px;object-fit:contain}.pass{color:#9fdbab}button,select{padding:9px;background:#252d3b;color:white;border:1px solid #596476;font:inherit;border-radius:5px}#screen{width:100%}summary{cursor:pointer}small{color:#aeb9ca}</style><body>
<a href="../pyowol/review.html">Pyo Wol review</a><h1>Ichigo Kurosaki</h1>
<p>Ichigo in the illustrated roster style: 11 selectable forms, Mugetsu's finisher form, hand-drawn combat poses, and new Getsuga, Cero, slash and impact effects. Combat logic and voices adapted from Chickennuggetprime's all-forms edit.</p>
'''
page=page.replace('</style>','button[aria-pressed="true"]{background:#6a3d20;border-color:#ffbb77} #categories{display:flex;flex-wrap:wrap;gap:8px}</style>')
page+=f'<p class="pass">{report["passed"]} runtime checks passed; {report["failed"]} failed.</p>'
page+='<p><a href="README.md">Build notes and launch instructions</a> · <a href="runtime-validation.json">Validation report</a> · <a href="build-report.json">Build and source credits</a> · <a href="art/illustrated-v2/design-review.html">Artwork and exact prompts</a></p>'
captures={}
capture_ticks={}
for frame in report.get('frames',[]):
    p=S/'replays'/frame.get('capture_directory',report['capture_directory'])/frame['file']
    assert p.is_file(),p
    with Image.open(p) as im:im.verify()
    captures.setdefault(frame['case_name'],[]).append(p.relative_to(S).as_posix())
    capture_ticks.setdefault(frame['case_name'],[]).append(frame['case_tick'])
if captures:
    groups={name:[] for name in ('Intro','Charge up','Basics','Skills','Supers','Ultimates','Forms')}
    for name in captures:
        group='Intro' if name.startswith('Intro') else 'Charge up' if 'charge' in name else 'Basics' if name.endswith('slash') else 'Skills' if 'skill' in name else 'Supers' if name.endswith('super') else 'Ultimates' if name.endswith('ultimate') else 'Forms'
        groups[group].append(name)
    assert all(groups.values()), 'Every review category requires captured engine evidence'
    assert len(groups['Basics'])==66 and len(groups['Skills'])==66
    assert len(groups['Charge up'])==len(groups['Supers'])==len(groups['Ultimates'])==11
    page+='<section><h2>Illustrated combat in the engine</h2><p>The intro animates Ichigo stepping forward in his school uniform, gathering spiritual pressure, transforming his clothes into Bankai, then landing and drawing his sword. <a href="art/school-intro-v4/design-review.html">Intro drawings and exact generation prompt</a>. Explore charging, ground and air basics, every mapped skill, supers and ultimates below.</p><nav id="categories" aria-label="Move categories"></nav><p><label>Category <select id="category"></select></label> <label>Move <select id="clip"></select></label></p><button id="play">Play samples</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button><p id="counter"></p><img id="screen" alt="Ichigo illustrated engine combat capture"></section>'
    payload=json.dumps(dict(clips=captures,ticks=capture_ticks,groups=groups)).replace('</','<\\/')
    page+='<script>window.ICHIGO_REVIEW='+payload+';'+(R/'scripts/templates/ichigo-review-player.js').read_text(encoding='utf-8')+'</script>'
page+='''<section><h2>Controls</h2><p>Arrow keys move; hold back to guard. Z / X / C are the source normal attacks. W cycles forms; down + W returns to Shikai. Hold Enter to charge, S uses the super and D uses the ultimate. Q is the source flash step.</p><p>A uses skill 1; back + A skill 2; forward + A skill 3; down + A skill 4; down-forward + A skill 5; down-back + A skill 6. Directions are relative to facing. Skill availability and meter costs vary by form.</p></section><section><h2>Forms</h2><div class="forms">'''
for form in build['forms']:
    page+=f'<article><h3>{escape(form["name"])}</h3><img src="art/illustrated-v2/poses/{form["slug"]}-0.png" alt="{escape(form["name"])} illustrated game drawing"></article>'
page+='</div></section><section><h2>Move routes</h2><div class="scroll"><table><thead><tr><th>Form</th><th>Input</th><th>Meter</th></tr></thead><tbody>'
forms={f['id']:f['name'] for f in build['forms']}
for route in build['shortcut_routes']:
    page+=f'<tr><td>{escape(forms[route["form"]])}</td><td>{escape(route["input"].replace("ichigo_", ""))}</td><td>{route["cost"]}</td></tr>'
page+='</tbody></table></div></section><section><details><summary>All runtime checks</summary><ul>'
for check in report['checks']:
    page+=f'<li class="pass">{escape(check["name"])} — passed</li>'
page+='</ul></details></section></body></html>'
(S/'review.html').write_text(page,encoding='utf-8')
(S/'runtime-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ICHIGO_PACKAGED',report['passed'],'checks;',len(captures),'combat clips')
