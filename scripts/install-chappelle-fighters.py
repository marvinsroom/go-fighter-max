"""Install roster entries and launch shortcuts, preserving existing entries."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT/'sprite-fighter';E=GAME/'engine/ikemen-go-v1.0.0'
if (GAME/'characters/prince/paired-build-report.json').exists():
    import runpy
    runpy.run_path(str(ROOT/'scripts/install-chappelle-pairs.py'),run_name='__main__')
    raise SystemExit
select=E/'data/select.def';text=select.read_text()
labels={'prince':'Prince','negan':'Negan','rick':'Rick James'}
for slug,label in labels.items():
    if not any(line.split(',')[0].strip()==slug for line in text.splitlines()):text=text.replace('[Characters]','[Characters]\n'+slug+', stages/stage0-720.def, order=1',1)
    base='powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-chappelle-fighter.ps1" -Character '+slug
    for filename,options in [('Play '+label,'-Mode Play -AsPlayerOne'),('Play Will vs '+label,'-Mode Play'),('Fight CPU '+label,'-Mode CPU')]:
        (GAME/(filename+'.cmd')).write_text('@echo off\n'+base+' '+options+'\n')
select.write_text(text)
roster=ROOT/'design/roster.json';data=json.loads(roster.read_text())
ids={'chappelle_prince':'prince','chappelle_negan':'negan','chappelle_rick_james':'rick'}
for character in data['characters']:
    if character['id'] not in ids:continue
    slug=ids[character['id']];character['spritePackage']='sprite-fighter/engine/ikemen-go-v1.0.0/chars/'+slug
    character['playableStatus']='First playable; key poses, native combat and visual review'
    character['review']='sprite-fighter/characters/'+slug+'/review.html'
    if slug=='rick':character['forms']=['Rick James','Tyrone Biggums'];character['transformation']='W as P1, ] as P2; toggle, free, shared health/meter'
roster.write_text(json.dumps(data,indent=2)+'\n')
print('CHAPPELLE_ROSTER_INSTALLED',list(labels))
