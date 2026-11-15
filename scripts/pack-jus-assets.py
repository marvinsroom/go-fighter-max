"""Pack reviewed raster sheets into native assets; retain original drawings verbatim."""
from pathlib import Path
import json,re,io,hashlib,shutil
from PIL import Image
from mugen_sff import Sff
from edward_assets import write_v2
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/jus-upgrade'

def backup(path):
 d=O/'before'/path.relative_to(E);d.parent.mkdir(parents=True,exist_ok=True)
 if not d.exists():shutil.copy2(path,d)
 return d

def walk(slug,engine,ratio,baselines):
 folder=O/'art'/slug;native=E/'chars'/engine;path=native/(engine+'.sff')
 source=backup(path);sff=Sff(source);frames=extract(folder/'walk.png',4,2)
 assert not any(g==64150 for g,i in sff.keys)
 additions={};records=[]
 # One fixed anatomical scale and root anchor for the ENTIRE cycle, not a
 # per-frame fit that stretches a passing pose to the contact pose's height.
 for i,(im,bounds) in enumerate(frames):
  im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)
  axis=(round(((i%4)*400+200-bounds[0])*ratio),round((baselines[i//4]-bounds[1])*ratio))
  buffer=io.BytesIO();im.save(buffer,format='PNG');png=buffer.getvalue()
  frame=dict(image=im,png=png,axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())
  additions[(64150,i)]=frame;im.save(folder/f'walk-{i:02}.png')
  records.append(dict(key=[64150,i],bounds=bounds,axis=axis,size=im.size,rgba_sha256=frame['rgba_sha256']))
 path.write_bytes(sff.derive({},additions))
 airpath=native/(engine+'.air');air=backup(airpath).read_text()
 for action,sequence in [(20,range(8)),(21,reversed(range(8)))]:
  old=re.search(r'(?ims)^\[Begin Action '+str(action)+r'\](.*?)(?=^\[Begin Action|\Z)',air)
  assert old,(action,airpath)
  collision='\n'.join(line for line in old[0].splitlines() if line.lower().startswith('clsn'))
  block=f'[Begin Action {action}]\n{collision}\n'+''.join(f'64150,{i},0,0,2,,,.125,.125\n' for i in sequence)+'\n'
  air=air[:old.start()]+block+air[old.end():]
 airpath.write_text(air)
 revision='comic-face-v6' if slug in ('eugene','jin-mu-won') else 'comic-identity-v3'
 meta=dict(status='Packed; native visual review pending',reference=f'sprite-fighter/characters/{slug}/art/{revision}/movement.png',prompt='walk.prompt.txt',source_sha256=hashlib.sha256((folder/'walk.png').read_bytes()).hexdigest(),anatomical_scale=ratio,root_anchor='Fixed x=200 in each 400px cell; shared row floor',original_sprites_preserved=True,actions=[20,21],distinct_drawings=8,frames=records)
 (folder/'packing.json').write_text(json.dumps(meta,indent=2))
 print(slug+': eight-frame walk packed, all previous sprites preserved.')

def environment():
 folder=O/'art/environment';image=Image.open(folder/'effects.png').convert('RGBA')
 # Reviewed manual gutters include all disconnected stones and dust fragments.
 xs=[0,340,695,1085,image.width];ys=[0,305,680,875,image.height];floor=[280,625,815,1030]
 sprites=[]
 for row in range(4):
  for col in range(4):
   box=(xs[col],ys[row],xs[col+1],ys[row+1]);im=image.crop(box)
   sprites.append(dict(key=(row,col),image=im,axis=((xs[col+1]-xs[col])//2,floor[row]-ys[row])))
 native=E/'data/jusfx';native.mkdir(exist_ok=True);write_v2(native/'jusfx.sff',sprites)
 (native/'jusfx.def').write_text('[Info]\nprefix=JS\nfx.scale=.16\nlocalcoord=320,240\n[Files]\nsff=jusfx.sff\nair=jusfx.air\n')
 air=''
 for group in range(3):
  air+=f'[Begin Action {group}]\n'+''.join(f'{group},{i},0,0,4\n' for i in range(4))+'\n'
 for i in range(4):air+=f'[Begin Action {100+i}]\n3,{i},0,0,-1\n\n'
 (native/'jusfx.air').write_text(air)
 cfg=E/'save/config.ini';text=cfg.read_text()
 if 'data/jusfx/jusfx.def' not in text:text=re.sub(r'(?im)^(Fx\s*=.*)$',lambda m:m[0]+', data/jusfx/jusfx.def',text)
 cfg.write_text(text)
 (folder/'packing.json').write_text(json.dumps(dict(status='Packed; native effect review pending',source_sha256=hashlib.sha256((folder/'effects.png').read_bytes()).hexdigest(),columns=xs,rows=ys,baseline=floor,fx_scale=.16,prompt='effects.prompt.txt'),indent=2))
 print('Environment: dust, debris, shockwave and persistent damage sprites packed.')

if __name__=='__main__':
 import sys
 if len(sys.argv)==1 or 'kim-dokja' in sys.argv:walk('kim-dokja','kim_dokja',.916,[484,965])
 if len(sys.argv)==1 or 'eugene' in sys.argv:walk('eugene','eugene',.94,[495,958])
 if len(sys.argv)==1 or 'jin-mu-won' in sys.argv:walk('jin-mu-won','jin_mu_won',.98,[487,947])
 if len(sys.argv)==1 or 'gang-ryong' in sys.argv:walk('gang-ryong','gang_ryong',.995,[482,953])
 if len(sys.argv)==1 or 'mok-gyeongwoon' in sys.argv:walk('mok-gyeongwoon','mok_gyeongwoon',.925,[497,975])
 if len(sys.argv)==1 or 'arthur' in sys.argv:walk('arthur','arthur',.84,[490,979])
 if len(sys.argv)==1 or 'cha-yeon-woo' in sys.argv:walk('cha-yeon-woo','cha_yeon_woo',.94,[494,963])
 if len(sys.argv)==1 or 'lloyd' in sys.argv:walk('lloyd','lloyd',.977,[497,960])
 if len(sys.argv)==1 or 'zhuo-fan' in sys.argv:walk('zhuo-fan','zhuo_fan',.87,[492,977])
 if len(sys.argv)==1 or 'environment' in sys.argv:environment()
