"""Write local controls, art/motion reviews and a three-fighter hub."""
from pathlib import Path
import json
from importlib.machinery import SourceFileLoader
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'sprite-fighter/characters/prince/paired-build-report.json').exists():
    import runpy
    runpy.run_path(str(ROOT/'scripts/write-chappelle-pair-reviews.py'),run_name='__main__')
    raise SystemExit
builder=SourceFileLoader('chappelle_builder',str(ROOT/'scripts/build-chappelle-fighters.py')).load_module()
DESCRIPTIONS={
 'prince':'Regal basketball trickster: arcing basketball shots, sliding lows, a standing-strike counter, baseline side switches, enormous dunks and pancakes.',
 'negan':'Deliberate bat fighter: long swings, low boot checks, a whistle stance with follow-ups, a feint and a close command throw.',
 'rick':'Flamboyant slap-and-platform-boot fighter who transforms into Tyrone Biggums, a frantic rush fighter with separate specials and finishers.'}
DETAILS={
 'prince':'''| A / R | Check Ball stance |
| Z/X/C or F/G/H during stance | Royal Bounce / Baseline Cut / Royal Rejection |
| Toward + skill | Purple Slide low kick |
| Away + skill | Ruffle Counter: standing melee strikes only, active ticks 10-21 |
| Down + skill | Baseline Cut: visible side switch, no attack or invulnerability |
| Quarter-circle toward + attack | Three Royal Bounce strengths: 48 / 60 / 72 damage |
| Quarter-circle away + light / medium / heavy | Slide Feint / Purple Slide / Ruffle Counter |
| Forward, down, down-forward + heavy | Royal Rejection anti-air |
| Down, down + skill | Baseline Cut |''',
 'negan':'''| A / R | Whistle stance |
| Z/X/C or F/G/H during stance | Meet Lucille / Take a Knee / Back Off |
| Toward + skill | Take a Knee low kick |
| Away + skill | Swing and a Miss feint, no attack |
| Down + skill | Business Meeting close command grab |
| Quarter-circle toward + attack | Meet Lucille strengths: 72 / 100 / 125 damage |
| Quarter-circle away + light / medium / heavy | Feint / Take a Knee / Business Meeting |
| Forward, down, down-forward + heavy | Back Off anti-air |''',
 'rick':'''| W / ] | Toggle Rick James and Tyrone Biggums |
| A / R as Rick | Unity Slap |
| Toward / away / down + skill as Rick | Platform Rush / Couch Surf / Couch Crusher |
| Quarter-circle toward + attack as Rick | Cold Blooded strengths: 72 / 100 / 125 damage |
| Quarter-circle away + light or heavy as Rick | Couch Surf retreat |
| Quarter-circle away + medium as Rick | Platform Rush |
| Forward, down, down-forward + heavy as Rick | Funk Flash anti-air |
| A / R as Tyrone | Quick Rush |
| Toward / away / down + skill as Tyrone | Panic Lunge / Backpedal / Floor Scramble |
| Quarter-circle toward + light / medium / heavy as Tyrone | Quick Rush / Panic Lunge / Floor Scramble |
| Quarter-circle away + light or heavy as Tyrone | Backpedal |
| Quarter-circle away + medium as Tyrone | Floor Scramble |
| Forward, down, down-forward + heavy as Tyrone | Rising Flail |'''}
style='''*{box-sizing:border-box}body{background:#0c1120;color:#edf0ff;font:16px/1.6 system-ui;margin:0}main{max-width:1120px;padding:32px 24px;margin:auto}h1{font-size:clamp(32px,5vw,58px);line-height:1.15}h2{font-size:25px}p{color:#b8c8e6}a{color:#a4d2ff}.eyebrow{color:#d5a3ff;font-size:12px;letter-spacing:.14em;text-transform:uppercase}article{background:#141f36;border:1px solid #374566;border-radius:16px;padding:22px;margin:20px 0}img{max-width:100%;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}.status{color:#90e4bc}.links{display:flex;gap:20px;flex-wrap:wrap}canvas{width:100%;background:radial-gradient(ellipse at bottom,#344269,#11182b);border:1px solid #374566;border-radius:14px}button{background:#273655;color:#f0efff;border:1px solid #65749b;padding:8px 14px;border-radius:8px;margin:5px;cursor:pointer}.small{font-size:13px}code,kbd{color:#f9d37e}'''
hub=[]
for slug,cfg in builder.CONFIGS.items():
    source=ROOT/'sprite-fighter/characters'/slug;report=json.loads((source/'build-report.json').read_text())
    tests=source/'runtime-validation.json';native=json.loads(tests.read_text()) if tests.exists() else {}
    status=f"{native['passed']} native combat checks passed; {native['failed']} failed" if native.get('status')=='Complete' else 'Native validation in progress'
    label={'prince':'Prince','negan':'Negan','rick':'Rick James'}[slug]
    controls=f'''# {cfg['name']} - first playable

Launch **Play {label}.cmd** to control this fighter as Player 1 against inactive Will.
**Play Will vs {label}.cmd** puts the fighter on Player 2 for two-person play.
**Fight CPU {label}.cmd** puts basic fighter AI against Player 1 Will.

| Action | Player 1 | Player 2 |
|---|---|---|
| Move / jump / crouch | Arrows | I/J/K/L |
| Light / medium / heavy | Z/X/C | F/G/H |
| Skill | A | R |
| Super | S | T |
| Ultimate | D | Y |
| Throw | Q | [ |
| Back throw | Away + Q | Away + [ |
| Guard | Hold away or down-away | Hold away or down-away |

| Character input | Action |
|---|---|
{DETAILS[slug]}

Directions follow the opponent. Crouching and jumping change normal attacks.
Supers cost 1000 meter and deal 620 damage after a confirmed guardable starter.
Ultimates cost 2000 and deal 950. Their confirmed sequences last four/seven
seconds. A blocked or missed starter never begins the cinematic. Ultimate
starters are close range; these are intentionally exaggerated finishers.
Health is 1000 and maximum meter 3000. Launchers start full, with no timer.
F3 refills health/meter; Space resets positions/resources; Escape opens the menu.

'''
    if slug=='rick':controls+='Transformation is free, grounded, 42 ticks long, switches at tick 18 and has a 90-tick cooldown. It preserves health and meter. Tyrone has his own rush specials, Scramble City super and Midnight Mayhem ultimate. Press the same transform key to return to Rick. Basic attacks share timing/damage across forms.\n\n'
    else:controls+='No transformation is assigned to this roster slot. Stance follow-ups use the short visible window during ticks 8-26; stance and recovery remain vulnerable.\n\n'
    controls+='First pass uses nine key poses per look with shared attack drawings and a simple walk cycle. More animation, portraits, recorded voices, effects detail and competitive balance remain.\n'
    (source/'CONTROLS.md').write_text(controls)
    (source/'README.md').write_text(f'''# {cfg['name']}

{DESCRIPTIONS[slug]}

[Controls](CONTROLS.md) · [Visual/combat review](review.html) ·
[Native results](runtime-validation.json) · [Build report](build-report.json).

{status}. The companion verification.json records package hashes and embedded
PNG checks. Original built-in imagegen artwork and exact prompts are preserved
under art. Extraction crops cells without resampling or recoloring retained
pixels. Pose scales are consistent within each generated sheet.

Supers: {', '.join(cfg['supers'])}. Damage is 620 for supers and 950 for ultimates,
with 1000/2000 meter costs and guardable hit-confirm starters.

First playable uses key poses, shared drawings and code-native effects. More
authored in-betweens, portraits, voices and balance remain.

Builder: scripts/build-chappelle-fighters.py; shared core: scripts/chappelle_core.py.
Runtime is native IKEMEN CNS/AIR; Python only authors packages and review assets.
''')
    poses={k:dict(m,file='art/'+('tyrone-v1' if k.startswith('tyrone_') else 'v1')+'/'+k.removeprefix('tyrone_')+'.png') for k,m in report['sprites'].items() if not k.endswith('jump')}
    replay_names=['movement','special','super','ultimate']+(['transformation','tyrone-super','tyrone-ultimate','tyrone-reaction','tyrone-agent-capture'] if slug=='rick' else [])
    sections=''.join(f'<article><h2>{name.replace("-"," ").title()}</h2><img src="{name}-replay-v1.gif" alt="Actual engine replay: {name}"></article>' for name in replay_names)
    html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{cfg['name']} review</title><style>{style}</style><main>
<div class="eyebrow">Game1 · Chappelle roster · First playable</div><h1>{cfg['name']}</h1><p>{DESCRIPTIONS[slug]}</p><p class="status">{status}</p>
<div class="links"><a href="../chappelle/review.html">All Chappelle fighters</a><a href="CONTROLS.md">Controls</a><a href="runtime-validation.json">Combat checks</a><a href="verification.json">Package verification</a></div>
<h2>Gameplay-size poses</h2><canvas width="1000" height="470"></canvas><nav id="poses"></nav>
<p class="small">These drawings use the actual AIR scale and foot anchors. Replays below use real engine screenshots. First pass shares key poses; it is not a finished animation set.</p>
<article><h2>Finishers</h2><p>{cfg['supers'][0]}: 620 damage for 1000 meter. {cfg['supers'][1]}: 950 damage for 2000 meter. Four/seven-second confirmed sequences, guardable opening attacks, damage resolves once.</p></article>
{sections}<p class="small">Generated with built-in imagegen. <a href="art/{slug}-keyposes-v1.prompt.txt">Exact original prompt</a>. <a href="native-preview-report.json">Native replay provenance</a>. Artwork and source sheet retained under art.</p>
<script>const data={json.dumps(poses)},canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d'),images={{}};for(const[k,m]of Object.entries(data)){{const im=new Image;im.src=m.file;images[k]=im}}let keys=Object.keys(data),current=keys,begin=performance.now();const choices={{All:keys,Ready:['idle'],Walk:['walk_a','idle','walk_b','idle'],Attack:['idle','palm','kick','special'],Reaction:['hurt','down','crouch','idle']}};if(data.tyrone_idle)choices.Tyrone=keys.filter(k=>k.startsWith('tyrone_'));for(const[k,v]of Object.entries(choices)){{const b=document.createElement('button');b.textContent=k;b.onclick=()=>{{current=v;begin=performance.now()}};document.querySelector('nav').append(b)}}function draw(now){{ctx.clearRect(0,0,1000,470);ctx.strokeStyle='#617397';ctx.beginPath();ctx.moveTo(80,420);ctx.lineTo(920,420);ctx.stroke();const key=current[Math.floor((now-begin)/280)%current.length],m=data[key],im=images[key];if(im.complete)ctx.drawImage(im,500-m.axis[0]*m.scale,420-m.axis[1]*m.scale,im.width*m.scale,im.height*m.scale);ctx.fillStyle='#e2e8ff';ctx.font='16px system-ui';ctx.fillText(key.replaceAll('_',' '),24,36);requestAnimationFrame(draw)}}requestAnimationFrame(draw)</script></main></html>'''
    (source/'review.html').write_text(html)
    hub.append(f'<article><h2>{label}</h2><img src="../{slug}/engine-preview.png" alt="{label} in the actual game"><p>{DESCRIPTIONS[slug]}</p><p class="status">{status}</p><a href="../{slug}/review.html">Review moves and replays</a> · <a href="../{slug}/CONTROLS.md">Controls</a></article>')
H=ROOT/'sprite-fighter/characters/chappelle';H.mkdir(exist_ok=True)
(H/'review.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dave Chappelle fighters</title><style>{style}</style><main><div class="eyebrow">Game1 · New roster fighters</div><h1>One comedian. Four looks.</h1><p>Three separate fighters: Prince, Negan, and Rick James. Rick transforms into Tyrone Biggums with W as Player 1 or ] as Player 2, then uses the same key to return.</p><p>Use the Play Prince, Play Negan or Play Rick James shortcuts in sprite-fighter. Player 1 uses arrows, Z/X/C attacks, A skill, S super, D ultimate and Q throw. All start with full health/meter and no timer.</p><div class="grid">{''.join(hub)}</div><p>First playable artwork uses key poses. More animation, effects detail, portraits and competitive balance remain.</p><p class="small"><a href="capture-compatibility.json">Victim reaction compatibility fix</a>: incoming captures select the victim's own form-aware art. <a href="verification.json">Combined verification</a>.</p></main></html>''')
print('CHAPPELLE_REVIEWS_WRITTEN')
