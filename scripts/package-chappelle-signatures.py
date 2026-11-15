from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
for slug in ['prince','tyrone']:
    source=ROOT/'sprite-fighter/characters'/slug
    report=json.loads((source/'signature-preview-report.json').read_text())
    files=sorted((source/'replays'/report['capture_directory']).glob('Chappelle_signature_'+slug+'*.png'))
    assert len(files)==len(report['frames']) and len(files)>160,(slug,len(files))
    required={1500,1510,3010,3210,11500,11510,13010,13210} if slug=='prince' else {1500,1510,4410,4510,11500,11510,13010,13210}
    seen={row['state'] for row in report['frames']}
    if slug=='prince' and 11512 in seen:required.discard(11510) # Six-tick dive can fall between captures; its hit-only rebound proves the move.
    assert required<=seen,(slug,'missing move capture')
    records=list(zip(files,report['frames']))
    if report['capture_directory'].startswith(('proportions-','cinematics-')):
        assert {10,10010,5170,15170}<={row['animation'] for row in report['frames']},(slug,'missing crouch/fall capture')
        # Skip test-reset frames before the requested form has been selected.
        # The kept frames remain untouched, with their original capture ticks.
        records=[(path,row) for path,row in records if row['form']==(0 if row['tick']<=1400 else 1)]
    execution_source=ROOT/'sprite-fighter/characters/chappelle/negan-execution-preview-report.json'
    if slug=='tyrone' and execution_source.exists() and not report['capture_directory'].startswith('cinematics-v6'):
        execution=json.loads(execution_source.read_text());assert execution['passed']
        execution_root=execution_source.parent/'replays'/execution['capture_directory']
        execution_files=sorted(execution_root.glob('Negan_execution*.png'))
        assert len(execution_files)==len(execution['frames'])
        start=next(row['tick'] for path,row in records if row['state']==13210)
        records=[(path,row) for path,row in records if row['tick']<start]
        initial=execution['frames'][0]['state_time']
        for path,row in zip(execution_files,execution['frames']):
            records.append((path,dict(row,form=1,tick=start+row['state_time']-initial,source_tick=row['tick'])))
        provenance={'method':'Unaltered native renderer frames; original signatures plus revised Negan execution',
                    'sources':['signature-preview-report.json','../chappelle/negan-execution-preview-report.json'],
                    'frames':[dict(row,file=str(path.relative_to(ROOT))) for path,row in records]}
        (source/'signature-replay-provenance.json').write_text(json.dumps(provenance,indent=2))
    frames=[]
    for path,row in records:
        with Image.open(path) as im:
            frame=im.convert('RGB');frame.thumbnail((720,405))
            frames.append(frame.quantize(colors=256,method=Image.Quantize.FASTOCTREE))
    ticks=[row for path,row in records];durations=[max(20,round((ticks[i+1]['tick']-row['tick'])*1000/60)) if i+1<len(ticks) else 300 for i,row in enumerate(ticks)]
    frames[0].save(source/'signature-replay-v3.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False)
    print('SIGNATURE_REPLAY',slug,len(frames),flush=True)
    if report['capture_directory'].startswith('cinematics-'):
        for form,name in enumerate(['prince','rick'] if slug=='prince' else ['tyrone','negan']):
            selected=[(p,r) for p,r in records if r['form']==form and r['state']==((3210 if slug=='prince' else 4510) if form==0 else 13210)]
            assert len(selected)>20,(name,'ultimate capture too short')
            movie=[]
            for path,row in selected:
                with Image.open(path) as im:
                    im=im.convert('RGB');im.thumbnail((720,405));movie.append(im.quantize(colors=256,method=Image.Quantize.FASTOCTREE))
            delays=[max(20,round((selected[i+1][1]['tick']-r['tick'])*1000/60)) if i+1<len(selected) else 200 for i,(p,r) in enumerate(selected)]
            movie[0].save(ROOT/f'sprite-fighter/characters/chappelle/{name}-ultimate-v5.gif',save_all=True,append_images=movie[1:],duration=delays,loop=0,optimize=False)
            print('ULTIMATE_REPLAY',name,len(movie),flush=True)
