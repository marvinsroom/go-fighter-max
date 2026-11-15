"""Give live Jinwoo a modest taller, broader adult silhouette."""
from pathlib import Path
import hashlib,json,re

R=Path(__file__).resolve().parents[1]
cns=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo/cns.cns'
out=R/'sprite-fighter/characters/jinwoo/size-fixes/adult-v2';out.mkdir(parents=True,exist_ok=True)
backup=out/'before.cns'
if not backup.exists():backup.write_bytes(cns.read_bytes())
raw=backup.read_text(encoding='utf-8')
updated,nx=re.subn(r'(?im)^(\s*xscale\s*=\s*)[-+.0-9]+',r'\g<1>1.18',raw,count=1)
updated,ny=re.subn(r'(?im)^(\s*yscale\s*=\s*)[-+.0-9]+',r'\g<1>1.20',updated,count=1)
assert nx==ny==1
cns.write_text(updated,encoding='utf-8')
report={'status':'Installed','xscale_before':1.0,'yscale_before':1.0,'xscale_after':1.18,'yscale_after':1.20,
        'intent':'Tall, lean adult calibration against 166 cm Shippuden Naruto; Jinwoo has no confirmed official height, so 180-183 cm is treated as a visual estimate.',
        'before_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'installed_sha256':hashlib.sha256(cns.read_bytes()).hexdigest(),
        'controllers_changed':False,'air_changed':False,'sprites_changed':False,'recording':False}
(out/'installation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
