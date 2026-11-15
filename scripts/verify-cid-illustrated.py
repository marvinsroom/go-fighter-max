"""Check derived artwork identity, source preservation and native test evidence."""
from pathlib import Path
import hashlib,io,json,re,struct
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/cid';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';C=E/'chars/cid_shadow';U=S/'source/upstream/.Cid'
port=json.loads((S/'port-report.json').read_text());build=json.loads((S/'illustrated-build-report.json').read_text())
for name,meta in port['original_files'].items():assert hashlib.sha256((U/name).read_bytes()).hexdigest()==meta['sha256'],name
assert hashlib.sha256((S/'source/cid-ryoumens-balanced.rar').read_bytes()).hexdigest()==port['source']['sha256']
assert (C/'Cid.snd').read_bytes()==(U/'Cid.snd').read_bytes()
for name in ['AI.cns','Cid common.cns']:assert (C/name).read_bytes()==(U/name).read_bytes(),name
for name,expected in [('Atomic.cns',3),('Skills.cns',10),('Fx.cns',5)]:
    original=(U/name).read_text(encoding='cp1252');derived=(C/name).read_text(encoding='utf-8')
    # Only visual scale assignments may differ; preserve every state, trigger,
    # hit definition, damage value, animation event and timing expression.
    strip=lambda value:re.sub(r'(?im)^scale\s*=.*$', '',value)
    assert strip(original)==strip(derived),name
    adapter=build['scale_adapters'][name]
    assert len(adapter['changes'])==expected,(name,adapter)
    assert hashlib.sha256((C/name).read_bytes()).hexdigest()==adapter['sha256'],name
def rows(path):
    out=[]
    for line in path.read_text(encoding='utf-8-sig',errors='replace').splitlines():
        if not re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',line):continue
        parts=[p.strip() for p in line.split(';',1)[0].split(',')]
        out.append(parts)
    return out
a,b=rows(U/'Cid.air'),rows(C/'Cid.air');assert len(b)==len(a)+8+(17 if build.get('summons') else 0)+build.get('garden',{}).get('air_rows',0)
assert [int(row[4]) for row in b[len(a):len(a)+8]]==[8,10,10,12,78,12,10,10]
assert all(row[:2]==['7900',str(i)] for i,row in enumerate(b[len(a):len(a)+8]))
for old,new in zip(a,b):
    assert old[:7]==new[:7]+['']*(len(old[:7])-len(new[:7])) or (old+['']*9)[:7]==(new+['']*9)[:7],(old,new)
    assert old[9:]==new[9:],(old,new)
    meta=build['replaced_sprite_keys'].get(','.join(new[:2]))
    if meta:
        assert all(abs(float(v)-meta['scale'])<1e-8 or float(v)==0 for v in new[7:9]),new
assert build['replaced_sprite_keys']['0,71']['pose']=='movement-b:2','Dash must use running anatomy, not a crouch'
assert build['replaced_sprite_keys']['40,0']['pose']=='movement-b:10','Airborne ascent must not use the takeoff crouch'
walk_order=[4,5,6,6,7,8,9,10,10,11]
assert [build['replaced_sprite_keys'][f'69,{i}']['pose'] for i in range(10)]==[f'movement-a:{i}' for i in walk_order]
from cid_illustrated import cells
registered,_=cells(R)
for key,anatomy in build['pose_anatomy'].items():
    assert abs(anatomy['scale']-registered[key]['scale'])<1e-8,key
for sheet,indices in [('movement-a',range(4,12)),('movement-b',range(2,12)),('combat',range(12))]:
    assert len({registered[f'{sheet}:{i}']['scale'] for i in indices})==1,sheet+' must use a fixed sequence scale'
for i in range(4,9):
    m=registered[f'cinematic:{i}'];assert abs((m['bounds'][3]-m['bounds'][1])*m['scale']-55)<1e-8
def collision(path):return [l.strip() for l in path.read_text(encoding='utf-8-sig',errors='replace').splitlines() if re.match(r'\s*Clsn',l,re.I)]
original_collision=collision(U/'Cid.air')
assert original_collision==collision(C/'Cid.air')[:len(original_collision)]
data=(C/'Cid.sff').read_bytes();offset,count=struct.unpack_from('<II',data,36);lo=struct.unpack_from('<I',data,52)[0]
assert hashlib.sha256(data).hexdigest()==build['runtime_sff_sha256']
for i in range(count):
    h=struct.unpack_from('<HHHHhhHBBIIHH',data,offset+i*28);key=f'{h[0]},{h[1]}'
    if key not in build['replaced_sprite_keys']:continue
    target=h
    while target[10]==0:target=struct.unpack_from('<HHHHhhHBBIIHH',data,offset+target[6]*28)
    assert target[7]==12 and target[8]==32
    with Image.open(io.BytesIO(data[lo+target[9]+4:lo+target[9]+target[10]])) as im:
        assert hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()==build['replaced_sprite_keys'][key]['rgba_sha256'],key
for filename,expected in [('runtime-validation.json',26),('runtime-anatomy-v3.json',10)]:
    report=json.loads((S/filename).read_text());assert report['passed']==expected and report['failed']==0,filename
    assert report['capture_directory'] in (('taunt-release-v3','scale-v5','summons-v1-combat-final','proportions-v6-combat','proportions-v6-final','garden-v1-combat') if expected==26 else ('anatomy-v3-final',)),filename
    assert all((S/'replays'/report['capture_directory']/f"Cid_reference{f['index']-1:03d}.png").exists() for f in report['frames']),filename
walk=json.loads((S/'runtime-walking-v4.json').read_text())
assert walk['passed']==4 and walk['failed']==0 and walk['capture_directory'] in ('walking-v4-final','proportions-v6-walking','garden-v1-walking')
for check in walk['checks']:
    expected='21' if check['name'].startswith('Backward') else '20'
    assert check['animations'].get(expected) and check['final_state']==0,check
for name in ['walk-forward-v4','walk-backward-v4']:
    with Image.open(S/f'{name}.gif') as im:assert im.n_frames>8
for name in ['movement','combat','atomic','all-range','final-atomic']:
    with Image.open(S/f'{name}.gif') as im:assert im.n_frames>4
select=(E/'data/select.def').read_text()
for slug in [*port['preserved_roster'],'cid_shadow']:assert re.search(r'^'+slug+r',',select,re.M),slug
page=(S/'review.html').read_text(encoding='utf-8')
for ref in re.findall(r'(?:src|href)="([^"]+)"',page):
    if ref.startswith(('http','#')):continue
    assert (S/ref.split('?')[0]).exists(),ref
from stable_body_scale import stabilize
body_keys={tuple(map(int,k.split(','))) for k in build['replaced_sprite_keys']}
_,remaining=stabilize((C/'Cid.air').read_text(),body_keys)
assert not remaining,'Player scale interpolation must not blend calibrated drawings'
build['status']='Verified: 26 combat regressions, 10 anatomy/taunt checks and 4 focused walking checks passed; player scale blending removed; original combat timing preserved'
(S/'illustrated-build-report.json').write_text(json.dumps(build,indent=2))
port['status']='Illustrated runtime installed and native verified; original resources preserved'
(S/'port-report.json').write_text(json.dumps(port,indent=2))
print('CID_ILLUSTRATED_VERIFIED: 40 native checks; both walk directions/recovery, original timing/collisions, calibrated anatomy, lossless RGBA sprites, taunt and review links')
