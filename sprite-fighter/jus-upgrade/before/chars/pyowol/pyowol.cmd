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
command.buffer.time=6

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
name="snare"
command=~x
time=1

[Command]
name="daggers"
command=/$F, ~x
time=15

[Command]
name="reel"
command=/$B, ~x
time=15

[Command]
name="step"
command=/$D, ~x
time=15

[Command]
name="super"
command=~y
time=1

[Command]
name="rain"
command=/$B, ~y
time=15

[Command]
name="prison"
command=/$F, ~y
time=15

[Command]
name="ultimate"
command=~z
time=1

[Command]
name="veil"
command=~w
time=1

[Command]
name="hold_charge"
command=/s
time=1

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

[State -1, ultimate]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=3000

trigger1=command="ultimate"
value=4000
ctrl=0

[State -1, prison]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=2000

trigger1=command="prison"
value=3200
ctrl=0

[State -1, rain]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=1500

trigger1=command="rain"
value=3100
ctrl=0

[State -1, super]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=1000

trigger1=command="super"
value=3000
ctrl=0

[State -1, step]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=500
triggerall=var(10)=0

trigger1=command="step"
value=1200
ctrl=0

[State -1, daggers]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=500

trigger1=command="daggers"
value=1100
ctrl=0

[State -1, reel]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=500

trigger1=command="reel"
value=1120
ctrl=0

[State -1, snare]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=250
triggerall=numhelper(8100)=0
triggerall=var(11)=0

trigger1=command="snare"
value=1000
ctrl=0

[State -1, veil]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
triggerall=var(10)=0

trigger1=command="veil"
value=1300
ctrl=0

[State -1, hold_charge]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
triggerall=power<3000

trigger1=command="hold_charge"
value=500
ctrl=0

[State -1, H]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype=A
triggerall=ailevel=0

trigger1=command="H"
value=620
ctrl=0

[State -1, M]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype=A
triggerall=ailevel=0

trigger1=command="M"
value=610
ctrl=0

[State -1, L]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype=A
triggerall=ailevel=0

trigger1=command="L"
value=600
ctrl=0

[State -1, H]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && stateno=410))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=command="holddown"

trigger1=command="H"
value=420
ctrl=0

[State -1, M]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && stateno=400))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=command="holddown"

trigger1=command="M"
value=410
ctrl=0

[State -1, L]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=command="holddown"

trigger1=command="L"
value=400
ctrl=0

[State -1, H]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && stateno=210))
triggerall=statetype!=A
triggerall=ailevel=0

trigger1=command="H"
value=220
ctrl=0

[State -1, M]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && stateno=200))
triggerall=statetype!=A
triggerall=ailevel=0

trigger1=command="M"
value=210
ctrl=0

[State -1, L]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0

trigger1=command="L"
value=200
ctrl=0

[State -1, holddown]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=stateno!=10

trigger1=command="holddown"
value=10
ctrl=0

[State -1, holdup]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=1

trigger1=command="holdup"
value=40
ctrl=0

[State -1, holdfwd]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=stateno=0

trigger1=command="holdfwd"
value=20
ctrl=0

[State -1, holdback]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=stateno=0

trigger1=command="holdback"
value=21
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
value=4000
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=1000
triggerall=p2bodydist x<330
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
triggerall=p2bodydist x<200
triggerall=random<65
trigger1=1
value=210
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=500
triggerall=p2bodydist x>220
triggerall=numproj=0
triggerall=random<25
trigger1=1
value=1100
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=stateno=0
triggerall=p2bodydist x>160
trigger1=1
value=20
ctrl=0
