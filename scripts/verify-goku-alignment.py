"""Verify final portraits and native beam/projectile registration evidence."""
from pathlib import Path
from collections import defaultdict
import json, math, sys, hashlib
from mugen_sff import Sff

root=Path(__file__).resolve().parents[1]
kind=sys.argv[1]
folder=root/'sprite-fighter/characters'/kind
engine=root/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'/('goku' if kind=='goku' else 'gt_goku')
capture=sys.argv[2]
report=json.loads((folder/'replays'/capture/'validation.json').read_text())
build=json.loads((folder/'build-report.json').read_text())
assert report['status']=='Complete' and report['failed']==0
assert report['runtime_sha256']==build['runtime_sha256']
archive=Sff(engine/('Goku.sff' if kind=='goku' else 'GokuGT.sff'))
for number,size in ((0,(200,200)),(1,(960,1120))):
 image=archive.decode(archive.keys[9000,number])
 assert image.size==size
 bounds=image.getbbox();margin=round(min(size)*.08)
 assert bounds[0]>=margin-2 and bounds[1]>=margin-2 and bounds[2]<=size[0]-margin+2 and bounds[3]<=size[1]-margin+2,bounds
definition=(engine/('goku.def' if kind=='goku' else 'gt_goku.def')).read_text()
assert 'portraitscale=.125' in definition
shots=report['shots'];assert shots
beams=[s for s in shots if s['beam'] and s['emitting'] and s['age']>2]
flights=[s for s in shots if not s['beam']]
assert beams and flights and {s['facing'] for s in shots}=={-1,1}
# Engine screen positions use 4/3 display units per 320-local-coordinate unit
# on the installed 1280x720 stage. Physical positions below avoid camera drift.
errors=[max(abs(s['x']-s['root_x']-s['muzzle_x']*s['facing']*4/3),abs(s['y']-s['root_y']-s['muzzle_y']*4/3)) for s in beams]
assert max(errors)<1,('Beam detached from releasing palms',max(errors))
angles=[abs((s['angle']+math.degrees(math.atan2(s['vy'],s['vx']))+180)%360-180) for s in flights if s['vx']]
assert max(angles)<.1,('Projectile drawing does not follow velocity',max(angles))
groups=defaultdict(list)
for shot in flights:groups[(shot['case_name'],shot['id'])].append(shot)
drifts=[]
for samples in groups.values():
 for previous,current in zip(samples,samples[1:]):
  if current['age']<=previous['age'] or (current['vx'],current['vy'])!=(previous['vx'],previous['vy']):continue
  dx=current['px']-previous['px'];dy=current['py']-previous['py']
  vx=current['vx']*current.get('shot_facing',current['facing']);vy=current['vy']
  drift=abs(dx*vy-dy*vx)/max(.001,math.hypot(vx,vy))
  drifts.append(drift)
assert drifts and max(drifts)<.1,('Projectile left its launch line',max(drifts))
result=dict(status='Complete',character=kind,native_cases=report['passed'],beam_samples=len(beams),flight_samples=len(flights),trajectory_segments=len(drifts),max_hand_error=round(max(errors),5),max_angle_error=round(max(angles),5),max_trajectory_drift=round(max(drifts),5),facings=['left','right'],portrait_sizes=[[200,200],[960,1120]],evidence='replays/'+capture+'/validation.json',runtime_sha256=build['runtime_sha256'])
(folder/'alignment-validation.json').write_text(json.dumps(result,indent=2))
print('ALIGNMENT_VERIFIED',kind,result['native_cases'],'cases',len(beams),'beam samples',len(drifts),'trajectory segments')
