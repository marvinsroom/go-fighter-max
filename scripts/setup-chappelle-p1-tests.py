"""Verify every finisher from the Player 1 launch side."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
for slug in ['prince','negan','rick']:
    cap=ROOT/'sprite-fighter/characters'/slug/'replays/player-one';cap.mkdir(parents=True,exist_ok=True)
    cases="{{name='P1 super',pulse=5,damage=620,length=420},{name='P1 ultimate',pulse=6,damage=950,length=600}"
    if slug=='rick':cases+=",{name='P1 Tyrone super',tyrone=true,pulse=5,damage=620,length=420},{name='P1 Tyrone ultimate',tyrone=true,pulse=6,damage=950,length=600}"
    cases+='}'
    code='''
local cases=CASES
local index,tick=1,0
local report={checks={},status='Running'}
hook.add('loop','SLUG-player-one-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then report.status='Complete';jsonEncode(report,'../../characters/SLUG/player-one-validation.json');print('CHAPPELLE_P1_COMPLETE SLUG');os.exit() end
 tick=tick+1
 if tick==1 then for p=1,2 do player(p);mapSet('test.form',0);changeState(9000) end end
 if tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  player(2);mapSet('test.form',1)
  if c.tyrone then player(1);mapSet('test.form',2) end
 end
 if tick==20 then player(1);mapSet('test.pulse',c.pulse) end
 player(1)
 if (stateNo()==3010 or stateNo()==4410) and (time()==175 or time()==195) or (stateNo()==3210 or stateNo()==4510) and (time()==335 or time()==355) then screenshot() end
 if tick>=c.length then
  local actorFinal=stateNo();player(2);local damage=1000-life();local targetFinal=stateNo()
  local ok=damage==c.damage and actorFinal==0 and targetFinal==0
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,actorFinal=actorFinal,targetFinal=targetFinal})
  print('CHAPPELLE_P1 '..c.name..' '..tostring(ok));index=index+1;tick=0
 end
end)
'''.replace('CASES',cases).replace('SLUG',slug)
    (E/'external/mods'/('-'+slug+'-p1-tests.lua')).write_text(code)
    config=(E/'save'/(slug+'-combat-tests.ini')).read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-p1-tests.lua',config,flags=re.M)
    config=re.sub(r'^ScreenshotFolder\s*=.*$','ScreenshotFolder = ../../characters/'+slug+'/replays/player-one/',config,flags=re.M)
    config=re.sub(r'^WindowTitle\s*=.*$','WindowTitle = Chappelle_'+slug+'_P1',config,flags=re.M)
    (E/'save'/(slug+'-p1-tests.ini')).write_text(config)
print('CHAPPELLE_PLAYER_ONE_READY 8 checks')
