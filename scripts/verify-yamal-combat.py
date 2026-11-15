"""Validate the delivered package, native results and replay provenance."""
from pathlib import Path
from PIL import Image
import hashlib, json, re, struct
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'sprite-fighter/characters/yamal'
OUT=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/yamal'
build=json.loads((SOURCE/'build-report.json').read_text())
runtime=json.loads((SOURCE/'runtime-validation.json').read_text())
assert runtime['status']=='Complete' and runtime['passed']==43 and runtime['failed']==0,runtime.get('current')
assert all(c['passed'] for c in runtime['checks'])
p1=json.loads((SOURCE/'player-one-validation.json').read_text())
assert p1['status']=='Complete' and len(p1['checks'])==2 and all(c['passed'] for c in p1['checks'])
assert len(build['sprites'])==9
sff=(OUT/'yamal.sff').read_bytes();start=struct.unpack_from('<I',sff,52)[0]
offset,count=struct.unpack_from('<II',sff,36)
entries={}
for i in range(count):
    h=struct.unpack_from('<HHHHhhHBBIIHH',sff,offset+i*28);entries[h[0],h[1]]=h
for key,m in build['sprites'].items():
    path=ROOT/m['file'];raw=path.read_bytes();h=entries[m['group'],m['number']]
    assert hashlib.sha256(raw).hexdigest()==m['sha256']
    assert sff[start+h[9]+4:start+h[9]+h[10]]==raw,key
    with Image.open(path) as im:assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
scales=[m['scale'] for m in build['sprites'].values()]
assert max(scales)/min(scales)<1.09,scales
native=json.loads((SOURCE/'native-preview-report.json').read_text())
files=sorted((SOURCE/'replays/native-release').glob('Yamal_Native_Review*.png'))
assert len(files)==len(native['frames']) and len(files)>150
assert {'movement','curler','rainbow','super','ultimate'}=={f['move'] for f in native['frames']}
for move in ['movement','curler','rainbow','super','ultimate']:
    with Image.open(SOURCE/f'{move}-replay-v1.gif') as im:assert im.n_frames>10
review=(SOURCE/'review.html').read_text()
for link in re.findall(r'(?:src|href)="([^"]+)"',review):
    if '://' not in link and not link.startswith('#'):assert (SOURCE/link.replace('%20',' ')).exists(),link
assert 'yamal, stages/stage0-720.def' in (OUT.parents[1]/'data/select.def').read_text()
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('yamal.*')}
result={'status':'Passed','native_checks':45,'combat_checks':43,'player_one_checks':2,'failed':0,'lossless_character_pngs':9,
        'sprite_scale_ratio':max(scales)/min(scales),'native_replay_frames':len(files),'engine_package_sha256':hashes}
(SOURCE/'verification.json').write_text(json.dumps(result,indent=2))
build['status']='Native validated: 43 combat checks and 2 Player 1 checks passed'
build['validation']={'combat_passed':43,'player_one_passed':2,'failed':0,'native_replay_frames':len(files)}
(SOURCE/'build-report.json').write_text(json.dumps(build,indent=2))
print('YAMAL_VERIFIED',json.dumps(result))
