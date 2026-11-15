"""Preserve installed visual sources and native archives before body corrections."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
import json,shutil,hashlib
engine=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
for slug in SPECS:
    f=C/slug;out=f/'archive/before-comic-style-v4'
    if (out/'manifest.json').exists():
        print('Archived already',slug);continue
    out.mkdir(exist_ok=True,parents=True)
    art=f/'art/comic-identity-v3';target=out/'art';target.mkdir(exist_ok=True)
    for p in art.iterdir():
        if p.is_file() and (p.suffix in ('.png','.txt','.json')):shutil.copy2(p,target/p.name)
    native_id=PROFILES[slug]['id'] if slug in PROFILES else json.loads((art/'runtime-templates.json').read_text())['engine']
    runtime=out/'runtime';runtime.mkdir(exist_ok=True)
    for p in (engine/native_id).iterdir():
        if p.suffix in ('.sff','.air','.cns','.cmd','.snd','.zss','.def'):shutil.copy2(p,runtime/p.name)
    for name in ('review.html','build-report.json','runtime-validation.json','viewer-validation.json','comic-viewer-validation.json','animation-data.js','startup-validation.json'):
        if (f/name).exists():shutil.copy2(f/name,out/name)
    files={p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file()}
    (out/'manifest.json').write_text(json.dumps(dict(slug=slug,native_id=native_id,files=files),indent=2))
    print('ARCHIVED',slug,len(files),flush=True)
