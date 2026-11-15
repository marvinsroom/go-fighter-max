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
name="special_light"
command=D, DF, F, a
time=20

[Command]
name="special_medium"
command=D, DF, F, b
time=20

[Command]
name="special_heavy"
command=D, DF, F, c
time=20

[Command]
name="back_light"
command=D, DB, B, a
time=20

[Command]
name="back_medium"
command=D, DB, B, b
time=20

[Command]
name="back_heavy"
command=D, DB, B, c
time=20

[Command]
name="anti_air"
command=F, D, DF, c
time=20

[Command]
name="side_switch"
command=D, D, x
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
name="signature"
command=x+c
time=1
[Command]
name="holdskill"
command=/x
time=1
[Command]
name="holdheavy"
command=/c
time=1

[Statedef -1]

[State -1, Toggle paired form]
type=ChangeState
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=var(47)=0
trigger1=command="transform"
value=3900
ctrl=0

[State -1, Ankle-Breaker]
type=ChangeState
triggerall=roundstate=2
triggerall=var(45)=0
triggerall=ctrl
triggerall=statetype!=A
trigger1=command="signature"
value=1500
ctrl=0

[State -1, Purple Skyhook]
type=ChangeState
triggerall=roundstate=2
triggerall=var(45)=0
triggerall=ctrl
triggerall=statetype=A
trigger1=command="skill"
value=1510
ctrl=0

[State -1, Couch Surfboard]
type=ChangeState
triggerall=roundstate=2
triggerall=var(45)=1
triggerall=ctrl
triggerall=statetype!=A
trigger1=command="signature"
value=11500
ctrl=0

[State -1, Platform Pogo]
type=ChangeState
triggerall=roundstate=2
triggerall=var(45)=1
triggerall=ctrl
triggerall=statetype=A
trigger1=command="skill"
value=11510
ctrl=0
[State -1, ultimate_short]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=2000
trigger1=command="ultimate_short"
value=3200
ctrl=0

[State -1, super_short]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="super_short"
value=3000
ctrl=0

[State -1, special_light]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="special_light"
value=1000
ctrl=0

[State -1, special_medium]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="special_medium"
value=1010
ctrl=0

[State -1, special_heavy]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=numproj=0
trigger1=command="special_heavy"
value=1020
ctrl=0

[State -1, back_light]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_light"
value=1400
ctrl=0

[State -1, back_medium]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_medium"
value=1110
ctrl=0

[State -1, back_heavy]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_heavy"
value=1120
ctrl=0

[State -1, anti_air]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="anti_air"
value=1200
ctrl=0

[State -1, side_switch]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="side_switch"
value=1130
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="skill"
value=1130
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdback"
trigger1=command="skill"
value=1120
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdfwd"
trigger1=command="skill"
value=1110
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=1
trigger1=command="skill"
value=1100
ctrl=0

[State -1, Stance branch]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,26]
triggerall=numproj=0
trigger1=command="L"
value=1000
ctrl=0

[State -1, Stance branch]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,26]
trigger1=command="M"
value=1130
ctrl=0

[State -1, Stance branch]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=stateno=1100
triggerall=time=[8,26]
trigger1=command="H"
value=1200
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=var(45)=0
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
triggerall=var(45)=0
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
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="H"
value=620
ctrl=0

[State -1, Air M]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="M"
value=610
ctrl=0

[State -1, Air L]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L"
value=600
ctrl=0

[State -1, Low H]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=420
ctrl=0

[State -1, Low M]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=410
ctrl=0

[State -1, Low L]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=400
ctrl=0

[State -1, H]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="H"
value=220
ctrl=0

[State -1, M]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="M"
value=210
ctrl=0

[State -1, L]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="L"
value=200
ctrl=0

[State -1, Crouch]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno!=10
trigger1=command="holddown"
value=10
ctrl=0

[State -1, Jump]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="holdup"
value=40
ctrl=0

[State -1, Forward]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=0
trigger1=command="holdfwd"
value=20
ctrl=0

[State -1, Back]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=0
trigger1=command="holdback"
value=21
ctrl=0

[State -1, CPU attack]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=p2bodydist x<180
trigger1=random<35
value=210
ctrl=0

[State -1, CPU approach]
type=ChangeState
triggerall=var(45)=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=stateno=0
trigger1=p2bodydist x>160
value=20
ctrl=0
[State -1, ultimate_short]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=2000
trigger1=command="ultimate_short"
value=13200
ctrl=0

[State -1, super_short]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="super_short"
value=13000
ctrl=0

[State -1, special_light]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="special_light"
value=11000
ctrl=0

[State -1, special_medium]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="special_medium"
value=11010
ctrl=0

[State -1, special_heavy]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="special_heavy"
value=11020
ctrl=0

[State -1, back_light]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_light"
value=11120
ctrl=0

[State -1, back_medium]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_medium"
value=11110
ctrl=0

[State -1, back_heavy]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="back_heavy"
value=11120
ctrl=0

[State -1, anti_air]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="anti_air"
value=11200
ctrl=0

[State -1, side_switch]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="side_switch"
value=11130
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="skill"
value=11130
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdback"
trigger1=command="skill"
value=11120
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holdfwd"
trigger1=command="skill"
value=11110
ctrl=0

[State -1, Skill route]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=1
trigger1=command="skill"
value=11100
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=p2bodydist x<75
triggerall=p2statetype!=A
triggerall=p2movetype!=H
trigger1=command="throw" && command="holdback"
value=10810
ctrl=0

[State -1, Throw]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=p2bodydist x<75
triggerall=p2statetype!=A
triggerall=p2movetype!=H
trigger1=command="throw" && command!="holdback"
value=10800
ctrl=0

[State -1, Air H]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="H"
value=10620
ctrl=0

[State -1, Air M]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="M"
value=10610
ctrl=0

[State -1, Air L]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="L"
value=10600
ctrl=0

[State -1, Low H]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="H"
value=10420
ctrl=0

[State -1, Low M]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="M"
value=10410
ctrl=0

[State -1, Low L]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="L"
value=10400
ctrl=0

[State -1, H]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="H"
value=10220
ctrl=0

[State -1, M]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="M"
value=10210
ctrl=0

[State -1, L]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="L"
value=10200
ctrl=0

[State -1, Crouch]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno!=10010
trigger1=command="holddown"
value=10010
ctrl=0

[State -1, Jump]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="holdup"
value=10040
ctrl=0

[State -1, Forward]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=10000
trigger1=command="holdfwd"
value=10020
ctrl=0

[State -1, Back]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=stateno=10000
trigger1=command="holdback"
value=10021
ctrl=0

[State -1, CPU attack]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=p2bodydist x<180
trigger1=random<35
value=10210
ctrl=0

[State -1, CPU approach]
type=ChangeState
triggerall=var(45)=1
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=ailevel>0
triggerall=stateno=10000
trigger1=p2bodydist x>160
value=10020
ctrl=0
