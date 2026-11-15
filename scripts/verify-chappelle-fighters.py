"""Verify complete native reports, sprite bytes, form banks and review artifacts."""
from pathlib import Path
from PIL import Image
import hashlib,json,re,struct
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';CH=ROOT/'sprite-fighter/characters'
if (CH/'prince/paired-build-report.json').exists():
    import runpy
    runpy.run_path(str(ROOT/'scripts/verify-chappelle-pairs.py'),run_name='__main__')
    raise SystemExit
total=0;results={}
for slug,expected in [('prince',42),('negan',40),('rick',63)]:
    source=CH/slug;out=E/'chars'/slug
    build=json.loads((source/'build-report.json').read_text());runtime=json.loads((source/'runtime-validation.json').read_text());p1=json.loads((source/'player-one-validation.json').read_text())
    assert runtime['status']=='Complete' and runtime['passed']==expected and runtime['failed']==0,slug
    assert all(c['passed'] for c in runtime['checks'])
    assert p1['status']=='Complete' and len(p1['checks'])==(4 if slug=='rick' else 2) and all(c['passed'] for c in p1['checks']),slug
    cross=json.loads((source/'cross-validation.json').read_text())
    assert cross['status']=='Complete' and len(cross['checks'])==(3 if slug=='prince' else 2) and all(c['passed'] for c in cross['checks']),slug
    total+=expected+len(p1['checks'])+len(cross['checks'])
    archive=(out/(slug+'.sff')).read_bytes();offset,count=struct.unpack_from('<II',archive,36);start=struct.unpack_from('<I',archive,52)[0]
    entries={}
    for i in range(count):
        h=struct.unpack_from('<HHHHhhHBBIIHH',archive,offset+i*28);entries[h[0],h[1]]=h
    files=set()
    for key,m in build['sprites'].items():
        raw=(ROOT/m['file']).read_bytes();h=entries[m['group'],m['number']]
        assert hashlib.sha256(raw).hexdigest()==m['sha256'],(slug,key)
        assert archive[start+h[9]+4:start+h[9]+h[10]]==raw,(slug,key)
        with Image.open(ROOT/m['file']) as im:assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
        files.add(m['file'])
    assert len(files)==(18 if slug=='rick' else 9)
    for group in [50,51] if slug=='rick' else [50]:
        scales=[m['scale'] for m in build['sprites'].values() if m['group']==group];assert max(scales)==min(scales)
    banks=0
    if slug=='rick':
        text=(out/'rick.air').read_text();actions={int(m[1]):block for block in re.split(r'(?=\[Begin Action )',text) if (m:=re.match(r'\[Begin Action (\d+)\]',block))}
        def geometry(block):
            result=[]
            for line in block.strip().splitlines()[1:]:
                if re.match(r'^\d+,',line):
                    p=line.split(',');result.append(','.join(['DRAW']+p[2:7]+p[9:]))
                else:result.append(line)
            return result
        for n,block in actions.items():
            if n<10000:continue
            assert n-10000 in actions
            assert geometry(block)==geometry(actions[n-10000]),n
            assert re.search(r'^51,',block,re.M),n
            banks+=1
        assert banks>40,banks
    preview=json.loads((source/'native-preview-report.json').read_text())
    captured=sorted((source/'replays'/preview.get('capture_directory','native-v1')).glob('Chappelle_'+slug+'*.png'))
    assert len(captured)==len(preview['frames']) and len(captured)>120,(slug,len(captured),len(preview['frames']))
    moves=set(f['move'] for f in preview['frames'])
    for move in moves:
        with Image.open(source/(move+'-replay-v1.gif')) as im:assert im.n_frames>8,(slug,move)
    if slug=='rick':
        frames=[f for f in preview['frames'] if f['move']=='transformation']
        assert any(f['form']==1 and f['group']==51 for f in frames)
        assert any(f['tick']>190 and f['form']==0 and f['group']==50 for f in frames)
        for move in ['tyrone-reaction','tyrone-agent-capture']:
            assert all(f['group']==51 and f['form']==1 for f in preview['frames'] if f['move']==move and f['tick']>20),move
    result={'status':'Passed','native_combat_checks':expected,'player_one_checks':len(p1['checks']),'cross_capture_checks':len(cross['checks']),'failed':0,
      'lossless_png_payloads':len(files),'common_scale_per_form':True,'tyrone_animation_banks':banks,'native_replay_frames':len(captured),
      'engine_package_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob(slug+'.*')}}
    if slug=='rick':result['engine_package_sha256']['rick-common.cns.zss']=hashlib.sha256((out/'rick-common.cns.zss').read_bytes()).hexdigest()
    (source/'verification.json').write_text(json.dumps(result,indent=2));results[slug]=result
    build['status']='Native validated';build['validation']={'combat_passed':expected,'player_one_passed':len(p1['checks']),'failed':0}
    (source/'build-report.json').write_text(json.dumps(build,indent=2))
for slug,count in [('urkel',2),('jinwoo',4)]:
    r=json.loads((CH/'chappelle'/(slug+'-compat-validation.json')).read_text())
    assert r['status']=='Complete' and len(r['checks'])==count and all(c['passed'] for c in r['checks']),slug
    total+=count
compat=json.loads((CH/'chappelle/capture-compatibility.json').read_text())
assert hashlib.sha256((E/'chars/will_full/will.cns').read_bytes()).hexdigest()==compat['after_sha256']
assert set(compat['changed_victim_states'])=={820,821,1420,3050,3250,4550}
for slug in ['prince','negan','rick','chappelle']:
    for link in re.findall(r'(?:src|href)="([^"]+)"',(CH/slug/'review.html').read_text()):
        if link=='verification.json' and slug=='chappelle':continue
        assert (CH/slug/link).exists(),(slug,link)
for slug in ['prince','negan','rick']:assert any(line.split(',')[0].strip()==slug for line in (E/'data/select.def').read_text().splitlines())
assert total==166,total
result={'status':'Passed','native_checks':total,'new_fighter_combat_checks':145,'player_one_checks':8,'cross_capture_checks':7,'existing_form_regression_checks':6,'failed':0,'fighters':results}
(CH/'chappelle/verification.json').write_text(json.dumps(result,indent=2))
print('CHAPPELLE_VERIFIED',total,'native checks; 36 lossless PNGs; complete renderer replays')
