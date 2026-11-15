"""Package native captures and the illustrated Cid review; never invent gameplay frames."""
from pathlib import Path
import json,html,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/cid'
r=json.loads((S/'runtime-validation.json').read_text())
assert r.get('failed')==0 and r.get('passed')==26,r.get('status')
folder=S/'replays'/r['capture_directory']
previews=[('movement','Ten-frame walk',80),('combat','Combo A',80),('jump','Jump and landing',100),('taunt','Hood taunt full meter',100),('atomic','Atomic confirmed',140),('all-range','All Range Atomic',140),('final-atomic','Final Atomic',140)]
if (S/'runtime-walking-v4.json').exists():previews += [('walk-forward-v4','Forward walk and idle',80),('walk-backward-v4','Backward walk and idle',80)]
for name,case,duration in previews:
    if '--review-only' in sys.argv:continue
    if '--walking-only' in sys.argv and not name.startswith('walk-'):continue
    if '--taunt-only' in sys.argv and name!='taunt':continue
    record=json.loads((S/'runtime-walking-v4.json').read_text()) if name.startswith('walk-') else json.loads((S/'runtime-anatomy-v3.json').read_text()) if name=='taunt' else r
    folder=S/'replays'/record['capture_directory']
    frames=[];ticks=[]
    for meta in record['frames']:
        if meta['case_name']!=case:continue
        path=folder/f"Cid_reference{meta['index']-1:03d}.png"
        if path.exists():
            with Image.open(path) as im:frames.append(im.convert('RGB').resize((768,432)).quantize(colors=192));ticks.append(meta['case_tick'])
    assert len(frames)>4,(case,len(frames))
    if name.startswith('walk-'):duration=[max(40,round((b-a)*1000/60)) for a,b in zip(ticks,ticks[1:])]+[120]
    frames[0].save(S/f'{name}.gif',save_all=True,append_images=frames[1:],duration=duration,loop=0,disposal=2)
# Keep the review layout separate from capture/GIF packaging so partial refreshes
# preserve the same player, controls and attribution.
import hashlib
cases={}
preview_owners={}
for filename,expected in [('runtime-summon-preview.json',2),('runtime-garden-preview.json',1)]:
    path=S/filename
    if path.exists():
        preview=json.loads(path.read_text());assert preview.get('failed')==0 and preview.get('passed')==expected
        preview_owners.update({frame['case_name']:filename for frame in preview['frames']})
for record_name in ['runtime-validation.json','runtime-walking-v4.json','runtime-summons-v1.json','runtime-garden.json','runtime-summon-preview.json','runtime-garden-preview.json']:
    record_path=S/record_name
    if not record_path.exists():continue
    record=json.loads(record_path.read_text(encoding='utf-8'))
    assert record.get('failed')==0,record_name
    for frame in record['frames']:
        if frame['case_name'] in preview_owners and record_name!=preview_owners[frame['case_name']]:continue
        source=f"replays/{record['capture_directory']}/Cid_reference{frame['index']-1:03d}.png"
        assert (S/source).is_file(),source
        cases.setdefault(frame['case_name'],[]).append({
            'src':source,'case_tick':frame['case_tick'],
            'state':frame['state'],'animation':frame['animation']})
groups={
    'Team ultimate':[name for name in cases if name.startswith('Seven Shadows ')],
    'Summon supers':[name for name in cases if name.startswith(('Alpha ','Beta '))],
    'Atomics':['Atomic confirmed','All Range Atomic','Final Atomic'],
    'Combat':['Combo A','Magic blast'],
    'Movement':['Idle reference','Ten-frame walk','Crouch','Jump and landing',
                'Forward dash','Forward jump proportions','Back jump proportions',
                'Forward walk and idle','Backward walk and idle',
                'Forward walk short release','Backward walk short release'],
    'Taunt':['Hood taunt full meter','Hood taunt empty meter','Hood taunt interrupted'],
}
groups={name:[case for case in names if case in cases] for name,names in groups.items() if names}
if 'Summon supers' in groups:
    groups['Summon supers'].sort(key=lambda name:(not name.endswith('super hit'),name.startswith('Beta ')))
if 'Team ultimate' in groups:groups['Team ultimate'].sort(key=lambda name:not name.endswith(' hit'))
assert set(cases)=={case for names in groups.values() for case in names}
revision=hashlib.sha256(json.dumps(cases,sort_keys=True).encode()).hexdigest()[:12]
summon_report=S/'runtime-summons-v1.json'
data={'revision':revision,'passed':r['passed'],'captureDirectory':r['capture_directory'],'walkingCapture':json.loads((S/'runtime-walking-v4.json').read_text())['capture_directory'],'summonPassed':json.loads(summon_report.read_text())['passed'] if summon_report.exists() else 0,'gardenPassed':json.loads((S/'runtime-garden.json').read_text())['passed'] if (S/'runtime-garden.json').exists() else 0,'cases':cases,'groups':groups}
(S/'review-data.js').write_text('window.CID_REVIEW = '+json.dumps(data,indent=2)+';\n',encoding='utf-8')
template=(ROOT/'scripts/templates/cid-review.html').read_text(encoding='utf-8')
(S/'review.html').write_text(template.replace('__REVISION__',revision),encoding='utf-8')
from fighter_review import write_review
write_review('cid',template.replace('__REVISION__',revision),data)
print('CID_REVIEW_PACKAGED',len(cases),'clips',sum(map(len,cases.values())),'native frames')
