"""Install original creator character data, without reskinning or moveset changes."""
from pathlib import Path
import hashlib,json,shutil,re
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';E=S/'engine/ikemen-go-v1.0.0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for slug,dirname,definition in [('naruto','Naruto_JUS2','Naruto_JUS2.def'),('saitama','Saitama','Saitama.def')]:
 f=S/'characters'/slug;source=f/'source/upstream'/dirname;out=E/'chars'/slug
 assert not out.exists() or (f/'import-report.json').exists(),('Unregistered existing fighter',slug)
 out.mkdir(exist_ok=True);files={}
 for p in source.rglob('*'):
  if not p.is_file():continue
  relative=p.relative_to(source);target=out/relative;target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert sha(target)==sha(p),('Existing file modified',target)
  else:shutil.copy2(p,target)
  files[relative.as_posix()]=sha(p)
 alias=slug+'.def';shutil.copy2(source/definition,out/alias)
 de=(source/definition).read_text(encoding='cp1252');author=re.search(r'(?im)^author\s*=\s*"([^"]+)"',de)[1]
 report=dict(status='Imported original MUGEN files; native verification pending',slug=slug,creator=author,source=json.loads((f/'source/source-report.json').read_text()),source_files_sha256=files,definition_alias=alias,definition_alias_sha256=sha(out/alias),modifications=['A byte-identical definition alias matching the engine folder name'],artwork='Original MUGEN artwork, animation and voices. No illustrated replacements generated or installed.',gameplay='Original creator command routes, states, damage, forms and timing retained.')
 (f/'import-report.json').write_text(json.dumps(report,indent=2));print('MUGEN_IMPORTED',slug,author,len(files),flush=True)
