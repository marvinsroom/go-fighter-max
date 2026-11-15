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
name="curler"
command=D, DF, F, a
time=20

[Command]
name="curler_medium"
command=D, DF, F, b
time=20

[Command]
name="curler_heavy"
command=D, DF, F, c
time=20

[Command]
name="rainbow"
command=D, DB, B, a
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

[Statedef -1]

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

[State -1, curler]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="curler"
value=1000
ctrl=0

[State -1, curler_medium]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="curler_medium"
value=1010
ctrl=0

[State -1, curler_heavy]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="curler_heavy"
value=1020
ctrl=0

[State -1, rainbow]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="rainbow"
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

[State -1, Dribble route]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
triggerall=command="holddown"
trigger1=command="skill"
value=1130
ctrl=0

[State -1, Dribble route]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdback"
trigger1=command="skill"
value=1120
ctrl=0

[State -1, Dribble route]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdfwd"
trigger1=command="skill"
value=1110
ctrl=0

[State -1, Dribble route]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=1
trigger1=command="skill"
value=1100
ctrl=0

[State -1, Close Control branch]
type=ChangeState
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,22]
trigger1=command="H"
value=1200
ctrl=0

[State -1, Close Control branch]
type=ChangeState
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,22]
trigger1=command="M"
value=1110
ctrl=0

[State -1, Close Control branch]
type=ChangeState
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,22]
triggerall=numproj=0
trigger1=command="L"
value=1000
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

[State -1, CPU curler]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=p2bodydist x>180
triggerall=numproj=0
trigger1=random<25
value=1000
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
