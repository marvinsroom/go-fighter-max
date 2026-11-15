"""Install the bespoke school-uniform to Bankai animation drawings."""
import io,json,hashlib
from PIL import Image
from isolated_sprite_atlas import extract

DURATIONS=[18,10,12,14,14,14,12,14,12,12,12,12,12,12,14,26]
REVEAL=sum(DURATIONS[:10])
LENGTH=sum(DURATIONS)

def install(folder,additions):
 art=folder/'art/school-intro-v4';poses=art/'poses';poses.mkdir(exist_ok=True)
 tiles=extract(art/'school-to-bankai.png',4,4)
 # Normalize all poses by the standing school figure, preserving crouches.
 manifest=[]
 for i,(image,bounds) in enumerate(tiles):
  blend=max(0,min(1,(i-7)/3))
  scale=220/((1-blend)*tiles[0][0].height+blend*tiles[15][0].height)
  image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
  image.save(poses/f'{i:02}.png');buffer=io.BytesIO();image.save(buffer,format='PNG')
  axis=(round(image.width*.48),image.height)
  additions[63200,i]=dict(image=image,png=buffer.getvalue(),axis=axis,rgba_sha256=hashlib.sha256(image.tobytes()).hexdigest())
  manifest.append(dict(frame=i,school_uniform=i<8,transformation=8<=i<10,bankai=i>=10,ticks=DURATIONS[i],bounds=bounds,axis=axis))
 (art/'frames.json').write_text(json.dumps(dict(drawings=manifest,reveal_tick=REVEAL,duration=LENGTH),indent=2))
 action='\n[Begin Action 60100]\nClsn2Default: 1\nClsn2[0]=-10,-55,10,0\n'
 for i,ticks in enumerate(DURATIONS):action+=f'63200,{i},0,0,{ticks},,,.25,.25\n'
 # A separate pressure animation keeps charge-up timing independent.
 action+='\n[Begin Action 60102]\n63000,12,0,0,4,,AS100D256,.24,.24\n63000,13,0,0,4,,AS100D256,.24,.24\n'
 return action
