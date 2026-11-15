"""Install an opt-in test character/module; the normal Will DEF never loads it."""
from pathlib import Path
root=Path(__file__).resolve().parents[1];engine=root/'sprite-fighter/engine/ikemen-go-v1.0.0';char=engine/'chars/will_full'
definition=(char/'will_full.def').read_text().replace('st = will.cns','st = will.cns\nst1 = will-tests.cns')
(char/'will_test.def').write_text(definition,encoding='utf-8')
tests='[Statedef -3]\n'
commands=['L','M','H','skill','super_short','ultimate_short','throw','three','feint','freeze','windmill','taxi','M','transform']
for i,name in enumerate(commands,1):tests+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
tests+='''
[State -3, Hold test walk forward]
type=AssertCommand
trigger1=map(test.walk)=1
name="holdfwd"
[State -3, Hold test walk backward]
type=AssertCommand
trigger1=map(test.walk)=-1
name="holdback"
[State -3, Track foreign cinematic]
type=MapSet
triggerall=var(30)=1
trigger1=numexplod(6000)>0 || numexplod(6001)>0 || numexplod(6400)>0 || numexplod(6401)>0
map="test.foreignCinematic"
value=1
[State -3, Track Agent backdrop]
type=MapSet
trigger1=numexplod(6420)>0
map="test.agentBackdrop"
value=1
[State -3, Track orbital beam]
type=MapSet
trigger1=numexplod(6422)>0
map="test.agentBeam"
value=1
[State -3, Test form]
type=VarSet
trigger1=map(test.form)>0
var(30)=map(test.form)-1
[State -3, Test cooldown]
type=VarSet
trigger1=map(test.form)>0
var(31)=0
[State -3, Test flash cooldown]
type=VarSet
trigger1=map(test.form)>0
var(32)=0
[State -3, Consume form setup]
type=MapSet
trigger1=map(test.form)>0
map="test.form"
value=0
[State -3, Forward medium direction]
type=AssertCommand
trigger1=map(test.pulse)=13
name="holdfwd"
[State -3, Consume test command]
type=MapSet
trigger1=map(test.pulse)>0
map="test.pulse"
value=0
[State -3, Hold test down]
type=AssertInput
trigger1=map(test.down)>0
flag=D
[State -3, Down command]
type=AssertCommand
trigger1=map(test.down)>0
name="holddown"
[State -3, Hold test back]
type=AssertInput
trigger1=map(test.guard)>0
flag=B
[State -3, Back command]
type=AssertCommand
trigger1=map(test.guard)>0
name="holdback"
[State -3, Back throw direction]
type=AssertCommand
trigger1=map(test.backthrow)>0
name="holdback"
[State -3, Consume back throw direction]
type=MapSet
trigger1=map(test.backthrow)>0
map="test.backthrow"
value=0
[State -3, Stay in real guard states]
type=ChangeState
triggerall=map(test.guard)>0
trigger1=stateno=0 || stateno=10 || stateno=21
value=ifelse(map(test.down)>0,131,130)
ctrl=0
[Statedef 9001]
type=S
physics=N
ctrl=0
[State 9001, Far whiff target]
type=PosSet
trigger1=1
x=600
y=0
[State 9001, Stop]
type=VelSet
trigger1=1
x=0
y=0
[State 9001, Reset]
type=ChangeState
trigger1=1
value=0
ctrl=1
'''
(char/'will-tests.cns').write_text(tests,encoding='utf-8')
config=(engine/'save/config.ini').read_text(encoding='utf-8-sig')
import re
config=re.sub(r'^Modules\s*=.*$', 'Modules = external/mods/-will-combat-tests.lua',config,flags=re.M)
(engine/'save/will-combat-tests.ini').write_text(config,encoding='utf-8')
(engine/'external/mods').mkdir(exist_ok=True)
print('WILL_TEST_CONFIG_READY')
