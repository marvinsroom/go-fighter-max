"""Publish the illustrated GT fighter review using current native evidence."""
from gt_goku_model import *
import json,hashlib,html,shutil
from PIL import Image

build=json.loads((S/'build-report.json').read_text())
reports=[json.loads((S/name).read_text(encoding='utf-8')) for name in ['gameplay-validation.json','basics-validation.json','skills-validation.json','power-validation.json','intro-validation.json']]
for report in reports:
 assert report['status']=='Complete' and report['failed']==0
 assert all(c['passed'] for c in report['checks'])
 assert report['runtime_sha256']==build['runtime_sha256']
 # Lua 5.1 treats JSON-style Unicode escapes as literal uXXXX. Canonicalize
 # legacy capture labels; timings, state results and image files are unchanged.
 def canonical(name):
  # Older Windows fixtures wrote the Portuguese source label as ANSI. Go's
  # JSON encoder retained the successful test but replaced its invalid byte.
  return re.sub(r'u(00[0-9a-fA-F]{2})',lambda m:chr(int(m[1],16)),name).replace('punho do drag\ufffdo','punho do dragão')
 for check in report['checks']:check['name']=canonical(check['name'])
 for frame in report.get('frames',[]):frame['case_name']=canonical(frame['case_name'])
for name,digest in build['runtime_sha256'].items():
 with (O/name).open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==digest,name

groups={key:[] for key in ['Intro','Charge up','Basics','Skills','Supers','Ultimates','Forms']}
clips={};ticks={};frames=[]
def display_name(name):
 return name.replace('Super Saiyan 2 / Super Kamehameha SS1','Super Saiyan 2 / Super Kamehameha SS2').replace('punho do dragão','Dragon Fist').replace('Metteor impact','Meteor Impact')
for report in reports:
 cases=report.get('cases') or json.loads((S/'replays'/report['capture_directory']/'cases.json').read_text())
 cases=[case for batch in cases for case in (batch.get('value',[batch]) if isinstance(batch,dict) else batch)]
 categories={c['name']:c['category'] for c in cases}
 for frame in report.get('frames',[]):
  category=categories[frame['case_name']]
  if category not in groups or frame['case_tick']<20:continue
  if category=='Intro' and frame['animation']!=960100:continue
  name=display_name(frame['case_name']);directory=frame.get('capture_directory',report['capture_directory'])
  path=S/'replays'/directory/frame['file'];assert path.is_file(),path
  with Image.open(path) as im:im.verify()
  if name not in clips:groups[category].append(name);clips[name]=[];ticks[name]=[]
  clips[name].append(path.relative_to(S).as_posix());ticks[name].append(frame['case_tick']);frames.append(dict(frame,capture_directory=directory))
assert all(groups.values()),groups
runtime=dict(status='Complete',passed=sum(r['passed'] for r in reports),failed=0,checks=[c for r in reports for c in r['checks']],frames=frames,runtime_sha256=build['runtime_sha256'])
(S/'runtime-validation.json').write_text(json.dumps(runtime,indent=2))

art=S/'art/illustrated-v1';assets={}
for key in BANKS+['intro','effects']:
 path=art/(key+'.png')
 assets[key]=dict(file=path.name,prompt=key+'.prompt.txt',sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 if key=='effects':assets[key]['reused_from']='goku/art/illustrated-v1/effects.png'
(art/'provenance.json').write_text(json.dumps(dict(tool='built-in imagegen',api_fallback_used=False,assets=assets),indent=2))
esc=html.escape
style='body{max-width:1120px;margin:32px auto;padding:0 22px;background:#10141c;color:#edf0f5;font:16px/1.6 system-ui}a{color:#ffb76b}button,select{padding:9px;background:#252d3b;color:white;border:1px solid #596476;font:inherit;border-radius:5px}button[aria-pressed=true]{background:#703c18}#categories{display:flex;gap:8px;flex-wrap:wrap}img{max-width:100%;background:#202633;border-radius:8px}#screen{width:100%}.forms{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}.forms img{height:240px;width:100%;object-fit:contain}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:9px;border-bottom:1px solid #394252}.scroll{overflow:auto}section{margin:32px 0}'
head=lambda title:f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{style}</style><body>'
page=head('GT Goku — illustrated combat review')+'<a href="../goku/review.html">Goku DBS review</a><h1>GT Goku</h1><p>Kid Goku grows into Super Saiyan 4. Five source forms, 37 imported move routes and voices, rebuilt with our painted, inked roster artwork. Brown tails on the child forms; red tail on adult SS4.</p>'
page+=f'<p>{runtime["passed"]} engine checks passed; 0 failed. Illustrated key poses retain the imported animation timing; beam collision paths follow the artwork.</p><p><a href="README.md">Controls and source credits</a> · <a href="runtime-validation.json">Native validation</a> · <a href="art/illustrated-v1/design-review.html">Artwork and exact prompts</a></p>'
page+='<section><h2>Portrait and shot alignment</h2><p>Portraits fit inside the HUD frame. Beams start at the releasing palms; ki blasts keep their launch direction, and impact flashes follow the beam line.</p><p><a href="art/presentation-v3/portrait.png">Portrait</a> ? <a href="art/presentation-v3/portrait.prompt.txt">Portrait prompt</a> ? <a href="art/presentation-v3/provenance.json">Provenance</a> ? <a href="shot-registration.json">Hand registration</a> ? <a href="alignment-validation.json">Trajectory checks</a></p></section>'
page+='<section><h2>Combat review</h2><nav id="categories" aria-label="Move categories"></nav><p><label>Category <select id="category"></select></label> <label>Move <select id="clip"></select></label></p><button id="play">Play samples</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button><p id="counter"></p><img id="screen" alt="GT Goku combat captured in the game engine"></section>'
player=(R/'scripts/templates/ichigo-review-player.js').read_text(encoding='utf-8').replace('ICHIGO_REVIEW','GT_GOKU_REVIEW').replace('Math.max(60,','Math.max(16,')
page+='<script>window.GT_GOKU_REVIEW='+json.dumps(dict(clips=clips,ticks=ticks,groups=groups)).replace('</','<\\/')+';'+player+'</script>'
page+='<section><h2>Controls</h2><p>Arrows move; hold back to guard. Z / X / C attack on ground or in air. Repeat Z or X on contact to chain the native combos. W cycles base → SS1 → SS2 → SS3 → SS4; down + W returns to base. Hold Enter to charge ki.</p><p>A = Ki Liberation; back + A = secondary skill; forward + A = rush skill; down + A = Instant Transmission; down-forward + A = energy blast. S = Kamehameha. D = ultimate. SS4: down + Q = Full Power.</p><p>Base D uses Super Kamehameha at ordinary health. When both fighters have half health or less, it uses Super Cho Genkidama. SS1 uses Instant Kamehameha, SS2 Super Kamehameha, SS3 Dragon Fist, and SS4 Ryu Ken.</p></section><section><h2>Forms</h2><div class="forms">'
for f in FORMS:page+=f'<article><h3>{esc(f["name"])}</h3><img src="art/illustrated-v1/poses/{BANKS[f["bank"]]}-0.png" alt="{esc(f["name"])}"></article>'
page+='</div></section><section><h2>Move routes</h2><div class="scroll"><table><tr><th>Form</th><th>Move</th><th>Category</th><th>Meter</th></tr>'
for route in routes():
 name=display_name(FORMS[route['form']]['name']+' / '+route['name']).split(' / ',1)[1]
 page+=f'<tr><td>{esc(FORMS[route["form"]]["name"])}</td><td>{esc(name)}</td><td>{route["category"]}</td><td>{route["cost"]}</td></tr>'
page+='</table></div></section></body></html>'
if not (S/'art-review.html').exists():shutil.copy2(S/'review.html',S/'art-review.html')
(S/'review.html').write_text(page,encoding='utf-8')
design=head('GT Goku — artwork')+'<a href="../../review.html">Combat review</a><h1>GT Goku illustrated artwork</h1><p>80 combat key poses, 16 greeting frames and shared illustrated effects. Source voices, state logic and frame timings remain imported; beam and projectile collision paths follow the artwork. Artwork was generated with the built-in image tool.</p><a href="provenance.json">Provenance</a>'
for key in assets:design+=f'<section><h2>{esc(key)}</h2><a href="{key}.prompt.txt">Exact prompt</a><img src="{key}.png" alt="{esc(key)} sprite atlas"></section>'
(art/'design-review.html').write_text(design+'</body></html>',encoding='utf-8')
print('GT_GOKU_PACKAGED',runtime['passed'],'checks;',len(clips),'clips;',len(frames),'captures')
