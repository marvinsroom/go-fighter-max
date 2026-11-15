"""Load the current roster in Edge at desktop and phone widths."""
from pathlib import Path
from manhwa_expansion import BATCH
import subprocess,json,re,html
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter';T=ROOT/'.tmp/manhwa-hub-browser';T.mkdir(parents=True,exist_ok=True)
page=(S/'manhwa-roster.html').read_text(encoding='utf-8').replace('<head>','<head><base href="'+S.as_uri()+'/">',1)
test='''<pre id="qa-result">PENDING</pre><script>setTimeout(()=>{try{let n=0;const check=(ok,label)=>{n++;if(!ok)throw Error(label)};check(document.querySelectorAll('article').length===6,'six cards');check([...document.images].every(i=>i.complete&&i.naturalWidth>0),'portraits load');check(document.querySelectorAll('article .button').length===6,'six reviews');check(document.querySelectorAll('article .copy>a:last-child').length===6,'six art galleries');check(document.documentElement.scrollWidth<=innerWidth,'no horizontal overflow');document.getElementById('qa-result').textContent=JSON.stringify({status:'PASS',assertions:n,width:innerWidth})}catch(e){document.getElementById('qa-result').textContent=JSON.stringify({status:'FAIL',error:String(e)})}},1500)</script>'''
test=test.replace('===6','==='+str(len(BATCH))).replace('six ',str(len(BATCH))+' ')
file=T/'review.html';file.write_text(page+test,encoding='utf-8');results=[]
for label,size in [('desktop','1440,1100'),('phone','390,1000')]:
 target=file
 if label=='phone':
  target=T/'phone-frame.html'
  target.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:0}iframe{border:0;width:390px;height:1000px}#qa-result{position:absolute;left:400px}</style><pre id="qa-result">PENDING</pre><iframe id="frame" src="'+file.as_uri()+'" onload="setTimeout(()=>document.getElementById(\'qa-result\').textContent=document.getElementById(\'frame\').contentDocument.getElementById(\'qa-result\').textContent,2500)"></iframe>',encoding='utf-8')
 run=subprocess.run(['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files','--hide-scrollbars','--window-size='+size,'--user-data-dir='+str(T/label),'--dump-dom','--virtual-time-budget=5000','--screenshot='+str(T/(label+'.png')),target.as_uri()],capture_output=True,timeout=45,creationflags=0x08000000)
 out=run.stdout.decode('utf-8',errors='replace');m=re.search(r'<pre id="qa-result">(.*?)</pre>',out,re.S);assert m,run.stderr.decode('utf-8',errors='replace')[-1000:]
 result=json.loads(html.unescape(m[1]));assert result['status']=='PASS',result;results.append(dict(viewport=label,**result))
(S/'manhwa-hub-validation.json').write_text(json.dumps(results,indent=2));print('MANHWA_HUB_VERIFIED',results)
