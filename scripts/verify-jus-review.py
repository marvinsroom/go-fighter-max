"""Exercise the generated roster and every installed form player in real Edge."""
from pathlib import Path
from html import unescape
import subprocess,re,json,hashlib,uuid
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade'
p=O/'review.html';source=p.read_text(encoding='utf-8')
temp=R/'.tmp/jus-review-browser'/uuid.uuid4().hex;temp.mkdir(parents=True,exist_ok=True)
body=r'''
let checks=0;const check=(v,n)=>{checks++;if(!v)throw Error(n)};
const ready=im=>im.complete?Promise.resolve():new Promise((ok,bad)=>{im.onload=ok;im.onerror=()=>bad(Error('Missing image '+im.src))});
check(document.querySelectorAll('.fighter').length===28,'all 28 fighters');
check(document.querySelector('#fighterSelect').options.length===28,'fighter selection');
check(document.querySelector('#walkSelect').options.length===data.walk_cycles.length,'all installed cycles selectable');
for(const c of document.querySelectorAll('.fighter canvas'))check(c.getContext('2d').getImageData(0,0,c.width,c.height).data.some((v,i)=>i%4===3&&v>0),'lineup drawing');
for(let i=0;i<data.walk_cycles.length;i++){
 document.querySelector('#walkSelect').value=String(i);await loadWalk();await Promise.all(frames.map(ready));
 check(frames.length===8&&frames.every(im=>im.naturalWidth>0),'cycle '+i+' images');
 document.querySelector('#step').click();check(paused&&document.querySelector('#pause').textContent==='Play','step pauses');
 document.querySelector('#pause').click();check(!paused,'resume');
}
for(const row of rows){
 document.querySelector('#fighterSelect').value=row.slug;
 for(const suite of ['native','native-combat','native-forms']){
  document.querySelector('#suite').value=suite;capture=0;showProof();
  if(row[suite]){await ready(document.querySelector('#native'));check(document.querySelector('#native').naturalWidth>0,'native '+row.slug+' '+suite);document.querySelector('#next').click();document.querySelector('#prev').click();check(capture===0,'capture navigation')}
  else check(document.querySelector('#proof').textContent==='Current report pending','honest pending evidence');
 }
}
check(document.documentElement.scrollWidth<=innerWidth+1,'no horizontal overflow');
return {status:'PASS',checks,viewport:innerWidth,cycles:data.walk_cycles.length};
'''
harness='<pre id="jus-qa">PENDING</pre><script>setTimeout(async()=>{try{const result=await(async()=>{'+body+'})();document.querySelector("#jus-qa").textContent=JSON.stringify(result)}catch(e){document.querySelector("#jus-qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},2000)</script>'
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8')
reports=[]
for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=20000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=90,creationflags=0x08000000)
 m=re.search(r'<pre id="jus-qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S)
 assert m,run.stderr.decode('utf-8',errors='replace')[-1000:]
 proof=json.loads(unescape(m[1]));assert proof['status']=='PASS',proof
 proof['view']=label;reports.append(proof)
report=dict(status='PASS',review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),views=reports)
(O/'browser-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
