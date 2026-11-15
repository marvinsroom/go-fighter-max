from manhwa_fighters import *
from PIL import Image,ImageDraw
import sys
p=profile(sys.argv[1]);S=p['folder'];r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and not r['failed'] and r['runtime_sha256']==json.loads((S/'build-report.json').read_text())['runtime_sha256']
frames=[f for f in r['frames'] if f['case_name']==p['moves'][-1] and f['state']==3001]
out=Image.new('RGB',(1920,300),(20,29,43));pen=ImageDraw.Draw(out)
for col,(tick,label) in enumerate([(34,'Opening field'),(66,'Rising impact'),(98,'Amplification'),(134,'Finishing release')]):
    f=min(frames,key=lambda f:abs(f.get('cinematic_tick',0)-tick));im=Image.open(S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']);im.thumbnail((480,270))
    out.paste(im,(col*480,30));pen.text((col*480+10,8),label,fill='white')
out.save(S/'art/illustrated-v1/native-ultimate-preview.png');print('MANHWA_CINEMATIC_CONTACT',p['name'])
