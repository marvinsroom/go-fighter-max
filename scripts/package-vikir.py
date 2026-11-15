"""Publish native clips and a transparent sprite player for the original fighter."""
from pathlib import Path
import json,hashlib,html,re
from PIL import Image,ImageDraw
import fighter_review
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/vikir'
b=json.loads((S/'build-report.json').read_text(encoding='utf-8'))
r=json.loads((S/'runtime-validation.json').read_text(encoding='utf-8'))
art=Path(b['poses']['m0']['file']).parent.parent.relative_to(S.relative_to(R)).as_posix()
assert r['status']=='Complete' and r['failed']==0
assert r['runtime_sha256']==b['runtime_sha256']
cases={}
for f in r['frames']:
    path='replays/'+f.get('capture_directory',r['capture_directory'])+'/'+f['file']
    assert (S/path).exists(),path
    cases.setdefault(f['case_name'],[]).append(dict(f,src=path))
assert cases
groups={}
for title in ['Vikir','Night Hound','Choco']:
    rows=[n for n in cases if n.startswith(title+' / ') or n.startswith(title+' ')]
    # Vikir is a prefix of just its own form, not the other forms.
    groups[title]=rows
others=[n for n in cases if not any(n in rows for rows in groups.values())]
ultimates=[n for n in cases if 'Crimson Execution' in n]
supers=[n for n in cases if any(move in n for move in ('Three Fangs','Beelzebub Blood Draw','Sword Aura','Seven Fangs')) and n not in ultimates]
guests=[n for n in cases if '/ Guest ' in n or n.startswith('Guest ')]
archery=[n for n in cases if 'Anubis' in n]
featured=set(ultimates+supers+guests+archery)
if 'Academy' in b['forms']:
    academy=[n for n in others if n.startswith('Academy')]
    groups['Academy']=academy;others=[n for n in others if n not in academy]
groups={'Ultimates':ultimates,'Supers':supers,'Guests':guests,'Archery':archery,**{k:[n for n in rows if n not in featured] for k,rows in groups.items()},'Power and intro':[n for n in others if n not in featured]}
data=dict(passed=r['passed'],cases=cases,groups=groups,revision=hashlib.sha256(json.dumps(r).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.VIKIR_REVIEW='+json.dumps(data)+';',encoding='utf-8')
# Display every drawing at runtime scale, registered to its actual foot root.
timelines=json.loads((S/'animation-data.js').read_text(encoding='utf-8').split('=',1)[1].removesuffix(';'))
used={f['key'] for clip in timelines.values() for f in clip['frames']}
poses=[(k,v) for k,v in b['poses'].items() if v['group'] in range(70,74) or (k in used and v['group'] in range(50,58))]
canvas=Image.new('RGB',(1800,((len(poses)+5)//6)*300),(19,21,29));d=ImageDraw.Draw(canvas)
for i,(key,m) in enumerate(poses):
    im=Image.open(R/m['file']).convert('RGBA');sc=m['scale']*.49
    im=im.resize((max(1,round(im.width*sc)),max(1,round(im.height*sc))),Image.Resampling.LANCZOS)
    x=i%6*300+150-round(m['axis'][0]*sc);y=i//6*300+260-round(m['axis'][1]*sc)
    canvas.paste(im,(x,y),im);d.text((i%6*300+12,i//6*300+280),key+' / '+m['bank'],fill='white')
canvas.save(S/'proportions.jpg',quality=92)
css='body{margin:32px auto;max-width:1200px;background:#11151d;color:#eee;font:17px system-ui;padding:0 20px}a{color:#ff9e9e}img{max-width:100%}button,select{padding:10px;background:#242d39;color:white;border:1px solid #566}canvas{max-width:100%;background:repeating-linear-gradient(0deg,#1a2231,#1a2231 39px,#303c4d 40px)}'
(S/'proportion-audit.html').write_text('<!doctype html><meta charset="utf-8"><title>Vikir body registration</title><style>'+css+'</style><a href="review.html">Combat review</a><h1>Body registration</h1><p>The comic redraw preserves each previous pose?s visible height and foot registration. Weapon reach does not set body scale. Standing recoveries reuse the neutral body. Choco retains its separate small body and hurtbox.</p><img src="proportions.jpg" alt="Vikir, Night Hound, Choco, Academy, Anubis and guest drawings at runtime scale">',encoding='utf-8')
# AIR timeline data comes directly from the compiled drawing metadata/timings.
anim=(S/'animation-data.js').read_text(encoding='utf-8')
player='''const all=window.VIKIR_ANIMATION,sel=document.querySelector('select'),cv=document.querySelector('canvas'),ctx=cv.getContext('2d');let timer=null,idx=0,playing=true;const images={};for(const [key,clip] of Object.entries(all)){if(![0,20,21,40,41,43,190,200,210,220,400,410,420,600,610,620,500,700,710,800,1000,1100,1200,1300,1400,2000,2010,2020,2030,3000,3100,4000,4500,4510].includes(Number(key)%10000))continue;const o=document.createElement('option');o.value=key;o.textContent=['Vikir','Night Hound','Choco','Academy'][clip.form]+' / '+clip.name;sel.append(o)}function draw(){clearTimeout(timer);const rows=all[sel.value].frames,f=rows[idx];const src=f.file.replaceAll('\\\\','/').split('characters/vikir/')[1];let im=images[src];if(!im){im=images[src]=new Image();im.onload=draw;im.src=src;return}if(!im.complete)return;ctx.clearRect(0,0,1000,560);ctx.strokeStyle='#637188';ctx.beginPath();ctx.moveTo(0,480);ctx.lineTo(1000,480);ctx.stroke();ctx.drawImage(im,420-f.axis[0]*f.scale,480-f.axis[1]*f.scale,im.width*f.scale,im.height*f.scale);document.querySelector('#pose').textContent=f.key+' | drawing '+(idx+1)+' / '+rows.length+' | '+f.ticks+' ticks';if(playing)timer=setTimeout(()=>{idx=(idx+1)%rows.length;draw()},f.ticks<0?500:Math.max(16,f.ticks*1000/60))}sel.onchange=()=>{idx=0;draw()};document.querySelector('#play').onclick=e=>{playing=!playing;e.target.textContent=playing?'Pause':'Play';draw()};document.querySelector('#next').onclick=()=>{playing=false;document.querySelector('#play').textContent='Play';idx=(idx+1)%all[sel.value].frames.length;draw()};draw();'''
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vikir animation artwork</title><style>'+css+'</style><a href="review.html">Native combat review</a><h1>Vikir animation artwork</h1><p>Original key-pose animation. Playback uses the installed AIR timings, scale and foot registration. Native gameplay is in the combat review.</p><select aria-label="Animation"></select> <button id="play">Pause</button> <button id="next">Next drawing</button><p id="pose"></p><canvas width="1000" height="560" aria-label="Vikir sprite preview"></canvas><script>'+anim+player+'</script><h2>Original atlases and exact prompts</h2>'
for name in ['movement','combat','night-movement','night-combat-v2','choco','portrait','power','night-power','school-movement','school-combat','school-power']:
    bank=art if (S/art/(name+'.png')).exists() else 'art/v1'
    if not (S/bank/(name+'.png')).exists():continue
    page+=f'<p><a href="{bank}/{name}.prompt.txt">{html.escape(name)} exact generation prompt</a></p><img src="{bank}/{name}.png" alt="{html.escape(name)} original artwork">'
page+=f'<p><a href="{art}/provenance.json">Artwork hashes and provenance</a> · <a href="DESIGN.md">Design and source references</a></p></html>'
page=page.removesuffix('</html>')+'<h2>Guests and Academy Anubis artwork</h2>'
for name in ['dolores','camu','aiyen','sinclair','anubis','effects']:
    page+=f'<p><a href="art/guests-v1/{name}.prompt.txt">{name} exact generation prompt</a></p><img src="art/guests-v1/{name}.png" alt="{name} original sprite atlas">'
page+='<h2>Crimson Execution and colored arrows</h2><p><a href="art/presentation-v4/effects.prompt.txt">Exact effects prompt</a> | <a href="anatomy-calibration.json">Per-pose anatomy calibration</a></p><img src="art/presentation-v4/effects.png" alt="Animated crimson and emerald arrows, fang cuts and execution impacts">'
page+='<p><a href="art/guests-v1/provenance.json">Guest artwork hashes and provenance</a></p></html>'
(S/'animation-review.html').write_text(page,encoding='utf-8')
(S/'README.md').write_text((S/'DESIGN.md').read_text(encoding='utf-8')+'\n\nBuild: `tooling/mesh-client-venv/Scripts/python.exe scripts/build-vikir.py`. Validation: `powershell -ExecutionPolicy Bypass -File scripts/validate-vikir.ps1`. Native results and runtime hashes are in runtime-validation.json.\n',encoding='utf-8')
fighter_review.NAMES['vikir']='Vikir van Baskerville'
fighter_review.INTROS['vikir']='Hunter, Night Hound, Choco and the Colosseo academy uniform. Three sword supers, the cinematic Crimson Execution ultimate, four guest assists and animated Academy Anubis archery.'
content='''<section><h2>Controls</h2><p>Arrows move, crouch and jump. Hold away from the opponent to guard. Press attack keys to activate moves. Hold a direction before pressing for a directional skill.</p><table><tr><th>Key</th><th>Action</th><th>Power</th></tr><tr><td>Z / X / C</td><td>Light / medium / heavy; standing, crouching and air variants</td><td>Free</td></tr><tr><td>A</td><td>Hound Lunge</td><td>250</td></tr><tr><td>Down+A</td><td>Rising Hunt</td><td>500</td></tr><tr><td>Back+A</td><td>Silent Retreat</td><td>Free</td></tr><tr><td>S</td><td>Three Fangs</td><td>1000</td></tr><tr><td>Back+S</td><td>Beelzebub Blood Draw; heal on a confirmed hit</td><td>1500</td></tr><tr><td>Down+S</td><td>Sword Aura; 10-second mastery boost</td><td>1000</td></tr><tr><td>S+D together</td><td>Seven Fangs super</td><td>2000</td></tr><tr><td>D</td><td>Night Hound: Crimson Execution; confirm the opening dash to unleash the cinematic finisher</td><td>3000</td></tr><tr><td>Q / Down+Q</td><td>Cycle Hunter / Night Hound / Choco / Academy; down+Q restores Hunter</td><td>Free</td></tr><tr><td>W / Hold Enter</td><td>Quickstep / charge power (release Enter to stop; automatically stops at full power)</td><td>Free</td></tr><tr><td>Forward+A (Academy)</td><td>Anubis crimson arrow; four animated energy frames</td><td>Free</td></tr><tr><td>Forward+S</td><td>Dolores: heal 120 life</td><td>1250</td></tr><tr><td>Forward+D</td><td>Camu: fire bolt</td><td>1250</td></tr><tr><td>Back+D</td><td>Aiyen: three emerald wind arrows</td><td>1000</td></tr><tr><td>Down+D</td><td>Sinclair: mana lance</td><td>1250</td></tr></table><p>Guests share a six-second cooldown. Calls can be interrupted; healing caps at maximum life. Guest attacks and Anubis arrows travel across the arena and can be guarded.</p></section><section><h2>Manhwa appearances</h2><p>Hunter Vikir, the masked Night Hound disguise, Choco, and the Colosseo academy uniform with glasses. Choco has a small hurtbox; sword attacks restore the human body. Night Hound shares Vikir’s sword moves. Sword Aura represents mastery as a timed game power-up.</p><p><a href="proportion-audit.html">Body size audit</a> | <a href="animation-review.html">Animation and original artwork player</a> · <a href="DESIGN.md">Design decisions and sources</a></p><p>New key-pose artwork and authored combat; no imported MUGEN model. Damage, timing and move choreography are fan game adaptations. No novel-only forms.</p></section><footer>Vikir from <a href="https://tapas.io/series/revenge-of-the-baskerville-bloodhound/info">Revenge of the Baskerville Bloodhound</a>, by Step on a LEGO, S.arang and TO WALK / REDICE STUDIO. Original sprite art generated with imagegen; procedural game audio, no character voice imitation.</footer>'''
(fighter_review.TEMPLATES/'vikir-review-content.html').write_text(content,encoding='utf-8')
fighter_review.write_review('vikir',data=data)
print('VIKIR_REVIEW',len(cases),'native clips;',len(r['frames']),'frames')
