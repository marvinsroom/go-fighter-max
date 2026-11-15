"""Package captured native frames and the current fighter review."""
from pathlib import Path
from collections import defaultdict
import json,html,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/jinwoo';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
report=json.loads((S/'hybrid-native-validation.json').read_text());build=json.loads((S/'hybrid-build-report.json').read_text())
frames=defaultdict(list)
for row in report['frames']:
 path=S/'replays/hybrid-v6'/f"Jinwoo_hybrid{row['index']-1:03d}.png"
 if path.exists():frames[row['name']].append({'src':str(path.relative_to(S)).replace('\\','/'),**row})
framing=json.loads((S/'hybrid-framing-validation.json').read_text()) if (S/'hybrid-framing-validation.json').exists() else None
if framing and framing.get('status')=='Complete' and framing.get('failed')==0:
    latest=defaultdict(list)
    for row in framing['frames']:
        path=S/'replays/framing-v6'/f"Jinwoo_hybrid{row['index']-1:03d}.png"
        if path.exists():latest[row['name']].append({'src':str(path.relative_to(S)).replace('\\','/'),**row})
    frames.update(latest)
(S/'hybrid-review-data.js').write_text('window.JINWOO_REVIEW='+json.dumps({'cases':frames,'passed':report.get('passed'),'failed':report.get('failed'),'profiles':build['profiles']})+';',encoding='utf-8')
cards=''
for name,cfg in build['profiles'].items():
 cards+=f'<article><h3>{name.title()}</h3><img src="art/forms-v6/{name}-combat.png" alt="{name} combat animation sheet"><p>{html.escape(cfg["skill"])}<br>{html.escape(cfg["super"])}<br><strong>{html.escape(cfg["ultimate"])}</strong></p></article>'
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jinwoo · Imported combat / illustrated upgrade</title><style>
*{box-sizing:border-box}body{margin:0;background:#080b14;color:#eff1ff;font:17px/1.6 system-ui}main{max-width:1180px;margin:auto;padding:50px 24px}h1{font-size:clamp(38px,6vw,76px);line-height:1.05}p{color:#bdc6de;max-width:800px}a{color:#ae9bff}button,select{font:inherit;color:#fff;background:#25243d;border:1px solid #625c93;border-radius:7px;padding:8px;margin:4px}section{margin:48px 0}.capture{width:100%;background:#131626;border-radius:12px}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}article{background:#14192a;border:1px solid #303b59;padding:20px;border-radius:12px}article img{width:100%;background:#252b38}kbd{background:#2b2543;padding:3px 7px;border-radius:4px}.status{color:#b9e8d2}#detail{font:14px monospace}button:focus-visible,select:focus-visible{outline:3px solid #c7bcff}@media(max-width:700px){.cards{grid-template-columns:1fr}}</style><main>
<p>SHADOW MONARCH / ILLUSTRATED COMBAT PORT</p><h1>SUNG JINWOO</h1><p>Imported RyoumenS combat, upgraded with our illustrated fighter and four playable shadows. Dagger combinations, assigned summons, random transformations, and a distinct fighting style for every form.</p>
<p>Open <strong>Play Jinwoo.cmd</strong>. Player 1: arrows to move; <kbd>Z</kbd><kbd>X</kbd><kbd>C</kbd> attacks, <kbd>A</kbd> summon, <kbd>S</kbd> super, <kbd>D</kbd> ultimate, <kbd>W</kbd> random transformation. Hold <kbd>Enter</kbd> to charge meter. <a href="CONTROLS.md">All controls</a>.</p>
<section><h2>Native engine review</h2><p id="status" class="status"></p><select id="cases" aria-label="Choose captured move"></select><button id="play">Play</button><button id="previous">Previous frame</button><button id="next">Next frame</button><img id="frame" class="capture" alt="Native engine capture"><p id="detail"></p><p>The viewer shows actual game captures at their recorded ticks. Frame stepping makes posture and scale changes easier to inspect.</p></section>
<section><h2>Four independent combat styles</h2><p>Igris fences and cuts with his sword. Beru uses rapid claw attacks and aerial pursuit. Iron has slower axe and shield blows. Tank stays on four paws for charges and swipes. Each has nine normals, a grounded and aerial signature, a super and an ultimate.</p><div class="cards">CARDS</div></section>
<section><h2>Body collisions follow the form</h2><p>Tank has a wider, shorter body and push box. Igris, Beru and Iron each have their own head and torso geometry; crouching and knockdown use separate posture boxes. The native high/low attack probes test these differences during combat.</p><p><a href="hybrid-native-validation.json">Native results</a> · <a href="hybrid-build-report.json">Build and collision report</a> · <a href="art/forms-v6/README.md">96 new drawings and exact prompts</a></p></section>
<section><h2>Preserved summons and transformations</h2><p>Neutral summon calls Igris; toward calls Beru; away calls Iron; down calls Tank. Each costs 250 meter with a shared cooldown. Transformation chooses a random shadow; press again to return. Jinwoo’s army ultimate retains all four shadows.</p><p>Source: <a href="https://www.youtube.com/watch?v=0dYxiFJc-eE">RyoumenS’s creator release</a>. Original archive, credit and source files are retained. <a href="review-v5.html">Previous project version</a>.</p></section>
</main><script src="hybrid-review-data.js"></script><script>
const data=window.JINWOO_REVIEW,selector=document.getElementById('cases');let current=0,timer=null;
for(const name of Object.keys(data.cases)){const o=document.createElement('option');o.textContent=name;selector.append(o)}
document.getElementById('status').textContent=`${data.passed??'Pending'} native checks passed${data.failed?' · '+data.failed+' need attention':''}.`;
function show(delta=0){const rows=data.cases[selector.value]||[];if(!rows.length)return;current=(current+delta+rows.length)%rows.length;const row=rows[current];document.getElementById('frame').src=row.src;document.getElementById('detail').textContent=`Tick ${row.tick} · state ${row.state} · animation ${row.animation} · frame ${current+1}/${rows.length}`}
selector.onchange=()=>{current=0;show()};document.getElementById('previous').onclick=()=>show(-1);document.getElementById('next').onclick=()=>show(1);document.getElementById('play').onclick=function(){if(timer){clearInterval(timer);timer=null;this.textContent='Play'}else{timer=setInterval(()=>show(1),650);this.textContent='Pause'}};show();
</script></html>'''.replace('CARDS',cards)
(S/'review.html').write_text(page,encoding='utf-8')
print('HYBRID_REVIEW_PACKAGED',len(frames),'native captured cases')
