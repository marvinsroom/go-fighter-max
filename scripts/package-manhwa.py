"""Publish exact native evidence, controls, art, launchers and credits."""
from manhwa_fighters import *
from fighter_review import write_review,NAMES,INTROS
from PIL import Image,ImageDraw
import sys,hashlib
p=profile(sys.argv[1]);S=p['folder'];art=S/'art/illustrated-v1'
r=json.loads((S/'runtime-validation.json').read_text());b=json.loads((S/'build-report.json').read_text())
assert r['status']=='Complete' and not r['failed'] and r['runtime_sha256']==b['runtime_sha256']
cases={}
for f in r['frames']:
    path=S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']
    with Image.open(path) as im:im.verify()
    cases.setdefault(f['case_name'],[]).append(dict(f,src=path.relative_to(S).as_posix()))
groups={k:[] for k in ['Ultimates','Entrance and personality','Combos','Supers','Techniques','Basics and movement']}
for name in cases:
    group='Ultimates' if p['moves'][-1] in name or 'ultimate' in name.lower() else 'Entrance and personality' if name in ('Entrance',p['taunt']) else 'Combos' if any(tag in name for tag in ('Z Z Z','X X X','Z X C','Chain','chain')) else 'Supers' if any(label in name for label in p['moves'][4:7]) else 'Techniques' if any(label in name for label in p['moves'][:4]) else 'Basics and movement'
    groups[group].append(name)
data=dict(passed=r['passed'],cases=cases,groups={k:v for k,v in groups.items() if v},revision=hashlib.sha256(json.dumps(r).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.'+p['id'].upper()+'_REVIEW='+json.dumps(data)+';')
style='<style>body{max-width:1250px;margin:35px auto;padding:20px;background:#111925;color:#edf2f8;font:17px/1.6 system-ui}img{max-width:100%;background:#253143}a{color:#9cdbff}section{margin:30px 0}</style>'
page='<!doctype html><html lang="en"><meta charset="utf-8"><title>'+p['name']+' artwork</title>'+style+'<a href="../../review.html">Back to native combat review</a><h1>'+p['name']+'</h1><p>Custom illustrated adaptation. Character references guided the likeness and outfit. Built-in imagegen created the body poses, effects and portrait; exact prompts and original sheets are retained. W performs the character personality action.</p><p><a href="'+p['source']+'">Official series</a> | <a href="generation-requests.json">Generation requests</a></p>'
if (art/'native-ultimate-preview.png').exists():page+='<img src="native-ultimate-preview.png" alt="Native engine ultimate stages">'
for slug in ['movement','combat','story','effects','portrait']:page+=f'<section><h2>{slug}</h2><a href="{slug}.prompt.txt">Exact prompt</a><img src="{slug}.png" alt="{p["name"]} {slug}"></section>'
(art/'design-review.html').write_text(page+'</html>',encoding='utf-8')
(art/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen.imagegen',source=p['source'],requests='generation-requests.json',assets={slug:dict(file=slug+'.png',prompt=slug+'.prompt.txt',sha256=hashlib.sha256((art/(slug+'.png')).read_bytes()).hexdigest()) for slug in ['movement','combat','story','effects','portrait']}),indent=2))
scale=Image.new('RGB',(1800,530),(30,43,60));pen=ImageDraw.Draw(scale)
for j,(label,slug,index) in enumerate([('Movement neutral','movement',0),('Combat neutral','combat',0),('Cinematic neutral','story',4)]):
    im=Image.open(art/'poses'/f'{slug}-{index}.png').convert('RGBA');assert im.height==424
    scale.paste(im,(j*600+(600-im.width)//2,60),im);pen.text((j*600+15,15),label+' /424px',fill='white');pen.line((j*600,484,j*600+599,484),fill=(130,170,190))
scale.save(art/'scale-comparison.png')
(S/'proportion-audit.html').write_text('<!doctype html><meta charset="utf-8"><title>'+p['name']+' scale</title>'+style+'<a href="review.html">Combat review</a><h1>Consistent body registration</h1><img src="art/illustrated-v1/scale-comparison.png" alt="Movement, combat and cinematic neutral scale comparison"><p>Neutral body banks register at424px with AIR scale0.125 and192x144 coordinates. Crouches, lunges and jumps preserve their anatomical scale.</p><a href="pose-registration.json">Pose registrations</a>',encoding='utf-8')
rows='<tr><td>Z / X / C</td><td>Light / medium / heavy, with crouch and air variants</td><td>Free</td></tr><tr><td>Z Z Z / X X X / Z X C</td><td>Buffered contact chains</td><td>Free</td></tr>'
for key,move in zip(['A','Forward + A','Back + A','Down + A','S','Back + S','Forward + S','D'],p['movespec']):rows+=f'<tr><td>{key}</td><td>{move[4]}</td><td>{move[3]}</td></tr>'
rows+=f'<tr><td>W</td><td>{p["taunt"]}</td><td>Free</td></tr><tr><td>Q</td><td>Evade</td><td>Free</td></tr><tr><td>Hold Enter</td><td>Charge power</td><td>Free</td></tr>'
(S/'CONTROLS.md').write_text('# '+p['name']+' controls\n\nArrows move, crouch and jump; hold back to guard. Double-tap forward/back to dash.\n\n| Input | Action | Meter |\n|---|---|---|\n| Z / X / C | Light / medium / heavy; crouch and air variants | Free |\n| Z Z Z / X X X / Z X C | Contact combo chains | Free |\n'+''.join('| '+key+' | '+move[4]+' | '+str(move[3])+' |\n' for key,move in zip(['A','Forward + A','Back + A','Down + A','S','Back + S','Forward + S','D'],p['movespec']))+'| W | '+p['taunt']+' | Free |\n| Q | Evade | Free |\n| Hold Enter | Charge power | Free |\n\nEnter follow-ups as strikes connect. Whiffs cannot chain. Confirmed standing normals can cancel into skills or ultimate. The ultimate starter is guardable; only a confirmed hit starts the cinematic.\n',encoding='utf-8')
content='<section><h2>Controls</h2><p>Arrows move, crouch and jump. Hold back to guard; double-tap forward or back to dash. Tap combo follow-ups as a strike connects. Missed starters cannot chain. A confirmed standing normal can cancel into a skill or ultimate.</p><table><thead><tr><th>Key</th><th>Move</th><th>Meter</th></tr></thead><tbody>'+rows+'</tbody></table></section><section><h2>'+p['moves'][-1]+'</h2><p>The 3000-meter opener is guardable. Only a confirmed hit starts the 164-tick staged finisher, for '+str(p['ultimate'])+' total damage. Both fighters stay in front of the effects, and the attack makes room near the facing edge to keep the victim visible. Blocks and misses recover without forced capture.</p></section><section><h2>Character and artwork</h2><p>'+p['description']+' This is custom fan gameplay based on '+p['series']+', credited to '+p['credits']+'. No third-party MUGEN release is claimed. One illustrated appearance; W is '+p['taunt']+'.</p><p><a href="art/illustrated-v1/design-review.html">Artwork and exact prompts</a> | <a href="source/source-report.json">Sources and foundation</a></p></section>'
content+='<section><h2>Comic likeness</h2><p><a href="../../face-audit/review.html">Compare the comic face with the current portrait and body artwork</a>.</p></section>'
(ROOT/'scripts/templates'/(p['slug']+'-review-content.html')).write_text(content,encoding='utf-8')
for slug,other in PROFILES.items():
    if slug==p['slug'] or (ROOT/'sprite-fighter/characters'/slug/'review.html').exists():NAMES[slug]=other['name'];INTROS[slug]=other['description']
(S/'README.md').write_text('# '+p['name']+'\n\nCustom illustrated '+p['series']+' fan adaptation. Credits: '+p['credits']+'. Official source: '+p['source']+'\n\n'+p['description']+'\n\nControls: arrows move/guard; Z/X/C normals; ZZZ,XXX,ZXC contact chains; A/S directional techniques; D ultimate at 3000 meter; W '+p['taunt']+'; Q evade; Enter charge. One playable appearance; W performs a personality action.\n\nCompiled '+str(b['body_drawings'])+' unique body drawings into 48 registered body entries, 16 VFX and 2 portrait slots. Movement victory slot uses a full-body neutral to exclude possible cropped atlas art. Neutral body height 424 px at AIR scale 0.125 in 192x144 coordinates. Some animation frames share illustrated key poses. Source originals, prompts and provenance are in art/illustrated-v1/.\n\nCurrent build: '+str(r['passed'])+' passing native checks; '+str(len(cases))+' clips; '+str(len(r['frames']))+' captures. Runtime hashes are in build-report.json and runtime-validation.json. Source foundation is preserved under source/.\n\nBuild: scripts/build-manhwa-fighter.py '+p['slug']+'; test setup: scripts/setup-manhwa-tests.py '+p['slug']+' <fresh-directory>; launcher: scripts/run-manhwa-fighter.ps1 -Character '+p['slug']+' -Mode Tests -Wait (-RealTime for presentation). Package: scripts/package-manhwa.py '+p['slug']+'.\n',encoding='utf-8')
write_review(p['slug'],data=data)
for label,mode in [('Play','Play'),('Fight','CPU')]:
    file=ROOT/'sprite-fighter'/(label+' '+p['name']+(' CPU' if label=='Fight' else '')+'.cmd')
    file.write_text('@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-manhwa-fighter.ps1" -Character '+p['slug']+' -Mode '+mode+'\n')
(ROOT/'sprite-fighter'/('Review '+p['name']+'.cmd')).write_text('@echo off\nstart "" "%~dp0characters\\'+p['slug']+'\\review.html"\n')
print('MANHWA_PACKAGED',p['name'],len(cases),'clips',len(r['frames']),'captures')
