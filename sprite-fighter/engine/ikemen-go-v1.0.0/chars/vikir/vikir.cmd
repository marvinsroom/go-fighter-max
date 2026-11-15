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
name="rise"
command=x
time=1

[Command]
name="retreat"
command=x
time=1

[Command]
name="super"
command=y
time=1

[Command]
name="drain"
command=y
time=1

[Command]
name="aura"
command=y
time=1

[Command]
name="ultimate"
command=z
time=1

[Command]
name="seven"
command=y+z
time=1

[Command]
name="form"
command=d
time=1

[Command]
name="base"
command=d
time=1

[Command]
name="step"
command=w
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

[Command]
name="guest_dolores"
command=y
time=1

[Command]
name="guest_camu"
command=z
time=1

[Command]
name="guest_aiyen"
command=z
time=1

[Command]
name="guest_sinclair"
command=z
time=1

[Command]
name="bow"
command=x
time=1

[Statedef -1]

[State -1, seven]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=2000
triggerall=command!="holddown"
triggerall=command!="holdback"
triggerall=command!="holdfwd"
trigger1=command="seven"
value=4000
ctrl=0

[State -1, guest_dolores]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=var(21)=0
triggerall=power>=1250
triggerall=command="holdfwd"
triggerall=command!="holddown"
trigger1=command="guest_dolores"
value=2000
ctrl=0

[State -1, guest_camu]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=var(21)=0
triggerall=power>=1250
triggerall=command="holdfwd"
triggerall=command!="holddown"
trigger1=command="guest_camu"
value=2010
ctrl=0

[State -1, guest_aiyen]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=var(21)=0
triggerall=power>=1000
triggerall=command="holdback"
triggerall=command!="holddown"
trigger1=command="guest_aiyen"
value=2020
ctrl=0

[State -1, guest_sinclair]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=var(21)=0
triggerall=power>=1250
triggerall=command="holddown"
trigger1=command="guest_sinclair"
value=2030
ctrl=0

[State -1, bow]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=map(vikir.form)=3
triggerall=command="holdfwd"
triggerall=command!="holddown"
trigger1=command="bow"
value=1400
ctrl=0

[State -1, base]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
triggerall=command="holddown"
trigger1=command="base"
value=710
ctrl=0

[State -1, form]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
triggerall=command!="holddown"
trigger1=command="form"
value=700
ctrl=0

[State -1, ultimate]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=3000
triggerall=command!="holdfwd"
triggerall=command!="holdback"
triggerall=command!="holddown"
trigger1=command="ultimate"
value=4500
ctrl=0

[State -1, aura]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=1000
triggerall=command="holddown"
triggerall=var(20)=0
trigger1=command="aura"
value=800
ctrl=0

[State -1, drain]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=1500
triggerall=command="holdback"
triggerall=command!="holddown"
trigger1=command="drain"
value=3100
ctrl=0

[State -1, super]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=1000
triggerall=command!="holddown"
triggerall=command!="holdback"
triggerall=command!="holdfwd"
trigger1=command="super"
value=3000
ctrl=0

[State -1, rise]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=500
triggerall=command="holddown"
trigger1=command="rise"
value=1100
ctrl=0

[State -1, retreat]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
triggerall=command="holdback"
triggerall=command!="holddown"
trigger1=command="retreat"
value=1200
ctrl=0

[State -1, skill]
type=ChangeState
triggerall=roundstate=2
triggerall=(ctrl || (movecontact && time>=8 && (stateno=[200,220] || stateno=[400,420])))
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=250
triggerall=command!="holddown"
triggerall=command!="holdback"
triggerall=map(vikir.form)!=3 || command!="holdfwd"
trigger1=command="skill"
value=1000
ctrl=0

[State -1, step]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel=0
triggerall=power>=0
trigger1=command="step"
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
triggerall=p2bodydist x<260
triggerall=random<14
trigger1=1
value=4500
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=power>=1000
triggerall=p2bodydist x<200
triggerall=random<24
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
triggerall=p2bodydist x=[160,350]
triggerall=random<35
trigger1=1
value=1000
ctrl=0

[State -1, CPU]
type=ChangeState
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=ailevel>0
triggerall=p2bodydist x<150
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
triggerall=stateno=0
triggerall=p2bodydist x>150
trigger1=1
value=20
ctrl=0
