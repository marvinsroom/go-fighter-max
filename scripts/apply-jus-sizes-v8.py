"""Apply the confirmed gameplay size policy without restoring old character data."""
from pathlib import Path
import json,re,statistics,collections,hashlib,shutil,copy
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/size-fix-v8';J=R/'sprite-fighter/jus-upgrade';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
policy=json.loads((O/'policy.json').read_text());manifest=json.loads((J/'manifest.json').read_text());measured={r['slug']:r for r in json.loads((R/'.tmp/size-redesign/measurements.json').read_text())}
if not (O/'measurements-before.json').exists():(O/'measurements-before.json').write_text(json.dumps(list(measured.values()),indent=2))
measured={r['slug']:r for r in json.loads((O/'measurements-before.json').read_text())}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def save(path):
 relative=path.relative_to(E) if path.is_relative_to(E) else Path('metadata')/path.relative_to(R/'sprite-fighter')
 backup=O/'before'/relative;backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():shutil.copy2(path,backup)
 return backup
def fields(line):return [v.strip() for v in line.split(';')[0].split(',')]
reports=[]
for row in manifest['fighters']:
 slug=row['slug'];measurement=measured[slug];native=E/row['engine'];names=measurement['files'];cns=native/names['cns'];airfile=native/names['anim'];before_cns=save(cns).read_bytes();before_air=save(airfile).read_bytes();text=before_air.decode('latin1')
 target=policy['neutral_world_height'][slug];global_factor=target/measurement['world_height'];new_native=[v*global_factor for v in measurement['cns_scale']]
 size=re.search(rb'(?ims)^\s*\[Size\](.*?)(?=^\s*\[|\Z)',before_cns);section=size[0]
 for name,value in zip(['xscale','yscale'],new_native):section,count=re.subn(rb'(?im)^(\s*'+name.encode()+rb'\s*=\s*)[-+0-9.eE]+',lambda m:m[1]+format(value,'.10g').encode(),section,count=1);assert count==1
 new_cns=before_cns[:size.start()]+section+before_cns[size.end():]
 definition=native/row['definition'];save(definition)
 width=measurement['width'];reference=tuple(measurement['key']);scales={}
 for line in text.splitlines():
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=fields(line);key=tuple(map(int,f[:2]));scales.setdefault(key,[]).append((float(f[7]) if len(f)>7 and f[7] else 1,float(f[8]) if len(f)>8 and f[8] else 1))
 scales={key:collections.Counter(values).most_common(1)[0][0] for key,values in scales.items()}
 sprites=None;groups={};form_targets=policy['forms'].get(slug,{})
 if form_targets:
  sprites=Sff(native/names['sprite'])
  for group,value in form_targets.items():
   g=int(group);key=(g,11 if slug=='rimuru' and g==8790 else 0)
   if key not in sprites.keys or key not in scales:continue
   im=sprites.decode(sprites.keys[key]);bounds=im.getbbox();world=(bounds[3]-bounds[1])*scales[key][1]*new_native[1]*320/width
   groups[g]=dict(factor=value/world,target=value,old_world=world/global_factor,key=key)
  if slug=='rimuru' and 8790 in groups:groups[8793]=dict(groups[8790])
  if slug=='baam' and 62100 in groups:groups[62500]=dict(groups[62100])
  del sprites
 # New walk banks are calibrated to the corresponding standing body, using
 # one multiplier for the complete cycle, rather than fitting individual poses.
 packing=J/'art'/slug/'packing.json';form=J/'art'/slug/'form-cycles-packing.json';walks=[];form_report=None
 if form.exists():
  backup=save(form);form_report=json.loads(backup.read_text());walks=form_report['cycles']
 elif packing.exists():walks=[json.loads(save(packing).read_text())]
 walk_reports=[]
 for cycle in walks:
  source_group=cycle.get('source_group',reference[0]);g=cycle.get('output_group',cycle['frames'][0]['key'][0]);desired=groups.get(source_group,{}).get('target',target)*policy['walk_stance_ratio']
  heights=[]
  for frame in cycle['frames']:
   key=tuple(frame['key']);heights.append(frame['size'][1]*scales[key][1]*new_native[1]*320/width)
  factor=desired/statistics.median(heights);groups[g]=dict(factor=factor,target=desired,old_world=statistics.median(heights)/global_factor,key=cycle['frames'][0]['key'])
  cycle['status']='Installed; consistent JUS size; recordings deferred';cycle['gameplay_world_height']=desired
  cycle['air_scale']=[scales[tuple(cycle['frames'][0]['key'])][i]*factor for i in [0,1]]
  walk_reports.append(dict(group=g,label=cycle.get('label',slug),old_world_height=statistics.median(heights)/global_factor,new_world_height=desired,factor=factor))
 def factor_for(key):
  if slug=='baam' and key[0]==62600 and key[1]>=8:return groups.get(62100,{}).get('factor',1)
  return groups.get(key[0],{}).get('factor',1)
 new_blocks=[];changed_rows=0;changed_boxes=0
 for block in re.split(r'(?=^\s*\[Begin Action\s+)',text,flags=re.I|re.M):
  body_factors=[]
  for line in block.splitlines():
   if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
    key=tuple(map(int,fields(line)[:2]))
    if key[0] in groups:body_factors.append(factor_for(key))
  box_factor=statistics.median(body_factors) if body_factors else 1
  lines=[]
  for line in block.splitlines(keepends=True):
   if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
    content,mark,comment=line.rstrip('\r\n').partition(';');f=content.split(',');key=tuple(int(v.strip()) for v in f[:2]);factor=factor_for(key)
    if abs(factor-1)>1e-9:
     while len(f)<9:f.append('')
     for index in [7,8]:f[index]=format((float(f[index]) if f[index].strip() else 1)*factor,'.10f')
     line=','.join(f)+(mark+comment if mark else '')+('\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else '');changed_rows+=1
   elif abs(box_factor-1)>1e-9 and re.match(r'^\s*Clsn[12]\s*\[',line,re.I):
    lhs,rhs=line.split('=',1);line=lhs+'='+re.sub(r'-?\d+(?:\.\d+)?',lambda m:str(round(float(m[0])*box_factor)),rhs);changed_boxes+=1
   lines.append(line)
  new_blocks.append(''.join(lines))
 result=''.join(new_blocks).encode('latin1')
 def timeline(raw):return [(tuple(fields(l)[:7]),fields(l)[9:]) for l in raw.decode('latin1').splitlines() if re.match(r'^\s*\d+\s*,\s*\d+\s*,',l)]
 assert timeline(before_air)==timeline(result),(slug,'timing or routing changed')
 for path,raw in [(cns,new_cns),(airfile,result)]:pending=path.with_suffix(path.suffix+'.pending');pending.write_bytes(raw);pending.replace(path)
 if form_report:
  form_report['status']='Installed; consistent JUS sizes; recordings deferred';form_report['installed_air_sha256']=sha(result);form.write_text(json.dumps(form_report,indent=2))
  for cycle in walks:
   path=J/'art'/slug/'cycles'/str(cycle['source_group'])/'packing.json';save(path);path.write_text(json.dumps(cycle,indent=2))
  save(packing);packing.write_text(json.dumps(walks[0],indent=2))
 elif walks:packing.write_text(json.dumps(walks[0],indent=2))
 row['target_world_height']=target;row['gameplay_size_role']='small / child' if target<46 else 'teen' if target<51 else 'adult';row['sizing_revision']='consistent-jus-v8'
 reports.append(dict(slug=slug,old_neutral_world_height=measurement['world_height'],new_neutral_world_height=target,native_scale=new_native,forms=groups,walks=walk_reports,changed_air_rows=changed_rows,changed_collision_boxes=changed_boxes,cns_sha256=sha(new_cns),air_sha256=sha(result),timing_preserved=True))
 print('SIZED',slug,measurement['world_height'],'->',target,'walk banks',len(walks),flush=True)
manifest['sizing_policy']=policy['policy'];manifest['status']='Consistent JUS size fixes installed; recordings deferred';(J/'manifest.json').write_text(json.dumps(manifest,indent=2))
(O/'installation.json').write_text(json.dumps(dict(status='Installed; direct verification next; recordings deferred',policy=policy['policy'],fighters=reports),indent=2))
