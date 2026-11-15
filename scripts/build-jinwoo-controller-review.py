"""Build Jinwoo's fresh live-runtime move and controller review."""
from pathlib import Path
import json, hashlib

R=Path(__file__).resolve().parents[1]; S=R/'sprite-fighter/characters/jinwoo'
base='full-review-20261024'; complete='full-review-complete-20261024'; r2='full-review-retakes2-20261024'; r3='full-review-retakes3-20261024'
na='full-review-naruto-a-20261024';nb='full-review-naruto-b-20261024';nc='full-review-naruto-c-20261024'
jr='full-review-naruto-jump-retake-20261024'
fr='full-review-naruto-final-retake-20261024'
jr2='full-review-naruto-jump-retake-v2-20261024'
feel='full-review-naruto-feel-retake-v6-20261024'
audit='full-review-naruto-audit-retake-v6-20261024'
airlive='full-review-naruto-final-retake-air-live-v4-20261024'
igrisfix='full-review-naruto-igris-art-v3-20261024'
completeart='full-review-naruto-complete-art-v10-20261025'
runs=(na,nb,nc,jr,fr,jr2,feel,audit,airlive,igrisfix,completeart)
reports={n:json.loads((S/f'validation/{n}.json').read_text()) for n in runs}
replace={}
checks={n:{c['name']:c for c in data['checks']} for n,data in reports.items()}
frames={n:{} for n in reports}
for run,data in reports.items():
 for f in data['frames']:frames[run].setdefault(f['case_name'],[]).append(f)
ordered=[]
aliases={
 'Jinwoo greatsword light':'Greatsword attack 1',
 'Igris normal 1':'igris normal 1','Igris normal 2':'igris normal 2','Igris normal 3':'igris normal 3',
 'Beru normal 1':'beru normal 1','Beru normal 2':'beru normal 2','Beru normal 3':'beru normal 3',
 'Iron normal 1':'iron normal 1','Iron normal 2':'iron normal 2','Iron normal 3':'iron normal 3',
 'Tank normal 1':'tank normal 1','Tank normal 2':'tank normal 2','Tank normal 3':'tank normal 3',
 'Jinwoo corrected stance':'Daggers stance',
 'Jinwoo corrected walk':'Daggers walk',
 'Jinwoo corrected jump':'Daggers jump',
 'Greatsword corrected stance':'Greatsword stance',
 'Greatsword corrected walk':'Greatsword walk',
 'Tank corrected walk':'tank walk',
 'Tank corrected attack':'tank normal 1',
 'Tank corrected normal 2':'tank normal 2',
 'Tank corrected normal 3':'tank normal 3',
 'Tank corrected crouch 1':'tank crouch 1',
 'Tank corrected crouch 2':'tank crouch 2',
 'Tank corrected crouch 3':'tank crouch 3',
 'Tank corrected air 1':'tank air 1',
 'Tank corrected air 2':'tank air 2',
 'Tank corrected air 3':'tank air 3',
 'Tank corrected signature':'tank signature',
 'Tank corrected air signature':'tank air signature',
 'Tank corrected super':'Tank super',
 'Tank corrected ultimate':'Tank ultimate',
 'Tank corrected assist':'Tank assist',
 'Domain power-up corrected':'Domain power-up',
 'Mutilate ultimate corrected':'Mutilate ultimate',
 'Greatsword King Domain corrected':'Greatsword King Domain ultimate',
 'Greatsword Antares corrected':'Greatsword Antares ultimate',
}
for run in runs:
 for f in reports[run]['frames']:
  name=aliases.get(f['case_name'],f['case_name'])
  if name not in ordered:ordered.append(name)
cases=[]
obsolete={
 'Jinwoo walk','Jinwoo back','Jinwoo down','Jinwoo jump','Jinwoo normal 1','Jinwoo normal 2','Jinwoo normal 3',
 'Jinwoo ultimate hit','igris ultimate hit','beru ultimate hit','iron ultimate hit','tank ultimate hit',
 'Igris ultimate','Beru ultimate','Iron ultimate','Tank ultimate',
}
for name in ordered:
 if name in obsolete:continue
 corrected=next((raw for raw,canonical in aliases.items() if canonical==name and raw in frames[audit]),None)
 fresh=next((raw for raw,canonical in aliases.items() if canonical==name and raw in frames[completeart]),None)
 if name in frames[completeart]:run=completeart;recorded=name
 elif fresh:run=completeart;recorded=fresh;replace[name]=fresh
 elif corrected:
  run=audit;recorded=corrected;replace[name]=corrected
 else:
  run=next(r for r in (igrisfix,airlive,feel,jr2,fr,jr,nc,na,nb) if name in frames[r]);recorded=name
 take=frames[run].get(recorded,[])
 if name.startswith('Daggers air attack'):
  # Review the airborne move itself, not the grounded setup/recovery frames.
  take=[f for f in take if f.get('y',0)<-20 and f.get('state') in (50,600,610,620)]
 if not take:continue
 check=checks[run][recorded]
 name=name.replace('â€”','—')
 cases.append(dict(name=name,frames=[f'replays/{run}/Jinwoo_hybrid{f["index"]-1:03d}.png' for f in take],passed=bool(check['passed']),damage=check.get('damage',0)))

def category(name):
 low=name.lower()
 if name in {'Responsive dagger walk','Dagger light chain','Dagger light to medium','Dagger light to heavy','X — close grab and throw'}:
  return 'Core controls and combos'
 if 'super' in low or 'ultimate' in low or 'domain' in low:return 'Supers and ultimates'
 if low.startswith('dagger') or name=='Return to daggers':return 'Daggers'
 if low.startswith('greatsword') or name=='Equip greatsword':return 'Greatsword'
 if 'Skill' in name or name.startswith(('QCF','QCB','Down +','R3','L3','Right stick right')):return 'Human skills'
 if 'assigned summon' in low or 'assist' in low or name=='Native summon selector':return 'Summons and assists'
 if low.startswith('igris'):return 'Igris moves'
 if low.startswith('beru'):return 'Beru moves'
 if low.startswith('iron'):return 'Iron moves'
 if low.startswith('tank'):return 'Tank moves'
 return 'Other'

category_order=['Core controls and combos','Daggers','Greatsword','Human skills','Summons and assists','Igris moves','Beru moves','Iron moves','Tank moves','Supers and ultimates','Other']
for c in cases:c['category']=category(c['name'])
cases.sort(key=lambda c:(category_order.index(c['category']),c['name'].lower()))

controls=[
 ('Move / crouch / jump','Left stick','Arrow keys'),('Light / medium / grab / heavy','A / B / X / Y','Z / X / A / C'),
 ('Dagger air attacks','Jump, then A / B / Y','Jump, then Z / X / C'),
 ('Charge meter','Hold LB','Hold Enter'),('Summon Igris / Beru / Iron / Tank','LT / toward+LT / away+LT / down+LT','W / toward+W / away+W / down+W'),
 ('Transform Igris / Beru / Iron / Tank','D-pad Up / Right / Left / Down','Q+F / Q+G / Q+H / Q+R'),
 ('Super / ultimate','RT / RB','S / D'),('Switch daggers ↔ greatsword','Right stick Down','Down+S'),
 ('Mutilate / King Domain','Right stick Up','Q+Y'),('Monarch Domain','Right stick Left','W+Y'),('Spoiler Skill','Right stick Right','W+T'),
 ('Skill 11 / Skill 12','R3 / L3','Q+W / Q+T'),('Guard high / low','Away / down-away','Away / down-away'),
 ('Skills 1–6','QCF/QCB + A, B, or RT','QCF/QCB + Z, X, or S'),('Skills 7–9','Down + A, B, or RT','Down + Z, X, or S')]
rows=''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in controls)
data=json.dumps(cases,separators=(',',':')).replace('</','<\\/')
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sung Jinwoo - Combat review</title><style>
:root{{color-scheme:dark;--bg:#0a0a11;--panel:#14141f;--line:#2e2c40;--muted:#b2aec5;--violet:#9d7cff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:#f6f3ff;font:16px/1.6 system-ui,sans-serif}}main{{max-width:1120px;margin:auto;padding:48px 24px}}a{{color:var(--violet)}}.eyebrow{{font-size:12px;letter-spacing:.22em;color:var(--violet)}}h1{{font-size:clamp(42px,7vw,80px);letter-spacing:-.05em;line-height:1;text-transform:uppercase;margin:16px 0}}h2{{font-size:27px;letter-spacing:-.02em;margin:0 0 12px}}p{{color:var(--muted);margin:10px 0 18px}}.intro{{max-width:760px}}section{{margin:40px 0}}.character-nav,.featured,.toolbar{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}.character-nav{{margin-bottom:32px}}.character-nav a{{padding:8px 14px;border:1px solid var(--line);border-radius:7px;text-decoration:none}}.character-nav a[aria-current=page]{{color:#fff;background:#30233f;border-color:var(--violet)}}button,select{{font:inherit;color:inherit;background:var(--panel);border:1px solid #4a415f;border-radius:6px;padding:8px 12px}}button{{cursor:pointer}}button:hover{{border-color:var(--violet)}}button[aria-pressed=true]{{background:#49325f;border-color:var(--violet)}}.featured{{margin:18px 0}}.featured button{{flex:1 1 190px;text-align:left}}.toolbar{{margin:16px 0;align-items:flex-end}}.toolbar label{{display:flex;flex-direction:column;gap:5px;font-size:13px;color:var(--muted);min-width:0}}.category-label{{flex:1 1 230px}}.clip-label{{flex:2 1 330px}}select{{width:100%}}#capture{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;background:#050509;border:1px solid var(--line);border-radius:10px}}.playback button{{flex:1 1 120px}}#detail,#status{{font-size:13px;color:var(--muted)}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:620px}}td,th{{border-bottom:1px solid var(--line);padding:12px;text-align:left}}th{{color:var(--muted);font-weight:500;font-size:13px}}.shadows{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.shadow{{padding:14px;background:var(--panel);border:1px solid var(--line);border-radius:8px}}.shadow strong{{display:block;color:#fff}}.shadow span{{font-size:13px;color:var(--muted)}}.review-links{{font-size:14px}}footer{{border-top:1px solid var(--line);padding-top:20px;font-size:13px;color:var(--muted)}}@media(max-width:700px){{main{{padding:30px 16px}}.toolbar>label{{flex:1 1 100%}}.shadows{{grid-template-columns:1fr 1fr}}.character-nav a{{flex:1 1 145px;text-align:center}}}}
</style></head><body><main>
<nav class="character-nav" aria-label="Character reviews"><a href="../rimuru/review.html">Rimuru Tempest</a><a href="../cid/review.html">Cid Kagenou</a><a href="../jinwoo/review.html" aria-current="page">Sung Jinwoo</a><a href="../pyowol/review.html">Pyo Wol</a><a href="../edward/review.html">Edward Elric</a><a href="../vikir/review.html">Vikir</a><a href="../jin-mori/review.html">Jin Mori</a><a href="../baam/review.html">Baam</a><a href="../jin-mu-won/review.html">Jin Mu-Won</a><a href="../kim-dokja/review.html">Kim Dokja</a></nav>
<header><div class="eyebrow">FIGHTER / COMBAT REVIEW</div><h1>Sung Jinwoo</h1><p class="intro">Daggers and greatsword combat, three playable dagger aerials, controller routes, shadow soldiers, assists, supers, and cinematic ultimates—recorded against Naruto from the live fighter runtime.</p></header>
<section id="viewer" aria-labelledby="viewer-title"><h2 id="viewer-title">Native game captures</h2><p>Choose a category and move, or use a featured shortcut. Pause, step, or slow playback to inspect individual frames.</p>
<nav id="featured" class="featured" aria-label="Featured move previews"></nav>
<div class="toolbar"><label class="category-label">Category<select id="category" aria-label="Move category"></select></label><label class="clip-label">Move<select id="clip" aria-label="Capture clip"></select></label></div>
<img id="capture" alt="Sung Jinwoo native game capture" width="1280" height="720">
<div class="toolbar playback"><button id="previous" type="button">Previous frame</button><button id="play" type="button">Pause</button><button id="next" type="button">Next frame</button><label>Playback speed<select id="speed" aria-label="Playback speed"><option value="1">1x</option><option value="0.5">0.5x</option><option value="0.25">0.25x</option></select></label></div>
<p id="detail" aria-live="polite"></p><p id="status">{len(cases)} live move cases · {sum(len(c['frames']) for c in cases)} recorded frames · updated October 24, 2026</p></section>
<section><h2>Controls</h2><p>Controller shortcuts use the Jinwoo bridge launched with Play Jinwoo. QCF means down, down-forward, forward; QCB means down, down-back, back.</p><div class="table-wrap"><table><thead><tr><th>Action</th><th>Xbox controller</th><th>Keyboard (P1)</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>Shadow army</h2><div class="shadows"><div class="shadow"><strong>Igris</strong><span>Sword pressure and fast confirms</span></div><div class="shadow"><strong>Beru</strong><span>Rapid aerial and claw offense</span></div><div class="shadow"><strong>Iron</strong><span>Armored impact attacks</span></div><div class="shadow"><strong>Tank</strong><span>Large-body rushes and assists</span></div></div></section>
<footer><p class="review-links"><a href="CONTROLS.md">Detailed keyboard notes</a> · <a href="../../Jinwoo%20Controls.txt">Controller quick reference</a> · <a href="validation/controller-review.json">Validation manifest</a></p></footer>
</main><script>const cases={data};const byCategory={{}};for(const c of cases)(byCategory[c.category]??=[]).push(c);const category=document.querySelector('#category'),clip=document.querySelector('#clip'),capture=document.querySelector('#capture'),detail=document.querySelector('#detail'),play=document.querySelector('#play'),featured=document.querySelector('#featured'),speed=document.querySelector('#speed');let current=null,index=0,playing=true,timer=null;for(const name of Object.keys(byCategory)){{const o=document.createElement('option');o.value=name;o.textContent=name;category.append(o)}}function populate(){{clip.replaceChildren();for(const c of byCategory[category.value]){{const o=document.createElement('option');o.value=c.name;o.textContent=c.name;clip.append(o)}}choose()}}function choose(){{current=cases.find(c=>c.category===category.value&&c.name===clip.value)||byCategory[category.value][0];index=0;show()}}function show(delta=0){{clearTimeout(timer);index=(index+delta+current.frames.length)%current.frames.length;capture.dataset.loaded='pending';capture.src=current.frames[index];detail.textContent=`${{current.name}} · Frame ${{index+1}} of ${{current.frames.length}}${{current.damage?' · Recorded damage '+current.damage:''}}`;for(const b of featured.children)b.setAttribute('aria-pressed',String(b.dataset.name===current.name))}}function schedule(){{clearTimeout(timer);if(playing&&capture.dataset.loaded==='true')timer=setTimeout(()=>show(1),100/Number(speed.value))}}capture.onload=()=>{{capture.dataset.loaded='true';schedule()}};capture.onerror=()=>{{playing=false;play.textContent='Play';detail.textContent='Capture unavailable: '+current.frames[index]}};category.onchange=populate;clip.onchange=choose;play.onclick=()=>{{playing=!playing;play.textContent=playing?'Pause':'Play';schedule()}};document.querySelector('#previous').onclick=()=>show(-1);document.querySelector('#next').onclick=()=>show(1);speed.onchange=schedule;for(const name of ['Daggers air attack 1','Daggers air attack 2','Daggers air attack 3','Mutilate ultimate','Greatsword King Domain ultimate','Greatsword Antares ultimate']){{const c=cases.find(x=>x.name===name);if(!c)continue;const b=document.createElement('button');b.type='button';b.textContent=name;b.dataset.name=name;b.onclick=()=>{{category.value=c.category;populate();clip.value=c.name;choose()}};featured.append(b)}}category.value=byCategory['Daggers']?'Daggers':Object.keys(byCategory)[0];populate();</script></body></html>'''
(S/'controller-review.html').write_text(html,encoding='utf-8')
(S/'review.html').write_text(html,encoding='utf-8')
manifest=dict(status='Complete',date='2026-10-24',runtime='chars/jinwoo',opponent='chars/naruto at corrected live scale',cases=len(cases),frames=sum(len(c['frames']) for c in cases),runtime_sha256=json.loads((S/f'validation/{feel}-runtime.json').read_text()),sources=list(runs),replacements=replace,note='Fresh movement and move recordings against test-controlled Naruto. Includes the proportioned dagger jump, three dagger air attacks, working close throw, responsive walk, four-hit light chain, and medium/heavy cancel routes.',recordings=cases)
(S/'validation/controller-review.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
missing=[f for c in cases for f in c['frames'] if not (S/f).exists()]
assert not missing,missing[:3]
print('JINWOO_CONTROLLER_REVIEW',len(cases),manifest['frames'],hashlib.sha256((S/'controller-review.html').read_bytes()).hexdigest())
