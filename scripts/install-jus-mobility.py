"""Install the roster-wide illustrated JUS size/mobility pass, with immutable backups.

Does not redraw sprites or relabel historical animation tests as current proof.
"""
from pathlib import Path
import json,re,hashlib,shutil

R=Path(__file__).resolve().parents[1]
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
O=R/'sprite-fighter/jus-upgrade'
O.mkdir(exist_ok=True)

def backup(path):
    dest=O/'before'/path.relative_to(E)
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,dest)
    return dest

def patch_definition(path,width,flight):
    original=backup(path).read_bytes().decode('cp1252')
    coord=f'localcoord = {width},{width*.75:g}'
    if re.search(r'(?im)^\s*localcoord\s*=',original):
        text=re.sub(r'(?im)^\s*localcoord\s*=.*$',coord,original)
    else:
        text=re.sub(r'(?im)^\[Info\]',lambda m:m[0]+'\n'+coord,original,count=1)
    assert not re.search(r'(?im)^\[Map\]',text),path
    text+='\n; Illustrated JUS movement layer; original artwork and native moves retained.\n[Map]\njus.enabled = 1\njus.flight_allowed = '+str(int(flight))+'\n'
    path.write_bytes(text.encode('cp1252'))

def install():
    profiles=json.loads((R/'sprite-fighter/face-audit/identity-scale-v5/profiles.json').read_text())['fighters']
    rows=[]
    for p in profiles:
        width=round(p['localcoord_width']/0.6)
        flight=p['slug'] in ('goku','gt-goku','ichigo','rimuru','jin-mori')
        rows.append(dict(slug=p['slug'],engine=p.get('roster_entry',p['engine']),definition='jinwoo.def' if p['slug']=='jinwoo' else p['definition'],old_width=p['localcoord_width'],width=width,flight=flight,height_cm=p['height_cm'],target_world_height=p['target_neutral_world_height']*p['localcoord_width']/width))
        paths=[E/'chars'/p['engine']/p['definition']]
        if p['slug']=='jinwoo':paths.append(E/'chars/jinwoo/jinwoo.def')
        for path in paths:
            assert path.exists(),path
            # Archive all referenced author data, excluding old test fixtures and large unchanged art.
            for file in path.parent.iterdir():
                if file.suffix.lower() in ('.cns','.cmd','.zss','.air','.def') and not any(x in file.name for x in ('test','controls','stature','target')):backup(file)
            patch_definition(path,width,flight)
    # Both imported originals are normalized to the same cm scale, rather than
    # blindly shrinking the already-small Naruto by another 40 percent.
    for slug,width,height,old,neutral in [('naruto',328,166,320,50),('saitama',404,175,180,65)]:
        path=E/'chars'/slug/(slug+'.def')
        for file in path.parent.iterdir():
            if file.suffix.lower() in ('.cns','.cmd','.air','.def') and not any(x in file.name for x in ('test','controls','target')):backup(file)
        patch_definition(path,width,False)
        rows.append(dict(slug=slug,engine=slug,definition=slug+'.def',old_width=old,width=width,flight=False,height_cm=height,target_world_height=neutral*320/width,height_evidence='Approximate visual scale; preserves source stance'))
    for name in ('config.ini',):
        path=E/'save'/name
        text=backup(path).read_text(encoding='utf-8')
        text=re.sub(r'(?im)^(States\s*=.*)$',lambda m:m[0]+', data/jus-mobility.cns',text,count=1)
        text=re.sub(r'(?im)^(Cmd\s*=.*)$',lambda m:m[0]+', data/jus-mobility.cmd',text,count=1)
        path.write_text(text,encoding='utf-8')
    queue=R/'sprite-fighter/anime-import-queue.json'
    data=json.loads(queue.read_text())
    data['artwork_stage']='New-character art and Gojo remain on hold. Confirmed: retain illustrated artwork, JUS size/motion/environment upgrade across all 28 authored playable fighters.'
    queue.write_text(json.dumps(data,indent=2)+'\n')
    report=dict(status='Implementation in progress',scope='All 28 authored playable fighters and their existing forms',art_policy='Retain current illustrations and identity; new anime art remains on hold',world_units_per_cm=.3,fighters=rows,animation_status='Existing drawings retained; new animation work pending',validation_status='Native mobility and combat checks pending')
    (O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    memory='\n\n## Confirmed illustrated JUS upgrade — 2026-10-21\nUser confirmed option 1 (KEEP current illustrated art) and WHOLE playable roster (28 authored entries). Compact JUS-like size, fluid combat animation, aerial movement/pursuit, flight where appropriate, and environment reactions. New-character work including Gojo/style conversion is ON HOLD. Supersedes earlier JUS cancellation for size/motion only. Immutable text backups and current work: sprite-fighter/jus-upgrade/. Native validation and additional animation work remain pending; do not claim complete from old face/stature evidence.\n'
    with (R/'PROJECT_MEMORY.md').open('ab') as f:f.write(memory.encode('utf-8'))
    print('Installed compact definitions for',len(rows),'fighters; native checks pending.')

if __name__=='__main__':install()
