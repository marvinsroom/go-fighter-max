"""Exercise before/after sprite playback and all sheets without recording."""
from pathlib import Path
from html import unescape
import json,re,subprocess,uuid,hashlib
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/proportions-v9';temp=R/'.tmp/proportions-browser'/uuid.uuid4().hex;temp.mkdir(parents=True)
source=(O/'review.html').read_text(encoding='utf-8')
body=r'''
let checks=0;const check=(ok,label)=>{checks++;if(!ok)throw Error(label)};
const ready=im=>im.complete?(im.naturalWidth?Promise.resolve():Promise.reject(Error('Missing '+im.src))):new Promise((ok,bad)=>{im.onload=ok;im.onerror=()=>bad(Error('Missing '+im.src))});
check(data.length===3,'three body variants');
for(const a of data)for(const v of ['before','after']){check(a[v].length===9,'standing plus eight walk drawings');for(const f of a[v]){await ready(image(f.file));check(image(f.file).naturalWidth>0,'sprite '+f.file)}}
for(const im of document.querySelectorAll('img')){im.loading='eager';await ready(im);check(im.naturalWidth>0,'sheet '+im.src)}
document.querySelector('#step').click();check(paused,'step pauses');check(frame>=0&&frame<8,'valid frame');document.querySelector('#pause').click();check(!paused,'resumes');
document.querySelector('#flip').click();check(flip,'facing flips');document.querySelector('#mode').value='stand';check(document.querySelector('#mode').value==='stand','standing mode');
check(document.documentElement.scrollWidth<=innerWidth+1,'no overflow');return{status:'PASS',checks,viewport:innerWidth};
'''
harness='<pre id="qa">PENDING</pre><script>setTimeout(async()=>{try{let r=await(async()=>{'+body+'})();document.querySelector("#qa").textContent=JSON.stringify(r)}catch(e){document.querySelector("#qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},2000)</script>'
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');results=[]
for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=20000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=90,creationflags=0x08000000);match=re.search(r'<pre id="qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert match,run.stderr.decode('utf-8',errors='replace')[-700:]
 result=json.loads(unescape(match[1]));assert result['status']=='PASS',result;result['view']=label;results.append(result)
report=dict(status='PASS',review_sha256=hashlib.sha256((O/'review.html').read_bytes()).hexdigest(),views=results);(O/'browser-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
