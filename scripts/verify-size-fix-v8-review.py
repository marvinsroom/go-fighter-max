"""Check actual asset playback and controls in Edge, without game recording."""
from pathlib import Path
from html import unescape
import json,re,subprocess,uuid,hashlib
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/size-fix-v8';temp=R/'.tmp/size-redesign/browser'/uuid.uuid4().hex;temp.mkdir(parents=True)
source=(O/'review.html').read_text(encoding='utf-8')
body=r'''
let checks=0;const check=(ok,label)=>{checks++;if(!ok)throw Error(label)};
const ready=im=>im.complete?Promise.resolve():new Promise((ok,bad)=>{im.onload=ok;im.onerror=()=>bad(Error('Missing '+im.src))});
check(data.fighters.length===23,'23 fighters');check(document.querySelectorAll('.card').length===23,'23 lineup cards');check(items.length===59,'59 body references');
for(let i=0;i<items.length;i++){
 document.querySelector('#actor').value=String(i);select();await ready(img(items[i].neutral.file));check(img(items[i].neutral.file).naturalWidth>0,'neutral '+i);
 await Promise.all(frames.map(f=>ready(img(f.file))));check(frames.every(f=>img(f.file).naturalWidth>0),'walk '+i);
 document.querySelector('#step').click();check(paused,'step pauses');document.querySelector('#pause').click();check(!paused,'resumes');
 const previous=flip;document.querySelector('#flip').click();check(flip!==previous,'facing toggles');document.querySelector('#flip').click();
}
check(document.documentElement.scrollWidth<=innerWidth+1,'no overflow');
return {status:'PASS',checks,viewport:innerWidth,fighters:data.fighters.length,body_references:items.length};
'''
harness='<pre id="size-qa">PENDING</pre><script>setTimeout(async()=>{try{const r=await(async()=>{'+body+'})();document.querySelector("#size-qa").textContent=JSON.stringify(r)}catch(e){document.querySelector("#size-qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},2000)</script>'
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');results=[]
for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=20000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=90,creationflags=0x08000000);match=re.search(r'<pre id="size-qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S)
 assert match,run.stderr.decode('utf-8',errors='replace')[-700:]
 result=json.loads(unescape(match[1]));assert result['status']=='PASS',result;result['view']=label;results.append(result)
report=dict(status='PASS',review_sha256=hashlib.sha256((O/'review.html').read_bytes()).hexdigest(),views=results);(O/'browser-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
