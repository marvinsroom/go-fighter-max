"""Replace Jinwoo review.html while preserving the established review format."""
from pathlib import Path
import json,re,shutil,hashlib

R=Path(__file__).resolve().parents[1]; S=R/'sprite-fighter/characters/jinwoo'
page=S/'review.html'; archive=S/'archive/before-controller-review'; archive.mkdir(parents=True,exist_ok=True)
if not (archive/'review.html').exists():shutil.copy2(page,archive/'review.html')
html=(archive/'review.html').read_text(encoding='utf-8')
manifest=json.loads((S/'validation/controller-review.json').read_text(encoding='utf-8'))

cases={}; groups={'Ultimates':[],'Supers':[],'Human skills':[],'Shadows':[],'Weapons & movement':[]}
for row in manifest['recordings']:
 source_name=row['name']; name=source_name.replace('â€”','—').replace('â€“','–').replace('â†”','↔'); low=name.lower()
 cases[name]=[{'src':src,'case_tick':i*12+24} for i,src in enumerate(row['frames'])]
 if any(x in low for x in ('ultimate','mutilate','king domain','antares')):group='Ultimates'
 elif 'super' in low:group='Supers'
 elif any(x in name for x in ('Skill','QCF','QCB','Down +')):group='Human skills'
 elif any(x in low for x in ('igris','beru','iron','tank','shadow','assist','signature')):group='Shadows'
 else:group='Weapons & movement'
 groups[group].append(name)
groups={k:v for k,v in groups.items() if v}
short=[]
for name in groups.get('Ultimates',[]):
 if any(x in name.lower() for x in ('mutilate','king domain','antares','ultimate hit')):short.append({'category':'Ultimates','clip':name})
data={'revision':hashlib.sha256(json.dumps(cases).encode()).hexdigest()[:12],'passed':manifest['cases'],'introPassed':0,'cases':cases,'groups':groups,'slug':'jinwoo','name':'Sung Jinwoo','shortcuts':short[:12],'sheets':[],'status':f"{manifest['cases']} newly recorded live move/control cases · {manifest['frames']} frames · Xbox and keyboard guide updated.",'pageRevision':'controller-review-20261024'}

html=re.sub(r'<title>.*?</title>','<title>Sung Jinwoo - Complete move and controller review</title>',html,count=1,flags=re.S)
html=re.sub(r'<body>.*?<main>', '<body><main>',html,count=1,flags=re.S)
html=re.sub(r'<header>.*?</header>', '<header><div class="eyebrow">FIGHTER / COMPLETE MOVE REVIEW</div><h1>Sung Jinwoo vs Naruto</h1><p class="intro">Fresh live-runtime recordings against corrected-scale Naruto for both weapons, the close throw, every human skill, four playable shadows, assists, supers and ultimates — with Xbox and keyboard controls.</p></header>',html,count=1,flags=re.S)
html=html.replace('Choose an ultimate below, or browse supers, movement and other recorded moves. Pause or slow playback to inspect individual frames.',f"Browse {manifest['cases']} newly recorded move and control cases against Naruto. Pause, step, or slow playback to inspect every sequence.")
controls='''<section aria-labelledby="controls"><h2 id="controls">Xbox and keyboard controls</h2><p>Player 1 controls. Directions are relative to the opponent. The Play Jinwoo launcher starts the controller bridge for D-pad, right-stick and stick-click shortcuts.</p><div class="table-wrap"><table class="moves"><thead><tr><th>Action</th><th>Xbox controller</th><th>Keyboard</th></tr></thead><tbody>
<tr><td>Move / crouch / jump</td><td><kbd>Left stick</kbd></td><td>Arrow keys</td></tr><tr><td>Light / medium / grab / heavy</td><td><kbd>A</kbd> / <kbd>B</kbd> / <kbd>X</kbd> / <kbd>Y</kbd></td><td><kbd>Z</kbd> / <kbd>X</kbd> / <kbd>A</kbd> / <kbd>C</kbd></td></tr>
<tr><td>Charge</td><td>Hold <kbd>LB</kbd></td><td>Hold <kbd>Enter</kbd></td></tr><tr><td>Summon Igris / Beru / Iron / Tank</td><td><kbd>LT</kbd> / toward+LT / away+LT / down+LT</td><td><kbd>W</kbd> with the same directions</td></tr>
<tr><td>Transform Igris / Beru / Iron / Tank</td><td>D-pad Up / Right / Left / Down</td><td><kbd>Q+F</kbd> / <kbd>Q+G</kbd> / <kbd>Q+H</kbd> / <kbd>Q+R</kbd></td></tr><tr><td>Super / ultimate</td><td><kbd>RT</kbd> / <kbd>RB</kbd></td><td><kbd>S</kbd> / <kbd>D</kbd></td></tr>
<tr><td>Switch daggers / greatsword</td><td>Right stick Down</td><td>Down + <kbd>S</kbd></td></tr><tr><td>Mutilate / King Domain</td><td>Right stick Up</td><td><kbd>Q+Y</kbd></td></tr><tr><td>Monarch Domain</td><td>Right stick Left</td><td><kbd>W+Y</kbd></td></tr><tr><td>Spoiler Skill</td><td>Right stick Right</td><td><kbd>W+T</kbd></td></tr><tr><td>Skill 11 / Skill 12</td><td><kbd>R3</kbd> / <kbd>L3</kbd></td><td><kbd>Q+W</kbd> / <kbd>Q+T</kbd></td></tr>
<tr><td>Skills 1–6</td><td>QCF/QCB + A, B, or RT</td><td>QCF/QCB + Z, X, or S</td></tr><tr><td>Skills 7–9</td><td>Down + A, B, or RT</td><td>Down + Z, X, or S</td></tr><tr><td>Guard high / low</td><td>Away / down-away</td><td>Away / down-away</td></tr></tbody></table></div><p class="note">QCF means down, down-forward, forward. QCB means down, down-back, back. <a href="CONTROLS.md">Detailed control notes</a>.</p></section>'''
html=re.sub(r'<section aria-labelledby="controls">.*?</section>',controls,html,count=1,flags=re.S)
html=html.replace('Earlier native recordings below predate this size correction.','The native recordings below are current as of October 24, 2026.')
html=html.replace('Earlier move recordings are preserved; fresh recordings are deferred while fixes continue.','Jinwoo now has fresh move recordings against corrected-scale Naruto.')
replacement='<script>window.FIGHTER_REVIEW=window.JINWOO_REVIEW='+json.dumps(data,separators=(',',':')).replace('</','<\\/')+';</script>'
html=re.sub(r'<script>window\.FIGHTER_REVIEW=.*?</script>',lambda _m:replacement,html,count=1,flags=re.S)
html=html.replace('validation/current.json">Native validation','validation/controller-review.json">Recording manifest')
html=html.replace('Review build: d6194d61e1bf','Review build: controller-review-20261024')
page.write_text(html,encoding='utf-8')
print('JINWOO_REVIEW_REPLACED',len(cases),sum(len(v) for v in cases.values()),data['revision'])
