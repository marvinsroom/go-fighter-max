"""Exercise the local review in an isolated headless Edge browser, without dependencies."""
from pathlib import Path
import json,subprocess,os,re,uuid

R=Path(__file__).resolve().parents[1]
folder=R/'tmp/vikir-review-qa';folder.mkdir(parents=True,exist_ok=True)
page=R/'sprite-fighter/characters/vikir/review.html'
checks='''<!doctype html><meta charset="utf-8"><body><pre id="result">PENDING</pre>
<iframe style="width:1280px;height:900px" id="page"></iframe><script>
const iframe=document.getElementById('page'),results=[];
const wait=ms=>new Promise(r=>setTimeout(r,ms));
function check(ok,name){results.push({name,passed:!!ok});if(!ok)throw Error(name)}
iframe.onload=async()=>{try{
await wait(1000);const w=iframe.contentWindow,d=w.document,$=id=>d.getElementById(id);
check(d.title.includes('Vikir'),'Page title');
if($('play').textContent==='Pause')$('play').click();
await wait(500);
check([...d.images].every(i=>i.complete&&i.naturalWidth>0),'All page images load');
check(!!d.querySelector('.character-nav'),'Shared character navigation');
check(!!w.FIGHTER_REVIEW,'Shared review data contract');
const data=w.FIGHTER_REVIEW;
for(const category of ['Ultimates','Supers','Academy','Guests','Archery'])check([...$('category').options].some(o=>o.value===category),category+' category');
for(const guest of ['Dolores','Camu','Aiyen','Sinclair'])check(data.groups.Guests.some(n=>n.includes(guest)),guest+' guest clips');
check(data.groups.Archery.some(n=>n.includes('Anubis')),'Anubis archery clips');
check($('ultimates').children.length>=4,'Ultimate shortcuts for every appearance');
if($('play').textContent==='Pause')$('play').click();
$('category').value='Supers';$('category').dispatchEvent(new w.Event('change'));await wait(500);
check([...$('clip').options].some(o=>o.value.includes('Three Fangs')),'Three Fangs super');
check([...$('clip').options].some(o=>o.value.includes('Beelzebub')),'Blood Draw super');
check([...$('clip').options].some(o=>o.value.includes('Seven Fangs')),'Seven Fangs is a super');
check(data.groups.Ultimates.every(n=>!n.includes('Seven Fangs')),'Seven Fangs excluded from ultimates');
check(d.body.textContent.includes('Hold Enter'),'Power charge control documented');
$('category').value='Academy';$('category').dispatchEvent(new w.Event('change'));await wait(500);
check($('capture').complete&&$('capture').naturalWidth===1280,'Academy captures load');
$('category').value='Guests';$('category').dispatchEvent(new w.Event('change'));await wait(500);
check($('capture').complete&&$('capture').naturalWidth===1280,'Guest captures load');
$('category').value='Archery';$('category').dispatchEvent(new w.Event('change'));await wait(500);
check($('capture').complete&&$('capture').naturalWidth===1280,'Anubis captures load');
$('ultimates').lastElementChild.click();await wait(500);
check($('category').value==='Ultimates'&&$('detail').textContent.includes('Crimson Execution'),'Ultimate shortcut selects capture');
const old=$('detail').textContent;$('next').click();await wait(500);
check($('detail').textContent!==old,'Native frame stepping');
$('speed').value='0.25';$('speed').dispatchEvent(new w.Event('change'));
check($('capture').complete&&$('capture').naturalWidth===1280,'Capture image loaded');
check($('controls').textContent==='Controls','Shared controls section');
check(Object.keys(data.cases).length>=90,'Native clip library includes academy');
iframe.style.width='390px';await wait(500);
check(d.documentElement.scrollWidth<=d.documentElement.clientWidth,'Mobile has no horizontal overflow');
document.getElementById('result').textContent=JSON.stringify({status:'PASS',checks:results});
}catch(e){document.getElementById('result').textContent=JSON.stringify({status:'FAIL',error:String(e),checks:results})}};
iframe.src=PAGE;
</script>'''.replace('PAGE',json.dumps(page.as_uri()))
qa=folder/'checks.html';qa.write_text(checks,encoding='utf-8')
edge=Path(os.environ.get('PROGRAMFILES(X86)','C:/Program Files (x86)'))/'Microsoft/Edge/Application/msedge.exe'
common=[str(edge),'--headless=new','--disable-gpu','--in-process-gpu','--no-sandbox','--disable-gpu-sandbox','--no-first-run','--no-default-browser-check','--allow-file-access-from-files','--hide-scrollbars',f'--user-data-dir={folder / ("browser-"+uuid.uuid4().hex[:8])}']
creation=getattr(subprocess,'CREATE_NO_WINDOW',0)
run=subprocess.run(common+['--dump-dom','--virtual-time-budget=15000',qa.as_uri()],capture_output=True,text=True,timeout=90,creationflags=creation)
match=re.search(r'<pre id="result">(.*?)</pre>',run.stdout,re.S)
assert match,run.stderr[-1500:]
result=json.loads(match[1]);(folder/'result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
assert result['status']=='PASS',result
for label,width,height in [('desktop',1440,1100),('mobile',390,900)]:
    screenshot=folder/(label+'.png')
    target=page
    if label=='mobile':
        # Edge enforces a minimum top-level layout width in headless mode.
        # An explicitly sized frame exercises a real 390px CSS viewport.
        target=folder/'mobile-preview.html'
        target.write_text(f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;overflow:hidden}}iframe{{display:block;border:0;width:{width}px;height:{height}px}}</style><iframe title="Mobile review" src="{page.as_uri()}"></iframe>',encoding='utf-8')
    subprocess.run(common+[f'--window-size={width},{height}',f'--screenshot={screenshot}','--virtual-time-budget=2000',target.as_uri()],capture_output=True,timeout=60,creationflags=creation,check=True)
    assert screenshot.exists()
print('VIKIR_REVIEW_BROWSER_VERIFIED',len(result['checks']),'checks; desktop and mobile screenshots in',folder)
