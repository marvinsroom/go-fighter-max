"""Opt-in native tests with Will as P1 and Urkel as P2."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1];ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';CHAR=ENGINE/'chars/urkel'
definition=(CHAR/'urkel.def').read_text().replace('st=urkel.cns','st=urkel.cns\nst1=urkel-tests.cns')
(CHAR/'urkel_test.def').write_text(definition,encoding='utf-8')
text='[Statedef -3]\n'
for i,name in enumerate(['L','M','H','skill','super_short','ultimate_short','throw','cheese','stumble','snap','retreat','transform'],1):
    text+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
text+='''
[State -3, Setup form]
type=VarSet
trigger1=map(test.form)>0
var(30)=map(test.form)-1
[State -3, Clear setup cooldown]
type=VarSet
trigger1=map(test.form)>0
var(31)=0
[State -3, Consume form setup]
type=MapSet
trigger1=map(test.form)>0
map="test.form"
value=0
[State -3, Robot seen]
type=MapSet
trigger1=numexplod(6402)>0 || numexplod(6403)>0
map="test.robotSeen"
value=1
[State -3, Robot missing during cinematic]
type=MapSet
triggerall=stateno=3210
triggerall=time>2 && time<238
trigger1=numexplod(6402)=0 && numexplod(6403)=0
map="test.robotMissing"
value=1
[State -3, Robot excluded from Stefan]
type=MapSet
triggerall=var(30)=1
trigger1=numexplod(6402)>0 || numexplod(6403)>0
map="test.robotLeak"
value=1
[State -3, Back throw]
type=AssertCommand
trigger1=map(test.backthrow)>0
name="holdback"
[State -3, Consume pulse]
type=MapSet
trigger1=map(test.pulse)>0
map="test.pulse"
value=0
[State -3, Consume throw direction]
type=MapSet
trigger1=map(test.backthrow)>0
map="test.backthrow"
value=0
[State -3, Hold down]
type=AssertInput
trigger1=map(test.down)>0
flag=D
[State -3, Down command]
type=AssertCommand
trigger1=map(test.down)>0
name="holddown"
[State -3, Hold guard]
type=AssertInput
trigger1=map(test.guard)>0
flag=B
[State -3, Guard command]
type=AssertCommand
trigger1=map(test.guard)>0
name="holdback"
[State -3, Enter guard]
type=ChangeState
triggerall=map(test.guard)>0
trigger1=stateno=0 || stateno=10 || stateno=21
value=ifelse(map(test.down)>0,131,130)
ctrl=0
[State -3, Walk forward]
type=AssertCommand
trigger1=map(test.walk)=1
name="holdfwd"
[State -3, Walk back]
type=AssertCommand
trigger1=map(test.walk)=-1
name="holdback"
'''
(CHAR/'urkel-tests.cns').write_text(text,encoding='utf-8')
config=(ENGINE/'save/config.ini').read_text(encoding='utf-8-sig')
config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-urkel-combat-tests.lua',config,flags=re.M)
(ENGINE/'save/urkel-combat-tests.ini').write_text(config,encoding='utf-8')
print('URKEL_TEST_CONFIG_READY')
