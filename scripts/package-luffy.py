"""Publish only passing illustrated Luffy captures tied to the installed build."""
from pathlib import Path
import json,hashlib,html,re
from PIL import Image
from luffy_model import FORMS,routes
from luffy_funny_intro import DURATIONS

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/luffy';O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/luffy'
build=json.loads((S/'build-report.json').read_text());assert build['art']=='illustrated'
files=['gameplay-validation.json','basics-validation.json','skills-validation.json','power-validation.json','intro-validation.json']
reports=[json.loads((S/f).read_text()) for f in files]
for report in reports:
 assert report['status']=='Complete' and report['failed']==0
 assert report['passed']==len(report['checks']) and all(c['passed'] for c in report['checks'])
 assert report['runtime_sha256']==build['runtime_sha256']
for name,digest in build['runtime_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
frames=[dict(f,capture_directory=r['capture_directory']) for r in reports for f in r.get('frames',[])]
runtime=dict(status='Complete',passed=sum(r['passed'] for r in reports),failed=0,checks=[c for r in reports for c in r['checks']],frames=frames,runtime_sha256=build['runtime_sha256'],suites=[dict(file=f,passed=r['passed']) for f,r in zip(files,reports)])
categories={};clips={};ticks={}
for report in reports:
 cases=json.loads((S/'replays'/report['capture_directory']/'cases.json').read_text());categories.update({c['name']:c['category'] for c in cases})
for frame in frames:
 name=frame['case_name'];path=S/'replays'/frame['capture_directory']/frame['file'];assert path.is_file(),path
 with Image.open(path) as im:im.verify()
 # Keep reset-fixture screenshots in the evidence report, while playback
 # starts with the requested move instead of a preceding gallery pose.
 if categories[name]!='Intro' and frame['case_tick']<20:continue
 clips.setdefault(name,[]).append(path.relative_to(S).as_posix());ticks.setdefault(name,[]).append(frame['case_tick'])
groups={name:[] for name in ('Intro','Charge up','Basics','Skills','Supers','Ultimates','Forms')}
for name in clips:groups[categories[name]].append(name)
assert {g:len(v) for g,v in groups.items()}==dict(Intro=1,**{'Charge up':5},Basics=30,Skills=36,Supers=5,Ultimates=5,Forms=6)
intro=[f for f in frames if f['animation']==60100 and f['case_name'].startswith('Intro - ')]
assert {f['animation_element'] for f in intro}==set(range(1,17))
escape=html.escape;art=S/'art/illustrated-v1'
style='body{max-width:1120px;margin:32px auto;padding:0 22px;background:#10141c;color:#edf0f5;font:16px/1.6 system-ui}a{color:#ffbb77}h1,h2{line-height:1.2}section{margin:36px 0}img{max-width:100%;background:#202633;border-radius:8px}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:10px;border-bottom:1px solid #394252}.forms{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px}.forms img{width:100%;height:280px;object-fit:contain}.pass{color:#9fdbab}button,select{padding:9px;background:#252d3b;color:white;border:1px solid #596476;font:inherit;border-radius:5px}button[aria-pressed="true"]{background:#6a3d20;border-color:#ffbb77}#categories{display:flex;flex-wrap:wrap;gap:8px}#screen{width:100%}.scroll{overflow:auto}'
head=lambda title:f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{style}</style><body>'
design=head('Luffy illustrated artwork')+'<a href="../../review.html">Engine review</a><h1>Luffy illustrated artwork</h1><p>96 combat drawings across five playable forms and the temporary Tankman finisher, sixteen intro drawings and sixteen combat-effect motifs. Generated with built-in imagegen. <a href="provenance.json">Provenance</a>.</p>'
design+='<h2>Funny meat intro — base Luffy</h2><div style="height:390px;display:flex;align-items:end;justify-content:center;background:#202633"><img id="actor" src="poses/intro-0.png" style="height:auto;max-height:350px;background:transparent" alt="Luffy taking a huge bite, puffing his cheeks and grinning into a ready stance"></div><p><button id="pause">Pause animation</button> <a href="../funny-intro-v2/intro.prompt.txt">Exact intro prompt</a> · <a href="../funny-intro-v2/provenance.json">Intro provenance</a></p>'
design+='<script>const duration='+json.dumps(DURATIONS)+';let frame=0,timer,playing=true;function next(){timer=setTimeout(()=>{frame=(frame+1)%16;document.getElementById("actor").src=`poses/intro-${frame}.png`;next()},duration[frame]*1000/60+(frame===15?650:0))}document.getElementById("pause").onclick=()=>{playing=!playing;document.getElementById("pause").textContent=playing?"Pause animation":"Play animation";if(playing)next();else clearTimeout(timer)};next();</script>'
for slug,label in [(f['slug'],f['name']) for f in FORMS]+[('tankman','Tankman finisher'),('../funny-intro-v2/intro','Funny meat intro'),('effects','Haki, giant fists, Red Hawk, steam and impacts'),('portrait','Character portrait')]:design+=f'<section><h2>{escape(label)}</h2><p><a href="{slug}.prompt.txt">Exact generation prompt</a></p><img loading="lazy" src="{slug}.png" alt="{escape(label)} illustrated artwork"></section>'
(art/'design-review.html').write_text(design+'</body></html>',encoding='utf-8')
page=head('Monkey D. Luffy — combat review')+'<a href="../ichigo/review.html">Ichigo review</a><h1>Monkey D. Luffy</h1><p>Luffy in the illustrated roster style: base, Gear 4 Boundman, Gear 4 Snakeman, Nightmare and Gear 5 Nika, plus Tankman during his finisher. Imported move logic and voices adapted from TheCube’s all-forms release.</p>'
page+=f'<p class="pass">{runtime["passed"]} runtime checks passed; 0 failed.</p><p><a href="README.md">Controls and build notes</a> · <a href="runtime-validation.json">Runtime validation</a> · <a href="build-report.json">Build and source credits</a> · <a href="art/illustrated-v1/design-review.html">Animated intro, artwork and exact prompts</a></p>'
page+='<section><h2>Illustrated combat in the engine</h2><p><strong>Starts in base Luffy.</strong> His funny intro has him take a huge bite of meat, try to act tough with his cheeks stuffed, gulp it down, then scratch his head, grin and get ready to fight. He stays in his regular pirate clothes throughout. Select a category to inspect his charge-up, ground and air basics, skills, supers, ultimates and form changes.</p><nav id="categories" aria-label="Move categories"></nav><p><label>Category <select id="category"></select></label> <label>Move <select id="clip"></select></label></p><button id="play">Play samples</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button><p id="counter"></p><img id="screen" alt="Luffy illustrated engine combat capture"></section>'
player=(R/'scripts/templates/ichigo-review-player.js').read_text(encoding='utf-8').replace('ICHIGO_REVIEW','LUFFY_REVIEW')
page+='<script>window.LUFFY_REVIEW='+json.dumps(dict(clips=clips,ticks=ticks,groups=groups)).replace('</','<\\/')+';'+player+'</script>'
page+='<section><h2>Controls</h2><p>Arrow keys move; hold back to guard. Z / X / C are the three normal attack buttons. W cycles forms; down + W returns to base Luffy. Hold Enter to charge. S uses the super; D uses the ultimate.</p><p>A uses skill 1; back + A skill 2; forward + A skill 3; down + A skill 4; down-forward + A skill 5; down-back + A skill 6. Where available, Q uses skill 7, back + Q skill 8, forward + Q skill 9. Directions are relative to facing. Availability and meter cost depend on the form; see the route table below.</p></section><section><h2>Forms</h2><div class="forms">'
for form in FORMS:page+=f'<article><h3>{escape(form["name"])}</h3><img src="art/illustrated-v1/poses/{form["slug"]}-0.png" alt="{escape(form["name"])} illustrated fighter"></article>'
page+='</div></section><section><h2>Mapped moves</h2><div class="scroll"><table><tr><th>Form</th><th>Move</th><th>Shortcut</th><th>Meter</th></tr>'
for route in routes():page+=f'<tr><td>{escape(FORMS[route["form"]]["name"])}</td><td>{escape(route["name"])}</td><td>{escape(route["command"].replace("luffy_",""))}</td><td>{route["cost"]}</td></tr>'
page+='</table></div></section><section><details><summary>All runtime checks</summary><ul>'
for check in runtime['checks']:page+=f'<li class="pass">{escape(check["name"])} — passed</li>'
page+='</ul></details></section></body></html>'
(S/'review.html').write_text(page,encoding='utf-8');(S/'runtime-validation.json').write_text(json.dumps(runtime,indent=2))
print('LUFFY_PACKAGED',runtime['passed'],'checks;',len(clips),'clips;',len(frames),'engine captures')
