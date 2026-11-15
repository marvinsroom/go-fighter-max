"""Prove requested fighters reach an active native round, without recording media."""
from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'mugen-expansion/validation'
queue=json.loads((G/'mugen-expansion/queue.json').read_text());rows={r['slug']:r for r in queue['fighters']}
O.mkdir(exist_ok=True)
lua='''local ticks=0
local states={}
hook.add('loop','original-import-check',function()
 if not player(1) or roundState()~=2 then return end
 ticks=ticks+1
 states[tostring(stateNo())]=true
 if ticks>=180 then
  jsonEncode({status='PASS',slug='SLUG',scope='Verified loaded fighter identity and 180 active-round ticks; full moves/forms audit pending',recording=false,active_round_ticks=ticks,loaded_name=name(),animation=anim(),states=states},'../../mugen-expansion/validation/SLUG.json')
  os.exit(0)
 end
end)
'''
def quote(v):return "'"+str(v).replace("'","''")+"'"
failures=[]
for slug in [arg for arg in sys.argv[1:] if arg!='--force']:
 assert slug in rows and rows[slug].get('engine'), 'Not an imported fighter: '+slug
 report=O/(slug+'.json')
 if report.exists():
  old=json.loads(report.read_text(encoding='utf-8-sig'))
  if '--force' not in sys.argv and old.get('status')=='PASS' and old.get('active_round_ticks',0)>=180:print(slug,'already verified',flush=True);continue
  report.unlink()
 mod='external/mods/-import-check-'+slug+'.lua';(E/mod).write_text(lua.replace('SLUG',slug))
 config=(E/'save/config.ini').read_text()
 for key,value in {'Modules':mod,'MasterVolume':'0'}.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 ini='save/import-check-'+slug+'.ini';(E/ini).write_text(config)
 args=['-config',ini,'-loadmotif','-p1',slug,'-p2','baam','-p1.ai','8','-p2.ai','0','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
 command='$p=Start-Process -FilePath '+quote(E/'Ikemen_GO.exe')+' -WorkingDirectory '+quote(E)+' -ArgumentList @('+','.join(map(quote,args))+') -WindowStyle Hidden -RedirectStandardOutput '+quote(O/(slug+'-stdout.log'))+' -RedirectStandardError '+quote(O/(slug+'-stderr.log'))+' -PassThru; $null=$p.Handle; if(!$p.WaitForExit(45000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode'
 result=subprocess.run(['powershell','-NoProfile','-Command',command],timeout=55)
 err=(O/(slug+'-stderr.log')).read_text(errors='replace')
 if not report.exists():
  data=dict(slug=slug,status='FAIL',scope='No proof of an active round',recording=False,exit_code=result.returncode,stderr=err)
 else:
  data=json.loads(report.read_text())
  definition=(E/'chars'/slug/(slug+'.def')).read_text(encoding='cp1252',errors='replace')
  expected=re.search(r'(?im)^\s*name\s*=\s*"?([^\r\n";]+)',definition)[1].strip()
  data['expected_name']=expected
  data['roster_count_at_test']=queue['main_roster_count']
  data['identity_matches']=data.get('loaded_name','').casefold()==expected.casefold()
  if result.returncode or not data['identity_matches'] or re.search(r'(?im)Panic:|stack traceback:|error parsing|error loading|failed to load',err):data['status']='FAIL';data['stderr']=err
 report.write_text(json.dumps(data,indent=2))
 print(slug,data['status'],data.get('loaded_name',''),flush=True)
 if data['status']!='PASS':failures.append(slug)
assert not failures,'Native check failed: '+', '.join(failures)
