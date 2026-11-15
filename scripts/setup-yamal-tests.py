"""Prepare isolated native tests without changing the normal play configuration."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
prep=(S/'prepare-urkel-combat-tests.py').read_text().replace('urkel','yamal').replace('Urkel','Yamal')
prep=prep.replace("'cheese','stumble','snap','retreat','transform'","'curler','rainbow','retreat','curler_medium','curler_heavy'")
# Remove robot/form instrumentation: Yamal has no transformation or summon.
prep=prep[:prep.index("text+='''")]+"text+='''\n"+prep[prep.index('[State -3, Back throw]'):]
exec(compile(prep,str(S/'prepare-yamal-tests.py'),'exec'),{'__file__':str(S/'prepare-yamal-tests.py')})
testconfig=ENGINE/'save/yamal-combat-tests.ini'
testconfig.write_text(re.sub(r'^VSync\s*=.*$','VSync = 0',testconfig.read_text(),flags=re.M))
lua=(ENGINE/'external/mods/-urkel-combat-tests.lua').read_text()
cases="""local cases={
 {name='Inside Tap',pulse=1,state=200,exact=30},
 {name='Turning Kick',pulse=2,state=210,exact=52},
 {name='Left-Foot Drive',pulse=3,state=220,exact=82},
 {name='Low Toe Poke',pulse=1,down=true,state=400,exact=26},
 {name='Slide Tackle',pulse=2,down=true,state=410,exact=58},
 {name='Rising Flick',pulse=3,down=true,state=420,exact=78},
 {name='Air Tap',pulse=1,jump=true,state=600,damage=true},
 {name='Air Volley',pulse=2,jump=true,state=610,damage=true},
 {name='Bicycle Volley',pulse=3,jump=true,state=620,damage=true},
 {name='Jump and land',jump=true},
 {name='Walk forward',walk=1,state=20,noDamage=true},
 {name='Walk backward',walk=-1,state=21,noDamage=true},
 {name='Forward challenge',pulse=7,state=801,exact=105},
 {name='Back challenge',pulse=7,back=true,state=811,exact=105},
 {name='Curler light',pulse=8,state=1000,exact=48},
 {name='Curler medium',pulse=11,state=1010,exact=60},
 {name='Curler heavy',pulse=12,state=1020,exact=72},
 {name='Close Control',pulse=4,state=1100,exact=45},
 {name='Cut Inside',pulse=4,walk=1,state=1110,exact=85},
 {name='Elastico',pulse=4,walk=-1,state=1120,exact=70},
 {name='Nutmeg',pulse=4,down=true,state=1130,exact=65},
 {name='Rainbow Flick',pulse=9,state=1200,exact=90},
 {name='Retreat',pulse=10,state=1400,noDamage=true},
 {name='Left-Foot Lightning',pulse=5,state=3010,exact=620,power=2000},
 {name='Super blocked',pulse=5,guard=true,notState=3010,noDamage=true,power=2000},
 {name='Super needs meter',pulse=5,meter=0,notState=3000,noDamage=true,power=0},
 {name='Super whiff',pulse=5,far=true,notState=3010,noDamage=true,power=2000},
 {name='World Is My Pitch',pulse=6,state=3210,exact=950,power=1000},
 {name='Ultimate full screen',pulse=6,far=true,state=3210,exact=950,power=1000},
 {name='Ultimate blocked',pulse=6,guard=true,notState=3210,noDamage=true,power=1000},
 {name='Ultimate needs meter',pulse=6,meter=1000,notState=3200,noDamage=true,power=1000},
 {name='Standing guard',defend=true,state=150,noDamage=true},
 {name='Crouch guard',defend=true,down=true,state=152,noDamage=true},
 {name='Thrown by Will',actor=1,pulse=7,state=801,exact=110},
 {name='Fresh Prince captures Yamal',actor=1,pulse=6,state=3210,exact=420},
 {name='Agent J captures Yamal',actor=1,agentWill=true,pulse=6,state=4510,exact=390},
 {name='Throw Agent J',agentWill=true,pulse=7,state=801,exact=105},
 {name='Ultimate captures Agent J',agentWill=true,pulse=6,state=3210,exact=950},
 {name='Close Control light branch',pulse=4,branch=1,state=1000},
 {name='Close Control medium branch',pulse=4,branch=2,state=1110},
 {name='Close Control heavy branch',pulse=4,branch=3,state=1200},
 {name='Curler blocked',pulse=8,guard=true,state=1000,noDamage=true},
 {name='Nutmeg blocked low',pulse=4,down=true,guard=true,targetDown=true,state=1130,noDamage=true},
}
"""
lua=lua[:lua.index('local cases=')]+cases+lua[lua.index('local filter='):]
lua=lua.replace('urkel','yamal').replace('Urkel','Yamal').replace('URKEL','YAMAL')
lua=lua.replace("if c.guard then mapSet('test.guard',1) end", "if c.guard then mapSet('test.guard',1);if c.targetDown then mapSet('test.down',1) end end")
lua=lua.replace(' if c.enemyAt', " if c.branch and tick==43 then player(actor);mapSet('test.pulse',c.branch) end\n if c.enemyAt")
lua=lua.replace('local correct=form==1 and (group==30 or group==10) or form==0 and (group==0 or group==20)','local correct=group==0 or group==50')
lua=lua.replace("  if c.name=='Yamal invention ultimate' and robotSeen~=1 then ok=false end",'')
lua=lua.replace("if c.far then changeState(9001) end", "if c.far then changeState(9001);player(actor);changeState(9001) end")
lua=lua.replace('((c.pulse==6 or c.pulse==5) and 440 or 280)','(c.pulse==6 and 600 or c.pulse==5 and 420 or 280)')
lua=lua.replace('  if c.exact or c.damage then','  if actorFinal~=0 and actorFinal~=10 and actorFinal~=130 and actorFinal~=131 and actorFinal~=140 then ok=false end\n  if c.exact or c.damage then')
(ENGINE/'external/mods/-yamal-combat-tests.lua').write_text(lua,encoding='utf-8')
# Isolated fixture for placing the target outside the short-range starter.
char=ENGINE/'chars/yamal'
with (char/'yamal-tests.cns').open('a') as f:f.write('\n[Statedef 9001]\ntype=S\nmovetype=I\nphysics=N\nanim=0\nctrl=0\n[State 9001, Far]\ntype=PosSet\ntrigger1=1\nx=ifelse(teamside=1,500,-500)\ny=0\n[State 9001, Ready]\ntype=ChangeState\ntrigger1=time>1\nvalue=0\nctrl=1\n')
launch=(S/'run-will-vs-urkel.ps1').read_text().replace('urkel','yamal')
launch=launch[:launch.index('Get-Process -Name')]+launch[launch.index("if($Mode -eq 'Tests')"):]
launch=launch.replace("@('-config'", "@('-speedtest','4','-config'")
launch=launch.replace('Write-Output "$Mode process: $($game.Id)"', 'Set-Content -LiteralPath (Join-Path $workspace "sprite-fighter/yamal-process.txt") -Value $game.Id\nWrite-Output "$Mode process: $($game.Id)"')
launch=launch.replace('$game=Start-Process', "$launchOptions=@{}\nif($Mode -eq 'Tests'){$launchOptions.WindowStyle='Hidden'}\n$game=Start-Process @launchOptions")
launch=launch.replace("[string]$Mode='Play')", "[string]$Mode='Play',[switch]$AsYamal)")
launch=launch.replace(" $arguments=@('-loadmotif','-p1','will_full','-p2','yamal'", " $firstFighter=if($AsYamal){'yamal'}else{'will_full'}\n $secondFighter=if($AsYamal){'will_full'}else{'yamal'}\n $arguments=@('-loadmotif','-p1',$firstFighter,'-p2',$secondFighter")
(S/'run-will-vs-yamal.ps1').write_text(launch,encoding='utf-8')
for name,mode in [('Play Will vs Yamal','Play'),('Fight CPU Yamal','CPU')]:
    (ROOT/'sprite-fighter'/f'{name}.cmd').write_text(f'@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-will-vs-yamal.ps1" -Mode {mode}\n')
(ROOT/'sprite-fighter/Play as Yamal.cmd').write_text('@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\\scripts\\run-will-vs-yamal.ps1" -Mode Play -AsYamal\n')
print('YAMAL_HARNESS_READY',43,'native checks')
