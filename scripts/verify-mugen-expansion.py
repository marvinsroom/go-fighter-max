"""Verify registered imports, local review links and browser image loading."""
from pathlib import Path
from html import unescape
import json,re,subprocess,uuid,hashlib,urllib.parse
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';O=G/'mugen-expansion';E=G/'engine/ikemen-go-v1.0.0'
d=json.loads((O/'queue.json').read_text());ready=[r for r in d['fighters'] if r.get('review')];checks=0
for p in [O/'review.html']+[G/r['review'] for r in ready]:
 text=p.read_text(encoding='utf-8')
 for ref in re.findall(r'(?:src|href)="([^"]+)"',text):
  ref=unescape(ref)
  if ref.startswith(('http:','https:','#','data:')):continue
  target=(p.parent/urllib.parse.unquote(ref.split('#')[0].split('?')[0])).resolve()
  assert target.is_relative_to(R) and target.exists(),(p,ref);checks+=1
for r in ready:
 v=json.loads((O/'validation'/(r['slug']+'.json')).read_text(encoding='utf-8-sig'));assert v['status']=='PASS'
 select=(E/'data/select.def').read_text();assert re.search(r'(?im)^'+re.escape(r['slug'])+r'\s*,',select)
 report=json.loads((G/'characters'/r['slug']/'import-report.json').read_text())
 for name,digest in report['source_files_sha256'].items():
  compatibility=report.get('native_compatibility',{}).get(name)
  if compatibility:assert hashlib.sha256((G/'characters'/r['slug']/compatibility['original_retained']).read_bytes()).hexdigest()==digest
  assert hashlib.sha256((E/'chars'/r['slug']/name).read_bytes()).hexdigest()==(compatibility['installed_sha256'] if compatibility else digest)
 checks+=1
yuji=json.loads((O/'validation/yuji-sukuna.json').read_text());assert yuji['passed'] and not yuji['recording'];checks+=1
temp=R/'.tmp/mugen-expansion-browser'/uuid.uuid4().hex;temp.mkdir(parents=True);body=(O/'review.html').read_text(encoding='utf-8');expected=len(ready)
harness='''<pre id="qa">PENDING</pre><script>setTimeout(async()=>{try{
 let count=0;const check=(ok,msg)=>{count++;if(!ok)throw Error(msg)};
 check(document.querySelectorAll('article').length===EXPECTED,'all imports listed');
 for(const im of document.querySelectorAll('img')){await new Promise((ok,bad)=>{if(im.complete)return im.naturalWidth?ok():bad(Error(im.src));im.onload=ok;im.onerror=()=>bad(Error(im.src))});check(im.naturalWidth>0,'portrait decoded')}
 check(document.documentElement.scrollWidth<=innerWidth+1,'no horizontal overflow');
 check(document.body.textContent.includes('styling')||document.body.textContent.includes('Styling'),'import phase shown');
 document.querySelector('#qa').textContent=JSON.stringify({status:'PASS',checks:count,portraits:document.images.length});
 }catch(e){document.querySelector('#qa').textContent=JSON.stringify({status:'FAIL',error:String(e)})}},1000)</script>'''.replace('EXPECTED',str(expected))
test=temp/'review.html';test.write_text(body.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');views=[]
for width,height,name in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/name),f'--window-size={width},{height}','--virtual-time-budget=15000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=45,creationflags=0x08000000);m=re.search(r'<pre id="qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert m,run.stderr[-500:];result=json.loads(unescape(m[1]));assert result['status']=='PASS',result;result['view']=name;views.append(result)
report=dict(status='PASS',imports=len(ready),requested=d['requested'],main_roster_count=d['main_roster_count'],local_checks=checks,browser=views,original_source_files_preserved=True,yuji_sukuna=yuji,recordings=False,scope='Original source hashes, DEF dependencies (publish audit), startup reports, registration, review links and browser portraits; exhaustive moves/form audit pending')
(O/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
