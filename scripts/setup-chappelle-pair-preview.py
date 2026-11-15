"""Native demonstration of the corrected pair transforms and both kits."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
for slug in ['prince','tyrone']:
    cap=ROOT/'sprite-fighter/characters'/slug/'replays/paired-v2';cap.mkdir(parents=True,exist_ok=True)
    fixture=E/'chars'/slug/(slug+'-paired-tests.cns')
    text=fixture.read_text()
    if '[Statedef 9012]' not in text:text+='''
[Statedef 9012]
type=S
movetype=I
physics=N
ctrl=0
anim=ifelse(var(45)>0,10000,0)
[State 9012, Preserve form and refill health]
type=LifeSet
trigger1=1
value=1000
[State 9012, Refill meter]
type=PowerSet
trigger1=1
value=3000
[State 9012, Position]
type=PosSet
trigger1=1
x=ifelse(teamside=1,-60,60)
y=0
[State 9012, Stop]
type=VelSet
trigger1=1
x=0
y=0
[State 9012, Ready]
type=ChangeState
trigger1=time>1
value=ifelse(var(45)>0,10000,0)
ctrl=1
'''
    fixture.write_text(text)
    code='''
local tick,shot=0,0
local pending=nil
local report={method='Actual native engine; command asserted for each transform and move',capture_directory='paired-v2',frames={}}
hook.add('loop','SLUG-pair-preview',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/SLUG/replays/paired-v2/Chappelle_pair_SLUG'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then for p=1,2 do player(p);for _,k in ipairs({'pulse','walk','form','down','guard','backthrow'}) do mapSet('test.'..k,0) end;changeState(9000) end end
 if tick==20 or tick==540 then player(2);mapSet('test.pulse',13) end
 if tick==90 or tick==610 then player(2);mapSet('test.pulse',8) end
 if tick==150 or tick==520 or tick==700 then player(1);changeState(9000);player(2);changeState(9012) end
 if tick==170 then player(2);mapSet('test.pulse',5) end
 if tick==720 then player(2);mapSet('test.pulse',6) end
 if not pending and tick>=14 and tick<1310 and tick%8==6 then
  player(2);screenshot();pending={index=shot+1,tick=tick,state=stateNo(),animation=anim(),form=_G['var'](45),group=spriteVar('group')}
 end
 if tick>=1320 then jsonEncode(report,'../../characters/SLUG/paired-preview-report.json');print('PAIRED_PREVIEW_COMPLETE SLUG '..shot);os.exit() end
end)
'''.replace('SLUG',slug)
    (E/'external/mods'/('-'+slug+'-paired-preview.lua')).write_text(code)
    config=(E/'save'/(slug+'-paired-tests.ini')).read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-paired-preview.lua',config,flags=re.M)
    config=re.sub(r'^VSync\s*=.*$','VSync = 1',config,flags=re.M)
    config=re.sub(r'^ScreenshotFolder\s*=.*$','ScreenshotFolder = ../../characters/'+slug+'/replays/paired-v2/',config,flags=re.M)
    config=re.sub(r'^WindowTitle\s*=.*$','WindowTitle = Chappelle_pair_'+slug,config,flags=re.M)
    (E/'save'/(slug+'-paired-preview.ini')).write_text(config)
print('CHAPPELLE_PAIR_PREVIEW_READY')
