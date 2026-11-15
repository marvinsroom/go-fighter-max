"""One-time migration: retain build inputs and move history out of the character."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/jinwoo';A=R/'sprite-fighter/archive/jinwoo/previous'
assert not A.exists(),'History has already been migrated'
A.mkdir(parents=True)
moved=[]
def move(src,dst):
    src=src.resolve();dst=dst.resolve()
    assert src.is_relative_to(R) and dst.is_relative_to(R) and not dst.is_relative_to(src),(src,dst)
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.move(str(src),str(dst));moved.append({'from':str(src.relative_to(R)),'to':str(dst.relative_to(R))})

registration=json.loads((S/'source/project-v5/build-report.json').read_text())['sprites']
active={}
for key,entry in registration.items():
    if key.startswith('sheet_'):continue
    m=dict(entry);old=R/m['file'];wardrobe=S/'art/white-shirt-v9'/old.name
    if not key.startswith(('igris','beru','iron','tank')):
        assert wardrobe.exists(),key
        new=S/'art/daggers'/old.name
    else:
        new=S/'art/forms-v6'/(key.rsplit('_',1)[0]+'-assist.png')
        if not new.exists():shutil.copy2(old,new)
        new=S/'art/shadows'/new.name
    m['file']=str(new.relative_to(R));active[key]=m
(S/'source/art-registration.json').write_text(json.dumps({'sprites':active},indent=2))
(S/'validation/source-files.json').write_text(json.dumps(json.loads((S/'import-report.json').read_text())['original_files'],indent=2))
shutil.copy2(S/'hybrid-build-report.json',S/'validation/build.json')
move(S/'art/white-shirt-v9',S/'art/daggers')
move(S/'art/forms-v6',S/'art/shadows')
for name in ('v1','v2','references','README.md'):move(S/'art'/name,A/'art'/name)
for name in ('core-draft.png','core-layout-draft.png','README.md'):move(S/'art/daggers'/name,A/'art/daggers'/name)
move(S/'art/shadows/README.md',A/'art/shadows/README.md')
for path in list((S/'source').iterdir()):
    if path.name not in ('upstream','source-report.json','art-registration.json'):move(path,A/'source'/path.name)
for path in list((S/'replays').iterdir()):
    if path.name!='current':move(path,A/'replays'/path.name)
for path in list(S.iterdir()):
    if path.is_file():move(path,A/path.name)
(A.parent/'migration.json').write_text(json.dumps(moved,indent=2))
print('ARCHIVED',len(moved),'items to',A)
