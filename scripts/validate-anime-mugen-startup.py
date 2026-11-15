"""Observe unmodified imported fighters entering and fighting in the real engine."""
from pathlib import Path
import json,re,subprocess,datetime,concurrent.futures,hashlib
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';stamp=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
def quote(s):return "'"+str(s).replace("'","''")+"'"
def run(slug):
 f=R/'sprite-fighter/characters'/slug;capture='import-startup-'+stamp;folder=f/'replays'/capture;folder.mkdir(parents=True)
 code='''local report={status='Running',method='Unmodified production definition; natural entrance and AI combat',frames={},states_seen={},damage=0,combat_ticks=0}
local total,shot,pending=0,0,nil
local function save() jsonEncode(report,'../../characters/SLUG/startup-validation.json') end
hook.add('loop','anime-import-startup',function()
 if not player(1) then return end
 total=total+1
 if total>5000 then report.status='Failed';report.error='No completed combat observation';save();os.exit(1) end
 if pending then
  local file=io.open('../../characters/SLUG/replays/CAPTURE/Anime_import'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);shot=shot+1;pending=nil;save() end
 end
 report.states_seen[tostring(stateNo())]=true
 if roundState()==1 and total%50==0 and shot<3 and not pending then pending={label='Natural entrance',file='Anime_import'..string.format('%03d',shot)..'.png',state=stateNo(),animation=anim()};screenshot() end
 if roundState()>=2 then
  if roundState()==2 then report.combat_ticks=report.combat_ticks+1 end
  player(2);report.damage=math.max(report.damage,1000-life());player(1)
  if not pending and (report.combat_ticks%60==0 or report.damage>0) and shot<12 then pending={label='Natural AI combat',file='Anime_import'..string.format('%03d',shot)..'.png',state=stateNo(),animation=anim(),target_damage=report.damage,form=var(2)};screenshot() end
  if (report.damage>0 and report.combat_ticks>80 or report.combat_ticks>=1800 or roundState()>2) and not pending then
   report.passed=report.damage>0 and report.combat_ticks>0;report.status=report.passed and 'Complete' or 'Failed';save();os.exit(report.passed and 0 or 1)
  end
 end
end)
'''.replace('SLUG',slug).replace('CAPTURE',capture)
 mod='external/mods/-anime-import-startup-'+slug+'.lua';(E/mod).write_text(code)
 config=(E/'save/config.ini').read_text();values={'Modules':mod,'ScreenshotFolder':'../../characters/'+slug+'/replays/'+capture+'/','WindowTitle':'Anime_import','MasterVolume':'0'}
 for key,value in values.items():config=re.sub(r'(?im)^'+key+r'\s*=.*$',key+' = '+value,config)
 ini='save/anime-import-startup-'+slug+'.ini';(E/ini).write_text(config)
 args=['-config',ini,'-loadmotif','-p1',slug,'-p2','kfm','-p1.ai','5','-p2.ai','0','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
 cmd='$g=Start-Process -FilePath '+quote(E/'Ikemen_GO.exe')+' -WorkingDirectory '+quote(E)+' -ArgumentList @('+','.join(map(quote,args))+') -WindowStyle Hidden -RedirectStandardOutput '+quote(f/'startup-stdout.log')+' -RedirectStandardError '+quote(f/'startup-stderr.log')+' -PassThru; $null=$g.Handle; $g.WaitForExit(); exit $g.ExitCode'
 result=subprocess.run(['powershell','-NoProfile','-Command',cmd],cwd=R,timeout=180)
 if result.returncode:raise RuntimeError(slug+' engine failed: '+(f/'startup-stderr.log').read_text(errors='replace')[-4000:])
 d=json.loads((f/'startup-validation.json').read_text());assert d['status']=='Complete' and d['passed'],d;d['capture_directory']=capture;manifest=json.loads((f/'import-report.json').read_text());d['runtime_sha256']={name:hashlib.sha256((E/'chars'/slug/name).read_bytes()).hexdigest() for name in manifest['source_files_sha256']};(f/'startup-validation.json').write_text(json.dumps(d,indent=2))
 for frame in d['frames']:assert (folder/frame['file']).is_file()
 print('ANIME_NATIVE_STARTUP_PASS',slug,d['damage'],len(d['frames']),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for result in pool.map(run,['naruto','saitama']):pass
