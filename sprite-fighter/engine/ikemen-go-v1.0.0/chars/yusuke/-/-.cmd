
[Remap]
x=x
y=y
z=z
a=a
b=b
c=c
s=s

[Command]
name="Full Jump"
Command=~D,U
time=10

[Command]
name="ULTIMATE 1"
Command=~F,DF,D,DB,B,b
time=35

[Command]
name="SUPER FWD+A"
Command=~D,DF,F,D,DF,F,a
time=30

[Command]
name="SUPER FWD+B"
Command=~D,DF,F,D,DF,F,b
time=30

[Command]
name="SUPER FWD+C"
Command=~D,DF,F,D,DF,F,c
time=30

[Command]
name="SUPER BACK+A"
Command=~D,DB,B,D,DB,B,a
time=30

[Command]
name="SUPER BACK+B"
Command=~D,DB,B,D,DB,B,b
time=30

[Command]
name="SUPER BACK+C"
Command=~D,DB,B,D,DB,B,c
time=30

[Command]
name="SPECIAL1"
Command=~D,DF,F,a
time=15

[Command]
name="SPECIAL2"
Command=~D,DB,B,a
time=15

[Command]
name="SPECIAL3"
Command=~D,DF,F,b
time=15

[Command]
name="SPECIAL4"
Command=~D,DB,B,b
time=15

[Command]
name="SPECIAL5"
Command=~D,DF,F,c
time=15

[Command]
name="SPECIAL6"
Command=~D,DB,B,c
time=15

[Defaults]

[Command]
name="FF"
Command=F,F
time=10

[Command]
name="BB"
Command=B,B
time=10

[Command]
name="recovery"
Command=x+y
time=1

[Command]
name="recovery"
Command=y+z
time=1

[Command]
name="recovery"
Command=x+z
time=1

[Command]
name="recovery"
Command=a+b
time=1

[Command]
name="recovery"
Command=b+c
time=1

[Command]
name="recovery"
Command=a+c
time=1

[Command]
name="back_x"
Command=/$B,x
time=1

[Command]
name="back_y"
Command=/$B,y
time=1

[Command]
name="back_z"
Command=/$B,z
time=1

[Command]
name="down_x"
Command=/$D,x
time=1

[Command]
name="down_y"
Command=/$D,y
time=1

[Command]
name="down_z"
Command=/$D,z
time=1

[Command]
name="fwd_x"
Command=/$F,x
time=1

[Command]
name="fwd_y"
Command=/$F,y
time=1

[Command]
name="fwd_z"
Command=/$F,z
time=1

[Command]
name="up_x"
Command=/$U,x
time=1

[Command]
name="up_y"
Command=/$U,y
time=1

[Command]
name="up_z"
Command=/$U,z
time=1

[Command]
name="back_a"
Command=/$B,a
time=1

[Command]
name="back_b"
Command=/$B,b
time=1

[Command]
name="back_c"
Command=/$B,c
time=1

[Command]
name="down_a"
Command=/$D,a
time=1

[Command]
name="down_b"
Command=/$D,b
time=1

[Command]
name="down_c"
Command=/$D,c
time=1

[Command]
name="fwd_a"
Command=/$F,a
time=1

[Command]
name="fwd_b"
Command=/$F,b
time=1

[Command]
name="fwd_c"
Command=/$F,c
time=1

[Command]
name="up_a"
Command=/$U,a
time=1

[Command]
name="up_b"
Command=/$U,b
time=1

[Command]
name="up_c"
Command=/$U,c
time=1

[Command]
name="a"
Command=a
time=1

[Command]
name="b"
Command=b
time=1

[Command]
name="c"
Command=c
time=1

[Command]
name="x"
Command=x
time=1

[Command]
name="y"
Command=y
time=1

[Command]
name="z"
Command=z
time=1

[Command]
name="s"
Command=s
time=1

[Command]
name="fwd"
Command=$F
time=1

[Command]
name="downfwd"
Command=$DF
time=1

[Command]
name="down"
Command=$D
time=1

[Command]
name="downback"
Command=$DB
time=1

[Command]
name="back"
Command=$B
time=1

[Command]
name="upback"
Command=$UB
time=1

[Command]
name="up"
Command=$U
time=1

[Command]
name="upfwd"
Command=$UF
time=1

[Command]
name="hold_x"
Command=/x
time=1

[Command]
name="hold_y"
Command=/y
time=1

[Command]
name="hold_z"
Command=/z
time=1

[Command]
name="hold_a"
Command=/a
time=1

[Command]
name="hold_b"
Command=/b
time=1

[Command]
name="hold_c"
Command=/c
time=1

[Command]
name="hold_s"
Command=/s
time=1

[Command]
name="holdfwd"
Command=/$F
time=1

[Command]
name="holddownfwd"
Command=/$DF
time=1

[Command]
name="holddown"
Command=/$D
time=1

[Command]
name="holddownback"
Command=/$DB
time=1

[Command]
name="holdback"
Command=/$B
time=1

[Command]
name="holdupback"
Command=/$UB
time=1

[Command]
name="holdup"
Command=/$U
time=1

[Command]
name="holdupfwd"
Command=/$UF
time=1

[Command]
name="AI Prueba"
Command=y+z
time=1

[Command]
name="AI desactivado"
Command=b+c
time=1

[Statedef -1]

[State -1,Roll Var]
type=VarSet
trigger1=(Var(0)=0)&&(MoveType=H)&&(Command="a")
trigger2=(Var(0)=0)&&(MoveType=H)&&(Command="b")
trigger3=(Var(0)=0)&&(MoveType=H)&&(Command="c")
v=0
value=1

[State -1,Roll Var]
type=VarSet
trigger1=((Var(0)=1)&&(MoveType!=H))||(Lose)
v=0
value=0

[State -1,Power Charge]
type=ChangeState
TriggerALL=AiLevel=0
Triggerall=power<3000
Triggerall=statetype!=A
triggerall=Command="s"
trigger1=ctrl
value=500

[State -1,Air Dash Forward]
type=ChangeState
TriggerALL=AiLevel=0
triggerall=stateno!=110
triggerall=stateno!=115
value=110
trigger1=Command="FF"
trigger1=statetype=A
trigger1=ctrl

[State -1,Air Dash Backwards]
type=ChangeState
TriggerALL=AiLevel=0
triggerall=stateno!=110
triggerall=stateno!=115
value=115
trigger1=Command="BB"
trigger1=statetype=A
trigger1=ctrl

[State -1,Quick Step Forward]
type=ChangeState
TriggerALL=AiLevel=0
triggerall=stateno!=60
triggerall=stateno!=70
value=60
trigger1=Command="FF"
trigger1=statetype!=A
trigger1=ctrl

[State -1,Quick Step Backwards]
type=ChangeState
TriggerALL=AiLevel=0
triggerall=stateno!=60
triggerall=stateno!=70
value=70
trigger1=Command="BB"
trigger1=statetype!=A
trigger1=ctrl

[State -1,Full Jump]
type=ChangeState
TriggerALL=AiLevel=0
trigger1=Command="Full Jump"
trigger1=statetype=S
trigger1=ctrl
value=75

[State -1,ChangeState]
type=ChangeState
TriggerALL=AiLevel=0
triggerall=power>=2500
triggerall=!var(50)
triggerall=NumHelper(2015)=0
Triggerall=statetype!=A
triggerall=Command="holddown"
triggerall=Command="s"
value=2000
trigger1=ctrl

[State -1,ChangeState]
type=ChangeState
TriggerALL=AiLevel=0
Triggerall=teammode!=simul && enemynear,teammode!=simul
Triggerall=power>=3000
Triggerall=p2life<=lifemax/3
triggerall=Command="ULTIMATE 1"
Triggerall=statetype!=A
value=3000
trigger1=ctrl

[State -1,ChangeState]
type=ChangeState
TriggerALL=AiLevel=0
Triggerall=power>=1500
value=1550
triggerall=Command="SUPER FWD+B"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,ChangeState]
type=ChangeState
TriggerALL=AiLevel=0
Triggerall=power>=2000
Triggerall=NumHelper(1205)=0
Triggerall=NumHelper(1505)=0
value=1500
triggerall=Command="SUPER FWD+C"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,SPECIAL 1]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=Power>=1000
TriggerALL=Command="SPECIAL1"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1000

[State -1,SPECIAL 2]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=Power>=1000
TriggerALL=Command="SPECIAL2"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1050

[State -1,SPECIAL 3]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=NumHelper(1105)=0
TriggerALL=Power>=1000
TriggerALL=Command="SPECIAL3"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1100+((VAR(50)>0)*15)

[State -1,SPECIAL 4]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=Power>=1000
TriggerALL=Command="SPECIAL4"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1150

[State -1,SPECIAL 5]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=NumHelper(1205)=0
TriggerALL=NumHelper(1505)=0
TriggerALL=Power>=1250
TriggerALL=Command="SPECIAL5"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1200

[State -1,SPECIAL 6]
type=ChangeState
TriggerALL=AiLevel=0
TriggerALL=NumHelper(1255)=0
TriggerALL=NumHelper(1256)=0
TriggerALL=NumHelper(1257)=0
TriggerALL=Power>=1250
TriggerALL=Command="SPECIAL6"
TriggerALL=statetype!=A
Trigger1=!AiLevel
trigger1=ctrl
value=1250

[State 0,DisplayToClipboard]
Type=DisplayToClipboard
Trigger1=1
Text="Value=%d"
Params=var(45)
IgnoreHitPause=1

[State 0,AI_Check]
Type=Null
Trigger1=!SelfAnimExist(0)||!SelfAnimExist(2)||!SelfAnimExist(5305)||!SelfAnimExist(9998)
Trigger1=var(45):=1
Trigger1=Anim=0%Random%Alive%Time%1.1=Anim=0%Random%Alive%Time%1.1
Trigger2=!var(46)||!var(47)||!var(48)||!var(49)
Trigger2=var(45):=1
Trigger2=power%movehit%ctrl%random%1.1=power%movehit%ctrl%random%1.1
Trigger3=!NumHelper(15)
Trigger3=var(45):=1
Trigger3=powermax%ID%IsHelper%gametime%1.1=powermax%ID%IsHelper%gametime%1.1
IgnoreHitPause=1

[State 0,AI_Check 2]
Type=Explod
Trigger1=var(45)||!var(46)||!var(47)||!var(48)||!var(49)
Anim=0
Scale=0,0
RemoveTime=-1
IgnoreHitPause=1

[State 0,AI_Check 3]
Type=StopSnd
Trigger1=var(45)||!var(46)||!var(47)||!var(48)||!var(49)
Channel=-1
IgnoreHitPause=1

[State 0,AI_Check 4]
Type=Projectile
Trigger1=var(45)||!var(46)||!var(47)||!var(48)||!var(49)
ProjID=0
ProjAnim=0
ProjHitAnim=0
ProjRemAnim=0
ProjCancelAnim=0
ProjScale=0,0
ProjRemove=0
ProjRemoveTime=-1
Velocity=0,0
RemVelocity=0,0
Accel=0,0
VelMul=1.0,1.0
ProjHits=1
ProjPriority=1
ProjSprPriority=3
ProjEdgeBound=999999
ProjStageBound=999999
projHeightBound=999999,999999
OffSet=0,0
PosType=P1
projShadow=0,0,0
SuperMoveTime=0
PauseMoveTime=0

[State 0,AI_Check 5]
Type=Helper
Trigger1=var(45)||!var(46)||!var(47)||!var(48)||!var(49)
Name="9999"
ID=9999
StateNO=15
Pos=0,0
PosType=P1
Facing=1
KeyCtrl=0
OwnPal=0
SuperMoveTime=0
PauseMoveTime=0
IgnoreHitPause=1

[State -1,Down+A]
type=ChangeState
TriggerALL=AiLevel=0
value=285
triggerall=Command="holddown"
triggerall=Command="a"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,Down+B]
type=ChangeState
TriggerALL=AiLevel=0
value=290
triggerall=Command="holddown"
triggerall=Command="b"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,A Combo]
type=ChangeState
TriggerALL=AiLevel=0
value=200
triggerall=Command="a"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,B Combo]
type=ChangeState
TriggerALL=AiLevel=0
value=220
triggerall=Command="b"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,C Attack]
type=ChangeState
TriggerALL=AiLevel=0
value=240
triggerall=Command="c"
Triggerall=statetype!=A
trigger1=ctrl

[State -1,A Air Combo]
type=ChangeState
TriggerALL=AiLevel=0
value=250
triggerall=Command="a"
Triggerall=statetype=A
trigger1=ctrl

[State -1,B Air Combo]
type=ChangeState
TriggerALL=AiLevel=0
value=260
triggerall=Command="b"
Triggerall=statetype=A
trigger1=ctrl

[State -1,C Air Attack]
type=ChangeState
TriggerALL=AiLevel=0
value=270
triggerall=power>=200
triggerall=Command="c"
Triggerall=statetype=A
trigger1=ctrl
