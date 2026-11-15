"""Verify all seven actors, damage gates, actual blackout pixels and recovery."""
from pathlib import Path
import hashlib,json,re
import numpy as np
from PIL import Image
from mugen_sff import Sff
from cid_garden import art,MEMBERS

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/cid'
C=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/cid_shadow'
build=json.loads((S/'garden-build.json').read_text())
for name,digest in build['runtime'].items():
    assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,name
frames,meta=art(R);archive=Sff(C/'Cid.sff')
for key,m in frames.items():
    assert archive.decode(archive.keys[key]).tobytes()==m['image'].tobytes(),key
    assert tuple(archive.headers[archive.keys[key]][4:6])==tuple(m['axis']),key
for group in range(7922,7927):
    assert len({m['scale'] for key,m in frames.items() if key[0]==group})==1
air=(C/'Cid.air').read_text();states=(C/'cid_garden.cns').read_text()
for i,name in enumerate(MEMBERS):
    assert f'ID={7950+i}' in states
    for n in (7950+i*2,7951+i*2):
        block=re.search(r'(?im)^\[Begin Action '+str(n)+r'\][\s\S]*?(?=^\[Begin Action|\Z)',air)[0]
        assert 'Interpolate Scale' not in block
assert 'command=/$D,~x' in (C/'Cid.cmd').read_text()
assert 'removetime=24' in states and 'trigger1=time>=212' in states
assert 'trigger1=time>=265' in states,'Victim safety recovery'
for filename,expected in [('runtime-garden.json',6),('runtime-garden-preview.json',1)]:
    report=json.loads((S/filename).read_text())
    assert report['status']=='Complete' and report['passed']==expected and report['failed']==0,filename
    for name,digest in report['runtime'].items():
        assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,filename+' '+name
    for check in report['checks']:
        assert check['final_state']==0
        assert check['target_final_state'] not in (7929,7949)
        if check['name'].endswith(' hit'):
            assert check['damage']==520 and check['min_power']==0
            assert check['garden_actors']==[1]*7 and check['blackout']==1 and check['finish']==1
        elif check['name'].endswith(' blocked'):assert check['damage']==2 and not check['seen'].get('7921')
        elif check['name'].endswith((' misses',' interrupted')):assert check['damage']==0 and not check['seen'].get('7921')
        else:assert check['min_power']==(2999 if 'insufficient' in check['name'] else 0)
preview=json.loads((S/'runtime-garden-preview.json').read_text());assert len(preview['frames'])>=100
black=[];restored=[]
for row in preview['frames']:
    path=S/f"replays/{preview['capture_directory']}/Cid_reference{row['index']-1:03d}.png"
    with Image.open(path) as im:pixels=np.array(im.convert('RGB'))
    if row['blackout']:
        black.append(float(np.all(pixels<8,axis=2).mean()))
    elif row['case_tick']>330 and row['state']==0:
        restored.append(float(pixels.mean()))
assert len([ratio for ratio in black if ratio>.97])>=2,black
assert restored and min(restored)>20,'Arena must return after blackout'
build['status']='Verified: six team ultimate gates and one dense preview; all seven members, 520 damage, actual blackout and both-fighter recovery'
(S/'garden-build.json').write_text(json.dumps(build,indent=2))
print('CID_GARDEN_VERIFIED: 7 members; 520 damage; block/miss/meter/interruption gates; blackout pixels and recovery verified')
