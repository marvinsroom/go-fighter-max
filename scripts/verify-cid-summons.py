"""Check new assist art, runtime hashes, native meter/guard/whiff cases."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
from mugen_sff import Sff
from cid_summons import art

R=Path(__file__).resolve().parents[1]
S=R/'sprite-fighter/characters/cid'
C=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/cid_shadow'
build=json.loads((S/'summon-build.json').read_text())
for name,digest in build['runtime'].items():
    assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,name
frames,meta=art(R);archive=Sff(C/'Cid.sff')
for key,frame in frames.items():
    assert archive.decode(archive.keys[key]).tobytes()==frame['image'].tobytes(),key
    assert tuple(archive.headers[archive.keys[key]][4:6])==tuple(frame['axis']),key
for group in (7911,7916):
    scales={frame['scale'] for key,frame in frames.items() if key[0]==group}
    assert len(scales)==1,'One body scale per sequence'
report=json.loads((S/'runtime-summons-v1.json').read_text())
assert report['status']=='Complete' and report['passed']==12 and report['failed']==0
checks={c['name']:c for c in report['checks']}
for name,damage,chip in [('Alpha',210,21),('Beta',195,18)]:
    assert checks[name+' super hit']['damage']==damage
    assert checks[name+' super blocked']['damage']==chip
    assert checks[name+' super misses']['damage']==0
    for suffix,meter in [('insufficient meter',999),('empty meter',0)]:
        check=checks[name+' super '+suffix]
        assert check['min_power']==meter and check['max_power']==meter
    assert checks[name+' super hit']['min_power']==2000
    interrupted=checks[name+' super interrupted']
    assert interrupted['suffered_hit'] and interrupted['final_state']==0 and interrupted['damage']==0
for row in report['frames']:
    path=S/f"replays/{report['capture_directory']}/Cid_reference{row['index']-1:03d}.png"
    with Image.open(path) as image:image.verify()
preview=json.loads((S/'runtime-summon-preview.json').read_text())
assert preview['status']=='Complete' and preview['passed']==2 and preview['failed']==0
for name,digest in preview['runtime'].items():
    assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,'Preview runtime '+name
for name in ('Alpha super hit','Beta super hit'):
    rows=[f for f in preview['frames'] if f['case_name']==name]
    # Super pause and hit pause can bridge several hook ticks without a new
    # rendered frame. Preserve their tick timestamps for accurate playback.
    assert len(rows)>=48 and all(b['case_tick']>a['case_tick'] for a,b in zip(rows,rows[1:]))
command=(C/'Cid.cmd').read_text(encoding='utf-8')
for name,direction in [('alpha','D'),('beta','B')]:
    assert f'name="cid_{name}"\ncommand=/${direction},y' in command
states=(C/'cid_summons.cns').read_text()
assert states.count('poweradd=-1000')==2
assert 'x=min(4,max(0,p2dist x-24))' in states
assert 'trigger2=time>=45' in states
native=json.loads((S/'runtime-validation.json').read_text())
assert native['status']=='Complete' and native['passed']==26 and native['failed']==0
for name,digest in native['runtime'].items():
    assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,'Native regression runtime '+name
build['status']='Verified: 12 summon checks and 26 native regressions passed'
(S/'summon-build.json').write_text(json.dumps(build,indent=2))
print('CID_SUMMONS_VERIFIED: Alpha 210/21, Beta 195/18; misses, meter gates, interruption, 16 fixed-scale poses and 26 native regressions passed')
