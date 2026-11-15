"""Native proof contact sheet for the two Endless Sky finishes."""
from baam_model import *
from PIL import Image,ImageDraw

r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and not r['failed']
assert r['runtime_sha256']==json.loads((S/'build-report.json').read_text())['runtime_sha256']
out=Image.new('RGB',(1920,600),(20,29,43));pen=ImageDraw.Draw(out)
for row,prefix in enumerate(('Base / ','Viole / ')):
    frames=[f for f in r['frames'] if f['case_name']==prefix+'Shinwonryu' and f['state']==3001]
    for col,(tick,label) in enumerate([(34,'Shinsu field'),(66,'Pillar / suspension'),(98,'Amplification'),(134,'Final discharge')]):
        f=min(frames,key=lambda f:abs(f.get('cinematic_tick',0)-tick))
        im=Image.open(S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']);im.thumbnail((480,270))
        x,y=col*480,row*300;out.paste(im,(x,y+30));pen.text((x+10,y+8),prefix+label,fill='white')
out.save(S/'art/combat-v3/native-ultimate-preview.png')
print('BAAM_CINEMATIC_CONTACT_SAVED')
