"""Verify candidate assets, playback controls and runtime preservation honestly."""
from pathlib import Path
from html import unescape
import json,re,subprocess,uuid,hashlib
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/comic-style-v10';temp=R/'.tmp/native-style-v10/browser'/uuid.uuid4().hex;temp.mkdir(parents=True)
progress=json.loads((O/'progress.json').read_text());assert progress['runtime_preservation']['status']=='PASS';expected=progress['sheets_ready'];source=(O/'review.html').read_text(encoding='utf-8')
body=r'''
let checks=0,poses=0;const check=(ok,label)=>{checks++;if(!ok)throw Error(label)};
const ready=im=>im.complete?(im.naturalWidth?Promise.resolve():Promise.reject(Error('Missing '+im.src))):new Promise((ok,bad)=>{im.onload=ok;im.onerror=()=>bad(Error('Missing '+im.src))});
check(data.length===EXPECTED,'saved sheet count');check(document.querySelectorAll('#sheet option').length===data.length,'all sheets selectable');
for(let i=0;i<data.length;i++){
 document.querySelector('#sheet').value=String(i);select();check(frame===0,'selection resets pose');
 for(const f of data[i].frames){await Promise.all([ready(img(f.before.file)),ready(img(f.after.file))]);check(img(f.before.file).naturalWidth>0,'source pose');check(img(f.after.file).naturalWidth>0,'candidate pose');poses++}
 document.querySelector('#step').click();check(!playing,'stepping pauses');document.querySelector('#pause').click();check(playing,'play starts');document.querySelector('#pause').click();check(!playing,'play stops');const old=flip;document.querySelector('#flip').click();check(flip!==old,'facing toggle');document.querySelector('#flip').click();
}
for(const im of document.querySelectorAll('img')){im.loading='eager';await ready(im);check(im.naturalWidth>0,'full sheet')}
check(document.documentElement.scrollWidth<=innerWidth+1,'no horizontal overflow');check(document.querySelector('.status').textContent.includes('Installed illustrated artwork'),'installed status explicit');
return{status:'PASS',checks,poses,sheets:data.length,viewport:innerWidth};
'''.replace('EXPECTED',str(expected))
harness='<pre id="qa">PENDING</pre><script>setTimeout(async()=>{try{let r=await(async()=>{'+body+'})();document.querySelector("#qa").textContent=JSON.stringify(r)}catch(e){document.querySelector("#qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},2000)</script>'
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');results=[]
for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=30000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=90,creationflags=0x08000000);match=re.search(r'<pre id="qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert match,run.stderr.decode('utf-8',errors='replace')[-700:]
 result=json.loads(unescape(match[1]));assert result['status']=='PASS',result;result['view']=label;results.append(result)
report=dict(status='PASS',scope='Installed illustrated artwork review',review_sha256=hashlib.sha256((O/'review.html').read_bytes()).hexdigest(),runtime_preservation=progress['runtime_preservation']['status'],views=results);(O/'browser-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
