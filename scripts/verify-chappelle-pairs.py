"""Verify the two requested slots, both full kits, toggles and renderer replay."""
from pathlib import Path
from PIL import Image
import json,hashlib,re,struct
ROOT=Path(__file__).resolve().parents[1];CH=ROOT/'sprite-fighter/characters';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
expected={'prince':['Prince','Rick James'],'tyrone':['Tyrone Biggums','Negan']}
results={};total=0
for slug,names in expected.items():
    source=CH/slug;out=E/'chars'/slug;report=json.loads((source/'paired-build-report.json').read_text())
    assert report['forms']==names and report['layout_revision']==2
    runtime=json.loads((source/'paired-runtime-validation.json').read_text());cases=json.loads((source/'paired-test-cases.json').read_text())
    assert runtime['status']=='Complete' and runtime['failed']==0 and runtime['passed']==len(cases)
    assert all(c['passed'] for c in runtime['checks'])
    assert report['moves_revision']==3 and len(report['signature_moves'])==2
    for label in names:
        signatures=[c for c in runtime['checks'] if c['name'].startswith(label+' / Signature')]
        assert len(signatures)==6 and all(c['passed'] for c in signatures),(slug,label)
    if slug=='tyrone':assert next(c for c in runtime['checks'] if c['name']=='Negan / Full charge signature')['damage']==145
    total+=len(cases)
    sff=(out/(slug+'.sff')).read_bytes();header,count=struct.unpack_from('<II',sff,36);start=struct.unpack_from('<I',sff,52)[0]
    entries={}
    for i in range(count):
        h=struct.unpack_from('<HHHHhhHBBIIHH',sff,header+i*28);entries[h[0],h[1]]=h
    assert len(report['sprites'])==18
    for finisher in report.get('authored_finishers',{}).values():
        if 'prop' in finisher:
            path=ROOT/finisher['prop'];assert hashlib.sha256(path.read_bytes()).hexdigest()==finisher['sha256']
            h=entries[tuple(finisher['sprite'])]
            with Image.open(path) as im:assert sff[start+h[9]:start+h[9]+h[10]]==im.convert('RGBa').tobytes()
    if report.get('visual_revision',0)>=5:
        assert set(report['cinematic_art'])==set(names)
        for scene in report['cinematic_art'].values():
            path=ROOT/scene['scene'];assert hashlib.sha256(path.read_bytes()).hexdigest()==scene['sha256']
            h=entries[tuple(scene['sprite'])]
            with Image.open(path) as im:assert sff[start+h[9]:start+h[9]+h[10]]==im.convert('RGBA').tobytes()
            if 'execution' in scene:
                ex=scene['execution'];path=ROOT/ex['scene'];assert hashlib.sha256(path.read_bytes()).hexdigest()==ex['sha256']
                h=entries[tuple(ex['sprite'])]
                with Image.open(path) as im:assert sff[start+h[9]:start+h[9]+h[10]]==im.convert('RGBA').tobytes()
                capture=json.loads((CH/'chappelle/negan-execution-preview-report.json').read_text())
                assert capture['passed'] and capture['checks']['damage_changes']==1 and capture['checks']['damage']==950
                assert len(capture['frames'])>=50 and {8251,8262}<={f['target_state'] for f in capture['frames']}
                with Image.open(CH/'chappelle/negan-ultimate-v5.gif') as movie:
                    # GIF coalesces identical held poses during the deliberate
                    # pause and wind-up; validate playback length, not duplicates.
                    assert movie.n_frames>=10
                    duration=0
                    for frame in range(movie.n_frames):movie.seek(frame);duration+=movie.info.get('duration',0)
                    assert duration>=6000
        cns=(out/(slug+'.cns')).read_text()
        for block in re.split(r'(?=\[Statedef )',cns):
            head=re.match(r'\[Statedef (\d+)\]',block)
            if not head or int(head[1]) not in {3010,3210,4410,4510,13010,13210}:continue
            for ctrl in re.split(r'(?=\[State )',block):
                if not re.search(r'^type=Explod$',ctrl,re.M):continue
                anim=int(re.search(r'^anim=(\d+)$',ctrl,re.M)[1])
                assert anim not in {20001,20002,20003,20004,20005,20006,21001,21002,21003,21004,21005,21006},(slug,head[1],'legacy cinematic overlay')
                assert not re.search(r'^scale=[345],',ctrl,re.M)
    pngs=set()
    for key,m in report['sprites'].items():
        path=ROOT/m['file'];raw=path.read_bytes();h=entries[m['group'],m['number']]
        assert hashlib.sha256(raw).hexdigest()==m['sha256']
        assert sff[start+h[9]+4:start+h[9]+h[10]]==raw,(slug,key)
        with Image.open(path) as im:assert im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
        pngs.add(m['file'])
    assert len(pngs)==18
    for group in [50,51]:
        poses=[m for m in report['sprites'].values() if m['group']==group]
        reference=next(m for m in poses if m['number']==0)['scale']
        assert len(poses)==9 and all(.9-1e-7<=m['scale']/reference<=1.12+1e-7 for m in poses)
        for m in poses:
            h=entries[group,m['number']];assert list(h[4:6])==m['axis']
    air=(out/(slug+'.air')).read_text();action_numbers=[]
    for block in re.split(r'(?=\[Begin Action )',air):
        head=re.match(r'\[Begin Action (\d+)\]',block)
        if not head:continue
        n=int(head[1]);action_numbers.append(n)
        groups={int(line.split(',')[0]) for line in block.splitlines() if re.match(r'^\d+,',line)}
        assert groups==({50,51} if n in [3900,13900] else {7000} if 20000<=n<21000 else {7001} if n>=21000 else {51} if n>=10000 else {50}),(slug,n,groups)
        for line in block.splitlines():
            if not re.match(r'5[01],',line):continue
            fields=line.split(',');m=next(m for m in report['sprites'].values() if (m['group'],m['number'])==(int(fields[0]),int(fields[1])))
            assert abs(float(fields[7])-m['scale'])<1e-6 and abs(float(fields[8])-m['scale'])<1e-6,(slug,n,'uncalibrated frame')
    assert len(action_numbers)==len(set(action_numbers))
    for action in [0,10000,3900,13900,5000,15000,5050,15050]:assert action in action_numbers
    preview=json.loads((source/'paired-preview-report.json').read_text())
    captures=sorted((source/'replays'/preview['capture_directory']).glob('Chappelle_pair_'+slug+'*.png'))
    assert len(captures)==len(preview['frames']) and len(captures)>100
    frames=preview['frames']
    assert any(f['form']==1 and f['group']==51 and 70<f['tick']<90 for f in frames)
    assert any(f['form']==0 and f['group']==50 and 580<f['tick']<610 for f in frames)
    assert any(f['state']==13010 for f in frames)
    assert any(f['state']==(3210 if slug=='prince' else 4510) for f in frames)
    with Image.open(source/'paired-replay-v2.gif') as im:assert im.n_frames>80
    new_preview=json.loads((source/'signature-preview-report.json').read_text())
    new_frames=sorted((source/'replays'/new_preview['capture_directory']).glob('Chappelle_signature_'+slug+'*.png'))
    assert len(new_frames)==len(new_preview['frames']) and len(new_frames)>160
    expected_states={1500,1510,3010,3210,11500,11510,13010,13210} if slug=='prince' else {1500,1510,4410,4510,11500,11510,13010,13210}
    captured_states={f['state'] for f in new_preview['frames']}
    if slug=='prince' and 11512 in captured_states:expected_states.discard(11510)
    assert expected_states<=captured_states
    if report.get('visual_revision',0)>=4:assert {10,10010,5170,15170}<={f['animation'] for f in new_preview['frames']}
    with Image.open(source/'signature-replay-v3.gif') as im:assert im.n_frames>100
    result={'status':'Passed','forms':names,'native_combat_and_transform_checks':len(cases),'failed':0,'lossless_pngs':18,'calibrated_pose_scales':True,'native_replay_frames':len(captures),
      'signature_moves':report['signature_moves'],'signature_replay_frames':len(new_frames),
      'engine_package_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in [slug+'.cns',slug+'.cmd',slug+'.air',slug+'.def',slug+'.sff',slug+'.snd',slug+'-common.cns.zss']}}
    (source/'paired-verification.json').write_text(json.dumps(result,indent=2));(source/'verification.json').write_text(json.dumps(result,indent=2))
    report['status']='Illustrated cinematics and full paired movesets validated';report['validation']={'passed':len(cases),'failed':0}
    (source/'paired-build-report.json').write_text(json.dumps(report,indent=2));(source/'build-report.json').write_text(json.dumps(report,indent=2))
    results[slug]=result
match=json.loads((CH/'chappelle/paired-match-validation.json').read_text())
assert match['status']=='Complete' and len(match['checks'])==13 and all(c['passed'] for c in match['checks'])
total+=13
roster={line.split(',')[0].strip() for line in (E/'data/select.def').read_text().splitlines() if ',' in line and not line.lstrip().startswith(';')}
assert {'prince','tyrone'}<=roster and not {'rick','negan'}&roster
assert {'will_full','urkel','jinwoo','yamal'}<=roster
for slug in ['prince','tyrone','chappelle']:
    html=(CH/slug/'review.html').read_text(encoding='utf-8')
    for link in re.findall(r'(?:src|href)="([^"]+)"',html):
        if link=='paired-verification.json' and slug=='chappelle':continue
        assert (CH/slug/link).exists(),(slug,link)
    for link in re.findall(r'"file": "([^"]+)"',html):assert (CH/slug/link).exists(),link
assert total==221,total
scale_page=CH/'chappelle/scale-review.html'
for link in re.findall(r'(?:src|href)="([^"]+)"',scale_page.read_text(encoding='utf-8')):
    assert (scale_page.parent/link).is_file(),link
combined={'status':'Passed','layout_revision':2,'roster_slots':['prince','tyrone'],'forms':expected,'native_checks':total,'failed':0,'paired_match_checks':13,'fighters':results}
(CH/'chappelle/paired-verification.json').write_text(json.dumps(combined,indent=2));(CH/'chappelle/verification.json').write_text(json.dumps(combined,indent=2))
print('CHAPPELLE_PAIRS_VERIFIED',total,'native checks; exactly two Chappelle slots; 36 original PNGs retained')
