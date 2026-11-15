"""Install proportion redraws into current archives without rebuilding gameplay."""
from pathlib import Path
import json,hashlib,shutil,io,statistics,sys
from PIL import Image
from mugen_sff import Sff
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1];C=R/'sprite-fighter/characters';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars';J=R/'sprite-fighter/jus-upgrade/art'
def sha(b):return hashlib.sha256(b).hexdigest()
def frame(im,axis):
 b=io.BytesIO();im.save(b,format='PNG');return dict(image=im,png=b.getvalue(),axis=axis,rgba_sha256=sha(im.tobytes()))
for slug,engine in [('lloyd','lloyd'),('jin-mori','jin_mori')]:
 if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
 a=C/slug/'art/proportions-v9';n=E/engine;backup=a/'before';backup.mkdir(exist_ok=True)
 for p in n.iterdir():
  if p.suffix.lower() in ['.sff','.air','.cns','.cmd','.def','.zss','.snd'] and not (backup/p.name).exists():shutil.copy2(p,backup/p.name)
 sf=next(backup.glob('*.sff'));s=Sff(sf);replacements={};sheets={};canonical={};walkmeta={}
 if slug=='jin-mori':
  for page in json.loads((C/slug/'art/comic-identity-v3/runtime-templates.json').read_text())['pages']:
   canonical[page['kind']]=[tuple(f['keys'][0]) for f in page['frames']]
 else:
  canonical={kind:[(group,i) for i in range(16)] for kind,group in [('movement',62000),('combat',62400),('story',62600)]}
 jobs=json.loads((a/'requests.json').read_text(encoding='utf-8'))
 for job in jobs:
  kind=job['kind'];tiles=extract(a/(kind+'.png'),job['columns'],job['rows'],count=job['count']);out=a/'extracted'/kind;out.mkdir(parents=True,exist_ok=True)
  walk=kind.startswith('walk');packpath=None
  if walk:
   folder=J/slug if slug=='lloyd' else J/slug/'cycles'/('62000' if kind=='walk-base' else '62300')
   packpath=folder/'packing.json';meta=json.loads(packpath.read_text());(backup/(kind+'-packing.json')).write_text(json.dumps(meta,indent=2))
   keys=[tuple(f['key']) for f in meta['frames']]
  else:keys=canonical[kind]
  old=[s.decode(s.keys[k]) for k in keys]
  # One uniform raster scale per coherent sequence; never fit individual poses.
  factor=(statistics.median(im.height for im in old)/statistics.median(im.height for im,b in tiles)) if walk else old[0].height/tiles[0][0].height
  extra=old[4].height/tiles[4][0].height if slug=='lloyd' and kind=='story' else factor
  records=[]
  for i,((im,bounds),key) in enumerate(zip(tiles,keys)):
   f=extra if slug=='lloyd' and kind=='story' and 4<=i<=11 else factor
   im=im.resize((max(1,round(im.width*f)),max(1,round(im.height*f))),Image.Resampling.LANCZOS)
   h=s.headers[s.keys[key]];axis=(round(h[4]/old[i].width*im.width),im.height+(h[5]-old[i].height));v=frame(im,axis)
   replacements[key]=v;im.save(out/f'{i:02d}.png')
   if walk:im.save(folder/f'walk-{i:02d}.png')
   rec=dict(key=key,axis=axis,bounds=bounds,size=im.size,rgba_sha256=v['rgba_sha256'],scale=f);records.append(rec)
   # Replace all existing raster aliases, retaining their root displacements.
   if not walk:
    digest=sha(old[i].tobytes())
    for alias,index in s.keys.items():
     ah=s.headers[index]
     if alias in replacements or tuple(ah[2:4])!=old[i].size:continue
     if sha(s.decode(index).tobytes())==digest:
      replacements[alias]=dict(v,axis=(axis[0]+ah[4]-h[4],axis[1]+ah[5]-h[5]))
  if slug=='lloyd' and kind=='movement':replacements[(62000,15)]=replacements[(62000,0)]
  if walk:
   shutil.copy2(a/(kind+'.png'),folder/'walk.png');meta.update(frames=records,source_sha256=sha((a/(kind+'.png')).read_bytes()),revision='proportions-v9',status='Installed; anatomy redesigned; gameplay size preserved; recordings deferred')
   packpath.write_text(json.dumps(meta,indent=2));walkmeta[kind]=meta
  sheets[kind]=dict(frames=records,source_sha256=sha((a/(kind+'.png')).read_bytes()),uniform_scale=factor)
 result=s.derive(replacements,{});target=n/sf.name;pending=target.with_suffix('.sff.pending');pending.write_bytes(result);pending.replace(target);fresh=Sff(target)
 checks=[]
 for key,index in s.keys.items():
  if key in replacements:assert sha(fresh.decode(fresh.keys[key]).tobytes())==replacements[key]['rgba_sha256'],key
  else:assert fresh.headers[fresh.keys[key]]==s.headers[index],key
 checks.append('Every replacement decoded exactly; every unrelated sprite header preserved')
 for p in backup.iterdir():
  if p.suffix in ['.air','.cns','.cmd','.def','.zss','.snd']:assert p.read_bytes()==(n/p.name).read_bytes(),p.name
 checks.append('AIR/CNS/CMD/DEF/ZSS/SND byte-identical: timing, collision boxes, controls, damage and sizes unchanged')
 if slug=='jin-mori':
  p=J/slug/'form-cycles-packing.json';d=json.loads(p.read_text());d['cycles']=[walkmeta['walk-base'],walkmeta['walk-king']];d['installed_sff_sha256']=sha(result);p.write_text(json.dumps(d,indent=2));(J/slug/'packing.json').write_text(json.dumps(walkmeta['walk-base'],indent=2))
 report=dict(status='Installed; static validation passed; recordings deferred',revision='proportions-v9',slug=slug,sheets=sheets,replaced_headers=len(replacements),unique_drawings=sum(len(v['frames']) for v in sheets.values()),checks=checks,installed_sff_sha256=sha(result),original_sff_sha256=sha(s.data),tool='built-in imagegen',prompts='requests.json')
 (a/'installation.json').write_text(json.dumps(report,indent=2));print(slug,len(replacements),'headers;',report['unique_drawings'],'drawings; gameplay unchanged',flush=True)
