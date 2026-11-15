"""Capture actual renderer frames with the engine's screenshot API."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
CAP=ROOT/'sprite-fighter/characters/yamal/replays/native-release';CAP.mkdir(parents=True,exist_ok=True)
config=(ENGINE/'save/yamal-combat-tests.ini').read_text()
config=re.sub(r'^VSync\s*=.*$','VSync = 1',config,flags=re.M)
config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-yamal-native-preview.lua',config,flags=re.M)
config=re.sub(r'^ScreenshotFolder\s*=.*$','ScreenshotFolder = ../../characters/yamal/replays/native-release/',config,flags=re.M)
config=re.sub(r'^WindowTitle\s*=.*$','WindowTitle = Yamal Native Review',config,flags=re.M)
(ENGINE/'save/yamal-native-preview.ini').write_text(config)
lua='''-- Opt-in visual replay: screenshots come directly from the real renderer.
local moves={
 {name='movement',length=230},
 {name='curler',pulse=8,length=120},
 {name='rainbow',pulse=9,length=120},
 {name='super',pulse=5,length=330},
 {name='ultimate',pulse=6,length=530},
}
local index,tick,shot=1,0,0
local pending=nil
local report={method='Native IKEMEN screenshot() frames; no simulated artwork',frames={}}
hook.add('loop','yamal-native-replay',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/yamal/replays/native-release/Yamal_Native_Review'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=moves[index]
 if not c then jsonEncode(report,'../../characters/yamal/native-preview-report.json');print('YAMAL_NATIVE_PREVIEW_COMPLETE '..shot);os.exit() end
 tick=tick+1
 if tick==1 then
  for p=1,2 do player(p);for _,k in ipairs({'pulse','down','guard','walk','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
 elseif tick==20 then
  player(2);if c.pulse then mapSet('test.pulse',c.pulse) end
 end
 if c.name=='movement' then
  player(2)
  if tick==20 then mapSet('test.walk',-1) end
  if tick==45 then mapSet('test.walk',0) end
  if tick==60 then mapSet('test.down',1) end
  if tick==85 then mapSet('test.down',0) end
  if tick==95 then changeState(40) end
  if tick==160 then mapSet('test.pulse',3) end
 end
 if not pending and tick>=14 and tick<c.length-4 and tick%6==2 then
  player(2);screenshot()
  pending={index=shot+1,move=c.name,tick=tick,state=stateNo(),animation=anim(),image=spriteVar('image'),life=life()}
 end
 if tick>=c.length then index=index+1;tick=0 end
end)
'''
(ENGINE/'external/mods/-yamal-native-preview.lua').write_text(lua)
print('YAMAL_NATIVE_PREVIEW_READY',CAP)
