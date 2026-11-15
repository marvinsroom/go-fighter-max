"""Verify preserved sources, installed hashes, body coverage and runtime proof."""
from jin_mori_assets import *
import hashlib,re,struct

b=json.loads((S/'build-report.json').read_text())
for n,v in b['original_files'].items():assert hashlib.sha256((U/n).read_bytes()).hexdigest()==v['sha256'],n
assert hashlib.sha256((S/'source/Jin_Mori.zip').read_bytes()).hexdigest()==b['source']['sha256']
for n,digest in b['runtime_sha256'].items():assert hashlib.sha256((E/'chars/jin_mori'/n).read_bytes()).hexdigest()==digest,n
air=(E/'chars/jin_mori/jin_mori.air').read_text();source=(U/'Jin Mori.air').read_text(encoding='latin1')
def actions(text):
    result={}
    for block in re.split(r'(?=\[Begin Action\s+)',text,flags=re.I):
        h=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
        if h:result[int(h[1])]=[int(line.split(';')[0].split(',')[4]) for line in block.splitlines() if re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',line)]
    return result
assert all(actions(air).get(k)==v for k,v in actions(source).items()),'Preserved source action durations changed'
assert not re.search(r'^\s*(?:[0-9]{1,3}|[1-5][0-9]{3})\s*,\s*\d+\s*,',air,re.M),'Unconverted actor frame'
proof=json.loads((S/'runtime-validation.json').read_text())
assert proof['status']=='Complete' and proof['failed']==0
assert proof['runtime_sha256']==b['runtime_sha256']
assert len(proof['checks'])>=71
assert all(c['target_final_state'] not in (315,4512,9804512,9804513) for c in proof['checks']),'Victim left in a custom state'
for name in ('Monkey King','Monkey King facing left'):
    c=next(c for c in proof['checks'] if c['name']==name)
    assert c['damage']>=500 and c['seen'].get('4501'),name
    frames=[f for f in proof['frames'] if f['case_name']==name and f['state']==4501]
    assert {10,11,12,13,14,15}<={f['drawing'] for f in frames},('Missing staff stage',name)
    assert all(f['group']==62302 and f.get('target_group',-1)>=0 for f in frames),name
startup=json.loads((S/'startup-validation.json').read_text())
assert startup['passed'] and startup['intro_seen'] and startup['greeting_seen'],'Natural round intro did not play'
assert len(json.loads((S/'pose-registration.json').read_text()))==48
assert len(json.loads((S/'upgrade-registration.json').read_text()))==48
transition=json.loads((S/'awakening-registration.json').read_text())
assert len(transition)==8 and {r['pose'] for r in transition}==set(range(8))
assert all(r['size'][1]==r['axis'][1]==424 for r in transition),'Transition changes planted body height'
registered=json.loads((S/'upgrade-registration.json').read_text())
for group,pose in ((62300,0),(62301,0),(62302,0),(62302,8)):
    assert next(r for r in registered if r['group']==group and r['pose']==pose)['size'][1]==424,(group,pose)
for name,order in [('Transform into Monkey King',list(range(8))),('Return to Jin Mori',list(range(7,-1,-1)))]:
    frames=sorted([f for f in proof['frames'] if f['case_name']==name and f['group']==62304],key=lambda f:f['case_tick'])
    seen=[]
    for f in frames:
        if not seen or seen[-1]!=f['drawing']:seen.append(f['drawing'])
    assert seen==order,('Missing or out-of-order awakening stage',name,seen)
    assert all(f['state']==980500 for f in frames),name
    # Completion must return to normal control, rather than leave the last art
    # frame posing as an idle animation.
    last=max((f for f in proof['frames'] if f['case_name']==name),key=lambda f:f['case_tick'])
    assert last['state']==0 and last['group']==(62300 if order[0]==0 else 62000),last
for name,states,damage in [('Z Z Z chain',[230,240,250],140),('X X X chain',[270,280,290],190),('Z X C chain',[230,260,310],160),('Monkey King Z X C chain',[230,260,310],160)]:
    c=next(c for c in proof['checks'] if c['name']==name)
    assert c['damage']>=damage and all(c['seen'].get(str(n)) for n in states),name
for name,form in [('Transform into Monkey King',1),('Return to Jin Mori',0),('Monkey King takes a hit',1)]:
    assert next(c for c in proof['checks'] if c['name']==name)['form']==form,name
for f in proof['frames']:
    if f['case_name']=='Monkey King idle' and f['case_tick']>20:assert f['group']==62300,f
cmd=(E/'chars/jin_mori/jin_mori.cmd').read_text(encoding='utf-8')
remap=cmd.split('[Remap]',1)[1].split('[command]',1)[0]
for key in ('a','b','c','x','y','z'):assert re.search(r'^'+key+r'\s*=\s*'+key+r'\s*$',remap,re.M),key
definitions={}
for block in re.split(r'(?i)\[command\]',cmd):
    n=re.search(r'(?im)^name\s*=\s*"([^"]+)"',block);k=re.search(r'(?im)^command\s*=\s*([^\n;]+)',block)
    if n and k:definitions[n[1]]=k[1].strip()
for route in b['routes']:assert definitions[route['name']]==route['input'],route
for key in ('a','b','c'):assert definitions[key]==key,key
page=(S/'review.html').read_text(encoding='utf-8')
for ref in re.findall(r'(?:src|href)="([^"]+)"',page):
    if not ref.startswith(('http','#','data:')):assert (S/ref.split('?')[0]).exists(),ref
print('MORI_VERIFIED',len(actions(source)),'source actions preserved;',proof['passed'],'native checks;',len(proof['frames']),'captures')
