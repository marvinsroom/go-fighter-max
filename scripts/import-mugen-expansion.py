"""Import staged creator archives without overwriting existing roster assets."""
from pathlib import Path
import json,hashlib,re,shutil,sys
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';Q=G/'mugen-expansion/queue.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads(Q.read_text(encoding='utf-8'))
preserve=G/'mugen-expansion'/d.get('preservation_snapshot','existing-roster-sha256.json')
if not preserve.exists():
 entries=[]
 for line in (E/'data/select.def').read_text().split('[Characters]',1)[1].splitlines():
  if line.startswith('['):break
  if line.strip() and not line.lstrip().startswith(';'):entries.append(line.split(',')[0].strip())
 saved={}
 for name in entries:
  folder=E/'chars'/name
  if folder.is_dir():
   saved[name]={p.relative_to(folder).as_posix():sha(p) for p in folder.rglob('*') if p.is_file()}
 preserve.write_text(json.dumps(saved,indent=2))
for row in d['fighters']:
 slug=row['slug']
 if sys.argv[1:] and slug not in sys.argv[1:]:continue
 f=G/'characters'/slug;up=f/'source/upstream'
 if not (f/'source/source-report.json').exists() or not up.exists():continue
 definitions=[p for p in up.rglob('*') if p.suffix.lower()=='.def' and re.search(r'(?im)^\s*sprite\s*=',p.read_text(encoding='cp1252',errors='replace')) and re.search(r'(?im)^\s*cns\s*=',p.read_text(encoding='cp1252',errors='replace'))]
 if len(definitions)!=1:
  row['status']='Select release definition';row['definition_candidates']=[p.relative_to(up).as_posix() for p in definitions];continue
 definition=definitions[0];source=definition.parent;out=E/'chars'/slug;reportpath=f/'import-report.json'
 if out.exists():
  assert reportpath.exists(),('Existing unregistered fighter',slug)
  continue
 out.mkdir();files={}
 for p in source.rglob('*'):
  if p.is_file():
   target=out/p.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);files[p.relative_to(source).as_posix()]=sha(p)
 alias=slug+'.def'
 if definition.name!=alias:shutil.copy2(definition,out/alias)
 text=definition.read_text(encoding='cp1252',errors='replace');author=re.search(r'(?im)^\s*author\s*=\s*([^;\r\n]+)',text)
 record=dict(status='Original MUGEN imported; native startup pending',slug=slug,name=row['name'],creator=author[1].strip().strip('"') if author else 'See upstream credits',definition=alias,original_definition=definition.name,source_files_sha256=files,source=json.loads((f/'source/source-report.json').read_text()),modifications=['Folder-name DEF alias only'] if definition.name!=alias else [],artwork='Original imported sprites, animations, sounds and gameplay; styling deferred')
 reportpath.write_text(json.dumps(record,indent=2));row.update(status=record['status'],creator=record['creator'],definition=alias,engine=slug)
 print('IMPORTED',slug,record['creator'],len(files),flush=True)
Q.write_text(json.dumps(d,indent=2),encoding='utf-8')
saved=json.loads(preserve.read_text())
for name,files in saved.items():
 for filename,digest in files.items():assert sha(E/'chars'/name/filename)==digest,('Existing fighter changed',name,filename)
print('PRESERVED',len(saved),'existing fighters')
