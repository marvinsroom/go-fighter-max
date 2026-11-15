"""Replay each actual packed form walk in both facings, with capture holds.

Copies the production AIR actions into isolated observation IDs. Other source
gameplay and sprites are unchanged. This is packed-form visual evidence;
ordinary physical walking is exercised separately by validate-jus-mobility.py.
"""
from pathlib import Path
import importlib.util,json,re,concurrent.futures,sys
spec=importlib.util.spec_from_file_location('jus_mobility',Path(__file__).with_name('validate-jus-mobility.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

FIXTURE='''[Statedef -4]
[State -4, Natural forward input]
type=AssertInput
trigger1=map(jusform.natural)=1
flag=F
[State -4, Natural forward command]
type=AssertCommand
trigger1=map(jusform.natural)=1
name="holdfwd"
buffer.time=1
[State -4, Initialize Urkel appearance]
type=VarSet
triggerall=!ishelper
trigger1=map(jusform.urkel)=1
v=30
value=map(jusform.form_value)
[Statedef 8797199]
type=S
movetype=I
physics=N
ctrl=0
velset=0,0
[State 8797199, Grounded form start]
type=PosSet
trigger1=1
x=-camerapos x
y=0
[State 8797199, Face into walking input]
type=Turn
trigger1=facing!=1
[State 8797199, Native form-aware idle]
type=SelfState
trigger1=time>=2
value=0
ctrl=1
[Statedef 8797198]
type=S
movetype=I
physics=N
ctrl=0
velset=0,0
[State 8797198, Native cycle observation]
type=ChangeAnim
trigger1=anim!=map(jusform.action)
trigger2=map(jusform.hold)=1
value=map(jusform.action)
elem=ifelse(map(jusform.hold)=1,map(jusform.elem),1)
[State 8797198, Ground root]
type=PosSet
trigger1=1
x=-camerapos x
y=0
[State 8797198, Observation facing]
type=Turn
trigger1=facing!=map(jusform.facing)
[State 8797198, No automatic turn]
type=AssertSpecial
trigger1=1
flag=noautoturn
'''
m.LUA='''local cases=jsonDecode('../../jus-upgrade/native-forms/SLUG/cases.json')
local report={status='Running',slug='SLUG',method='Production AIR cycles replayed in isolated observation IDs, both facings, short per-pose capture holds; physical movement tested separately',checks={},frames={}}
local index,tick,shot,warmup=1,0,0,0
local seen,pending={},nil
local function save() jsonEncode(report,'PROOF') end
local function finishCase(ok,why)
 table.insert(report.checks,{label=cases[index].label,facing=cases[index].facing,passed=ok,detail=why})
 index=index+1;tick=0;seen={};mapSet('jusform.hold',0);mapSet('jusform.natural',0);mapSet('jusform.urkel',0);save()
end
hook.add('loop','jus-form-cycles-SLUG',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if pending then
  -- Speed-test physics can advance several times between displayed frames.
  -- Hold the exact drawing long enough for fresh render buffers, then capture.
  if pending.settle<24 then pending.settle=pending.settle+1;return end
  if not pending.requested then screenshot();pending.requested=true;return end
  local f=io.open(pending.file,'rb')
  if f then
   f:close();pending.passed=spriteVar('group')==pending.group and spriteVar('image')==pending.drawing and facing()==pending.facing
   table.insert(report.frames,pending);seen[pending.drawing]=pending.passed;pending=nil;shot=shot+1;mapSet('jusform.hold',0);save()
  end
  return
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 tick=tick+1
 if c.natural then
  if tick==1 then
   mapSet('jusform.hold',0);mapSet('jusform.natural',1);mapSet('jusform.urkel',c.urkel and 1 or 0);mapSet('jusform.form_value',c.form_value)
   if c.form_map then mapSet(c.form_map,c.form_value) end
   mapSet('ichigo.manual',1);mapSet('luffy.manual',1);mapSet('goku.manual',1)
   setPower(3000);changeState(8797199)
  end
  if tick<10 then return end
  if spriteVar('group')~=c.group then finishCase(false,'Natural walk used wrong body group '..tostring(spriteVar('group')));return end
  seen[spriteVar('image')]=true
  local count=0;for _ in pairs(seen) do count=count+1 end
  if count==8 then finishCase(true,'Original forward controls played all eight form drawings; native state '..tostring(stateNo()));return end
  if tick>60 then finishCase(false,'Natural forward input did not play eight form drawings') end
  return
 end
 if tick==1 then
  mapSet('jusform.natural',0);mapSet('jusform.urkel',0)
  mapSet('jusform.action',c.action);mapSet('jusform.facing',c.facing);mapSet('jusform.hold',0);changeState(8797198)
 end
 if tick<3 then return end
 local count=0;for _,v in pairs(seen) do if v then count=count+1 end end
 if count==8 then finishCase(true,'All eight native drawings and scales captured');return end
 if tick>100 then finishCase(false,'Did not observe all eight drawings');return end
 local g,d=spriteVar('group'),spriteVar('image')
 if g~=c.group then finishCase(false,'Unexpected body group '..tostring(g));return end
 local sx,sy=animElemVar('xscale'),animElemVar('yscale')
 if math.abs(sx-c.xscale)>.000001 or math.abs(sy-c.yscale)>.000001 or facing()~=c.facing or posY()~=0 then finishCase(false,'Native scale/facing/root mismatch');return end
 if d>=0 and d<8 and seen[d]==nil then
  mapSet('jusform.elem',c.backward and 8-d or d+1);mapSet('jusform.hold',1)
  pending={label=c.label,facing=c.facing,group=g,drawing=d,xscale=sx,yscale=sy,settle=0,file='CAPTURE_DIR/JUS_SLUG'..string.format('%03d',shot)..'.png'}
 end
end)
'''

def run(row):
 slug=row['slug'];packing=m.O/'art'/slug/'form-cycles-packing.json'
 if not packing.exists():return None
 data=json.loads(packing.read_text());n=m.E/'chars'/row['engine'];definition=n/row['definition'];original=definition.read_text(encoding='cp1252')
 airname=re.search(r'(?im)^\s*anim\s*=\s*([^;\r\n]+)',original)[1].strip();air=(n/airname).read_text(encoding='cp1252');extra='';cases=[]
 used_forms=set()
 def natural(cycle,form_value,label=None):
  namespace={'baam':'baam.form','jin-mori':'mori.form','vikir':'vikir.form','goku':'goku.form','gt-goku':'goku.form','ichigo':'ichigo.form','luffy':'luffy.form'}.get(slug)
  cases.append(dict(label=(label or cycle['label'])+' natural forward walk',natural=True,facing=1,group=cycle['output_group'],form_map=namespace,form_value=form_value,urkel=slug=='urkel'));used_forms.add(form_value)
 for cycle in data['cycles']:
  for backward,facing in ((False,1),(True,-1)):
   source_action=next(a for a in cycle['actions'] if a%1000==(21 if backward else 20))
   block=re.search(r'(?ims)^\s*\[Begin Action\s+'+str(source_action)+r'\](.*?)(?=^\s*\[Begin Action|\Z)',air)[0]
   action=12001000+len(cases);extra+=re.sub(r'(?i)\[Begin Action\s+\d+\]',f'[Begin Action {action}]',block,count=1)+'\n'
   cases.append(dict(label=cycle['label']+(' backward / left' if backward else ' forward / right'),action=action,group=cycle['output_group'],xscale=cycle['air_scale'][0],yscale=cycle['air_scale'][1],facing=facing,backward=backward))
  group=cycle['source_group']
  if slug=='baam':form=int(group==62100)
  elif slug=='jin-mori':form=int(group==62300)
  elif slug=='vikir':form=group-50
  elif slug=='urkel':form=int(group==30)
  elif slug=='goku':
   from goku_model import FORMS
   form=next(f['id'] for f in FORMS if f['bank']==group-62000)
  else:form=group-62000
  natural(cycle,form)
 if slug=='goku':
  from goku_model import FORMS
  for form in FORMS:
   if form['id'] not in used_forms:
    cycle=next(c for c in data['cycles'] if c['source_group']==62000+form['bank']);natural(cycle,form['id'],form['name'])
 (n/'jus-form-cycles-test.air').write_text(air+'\n'+extra,encoding='cp1252')
 clone=re.sub(r'(?im)^(\s*anim\s*=).*$',r'\1jus-form-cycles-test.air',original,count=1)
 (n/'jus-form-cycles-test.def').write_text(clone,encoding='cp1252')
 folder=m.O/'native-forms'/slug;folder.mkdir(parents=True,exist_ok=True);casefile=folder/'cases.json';casefile.write_text(json.dumps(cases))
 test=dict(row,definition='jus-form-cycles-test.def',harness_inputs=['../../jus-upgrade/native-forms/'+slug+'/cases.json'])
 before=m.runtime(row);result=m.run(test,'native-forms');assert before==m.runtime(row),'Production changed during form capture'
 result['production_runtime_sha256']=before
 (folder/'current.json').write_text(json.dumps(result,indent=2))
 assert all(f['passed'] for f in result['frames'])
 return result

if __name__=='__main__':
 (m.E/'data/jus-test-fixture.cns').write_text(FIXTURE)
 all_rows=json.loads((m.O/'manifest.json').read_text())['fighters'];rows=[r for r in all_rows if (m.O/'art'/r['slug']/'form-cycles-packing.json').exists() and (len(sys.argv)==1 or r['slug'] in sys.argv[1:])]
 results=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  jobs={pool.submit(run,r):r['slug'] for r in rows}
  for job in concurrent.futures.as_completed(jobs):
   try:results.append(job.result())
   except Exception as error:errors.append(dict(slug=jobs[job],error=str(error)));print('FAILED',jobs[job],error,flush=True)
 combined=[]
 for row in all_rows:
  proof=m.O/'native-forms'/row['slug']/'current.json'
  if not proof.exists():continue
  value=json.loads(proof.read_text())
  test=dict(row,definition='jus-form-cycles-test.def',harness_inputs=['../../jus-upgrade/native-forms/'+row['slug']+'/cases.json'])
  if value.get('status')=='Complete' and value.get('failed')==0 and value.get('production_runtime_sha256')==m.runtime(row) and value.get('harness_sha256')==m.harness(test,'native-forms'):combined.append(value)
 expected=sum((m.O/'art'/r['slug']/'form-cycles-packing.json').exists() for r in all_rows)
 (m.O/'native-form-validation.json').write_text(json.dumps(dict(status='Complete' if len(combined)==expected and not errors else 'In progress',fighters=combined,errors=errors),indent=2))
 if errors or any(r['failed'] for r in results):raise SystemExit(1)
