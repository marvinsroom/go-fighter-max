"""Review actual restored-port captures, with timing-aware playback."""
from pathlib import Path
from collections import defaultdict
import json,html
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/jinwoo'
r=json.loads((S/'ported-native-validation.json').read_text());assert r['status']=='Complete' and r['failed']==0
cases=defaultdict(list)
for f in r['frames']:
 src=f.get('src',f"replays/{r['capture_directory']}/Jinwoo_hybrid{f['index']-1:03d}.png")
 assert (S/src).exists(),src
 cases[f['case_name']].append({'src':src,**f})
spacing_file=S/'spacing-ultimate-validation.json'
if spacing_file.exists():
 spacing=json.loads(spacing_file.read_text())
 assert spacing['status']=='Complete' and spacing['failed']==0
 fresh=defaultdict(list)
 for f in spacing['frames']:
  src=f"replays/{spacing['capture_directory']}/Jinwoo_hybrid{f['index']-1:03d}.png"
  assert (S/src).exists(),src
  fresh[f['case_name']].append({'src':src,**f})
 cases.update(fresh)
outfit_file=S/'white-shirt-native-validation.json'
if outfit_file.exists():
 outfit=json.loads(outfit_file.read_text())
 assert outfit['status']=='Complete' and outfit['failed']==0
 # Keep the previous outfit's capture review accessible as history, while the
 # current viewer shows only captures of the installed wardrobe.
 if not (S/'review-v8.html').exists():
  (S/'ported-review-data-v8.js').write_bytes((S/'ported-review-data.js').read_bytes())
  (S/'review-v8.html').write_text((S/'review.html').read_text(encoding='utf-8').replace('ported-review-data.js','ported-review-data-v8.js'),encoding='utf-8')
 cases=defaultdict(list)
 for f in outfit['frames']:
  src=f"replays/{outfit['capture_directory']}/Jinwoo_hybrid{f['index']-1:03d}.png"
  assert (S/src).exists(),src
  cases[f['case_name']].append({'src':src,**f})
idle_file=S/'idle-native-validation.json'
if idle_file.exists():
 idle=json.loads(idle_file.read_text())
 assert idle['status']=='Complete' and idle['failed']==0
 for f in idle['frames']:
  src=f"replays/{idle['capture_directory']}/Jinwoo_hybrid{f['index']-1:03d}.png"
  assert (S/src).exists(),src
  cases[f['case_name']].append({'src':src,**f})
for name,frames in list(cases.items()):
 if name.startswith('Original ') and any(word in name.lower() for word in ('ultimate','mutilate','antares')):
  start=next((i for i,f in enumerate(frames) if f['state'] in (3000,3100,3200)),None)
  if start is not None:cases[name]=frames[start:]
audit=json.loads((S/'ported-coverage-audit.json').read_text())
(S/'ported-review-data.js').write_text('window.PORTED_JINWOO='+json.dumps({'cases':cases,'passed':r['passed'],'audit':audit})+';',encoding='utf-8')
old=S/'review-v6.html'
if not old.exists():old.write_bytes((S/'review.html').read_bytes())
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jinwoo · Restored original combat</title>
<style>*{box-sizing:border-box}body{margin:0;background:#080b14;color:#eff1ff;font:17px/1.6 system-ui}main{max-width:1180px;margin:auto;padding:50px 24px}h1{font-size:clamp(38px,6vw,76px);line-height:1.05}p{color:#bdc6de;max-width:830px}a{color:#bcaaff}button,select{font:inherit;color:white;background:#24243c;border:1px solid #625c93;border-radius:7px;padding:8px;margin:4px}section{margin:42px 0}.capture{width:100%;background:#131626;border-radius:12px}kbd{background:#2b2543;padding:3px 7px;border-radius:4px}.status{color:#b9e8d2}#detail{font:14px monospace}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.cards img{width:100%;background:#1b2434;border-radius:10px}table{width:100%;text-align:left;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #2d3550}@media(max-width:700px){.cards{grid-template-columns:repeat(2,1fr)}}</style>
<main><p>SHADOW MONARCH / ORIGINAL COMBAT · ILLUSTRATED ROSTER</p><h1>SUNG JINWOO</h1><p>The original port's movement, directional moves, weapon changes, domain special and ultimate variants are restored. Our illustrated Jinwoo and four shadow designs replace their player and summon sprites.</p>
<p>Open <strong>Play Jinwoo.cmd</strong>. Player 1: arrows to move; <kbd>Z</kbd><kbd>X</kbd><kbd>C</kbd> attacks. Hold <kbd>Enter</kbd> to fill meter <em>and the separate Ruler gauge</em>. The original ultimate needs that gauge ready and at least 2000 meter.</p>
<table><tr><th>Input</th><th>Original port move / retained feature</th></tr><tr><td>D (release)</td><td>Original Mutilate ultimate; King Domain while the domain power-up is active</td></tr><tr><td>S (release)</td><td>Original Monarch's Domain power-up; original special in weapon mode</td></tr><tr><td>Down + S</td><td>Original weapon change</td></tr><tr><td>Down + D</td><td>Original Antares variant in the first weapon mode, with meter and Ruler gauge ready</td></tr><tr><td>A + C</td><td>Original summon selector</td></tr><tr><td>A / toward+A / away+A / down+A</td><td>Your assigned Igris / Beru / Iron / Tank assists</td></tr><tr><td>W</td><td>Random playable shadow, excluding the preceding choice; press again to return</td></tr></table><p><a href="CONTROLS.md">Player 1 and Player 2 controls</a></p>
<section><h2>Original port in the engine</h2><p id="status" class="status"></p><select id="case" aria-label="Choose native move"></select><button id="play">Play</button><button id="previous">Previous</button><button id="next">Next</button><select id="speed" aria-label="Playback speed"><option value="1">1× speed</option><option value="0.5">½ speed</option><option value="0.25">¼ speed</option></select><img id="frame" class="capture" alt="Native Jinwoo engine capture"><p id="detail"></p></section>
<section><h2>Our four shadows inside the port</h2><p>Igris, Beru, Iron and Tank use our illustrated animation drawings wherever their native actor sprites appear. Native timing, attack logic, movement and effects are retained. Other original summons retain their creator's artwork. Your playable shadow transformations still have their own attacks and finishers.</p><div class="cards">SHADOWS</div></section>
<section><h2>Move and motion audit</h2><p>All 809 original animation actions, 5075 original frame rows and 32 original command routes are retained. The audit checks original frame timing and offsets, state physics, velocity, damage and attack controllers. Visual adapters calibrate drawing scales, stabilize the camera and keep captured opponents in their own reaction artwork.</p><p><a href="ported-coverage-audit.json">Full source coverage audit</a> · <a href="ported-native-validation.json">Native results</a> · <a href="hybrid-build-report.json">Art and build report</a> · <a href="art/forms-v6/README.md">Shadow artwork and exact prompts</a></p></section>
<p>Original fighter by <a href="https://www.youtube.com/watch?v=0dYxiFJc-eE">RyoumenS</a>, with credited contributions by JONHNY6969. Original files remain preserved. <a href="review-v6.html">Previous custom-finisher review</a>.</p></main>
<script src="ported-review-data.js"></script><script>
const data=window.PORTED_JINWOO,select=document.getElementById('case');let index=0,timer=null,playing=false;
const names=Object.keys(data.cases),preferred=names.includes('Base idle')?'Base idle':'Original Mutilate ultimate';names.sort((a,b)=>(a===preferred?-1:b===preferred?1:0));for(const n of names){const o=document.createElement('option');o.textContent=n;select.append(o)}
document.getElementById('status').textContent=`${data.passed} native checks passed. Captures below come from the restored original moves.`;
function show(delta=0){const rows=data.cases[select.value]||[];if(!rows.length)return;index=(index+delta+rows.length)%rows.length;const f=rows[index];document.getElementById('frame').src=f.src;document.getElementById('detail').textContent=`Tick ${f.case_tick} · state ${f.state} · animation ${f.animation} · frame ${index+1}/${rows.length}`;}
function schedule(){clearTimeout(timer);if(!playing)return;const rows=data.cases[select.value],a=rows[index],b=rows[(index+1)%rows.length];const ms=b.case_tick>a.case_tick?(b.case_tick-a.case_tick)*1000/60:500;timer=setTimeout(()=>{show(1);schedule()},Math.max(30,ms/Number(document.getElementById('speed').value)))}
select.onchange=()=>{index=0;show();schedule()};document.getElementById('play').onclick=function(){playing=!playing;this.textContent=playing?'Pause':'Play';schedule()};document.getElementById('previous').onclick=()=>{show(-1);schedule()};document.getElementById('next').onclick=()=>{show(1);schedule()};document.getElementById('speed').onchange=schedule;show();
</script></html>'''
cards=''.join(f'<div><img src="art/forms-v6/{name}-combat.png" alt="{name} illustrated combat drawings"><p>{name.title()}</p></div>' for name in ('igris','beru','iron','tank'))
if spacing_file.exists():
 page=page.replace('Native timing, attack logic, movement and effects are retained.', 'Native attacks and effects are retained. The four shadows stop at the opponent\'s body instead of rushing through it; native grabs keep their captured-target positioning.')
 page=page.replace('Visual adapters calibrate drawing scales,', 'Explicit summon body guards stop overlap and cap approach speed at contact. Visual adapters calibrate drawing scales,')
 page=page.replace('<a href="ported-native-validation.json">Native results</a>', '<a href="ported-native-validation.json">Source combat results</a> · <a href="spacing-native-validation.json">64 summon contact checks</a> · <a href="spacing-ultimate-validation.json">Updated ultimates and assists</a>')
if outfit_file.exists():
 page=page.replace('<h1>SUNG JINWOO</h1>','<h1>SUNG JINWOO</h1><p><strong>White T-shirt · open black coat · black trousers · violet daggers.</strong> The outfit is consistent across all 32 player drawings, including movement, attacks, crouching and reactions.</p>')
 page=page.replace('<a href="CONTROLS.md">Player 1 and Player 2 controls</a>','<a href="CONTROLS.md">Player 1 and Player 2 controls</a> · <a href="art/white-shirt-v9/README.md">Outfit artwork and prompts</a> · <a href="white-shirt-native-validation.json">13 current-outfit checks</a> · <a href="review-v8.html">Previous outfit review</a>')
 page=page.replace('Captures below come from the restored original moves.', 'The 13 clips below show the current white-shirt outfit in the engine.')
if idle_file.exists():
 page=page.replace('The 13 clips below show the current white-shirt outfit in the engine.', 'Current captures include all three corrected idle loops, genuine knockdown recovery and the original moves.')
 page=page.replace('<h2>Original port in the engine</h2>', '<h2>Idle fix and original combat</h2><p>Standing stays upright throughout every idle frame in all three weapon modes. The imported P1 arrow is hidden. Actual knockdowns still fall, land and recover normally. <a href="idle-native-validation.json">Frame-by-frame idle and recovery checks</a>.</p>')
(S/'review.html').write_text(page.replace('SHADOWS',cards),encoding='utf-8')
print('PORTED_REVIEW_PACKAGED',len(cases),'native captured moves')
