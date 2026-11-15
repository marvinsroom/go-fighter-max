"""Validate source readiness and browser rendering, without recording gameplay."""
from pathlib import Path
import json,re,hashlib,subprocess,uuid,html,urllib.parse
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';O=G/'style-wave2';E=G/'engine/ikemen-go-v1.0.0'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk)
 return h.hexdigest()
d=json.loads((O/'queue.json').read_text());checks=0
for row in d['targets']:
 slug=row['slug'];inventory=json.loads((O/row['inventory']).read_text());v=json.loads((G/'mugen-expansion/validation'/(slug+'.json')).read_text())
 assert v['status']=='PASS' and v['active_round_ticks']>=180 and v['identity_matches'],slug
 assert not inventory['runtime_art_modified'] and not inventory['height_applied']
 for key,digest in inventory['source_sha256'].items():assert sha(E/'chars'/slug/inventory['files'][key])==digest,(slug,key)
 assert inventory['sprites'] and inventory['actions']
 checks+=7
for ref in re.findall(r'(?:src|href)="([^"]+)"',(O/'review.html').read_text(encoding='utf-8')):
 ref=html.unescape(ref)
 if ref.startswith(('http:','https:','data:','#')):continue
 path=(O/urllib.parse.unquote(ref)).resolve();assert path.is_relative_to(R) and path.exists(),ref;checks+=1
snapshot=json.loads((G/'mugen-expansion/existing-roster-before-wave2-sha256.json').read_text());preserved_files=0
for slug,files in snapshot.items():
 for name,digest in files.items():assert sha(E/'chars'/slug/name)==digest,(slug,name);preserved_files+=1
print('Preserved',len(snapshot),'existing fighters;',preserved_files,'files',flush=True)
temp=R/'.tmp/style-wave2-browser'/uuid.uuid4().hex;temp.mkdir(parents=True)
body=(O/'review.html').read_text(encoding='utf-8');harness='''<pre id="qa">PENDING</pre><script>
setTimeout(async()=>{try{
 let checks=0;const check=(ok,msg)=>{checks++;if(!ok)throw Error(msg)};
 check(document.querySelectorAll('article').length===11,'eleven fighters');
 for(const im of document.images){
  await new Promise((ok,bad)=>{if(im.complete)return im.naturalWidth?ok():bad(Error(im.src));im.onload=ok;im.onerror=()=>bad(Error(im.src))});
  check(im.naturalWidth>0,'source image loaded');
 }
 check(document.documentElement.scrollWidth<=innerWidth+1,'no overflow');
 check(document.body.textContent.includes('new artwork has not been generated'),'honest pending status');
 document.querySelector('#qa').textContent=JSON.stringify({status:'PASS',checks,source_images:document.images.length});
}catch(e){document.querySelector('#qa').textContent=JSON.stringify({status:'FAIL',error:String(e)})}},1000)</script>'''
test=temp/'review.html';test.write_text(body.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');views=[]
for width,height,name in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/name),f'--window-size={width},{height}','--virtual-time-budget=10000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=45,creationflags=0x08000000);m=re.search(r'<pre id="qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert m,run.stderr[-500:];result=json.loads(html.unescape(m[1]));assert result['status']=='PASS',result;result['view']=name;views.append(result)
report=dict(status='PASS',fighters=11,new_imports=10,existing_kenpachi_reused=True,source_inventory=d['inventory_totals'],native_identity_and_active_round='11/11 PASS',local_checks=checks,existing_fighters_preserved=len(snapshot),existing_files_preserved=preserved_files,browser=views,new_art_generated=False,runtime_art_modified=False,recordings=False,scope='Imports verified and source/reference briefs prepared; style conversion incomplete until image generation is available; exhaustive move/form playthrough pending')
(O/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
