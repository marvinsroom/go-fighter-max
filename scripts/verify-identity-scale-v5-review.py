"""Check the current roster comparison in desktop/mobile Edge and local links."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit,unquote
import subprocess,re,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/face-audit/identity-scale-v5';p=O/'review.html';source=p.read_text(encoding='utf-8');temp=R/'.tmp/identity-scale-v5-browser';temp.mkdir(exist_ok=True)
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ('href','src'))
links=Links();links.feed(source)
for link in links.links:
 u=urlsplit(link)
 if not u.scheme and u.path:assert (O/unquote(u.path)).is_file(),link
body="""let checks=0;const check=(v,n)=>{checks++;if(!v)throw Error(n)};check(document.querySelectorAll('article').length===26,'all26fighters');check(document.querySelector('#jin-mu-won .faces'),'Jin reference comparison');check(document.querySelector('#eugene .faces'),'adult Eugene comparison');for(const im of document.images){check(im.complete&&im.naturalWidth>0,'image '+im.getAttribute('src'))};for(const d of document.querySelectorAll('details')){d.open=true;check(d.open,'details opens');d.open=false};check(document.documentElement.scrollWidth<=innerWidth+1,'no page overflow');check(document.querySelector('.lineup').scrollWidth>document.querySelector('.lineup').clientWidth,'lineup scrolls');return {status:'PASS',checks,viewport:innerWidth,images:document.images.length};"""
harness='<pre id="stature-qa">PENDING</pre><script>setTimeout(()=>{try{const result=(()=>{'+body+'})();document.getElementById("stature-qa").textContent=JSON.stringify(result)}catch(e){document.getElementById("stature-qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},1500)</script>'
test=temp/'review.html';test.write_text(source.replace('<meta charset','<base href="'+O.as_uri()+'/"><meta charset',1)+harness,encoding='utf-8');reports=[]
for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile')]:
 args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=6000','--dump-dom',test.as_uri()]
 run=subprocess.run(args,capture_output=True,timeout=60,creationflags=0x08000000);m=re.search(r'<pre id="stature-qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert m,run.stderr.decode('utf-8',errors='replace')[-1000:];proof=json.loads(unescape(m[1]));assert proof['status']=='PASS',proof;proof['view']=label;reports.append(proof)
 # Screenshots are of the real final page, without the injected assertions.
 args=[a for a in args if a not in ('--dump-dom',test.as_uri())]+['--screenshot='+str(O/(label+'.png')),p.as_uri()];subprocess.run(args,capture_output=True,timeout=60,creationflags=0x08000000,check=True)
report=dict(status='PASS',review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),local_links=len(links.links),views=reports);(O/'browser-validation.json').write_text(json.dumps(report,indent=2));print('V5_REVIEW_BROWSER_PASS',report)
