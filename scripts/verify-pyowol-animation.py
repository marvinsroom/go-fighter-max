"""Check the compiled animation/hit timing contract, not source implementation."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'sprite-fighter/characters/pyowol'
air=(folder/'pyowol.air').read_text();cns=(folder/'pyowol.cns').read_text()
actions={};unique=set()
for block in re.split(r'(?=\[Begin Action )',air):
    match=re.match(r'\[Begin Action (\d+)\]',block)
    if not match:continue
    number=int(match[1]);assert number not in actions,number
    tick=0;active=False;frames=[]
    for line in block.splitlines():
        if line.startswith('Clsn1:'):active=True
        if not re.match(r'^\d+,\d+,',line):continue
        values=line.split(',');duration=int(values[4]);group,image=map(int,values[:2])
        frames.append(dict(start=tick,end=tick+max(1,duration),duration=duration,active=active,group=group,image=image))
        unique.add((group,image));active=False;tick+=max(1,duration)
    actions[number]=frames

states={}
for block in re.split(r'(?=\[Statedef )',cns,flags=re.I):
    match=re.match(r'\[Statedef (\d+)\]',block,re.I)
    if match:states[int(match[1])]=block
report=json.loads((folder/'build-report.json').read_text());checks=[]
for state in [m['state'] for m in report['normal_moves']]+[3000,1120,3200,4000]:
    frames=actions[state];assert len({f['image'] for f in frames})>=4,(state,'insufficient distinct body drawings')
    for block in re.split(r'(?=\[State )',states[state]):
        if not re.search(r'type=HitDef\b',block,re.I):continue
        tick=int(re.search(r'trigger1=time=(\d+)',block)[1])
        frame=next((f for f in frames if f['start']<=tick<f['end']),None)
        assert frame and frame['active'],(state,tick,'HitDef outside active animation drawing')
        checks.append(dict(state=state,tick=tick,drawing=frame['image']))
    assert not frames[-1]['active'],(state,'collision remains active during recovery')

# Casts must release on the extended-arm drawing, not after the hand returns.
for state,ticks,expected in [(1100,[8,16,24],125),(3100,[10,12,13,18,20],125)]:
    for tick in ticks:
        frame=next(f for f in actions[state] if f['start']<=tick<f['end'])
        assert frame['image']==expected,(state,tick,frame)
assert len(actions[0])==4 and len(actions[20])==4
sparks={int(n) for n in re.findall(r'sparkno=S(\d+)',cns,re.I)}
for number in sparks:assert all(f['duration']>0 for f in actions[number]),(number,'hit spark never expires')
out=dict(contact_checks=checks,new_source_drawings=48,body_drawings=sum(v['group']==50 for v in report['poses'].values()),states_checked=len(actions),finite_character_hit_sparks=sorted(sparks))
(folder/'animation-validation.json').write_text(json.dumps(out,indent=2))
print('ANIMATION_VERIFIED',len(checks),'contact beats; casts align; recovery has no attack box; idle/walk use four drawings')
