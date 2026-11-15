"""Verify source preservation, engine archives, army bounds and native results."""
from pathlib import Path
from PIL import Image
import hashlib,io,json,re,struct,wave
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'sprite-fighter/characters/jinwoo'
OUT=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo'
report=json.loads((SOURCE/'build-report.json').read_text())
sff=(OUT/'jinwoo.sff').read_bytes();assert len(sff)==report['sff_bytes']
header_start,count,_,_,data=struct.unpack_from('<IIIII',sff,36)
headers=[struct.unpack_from('<HHHHhhHBBIIHH',sff,header_start+i*28) for i in range(count)]
for key,item in report['sprites'].items():
    h=next(h for h in headers if h[:2]==(item['group'],item['number']))
    embedded=sff[data+h[9]+4:data+h[9]+h[10]]
    assert hashlib.sha256(embedded).hexdigest()==item['sha256'],key
    if 'source_rect' in item:
        with Image.open(ROOT/item['file']) as sheet:cell=sheet.crop(item['source_rect'])
        with Image.open(io.BytesIO(embedded)) as packed:
            assert packed.mode=='RGBA' and packed.tobytes()==cell.tobytes(),key
        assert hashlib.sha256(cell.tobytes()).hexdigest()==item['rgba_sha256']
    else:
        original=(ROOT/item['file']).read_bytes();assert embedded==original,key
    with Image.open(ROOT/item['file']) as im:assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0
    assert (ROOT/item['file']).with_suffix('.prompt.txt').is_file()
assert len(report['sprites'])==55
assert report['named_shadows']==['igris','beru','iron','tank']
for name,frames in [('walk',8),('dagger-cycle',8),('jump',8),('igris',4),('beru',4),('iron',4),('tank',4)]:
    assert report['motion_sheets'][name]['frames']==frames
    assert len({report['sprites'][f'{name}_{i}']['scale'] for i in range(frames)})==1
for number in range(14):
    h=next(h for h in headers if h[:2]==(0,number));assert h[10]==0 and headers[h[6]][0]==50
for item in report['army_framing']:
    l,t,r,b=item['bounds'];assert 40<=l<r<=1240 and 40<=t<b<=680
assert len(report['army_framing'])==48
snd=(OUT/'jinwoo.snd').read_bytes();assert snd[:12]==b'ElecbyteSnd\0'
sounds,offset=struct.unpack_from('<II',snd,16);assert sounds==4
for _ in range(sounds):
    nxt,size,group,number=struct.unpack_from('<IIII',snd,offset)
    with wave.open(io.BytesIO(snd[offset+16:offset+16+size])) as wav:assert wav.getnframes()>0
    offset=nxt
assert 'jinwoo-tests.cns' not in (OUT/'jinwoo.def').read_text()
for page in ['review.html','motion-review.html']:
    for relative in re.findall(r'(?:src|href)="([^"]+)"',(SOURCE/page).read_text(encoding='utf-8')):
        if '://' not in relative:assert (SOURCE/relative).is_file(),relative
native=json.loads((SOURCE/'runtime-validation.json').read_text())
assert native['status']=='Complete' and native['passed']==56 and native['failed']==0
for c in native['checks']:
    assert c['passed'] and not c['outfitViolations'] and c['armyMissing']==0 and c['armyLeak']==0,c
for name in ['Arise army ultimate','Agent captured by Arise']:
    c=next(c for c in native['checks'] if c['name']==name);assert c['armySeen']==1 and c['damage']==950
for name in ['Arise blocked','Arise needs meter','Dagger Tempest']:
    c=next(c for c in native['checks'] if c['name']==name);assert c['armySeen']==0
for i,(name,damage) in enumerate([('Igris',100),('Beru',110),('Iron',125),('Tank',115)]):
    c=next(c for c in native['checks'] if c['name']==name+' summon');assert c['damage']==damage and c['summon']==i
    repeat_casts=[c for c in native['checks'] if c['name'].startswith(name+' assigned repeat')]
    assert len(repeat_casts)==3 and all(c['summon']==i and c['damage']==damage for c in repeat_casts)
assert len(native['assignedSummons'])==4
for name,selection in [('Toward R selects Beru',1),('Away R selects Iron',2),('Down R selects Tank',3)]:
    c=next(c for c in native['checks'] if c['name']==name);assert c['summon']==selection
assert next(c for c in native['checks'] if c['name']=='Dagger Tempest')['damage']==620
assert next(c for c in native['checks'] if c['name']=='Tempest long-range catch')['damage']==620
assert next(c for c in native['checks'] if c['name']=='Arise full-screen catch')['damage']==950
assert report['revision']==3 and report['super']['confirmed_ticks']==240 and report['ultimate']['confirmed_ticks']==420
for name in ['Walk forward','Walk backward','Dagger check']:
    c=next(c for c in native['checks'] if c['name']==name);assert c['motionFrameCount']>=6
for name in ['Arise army ultimate','Agent captured by Arise']:
    c=next(c for c in native['checks'] if c['name']==name);assert all(v==1 for v in c['namedWaves'].values())
report['status']='Calibrated pose proportions, commanded shadows and overpowered finishers; 56 native checks passed'
report['native_validation']={'passed':56,'failed':0,'report':'runtime-validation.json'}
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('JINWOO_V3_VERIFIED: 56 native checks, assigned shadow moves, 620 super / 950 ultimate, original art, 48 screen bounds')
