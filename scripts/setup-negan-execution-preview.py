"""Native capture and assertions for the execution's setup, strike and aftermath."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
folder=ROOT/'sprite-fighter/characters/chappelle/replays/negan-execution-v1-final'
folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Preserve the previous take; choose a fresh folder.'
code='''
local tick,shot,pending=0,0,nil
local kneel,down,changes,oldLife=0,0,0,1000
local grounded,early=true,false
local report={method='Native renderer and real ultimate command route',capture_directory='negan-execution-v1-final',frames={}}
hook.add('loop','negan-execution-preview',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/chappelle/replays/negan-execution-v1-final/Negan_execution_preview'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  for p=1,2 do player(p);for _,k in ipairs({'pulse','form','guard','down','walk','charge'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then player(2);mapSet('test.form',2)
 elseif tick==20 then player(2);mapSet('test.pulse',6) end
 player(2);local actorState,actorTime,actorAnim=stateNo(),time(),anim()
 player(1);local targetState,targetAnim,targetLife=stateNo(),anim(),life()
 if targetState==8251 then kneel=kneel+1;grounded=grounded and math.abs(posY())<.1 end
 if targetState==8262 then down=down+1;grounded=grounded and math.abs(posY())<.1 end
 if targetLife~=oldLife then changes=changes+1;oldLife=targetLife end
 if actorState==13210 and actorTime<350 and targetLife~=1000 then early=true end
 if not pending and actorState==13210 and tick%4==0 then
  screenshot();pending={index=shot+1,tick=tick,state=actorState,state_time=actorTime,animation=actorAnim,target_state=targetState,target_animation=targetAnim,target_life=targetLife}
 end
 if tick>=640 then
  player(2);local recovered=stateNo()==10000
  player(1);recovered=recovered and stateNo()==0
  report.checks={kneeling_ticks=kneel,down_ticks=down,grounded=grounded,no_early_damage=not early,damage=1000-life(),damage_changes=changes,recovered=recovered}
  report.passed=kneel>=300 and down>=30 and grounded and not early and 1000-life()==950 and changes==1 and recovered
  jsonEncode(report,'../../characters/chappelle/negan-execution-preview-report.json');print('NEGAN_EXECUTION_COMPLETE '..tostring(report.passed)..' '..shot);os.exit()
 end
end)
'''
(E/'external/mods/-negan-execution-preview.lua').write_text(code)
config=(E/'save/tyrone-signature-preview.ini').read_text()
for key,value in [('Modules','external/mods/-negan-execution-preview.lua'),('ScreenshotFolder','../../characters/chappelle/replays/negan-execution-v1-final/'),('WindowTitle','Negan_execution_preview')]:
    config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/negan-execution-preview.ini').write_text(config)
print('NEGAN_EXECUTION_PREVIEW_READY')
