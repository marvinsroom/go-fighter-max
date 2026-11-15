"""Copy completed built-in generations into the project and retain provenance."""
from pathlib import Path
import json,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
for item in json.loads(Path(sys.argv[1]).read_text()):
    art=ROOT/'sprite-fighter/characters'/item['s']/'art/illustrated-v1'
    original=Path(item['path']);assert original.exists()
    target=art/(item['k']+'.png')
    shutil.copy2(original,target)
    file=art/'generation-requests.json';requests=json.loads(file.read_text())
    row=next(r for r in requests if r['file']==target.name)
    row['original_generated_file']=str(original);row['reference_images']=item['refs']
    file.write_text(json.dumps(requests,indent=2),encoding='utf-8')
    print('SAVED',item['s'],item['k'])
