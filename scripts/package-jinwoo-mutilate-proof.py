"""Compare the standing reference and every new Mutilate pose at native scale."""
import json
from PIL import Image,ImageDraw
from jinwoo_mutilate_evidence import SOURCE

report=json.loads((SOURCE/'validation/proportions-native.json').read_text())
keys=['base:idle']+[f'base:mutilate_{i}' for i in range(8)]
labels=['Standing reference','Mutilate ready','Forward step','Twin thrust','Turning slash','Execution windup','Downward strike','Follow-through','Recovery']
montage=Image.new('RGB',(1440,900),(10,10,17));draw=ImageDraw.Draw(montage)
for i,(key,label) in enumerate(zip(keys,labels)):
    f=next(f for f in report['frames'] if f['key']==key and f['facing']==1)
    with Image.open(SOURCE/f['src']) as native:im=native.convert('RGB').resize((480,270),Image.Resampling.LANCZOS)
    x=i%3*480;y=i//3*300;montage.paste(im,(x,y));draw.text((x+8,y+278),label,fill='white')
montage.save(SOURCE/'mutilate-proportions-native-v15.png')
print('MUTILATE_PROOF standing reference and eight poses, same native camera and scale')
