"""Validate the narrow timing change and every preview cycle."""
from pathlib import Path
from html import unescape
import json,re,hashlib,subprocess,uuid
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'walk-fix-v11';report=json.loads((O/'installation.json').read_text());checks=0
frame=re.compile(rb'(?m)^[ \t]*\d+[ \t]*,[ \t]*\d+[ \t]*,[^\r\n]*')
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk)
 return h.hexdigest()
def mask(data):return frame.sub(lambda m:b','.join(m[0].split(b',')[:4]+[b'TIME']+m[0].split(b',')[5:]),data)
for row in report['files']:
 old=(O/'before/chars'/row['engine']/row['air']).read_bytes();live=E/'chars'/row['engine'];new=(live/row['air']).read_bytes();assert mask(old)==mask(new),row['slug'];assert digest(live/row['sff'])==row['sff_sha256'];checks+=2
 before={int(m[1]):m[0] for m in re.finditer(rb'(?im)^\s*\[Begin Action\s+(\d+)\][\s\S]*?(?=^\s*\[Begin Action|\Z)',old)}
 after={int(m[1]):m[0] for m in re.finditer(rb'(?im)^\s*\[Begin Action\s+(\d+)\][\s\S]*?(?=^\s*\[Begin Action|\Z)',new)}
 changed={r['action'] for r in row['actions']};assert before.keys()==after.keys()
 for number in before:
  if number not in changed:assert before[number]==after[number],(row['slug'],number)
 checks+=1
for slug in ['lloyd','baam','jin_mori']:
 p=O/'validation'/(slug+'.json');native=json.loads(p.read_text());assert native['status']=='PASS' and native['passed'] and not native['recording'];checks+=1
temp=R/'.tmp/walk-v11-browser'/uuid.uuid4().hex;temp.mkdir(parents=True);source=(O/'review.html').read_text(encoding='utf-8')
harness='''<pre id="qa">PENDING</pre><script>setTimeout(async()=>{try{
 let checks=0,poses=0;const check=(ok,msg)=>{checks++;if(!ok)throw Error(msg)};
 const ready=im=>im.complete?(im.naturalWidth?Promise.resolve():Promise.reject(Error(im.src))):new Promise((ok,bad)=>{im.onload=ok;im.onerror=()=>bad(Error(im.src))});
 check(data.items.length===51,'every body/form cycle');
 for(let i=0;i<data.items.length;i++){
  document.querySelector('#actor').value=String(i);select();check(elapsed===0,'reset phase');
  for(const direction of ['forward','backward']){
   document.querySelector('#direction').value=direction;select();const pair=chosen();
   check(pair.after.reduce((n,f)=>n+f.ticks,0)===(direction==='forward'?40:48),'native loop duration');
   for(const f of pair.after){await ready(img(f.file));check(img(f.file).naturalWidth>0,'native pose decoded');poses++}
  }
 }
 document.querySelector('#pause').click();check(paused,'pause');document.querySelector('#pause').click();check(!paused,'play');document.querySelector('#step').click();check(paused,'step pauses');let prior=flip;document.querySelector('#flip').click();check(flip!==prior,'facing toggle');
 check(document.documentElement.scrollWidth<=innerWidth+1,'no horizontal overflow');check(document.querySelector('.note').textContent.includes('Complete'),'completed artwork disclosed');
 document.querySelector('#qa').textContent=JSON.stringify({status:'PASS',checks,poses,cycles:data.items.length});
 }catch(e){document.querySelector('#qa').textContent=JSON.stringify({status:'FAIL',error:String(e)})}},1000)</script>'''
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');views=[]
for width,height,name in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/name),f'--window-size={width},{height}','--virtual-time-budget=20000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=60,creationflags=0x08000000);m=re.search(r'<pre id="qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert m,run.stderr[-500:];result=json.loads(unescape(m[1]));assert result['status']=='PASS',result;result['view']=name;views.append(result)
result=dict(status='PASS',scope='Timing, pace, sprite preservation, non-walk action preservation, native forward/back displacement, corrected Lloyd alternating-leg artwork and full browser pose loading',static_native_checks=checks,browser=views,recordings=False,artwork_pending=False)
(O/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
