"""Check any shared fighter review in a real headless browser."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
slug = sys.argv[1]
folder = ROOT / 'sprite-fighter/characters' / slug
page = folder / 'review.html'
temporary = ROOT / '.tmp' / (slug + '-comic-browser')
temporary.mkdir(exist_ok=True)

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(value for key, value in attrs if key in ('src', 'href'))

source = page.read_text(encoding='utf-8')
parser = Links()
parser.feed(source)
for link in parser.links:
    url = urlsplit(link)
    if not url.scheme and url.path:
        assert (folder / unquote(url.path)).is_file(), link

body = """let assertions=0;
const check=(v,n)=>{assertions++;if(!v)throw Error(n)};
if(playing)play.click();let count=0,frameCount=0;
for(const [group,names] of Object.entries(data.groups)){
 category.value=group;category.onchange();
 check(clip.options.length===names.length,'category options');
 for(const name of names){
  clip.value=name;clip.onchange();check(index===0,'clip reset');
  const rows=frames();check(rows.length>0,'nonempty clip');frameCount+=rows.length;
  document.getElementById('previous').click();check(index===rows.length-1,'wrap backward');
  document.getElementById('next').click();check(index===0,'wrap forward');
  check(capture.getAttribute('src').includes(rows[0].src),'native frame path');count++;
 }
}
for(const button of ultimateNav.children){button.click();check(clip.value===button.dataset.clip,'shortcut')}
document.getElementById('speed').value='0.25';document.getElementById('speed').onchange();
await new Promise(resolve=>setTimeout(resolve,500));
check(capture.complete&&capture.naturalWidth>0,'native image loads');
play.click();check(playing,'play');play.click();check(!playing,'pause');
check(!!document.querySelector('a[href="art/comic-identity-v3/design-review.html"]'),'current artwork link');
return {status:'PASS',assertions,clips:count,frame_references:frameCount};"""
harness = '<pre id="comic-test-results">PENDING</pre><script>setTimeout(async()=>{try{const result=await(async()=>{' + body + '})();document.getElementById("comic-test-results").textContent=JSON.stringify(result)}catch(e){document.getElementById("comic-test-results").textContent=JSON.stringify({status:"FAIL",error:String(e)})}},1000)</script>'
test_page = temporary / 'review.html'
test_page.write_text(source.replace('<head>', '<head><base href="' + folder.as_uri() + '/">', 1) + harness, encoding='utf-8')
result = subprocess.run([
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', '--headless',
    '--disable-gpu', '--no-first-run', '--allow-file-access-from-files',
    '--user-data-dir=' + str(temporary / 'profile'), '--dump-dom',
    '--virtual-time-budget=7000', test_page.as_uri()], capture_output=True, timeout=60,
    creationflags=0x08000000)
match = re.search(r'<pre id="comic-test-results">(.*?)</pre>', result.stdout.decode('utf-8', errors='replace'), re.S)
assert match, result.stderr.decode('utf-8', errors='replace')[-1200:]
proof = json.loads(unescape(match[1]))
assert proof['status'] == 'PASS', proof
proof['review_sha256'] = hashlib.sha256(page.read_bytes()).hexdigest()
(folder / 'comic-viewer-validation.json').write_text(json.dumps(proof, indent=2))
print('COMIC_REVIEW_VERIFIED', slug, json.dumps(proof))
