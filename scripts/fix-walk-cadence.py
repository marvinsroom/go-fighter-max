"""Retune current illustrated walks without rebuilding sprites or other actions."""
from pathlib import Path
import json,re,hashlib,shutil
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'walk-fix-v11';O.mkdir(exist_ok=True)
manifest=json.loads((G/'jus-upgrade/manifest.json').read_text());reports=[]
frame=re.compile(rb'(?m)^[ \t]*\d+[ \t]*,[ \t]*\d+[ \t]*,[^\r\n]*')
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  while chunk:=stream.read(1024*1024):h.update(chunk)
 return h.hexdigest()
def backup(path):
 dest=O/'before'/path.relative_to(E);dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():shutil.copy2(path,dest)
 return dest
for row in manifest['fighters']:
 slug=row['slug']
 if slug in ['naruto','saitama']:continue
 n=E/'chars'/row['engine'];definition=(n/row['definition']).read_text(encoding='cp1252',errors='replace')
 airname=re.search(r'(?im)^\s*anim\s*=\s*([^;\r\n]+)',definition)[1].strip();sfname=re.search(r'(?im)^\s*sprite\s*=\s*([^;\r\n]+)',definition)[1].strip();af=n/airname
 original=backup(af).read_bytes();changed=[]
 def convert(match):
  number=int(match[1]);block=match[0];rows=list(frame.finditer(block))
  if not rows:return block
  fields=[[x.strip() for x in m[0].split(b';')[0].split(b',')] for m in rows]
  generated=len(rows)==8 and all(64150<=int(f[0])<64250 for f in fields)
  legacy=slug in ['cid','rimuru','edward','pyowol','jinwoo'] and number in [20,21]
  if not (generated or legacy):return block
  backward=number%1000==21
  assert number%1000 in [20,21],(slug,number)
  ticks=[int(f[4]) for f in fields]
  if min(ticks)<=0:return block
  total=48 if backward else 40;old_total=sum(ticks)
  boundaries=[round(sum(ticks[:i])*total/old_total) for i in range(len(ticks)+1)]
  durations=[boundaries[i+1]-boundaries[i] for i in range(len(ticks))];assert min(durations)>0
  iterator=iter(durations)
  def timing(m):
   line=m[0];head,*comment=line.split(b';',1);values=head.split(b',');values[4]=str(next(iterator)).encode();return b','.join(values)+(b';'+comment[0] if comment else b'')
  result=frame.sub(timing,block)
  def without_time(data):
   return frame.sub(lambda m:b','.join(m[0].split(b',')[:4]+[b'TIME']+m[0].split(b',')[5:]),data)
  assert without_time(result)==without_time(block),'Only durations may change'
  changed.append(dict(action=number,group=int(fields[0][0]),frames=len(rows),before_ticks=ticks,after_ticks=durations,cycle_ticks=total))
  return result
 result=re.sub(rb'(?im)^\s*\[Begin Action\s+(\d+)\][\s\S]*?(?=^\s*\[Begin Action|\Z)',convert,original)
 assert changed,slug
 af.write_bytes(result)
 reports.append(dict(slug=slug,engine=row['engine'],definition=row['definition'],air=airname,sff=sfname,sff_sha256=digest(n/sfname),before_air_sha256=digest(backup(af)),after_air_sha256=digest(af),actions=changed))
mobility=E/'data/jus-mobility.cns';before=backup(mobility).read_bytes();old=b'x=ifelse(vel x>0,const240p(1.9),const240p(-1.5))';new=b'x=ifelse(vel x>0,const240p(.95),const240p(-.72))';assert before.count(old)==1
mobility.write_bytes(before.replace(old,new))
report=dict(status='Cadence and ground speed installed; artwork phase repairs still pending image generation',fighters=len(reports),walk_actions=sum(len(r['actions']) for r in reports),forward_ticks=40,backward_ticks=48,world_speed=dict(before=dict(forward=1.9,backward=-1.5),after=dict(forward=.95,backward=-.72)),preservation='Only walk AIR duration fields and shared walk velocity changed. Sprite archives, scales, offsets, collision boxes, combat timing, dash speed and new original MUGEN imports preserved.',artwork_blocker=dict(character='lloyd',issue='Existing drawings repeat the same lead leg; needs correctly alternating support/swing phases',tool_error='usage_limit_reached',paid_api_authorized=False),recordings=False,files=reports)
(O/'installation.json').write_text(json.dumps(report,indent=2));print('WALK_CADENCE_FIXED',report['fighters'],'styled fighters;',report['walk_actions'],'walk actions; sprites/combat unchanged')
