"""Exercise the generated review's actual controls in headless Edge."""
from baam_model import *
from html import unescape
import re,subprocess

T=ROOT/'.tmp/baam-browser';T.mkdir(parents=True,exist_ok=True)
body='''let assertions=0;const check=(v,n)=>{assertions++;if(!v)throw Error(n)};if(playing)play.click();let count=0;for(const [g,names] of Object.entries(data.groups)){category.value=g;category.onchange();check(clip.options.length===names.length,'category');for(const n of names){clip.value=n;clip.onchange();check(index===0,'clip reset');document.getElementById('next').click();check(index===1%frames().length,'next');document.getElementById('previous').click();check(index===0,'previous');check(capture.getAttribute('src').includes(frames()[0].src),'capture');count++}}for(const button of ultimateNav.children){button.click();check(clip.value===button.dataset.clip,'ultimate shortcut')}document.getElementById('speed').value='0.25';document.getElementById('speed').onchange();await new Promise(r=>setTimeout(r,250));check(capture.naturalWidth>0,'native capture loads');play.click();check(playing,'play');play.click();check(!playing,'pause');return {status:'PASS',assertions,clips:count};'''
page=(S/'review.html').read_text(encoding='utf-8').replace('<head>','<head><base href="'+S.as_uri()+'/">',1)
harness='<pre id="test-results">PENDING</pre><script>setTimeout(async()=>{try{const result=await(async()=>{'+body+'})();document.getElementById("test-results").textContent=JSON.stringify(result)}catch(e){document.getElementById("test-results").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},1000)</script>'
p=T/'review.html';p.write_text(page+harness,encoding='utf-8')
run=subprocess.run(['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files',f'--user-data-dir={T/"profile"}','--dump-dom','--virtual-time-budget=5000',p.as_uri()],capture_output=True,timeout=45,creationflags=0x08000000)
out=run.stdout.decode('utf-8',errors='replace');m=re.search(r'<pre id="test-results">(.*?)</pre>',out,re.S)
assert m,run.stderr.decode('utf-8',errors='replace')[-1200:]
value=json.loads(unescape(m[1]));assert value['status']=='PASS',value
value['review_sha256']=__import__('hashlib').sha256((S/'review.html').read_bytes()).hexdigest()
(S/'viewer-validation.json').write_text(json.dumps(value,indent=2))
print('BAAM_REVIEW_VERIFIED',value)
