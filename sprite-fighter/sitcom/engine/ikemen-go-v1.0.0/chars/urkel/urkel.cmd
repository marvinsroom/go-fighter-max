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
name="cheese"
command=D, DF, F, a
time=20

[Command]
name="stumble"
command=D, DB, B, b
time=20

[Command]
name="snap"
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
name="transform"
command=w
time=1

[Statedef -1]

[State -1, Become Stefan]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=0
triggerall=var(31)=0
triggerall=power>=1000
trigger1=command="transform"
value=3900
ctrl=0

[State -1, Return to Steve]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=var(31)=0
trigger1=command="transform"
value=3901
ctrl=0

[State -1, Stefan ultimate_short]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=power>=2000
trigger1=command="ultimate_short"
value=4500
ctrl=0

[State -1, Stefan super_short]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=power>=1000
trigger1=command="super_short"
value=4400
ctrl=0

[State -1, Stefan cheese]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="cheese"
value=4300
ctrl=0

[State -1, Stefan snap]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="snap"
value=4310
ctrl=0

[State -1, Stefan retreat]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="retreat"
value=4330
ctrl=0

[State -1, Stefan skill]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="skill"
value=4300
ctrl=0

[State -1, Stefan stumble]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="stumble"
value=4300
ctrl=0

[State -1, Stefan low H]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=command="holddown"
trigger1=command="H"
value=4160
ctrl=0

[State -1, Stefan low M]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=command="holddown"
trigger1=command="M"
value=4150
ctrl=0

[State -1, Stefan low L]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=command="holddown"
trigger1=command="L"
value=4140
ctrl=0

[State -1, Stefan H]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="H"
value=4120
ctrl=0

[State -1, Stefan M]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="M"
value=4110
ctrl=0

[State -1, Stefan L]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
trigger1=command="L"
value=4100
ctrl=0

[State -1, Stefan air]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L" || command="M" || command="H"
value=4180
ctrl=0

[State -1, ultimate_short]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=2000
trigger1=command="ultimate_short"
value=3200
ctrl=0

[State -1, super_short]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="super_short"
value=3000
ctrl=0

[State -1, cheese]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="cheese"
value=1000
ctrl=0

[State -1, stumble]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="stumble"
value=1100
ctrl=0

[State -1, snap]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="snap"
value=1200
ctrl=0

[State -1, retreat]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="retreat"
value=1300
ctrl=0

[State -1, skill]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
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
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="H"
value=620
ctrl=0

[State -1, Air M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="M"
value=610
ctrl=0

[State -1, Air L]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L"
value=600
ctrl=0

[State -1, Low H]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=420
ctrl=0

[State -1, Low M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=410
ctrl=0

[State -1, Low L]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=400
ctrl=0

[State -1, H]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="H"
value=220
ctrl=0

[State -1, M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="M"
value=210
ctrl=0

[State -1, L]
type=ChangeState
triggerall=var(30)=0
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
triggerall=var(30)=0
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
