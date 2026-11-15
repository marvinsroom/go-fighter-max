"""Verify native evidence, source preservation, timing and installed hashes."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/edward';O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/edward'
d=json.loads((S/'runtime-validation.json').read_text());b=json.loads((S/'build-report.json').read_text());a=json.loads((S/'illustrated-build.json').read_text())
assert d['status']=='Complete' and d['failed']==0,d.get('failed')
assert d['runtime_sha256']==b['runtime_sha256'],'Build changed since engine verification'
for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
for name,meta in b['original_files'].items():assert hashlib.sha256((S/'source/upstream/Edward'/name).read_bytes()).hexdigest()==meta['sha256'],name
src=json.loads((S/'source/source-report.json').read_text());assert hashlib.sha256((S/'source'/src['archive']).read_bytes()).hexdigest()==src['sha256']
source=(S/'source/upstream/Edward/Animation.air').read_text(encoding='cp1252');derived=(O/'Animation.air').read_text()
def durations(s):
    out={}
    for block in re.split(r'(?=\[Begin Action\s+)',s,flags=re.I):
        m=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
        if m:out[m[1]]=[int(l.split(';',1)[0].split(',')[4]) for l in block.splitlines() if re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',l)]
    return out
assert durations(source)==durations(derived),'Source timing changed'
assert a['drawings']==64 and a['mapped_sprites']>=370
frames={}
for f in d['frames']:
    p=S/'replays'/f.get('capture_directory',d['capture_directory'])/f['file']
    with Image.open(p) as im:assert im.size==(1280,720);im.verify()
    frames.setdefault(f['case_name'],[]).append(f)
for case in json.loads((S/'test-cases.json').read_text()):
    if case.get('capture',True):assert len(frames.get(case['name'],[]))>=2,case['name']
checks={c['name']:c for c in d['checks']}
for name in ('Elric Final','Elric Final facing left'):
    assert checks[name]['damage']>400 and checks[name]['seen'].get('3105'),name
assert checks['Elric Final blocked']['damage']<30
assert checks['Charge and release']['max_power']>=100
if d.get('capture_repair'):
    expected={'Stone Spike':(3000,range(3)),'Stone Spike Medium':(3000,range(9,12)),
              'Stone Spike Strong':(3000,range(21,24)),'Stone Spike Ex':(1010,range(1)),
              'Stone Spike Barrage':(3000,range(24)),'Stone Spike Barrage Max':(3000,range(24)),
              'Stone Spike facing left':(3000,range(3)),'Stone Spike Barrage facing left':(3000,range(24))}
    for name,(group,numbers) in expected.items():
        assert any(f['group']==group and f['drawing'] in numbers for f in frames.get(name,[])),('Missing visible active spike frames',name)
for name,c in checks.items():
    if 'empty meter' in name:assert c['min_power']==0,name
    if name.endswith(' miss'):assert c['damage']==0,name
archive=Sff(O/'Edward.sff');assert len(archive.headers)==544
assert set(archive.keys)=={tuple(x['key']) for x in json.loads((S/'reference/sprites.json').read_text())}
print('EDWARD_VERIFIED',d['passed'],'native cases;',len(d['frames']),'captures;',len(durations(derived)),'actions retain timing;',a['mapped_sprites'],'registered sprites')
