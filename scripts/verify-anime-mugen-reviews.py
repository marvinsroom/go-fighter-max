"""Exercise native recording players and load every captured frame in Edge."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from html import unescape
import json,subprocess,re,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):self.links.extend(v for k,v in attrs if k in ('href','src'))
for slug in ('naruto','saitama'):
 f=S/'characters'/slug;p=f/'review.html';source=p.read_text(encoding='utf-8');links=Links();links.feed(source)
 for link in links.links:
  u=urlsplit(link)
  if not u.scheme and u.path:assert (f/unquote(u.path)).is_file(),link
 body="""let assertions=0,count=0;const check=(v,n)=>{assertions++;if(!v)throw Error(n)};const images=[];for(const [name,items] of Object.entries(groups)){clip.value=name;clip.onchange();check(index===0,'reset');document.getElementById('next').click();check(index===1%items.length,'next');document.getElementById('previous').click();check(index===0,'previous');for(const v of items){images.push(new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{check(im.naturalWidth>0,'frame loads');resolve()};im.onerror=()=>reject(Error(v.src));im.src=v.src}));count++}}await Promise.all(images);document.getElementById('play').click();check(timer!==null,'play');document.getElementById('play').click();check(timer===null,'pause');check(document.documentElement.scrollWidth<=innerWidth+1,'page fits');return {status:'PASS',assertions,clips:Object.keys(groups).length,frames:count,viewport:innerWidth};"""
 harness='<pre id="anime-qa">PENDING</pre><script>setTimeout(async()=>{try{document.getElementById("anime-qa").textContent=JSON.stringify(await(async()=>{'+body+'})())}catch(e){document.getElementById("anime-qa").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},1000)</script>'
 temp=R/'.tmp'/('anime-import-browser-'+slug);temp.mkdir(exist_ok=True);test=temp/'review.html';test.write_text(source.replace('<head>','<head><base href="'+f.as_uri()+'/">',1)+harness,encoding='utf-8');results=[]
 for width,height,label in [(1440,1000,'desktop'),(390,844,'narrow')]:
  args=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files','--user-data-dir='+str(temp/label),f'--window-size={width},{height}','--virtual-time-budget=12000','--dump-dom',test.as_uri()]
  run=subprocess.run(args,capture_output=True,timeout=60,creationflags=0x08000000);m=re.search(r'<pre id="anime-qa">(.*?)</pre>',run.stdout.decode('utf-8',errors='replace'),re.S);assert m,run.stderr.decode('utf-8',errors='replace')[-1200:];v=json.loads(unescape(m[1]));assert v['status']=='PASS',v;v['view']=label;results.append(v)
 proof=dict(status='PASS',review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),local_links=len(links.links),views=results);(f/'viewer-validation.json').write_text(json.dumps(proof,indent=2));print('ANIME_BROWSER_PASS',slug,proof,flush=True)
