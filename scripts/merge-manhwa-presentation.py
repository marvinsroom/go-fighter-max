from manhwa_fighters import *
import sys
p=profile(sys.argv[1]);S=p['folder'];baseline=json.loads((S/'validation'/sys.argv[2]).read_text());retake=json.loads((S/'runtime-validation.json').read_text())
assert baseline['status']==retake['status']=='Complete' and not baseline['failed'] and not retake['failed']
assert baseline['runtime_sha256']==retake['runtime_sha256'] and baseline['passed']>=66
(S/'validation'/sys.argv[3]).write_text(json.dumps(retake,indent=2));replace={c['name']:c for c in retake['checks']}
baseline['checks']=[replace.get(c['name'],c) for c in baseline['checks']]
frames=[]
for r in (baseline,retake):
    for f in r['frames']:
        if r is baseline and f['case_name'] in replace:continue
        frames.append(dict(f,capture_directory=f.get('capture_directory',r['capture_directory'])))
baseline['frames']=frames;baseline['presentation_retake']=dict(source=sys.argv[3],same_runtime=True,cases=sorted(replace))
(S/'runtime-validation.json').write_text(json.dumps(baseline,indent=2));(S/'validation/current.json').write_text(json.dumps(baseline,indent=2))
print('MANHWA_MERGED',p['name'],baseline['passed'],'checks',len(frames),'captures')
