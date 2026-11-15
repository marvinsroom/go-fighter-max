"""Production intro/CPU observation; never forces player states."""
from manhwa_fighters import *
import re,sys
p=profile(sys.argv[1]);capture=sys.argv[2];assert re.fullmatch('[a-z0-9-]+',capture)
S=p['folder'];folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('*.png'))
code='''local report={status='Running',intro_seen=false,attack_seen=false,frames={},states_seen={}}
local tick,shot,pending,introShots=0,0,nil,0
hook.add('loop','production-startup',function()
 if not player(1) then return end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then report.intro_seen=true end
 if roundState()==2 then tick=tick+1;report.states_seen[tostring(state)]=true;if state==200 or state==210 or state==220 or state>=1000 then report.attack_seen=true end end
 if pending then
  local f=io.open('../../characters/SLUG/replays/CAPTURE/TITLE'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='TITLE'..string.format('%03d',shot)..'.png';report.frames[#report.frames+1]=pending;pending=nil;shot=shot+1 end
 end
 if not pending and shot<24 and ((roundState()<2 and state==190 and introShots<4) or (tick>0 and tick%20==0)) then pending={state=state,group=spriteVar('group'),drawing=spriteVar('image'),tick=tick};if tick==0 then introShots=introShots+1 end;screenshot() end
 player(2);report.target_life=life();player(1)
 if (tick>=240 and report.attack_seen and report.target_life<1000) or tick>=900 or (tick>100 and roundState()>2) then
  report.status='Complete';report.observed_ticks=tick;report.passed=report.intro_seen and report.attack_seen and report.target_life<1000
  os.remove('../../characters/SLUG/startup-ai-validation.json');jsonEncode(report,'../../characters/SLUG/startup-ai-validation.json');print('STARTUP_AI '..tostring(report.passed));os.exit()
 end
end)
'''.replace('SLUG',p['slug']).replace('CAPTURE',capture).replace('TITLE',p['capture']+'_startup')
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256'];bank='{'+','.join('['+json.dumps(k)+']='+json.dumps(v) for k,v in runtime.items())+'}'
code=code.replace('local report={','local report={runtime_sha256='+bank+',',1)
(E/'external/mods'/('-'+p['id']+'-startup.lua')).write_text(code)
config=(E/'save/config.ini').read_text(encoding='utf-8-sig')
for key,value in [('Modules','external/mods/-'+p['id']+'-startup.lua'),('WindowTitle',p['capture']+'_startup'),('ScreenshotFolder','../../characters/'+p['slug']+'/replays/'+capture+'/'),('MasterVolume','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save'/(p['id']+'-startup.ini')).write_text(config,encoding='utf-8')
print('MANHWA_STARTUP_READY',p['name'])
