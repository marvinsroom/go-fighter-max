"""Export source group thumbnails for the illustrated replacement audit."""
from pathlib import Path
from collections import defaultdict
from PIL import Image,ImageDraw
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/ichigo'
source=Sff(S/'source/upstream/Ichigo/Ichigo.sff');groups=defaultdict(list)
for i,h in enumerate(source.headers):groups[h[0]].append(i)
items=sorted(groups.items())
for page in range((len(items)+47)//48):
 im=Image.new('RGB',(1440,1080),'#273344');d=ImageDraw.Draw(im)
 for j,(g,ids) in enumerate(items[page*48:(page+1)*48]):
  x=(j%8)*180;y=(j//8)*180;d.text((x+4,y+3),f'{g} ({len(ids)})',fill='white')
  for k,index in enumerate([ids[0],ids[len(ids)//2],ids[-1]]):
   sprite=source.decode(index);sprite.thumbnail((58,150))
   im.paste(sprite,(x+k*60,y+23+(150-sprite.height)//2),sprite)
 im.save(S/f'reference/source-groups-{page}.jpg')
print('AUDITED',len(items),'groups')

# Review small mixed-bank sprites rejected as actors by the new compiler.
from ichigo_illustrated import actor_form
excluded=[i for i,h in enumerate(source.headers) if h[0] in (23000,23001,23002,23003) and h[2]<=220 and h[3]<=150 and actor_form(source,h[:2]) is None]
for page in range((len(excluded)+79)//80):
 im=Image.new('RGB',(1200,1000),'#273344');d=ImageDraw.Draw(im)
 for j,index in enumerate(excluded[page*80:(page+1)*80]):
  h=source.headers[index];x=j%10*120;y=j//10*125;d.text((x+3,y+3),f'{h[0]},{h[1]}',fill='white')
  sprite=source.decode(index);sprite.thumbnail((115,100));im.paste(sprite,(x,y+20),sprite)
 im.save(S/f'reference/mixed-fx-audit-{page}.jpg')
print('SMALL_MIXED_FX',len(excluded))
