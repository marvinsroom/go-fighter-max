"""Build a local load-aware review from decoded native screenshots."""
from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
import numpy as np
from rimuru_source import ROOT,SOURCE

report=json.loads((SOURCE/'runtime-validation.json').read_text(encoding='utf-8'))
cases={}
for frame in report['frames']:
    path=SOURCE/'replays'/frame.get('capture_directory',report['capture_directory'])/frame['file']
    with Image.open(path) as im:im.verify()
    cases.setdefault(frame['case_name'],[]).append(dict(frame,src=str(path.relative_to(SOURCE)).replace('\\','/')))
for name,frames in cases.items():
    assert all(b['case_tick']>a['case_tick'] for a,b in zip(frames,frames[1:])),name
data=dict(cases=cases,revision=hashlib.sha256(json.dumps(report).encode()).hexdigest()[:12],passed=report['passed'],groups={'Intro and movement':[n for n in cases if n in ['Slime transformation intro','Idle','Walking','Jump']],'Attacks and magic':[n for n in cases if n not in ['Slime transformation intro','Idle','Walking','Jump'] and not n.startswith('Megiddo')],'Megiddo ultimate':[n for n in cases if n.startswith('Megiddo')]})
def category(name):
    if name.startswith('Megiddo'):return 'Megiddo ultimate'
    if 'Tempest Sever' in name or 'Predator Collapse' in name:return 'New supers'
    if any(s in name for s in ['Charge','transformation','Demon Lord','Slime','Return to']):return 'Charge and transformations'
    return 'Movement and magic'
data['groups']={group:[n for n in cases if category(n)==group] for group in ['Charge and transformations','New supers','Megiddo ultimate','Movement and magic']}
data['groups']['Charge and transformations'].sort(key=lambda n:(0 if n.startswith('Charge') else 1 if n=='Demon Lord transformation' else 2 if n=='Slime transformation' else 3 if n=='Return to masked human' else 4,n))
if (SOURCE/'forms-build.json').exists():
    forms=json.loads((SOURCE/'forms-build.json').read_text(encoding='utf-8'))
    ult_names=[m['name'] for m in forms['moves'] if m['offset']==90]
    super_names=[m['name'] for m in forms['moves'] if 60<=m['offset']<90]
    data['groups']={'Movement and form changes':[n for n in cases if ' / ' not in n],
                    'Slime moves':[n for n in cases if n.startswith('Slime /') and 'corner' not in n],
                    'Demon Lord moves':[n for n in cases if n.startswith('Demon Lord /') and 'corner' not in n],
                    'Masked human moves':[n for n in cases if n.startswith('Masked human /') and 'corner' not in n],
                    'Form ultimates':[n for n in cases if any(u in n for u in ult_names) and 'corner' not in n],
                    'Form supers':[n for n in cases if any(n==m['form_name']+' / '+m['name']+' hit' for m in forms['moves'] if m['name'] in super_names)],
                    'Corner framing':[n for n in cases if 'corner' in n]}
payload='window.RIMURU_REVIEW='+json.dumps(data).replace('</','<\\/')+';'
(SOURCE/'review-data.js').write_text(payload,encoding='utf-8')
template=(ROOT/'scripts/templates/cid-review.html').read_text(encoding='utf-8');css=re.search(r'<style>(.*?)</style>',template,re.S)[1]
script=template.split('const data=window.CID_REVIEW',1)[1].split('if(data){',1)[0]
script=('const data=window.RIMURU_REVIEW'+script).replace('cid-review','rimuru-review')
script+="if(data){document.getElementById('status').textContent=data.passed+' native checks passed. Frames play at recorded tick intervals.';for(const name of Object.keys(data.groups)){const option=document.createElement('option');option.value=name;option.textContent=name;category.append(option)}chooseCategory()}"
body='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rimuru Tempest - Combat review</title><style>CSS</style><main>
<div class="eyebrow">ILLUSTRATED FIGHTER</div><h1>Rimuru Tempest</h1><p class="intro">Masked Rimuru, with a slime-to-human transformation intro. Illustrated character drawings over SoulFire's original combat, voices and effects.</p>
<section><h2>Native game captures</h2><div class="toolbar"><select id="category" aria-label="Move category"></select><select id="clip" aria-label="Capture clip"></select><button id="previous">Previous frame</button><button id="play">Pause</button><button id="next">Next frame</button><select id="speed" aria-label="Playback speed"><option value="0.25">0.25x</option><option value="0.5">0.5x</option><option value="1" selected>1x</option></select></div><img id="capture" alt="Rimuru native game capture"><p id="detail"></p><p id="status"></p><a href="runtime-validation.json">Native test results</a> &middot; <a href="proportion-audit.html">All illustrated poses</a></section>
<section><h2>Controls</h2><table class="moves"><tr><th>Move</th><th>Player 1</th><th>Meter</th></tr><tr><td>Move / jump / crouch / block</td><td>Arrow keys / hold back to block</td><td>-</td></tr><tr><td>Katana attacks / magic</td><td>Z / X / C</td><td>C needs 250</td></tr><tr><td>Gluttony</td><td>Tap and release A</td><td>1000</td></tr><tr><td>Hell Flare</td><td>Tap and release S</td><td>1000</td></tr><tr><td>Black Lightning</td><td>Hold down, tap and release S</td><td>2000</td></tr><tr><td>Megiddo ultimate</td><td>Tap and release D; opening is unblockable and must connect</td><td>3000</td></tr><tr><td>Charge</td><td>Enter</td><td>Restores meter</td></tr></table><p>Original quarter-circle specials remain available: forward + Z = Gluttony, back + Z = Hell Flare, forward + X = Tempest Star Wolf, back + X = Black Flame, forward + C = Black Lightning, back + C = Time Stop.</p></section>
<section><h2>Animation artwork</h2><p><a href="art/illustrated-v1/README.md">Artwork and exact imagegen prompts</a></p><h3>Slime transformation</h3><img class="atlas" src="art/illustrated-v1/intro.png" alt="Eight transformation poses"><h3>Movement</h3><img class="atlas" src="art/illustrated-v1/movement.png" alt="Sixteen illustrated movement poses"><h3>Combat</h3><img class="atlas" src="art/illustrated-v1/combat.png" alt="Sixteen illustrated combat poses"></section>
<footer>Original MUGEN character by SoulFire / Diogo M. Source archive preserved. <a href="source/source-report.json">Source provenance</a> &middot; <a href="README.md">Build notes</a> &middot; <a href="../cid/review.html">Cid review</a> &middot; <a href="../jinwoo/review.html">Jinwoo review</a></footer></main><script src="review-data.js"></script><script>SCRIPT</script></html>'''.replace('CSS',css).replace('SCRIPT',script)
body=body.replace('opening is unblockable and must connect','opening must connect')
body=body.replace('Masked Rimuru, with a slime-to-human transformation intro. Illustrated character drawings over SoulFire\'s original combat, voices and effects.','Complete charge, three playable forms, illustrated Ranga, painted effects, two new supers and rebuilt Megiddo. Original combat and voices by SoulFire.')
body=body.replace('<section><h2>Controls</h2>','<section><h2>Controls</h2><p><kbd>W</kbd> cycles masked human &rarr; winged Demon Lord &rarr; slime &rarr; masked human. Hold <kbd>Enter</kbd> to charge; release to recover. Forward + A: <strong>Tempest Sever</strong> (1000 meter). Back + A: <strong>Predator Collapse</strong> (2000). Down + A: Black Flame (1500). Back + S: Ranga (1500). Forward + S: Time Stop (2000). Tap and release A/S for directional supers.</p>')
upgraded='<section><h2>Complete move artwork</h2><p><a href="art/complete-v2/README.md">New artwork and exact imagegen prompts</a></p>'
for name in ['forms','wings','effects','ranga']:upgraded+=f'<h3>{name.title()}</h3><img class="atlas" src="art/complete-v2/{name}.png" alt="Rimuru {name} artwork">'
if (SOURCE/'art/complete-v2/effects-v4.png').exists():
    upgraded=upgraded.replace('art/complete-v2/effects.png','art/complete-v2/effects-v4.png')
    upgraded+='<p><a href="art/complete-v2/effects-v4-prompts.json">Complete effect artwork and exact prompts</a></p>'
body=body.replace('<footer>',upgraded+'</section><footer>').replace('src="review-data.js"','src="review-data.js?v='+data['revision']+'"')
if (SOURCE/'forms-build.json').exists():
    css+='main,section{min-width:0;max-width:100%}main{max-width:1120px}.toolbar>*{min-width:0;max-width:100%}#clip{min-width:0;flex:1 1 260px}#capture{height:auto;max-width:100%}.ultimate-links{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}.ultimate-links button{flex:1 1 220px;text-align:left}.ultimate-links small{display:block;color:var(--muted)}.moves{table-layout:fixed;overflow-wrap:anywhere}@media(max-width:500px){.toolbar select{flex:1 1 100%}}'
    body=re.sub(r'<style>.*?</style>',lambda _:'<style>'+css+'</style>',body,count=1,flags=re.S)
    buttons='<nav id="ultimates" class="ultimate-links" aria-label="Form ultimates"></nav>'
    body=body.replace('<div class="toolbar"><select id="category"',buttons+'<div class="toolbar"><select id="category"',1)
    body=body.replace('<h2>Native game captures</h2>','<h2>Native game captures</h2><p>Choose a form ultimate below, or browse each form\'s moves. <kbd>W</kbd> changes form in game; <kbd>D</kbd> uses that form\'s ultimate at full meter.</p><p>Review build: v4 / '+data['revision']+'</p>')
    script+='''
const ultimateNav=document.getElementById('ultimates');
for(const name of data.groups['Form ultimates']){
 const button=document.createElement('button');button.type='button';
 button.textContent=name.replace(' hit','');button.setAttribute('aria-pressed','false');
 button.onclick=()=>{category.value='Form ultimates';chooseCategory();clip.value=name;index=0;show();for(const child of ultimateNav.children)child.setAttribute('aria-pressed',String(child===button))};
 ultimateNav.append(button);
}
ultimateNav.children[0].onclick();
'''
    body=re.sub(r'<script src="review-data.js[^\"]*"></script><script>.*?</script>',lambda _:'<script>'+payload+'</script><script>'+script+'</script>',body,count=1,flags=re.S)
    rows=[('Z / X / C','Light / medium / heavy in every form','Standing, crouching and airborne'),('A','Neutral signature','500 meter'),('Forward / back / down + A','Three directional signatures','500 meter each'),('S','Main form super','1000 meter'),('Back + S','Second form super','1500 meter'),('Forward + S','Third form super','2000 meter'),('D','Current form ultimate','3000 meter; opening must hit'),('W or down + S','Cycle masked human / Demon Lord / slime','Free'),('Hold Enter','Charge meter; release to recover','Caps at 3000')]
    guide='<section><h2>Controls and movesets</h2><p>Each form has <strong>17 attacks</strong>: nine standing/crouching/aerial normals, four signatures, three supers and its own ultimate. Controls follow the same pattern as Jinwoo: Z/X/C attacks, A signatures, S supers, D ultimate. Tap and release A/S/D. Directions are relative to the opponent.</p><table class="moves"><tr><th>Input</th><th>Action</th><th>Requirement</th></tr>'
    guide+=''.join('<tr>'+''.join('<td>'+s+'</td>' for s in row)+'</tr>' for row in rows)+'</table><h3>Form-specific attacks</h3><table class="moves"><tr><th>Form</th><th>A signatures</th><th>S supers</th><th>D ultimate</th></tr>'
    for form,name in enumerate(forms['forms']):
        entries=[m for m in forms['moves'] if m['form']==form]
        guide+='<tr><td>'+name+'</td><td>'+', '.join(m['name'] for m in entries if 30<=m['offset']<60)+'</td><td>'+', '.join(m['name'] for m in entries if 60<=m['offset']<90)+'</td><td>'+next(m['name'] for m in entries if m['offset']==90)+'</td></tr>'
    guide+='</table><p>Slime walking uses complete eight-pose artwork. Effects stay within the arena, and confirmed ultimates hold both fighters in view at their normal size.</p><p><a href="forms-build.json">Full move list</a> &middot; <a href="framing-validation.json">Native screen-bound checks</a></p></section>'
    body=re.sub(r'<section><h2>Controls</h2>.*?</section>',lambda _:guide,body,count=1,flags=re.S)
    body=body.replace('Complete charge, three playable forms, illustrated Ranga, painted effects, two new supers and rebuilt Megiddo. Original combat and voices by SoulFire.','Three complete movesets, three distinct ultimates, and repaired slime walking. Original character and voices by SoulFire.')
    art='<section><h2>Independent form artwork</h2><p><a href="art/forms-v3/README.md">New artwork and exact imagegen prompts</a></p>'
    for name in ['slime-walk','slime-combat','demon-combat','clean-casters']:art+=f'<h3>{name.replace("-"," ").title()}</h3><img class="atlas" src="art/forms-v3/{name}.png" alt="{name} sprite sheet">'
    body=body.replace('<footer>',art+'</section><footer>')
    if forms.get('cinematic_revision')==5:
        cinematic='<section><h2>Cinematic ultimates</h2><p>Megiddo forms celestial lenses before a rain of light and a star detonation. Draconic Storm summons a spectral dragon and lifts its victim into a finishing storm. Beelzebuth opens a devouring abyss, pulls the opponent inward, then closes into darkness and a shockwave.</p><p><a href="art/ultimates-v5/README.md">Ultimate artwork and prompts</a></p><img class="atlas" src="art/ultimates-v5/cinematics.png" alt="Light barrage, spectral dragon and devouring abyss artwork"><h3>Complete slime attacks</h3><img class="atlas" src="art/ultimates-v5/slime-combat.png" alt="Complete slime attack drawings"></section>'
        body=body.replace('<footer>',cinematic+'<footer>')
    showcase=[m for m in forms['moves'] if m['offset']==90]+[m for m in forms['moves'] if 60<=m['offset']<90]
    montage=Image.new('RGB',(1440,4*300),(10,10,17));draw=ImageDraw.Draw(montage)
    for i,move in enumerate(showcase):
        name=move['form_name']+' / '+move['name']+' hit'
        candidates=[f for f in cases[name] if f.get('fx_count',0)>0 and f['state']==move.get('confirmed',move['state'])]
        assert candidates,('No active effect capture',name)
        def visible_energy(frame):
            with Image.open(SOURCE/frame['src']) as image:
                pixels=np.array(image.convert('RGB'))[170:690]
            return int(((pixels[:,:,1]>150)&(pixels[:,:,2]>180)&(pixels[:,:,0]<140)).sum())
        f=max(candidates,key=visible_energy)
        with Image.open(SOURCE/f['src']) as native:
            thumbnail=native.convert('RGB').resize((480,270),Image.Resampling.LANCZOS)
        x=i%3*480;y=i//3*300;montage.paste(thumbnail,(x,y));draw.text((x+8,y+278),name.removesuffix(' hit'),fill='white')
    montage.save(SOURCE/'supers-ultimates-native-v4.png')
    body=body.replace('<section><h2>Controls and movesets</h2>','<section><h2>All three ultimates and nine supers</h2><a href="supers-ultimates-native-v4.png"><img class="atlas" src="supers-ultimates-native-v4.png" alt="Native captures of the three form ultimates and nine form supers"></a></section><section><h2>Controls and movesets</h2>')
(SOURCE/'review.html').write_text(body,encoding='utf-8')
(SOURCE/'review-forms-v3.html').write_text(body,encoding='utf-8')
(SOURCE/'review-forms-v4.html').write_text(body,encoding='utf-8')
audit='<html><meta charset="utf-8"><title>Rimuru proportion audit</title><style>'+css+'</style><main><h1>Rimuru proportions</h1><p>One fixed drawing scale per sheet. Crouching and lunging retain their natural height; no frame-by-frame bounding-box resizing. The slime intentionally grows during the intro.</p><p><a href="review.html">Native game review</a> &middot; <a href="build-report.json">Sprite scale and registration data</a></p>'
for name in ['movement','combat','intro']:audit+=f'<h2>{name.title()}</h2><img class="atlas" src="art/illustrated-v1/{name}.png">'
for name in ['forms','wings','effects','ranga']:audit+=f'<h2>{name.title()}</h2><img class="atlas" src="art/complete-v2/{name}.png">'
if (SOURCE/'art/complete-v2/effects-v4.png').exists():audit+='<h2>Complete effect drawings</h2><img class="atlas" src="art/complete-v2/effects-v4.png">'
if (SOURCE/'forms-build.json').exists():
    for name in ['slime-walk','slime-combat','demon-combat','clean-casters']:audit+=f'<h2>{name.title()}</h2><img class="atlas" src="art/forms-v3/{name}.png">'
(SOURCE/'proportion-audit.html').write_text(audit+'</main></html>',encoding='utf-8')
print('RIMURU_REVIEW',len(cases),'clips',sum(map(len,cases.values())),'decoded PNGs')
from fighter_review import write_review
write_review('rimuru',body,data)
