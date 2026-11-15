"""Register current native artwork and rebuild preview images from the installed SFF."""
from comic_identity_v3 import *
from mugen_sff import Sff
import json,hashlib,sys,shutil
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'
for slug in sys.argv[1:]:
 f=C/slug;art=f/'art/comic-identity-v3';data=json.loads((art/'runtime-templates.json').read_text());installed=json.loads((art/'installed.json').read_text());native=E/data['engine'];sff=Sff(native/data['sff'])
 reportpath=f/'build-report.json'
 if reportpath.exists():
  report=json.loads(reportpath.read_text());report['revision']='comic-identity-v3';report['comic_identity']=SPECS[slug]
  original_report=f/'archive/before-comic-identity-v3/build-report.json'
  original_poses=json.loads(original_report.read_text()).get('poses',{}) if original_report.exists() else {}
  report['runtime_sha256']={n:hashlib.sha256((native/n).read_bytes()).hexdigest() for n in report['runtime_sha256']}
  installed['runtime_sha256']=report['runtime_sha256']
  for key,entry in report.get('poses',{}).items():
   sprite=(entry['group'],entry['number'])
   if sprite[0]!=9000 and not any(list(sprite) in row['keys'] for row in installed['poses']):continue
   index=sff.keys[sprite];im=sff.decode(index);out=art/'registered';out.mkdir(exist_ok=True);target=out/(key+'.png');im.save(target)
   # The PNG is the native sprite payload. AIR still applies the original
   # registration scale; decoding an SFF does not bake that scale into pixels.
   scale=original_poses.get(key,entry)['scale']
   entry.update(file=str(target.relative_to(R)),scale=scale,pre_comic_scale=scale,axis=sff.headers[index][4:6],bounds=im.getchannel('A').getbbox(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),comic_redraw=True)
  reportpath.write_text(json.dumps(report,indent=2))
  timeline_path=f/'animation-data.js'
  if timeline_path.exists():
   variable,payload=timeline_path.read_text(encoding='utf-8').split('=',1)
   timelines=json.loads(payload.removesuffix(';'))
   for clip in timelines.values():
    for frame in (clip['frames'] if isinstance(clip,dict) else clip):
     entry=report['poses'].get(frame['key'])
     if not entry or not entry.get('comic_redraw'):continue
     frame.update(scale=entry['scale'],axis=entry['axis'])
     if 'file' in frame:frame['file']=entry['file']
     if 'src' in frame:frame['src']=Path(entry['file']).relative_to(f.relative_to(R)).as_posix()
   timeline_path.write_text(variable+'='+json.dumps(timelines)+';',encoding='utf-8')
 else:
  reportpath=f/'validation/build.json';report=json.loads(reportpath.read_text());report['comic_identity']=SPECS[slug];report['comic_revision']='comic-identity-v3'
  for key,entry in report.get('art',{}).items():
   sprite=(entry['group'],entry['number'])
   if not any(list(sprite) in row['keys'] for row in installed['poses']):continue
   index=sff.keys[sprite];im=sff.decode(index);out=art/'registered';out.mkdir(exist_ok=True)
   target=out/(key.replace(':','-')+'.png');im.save(target)
   entry.update(source=str(target.relative_to(R)),axis=list(sff.headers[index][4:6]),bounds=list(im.getchannel('A').getbbox()),rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest(),comic_redraw=True)
  reportpath.write_text(json.dumps(report,indent=2))
  runtime=f/'validation/runtime.json';old=json.loads(runtime.read_text());installed['runtime_sha256']={n:hashlib.sha256((native/n).read_bytes()).hexdigest() for n in old}
  proportions_path=f/'validation/proportions-art.json'
  proportions=json.loads(proportions_path.read_text())
  for entry in proportions['entries']:
   registered=report['art'][entry['key']]
   if not registered.get('comic_redraw'):continue
   image=sff.decode(sff.keys[entry['group'],entry['number']]);target=f/entry['src'];image.save(target)
   entry.update(axis=registered['axis'],bounds=list(image.getchannel('A').getbbox()),source=registered['source'],sha256=registered['rgba_sha256'],comic_redraw=True)
  proportions['revision']='comic-identity-v3'
  proportions_path.write_text(json.dumps(proportions,indent=2))
  (f/'proportion-audit-data.js').write_text('window.JINWOO_PROPORTIONS='+json.dumps(proportions)+';',encoding='utf-8')
 (art/'installed.json').write_text(json.dumps(installed,indent=2))
 if (f/data['sff']).exists():
  # The character folder also contains the distributable native archive.
  shutil.copy2(native/data['sff'],f/data['sff'])
 # Current portrait aliases in existing review sources, with originals archived.
 oldart=f/('art/canonical-v2' if slug=='baam' else 'art/illustrated-v1' if slug=='jin-mori' else 'art/v3' if slug=='vikir' else 'art/animation-v5' if slug=='pyowol' else 'art/daggers')
 if slug!='jinwoo':
  name='profile-portrait.png' if slug=='pyowol' else 'portrait.png';prior=oldart/name;backup=f/'archive/before-comic-identity-v3'/name
  if prior.exists() and not backup.exists():shutil.copy2(prior,backup)
  shutil.copy2(art/'portrait.png',prior)
  for suffix in ('.prompt.txt','.generation.json'):
   current=art/('portrait'+suffix);target=prior.with_name(prior.stem+suffix)
   if current.exists():
    backup=f/'archive/before-comic-identity-v3'/target.name
    if target.exists() and not backup.exists():shutil.copy2(target,backup)
    shutil.copy2(current,target)
 print('COMIC_REGISTERED',slug,flush=True)
