"""Validate every comparison asset and exercise the face review in Edge."""
from pathlib import Path
import json,re,subprocess,html,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';A=S/'face-audit';T=R/'.tmp/face-audit-browser';T.mkdir(parents=True,exist_ok=True)
audit=json.loads((A/'audit.json').read_text());assert len(audit['fighters'])==14
page=(A/'review.html').read_text(encoding='utf-8')
for ref in re.findall(r'(?:src|href)="([^"]+)"',page):
 if not ref.startswith('http'):assert (A/ref).exists(),ref
for row in audit['fighters']:assert (S/row['reference']).exists()
page=page.replace('<html lang="en">','<html lang="en"><head><base href="'+A.as_uri()+'/"></head>',1)
test='''<pre id="qa-result">PENDING</pre><script>setTimeout(()=>{try{let assertions=0;const check=(ok,label)=>{assertions++;if(!ok)throw Error(label)};check(document.querySelectorAll('article').length===14,'fourteen comparisons');for(const im of document.images)check(im.complete&&im.naturalWidth>0,'image '+im.src);check(document.documentElement.scrollWidth<=innerWidth,'no horizontal overflow');document.getElementById('qa-result').textContent=JSON.stringify({status:'PASS',assertions,width:innerWidth})}catch(e){document.getElementById('qa-result').textContent=JSON.stringify({status:'FAIL',error:String(e)})}},1800)</script>'''
file=T/'review.html';file.write_text(page+test,encoding='utf-8');results=[]
for label,size in [('desktop','1440,1100'),('phone','390,1000')]:
 target=file
 if label=='phone':
  target=T/'phone-frame.html'
  target.write_text('<!doctype html><meta charset="utf-8"><style>body{margin:0}iframe{border:0;width:390px;height:1000px}#qa-result{position:absolute;left:400px}</style><pre id="qa-result">PENDING</pre><iframe id="frame" src="'+file.as_uri()+'" onload="setTimeout(()=>document.getElementById(\'qa-result\').textContent=document.getElementById(\'frame\').contentDocument.getElementById(\'qa-result\').textContent,2500)"></iframe>',encoding='utf-8')
 run=subprocess.run(['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files','--hide-scrollbars','--window-size='+size,'--user-data-dir='+str(T/label),'--dump-dom','--virtual-time-budget=5000','--screenshot='+str(T/(label+'.png')),target.as_uri()],capture_output=True,timeout=45,creationflags=0x08000000)
 out=run.stdout.decode('utf-8',errors='replace');m=re.search(r'<pre id="qa-result">(.*?)</pre>',out,re.S);assert m,run.stderr.decode('utf-8',errors='replace')[-1000:]
 result=json.loads(html.unescape(m[1]));assert result['status']=='PASS',result;results.append(dict(viewport=label,**result))
(A/'viewer-validation.json').write_text(json.dumps(dict(review_sha256=hashlib.sha256((A/'review.html').read_bytes()).hexdigest(),results=results),indent=2));print('FACE_REVIEW_VERIFIED',results)
