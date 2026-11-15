"""Give the existing training arena room for real aerial fights, with rollback data."""
from pathlib import Path
import re,json,shutil
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/jus-upgrade'
p=E/'stages/stage0-720.def';b=O/'before/stages/stage0-720.def';b.parent.mkdir(parents=True,exist_ok=True)
if not b.exists():shutil.copy2(p,b)
text=b.read_bytes().decode('cp1252')
values={'boundleft':'-700','boundright':'700','boundhigh':'-1000'}
for key,value in values.items():text=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,text,count=1)
settings={'autozoom':'1','autocenter':'1','lowestcap':'1','startzoom':'1','zoomin':'1','zoomout':'.55','tensionhigh':'480','tensionlow':'40','zoomoutspeed':'1','zoominspeed':'.35','zoomindelay':'20','yscrollspeed':'.9'}
camera='\n; Illustrated JUS aerial framing; both high and low fighters stay visible.\n'+''.join(k+' = '+v+'\n' for k,v in settings.items())
text=re.sub(r'(?im)^\[Camera\]',lambda m:m[0]+camera,text,count=1)
# The grid must cover the larger camera range; keep the floor attached to
# the actors' ground plane instead of drifting under vertical camera motion.
parts=re.split(r'(?=^\[BG\s+\d+\])',text,flags=re.M|re.I)
for i,part in enumerate(parts):
 if re.match(r'\[BG\s+0\]',part,re.I):
  part=re.sub(r'(?im)^\s*;tile\s*=.*$','tile = 1,1',part,count=1);parts[i]=part
 elif re.match(r'\[BG\s+1\]',part,re.I):parts[i]=re.sub(r'(?im)^(delta\s*=\s*[^,]+,)\s*[^\r\n]+',r'\g<1> 1',part,count=1)
text=''.join(parts);p.write_bytes(text.encode('cp1252'))
(O/'arena-settings.json').write_text(json.dumps(dict(status='Installed; native ceiling/ground framing checks pending',camera=settings,bounds=values,grid='Tiled for expanded camera range',floor='Vertical delta 1 keeps the floor on the actor ground plane',reference='https://github.com/ikemen-engine/Ikemen-GO/wiki/Stage-features'),indent=2))
print('Training arena: aerial zoom, extended grid and ground-aligned floor installed.')
