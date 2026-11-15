"""Observe the real production round entrance without forcing a character state."""
from jin_mori_assets import *
import re,sys

capture=sys.argv[1] if len(sys.argv)>1 else 'startup-v2'
assert re.fullmatch('[a-z0-9-]+',capture)
p=S/'replays'/capture;p.mkdir(parents=True,exist_ok=True)
assert not list(p.glob('*.png')),'Use a fresh directory'
code='''local tick,shot,ready,pending=0,0,0,nil
local report={status='Running',intro_seen=false,greeting_seen=false,frames={}}
hook.add('loop','mori-real-entrance',function()
 if not player(1) then return end
 tick=tick+1
 if pending then
  local f=io.open('../../characters/jin-mori/replays/CAPTURE/Mori_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='Mori_startup'..string.format('%03d',shot)..'.png';table.insert(report.frames,pending);pending=nil;shot=shot+1 end
 end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then
  report.intro_seen=true
  if spriteVar('group')==62302 and spriteVar('image')==3 then report.greeting_seen=true end
  if tick%6==0 and not pending then
   pending={case_name='Natural round entrance',case_tick=tick,state=state,group=spriteVar('group'),drawing=spriteVar('image'),capture_directory='CAPTURE'};screenshot()
  end
 end
 if roundState()==2 then ready=ready+1 end
 if ready>=20 or tick>900 then
  report.status='Complete';report.passed=report.intro_seen and report.greeting_seen and ready>=20
  os.remove('../../characters/jin-mori/startup-validation.json');jsonEncode(report,'../../characters/jin-mori/startup-validation.json');print('MORI_STARTUP '..tostring(report.passed));os.exit()
 end
end)
'''.replace('CAPTURE',capture)
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256']
bank='{'+','.join('['+json.dumps(k)+']='+json.dumps(v) for k,v in runtime.items())+'}'
code=code.replace('local report={','local report={runtime_sha256='+bank+',',1)
(E/'external/mods/-mori-startup.lua').write_text(code)
config=(E/'save/config.ini').read_text(encoding='utf-8')
for key,value in [('Modules','external/mods/-mori-startup.lua'),('WindowTitle','Mori_startup'),('ScreenshotFolder','../../characters/jin-mori/replays/'+capture+'/'),('MasterVolume','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/mori-startup.ini').write_text(config,encoding='utf-8')
print('MORI_STARTUP_READY')
