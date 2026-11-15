"""Publish inspected face sheets while preserving prior artwork and proof."""
from pathlib import Path
import json,shutil,sys
R=Path(__file__).resolve().parents[1]
for slug in sys.argv[1:]:
 s=R/'sprite-fighter/characters'/slug;a=s/'art/illustrated-v1';new=s/'art/manhwa-faces-v2';backup=s/'archive/before-manhwa-faces-v2';backup.mkdir(parents=True,exist_ok=True)
 for name in ['build-report.json','runtime-validation.json','startup-ai-validation.json','viewer-validation.json','review.html','review-data.js','pose-registration.json']:
  if (s/name).exists() and not (backup/name).exists():shutil.copy2(s/name,backup/name)
 engine=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'/slug.replace('-','_')
 for file in engine.iterdir():
  if file.suffix in ('.def','.cns','.cmd','.air','.sff','.snd','.zss') and not (backup/file.name).exists():shutil.copy2(file,backup/file.name)
 requests=json.loads((a/'generation-requests.json').read_text());history=a/'generation-history.json';old=json.loads(history.read_text()) if history.exists() else []
 for kind in ('movement','combat','story','portrait'):
  assert (new/(kind+'.png')).exists()
  row=next(q for q in requests if q['file']==kind+'.png');old.append(dict(row,archived_candidate='../before-manhwa-faces-v2/'+kind+'.png',reason='Comic face and user-requested Gang Yong design correction'))
  for suffix in ('.png','.prompt.txt'):shutil.copy2(new/(kind+suffix),a/(kind+suffix))
  meta=json.loads((new/(kind+'.generation.json')).read_text());row.update(original_generated_file=meta['original_generated_file'],reference_images=meta['references'],selected_version='../manhwa-faces-v2/'+kind+'.png',prompt=kind+'.prompt.txt')
 history.write_text(json.dumps(old,indent=2));(a/'generation-requests.json').write_text(json.dumps(requests,indent=2));print('PUBLISHED',slug)
