"""Check the Play as Yamal side and capture the opposite-facing finishers."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
cap=ROOT/'sprite-fighter/characters/yamal/replays/player-one';cap.mkdir(parents=True,exist_ok=True)
config=(ENGINE/'save/yamal-combat-tests.ini').read_text()
config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-yamal-p1-smoke.lua',config,flags=re.M)
config=re.sub(r'^ScreenshotFolder\s*=.*$','ScreenshotFolder = ../../characters/yamal/replays/player-one/',config,flags=re.M)
config=re.sub(r'^WindowTitle\s*=.*$','WindowTitle = Yamal Player One',config,flags=re.M)
(ENGINE/'save/yamal-p1-smoke.ini').write_text(config)
(ENGINE/'external/mods/-yamal-p1-smoke.lua').write_text('''
local index,tick=1,0
local cases={{name='Player one super',pulse=5,damage=620,length=420},{name='Player one ultimate',pulse=6,damage=950,length=600}}
local report={checks={},status='Running'}
hook.add('loop','yamal-p1-smoke',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/yamal/player-one-validation.json');print('YAMAL_P1_COMPLETE');os.exit() end
 tick=tick+1
 if tick==1 then for p=1,2 do player(p);changeState(9000) end end
 if tick==8 then for p=1,2 do player(p);setLife(1000);setPower(3000) end end
 if tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 player(1)
 if (stateNo()==3010 and (time()==175 or time()==195)) or (stateNo()==3210 and (time()==335 or time()==355)) then screenshot() end
 if tick>=c.length then
  local actorFinal=stateNo();player(2);local damage=1000-life();local targetFinal=stateNo()
  local ok=damage==c.damage and actorFinal==0 and targetFinal==0
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,actorFinal=actorFinal,targetFinal=targetFinal})
  print('YAMAL_P1 '..c.name..' '..tostring(ok)..' '..damage);index=index+1;tick=0
 end
end)
''')
print('YAMAL_P1_SMOKE_READY')
