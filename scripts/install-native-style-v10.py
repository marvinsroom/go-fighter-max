"""Replace complete imported pose banks with illustrated art; preserve gameplay."""
from pathlib import Path
import json,re,hashlib,io,sys,collections
from PIL import Image,ImageOps
from mugen_sff import Sff
from edward_assets import read_v1,write_v2
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0/chars'
def sha(data):return hashlib.sha256(data).hexdigest()
def pack(im,axis):
 b=io.BytesIO();im.save(b,format='PNG');return dict(image=im,png=b.getvalue(),axis=axis,rgba_sha256=sha(im.tobytes()))
def timeline(raw):
 result=[]
 for line in raw.decode('cp1252').splitlines():
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=[x.strip() for x in line.split(';')[0].split(',')]
   while len(f)<9:f.append('')
   result.append((f[:7],f[9:]))
  else:result.append(line)
 return result
for slug in sys.argv[1:] or ['naruto','saitama']:
 a=G/'characters'/slug/'art/comic-style-v10';n=E/slug;b=a/'before';sf=next(b.glob('*.sff'));requests=json.loads((a/'requests.json').read_text());replacements={};scales={};entries={};sheets=[];formdata={};checks=[]
 missing=[q['kind'] for q in requests if not (a/(q['kind']+'.generation.json')).exists()]
 if not (a/'portrait.png').exists():missing.append('portrait')
 if missing:raise SystemExit('Conversion incomplete; runtime untouched. '+slug+' pending: '+', '.join(missing))
 # Refuse a partial conversion; every planned drawing must be present and audited.
 for q in requests:
  meta=json.loads((a/(q['kind']+'.generation.json')).read_text(encoding='utf-8'));assert meta['layout_validation']['status']=='PASS',(q['kind'],meta['layout_validation'].get('failures'));assert sha((a/(q['kind']+'.png')).read_bytes())==meta['sha256'],q['kind']
  assert len(meta['layout_validation']['cells'])==q['count'],q['kind']
  q['prompt']=meta['prompt'];q['references']=meta['references']
  folder=a/'extracted'/q['kind'];tiles=[Image.open(folder/(str(i).zfill(2)+'.png')).convert('RGBA') for i in range(q['count'])]
  anchor=q['frames'][0];oldheight=anchor['bounds'][3]-anchor['bounds'][1]
  anchor_index=1 if q['frames'][1]['rgba_sha256']==anchor['rgba_sha256'] else 0
  factor=tiles[anchor_index].height/oldheight
  assert .1<factor<30,(q['kind'],factor)
  for i,(im,f) in enumerate(zip(tiles[1:],q['frames'][1:]),1):
   for alias in f['aliases']:
    key=tuple(alias['key']);left,top,right,bottom=alias['bounds'];oldaxis=alias['axis']
    # Root location follows the source silhouette and its original floor/air offset.
    axis=(round((oldaxis[0]-left)/(right-left)*im.width),round(im.height+(oldaxis[1]-bottom)*factor));v=pack(im,axis)
    # Some original AIR frames intentionally reuse the same native sprite key
    # in multiple template slots. Install the first illustrated occurrence;
    # there is only one raster slot to replace and all actions keep sharing it.
    if key in replacements:continue
    replacements[key]=v;scales[key]=factor;entries[','.join(map(str,key))]=dict(form=q['form'],sheet=q['kind'],cell=i,source=f['source'],axis=axis,size=im.size,anatomical_factor=factor,rgba_sha256=v['rgba_sha256'],old_bounds=alias['bounds'],old_axis=oldaxis)
  formdata.setdefault(q['form'],dict(neutral_key=q['frames'][1]['keys'][0],drawings=0,sheets=[]));formdata[q['form']]['drawings']+=q['count']-1;formdata[q['form']]['sheets'].append(q['kind']);sheets.append(dict(kind=q['kind'],drawings=q['count']-1,source_sha256=meta['sha256'],anatomical_factor=factor))
 if sf.read_bytes()[15]==1:
  source=read_v1(sf);original={s['key']:s for s in source}
 else:
  sff=Sff(sf);original={key:dict(image=sff.decode(index),axis=sff.headers[index][4:6],key=key) for key,index in sff.keys.items()}
 assert all(k in original for k in replacements)
 # Replace the two native HUD/selection portrait slots if the new bust exists.
 portrait_path=a/'portrait.png'
 if portrait_path.exists():
  portrait=Image.open(portrait_path).convert('RGBA');slots=[k for k in original if k[0]==9000 and (k[1] in [0,1] or (slug=='saitama' and k[1]==2))]
  for key in slots:
   old=original[key];im=Image.new('RGBA',old['image'].size);fit=ImageOps.contain(portrait,im.size,Image.Resampling.LANCZOS);im.alpha_composite(fit,((im.width-fit.width)//2,0));replacements[key]=pack(im,old['axis'])
 else:raise AssertionError('Missing illustrated HUD portrait for '+slug)
 target=n/sf.name;pending=target.with_suffix('.sff.pending')
 if sf.read_bytes()[15]==1:
  # SFF1 cannot store RGBA illustrations. Re-encode every unrelated decoded
  # original losslessly in SFF2, keeping every group, number, size and axis.
  sprites=[dict(key=k,axis=replacements.get(k,o)['axis'],image=replacements.get(k,o)['image']) for k,o in original.items()];write_v2(pending,sprites)
 else:pending.write_bytes(sff.derive(replacements,{}))
 proof=Sff(pending);assert set(proof.keys)==set(original),('Sprite key coverage',slug)
 for key,index in proof.keys.items():
  expected=replacements.get(key,original[key]);actual=proof.decode(index)
  assert sha(actual.tobytes())==sha(expected['image'].tobytes()),('Raster changed during packing',key)
  assert tuple(proof.headers[index][4:6])==tuple(expected['axis']),('Root axis mismatch',key)
 checks.append('Every original sprite key retained; every replacement and every unrelated effect raster/axis decoded exactly')
 airpath=next(b.glob('*.air'))
 # Retain the approved giant Kurama scale and collision geometry through conversion.
 approved=G/'characters'/slug/'size-fixes/kurama/approved.air'
 before=approved.read_bytes() if approved.exists() else airpath.read_bytes()
 assert (n/airpath.name).read_bytes()==before,'Live AIR differs from approved conversion baseline'
 changed=0;used=set()
 def patch(match):
  global changed
  line=match[0];head,*comment=line.split(b';',1);f=head.split(b',');key=tuple(int(v.strip()) for v in f[:2])
  if key not in scales:return line
  while len(f)<9:f.append(b'')
  for index in [7,8]:f[index]=format((float(f[index].strip()) if f[index].strip() else 1)/scales[key],'.12f').encode()
  used.add(key);changed+=1;return b','.join(f)+(b';'+comment[0] if comment else b'')
 air=re.sub(rb'(?m)^[ \t]*\d+[ \t]*,[ \t]*\d+[ \t]*,[^\r\n]*',patch,before)
 assert timeline(air)==timeline(before),'Animation behavior or collision boxes changed'
 checks.append('AIR actions, sprite sequence, frame times, offsets, flip/alpha flags, collision geometry and comments preserved; only image-resolution scale fields changed')
 for p in b.iterdir():
  if p.suffix.lower() in ['.cns','.cmd','.def','.zss','.snd','.act']:assert p.read_bytes()==(n/p.name).read_bytes(),('Gameplay file changed',p.name)
 checks.append('All state/controller files, commands, definitions, voices and palettes byte-identical')
 pending.replace(target);(n/airpath.name).write_bytes(air)
 report=dict(status='Installed; complete sprite and preservation audit passed; native/browser verification next; recordings deferred',revision='comic-style-v10',slug=slug,source_version=sf.read_bytes()[15],installed_version=2,drawings=sum(s['drawings'] for s in sheets),sheets=sheets,forms=formdata,entries=entries,body_keys=len(scales),replaced_headers=len(replacements),body_keys_referenced_by_air=len(used),rewritten_air_rows=changed,original_sff_sha256=sha(sf.read_bytes()),installed_sff_sha256=sha(target.read_bytes()),installed_air_sha256=sha(air),checks=checks,tool='built-in imagegen',prompt_set='requests.json',runtime_sha256={p.name:sha((n/p.name).read_bytes()) for p in b.iterdir() if p.is_file()})
 (a/'installation.json').write_text(json.dumps(report,indent=2));(a/'requests.json').write_text(json.dumps(requests,indent=2),encoding='utf-8');print('STYLE_INSTALLED',slug,report['drawings'],'drawings;',len(scales),'body keys;',len(formdata),'form/assist banks;',changed,'AIR rows',flush=True)
