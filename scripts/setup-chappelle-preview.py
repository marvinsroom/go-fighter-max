"""Record the actual renderer, including Rick's real transformation command."""
from pathlib import Path
import re,sys,json
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';S=ROOT/'scripts'
def lua_value(v):
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,dict):return '{'+','.join(k+'='+lua_value(x) for k,x in v.items())+'}'
    if isinstance(v,list):return '{'+','.join(lua_value(x) for x in v)+'}'
    return str(v)
for slug in sys.argv[1:] or ['prince','negan','rick']:
    take='native-v2' if slug=='rick' else 'native-v1'
    cap=ROOT/'sprite-fighter/characters'/slug/'replays'/take;cap.mkdir(parents=True,exist_ok=True)
    title='Chappelle_'+slug
    config=(E/'save'/(slug+'-combat-tests.ini')).read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-native-preview.lua',config,flags=re.M)
    config=re.sub(r'^VSync\s*=.*$','VSync = 1',config,flags=re.M)
    config=re.sub(r'^ScreenshotFolder\s*=.*$','ScreenshotFolder = ../../characters/'+slug+'/replays/'+take+'/',config,flags=re.M)
    config=re.sub(r'^WindowTitle\s*=.*$','WindowTitle = '+title,config,flags=re.M)
    (E/'save'/(slug+'-native-preview.ini')).write_text(config)
    moves=[dict(name='movement',length=220),dict(name='special',pulse=8,length=120),dict(name='super',pulse=5,length=330),dict(name='ultimate',pulse=6,length=530)]
    if slug=='rick':moves += [dict(name='transformation',length=260),dict(name='tyrone-super',pulse=5,tyrone=True,length=330),dict(name='tyrone-ultimate',pulse=6,tyrone=True,length=530),dict(name='tyrone-reaction',pulse=7,actor=1,tyrone=True,length=200),dict(name='tyrone-agent-capture',pulse=6,actor=1,tyrone=True,agent=True,length=400)]
    lua='''
local moves=MOVES
local index,tick,shot=1,0,0
local pending=nil
local report={method='Actual native screenshot API with acknowledged image files',capture_directory='TAKE',frames={}}
hook.add('loop','SLUG-native-replay',function()
 if not player(1) or roundState()~=2 then return end
 if pending then
  local f=io.open('../../characters/SLUG/replays/TAKE/TITLE'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 local c=moves[index]
 if not c then jsonEncode(report,'../../characters/SLUG/native-preview-report.json');print('CHAPPELLE_PREVIEW_COMPLETE SLUG '..shot);os.exit() end
 tick=tick+1
 if tick==1 then
  for p=1,2 do player(p);for _,k in ipairs({'pulse','down','guard','walk','backthrow','form'}) do mapSet('test.'..k,0) end;changeState(9000) end
 elseif tick==8 then
  for p=1,2 do player(p);setLife(1000);setPower(3000) end
  if c.tyrone then player(2);mapSet('test.form',2) end
  if c.agent then player(1);mapSet('test.form',2) end
 elseif tick==20 then player(c.actor or 2);if c.pulse then mapSet('test.pulse',c.pulse) end end
 if c.name=='movement' then
  player(2)
  if tick==20 then mapSet('test.walk',-1) end
  if tick==45 then mapSet('test.walk',0) end
  if tick==60 then mapSet('test.down',1) end
  if tick==85 then mapSet('test.down',0) end
  if tick==95 then changeState(40) end
  if tick==160 then mapSet('test.pulse',3) end
 elseif c.name=='transformation' then
  player(2)
  if tick==20 or tick==150 then mapSet('test.pulse',13) end
  if tick==85 then mapSet('test.pulse',4) end
 end
 if not pending and tick>=14 and tick<c.length-4 and tick%8==6 then
  player(2);screenshot();pending={index=shot+1,move=c.name,tick=tick,state=stateNo(),animation=anim(),group=spriteVar('group'),form=_G['var'](45)}
 end
 if tick>=c.length then index=index+1;tick=0 end
end)
'''.replace('MOVES',lua_value(moves)).replace('SLUG',slug).replace('TITLE',title).replace('TAKE',take)
    (E/'external/mods'/('-'+slug+'-native-preview.lua')).write_text(lua)
    print('CHAPPELLE_PREVIEW_READY',slug)
