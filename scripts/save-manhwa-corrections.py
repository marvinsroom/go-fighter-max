"""Retain first-generation candidates and publish corrected built-in sheets."""
from pathlib import Path
import sys,json,shutil
ROOT=Path(__file__).resolve().parents[1]
for item in json.loads(Path(sys.argv[1]).read_text()):
 art=ROOT/'sprite-fighter/characters'/item['s']/'art/illustrated-v1';k=item['k'];candidate=art/'candidates';candidate.mkdir(exist_ok=True)
 requests_file=art/'generation-requests.json';requests=json.loads(requests_file.read_text());row=next(r for r in requests if r['file']==k+'.png')
 history=art/'generation-history.json';old=json.loads(history.read_text()) if history.exists() else []
 assert not (candidate/(k+'-v1.png')).exists(),('Correction already saved',item)
 shutil.copy2(art/(k+'.png'),candidate/(k+'-v1.png'));shutil.copy2(art/(k+'.prompt.txt'),candidate/(k+'-v1.prompt.txt'))
 old.append(dict(row,archived_candidate='candidates/'+k+'-v1.png',archived_prompt='candidates/'+k+'-v1.prompt.txt',reason='Layout/whole-body consistency correction'))
 original=Path(item['path']);assert original.exists();shutil.copy2(original,art/(k+'-v2.png'));shutil.copy2(original,art/(k+'.png'))
 (art/(k+'-v2.prompt.txt')).write_text(item['prompt'],encoding='utf-8');(art/(k+'.prompt.txt')).write_text(item['prompt'],encoding='utf-8')
 row.update(original_generated_file=str(original),reference_images=item['refs'],preserved_input='candidates/'+k+'-v1.png',selected_version=k+'-v2.png',prompt=k+'-v2.prompt.txt')
 history.write_text(json.dumps(old,indent=2),encoding='utf-8');requests_file.write_text(json.dumps(requests,indent=2),encoding='utf-8')
 print('CORRECTED',item['s'],k,flush=True)
