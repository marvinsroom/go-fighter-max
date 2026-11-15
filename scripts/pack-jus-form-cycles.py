"""Add eight-frame, form-specific walks without changing other native animations.

Use one uniform anatomical scale and one root anchor per complete cycle.
Keep drawings at generated resolution: native AIR scaling avoids huge upscales.
"""
from pathlib import Path
import re,json,io,hashlib,shutil,statistics,sys,struct
import numpy as np
from PIL import Image
from mugen_sff import Sff
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'

def sha(data):return hashlib.sha256(data).hexdigest()
def backup(path):
 p=O/'before'/path.relative_to(E);p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():shutil.copy2(path,p)
 return p
def silhouette(im):
 a=np.asarray(im.convert('RGBA'))[:,:,3]>128;yy,xx=np.where(a)
 assert len(yy)>20
 height=int(yy.max()-yy.min()+1)
 # Lower-third mass approximates the foot/leg midline. Fixed across a cycle,
 # so leg extension changes cannot recenter the actor independently per pose.
 feet=xx[yy>=yy.max()-height*.32]
 return dict(height=height,foot_x=float(feet.mean()),bottom=int(yy.max()+1))
def blocks(text):
 return re.split(r'(?=^\s*\[Begin Action\s+)',text,flags=re.M|re.I)
def frame_rows(block):
 return [[v.strip() for v in line.split(';')[0].split(',')] for line in block.splitlines() if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line)]
def scales(row):return tuple(float(row[i]) if len(row)>i and row[i] else 1 for i in (7,8))

def install(slug,cycles):
 n=E/'chars'/cycles[0]['engine'];sf=n/cycles[0]['sff'];af=n/cycles[0]['air']
 missing=[c['source_group'] for c in cycles if not (R/c['folder']/'walk.png').exists()]
 if missing:print('PENDING',slug,'banks',missing,flush=True);return None
 original=Sff(backup(sf));old_air=backup(af).read_bytes().decode('cp1252');parts=blocks(old_air);old_blocks={};all_rows=[]
 for i,b in enumerate(parts):
  m=re.match(r'\s*\[Begin Action\s+(\d+)\]',b,re.I)
  if m:
   old_blocks[int(m[1])]=(i,b)
   all_rows+=frame_rows(b)
 additions={};reports=[];changed=[]
 for c in cycles:
  folder=R/c['folder'];sheet=Image.open(folder/'walk.png');frames=extract(folder/'walk.png',4,2)
  key=tuple(c['reference_key']);index=original.keys[key];ref=original.decode(index);ref_info=silhouette(ref);ref_axis=original.headers[index][4:6]
  ref_row=next(row for row in all_rows if tuple(map(int,row[:2]))==key)
  ref_scale=scales(ref_row);infos=[silhouette(im) for im,b in frames]
  median_height=statistics.median(v['height'] for v in infos)
  # Preserve the actual original walk bank's logical body height, including
  # its established form scale. Idle/intro frames can use different scales.
  old_walk_heights=[];old_ratios=[]
  for action in c['actions']:
   for old_row in action['frames']:
    old_key=tuple(map(int,old_row[:2]));old_im=original.decode(original.keys[old_key]);sx,sy=scales(old_row)
    old_walk_heights.append(silhouette(old_im)['height']*sy);old_ratios.append(sx/sy)
  logical_height=statistics.median(old_walk_heights)
  air_scale=(logical_height/median_height*statistics.median(old_ratios),logical_height/median_height)
  anatomical_ratio=air_scale[1]/ref_scale[1]
  cell=sheet.width/4
  generated_foot_mid=statistics.median(b[0]-(i%4)*cell+infos[i]['foot_x'] for i,(im,b) in enumerate(frames))
  root_anchor=generated_foot_mid-(ref_info['foot_x']-ref_axis[0])*ref_scale[0]/air_scale[0]
  baseline=[max(b[3] for im,b in frames[0:4]),max(b[3] for im,b in frames[4:8])]
  gap=(ref_axis[1]-ref_info['bottom'])/anatomical_ratio
  records=[]
  assert not any(g==c['output_group'] for g,i in original.keys),(slug,c['output_group'],'original sprite group collision')
  for i,(im,bounds) in enumerate(frames):
   axis=(round((i%4)*cell+root_anchor-bounds[0]),round(baseline[i//4]+gap-bounds[1]))
   buf=io.BytesIO();im.save(buf,format='PNG');png=buf.getvalue();identity=sha(im.tobytes());sprite_key=(c['output_group'],i)
   additions[sprite_key]=dict(image=im,png=png,axis=axis,rgba_sha256=identity)
   im.save(folder/f'walk-{i:02d}.png')
   records.append(dict(key=sprite_key,axis=axis,bounds=bounds,size=im.size,rgba_sha256=identity))
  for action in c['actions']:
   number=action['action'];part_index,old=old_blocks[number];rows=frame_rows(old);first=rows[0]
   # Keep the source's first hurt boxes, offsets, transparency, facing and
   # rotation. Make the standing walk hurt boxes persistent across all poses.
   prefix=old[:re.search(r'(?m)^\s*\d+\s*,\s*\d+\s*,',old).start()]
   prefix=re.sub(r'(?im)^(\s*Clsn[12])\s*:',r'\1Default:',prefix)
   sequence=list(range(8))
   if number%1000==21:sequence.reverse()
   new=prefix.rstrip()+'\n'
   for image_index in sequence:
    fields=first.copy()
    while len(fields)<10:fields.append('')
    fields[0:2]=[str(c['output_group']),str(image_index)];fields[4]='2';fields[7]=f'{air_scale[0]:.10f}';fields[8]=f'{air_scale[1]:.10f}'
    new+=','.join(fields)+'\n'
   new+='\n';parts[part_index]=new;changed.append(number)
  report=dict(status='Packed; native visual review pending',slug=slug,label=c['label'],source_group=c['source_group'],output_group=c['output_group'],source_sha256=sha((folder/'walk.png').read_bytes()),reference_sha256=c['reference_sha256'],anatomical_ratio=anatomical_ratio,air_scale=air_scale,original_logical_walk_height=logical_height,root_anchor=root_anchor,baselines=baseline,distinct_drawings=8,frames=records,actions=[a['action'] for a in c['actions']],method='One scale and one lower-leg root anchor per complete sequence; preserve original logical walk height and collision boxes; no per-pose bounding-box fitting')
  (folder/'packing.json').write_text(json.dumps(report,indent=2));reports.append(report)
 derived=original.derive({},additions)
 pending=sf.with_suffix('.sff.pending');pending.write_bytes(derived);pending.replace(sf)
 new_sff=Sff(sf)
 assert new_sff.data[new_sff.lo:new_sff.lo+original.ls]==original.data[original.lo:original.lo+original.ls],'Original sprite payload changed'
 assert new_sff.data[new_sff.offset:new_sff.offset+original.count*28]==original.data[original.offset:original.offset+original.count*28],'Original sprite headers changed'
 old_pal,old_count=struct.unpack_from('<II',original.data,44)
 new_pal,new_count=struct.unpack_from('<II',new_sff.data,44)
 assert new_count==old_count and new_sff.data[new_pal:new_pal+new_count*16]==original.data[old_pal:old_pal+old_count*16],'Palette table changed'
 for key,frame in additions.items():
  index=new_sff.keys[key];header=new_sff.headers[index]
  assert header[7:9]==(12,32),('Invalid appended sprite format',slug,key,header)
  assert sha(new_sff.decode(index).tobytes())==frame['rgba_sha256'],('Appended sprite payload mismatch',slug,key)
 new_air=''.join(parts);af.write_bytes(new_air.encode('cp1252'))
 fresh_blocks={int(m[1]):b for b in blocks(new_air) if (m:=re.match(r'\s*\[Begin Action\s+(\d+)\]',b,re.I))}
 for number,(i,b) in old_blocks.items():
  if number not in changed:assert fresh_blocks[number]==b,('Non-walk animation changed',slug,number)
 result=dict(slug=slug,status='Packed; current native checks pending',banks=len(cycles),drawings=len(additions),changed_walk_actions=changed,original_sprite_payload_preserved=True,all_non_walk_actions_preserved=True,source_sff_sha256=sha(original.data),installed_sff_sha256=sha(derived),installed_air_sha256=sha(new_air.encode('cp1252')),cycles=reports)
 (O/'art'/slug/'form-cycles-packing.json').write_text(json.dumps(result,indent=2))
 # The simple review/player and base mobility test can consume root metadata.
 root=cycles[0];root_folder=R/root['folder'];root_report=reports[0]
 (O/'art'/slug/'packing.json').write_text(json.dumps(root_report,indent=2))
 for i in range(8):shutil.copy2(root_folder/f'walk-{i:02d}.png',O/'art'/slug/f'walk-{i:02d}.png')
 print('PACKED',slug,len(cycles),'banks',len(additions),'new drawings;',len(changed),'walk actions; all other art/actions preserved',flush=True)
 return result

if __name__=='__main__':
 data=json.loads((O/'animation-cycles.json').read_text());slugs=list(dict.fromkeys(c['slug'] for c in data['cycles']));results=[]
 for slug in slugs:
  if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
  result=install(slug,[c for c in data['cycles'] if c['slug']==slug])
  if result:results.append(result)
 combined=[]
 for slug in slugs:
  path=O/'art'/slug/'form-cycles-packing.json'
  if path.exists():combined.append(json.loads(path.read_text()))
 (O/'form-cycle-installation.json').write_text(json.dumps(dict(status='In progress' if len(combined)<len(slugs) else 'Packed; native validation pending',fighters=combined),indent=2))
