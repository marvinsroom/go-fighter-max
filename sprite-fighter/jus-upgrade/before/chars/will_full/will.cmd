[Remap]
a=a
b=b
c=c
x=x
y=y
z=z
s=s
d=d
w=w
[Defaults]
command.time=20
command.buffer.time=3

[Command]
name="super"
command=D, DF, F, D, DF, F, c
time=32

[Command]
name="ultimate"
command=D, DB, B, D, DB, B, c
time=32

[Command]
name="three"
command=D, DF, F, a
time=20

[Command]
name="feint"
command=D, DB, B, a
time=20

[Command]
name="freeze"
command=D, DB, B, b
time=20

[Command]
name="windmill"
command=D, DF, F, c
time=20

[Command]
name="taxi"
command=D, DB, B, c
time=20

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

[State -1, Suit up]
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

[State -1, Return to Fresh Prince]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(30)=1
triggerall=var(31)=0
trigger1=command="transform"
value=3901
ctrl=0

[State -1, Galaxy Protocol]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=2000
trigger1=command="ultimate_short"
value=4500
ctrl=0

[State -1, Noisy Cricket Overload]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="super_short"
value=4400
ctrl=0

[State -1, Noisy Cricket]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="three"
value=4300
ctrl=0

[State -1, Deatomizer]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="windmill"
value=4310
ctrl=0

[State -1, Evasive Protocol]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="taxi"
value=4330
ctrl=0

[State -1, Neuralyzer]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(32)=0
triggerall=power>=250
trigger1=command="skill" || command="freeze"
value=4320
ctrl=0

[State -1, Agent air kick]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L" || command="M" || command="H"
value=4180
ctrl=0

[State -1, Agent crouch H]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=4160
ctrl=0

[State -1, Agent crouch M]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=4150
ctrl=0

[State -1, Agent crouch L]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=4140
ctrl=0

[State -1, Agent H]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="H"
value=4120
ctrl=0

[State -1, Agent M]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="M"
value=4110
ctrl=0

[State -1, Agent L]
type=ChangeState
triggerall=roundstate=2
triggerall=var(30)=1
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="L"
value=4100
ctrl=0

[State -1, ultimate]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit) || ((stateno=1000 || stateno=1010) && movehit)
triggerall=power>=2000
trigger1=command="ultimate" || command="ultimate_short"
value=3200
ctrl=0

[State -1, super]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit) || ((stateno=1000 || stateno=1010) && movehit)
triggerall=power>=1000
trigger1=command="super" || command="super_short"
value=3000
ctrl=0

[State -1, Run It Back]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=stateno=1010
triggerall=time=[12,28]
triggerall=power>=1000
trigger1=command="skill"
value=1100
ctrl=0

[State -1, three]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit)
trigger1=command="three"
value=1000
ctrl=0

[State -1, feint]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit)
trigger1=command="feint"
value=1050
ctrl=0

[State -1, freeze]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit)
trigger1=command="freeze"
value=1200
ctrl=0

[State -1, windmill]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit)
trigger1=command="windmill"
value=1300
ctrl=0

[State -1, taxi]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=[200,420]) && movehit)
trigger1=command="taxi"
value=1400
ctrl=0

[State -1, Three Piece second hit]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=stateno=1000
triggerall=time=[13,27]
trigger1=command="L" || command="M" || command="H"
value=1010
ctrl=0

[State -1, Three Piece ending L]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=stateno=1010
triggerall=time=[12,29]
trigger1=command="L"
value=1020
ctrl=0

[State -1, Three Piece ending M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=stateno=1010
triggerall=time=[12,29]
trigger1=command="M"
value=1030
ctrl=0

[State -1, Three Piece ending H]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=stateno=1010
triggerall=time=[12,29]
trigger1=command="H"
value=1040
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=p2bodydist x < 75
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
triggerall=p2bodydist x < 75
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

[State -1, Crouch H]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=420
ctrl=0

[State -1, Crouch M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=410
ctrl=0

[State -1, Crouch L]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=400
ctrl=0

[State -1, High Five]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdfwd"
trigger1=command="M"
value=280
ctrl=0

[State -1, Standing H]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=200 || stateno=210) && movehit)
trigger1=command="H"
value=220
ctrl=0

[State -1, Standing M]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((stateno=200) && movehit)
trigger1=command="M"
value=210
ctrl=0

[State -1, Standing L]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl || ((0) && movehit)
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

[State -1, Walk forward]
type=ChangeState
triggerall=roundstate=2
triggerall=stateno=0
triggerall=ctrl
trigger1=command="holdfwd"
value=20
ctrl=0

[State -1, Walk back]
type=ChangeState
triggerall=roundstate=2
triggerall=stateno=0
triggerall=ctrl
trigger1=command="holdback"
value=21
ctrl=0

[State -1, CPU basic punish]
type=ChangeState
triggerall=var(30)=0
triggerall=roundstate=2
triggerall=ailevel>0
triggerall=ctrl
triggerall=p2bodydist x<150
trigger1=random<35
value=210
ctrl=0

[State -1, CPU approach]
type=ChangeState
triggerall=roundstate=2
triggerall=ailevel>0
triggerall=ctrl
triggerall=stateno=0
trigger1=p2bodydist x>160
value=20
ctrl=0
