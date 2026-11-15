"""Publish original MUGEN imports after native control and startup checks pass."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,re,hashlib,html,shutil
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';E=S/'engine/ikemen-go-v1.0.0'
CONTROLS={
'naruto':'''Arrows move, crouch, jump and guard. Z/X/C are the original a/b/c attacks; A/S/D are the original x/y/z buttons. Hold Enter to charge power and the separate chakra bar.

Hold S for Sage Mode. A enters KCM1 with at least 500 chakra; Down+A enters KCM2 with at least 900. In KCM1/KCM2, S calls the Kurama avatar and costs 1500 power. D enters four-tail mode with at least 300 chakra; Down+D enters six-tail mode with at least 900. Down+S selects the source's Ashura form with at least 900 chakra. Down+Enter returns chakra forms to base; Sage Mode uses its original timed helper.

Quarter-circle forward + Z: Rasengan (1000 power). Quarter-circle back + Z: shadow shuriken. Quarter-circle forward + X: shadow clones. Quarter-circle back + X: clone charge. Quarter-circle forward + C: clone barrage. Quarter-circle back + C: Rasenshuriken. Techniques vary with the active form. Down+C uses the form-specific super.

These are the imported creator controls. The supplied Zz-MOVESET.txt describes the Ashura-specific techniques; the controls above also document the verified base and transformation routes.''',
'saitama':'''Arrows move, crouch, jump and guard. Z/X/C are the original a/b/c buttons; A/S/D are the original x/y/z buttons. Enter performs the original taunt. Double-tap a direction to run or hop back.

Quarter-circle forward + D: Serious Punch. Quarter-circle forward + S: Consecutive Normal Punches. Quarter-circle forward + A: Death Punch counter. Quarter-circle forward + Z: Serious Table Flip. Quarter-circle forward + X: Serious Headbutt. Quarter-circle forward + C: Serious Sidehops. Quarter-circle back + D: Meteor Punch.

Back+D summons Genos; Back+C summons Tatsumaki; Back+S calls King; Back+X calls Silver Fang. Down, Down + A/S teleports forward; Down, Down + Z/X teleports backward. See the original Movelist.txt for the remaining moves.

The original author intentionally makes Saitama unable to die. Holding Enter allows him to be hit; releasing it restores his life. This source behavior is retained. Serious Punch has a long cinematic; let it finish.'''}
NAMES={'naruto':'Naruto Shippuden','saitama':'Saitama'}
STYLE='''*{box-sizing:border-box}body{margin:0;background:#111824;color:#eef4ff;font:17px/1.6 system-ui}main{max-width:1300px;margin:auto;padding:24px}a{color:#b6d9ff}img{max-width:100%;height:auto;display:block}article,section{background:#202c3c;padding:20px;border-radius:12px;margin:24px 0}select,button{font:inherit;margin:5px;padding:8px;max-width:100%}.capture{width:100%;background:#273342}.controls{white-space:pre-wrap}h1{line-height:1.2}'''
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
results=[]
for slug in ('naruto','saitama'):
 f=S/'characters'/slug;manifest=json.loads((f/'import-report.json').read_text());native=json.loads((f/'runtime-validation.json').read_text());startup=json.loads((f/'startup-validation.json').read_text())
 assert native['status']=='Complete' and native['failed']==0 and startup['status']=='Complete' and startup['passed']
 current={name:sha(E/'chars'/slug/name) for name in manifest['source_files_sha256']};assert current==manifest['source_files_sha256']==native['runtime_sha256']==startup['runtime_sha256']
 groups={}
 groups['Natural entrance and AI combat']=[dict(v,src='replays/'+startup['capture_directory']+'/'+v['file']) for v in startup['frames']]
 for v in native['frames']:groups.setdefault(v['case_name'],[]).append(dict(v,src='replays/'+native['capture_directory']+'/'+v['file']))
 selected=[]
 wanted=['Base normal attack','Sage normal attack','KCM1 normal attack','KCM2 normal attack','Kurama avatar transformation','Ashura normal attack'] if slug=='naruto' else ['Walk forward','Jump','Normal punch','Consecutive normal punches','Serious punch','Serious table flip']
 for label in wanted:
  frames=groups[label];wanted_tick={'Serious punch':600,'Serious table flip':90,'Jump':30}.get(label)
  chosen=next((v for v in frames if v.get('case_tick')==wanted_tick),frames[min(2,len(frames)-1)]);selected.append((label,chosen))
 board=Image.new('RGB',(1280,385*3),'#18202c');draw=ImageDraw.Draw(board)
 for i,(label,v) in enumerate(selected):
  im=Image.open(f/v['src']).convert('RGB');im.thumbnail((640,360));x=i%2*640;y=i//2*385;board.paste(im,(x,y+25));draw.text((x+8,y+5),label,fill='white')
 board.save(f/'import-native-contact.jpg',quality=92)
 data=json.dumps(groups);page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+NAMES[slug]+' original MUGEN import</title><style>'+STYLE+'</style></head><body><main><a href="../../anime-imports.html">Anime imports</a><h1>'+NAMES[slug]+' — original MUGEN import</h1><p>Imported from '+html.escape(manifest['creator'])+'. Original MUGEN artwork, voices, animations, moves and transformation logic are retained. No illustrated replacement has been applied.</p><p>'+str(native['passed'])+' native control checks passed, plus natural entrance and AI combat. <a href="runtime-validation.json">Control proof</a> | <a href="startup-validation.json">Startup proof</a> | <a href="import-report.json">Original-file hashes and credits</a> | <a href="'+html.escape(manifest['source']['listing'])+'">Release source</a></p><section><h2>Controls</h2><div class="controls">'+html.escape(CONTROLS[slug])+'</div></section><section><h2>Native engine recordings</h2><label for="clip">Move or form</label> <select id="clip"></select><div><button id="previous">Previous frame</button><button id="play">Play</button><button id="next">Next frame</button><label for="speed">Playback</label><select id="speed"><option value="500">Slow</option><option value="250" selected>Normal</option><option value="100">Fast</option></select></div><p id="caption"></p><img id="capture" class="capture" alt="Actual native engine capture"></section><section><h2>Forms and signature moves</h2><img src="import-native-contact.jpg" alt="Original MUGEN fighter in the native engine"></section><p>Player 1 controls above. Player 2 uses I/J/K/L, F/G/H and R/T/Y, with Right Shift for Start. Launch with Play '+NAMES[slug]+'.cmd or Fight '+NAMES[slug]+' CPU.cmd.</p></main><script>const groups='+data+''';const clip=document.getElementById('clip'),capture=document.getElementById('capture'),caption=document.getElementById('caption');let index=0,timer=null;for(const name of Object.keys(groups)){const o=document.createElement('option');o.value=name;o.textContent=name;clip.append(o)}function frames(){return groups[clip.value]}function render(){const v=frames()[index];capture.src=v.src;caption.textContent=clip.value+' · frame '+(index+1)+'/'+frames().length+' · state '+v.state}clip.onchange=()=>{index=0;render()};document.getElementById('next').onclick=()=>{index=(index+1)%frames().length;render()};document.getElementById('previous').onclick=()=>{index=(index+frames().length-1)%frames().length;render()};function stop(){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}function start(){timer=setInterval(()=>document.getElementById('next').click(),Number(document.getElementById('speed').value));document.getElementById('play').textContent='Pause'}document.getElementById('play').onclick=()=>timer?stop():start();document.getElementById('speed').onchange=()=>{if(timer){stop();start()}};render();</script></body></html>'''
 (f/'review.html').write_text(page,encoding='utf-8');(f/'CONTROLS.md').write_text('# '+NAMES[slug]+'\n\n'+CONTROLS[slug]+'\n',encoding='utf-8');(f/'README.md').write_text('# '+NAMES[slug]+' MUGEN import\n\nOriginal creator: '+manifest['creator']+'.\n\n[Native review](review.html) | [Controls](CONTROLS.md) | [Source and hashes](import-report.json).\n\nOriginal archives and original data are preserved under source/. No reskin or gameplay rebalance.\n',encoding='utf-8')
 for label,mode in [('Play','Play'),('Fight','CPU')]:
  filename=label+' '+NAMES[slug]+(' CPU' if mode=='CPU' else '')+'.cmd';(S/filename).write_text('@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-anime-mugen.ps1" -Character '+slug+' -Mode '+mode+'\n')
 (S/('Review '+NAMES[slug]+'.cmd')).write_text('@echo off\nstart "" "%~dp0characters\\'+slug+'\\review.html"\n')
 manifest.update(status='Native verified original MUGEN import',native_control_checks=native['passed'],native_startup=True,current_runtime_sha256=current);(f/'import-report.json').write_text(json.dumps(manifest,indent=2));results.append(dict(slug=slug,name=NAMES[slug],creator=manifest['creator'],checks=native['passed'],captures=len(native['frames'])+len(startup['frames'])))
 # Keep the original byte-identical selection aliases reproducible.
 assert sha(E/'chars'/slug/(slug+'.def'))==manifest['definition_alias_sha256']
cards=''.join('<article><h2>'+v['name']+'</h2><p>'+html.escape(v['creator'])+' · '+str(v['checks'])+' native control checks and natural AI startup passed.</p><a href="characters/'+v['slug']+'/review.html"><img src="characters/'+v['slug']+'/import-native-contact.jpg" alt="'+v['name']+' native captures">Open controls, forms and recordings</a></article>' for v in results)
(S/'anime-imports.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Original anime MUGEN imports</title><style>'+STYLE+'</style><main><h1>Anime fighters: original MUGEN imports</h1><p>Saitama and Naruto Shippuden are imported and tested with their original artwork and moves. Naruto includes Sage Mode and Kurama forms. Saitama retains the creator’s intentionally unkillable behavior. These imports precede any artwork upgrade.</p>'+cards+'<p><a href="anime-import-queue.json">Saved request queue</a> | <a href="face-audit/style-v4-review.html">Comic character review</a></p></main></html>',encoding='utf-8')
(S/'anime-import-validation.json').write_text(json.dumps(dict(status='Native verified; browser and roster registration pending',fighters=results),indent=2));print('ANIME_IMPORTS_PACKAGED',results)
