"""Separate clean casting bodies from independently animated magic effects."""
import hashlib,json,re
from pathlib import Path
from rimuru_source import SOURCE,ROOT
from rimuru_complete import load
from mugen_sff import Sff
import numpy as np

def install(out):
    out=Path(out);folder=SOURCE/'art/forms-v3'
    frames=load(folder,'clean-casters',2,[0,4])
    # Each row has its own body calibration; a raised arm never shrinks the body.
    heights=[]
    for reference in (0,4):
        pixels=np.array(frames[reference]['image']).astype('int16')
        hair=(pixels[:,:,3]>200)&(pixels[:,:,1]>110)&(pixels[:,:,2]>150)&(pixels[:,:,2]>pixels[:,:,0]+20)&(pixels[:,:,1]>pixels[:,:,0]+10)
        top=int(np.flatnonzero(hair.sum(axis=1)>=3)[0])
        heights.append(frames[reference]['image'].height-top)
    for i,f in enumerate(frames):f['scale']=50/heights[0 if i<4 else 1]
    sff=Sff(out/'Rimuru Demon Lord.sff')
    assert (8794,0) not in sff.keys,'Clean casting bodies already installed'
    extras={(8794,i):f for i,f in enumerate(frames)}
    (out/'Rimuru Demon Lord.sff').write_bytes(sff.derive({},extras))
    build=json.loads((SOURCE/'build-report.json').read_text())
    replacements={tuple(map(int,k.split(','))):{'combat:8':0,'combat:9':1,'combat:10':2,'combat:11':3}[v['pose']] for k,v in build['sprites'].items() if v['pose'] in ['combat:8','combat:9','combat:10','combat:11']}
    replacements.update({(8791,6):4,(8791,8):4,(8791,9):5,(8791,10):6})
    air=(out/'Rimuru Demon Lord.air').read_text();lines=[];changed=0
    for line in air.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            p=line.split(',');key=tuple(int(v.strip()) for v in p[:2])
            if key in replacements:
                i=replacements[key];p[:2]=['8794',str(i)]
                while len(p)<9:p.append('')
                p[7]=p[8]=f'{frames[i]["scale"]:.9f}';line=','.join(p);changed+=1
        lines.append(line)
    (out/'Rimuru Demon Lord.air').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    forms=json.loads((SOURCE/'forms-build.json').read_text())
    for i,f in enumerate(frames):
        meta=dict(scale=f['scale'],axis=list(f['axis']))
        forms['body_sprites'][f'8794,{i}']=meta
        forms['added_sprites'][f'8794,{i}']=dict(meta,rgba_sha256=f['rgba_sha256'])
    forms['art']['clean-casters.png']=hashlib.sha256((folder/'clean-casters.png').read_bytes()).hexdigest()
    forms['clean_casting']=dict(group=8794,frames=8,replaced_animation_rows=changed,separate_effects=True,reference_head_to_sole_pixels=heights,body_height=50)
    (SOURCE/'forms-build.json').write_text(json.dumps(forms,indent=2),encoding='utf-8')
    build['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.suffix in ('.def','.air','.cns','.cmd','.sff') and not p.name.startswith(('test-','rimuru_test'))}
    build['status']='Complete casting and effects built; native validation pending'
    (SOURCE/'build-report.json').write_text(json.dumps(build,indent=2),encoding='utf-8')
    print('RIMURU_CLEAN_CASTERS',changed,'animation rows; 8 complete bodies; separate effects')

if __name__=='__main__':install(ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru')
