"""Expose exactly two Chappelle roster slots and archive obsolete shortcuts."""
from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT/'sprite-fighter';CH=GAME/'characters';E=GAME/'engine/ikemen-go-v1.0.0'
archive=CH/'chappelle/components-v1';archive.mkdir(parents=True,exist_ok=True)
for slug in ['prince','rick','negan']:
    dest=archive/slug;dest.mkdir(exist_ok=True)
    for name in ['review.html','CONTROLS.md','README.md']:
        if (CH/slug/name).exists() and not (dest/name).exists():shutil.copy2(CH/slug/name,dest/name)
for name in ['review.html','verification.json','HANDOFF.md']:
    if (CH/'chappelle'/name).exists() and not (archive/('layout-v1-'+name)).exists():shutil.copy2(CH/'chappelle'/name,archive/('layout-v1-'+name))
select=E/'data/select.def'
text='\n'.join(line for line in select.read_text().splitlines() if line.split(',')[0].strip() not in ['prince','rick','negan','tyrone'])+'\n'
text=text.replace('[Characters]','[Characters]\nprince, stages/stage0-720.def, order=1\ntyrone, stages/stage0-720.def, order=1',1);select.write_text(text)
legacy=archive/'launchers';legacy.mkdir(exist_ok=True)
for label in ['Rick James','Negan']:
    for prefix in ['Play ','Play Will vs ','Fight CPU ']:
        old=GAME/(prefix+label+'.cmd')
        if old.exists():
            dest=legacy/old.name
            if not dest.exists():old.rename(dest)
for slug,label in [('prince','Prince'),('tyrone','Tyrone')]:
    base='powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-chappelle-fighter.ps1" -Character '+slug
    for name,options in [('Play '+label,'-Mode Play -AsPlayerOne'),('Play Will vs '+label,'-Mode Play'),('Fight CPU '+label,'-Mode CPU')]:
        (GAME/(name+'.cmd')).write_text('@echo off\n'+base+' '+options+'\n')
(GAME/'Play Chappelle Pairs.cmd').write_text('@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-chappelle-fighter.ps1" -Character prince -AsPlayerOne -Opponent tyrone -Mode Play\n')
roster=ROOT/'design/roster.json';data=json.loads(roster.read_text());updated=[]
for c in data['characters']:
    if c['id']=='chappelle_rick_james':continue
    if c['id']=='chappelle_prince':
        c.update(name='Dave Chappelle: Prince / Rick James',forms=['Prince','Rick James'],spritePackage='sprite-fighter/engine/ikemen-go-v1.0.0/chars/prince',review='sprite-fighter/characters/prince/review.html',transformation='Prince <-> Rick James; W as P1, ] as P2; free toggle, shared health/meter')
        c['role']='Basketball trickster / funk pressure transformation';c['movesetDocument']='concepts/chappelle-paired-fighters.md'
    elif c['id'] in ('chappelle_negan','chappelle_tyrone'):
        c.update(id='chappelle_tyrone',name='Dave Chappelle: Tyrone Biggums / Negan',forms=['Tyrone Biggums','Negan'],spritePackage='sprite-fighter/engine/ikemen-go-v1.0.0/chars/tyrone',review='sprite-fighter/characters/tyrone/review.html',transformation='Tyrone Biggums <-> Negan; W as P1, ] as P2; free toggle, shared health/meter')
        c['role']='Rush fighter / bat range transformation';c['movesetDocument']='concepts/chappelle-paired-fighters.md'
    updated.append(c)
data['characters']=updated;roster.write_text(json.dumps(data,indent=2)+'\n')
print('CHAPPELLE_LAYOUT_INSTALLED: Prince / Rick James; Tyrone Biggums / Negan')
