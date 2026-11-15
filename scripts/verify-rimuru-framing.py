"""Check native body extents and bounded attack effects against the viewport."""
import json,re,sys,hashlib
from pathlib import Path
import numpy as np
from mugen_sff import Sff
from rimuru_source import ROOT,SOURCE
C=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru'
r=json.loads((SOURCE/'runtime-validation.json').read_text());build=json.loads((SOURCE/'forms-build.json').read_text())
sff=Sff(C/'Rimuru Demon Lord.sff');air=(C/'Rimuru Demon Lord.air').read_text();actions={}
for block in re.split(r'(?=\[Begin Action\s+)',air,flags=re.I):
    m=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
    if not m:continue
    rows={}
    for line in block.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            p=line.split(';')[0].split(',');key=tuple(map(int,p[:2]));scale=float(p[7]) if len(p)>7 and p[7].strip() else 1
            rows[key]=(scale,-1 if len(p)>5 and 'H' in p[5] else 1)
    actions[int(m[1])]=rows
cache={};checks=[];failures=[];walk_seen=set()
target_sff=Sff(C.parent/'will_full/will.sff');target_actions={}
target_air=(C.parent/'will_full/hybrid-test.air').read_text(encoding='utf-8')
for block in re.split(r'(?=\[Begin Action\s+)',target_air,flags=re.I):
    m=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
    if not m:continue
    target_actions[int(m[1])]={}
    for line in block.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            p=line.split(';')[0].split(',');target_actions[int(m[1])][tuple(map(int,p[:2]))]=(float(p[7]) if len(p)>7 and p[7].strip() else 1,-1 if len(p)>5 and 'H' in p[5] else 1)
target_cache={};target_checks=0
for f in r['frames']:
    key=(int(f.get('group',-1)),int(f.get('drawing',-1)));anim=f['animation']
    if key not in sff.keys or key not in actions.get(anim,{}):continue
    if key not in cache:
        im=sff.decode(sff.keys[key]);bbox=im.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox();cache[key]=bbox
    bbox=cache[key];h=sff.headers[sff.keys[key]];scale,flip=actions[anim][key];render=scale*1.65
    # Lua screenPos uses the 320x240 screenpack basis (3px/unit at 720p),
    # while AIR drawing offsets use the character's 320-wide basis (4px/unit).
    x=[f['screen_x']*.75+(v-h[4])*render*f['facing']*flip for v in [bbox[0],bbox[2]]]
    y=[f['screen_y']*.75+(v-h[5])*render for v in [bbox[1],bbox[3]]]
    bounds=[min(x),min(y),max(x),max(y)];ok=bounds[0]>=-.6 and bounds[2]<=320.6 and bounds[1]>=-.6 and bounds[3]<=180.6
    row=dict(case=f['case_name'],tick=f['case_tick'],sprite=list(key),bounds=[round(v,2) for v in bounds],passed=ok)
    checks.append(row)
    if not ok:failures.append(row)
    if key[0]==8793:walk_seen.add(key[1])
    if f.get('fx_count',0):
        center=f['screen_x']*.75+f['fx_x']*f['facing']
        if center<39.4 or center>280.6:failures.append(dict(case=f['case_name'],tick=f['case_tick'],effect_center=center))
    tk=(int(f.get('target_group',-1)),int(f.get('target_drawing',-1)));ta=f.get('target_anim')
    # The fixture can begin with the target outside the safe visual margin.
    # Verify recoil from contact onward; setup frames precede the actual attack.
    contacted=f.get('target_life',999 if f['case_tick']>=60 else 1000)<1000
    if tk in target_sff.keys and tk in target_actions.get(ta,{}) and ' / ' in f['case_name'] and contacted:
        if tk not in target_cache:target_cache[tk]=target_sff.decode(target_sff.keys[tk]).getchannel('A').point(lambda a:255 if a>48 else 0).getbbox()
        tb=target_cache[tk];th=target_sff.headers[target_sff.keys[tk]];ts,tf=target_actions[ta][tk]
        tx=[f['target_screen']*4+(v-th[4])*ts*f['target_facing']*tf for v in [tb[0],tb[2]]];ty=[f['target_y']*4+(v-th[5])*ts for v in [tb[1],tb[3]]]
        target_checks+=1
        if min(tx)<-3 or max(tx)>1283 or min(ty)<-3 or max(ty)>723:failures.append(dict(case=f['case_name'],tick=f['case_tick'],victim_bounds=[round(min(tx),1),round(min(ty),1),round(max(tx),1),round(max(ty),1)]))
assert all(v['max_width']<=72.01 and v['max_height']<=84.01 for v in build['effects'].values())
for effect in build.get('cinematic_effects',{}).values():
    x,y=effect['anchor'];assert x-4-effect['width']*1.025/2>=0 and x+4+effect['width']*1.025/2<=320 and y-effect['height']*1.025>=0 and y<=180,effect
if walk_seen!=set(range(8)):failures.append(dict(walk_coverage=sorted(walk_seen),expected=list(range(8))))
out=dict(status='Passed' if not failures else 'Failed',method='Native 1280x720 training-stage captures. Actor alpha bounds on every recorded frame; victim bounds after contact; bounded effect dimensions and cast positions. Normal actor scales retained.',native_frames=len(checks),target_frames=target_checks,walk_drawings=sorted(walk_seen),failures=failures,checks=checks)
(SOURCE/'framing-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('RIMURU_FRAMING',len(checks),'body bounds and',target_checks,'victim bounds checked;',len(failures),'failures; walk cells',sorted(walk_seen))
for failure in failures[:12]:print(failure)
if failures:sys.exit(1)
