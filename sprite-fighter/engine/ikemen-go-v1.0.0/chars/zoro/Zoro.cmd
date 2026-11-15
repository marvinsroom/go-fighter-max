[Remap]
a=a
b=b
c=c
x=x
y=y
z=z
d=d
s=s
w=w
[Defaults]
command.time=15
command.buffer.time=4

[Command]
name="L"
command=a
time=1

[Command]
name="M"
command=b
time=1

[Command]
name="H"
command=c
time=1

[Command]
name="skill"
command=x
time=1

[Command]
name="rising"
command=/$D,x
time=15

[Command]
name="cyclone"
command=/$B,x
time=15

[Command]
name="super"
command=y
time=1

[Command]
name="tatsumaki"
command=/$B,y
time=15

[Command]
name="ultimate"
command=z
time=1

[Command]
name="holdcharge"
command=/s
time=1

[Command]
name="FF"
command=F,F
time=15

[Command]
name="BB"
command=B,B
time=15

[Command]
name="holdfwd"
command=/$F
time=1

[Command]
name="holdback"
command=/$B
time=1

[Command]
name="holddown"
command=/$D
time=1

[Command]
name="holdup"
command=/$U
time=1

[Statedef -1]

[State -1, San Zen Sekai]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=3000
trigger1=command="ultimate"
value=3200
ctrl=0

[State -1, Kokujou Oo Tatsumaki]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=2000
trigger1=command="tatsumaki"
value=3100
ctrl=0

[State -1, Rokudou no Tsuji]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=1000
triggerall=command!="holdback"
trigger1=command="super"
value=3000
ctrl=0

[State -1, Three Sword Cyclone]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=750
trigger1=command="cyclone"
value=1200
ctrl=0

[State -1, Rising Dragon]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=500
trigger1=command="rising"
value=1100
ctrl=0

[State -1, Oni Giri]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power>=250
triggerall=command!="holdback"
triggerall=command!="holddown"
trigger1=command="skill"
value=1000
ctrl=0

[State -1, Charge]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=power<3000
trigger1=command="holdcharge"
value=700
ctrl=0

[State -1, Forward dash]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
trigger1=command="FF"
value=100
ctrl=0

[State -1, Back dash]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
trigger1=command="BB"
value=105
ctrl=0

[State -1, Crouching cut]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=command="holddown"
trigger1=command="L"
value=400
ctrl=0

[State -1, Heavy cut]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=command!="holddown"
trigger1=command="H"
value=220
ctrl=0

[State -1, Sword cut]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=command!="holddown"
trigger1=command="M"
value=210
ctrl=0

[State -1, Quick strike]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel=0
triggerall=command!="holddown"
trigger1=command="L"
value=200
ctrl=0

[State -1, Air cut]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
triggerall=ailevel=0
trigger1=command="L"
value=600
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=3000
triggerall=p2bodydist x<230
triggerall=random<15
trigger1=1
value=3200
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=1000
triggerall=p2bodydist x<260
triggerall=random<30
trigger1=1
value=3000
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=250
triggerall=p2bodydist x<220
triggerall=random<40
trigger1=1
value=1000
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=p2bodydist x<160
triggerall=random<60
trigger1=1
value=210
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=p2bodydist x>=160
trigger1=1
value=20
ctrl=0
