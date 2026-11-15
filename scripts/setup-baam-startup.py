"""Observe the real production entrance and CPU, without forcing any fighter state."""
from baam_model import *
import re,sys

capture=sys.argv[1] if len(sys.argv)>1 else 'startup-cpu-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Choose a new startup capture folder'
code='''local report={status='Running',intro_seen=false,cuff_seen=false,attack_seen=false,frames={}}
local tick,shot,pending=0,0,nil
hook.add('loop','baam-production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true;if spriteVar('group')==62200 and spriteVar('image')==2 then report.cuff_seen=true end end
 if roundState()==2 then tick=tick+1;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/baam/replays/startup-cpu-v1/Baam_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='Baam_startup'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190) or (tick>0 and tick%20==0)) then
  pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};screenshot()
 end
 player(2);report.target_life=life();player(1)
 if tick>=200 or (tick>100 and roundState()>2) then
  report.status='Complete';report.passed=report.intro_seen and report.cuff_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/baam/startup-ai-validation.json');jsonEncode(report,'../../characters/baam/startup-ai-validation.json');print('BAAM_STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
'''
code=code.replace('startup-cpu-v1',capture)
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256']
bank='{'+','.join('['+json.dumps(k)+']='+json.dumps(v) for k,v in runtime.items())+'}'
code=code.replace('local report={','local report={runtime_sha256='+bank+',',1)
(E/'external/mods/-baam-startup.lua').write_text(code)
config=(E/'save/config.ini').read_text(encoding='utf-8-sig')
for key,value in [('Modules','external/mods/-baam-startup.lua'),('WindowTitle','Baam_startup'),('ScreenshotFolder','../../characters/baam/replays/'+capture+'/'),('MasterVolume','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/baam-startup.ini').write_text(config,encoding='utf-8')
print('BAAM_STARTUP_READY')
