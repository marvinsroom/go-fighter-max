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
command.time=20
command.buffer.time=3

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
name="super_short"
command=y
time=1

[Command]
name="ultimate_short"
command=z
time=1

[Command]
name="throw"
command=d
time=1

[Command]
name="transform"
command=w
time=1

[Command]
name="dagger"
command=D, DF, F, a
time=20

[Command]
name="knight"
command=D, DB, B, b
time=20

[Command]
name="lunge"
command=D, DF, F, c
time=20

[Command]
name="retreat"
command=D, DB, B, c
time=20

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

[Command]
name="step"
command=D, DF, F, b
time=20

[Command]
name="igris"
command=D, DB, B, a
time=20

[Command]
name="beru"
command=D, DB, B, b
time=20

[Command]
name="iron"
command=B, B, x
time=20

[Command]
name="tank"
command=D, D, x
time=20

[Statedef -1]

[State -1, Random shadow transformation]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="transform"
value=2000
ctrl=0

[State -1, ultimate_short]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=2000
trigger1=command="ultimate_short"
value=3200
ctrl=0

[State -1, super_short]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="super_short"
value=3000
ctrl=0

[State -1, dagger]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="dagger"
value=1000
ctrl=0

[State -1, igris]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
trigger1=command="igris"
value=1100
ctrl=0

[State -1, knight]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
trigger1=command="knight"
value=1110
ctrl=0

[State -1, beru]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
trigger1=command="beru"
value=1110
ctrl=0

[State -1, iron]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
trigger1=command="iron"
value=1120
ctrl=0

[State -1, tank]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
trigger1=command="tank"
value=1130
ctrl=0

[State -1, lunge]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="lunge"
value=1200
ctrl=0

[State -1, retreat]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="retreat"
value=1400
ctrl=0

[State -1, step]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="step"
value=1300
ctrl=0

[State -1, Choose named shadow]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
triggerall=command="holddown"
trigger1=command="skill"
value=1130
ctrl=0

[State -1, Choose named shadow]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
triggerall=command="holdback"
trigger1=command="skill"
value=1120
ctrl=0

[State -1, Choose named shadow]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
triggerall=command="holdfwd"
trigger1=command="skill"
value=1110
ctrl=0

[State -1, Choose named shadow]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=250
triggerall=var(31)=0
triggerall=1
trigger1=command="skill"
value=1100
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=p2bodydist x<75
triggerall=p2statetype!=A
triggerall=p2movetype!=H
trigger1=command="throw" && command="holdback"
value=810
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=p2bodydist x<75
triggerall=p2statetype!=A
triggerall=p2movetype!=H
trigger1=command="throw" && command!="holdback"
value=800
ctrl=0

[State -1, Air H]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="H"
value=620
ctrl=0

[State -1, Air M]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="M"
value=610
ctrl=0

[State -1, Air L]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L"
value=600
ctrl=0

[State -1, Low H]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=420
ctrl=0

[State -1, Low M]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=410
ctrl=0

[State -1, Low L]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=400
ctrl=0

[State -1, H]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="H"
value=220
ctrl=0

[State -1, M]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="M"
value=210
ctrl=0

[State -1, L]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="L"
value=200
ctrl=0

[State -1, Crouch]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno!=10
trigger1=command="holddown"
value=10
ctrl=0

[State -1, Jump]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="holdup"
value=40
ctrl=0

[State -1, Forward]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=0
trigger1=command="holdfwd"
value=20
ctrl=0

[State -1, Back]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=0
trigger1=command="holdback"
value=21
ctrl=0

[State -1, CPU attack]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=p2bodydist x<150
trigger1=random<35
value=210
ctrl=0

[State -1, CPU approach]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=stateno=0
trigger1=p2bodydist x>160
value=20
ctrl=0
