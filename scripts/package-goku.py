"""Package only captures validated against the currently installed Goku build."""
from goku_model import *
import json,hashlib,html
from PIL import Image
build=json.loads((S/'build-report.json').read_text())
reports=[]
for file in ['gameplay-validation.json','contact-validation.json','basics-validation.json','skills-validation.json','power-validation.json','intro-validation.json']:
 report=json.loads((S/file).read_text());assert report['status']=='Complete' and report['failed']==0,file
 assert all(c.get('passed') for c in report['checks']),file
 assert report['runtime_sha256']==build['runtime_sha256'],file
 reports.append(report)
for name,digest in build['runtime_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
groups={n:[] for n in ['Intro','Charge up','Basics','Skills','Supers','Ultimates','Forms']};clips={};ticks={};frames=[];clip_categories={}
for report in reports:
 cases=report.get('cases') or json.loads((S/'replays'/report['capture_directory']/'cases.json').read_text())
 cases=[case for batch in cases for case in (batch.get('value',[batch]) if isinstance(batch,dict) else batch)]
 categories={c['name']:c['category'] for c in cases}
 retained=set()
 for name,category in categories.items():
  clip_frames=[f for f in report.get('frames',[]) if f['case_name']==name and f['case_tick']>=20]
  if category in ('Intro','Basics','Charge up','Forms'):
   active=[f for f in clip_frames if f['animation']==960100] if category=='Intro' else [f for f in clip_frames if f['state'] not in (0,11)]
   if active:
    tail=next((f for f in clip_frames if f['case_tick']>active[-1]['case_tick']),None)
    selected=active+([tail] if tail else [])
   else:selected=clip_frames
  else:selected=clip_frames
  retained.update(id(f) for f in selected)
 for frame in report.get('frames',[]):
  name=frame['case_name'];category=categories[name]
  if category not in groups or id(frame) not in retained:continue
  clip_name=name
  if name in clip_categories and clip_categories[name]!=category:clip_name=name+' ('+category.rstrip('s').lower()+')'
  capture_directory=frame.get('capture_directory',report['capture_directory'])
  path=S/'replays'/capture_directory/frame['file'];assert path.is_file(),path
  with Image.open(path) as im:im.verify()
  if clip_name not in clips:groups[category].append(clip_name);clips[clip_name]=[];ticks[clip_name]=[];clip_categories[clip_name]=category
  clips[clip_name].append(path.relative_to(S).as_posix());ticks[clip_name].append(frame['case_tick']);frames.append(dict(frame,capture_directory=capture_directory))
assert all(groups.values()),{k:len(v) for k,v in groups.items()}
assert {f['animation_element'] for f in frames if f['animation']==960100}==set(range(1,17))
runtime=dict(status='Complete',passed=sum(r['passed'] for r in reports),failed=0,checks=[c for r in reports for c in r['checks']],frames=frames,runtime_sha256=build['runtime_sha256'])
(S/'runtime-validation.json').write_text(json.dumps(runtime,indent=2))
esc=html.escape
style='body{max-width:1120px;margin:32px auto;padding:0 22px;background:#10141c;color:#edf0f5;font:16px/1.6 system-ui}a{color:#ffb76b}h1,h2{line-height:1.2}section{margin:36px 0}img{max-width:100%;background:#202633;border-radius:8px}button,select{padding:9px;background:#252d3b;color:white;border:1px solid #596476;font:inherit;border-radius:5px}button[aria-pressed=true]{background:#703c18}#categories{display:flex;gap:8px;flex-wrap:wrap}#screen{width:100%}.forms{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px}.forms img{height:230px;width:100%;object-fit:contain}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:9px;border-bottom:1px solid #394252}.pass{color:#a0dfa9}.scroll{overflow:auto}'
head=lambda title:f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{style}</style><body>'
page=head('Goku — illustrated combat review')+'<a href="../luffy/review.html">Luffy review</a><h1>Son Goku</h1><p>Goku DBS V3.5 imported with its original move logic and voices, rebuilt in our painted, inked roster style. Eleven playable forms: base, Kaioken, Super Saiyan 1–3, God, Blue, Blue Kaioken, Blue Kaioken x10, Ultra Instinct Omen and Mastered Ultra Instinct. This DBS release does not contain GT Super Saiyan 4.</p>'
page+=f'<p class="pass">{runtime["passed"]} engine checks passed; 0 failed.</p><p><a href="README.md">Controls and source credits</a> · <a href="runtime-validation.json">Engine validation</a> · <a href="build-report.json">Build report</a> · <a href="art/illustrated-v1/design-review.html">Artwork and exact prompts</a></p>'
page+='<section><h2>Portrait and shot alignment</h2><p>Portraits fit inside the HUD frame. Beams start at the releasing palms; ki blasts keep their launch direction, and impact flashes follow the beam line.</p><p><a href="art/presentation-v3/portrait.png">Portrait</a> ? <a href="art/presentation-v3/portrait.prompt.txt">Portrait prompt</a> ? <a href="art/presentation-v3/provenance.json">Provenance</a> ? <a href="shot-registration.json">Hand registration</a> ? <a href="alignment-validation.json">Trajectory checks</a></p></section>'
page+='<section><h2>Combat review</h2><p>Starts in base form. His animated intro waves hello, scratches the back of his head, stretches, and settles into his guard. Browse the charge-up, ground and air basics, skills, supers, ultimates and transformations below.</p><nav id="categories" aria-label="Move categories"></nav><p><label>Category <select id="category"></select></label> <label>Move <select id="clip"></select></label></p><button id="play">Play samples</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button><p id="counter"></p><img id="screen" alt="Goku illustrated combat captured in the game engine"></section>'
player=(R/'scripts/templates/ichigo-review-player.js').read_text(encoding='utf-8').replace('ICHIGO_REVIEW','GOKU_REVIEW').replace('Math.max(60,','Math.max(16,')
page+='<script>window.GOKU_REVIEW='+json.dumps(dict(clips=clips,ticks=ticks,groups=groups)).replace('</','<\\/')+';'+player+'</script>'
page+='<section><h2>Controls</h2><p>Arrows move; hold back to guard. Z / X / C use light, medium and ki attacks on the ground or in the air. Repeat the normal buttons on contact for the imported combo chains. W cycles forms; down + W returns to base. Hold Enter to charge ki.</p><p>A = skill 1; back + A = skill 2; forward + A = skill 3; down + A = skill 4; down-forward + A = skill 6; Q = skill 7. S uses Kamehameha on the ground or in the air. D uses the form’s ultimate; down + D uses the second super where available. In Blue Kaioken, back + Q accesses Meteor Rush God Kamehameha, while forward + A enters Blue Kaioken x10.</p><p>Base Spirit Bomb: hold D with a full meter to gather energy for about ten seconds, then press D again to release the completed bomb. The entry gate costs 500, and gathering continuously drains ki. Arrow directions are relative to facing; form availability and meter costs appear below.</p></section>'
page+='<section><h2>Illustrated forms</h2><div class="forms">'
for f in FORMS:page+=f'<article><h3>{esc(f["name"])}</h3><img src="art/illustrated-v1/poses/{BANKS[f["bank"]]}-0.png" alt="{esc(f["name"])}"><p>{"Kaioken uses its native red aura over this outfit." if f["flags"][1] else ""}</p></article>'
page+='</div></section><section><h2>Imported move routes</h2><div class="scroll"><table><tr><th>Form</th><th>Move</th><th>Shortcut</th><th>Category</th><th>Meter</th><th>Position</th></tr>'
shortcuts={'x':'A','/$B,x':'Back + A','/$F,x':'Forward + A','/$D,x':'Down + A','y':'S','/$D,/$F,x':'Down-forward + A','d':'Q','z':'D','/$D,z':'Down + D','/$B,d':'Back + Q'}
for r in routes():page+=f'<tr><td>{esc(FORMS[r["form"]]["name"])}</td><td>{esc(r["name"])}</td><td>{shortcuts[r["input"]]}</td><td>{r["category"]}</td><td>{r["cost"]}</td><td>{"Air" if r["air"] else "Ground"}</td></tr>'
page+='</table></div></section></body></html>';(S/'review.html').write_text(page,encoding='utf-8')
art=S/'art/illustrated-v1';design=head('Goku — illustrated assets')+'<a href="../../review.html">Combat review</a><h1>Goku illustrated assets</h1><p>128 combat key poses across eight appearance banks, sixteen signature-technique drawings, sixteen greeting frames, and sixteen energy-effect motifs. Spirit Bomb, Solar Flare, Instant Transmission and Dragon Fist use dedicated technique poses. Kaioken variants share their base or Blue outfit with red energy. Native AIR frame timing is preserved; beam and projectile collision paths follow the registered artwork; these drawings are key-pose adaptations, rather than individual redraws of every imported frame.</p><p><a href="provenance.json">Built-in image generation provenance</a></p>'
design+='<h2>Animated base-form intro</h2><div style="height:330px;display:flex;align-items:end;justify-content:center"><img id="actor" src="poses/intro-0.png" style="max-height:320px;background:transparent" alt="Goku greeting animation"></div><button id="pause">Pause animation</button><script>let f=0,playing=true;const actor=document.getElementById("actor");setInterval(()=>{if(playing){f=(f+1)%16;actor.src=`poses/intro-${f}.png`}},167);document.getElementById("pause").onclick=()=>{playing=!playing;document.getElementById("pause").textContent=playing?"Pause animation":"Play animation"};</script>'
for slug in BANKS+['techniques','intro-v2','effects']:design+=f'<section><h2>{esc(slug)}</h2><a href="{slug}.prompt.txt">Exact prompt</a><img loading="lazy" src="{slug}.png" alt="{esc(slug)} illustrated sprite atlas"></section>'
design+='<section><h2>Energy animation revision</h2><p>Each appearance bank has sixteen dedicated charge, two-hand beam release, recoil, recovery and one-hand ki-shot drawings. The energy sheets add sixteen beam frames and sixteen projectile, charge-orb and impact frames. Charging holds at the cupped hands, and beam recoil plays while its helper remains active.</p><a href="../energy-v2/provenance.json">Energy artwork provenance</a></section>'
energy_assets=json.loads((S/'art/energy-v2/provenance.json').read_text())['assets']
for slug in ['body-'+b for b in BANKS]+['beam','ki-impact']:
 asset=energy_assets[slug];design+=f'<section><h2>{esc(slug)}</h2><a href="../energy-v2/{asset["prompt"]}">Exact prompt</a><img loading="lazy" src="../energy-v2/{asset["file"]}" alt="{esc(slug)} animation atlas"></section>'
(art/'design-review.html').write_text(design+'</body></html>',encoding='utf-8')
print('GOKU_PACKAGED',runtime['passed'],'checks;',len(clips),'clips;',len(frames),'captures;', {k:len(v) for k,v in groups.items()})
