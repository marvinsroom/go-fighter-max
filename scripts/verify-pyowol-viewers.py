"""Exercise local animation and native-capture controls in a real browser."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'sprite-fighter/characters/pyowol';TMP=ROOT/'.tmp/pyo-viewer-checks';TMP.mkdir(parents=True,exist_ok=True)
EDGE=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
checks={
 'animation':('animation-review.html',r'''
let assertions=0;function check(ok,label){assertions++;if(!ok)throw Error(label)}
check(menu.options.length===Object.keys(clips).length,'all animation options');
for(const name of Object.keys(clips)){
 menu.value=name;menu.onchange();check(index===0,'selection resets frame');
 check(rows().length>=4,'sequence includes all motion stages');
 document.getElementById('next').click();check(index===1&&!playing,'next pauses and steps');
 document.getElementById('previous').click();check(index===0,'previous steps back');
 check(detail.textContent.includes(name),'move label');
}
speed.value='0.25';speed.onchange();check(Number(speed.value)===.25,'slow playback');
play.click();check(playing,'play resumes');play.click();check(!playing,'pause works');
check([...images.values()].every(im=>im.complete&&im.naturalWidth>0),'every drawing loads');
return {status:'PASS',assertions,clips:Object.keys(clips).length};
'''),
 'native':('review.html',r'''
let assertions=0,count=0;function check(ok,label){assertions++;if(!ok)throw Error(label)}
if(playing)play.click();
for(const [group,names] of Object.entries(data.groups)){
 category.value=group;category.onchange();check(clip.options.length===names.length,'category options');
 for(const name of names){
  clip.value=name;clip.onchange();check(index===0,'clip resets');
  document.getElementById('next').click();check(index===1%frames().length,'native next');
  document.getElementById('previous').click();check(index===0,'native previous');
  check(capture.getAttribute('src').includes(frames()[0].src),'selected capture source');count++;
 }
}
document.getElementById('speed').value='0.25';document.getElementById('speed').onchange();
play.click();check(playing,'native play');play.click();check(!playing,'native pause');
return {status:'PASS',assertions,clips:count};
''')
}
results={}
for name,(filename,body) in checks.items():
    source=(FOLDER/filename).read_text(encoding='utf-8')
    source=source.replace('<head>','<head><base href="'+FOLDER.as_uri()+'/">',1)
    # Both pages use <head> with no attributes. Their own scripts run unchanged.
    harness='''<pre id="test-results">PENDING</pre><script>setTimeout(()=>{try{const result=(()=>{'''+body+'''})();document.getElementById('test-results').textContent=JSON.stringify(result)}catch(error){document.getElementById('test-results').textContent=JSON.stringify({status:'FAIL',error:String(error)})}},1000)</script>'''
    path=TMP/f'{name}.html';path.write_text(source+harness,encoding='utf-8')
    run=subprocess.run([str(EDGE),'--headless','--disable-gpu','--no-first-run','--allow-file-access-from-files',f'--user-data-dir={TMP/(name+"-profile")}','--dump-dom','--virtual-time-budget=4000',path.as_uri()],capture_output=True,timeout=45,creationflags=0x08000000)
    output=run.stdout.decode('utf-8',errors='replace')
    match=re.search(r'<pre id="test-results">(.*?)</pre>',output,re.S)
    assert match,run.stderr.decode('utf-8',errors='replace')[-1500:]
    result=json.loads(unescape(match[1]));assert result['status']=='PASS',result
    results[name]=result

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):self.links += [v for k,v in attrs if k in ('href','src')]

links=0
for filename in ('review.html','animation-review.html','art/animation-v5/design-review.html','proportion-audit.html','art/thread-v6/review.html'):
    path=FOLDER/filename;parser=Links();parser.feed(path.read_text(encoding='utf-8'))
    for link in parser.links:
        url=urlsplit(link)
        if not url.scheme and url.path:
            assert (path.parent/unquote(url.path)).exists(),(filename,link);links+=1
results['local_asset_links']=links
(FOLDER/'viewer-validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('VIEWERS_VERIFIED',sum(v['assertions'] for v in results.values() if isinstance(v,dict)),'browser interactions;',links,'local links')
