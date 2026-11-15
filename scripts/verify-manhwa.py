"""Verify installed runtime, source preservation, combat and cinematic presentation."""
from manhwa_fighters import *
from PIL import Image
import sys,hashlib,re
p=profile(sys.argv[1]);S=p['folder'];b=json.loads((S/'build-report.json').read_text());r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and r['failed']==0 and r['passed']>=66
assert r['runtime_sha256']==b['runtime_sha256']
for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((E/'chars'/p['id']/name).read_bytes()).hexdigest()==digest,name
source=json.loads((S/'source/source-report.json').read_text());assert source['kind']=='custom adaptation' and source['upstream_character_release'] is None
for name,digest in source['foundation'].items():assert hashlib.sha256((S/'source/engine-foundation'/name).read_bytes()).hexdigest()==digest
rows=json.loads((S/'pose-registration.json').read_text());assert len(rows)==48
for group,pose in [(62000,0),(62400,0),(62600,4)]:assert next(row for row in rows if row['group']==group and row['pose']==pose)['size'][1]==424
assert r.get('natural_intro_seen')
checks={c['name']:c for c in r['checks']}
for name,damage in [('Light',35),('Medium',45),('Heavy',80),('Low light',30),('Low medium',50),('Low heavy',70)]:assert checks[name]['damage']==damage,(name,checks[name])
for name,states,damage in [('Z Z Z',[200,210,220],140),('X X X',[230,240,250],170),('Z X C',[200,230,260],160)]:
    for suffix in ('',' facing left'):
        c=checks[name+suffix];assert c['damage']>=damage and all(c['seen'].get(str(n)) for n in states),c
for index in (2,5):assert checks[p['moves'][index]]['damage']>0
for suffix in ('',' facing left',' left wall',' right wall'):
    name=p['moves'][-1]+suffix;c=checks[name];assert c['damage']==p['ultimate'] and c['min_power']==0 and c['seen'].get('3001'),c
    frames=[f for f in r['frames'] if f['case_name']==name and f['state']==3001]
    if suffix in ('',' facing left'):
        assert set(range(5,12))<={f['drawing'] for f in frames if f['group']==62600},('Missing ultimate pose',name)
        assert any(f.get('beam_count',0)>0 for f in frames),('Missing final discharge',name)
for suffix in (' blocked',' miss',' insufficient meter'):assert not checks[p['moves'][-1]+suffix]['seen'].get('3001')
for suffix in ('',' facing left'):assert checks['Light into ultimate'+suffix]['damage']==p['ultimate']+35
assert checks['Chain on guard']['seen'].get('220') and not checks['Whiff cannot chain']['seen'].get('210')
assert checks[p['taunt']]['seen'].get('800')
if p['slug']=='arthur':
    greeting=[f for f in r['frames'] if f['case_name']==p['taunt'] and f['state']==800]
    assert any(f['drawing'] in (14,15) and f.get('companion_count',0)>0 for f in greeting), 'Missing Sylvie companion'
    assert all(not f.get('companion_count',0) for f in greeting if f['drawing']==13), 'Duplicate Sylvie over the authored shoulder pose'
assert all(c['target_final_state'] not in (3050,3051,3052) for c in r['checks'])
for f in r['frames']:
    with Image.open(S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']) as im:im.verify()
    if f['state']==3001 and 8<=f.get('cinematic_tick',0)<140:assert 40<=f['target_screen']<=280,('Unsafe cinematic framing',f)
startup=json.loads((S/'startup-ai-validation.json').read_text());assert startup['passed'] and startup['runtime_sha256']==b['runtime_sha256']
for ref in re.findall(r'(?:src|href)="([^"]+)"',(S/'review.html').read_text(encoding='utf-8')):
    if not ref.startswith(('http','#','data:')):assert (S/ref.split('?')[0]).exists(),ref
print('MANHWA_VERIFIED',p['name'],r['passed'],'checks',len(r['frames']),'captures')
