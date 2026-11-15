"""Verify installed assets and actual native behavioral evidence."""
from baam_model import *
from baam_combat_v3 import ULTIMATE_BASE,ULTIMATE_VIOLE
from PIL import Image
import hashlib,re

b=json.loads((S/'build-report.json').read_text())
r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and r['failed']==0
assert r['runtime_sha256']==b['runtime_sha256']
for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((E/'chars/baam'/name).read_bytes()).hexdigest()==digest,name
src=json.loads((S/'source/source-report.json').read_text())
assert src['kind']=='custom adaptation' and src['upstream_baam_release'] is None
for name,digest in src['foundation'].items():assert hashlib.sha256((S/'source/engine-foundation'/name).read_bytes()).hexdigest()==digest
rows=json.loads((S/'pose-registration.json').read_text())
assert len(rows)==136
for g in (62000,62001,62100,62101,62400,62500):assert next(x for x in rows if x['group']==g and x['pose']==0)['size'][1]==424
assert all(x['size'][1]==x['axis'][1]==424 for x in rows if x['group']==62300)
assert len(r['checks'])>=130,'Incomplete full gameplay suite'
assert r.get('natural_intro_seen') and r.get('cuff_adjustment_seen'),'Production entrance did not play'
startup=json.loads((S/'startup-ai-validation.json').read_text())
assert startup['passed'] and startup['runtime_sha256']==b['runtime_sha256'],'Production CPU/entrance proof missing or stale'
checks={c['name']:c for c in r['checks']}
for prefix in ('Base / ','Viole / '):
    for name,states,damage in [('Z Z Z',[200,210,220],140),('X X X',[230,240,250],170),('Z X C',[200,230,260],160)]:
        for suffix in ('',' facing left'):
            c=checks[prefix+name+suffix];assert c['damage']>=damage and all(c['seen'].get(str(n)) for n in states),(prefix,name,suffix)
    for name,damage in [('Light',35),('Medium',45),('Heavy',80)]:assert checks[prefix+name]['damage']==damage,(prefix,name)
    for suffix in ('',' facing left'):
        name=prefix+'Shinwonryu'+suffix
        c=checks[name];assert c['seen'].get('3001') and c['damage']==(ULTIMATE_BASE if prefix.startswith('Base') else ULTIMATE_VIOLE) and c['min_power']==0,c
        stages={f['drawing'] for f in r['frames'] if f['case_name']==name and f['state']==3001 and f['group']==62600}
        assert ({1,2,3,4,5,6,7} if prefix.startswith('Base') else {9,10,11,12,13,14,15})<=stages,('Ultimate stages missing from native capture',name,stages)
    beam=[f for f in r['frames'] if f['case_name']==prefix+'Shinwonryu' and f['state']==3001 and f.get('beam_count',0)>0]
    assert beam,'Final discharge missing from native capture'
    for side in ('left wall','right wall'):
        c=checks[prefix+'Shinwonryu '+side];assert c['damage']==(ULTIMATE_BASE if prefix.startswith('Base') else ULTIMATE_VIOLE) and c['seen'].get('3001'),c
    for suffix in ('',' facing left'):
        c=checks[prefix+'Light into Shinwonryu'+suffix];assert c['seen'].get('200') and c['seen'].get('3001'),c
    for suffix in (' blocked',' miss',' insufficient meter'):assert not checks[prefix+'Shinwonryu'+suffix]['seen'].get('3001'),(prefix,suffix)
    for name in ('Reverse Flow Control','Blue Thryssa Guard'):assert checks[prefix+name]['damage']>0,(prefix,name)
for name,form in [('Transform into Viole',1),('Return to base',0),('Viole survives damage',1),('Interrupted awakening',0)]:assert checks[name]['form']==form,name
assert all(c['target_final_state'] not in (3050,3051,3052) for c in r['checks'])
for name,order in [('Transform into Viole',list(range(8))),('Return to base',list(range(7,-1,-1)))]:
    frames=sorted((f for f in r['frames'] if f['case_name']==name and f['group']==62300),key=lambda f:f['case_tick']);seen=[]
    for f in frames:
        if not seen or seen[-1]!=f['drawing']:seen.append(f['drawing'])
    assert seen==order,(name,seen)
for f in r['frames']:
    path=S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']
    with Image.open(path) as im:im.verify()
    if f['case_name']=='Viole / Idle' and f['case_tick']>20:assert f['group']==62100
    if f['state']==3001 and 8<=f.get('cinematic_tick',0)<140:
        assert 40<=f['target_screen']<=280,('Cinematic victim outside safe framing',f)
page=(S/'review.html').read_text(encoding='utf-8')
for ref in re.findall(r'(?:src|href)="([^"]+)"',page):
    if not ref.startswith(('http','#','data:')):assert (S/ref.split('?')[0]).exists(),ref
print('BAAM_VERIFIED',r['passed'],'checks;',len(r['frames']),'native captures')
