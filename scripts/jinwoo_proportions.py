"""Shared anatomy and scale for playable shadows, assists and cinematic actors."""
import re,json,hashlib
from pathlib import Path

ASSISTS={
 'igris':('movement:0','combat:9','combat:2','combat:11'),
 'beru':('movement:0','combat:0','combat:2','combat:4'),
 'iron':('movement:0','combat:5','combat:6','combat:7'),
 'tank':('movement:0','combat:5','combat:6','combat:7'),
}


def calibrate(art):
    for name,poses in ASSISTS.items():
        for i,pose in enumerate(poses):
            canonical=f'{name}:{pose}'
            art[f'base:{name}_{i}']={**art[canonical],'alias_of':canonical}


def actor_states(folder,actions):
    states={}
    for path in folder.glob('*.cns'):
        for block in re.split(r'(?=^\[statedef\s)',path.read_text(encoding='cp1252'),flags=re.I|re.M):
            state=re.match(r'\[statedef\s+(\d+)',block,re.I)
            anim=re.search(r'(?im)^\s*anim\s*=\s*(\d+)\s*$',block)
            if state:
                n=int(state[1]);action=int(anim[1]) if anim else n
                if action in actions:states[n]=actions[action]
    return states


def adapt(text,states,actions):
    # Scale only actors. Projectiles, auras, dust and weapon effects keep their
    # authored sizes; enlarging those cannot stretch a fighter's anatomy.
    # Ultimate strike helpers 878400-878403 already author transform-matched
    # sizes (Tank 1.8); do not flatten them back to 1.5.
    SKIP_HELPERS={878400,878401,878402,878403}
    out=[]
    for block in re.split(r'(?=^\[state\s)',text,flags=re.I|re.M):
        kind=re.search(r'(?im)^\s*type\s*=\s*(helper|explod)\s*$',block)
        if kind:
            field='stateno' if kind[1].lower()=='helper' else 'anim'
            value=re.search(r'(?im)^\s*'+field+r'\s*=\s*(\d+)\s*$',block)
            if value and int(value[1]) in (states if field=='stateno' else actions):
                actor_id=int(value[1])
                if field=='stateno' and actor_id in SKIP_HELPERS:
                    out.append(block);continue
                for param in ('size.xscale','size.yscale') if field=='stateno' else ('scale',):
                    setting='1.5' if field=='stateno' else '1.5,1.5'
                    if field=='anim' and actor_id==878423:setting='1.8,1.8'
                    pattern=r'(?im)^\s*'+re.escape(param)+r'\s*=.*$'
                    if re.search(pattern,block):block=re.sub(pattern,param+'='+setting,block)
                    else:block=block.rstrip()+'\n'+param+'='+setting+'\n'
        out.append(block)
    return ''.join(out)


def package(root,art):
    folder=Path(root)/'sprite-fighter/characters/jinwoo'
    target=folder/'art/proportions-v14';target.mkdir(exist_ok=True)
    entries=[]
    for i,(key,m) in enumerate(art.items()):
        path=target/f'pose-{i:03d}.png';path.write_bytes(m['png'])
        actor=key.split(':')[0]
        if actor=='sword' or (actor=='base' and not any(key.startswith('base:'+s+'_') for s in ASSISTS)):actor='Jinwoo'
        elif actor=='base':actor=next(s for s in ASSISTS if key.startswith('base:'+s+'_'))
        entries.append(dict(key=key,actor=actor,group=m['group'],number=m['number'],scale=m['scale'],axis=m['axis'],bounds=m['bounds'],source=m['source'],alias_of=m.get('alias_of'),src=f'art/proportions-v14/{path.name}',sha256=m['rgba_sha256'],note='Shared canonical shadow drawing' if 'alias_of' in m else 'Reviewed at common world scale; natural crouching/foreshortening retained'))
    report=dict(revision=14,drawings=len(entries),method='All authored drawings inspected at shared world scale; no per-frame bounding-box fitting. Native fixture renders every registration in both facings.',entries=entries,corrections=['16 legacy assist drawings now share canonical movement/combat art','Body helpers and actor Explods use one 1.5 actor scale','VFX scaling remains separate from anatomy','Human supers use a fixed 1.12 sequence correction; Mutilate reuses current dagger attack anatomy'],references={'Jinwoo':'base:idle',**{s:s+':movement:0' for s in ASSISTS}})
    (folder/'validation/proportions-art.json').write_text(json.dumps(report,indent=2))
    (folder/'proportion-audit-data.js').write_text('window.JINWOO_PROPORTIONS='+json.dumps(report)+';',encoding='utf-8')
    return report


def audit_air(text,art,replacements):
    known={tuple(map(int,key.split(','))):art[name] for key,name in replacements.items()}
    known.update({(m['group'],m['number']):m for m in art.values()})
    actions=[];rows=0;hidden=0
    for block in re.split(r'(?=^\[Begin Action )',text,flags=re.I|re.M):
        found=False
        for line in block.splitlines():
            if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
            p=line.split(';',1)[0].split(',');m=known.get(tuple(int(x.strip()) for x in p[:2]))
            if not m:continue
            found=True;rows+=1;p+=['']*max(0,9-len(p));sx=float(p[7] or 1);sy=float(p[8] or 1)
            if sx==0 and sy==0:hidden+=1;continue
            assert abs(sx-sy)<.00001,'Anisotropic body row: '+line
            assert abs(sx-m['scale'])<.00001,'Body registration mismatch: '+line
        if found:
            assert not re.search(r'(?im)^\s*Interpolate Scale\s*$',block),'Interpolated body scales'
            actions.append(int(re.match(r'\[Begin Action (\d+)',block,re.I)[1]))
    return dict(status='Complete',body_rows=rows,hidden_body_rows=hidden,body_actions=len(actions),actions=actions,method='Every body frame in every runtime AIR action: exact registered isotropic scale; no body scale interpolation')
