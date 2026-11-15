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
command.buffer.time=1

[Command]
name="a"
command=a
time=1

[Command]
name="b"
command=b
time=1

[Command]
name="c"
command=c
time=1

[Command]
name="hold_s"
command=/s
time=1

[Command]
name="taunt"
command=w
time=1

[Command]
name="evade"
command=d
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

[Command]
name="palm"
command=x
time=1

[Command]
name="piercer"
command=/$F,x
time=1

[Command]
name="stop"
command=/$B,x
time=1

[Command]
name="orb"
command=/$D,x
time=1

[Command]
name="butterfly"
command=y
time=1

[Command]
name="shield"
command=/$B,y
time=1

[Command]
name="wave"
command=/$F,y
time=1

[Command]
name="ultimate"
command=z
time=1

[Statedef -1]

[State -1, Silent Step]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=700
trigger1=command="piercer"
value=1100
ctrl=0

[State -1, Snow Flower Reversal]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=600
trigger1=command="stop"
value=1200
ctrl=0

[State -1, Shadow Crescent]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=500
trigger1=command="orb"
value=1300
ctrl=0

[State -1, Iron Wall]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power>=1000
trigger1=command="shield"
value=2100
ctrl=0

[State -1, Black Horizon]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=2000
trigger1=command="wave"
value=2200
ctrl=0

[State -1, Drawing Cut]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=500
triggerall=command!="holdfwd"
triggerall=command!="holdback"
triggerall=command!="holddown"
trigger1=command="palm"
value=1000
ctrl=0

[State -1, Northern Threefold]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=1500
triggerall=command!="holdfwd"
triggerall=command!="holdback"
trigger1=command="butterfly"
value=2000
ctrl=0

[State -1, Ten Thousand Shadows]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=(ctrl || ((stateno=200 || stateno=210 || stateno=230 || stateno=240 || stateno=260) && movecontact && time>=8))
triggerall=power>=3000
trigger1=command="ultimate"
value=3000
ctrl=0

[State -1, form]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="taunt"
value=800
ctrl=0

[State -1, evade]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="evade"
value=900
ctrl=0

[State -1, hold_s]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=power<3000
trigger1=command="hold_s"
value=700
ctrl=0

[State -1, FF]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="FF"
value=100
ctrl=0

[State -1, BB]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="BB"
value=105
ctrl=0

[State -1, Air a]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="a"
value=600
ctrl=0

[State -1, Air b]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="b"
value=610
ctrl=0

[State -1, Air c]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype=A
triggerall=ctrl
trigger1=command="c"
value=620
ctrl=0

[State -1, Low a]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="a"
value=400
ctrl=0

[State -1, Low b]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="b"
value=410
ctrl=0

[State -1, Low c]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
triggerall=command="holddown"
trigger1=command="c"
value=420
ctrl=0

[State -1, Normal a]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="a"
value=200
ctrl=0

[State -1, Normal b]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="b"
value=230
ctrl=0

[State -1, Normal c]
type=ChangeState
triggerall=AILevel=0
triggerall=roundstate=2
triggerall=statetype!=A
triggerall=ctrl
trigger1=command="c"
value=260
ctrl=0

[State -1, CPU Shinwonryu]
type=ChangeState
triggerall=AILevel>0
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=power>=3000
triggerall=p2bodydist x<40
trigger1=random<25
value=3000
ctrl=0

[State -1, CPU palm]
type=ChangeState
triggerall=AILevel>0
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=power>=500
triggerall=p2bodydist x<38
trigger1=random<35
value=1000
ctrl=0

[State -1, CPU baang]
type=ChangeState
triggerall=AILevel>0
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=power>=500
triggerall=numhelper(10001)=0
triggerall=p2bodydist x>50
trigger1=random<18
value=1300
ctrl=0

[State -1, CPU strike]
type=ChangeState
triggerall=AILevel>0
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=p2bodydist x<35
trigger1=random<65
value=200
ctrl=0

[State -1, CPU approach]
type=ChangeState
triggerall=AILevel>0
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=stateno!=20
triggerall=p2bodydist x>=35
trigger1=random<60
value=20
ctrl=0
