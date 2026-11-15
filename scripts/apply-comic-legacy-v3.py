"""Replace human drawings losslessly, retaining original gameplay and form scale."""
from comic_identity_v3 import *
from isolated_sprite_atlas import extract
from mugen_sff import Sff
from PIL import Image
import io,json,hashlib,shutil,sys
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
def digest(image):return hashlib.sha256(image.tobytes()).hexdigest()
def frame(image,axis):
 b=io.BytesIO();image.save(b,format='PNG')
 return dict(image=image,png=b.getvalue(),axis=axis,rgba_sha256=digest(image))
for slug in [arg for arg in sys.argv[1:] if not arg.startswith('--')]:
 f=C/slug;art=f/'art/comic-identity-v3';data=json.loads((art/'runtime-templates.json').read_text());native=E/data['engine'];path=native/data['sff']
 reportpath=art/'installed.json'
 if '--refresh' not in sys.argv and reportpath.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==json.loads(reportpath.read_text())['sff_sha256']:
  print('ALREADY_INSTALLED',slug);continue
 sourcepath=path
 if hashlib.sha256(path.read_bytes()).hexdigest()!=data['baseline_sha256']:
  assert not reportpath.exists() or ('--refresh' in sys.argv and hashlib.sha256(path.read_bytes()).hexdigest()==json.loads(reportpath.read_text())['sff_sha256']),('Native source changed',slug)
  sourcepath=f/'archive/before-comic-identity-v3/runtime'/data['sff']
 assert hashlib.sha256(sourcepath.read_bytes()).hexdigest()==data['baseline_sha256'],('Native source changed',slug)
 replacements={};byhash={};preview=[]
 for page in data['pages']:
  tiles=extract(Path(page['destination']),page['columns'],page['rows'],count=page['count'])
  for i,((im,bounds),old) in enumerate(zip(tiles,page['frames'])):
   left,top,right,bottom=old['bounds'];factor=(bottom-top)/im.height
   im=im.resize((round(im.width*factor),bottom-top),Image.Resampling.LANCZOS)
   axis=(round((old['axis'][0]-left)/(right-left)*im.width),old['axis'][1]-top)
   byhash[old['rgba_sha256']]=dict(frame(im,axis),source_axis=old['axis'])
   preview.append(dict(keys=old['keys'],old_bounds=old['bounds'],size=im.size,axis=axis))
 backup=f/'archive/before-comic-identity-v3'
 if not backup.exists():
  backup.mkdir(parents=True);(backup/'runtime').mkdir()
  for x in native.iterdir():
   if x.suffix in ('.def','.cns','.cmd','.air','.snd','.zss','.sff'):shutil.copy2(x,backup/'runtime'/x.name)
  for n in ('review.html','build-report.json','runtime-validation.json','viewer-validation.json'):
   if (f/n).exists():shutil.copy2(f/n,backup/n)
 sff=Sff(sourcepath);cache={}
 # A matching raster must have identical dimensions. Avoid decoding unrelated
 # full-screen effect banks, particularly Jinwoo's large paletted sprites.
 body_sizes={tuple(old['size']) for page in data['pages'] for old in page['frames']}
 for key,index in sff.keys.items():
  header=sff.headers[index];actual=index
  while sff.headers[actual][10]==0:actual=sff.headers[actual][6]
  if tuple(sff.headers[actual][2:4]) not in body_sizes:continue
  if actual not in cache:cache[actual]=digest(sff.decode(actual))
  if cache[actual] in byhash:
   source=byhash[cache[actual]];replacement=source.copy()
   # Aliases can have distinct source axes. Retain their exact relative displacement.
   replacement['axis']=(source['axis'][0]+header[4]-source['source_axis'][0],source['axis'][1]+header[5]-source['source_axis'][1])
   replacements[key]=replacement
 portrait=Image.open(art/'portrait.png').convert('RGBA');portrait_hashes={};portrait_sizes=set()
 for key,index in sff.keys.items():
  if key[0]==9000:
   portrait_hashes[digest(sff.decode(index))]=True;portrait_sizes.add(tuple(sff.headers[index][2:4]))
 for key,index in sff.keys.items():
  h=sff.headers[index]
  if key[0]==9000 or (key[0]==0 and tuple(h[2:4]) in portrait_sizes and digest(sff.decode(index)) in portrait_hashes):
   box=sff.decode(index).getchannel('A').getbbox() or (0,0,*h[2:4])
   im=portrait.copy();im.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
   canvas=Image.new('RGBA',h[2:4]);canvas.alpha_composite(im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]));replacements[key]=frame(canvas,h[4:6])
 output=sff.derive(replacements,{})
 path.write_bytes(output);proof=Sff(path);assert proof.count==sff.count
 # Unchanged headers still address byte-identical original payload, including palettes.
 assert proof.data[proof.lo:proof.lo+sff.ls]==sff.data[sff.lo:sff.lo+sff.ls]
 for key,index in proof.keys.items():
  if key not in replacements:assert proof.headers[index]==sff.headers[sff.keys[key]],('Unrelated drawing changed',key)
 for x in (backup/'runtime').iterdir():
  if x.suffix!='.sff':assert x.read_bytes()==(native/x.name).read_bytes(),('Gameplay changed',x.name)
 nativehash={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (backup/'runtime').iterdir()}
 nativehash[data['sff']]=hashlib.sha256(output).hexdigest()
 report=dict(revision='comic-identity-v3',slug=slug,unique_body_drawings=len(byhash),replaced_sprite_keys=len(replacements),sff_sha256=hashlib.sha256(output).hexdigest(),baseline_sha256=data['baseline_sha256'],runtime_sha256=nativehash,unchanged_gameplay=True,scale_method='Each matching pose retains original visible height and root-axis displacement; no AIR/CNS changes.',poses=preview)
 reportpath.write_text(json.dumps(report,indent=2))
 print('COMIC_LEGACY_INSTALLED',slug,len(byhash),'bodies',len(replacements),'keys',flush=True)
