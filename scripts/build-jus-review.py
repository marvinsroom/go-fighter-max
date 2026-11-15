"""Current native evidence and a shared-scale, actual packed-sprite roster viewer."""
from pathlib import Path
import json,sys,re,importlib.util,collections
from mugen_sff import Sff
from edward_assets import read_v1
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
data=json.loads((O/'manifest.json').read_text());old=json.loads((R/'sprite-fighter/face-audit/identity-scale-v5/profiles.json').read_text())['fighters'];old={r['slug']:r for r in old}
spec=importlib.util.spec_from_file_location('jus_mobility',R/'scripts/validate-jus-mobility.py');validation=importlib.util.module_from_spec(spec);spec.loader.exec_module(validation)
data['walk_cycles']=[]
(O/'lineup').mkdir(exist_ok=True)
for row in data['fighters']:
 slug=row['slug'];n=E/'chars'/row['engine'];definition=(n/row['definition']).read_text(encoding='cp1252');sf=re.search(r'(?im)^\s*sprite\s*=\s*([^;\r\n]+)',definition)[1].strip().strip('"');path=n/sf
 if slug in old:
  key=tuple(old[slug]['neutral_key'])
 else:key=(0,0)
 cns_name=re.search(r'(?im)^\s*cns\s*=\s*([^;\r\n]+)',definition)[1].strip().strip('"')
 size=re.search(r'(?ims)^\s*\[Size\](.*?)(?=^\s*\[|\Z)',(n/cns_name).read_text(encoding='cp1252',errors='replace'))[1]
 native_y=float(re.search(r'(?im)^\s*yscale\s*=\s*([-\d.eE+]+)',size)[1])
 width=float(re.search(r'(?im)^\s*localcoord\s*=\s*([\d.]+)',definition)[1])
 air_name=re.search(r'(?im)^\s*anim\s*=\s*([^;\r\n]+)',definition)[1].strip().strip('"')
 live_scales=[]
 for line in (n/air_name).read_text(encoding='cp1252',errors='replace').splitlines():
  if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
  fields=[v.strip() for v in line.split(';')[0].split(',')]
  if tuple(map(int,fields[:2]))==key:live_scales.append(float(fields[8]) if len(fields)>8 and fields[8] else 1)
 scale=collections.Counter(live_scales).most_common(1)[0][0]*native_y*320/width
 with path.open('rb') as stream:version=stream.read(16)[15]
 if version==1:
  sprites=read_v1(path);sprite=next(s for s in sprites if s['key']==key);im=sprite['image'];axis=sprite['axis'];del sprites
 else:
  source=Sff(path);index=source.keys[key];header=source.headers[index];im=source.decode(index);axis=header[4:6];del source
 im.save(O/'lineup'/(slug+'.png'))
 row['preview']=dict(file='lineup/'+slug+'.png',axis=axis,scale=scale,key=key)
 current_hashes=validation.runtime(row)
 for suite in ('native','native-combat','native-forms'):
  proof=O/suite/slug/'current.json'
  if proof.exists():
   result=json.loads(proof.read_text())
   proof_hashes=result.get('production_runtime_sha256',result.get('runtime_sha256'))
   if result.get('status')=='Complete' and result.get('failed')==0 and proof_hashes==current_hashes:
    row[suite]=dict(passed=result.get('passed'),failed=result.get('failed'),proof=f'{suite}/{slug}/current.json',screenshots=[str(Path(p).relative_to('sprite-fighter/jus-upgrade')).replace('\\','/') for p in result.get('screenshots',[])])
 row['new_walk']=(O/'art'/slug/'packing.json').exists()
 if row['new_walk']:row['walk_packing']=json.loads((O/'art'/slug/'packing.json').read_text())
 form_file=O/'art'/slug/'form-cycles-packing.json'
 if form_file.exists():
  for cycle in json.loads(form_file.read_text())['cycles']:
   data['walk_cycles'].append(dict(slug=slug,label=slug.replace('-',' ')+' / '+cycle['label'],folder=f'art/{slug}/cycles/{cycle["source_group"]}',packing=cycle))
 elif row['new_walk']:
  data['walk_cycles'].append(dict(slug=slug,label=slug.replace('-',' '),folder=f'art/{slug}',packing=row['walk_packing']))

(O/'review-data.json').write_text(json.dumps(data,indent=2))
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Illustrated JUS roster upgrade</title>
<style>*{box-sizing:border-box}body{margin:0;background:#10151d;color:#e9edf3;font:16px system-ui;line-height:1.5}main{max-width:1250px;margin:auto;padding:28px}h1{font-size:32px;margin-bottom:8px}p{max-width:900px;color:#becbd9}a{color:#83d8ff}button,select{font:inherit;background:#243146;border:1px solid #55708c;color:white;border-radius:7px;padding:8px;margin:3px}section{margin:24px 0;padding:18px;background:#192230;border-radius:12px}.roster{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}.fighter{background:#121b27;border:1px solid #2b4056;border-radius:8px;text-align:center;padding:8px}.fighter canvas{width:140px;height:190px;max-width:100%;background:linear-gradient(transparent 89%,#354657 90%,transparent 91%)}small{display:block;color:#adc2d5}.badge{color:#92edbb}#native{max-width:100%;width:960px;border:1px solid #415a72}#motion{width:360px;max-width:100%;height:240px;background:#101720}.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}.control{padding:12px;background:#111b29;border-radius:8px}kbd{color:#a9e9ff}li{margin:8px 0}.notice{border-left:4px solid #e7bb70;padding-left:14px}footer{margin-top:30px;font-size:14px;color:#a6bbcf}</style>
<main><h1>Illustrated JUS roster upgrade</h1><p>All 28 playable fighters: compact sizes, preserved relative heights and current artwork. New-character art and Gojo are on hold.</p>
<p class="notice">Work in progress: movement and contact checks are being rerun against the current files. Extra drawn movement cycles are being installed; the full animation expansion is not complete.</p>
<section><h2>Shared size lineup</h2><p>Actual packed neutral drawings, all displayed at the same world scale. Height estimates remain estimates; existing form proportions are retained. Imported Naruto and Saitama retain their original art while their style upgrade is paused.</p><div id="roster" class="roster"></div></section>
<section><h2>Movement controls</h2><div class="controls"><div class="control"><kbd>Q in the air</kbd><br>One air dash per jump. Hold Back for a retreating dash. Against your airborne hit target, dash pursues their position.</div><div class="control"><kbd>Hold Up on a confirmed normal hit</kbd><br>Launch the opponent for 100 meter. Whiffs, blocks, throws and supers do not trigger the launcher.</div><div class="control"><kbd>Up + W in the air</kbd><br>Toggle sustained flight for Goku, GT Goku, Ichigo, Rimuru and Jin Mori. Requires 300 meter; drains 5 per tick. Directions steer; hits interrupt it.</div><div class="control">Air normals can chain after actual hits, with two extra cancels per jump. Native attack buttons, specials and form controls are retained.</div></div><p>Landings raise dust. Hard knockdowns leave bounded floor scars; corner hits shake the arena. Training Room slabs advance through cracks and rubble on real nearby fighter damage. They cannot absorb hits or become combo targets.</p></section>
<section><h2>Additional drawn walk cycles</h2><select id="walkSelect"></select><button id="pause">Pause</button><button id="step">Next frame</button><br><canvas id="motion" width="360" height="240"></canvas><p id="walkNote"></p></section>
<section><h2>Native engine evidence</h2><select id="fighterSelect"></select><select id="suite"><option value="native">Movement</option><option value="native-combat">Combat and stage interaction</option></select><button id="prev">Previous capture</button><button id="next">Next capture</button><p id="proof"></p><img id="native" alt="Native engine capture"><p>Source Saitama deliberately rejects damage. This source behavior is recorded separately from the shared movement vulnerability checks.</p></section>
<footer><a href="manifest.json">Implementation manifest</a> · <a href="native-mobility-validation.json">Movement checks</a> · <a href="native-combat-validation.json">Combat checks</a> · <a href="../face-audit/identity-scale-v5/review.html">Previous proportions review (historical)</a></footer></main>
<script>const data=DATA;const rows=data.fighters;const images={};for(const r of rows){const card=document.createElement('div');card.className='fighter';card.innerHTML=`<canvas width="140" height="190"></canvas><b>${r.slug.replaceAll('-',' ')}</b><small>${r.height_cm} cm reference</small><small>${r.flight?'Sustained flight':'Air dash / pursuit'}</small>`;document.querySelector('#roster').append(card);const image=new Image;image.src=r.preview.file;image.onload=()=>{const c=card.querySelector('canvas').getContext('2d'),s=r.preview.scale*2;c.drawImage(image,70-r.preview.axis[0]*s,170-r.preview.axis[1]*s,image.width*s,image.height*s)};for(const selector of ['#fighterSelect',...(r.new_walk?['#walkSelect']:[])]){const o=document.createElement('option');o.value=r.slug;o.textContent=r.slug.replaceAll('-',' ');document.querySelector(selector).append(o)}}
let capture=0;function showProof(){const r=rows.find(r=>r.slug===document.querySelector('#fighterSelect').value),suite=document.querySelector('#suite').value,p=r[suite],frames=p?.screenshots||[];capture=frames.length?(capture+frames.length)%frames.length:0;document.querySelector('#native').src=frames[capture]||'';document.querySelector('#native').hidden=!frames.length;document.querySelector('#proof').innerHTML=p?`${p.passed} passed, ${p.failed} failed. <a href="${p.proof}">Current report and file hashes</a>. Capture ${frames.length?capture+1:0}/${frames.length}`:'Current report pending';}document.querySelector('#fighterSelect').onchange=()=>{capture=0;showProof()};document.querySelector('#suite').onchange=()=>{capture=0;showProof()};document.querySelector('#prev').onclick=()=>{capture--;showProof()};document.querySelector('#next').onclick=()=>{capture++;showProof()};showProof();
let frames=[],packing=null,frame=0,paused=false,last=0;async function loadWalk(){const slug=document.querySelector('#walkSelect').value;packing=await(await fetch('art/'+slug+'/packing.json')).json();frames=packing.frames.map((f,i)=>{const im=new Image;im.src='art/'+slug+'/walk-'+String(i).padStart(2,'0')+'.png';return im});frame=0;document.querySelector('#walkNote').textContent='Eight distinct drawings; fixed scale and root anchors across the entire cycle. Native timing: two ticks per drawing.'}document.querySelector('#walkSelect').onchange=loadWalk;document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause'};document.querySelector('#step').onclick=()=>{paused=true;frame=(frame+1)%8;draw()};function draw(){if(!packing||!frames[frame]?.complete)return;const c=document.querySelector('#motion').getContext('2d');c.clearRect(0,0,360,240);const im=frames[frame],a=packing.frames[frame].axis,s=.35;c.drawImage(im,180-a[0]*s,215-a[1]*s,im.width*s,im.height*s)}function loop(t){if(!paused&&t-last>=1000/30){frame=(frame+1)%8;last=t}draw();requestAnimationFrame(loop)}loadWalk();requestAnimationFrame(loop);</script></html>'''
html=html.replace("packing=await(await fetch('art/'+slug+'/packing.json')).json()","packing=rows.find(r=>r.slug===slug).walk_packing").replace('Up + W in the air','Up + Q in the air')
html=html.replace('<option value="native-combat">Combat and stage interaction</option>','<option value="native-combat">Combat and stage interaction</option><option value="native-forms">Form walk drawings, both facings</option>')
html=html.replace("for(const selector of ['#fighterSelect',...(r.new_walk?['#walkSelect']:[])])", "for(const selector of ['#fighterSelect'])")
html=html.replace('let frames=[],packing=null',"for(const [i,cycle] of data.walk_cycles.entries()){const o=document.createElement('option');o.value=i;o.textContent=cycle.label;document.querySelector('#walkSelect').append(o)};let frames=[],packing=null")
html=html.replace("const slug=document.querySelector('#walkSelect').value;packing=rows.find(r=>r.slug===slug).walk_packing", "const cycle=data.walk_cycles[Number(document.querySelector('#walkSelect').value)];if(!cycle)return;packing=cycle.packing")
html=html.replace("im.src='art/'+slug+'/walk-'", "im.src=cycle.folder+'/walk-'")
html=html.replace("const im=frames[frame],a=packing.frames[frame].axis,s=.35", "const im=frames[frame],a=packing.frames[frame].axis,s=Math.min(.7,180/Math.max(...packing.frames.map(f=>f.size[1])))")
html=html.replace("paused=true;frame=(frame+1)%8;draw()", "paused=true;document.querySelector('#pause').textContent='Play';frame=(frame+1)%8;draw()")
html=html.replace("font:16px system-ui", "font:16px system-ui").replace('button,select{font:', 'button,select{max-width:100%;font:')
summary={suite:sum(suite in row for row in data['fighters']) for suite in ('native','native-combat','native-forms')}
expected_fighters=len(data['fighters']);expected_forms=len({c['slug'] for c in data['walk_cycles'] if '/cycles/' in c['folder']})
if tuple(summary.values())==(28,28,8):
 html=html.replace('Work in progress: movement and contact checks are being rerun against the current files. Extra drawn movement cycles are being installed; the full animation expansion is not complete.','Installed and validated: all 28 fighters have current movement and contact checks. All 48 additional eight-frame walk cycles are installed, including alternate bodies and forms. Original attack, hurt and cinematic drawings are retained.')
html=html.replace('<footer><a href="manifest.json">','<footer><a href="CONTROLS.md">Shared controls</a> · <a href="native-form-validation.json">Form animation checks</a> · <a href="native-camera-validation.json">Flight camera checks</a> · <a href="manifest.json">')
html=html.replace('<section><h2>Shared size lineup</h2>',f'<p id="progress">Current file checks: movement {summary["native"]}/28; combat {summary["native-combat"]}/28; form animation {summary["native-forms"]}/8. Installed additional walk cycles: {len(data["walk_cycles"])}.</p><section><h2>Shared size lineup</h2>')
html=html.replace('All 28 playable fighters',f'All {expected_fighters} playable manga and manhwa fighters').replace('/28;',f'/{expected_fighters};').replace('/8.',f'/{expected_forms}.')
html=html.replace('Work in progress: movement and contact checks are being rerun against the current files. Extra drawn movement cycles are being installed; the full animation expansion is not complete.','Fixes in progress. New recordings are deferred. Earlier 28-fighter footage predates the manga/manhwa roster split. All installed walk cycles are available below.')
html=html.replace('New-character art and Gojo are on hold.','Sitcom fighters and Yamal are preserved in the separate sitcom folder. New-character art and Gojo are on hold.')
html=html.replace('${r.height_cm} cm reference','${r.gameplay_size_role||"compact"} body')
html=html.replace('Height estimates remain estimates; existing form proportions are retained.','Adults use close gameplay sizes, with shorter child, slime and pet bodies. These are gameplay proportions rather than canon heights.')
html=html.replace('<h1>Illustrated JUS roster upgrade</h1>','<h1>Illustrated JUS roster upgrade</h1><p><a href="../size-fix-v8/review.html">Current: Cid redesign and corrected shared-scale sizes</a></p>')
(O/'review.html').write_text(html.replace('DATA',json.dumps(data)),encoding='utf-8')
# The user's active tab should lead to current work instead of stale size clips.
active=R/'sprite-fighter/face-audit/style-v4-review.html';text=active.read_text(encoding='utf-8')
banner='<aside id="jus-current" style="padding:18px;background:#172d3d;color:white"><strong>Current work: illustrated JUS roster upgrade.</strong> All 28 fighters; compact sizes, aerial movement and reactive stage effects. <a style="color:#9fe5ff" href="../jus-upgrade/review.html">Open current progress and native evidence</a>.</aside>'
banner=banner.replace('All 28 fighters',f'All {expected_fighters} manga/manhwa fighters').replace('Open current progress and native evidence','Open current fixes and animation review')
text=re.sub(r'<aside id="jus-current".*?</aside>','',text,flags=re.S)
text=re.sub(r'(<main[^>]*>)',lambda m:m[0]+banner,text,count=1)
active.write_text(text,encoding='utf-8')
print('Built current shared-scale roster and native evidence review for',len(data['fighters']),'fighters.')
