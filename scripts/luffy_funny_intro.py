"""Connected base-form meat gag for Luffy's pre-fight animation."""
from PIL import Image
from isolated_sprite_atlas import extract
import json

DURATIONS=[16,16,12,16,18,16,16,20,16,18,14,16,14,12,12,24]
LENGTH=sum(DURATIONS)

def install(folder,frames,poses):
 art=folder/'art/funny-intro-v2';tiles=extract(art/'intro.png',4,4)
 (art/'poses').mkdir(exist_ok=True)
 scale=264/tiles[15][0].height
 action='\n[Begin Action 60100]\nClsn2Default:1\nClsn2[0]=-12,-60,12,0\n'
 manifest=[]
 for i,(im,bounds) in enumerate(tiles):
  im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  im.save(poses/f'intro-{i}.png');im.save(art/'poses'/f'{i}.png');axis=(round(im.width*.5),im.height)
  frames.append(dict(key=(63200,i),image=im,axis=axis))
  action+=f'63200,{i},0,0,{DURATIONS[i]},,,.25,.25\n'
  manifest.append(dict(frame=i,ticks=DURATIONS[i],form=0,bounds=bounds,axis=axis))
 (art/'frames.json').write_text(json.dumps(dict(name='Funny meat intro',duration=LENGTH,starting_form=0,ending_form=0,drawings=manifest),indent=2))
 return action
