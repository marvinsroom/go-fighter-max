"""Build inspection boards from the saved packed drawings and native captures."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade';out=O/'visual-audit';out.mkdir(exist_ok=True)
cycles=[]
for row in json.loads((O/'manifest.json').read_text())['fighters']:
 folder=O/'art'/row['slug'];form=folder/'form-cycles-packing.json'
 if form.exists():
  for c in json.loads(form.read_text())['cycles']:cycles.append((row['slug']+' / '+c['label'],folder/'cycles'/str(c['source_group']),c))
 elif (folder/'packing.json').exists():cycles.append((row['slug'],folder,json.loads((folder/'packing.json').read_text())))
for start in range(0,len(cycles),8):
 group=cycles[start:start+8];board=Image.new('RGB',(1440,170*len(group)),(35,42,53));draw=ImageDraw.Draw(board)
 for row,(label,folder,packing) in enumerate(group):
  draw.text((8,row*170+3),label,fill='white')
  scale=min(130/max(f['size'][1] for f in packing['frames']),160/max(f['size'][0] for f in packing['frames']))
  for i,record in enumerate(packing['frames']):
   im=Image.open(folder/f'walk-{i:02d}.png').convert('RGBA');im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))))
   board.paste(im,(i*180+90-im.width//2,row*170+160-im.height),im)
 board.save(out/f'walks-{start//8+1}.jpg')
rows=json.loads((O/'manifest.json').read_text())['fighters'];board=Image.new('RGB',(1280,205*math.ceil(len(rows)/4)),(35,42,53));draw=ImageDraw.Draw(board)
for i,row in enumerate(rows):
 p=O/'native'/row['slug']/'current.json'
 if not p.exists():continue
 report=json.loads(p.read_text());frames=report.get('screenshots',[])
 if not frames:continue
 im=Image.open(R/frames[0]).convert('RGB').resize((320,180));x=(i%4)*320;y=(i//4)*205
 board.paste(im,(x,y+22));draw.text((x+4,y+3),row['slug'],fill='white')
board.save(out/'native-roster.jpg');print('Saved',len(cycles),'walk rows and',len(rows),'native panels to',out)
