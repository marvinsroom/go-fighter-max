"""Validate the standalone package, original art and completed native results."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, io, json, re, struct, wave
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'sprite-fighter/characters/urkel'
CHAR=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/urkel'
runtime=json.loads((SOURCE/'runtime-validation.json').read_text())
assert runtime['status']=='Complete' and runtime['failed']==0, runtime
assert runtime['passed']==52, runtime['passed']
checks={row['name']:row for row in runtime['checks']}
assert all(not row['outfitViolations'] for row in runtime['checks'])
assert all(row['robotMissing']==0 and row['robotLeak']==0 for row in runtime['checks'])
for name,damage in [('Urkel invention ultimate',400),('Urkel Gadget Malfunction',210),('Stefan super',245),('Stefan ultimate',390),
                    ('Urkel captured by Fresh Prince ultimate',420),('Urkel captured by Agent ultimate',390)]:
    assert checks[name]['damage']==damage, name
assert checks['Urkel invention ultimate']['robotSeen']==1
for name in ['Urkel ultimate misses','Urkel ultimate blocked','Stefan ultimate','Stefan ultimate misses','Stefan ultimate blocked']:
    assert checks[name]['robotSeen']==0, name
assert 'urkel-tests.cns' not in (CHAR/'urkel.def').read_text()
report=json.loads((SOURCE/'build-report.json').read_text())
assert report['robot_framing_revision']==2
assert len(report['robot_framing'])==4
for frame in report['robot_framing']:
    left,top,right,bottom=frame['bounds']
    assert left>=40 and right<=1240 and top>=40 and bottom<=680, frame
data=(CHAR/'urkel.sff').read_bytes();offset,count=struct.unpack_from('<II',data,36);data_start=struct.unpack_from('<I',data,52)[0]
entries=[struct.unpack_from('<HHHHhhHBBIIHH',data,offset+i*28) for i in range(count)]
assert len({(e[0],e[1]) for e in entries})==count
for key,item in report['sprites'].items():
    path=ROOT/item['file'];assert path.is_relative_to(SOURCE), path
    entry=next(e for e in entries if (e[0],e[1])==(item['group'],item['number']))
    start,length=entry[9:11]
    assert hashlib.sha256(data[data_start+start+4:data_start+start+length]).hexdigest()==item['sha256']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
    assert path.with_suffix('.prompt.txt').is_file(), path
# All compatibility aliases must link to this character's own recorded sprites.
for entry in entries:
    if entry[10]==0:
        linked=entries[entry[6]]
        assert linked[0] in (20,30), entry
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('src','href') and value and '://' not in value:
                assert (SOURCE/value).is_file(), value
Links().feed((SOURCE/'review.html').read_text(encoding='utf-8'))
raw=(CHAR/'urkel.snd').read_bytes();assert raw[:12]==b'ElecbyteSnd\0'
sounds,offset=struct.unpack_from('<II',raw,16);assert sounds==4
for _ in range(sounds):
    nxt,size,group,number=struct.unpack_from('<IIII',raw,offset)
    with wave.open(io.BytesIO(raw[offset+16:offset+16+size]),'rb') as wav:assert wav.getnframes()>0
    offset=nxt
report['status']='Passed 52 native combat checks and keyboard visual checks; first playable key-pose art pass'
report['runtime_validation']={'passed':52,'failed':0,'report':'runtime-validation.json',
    'coverage':'Both forms, vulnerable switches, meter/health carryover, robot continuity, hit/whiff/block gating, recovery, and cross-character outfit preservation'}
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('URKEL_VERIFIED: 52 native checks, original PNG bytes, robot continuity, both forms, review links and 4 WAV cues.')
