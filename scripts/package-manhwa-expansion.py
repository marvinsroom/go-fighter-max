"""Publish the current roster entry page only after exact builds are verified."""
from manhwa_expansion import BATCH
from pathlib import Path
import json,html,re,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter'
cards=[];proof=[]
for slug,p in BATCH.items():
 folder=S/'characters'/slug;r=json.loads((folder/'runtime-validation.json').read_text());v=json.loads((folder/'viewer-validation.json').read_text());b=json.loads((folder/'build-report.json').read_text());startup=json.loads((folder/'startup-ai-validation.json').read_text())
 assert r['status']=='Complete' and r['passed']==66 and not r['failed'] and r['runtime_sha256']==b['runtime_sha256']
 assert v['status']=='PASS' and v['review_sha256']==hashlib.sha256((folder/'review.html').read_bytes()).hexdigest()
 assert startup['passed'] and startup['runtime_sha256']==b['runtime_sha256']
 proof.append(dict(slug=slug,name=p['name'],gameplay=r['passed'],browser=v['assertions'],clips=v['clips'],captures=len(r['frames']),review_sha256=v['review_sha256']))
 path='characters/'+slug+'/'
 cards.append('<article><a class="portrait" href="'+path+'review.html"><img src="'+path+'art/illustrated-v1/portrait.png" alt="'+p['name']+'"></a><div class="copy"><p class="series">'+html.escape(p['series'])+'</p><h2>'+p['name']+'</h2><p>'+html.escape(p['description'])+'</p><p class="ultimate">D · '+html.escape(p['moves'][-1])+'</p><a class="button" href="'+path+'review.html">Moves and previews</a> <a href="'+path+'art/illustrated-v1/design-review.html">Artwork</a></div></article>')
style='body{margin:0;background:#0e1521;color:#edf3ff;font:16px/1.6 system-ui}main{max-width:1400px;margin:auto;padding:40px 24px}h1{font-size:clamp(32px,5vw,58px);margin:0}h2{margin:0;font-size:26px}a{color:#a5d8ff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:24px;margin-top:32px}article{background:#182334;border:1px solid #2b3b52;border-radius:16px;overflow:hidden}.portrait{display:block;height:320px;background:radial-gradient(ellipse at bottom,#314360,#162031)}.portrait img{width:100%;height:100%;object-fit:contain;object-position:top}.copy{padding:24px}.series{font-size:13px;color:#aabbd1;margin:0}.ultimate{color:#e5cc8c}.button{display:inline-block;background:#a5d8ff;color:#101a29;padding:10px 14px;border-radius:7px;text-decoration:none;margin-right:12px}.controls{max-width:950px;color:#b8c8dc}footer{margin-top:36px;color:#aabbd1}'
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Manhwa Fighters</title><style>'+style+'</style></head><body><main><h1>Manhwa Fighters</h1><p>'+str(len(BATCH))+' fighters in the illustrated roster. <a href="face-audit/review.html">Comic face comparisons</a></p><p class="controls">Arrows move and guard. Z / X / C attack; Z Z Z, X X X and Z X C chain on contact. A and S use directional techniques, D unleashes the ultimate, Q evades, W performs a character gesture, and Enter charges power.</p><div class="grid">'+''.join(cards)+'</div><footer>Custom fan adaptations. Each artwork page includes official character sources, generated sheets and exact prompts. Hamel appears as Eugene’s past-life homage in his finisher. <a href="manhwa-expansion-validation.json">Build verification</a></footer></main></body></html>'
(S/'manhwa-roster.html').write_text(page,encoding='utf-8');(S/'manhwa-expansion-validation.json').write_text(json.dumps(dict(status='Complete',fighters=proof,total_gameplay=sum(p['gameplay'] for p in proof),total_browser=sum(p['browser'] for p in proof)),indent=2))
(S/'Review Manhwa Fighters.cmd').write_text('@echo off\nstart "" "%~dp0manhwa-roster.html"\n')
fornav='<a href="../../manhwa-roster.html">Manhwa fighters</a>'
for slug in ['baam','jin-mori','vikir','jin-mu-won','lloyd']:
 file=S/'characters'/slug/'review.html';text=file.read_text(encoding='utf-8')
 if '../../manhwa-roster.html' not in text:text=re.sub(r'(<nav class="character-nav"[^>]*>.*?)(</nav>)',lambda m:m[1]+fornav+m[2],text,count=1,flags=re.S)
 file.write_text(text,encoding='utf-8')
print('MANHWA_EXPANSION_PACKAGED',len(proof),'fighters',sum(p['gameplay'] for p in proof),'gameplay checks')
