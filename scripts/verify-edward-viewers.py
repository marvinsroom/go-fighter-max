"""Exercise review controls in Edge and validate every local linked asset."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import json,re,subprocess
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/edward';T=R/'.tmp/edward-browser';T.mkdir(parents=True,exist_ok=True)
EDGE='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
checks={
 'review.html':'''let assertions=0;const check=(v,n)=>{assertions++;if(!v)throw Error(n)};if(playing)play.click();let count=0;for(const [g,names] of Object.entries(data.groups)){category.value=g;category.onchange();check(clip.options.length===names.length,'category');for(const n of names){clip.value=n;clip.onchange();check(index===0,'clip reset');document.getElementById('next').click();check(index===1%frames().length,'next');document.getElementById('previous').click();check(index===0,'previous');check(capture.getAttribute('src').includes(frames()[0].src),'capture');count++}}for(const button of ultimateNav.children){button.click();check(clip.value===button.dataset.clip,'ultimate shortcut')}document.getElementById('speed').value='.25';document.getElementById('speed').onchange();play.click();check(playing,'play');play.click();check(!playing,'pause');return {status:'PASS',assertions,clips:count};''',
 'animation-review.html':'''let assertions=0;const check=(v,n)=>{assertions++;if(!v)throw Error(n)};if(playing)play.click();check(menu.options.length===Object.keys(data.actions).length,'all actions');for(const id of Object.keys(data.actions)){menu.value=id;menu.onchange();check(index===0,'action reset');if(rows().length){document.getElementById('next').click();check(index===1%rows().length,'AIR next');document.getElementById('previous').click();check(index===0,'AIR previous')}}menu.value='0';menu.onchange();await new Promise(r=>setTimeout(r,300));check(images.get(rows()[0].sprite).naturalWidth>0,'drawing loads');check(detail.textContent.includes('Action 0'),'detail');speed.value='.25';speed.onchange();play.click();check(playing,'AIR play');play.click();check(!playing,'AIR pause');return {status:'PASS',assertions,actions:menu.options.length};'''
}
results={}
for filename,body in checks.items():
    page=(S/filename).read_text(encoding='utf-8').replace('<head>','<head><base href="'+S.as_uri()+'/">',1)
    harness='<pre id="test-results">PENDING</pre><script>setTimeout(async()=>{try{const result=await(async()=>{'+body+'})();document.getElementById("test-results").textContent=JSON.stringify(result)}catch(e){document.getElementById("test-results").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},1000)</script>'
    p=T/filename;p.write_text(page+harness,encoding='utf-8')
    run=subprocess.run([EDGE,'--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files',f'--user-data-dir={T/(filename+"-profile")}','--dump-dom','--virtual-time-budget=5000',p.as_uri()],capture_output=True,timeout=45,creationflags=0x08000000)
    out=run.stdout.decode('utf-8',errors='replace');m=re.search(r'<pre id="test-results">(.*?)</pre>',out,re.S)
    assert m,run.stderr.decode('utf-8',errors='replace')[-1200:]
    value=json.loads(unescape(m[1]));assert value['status']=='PASS',value;results[filename]=value
class Links(HTMLParser):
    def __init__(self):super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):self.targets += [v for k,v in attrs if k in ('href','src')]
count=0
for name in ['review.html','animation-review.html','proportion-audit.html','art/illustrated-v1/design-review.html']:
    p=S/name;parser=Links();parser.feed(p.read_text(encoding='utf-8'))
    for link in parser.targets:
        if link.startswith(('http','#','data:')):continue
        assert (p.parent/link.split('?')[0]).exists(),(name,link);count+=1
results['local_links']=count
(S/'viewer-validation.json').write_text(json.dumps(results,indent=2))
print('EDWARD_VIEWERS_VERIFIED',json.dumps(results))
