"""Capture current packed body/form samples in both facings in the native engine.

Production controls are never edited by the fixture. Reports bind each capture
to the installed files and test the engine's actual native scale and sprite key.
"""
from pathlib import Path
import json,re,hashlib,subprocess,os,sys,concurrent.futures,datetime,functools
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/face-audit/identity-scale-v5';profiles=json.loads((O/'profiles.json').read_text());stamp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
@functools.lru_cache(maxsize=None)
def sha(p):
 digest=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
 return digest.hexdigest()
def psq(s):return "'"+str(s).replace("'","''")+"'"
def execute(row):
 existing=O/'native'/row['slug']/'current.json'
 if existing.exists():
  saved=json.loads(existing.read_text())
  if saved.get('status')=='Complete' and not saved.get('failed') and saved.get('runtime_sha256')==row['runtime_sha256'] and any(x.get('label')=='Basic attack connects' and x.get('passed') for x in saved.get('checks',[])):
   print('STATURE_NATIVE_CURRENT',row['slug'],saved['passed'],flush=True);return dict(slug=row['slug'],passed=saved['passed'],proof=str(existing.relative_to(R)),runtime_sha256=saved['runtime_sha256'])
 slug=row['slug'];n=E/'chars'/row['engine'];de=(n/row['definition']).read_text(encoding='utf-8',errors='replace');air=(n/row['air']).read_text(encoding='utf-8',errors='replace');sprites=Sff(n/row['sff']);keys={};actions={}
 for block in re.split(r'(?=^\s*\[Begin Action )',air,flags=re.M|re.I):
  match=re.search(r'\[Begin Action (\d+)\]',block,re.I)
  if not match:continue
  frames=[]
  for line in block.splitlines():
   if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
   f=[v.strip() for v in line.split(';',1)[0].split(',')];key=tuple(map(int,f[:2]));scale=[float(f[j]) if len(f)>j and f[j] else 1 for j in (7,8)]
   if key in sprites.keys:keys.setdefault(key,scale);frames.append(key)
  actions[int(match[1])]=frames
 samples=[]
 def add(key,label):
  key=tuple(key)
  if key in keys and key not in [x[0] for x in samples]:samples.append((key,label))
 add(row['neutral_key'],'Neutral')
 template=R/'sprite-fighter/characters'/slug/'art/comic-identity-v3/runtime-templates.json'
 if template.exists():
  for page in json.loads(template.read_text())['pages']:
   for i in sorted(set((0,len(page['frames'])//2))):add(page['frames'][i]['keys'][0],page['kind']+f' pose {i}')
 elif slug in ('goku','gt-goku','ichigo','luffy'):
  for group in sorted({g for g,i in sprites.keys if 62000<=g<62100}):
   for pose in (0,8):add((group,pose),f'Form {group-62000}, pose {pose}')
 else:
  for action in (20,200,230,300,400):
   if actions.get(action):add(actions[action][min(1,len(actions[action])-1)],f'Action {action}')
  if slug in ('prince','tyrone'):
   for g in (50,51):add((g,0),f'Appearance {g}')
  if slug=='urkel':
   for g in (20,21,30,31):add((g,0),f'Appearance {g}')
  if slug=='rimuru':
   for key,label in [((8791,0),'Demon Lord'),((8790,11),'Slime'),((8793,0),'Slime walk'),((8794,0),'Human casting')]:add(key,label)
 if slug=='jinwoo':
  for group,label in [(61001,'Igris'),(61002,'Beru'),(61003,'Iron'),(61004,'Tank')]:add((group,0),label+' shadow form')
 if slug=='vikir':add((52,0),'Choco pet form')
 cases=[];extra=''
 for i,(key,label) in enumerate(samples):
  sx,sy=keys[key];extra+=f'\n[Begin Action {12000000+i}]\n{key[0]},{key[1]},0,0,-1,,,{sx},{sy}\n'
  for facing in (1,-1):cases.append(dict(id=i,label=label,group=key[0],drawing=key[1],xscale=sx,yscale=sy,facing=facing,native_scale=row['native_scale'][1]))
 cases.append(dict(id=0,label='Basic attack connects',combat=True,state=230 if slug=='jin-mori' else 200,facing=1,native_scale=row['native_scale'][1]))
 (n/'stature-v5-test.air').write_text(air+extra,encoding='utf-8')
 fixture=f'''\n[Statedef 879650]\ntype=S\nmovetype=I\nphysics=N\nctrl=0\nvelset=0,0\n[State 879650, Hold frame]\ntype=ChangeAnim\ntrigger1=anim!=12000000+map(stature.pose)\nvalue=12000000+map(stature.pose)\n[State 879650, Ground root]\ntype=PosSet\ntrigger1=1\nx=-{row['localcoord_width']*.10}\ny=0\n[State 879650, Facing]\ntype=Turn\ntrigger1=facing!=map(stature.facing)\n[State 879650, Native scale]\ntype=MapSet\ntrigger1=1\nmap="stature.native_scale"\nvalue=const(size.yscale)\n[State 879650, Prevent turning]\ntype=AssertSpecial\ntrigger1=1\nflag=noautoturn\n'''
 fixture=fixture.replace(f'x=-{row["localcoord_width"]*.10}',f'x=ifelse(map(stature.combat)=1,-{row["localcoord_width"]*.03125},-{row["localcoord_width"]*.10})')
 (n/'stature-v5-test.cns').write_text(fixture)
 definition=re.sub(r'(?im)^(\s*anim\s*=).*$',r'\1stature-v5-test.air',de);stnums=[int(x) for x in re.findall(r'(?im)^\s*st(\d+)\s*=',de)];definition=re.sub(r'(?im)^\s*\[Files\]',lambda m:m[0]+f'\nst{max(stnums+[4])+1}=stature-v5-test.cns',definition,count=1);(n/'stature-v5-test.def').write_text(definition,encoding='utf-8')
 folder=O/'native'/slug/f'run-{stamp}';folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('*.png'))
 rel=folder.relative_to(E.parent.parent).as_posix();# relative from sprite-fighter, prefix ../ from engine
 folder_from_engine='../../face-audit/identity-scale-v5/native/'+slug+'/run-'+stamp
 proof=O/'native'/slug/'current.json';proof.parent.mkdir(parents=True,exist_ok=True)
 casefile=O/'native'/slug/'cases.json';casefile.write_text(json.dumps(cases))
 runtime={name:sha(n/name) for name in row['runtime_sha256']};(O/'native'/slug/'runtime.json').write_text(json.dumps(runtime))
 target=E/'chars/will_full';targetdef=(target/'will_full.def').read_text()
 targetcns='''[Statedef 879651]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 879651, Ground target]
type=PosSet
trigger1=1
x=40
y=0
[State 879651, No push]
type=PlayerPush
trigger1=1
value=0
'''
 targetname='stature-v5-target-'+slug
 (target/(targetname+'.cns')).write_text(targetcns)
 (target/(targetname+'.def')).write_text(re.sub(r'(?im)^\s*\[Files\]',lambda m:m[0]+'\nst99='+targetname+'.cns',targetdef,count=1))
 lua='''local cases=jsonDecode('CASEFILE')
local report={status='Running',checks={},frames={},runtime_sha256=jsonDecode('RUNTIMEFILE'),method='Current native packed body samples, both facings, actual CNS and AIR scales'}
local index,tick,shot,pending,warmup=1,0,0,nil,0
local function save() jsonEncode(report,'PROOFFILE') end
hook.add('loop','stature-v5',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if pending then
  local file=io.open('CAPTURE/Stature_v5'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);table.insert(report.checks,{label=pending.label,facing=pending.facing,passed=pending.passed});index=index+1;tick=0;shot=shot+1;pending=nil;save() end
  return
 end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
 if c.combat then
  tick=tick+1
  if tick==1 then
   mapSet('stature.pose',0);mapSet('stature.facing',1);mapSet('stature.combat',1);changeState(879650)
   player(2);setLife(1000);changeState(879651);player(1)
  end
  if tick==8 then changeState(c.state) end
  if tick>=12 then
   player(2);local hp=life();player(1)
   if hp<1000 or tick>=240 then
    pending={label=c.label,facing=facing(),group=spriteVar('group'),drawing=spriteVar('image'),target_life=hp,passed=hp<1000,file='CAPTURE/Stature_v5'..string.format('%03d',shot)..'.png'};screenshot()
   end
  end
  return
 end
 tick=tick+1
 if tick==1 then mapSet('stature.pose',c.id);mapSet('stature.facing',c.facing);changeState(879650) end
 if tick>=24 then
  local g=tonumber(spriteVar('group'));local d=tonumber(spriteVar('image'));local sx=tonumber(animElemVar('xscale'));local sy=tonumber(animElemVar('yscale'));local native=tonumber(map('stature.native_scale')) or -1
  local ok=g==c.group and d==c.drawing and facing()==c.facing and math.abs(sx-c.xscale)<.00001 and math.abs(sy-c.yscale)<.00001 and math.abs(native-c.native_scale)<.00001 and posY()==0
  pending={label=c.label,facing=facing(),group=g,drawing=d,xscale=sx,yscale=sy,native_scale=native,screen_x=screenPosX(),screen_y=screenPosY(),passed=ok,file='CAPTURE/Stature_v5'..string.format('%03d',shot)..'.png'}
  screenshot()
 end
end)
'''
 for key,value in {'CASEFILE':'../../face-audit/identity-scale-v5/native/'+slug+'/cases.json','RUNTIMEFILE':'../../face-audit/identity-scale-v5/native/'+slug+'/runtime.json','PROOFFILE':'../../face-audit/identity-scale-v5/native/'+slug+'/current.json','CAPTURE':folder_from_engine}.items():lua=lua.replace(key,value)
 mod=f'external/mods/-stature-v5-{slug}.lua';(E/mod).write_text(lua)
 config=(E/'save/jinwoo-current-tests.ini').read_text();settings={'Modules':mod,'ScreenshotFolder':folder_from_engine+'/','WindowTitle':'Stature_v5','MasterVolume':'0'}
 for key,value in settings.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 configfile=f'save/stature-v5-{slug}.ini';(E/configfile).write_text(config)
 args=['-config',configfile,'-loadmotif','-p1',row['engine']+'/stature-v5-test.def','-p2','will_full/'+targetname+'.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
 command='$g=Start-Process -FilePath '+psq(E/'Ikemen_GO.exe')+' -WorkingDirectory '+psq(E)+' -ArgumentList @('+','.join(map(psq,args))+') -WindowStyle Hidden -RedirectStandardOutput '+psq(R/'.tmp'/f'stature-v5-{slug}-out.log')+' -RedirectStandardError '+psq(R/'.tmp'/f'stature-v5-{slug}-err.log')+' -PassThru; $null=$g.Handle; $g.WaitForExit(); exit $g.ExitCode'
 subprocess.run(['powershell','-NoProfile','-Command',command],cwd=R,check=True,timeout=300)
 result=json.loads(proof.read_text());assert result['status']=='Complete' and result['failed']==0,(slug,result.get('failed'))
 assert result['runtime_sha256']=={name:sha(n/name) for name in runtime}
 for frame in result['frames']:assert (E/frame['file']).exists()
 print('STATURE_NATIVE_PASS',slug,result['passed'],flush=True);return dict(slug=slug,passed=result['passed'],proof=str(proof.relative_to(R)),runtime_sha256=runtime)
if __name__=='__main__':
 selected=[r for r in profiles['fighters'] if len(sys.argv)==1 or r['slug'] in sys.argv[1:]]
 errors=[];results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  jobs={pool.submit(execute,row):row['slug'] for row in selected}
  for job in concurrent.futures.as_completed(jobs):
   try:results.append(job.result())
   except Exception as error:errors.append((jobs[job],str(error)));print('STATURE_NATIVE_FAILED',jobs[job],str(error),flush=True)
 combined=[]
 for row in profiles['fighters']:
  proof=O/'native'/row['slug']/'current.json'
  if not proof.exists():continue
  d=json.loads(proof.read_text())
  if d.get('status')=='Complete' and d.get('failed')==0 and d['runtime_sha256']=={name:sha(E/'chars'/row['engine']/name) for name in row['runtime_sha256']}:
   combined.append(dict(slug=row['slug'],passed=d['passed'],proof=str(proof.relative_to(R)),runtime_sha256=d['runtime_sha256']))
 (O/'native-validation.json').write_text(json.dumps(dict(status='Complete' if len(combined)==len(profiles['fighters']) else 'In progress',fighters=combined,checks=sum(x['passed'] for x in combined)),indent=2))
 if errors:raise RuntimeError(errors)
