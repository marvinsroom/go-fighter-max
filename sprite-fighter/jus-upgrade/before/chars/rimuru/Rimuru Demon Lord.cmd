;===============================================================================
;-------------------------------Comandos----------------------------------------
;===============================================================================
[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
[command]
name = "a+b"
command = a+b
time = 15

s = s

[Command]
name = "Super Jump"
command = ~D,U
time = 10

;-| Supers |-------------------------------------------------------

[command]
name = "SUPER1"
command = ~z
time = 30

;-| Specials |-------------------------------------------------------
[command]
name = "SPECIAL 1"
command = ~D,DF,F,a
time = 15

[command]
name = "SPECIAL 2"
command = ~D,DB,B,a
time = 15

[command]
name = "SPECIAL 3"
command = ~D,DF,F,b
time = 15

[command]
name = "SPECIAL 4"
command = ~D,DB,B,b
time = 15

[command]
name = "SPECIAL 5"
command = ~D,DF,F,c
time = 15

[command]
name = "SPECIAL 6"
command = ~D,DB,B,c
time = 15

[command]
name = "SPECIAL 7"
command = ~B,DB,D,DF,F,a
time = 30

[command]
name = "SPECIAL 8"
command = ~F,DF,D,DB,B,a
time = 30

[command]
name = "SPECIAL 9"
command = ~B,DB,D,DF,F,b
time = 30

[command]
name = "SPECIAL 10"
command = ~F,DF,D,DB,B,b
time = 30

[command]
name = "SPECIAL 11"
command = ~B,DB,D,DF,F,c
time = 30

[command]
name = "SPECIAL 12"
command = ~F,DF,D,DB,B,c
time = 30

[Defaults]

;-| Double Tap |-----------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10
;-| 2/3 Button Combination |-----------------------------------------------
[Command]
name = "recovery" ;Required (do not remove)
command = x+y
time = 1

[Command]
name = "recovery"
command = y+z
time = 1

[Command]
name = "recovery"
command = x+z
time = 1

[Command]
name = "recovery"
command = a+b
time = 1

[Command]
name = "recovery"
command = b+c
time = 1

[Command]
name = "recovery"
command = a+c
time = 1
;-| Dir + Button |---------------------------------------------------------
[Command]
name = "back_x"
command = /$B,x
time = 1

[Command]
name = "back_y"
command = /$B,y
time = 1

[Command]
name = "back_z"
command = /$B,z
time = 1

[Command]
name = "down_x"
command = /$D,x
time = 1

[Command]
name = "down_y"
command = /$D,y
time = 1

[Command]
name = "down_z"
command = /$D,z
time = 1

[Command]
name = "fwd_x"
command = /$F,x
time = 1

[Command]
name = "fwd_y"
command = /$F,y
time = 1

[Command]
name = "fwd_z"
command = /$F,z
time = 1

[Command]
name = "up_x"
command = /$U,x
time = 1

[Command]
name = "up_y"
command = /$U,y
time = 1

[Command]
name = "up_z"
command = /$U,z
time = 1

[Command]
name = "back_a"
command = /$B,a
time = 1

[Command]
name = "back_b"
command = /$B,b
time = 1

[Command]
name = "back_c"
command = /$B,c
time = 1

[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
time = 1

[Command]
name = "down_c"
command = /$D,c
time = 1

[Command]
name = "fwd_a"
command = /$F,a
time = 1

[Command]
name = "fwd_b"
command = /$F,b
time = 1

[Command]
name = "fwd_c"
command = /$F,c
time = 1

[Command]
name = "up_a"
command = /$U,a
time = 1

[Command]
name = "up_b"
command = /$U,b
time = 1

[Command]
name = "up_c"
command = /$U,c
time = 1
;-| Single Button |---------------------------------------------------------
[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "c"
command = c
time = 1

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
time = 1

[Command]
name = "s"
command = s
time = 1
;-| Single Dir |------------------------------------------------------------
[Command]
name = "fwd" ;Required (do not remove)
command = $F
time = 1

[Command]
name = "downfwd"
command = $DF
time = 1

[Command]
name = "down" ;Required (do not remove)
command = $D
time = 1

[Command]
name = "downback"
command = $DB
time = 1

[Command]
name = "back" ;Required (do not remove)
command = $B
time = 1

[Command]
name = "upback"
command = $UB
time = 1

[Command]
name = "up" ;Required (do not remove)
command = $U
time = 1

[Command]
name = "upfwd"
command = $UF
time = 1
;-| Hold Button |--------------------------------------------------------------
[Command]
name = "hold_x"
command = /x
time = 1

[Command]
name = "hold_y"
command = /y
time = 1

[Command]
name = "hold_z"
command = /z
time = 1

[Command]
name = "hold_a"
command = /a
time = 1

[Command]
name = "hold_b"
command = /b
time = 1

[Command]
name = "hold_c"
command = /c
time = 1

[Command]
name = "hold_s"
command = /s
time = 1
;-| Hold Dir |--------------------------------------------------------------
[Command]
name = "holdfwd" ;Required (do not remove)
command = /$F
time = 1

[Command]
name = "holddownfwd"
command = /$DF
time = 1

[Command]
name = "holddown" ;Required (do not remove)
command = /$D
time = 1

[Command]
name = "holddownback"
command = /$DB
time = 1

[Command]
name = "holdback" ;Required (do not remove)
command = /$B
time = 1

[Command]
name = "holdupback"
command = /$UB
time = 1

[Command]
name = "holdup" ;Required (do not remove)
command = /$U
time = 1

[Command]
name = "holdupfwd"
command = /$UF
time = 1
;---------------------------------------------------------------------------
[Command]
name="rimuru_hell"
command=~y
time=15
[Command]
name="rimuru_lightning"
command=/$D,~y
time=15
[Command]
name="rimuru_flare"
command=~x
time=15

[Command]
name="rimuru_form"
command=w
time=15
[Command]
name="rimuru_slash"
command=/$F,~x
time=15
[Command]
name="rimuru_predator"
command=/$B,~x
time=15
[Command]
name="rimuru_blackflame"
command=/$D,~x
time=15
[Command]
name="rimuru_ranga"
command=/$B,~y
time=15
[Command]
name="rimuru_timestop"
command=/$F,~y
time=15

[Command]
name="rf_ult"
command=~z
time=15
[Command]
name="rf_form"
command=/$D,~y
time=15
[Command]
name="rf_super_back"
command=/$B,~y
time=15
[Command]
name="rf_super_forward"
command=/$F,~y
time=15
[Command]
name="rf_super"
command=~y
time=15
[Command]
name="rf_down"
command=/$D,~x
time=15
[Command]
name="rf_back"
command=/$B,~x
time=15
[Command]
name="rf_forward"
command=/$F,~x
time=15
[Command]
name="rf_special"
command=~x
time=15

[Statedef -1]
[State -1, rf_ult]
type=ChangeState
trigger1=command="rf_ult" && ctrl && statetype!=A && power>=3000
value=870000+map(rimuru.form)*1000+90
[State -1, rf_form]
type=ChangeState
trigger1=command="rf_form" && ctrl && statetype!=A && power>=0
value=ifelse(map(rimuru.form)=0,7940,ifelse(map(rimuru.form)=1,7941,7942))
[State -1, rf_super_back]
type=ChangeState
trigger1=command="rf_super_back" && ctrl && statetype!=A && power>=1500
value=870000+map(rimuru.form)*1000+61
[State -1, rf_super_forward]
type=ChangeState
trigger1=command="rf_super_forward" && ctrl && statetype!=A && power>=2000
value=870000+map(rimuru.form)*1000+62
[State -1, rf_super]
type=ChangeState
trigger1=command="rf_super" && ctrl && statetype!=A && power>=1000
value=870000+map(rimuru.form)*1000+60
[State -1, rf_down]
type=ChangeState
trigger1=command="rf_down" && ctrl && statetype!=A && power>=500
value=870000+map(rimuru.form)*1000+33
[State -1, rf_back]
type=ChangeState
trigger1=command="rf_back" && ctrl && statetype!=A && power>=500
value=870000+map(rimuru.form)*1000+32
[State -1, rf_forward]
type=ChangeState
trigger1=command="rf_forward" && ctrl && statetype!=A && power>=500
value=870000+map(rimuru.form)*1000+31
[State -1, rf_special]
type=ChangeState
trigger1=command="rf_special" && ctrl && statetype!=A && power>=500
value=870000+map(rimuru.form)*1000+30
[State -1, Form normal]
type=ChangeState
trigger1=command="a" && statetype=A && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 0>stateno%1000))
value=870000+map(rimuru.form)*1000+20
[State -1, Form normal]
type=ChangeState
trigger1=command="a" && statetype=C && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 0>stateno%1000))
value=870000+map(rimuru.form)*1000+10
[State -1, Form normal]
type=ChangeState
trigger1=command="a" && statetype=S && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 0>stateno%1000))
value=870000+map(rimuru.form)*1000+0
[State -1, Form normal]
type=ChangeState
trigger1=command="b" && statetype=A && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 1>stateno%1000))
value=870000+map(rimuru.form)*1000+21
[State -1, Form normal]
type=ChangeState
trigger1=command="b" && statetype=C && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 1>stateno%1000))
value=870000+map(rimuru.form)*1000+11
[State -1, Form normal]
type=ChangeState
trigger1=command="b" && statetype=S && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 1>stateno%1000))
value=870000+map(rimuru.form)*1000+1
[State -1, Form normal]
type=ChangeState
trigger1=command="c" && statetype=A && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 2>stateno%1000))
value=870000+map(rimuru.form)*1000+22
[State -1, Form normal]
type=ChangeState
trigger1=command="c" && statetype=C && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 2>stateno%1000))
value=870000+map(rimuru.form)*1000+12
[State -1, Form normal]
type=ChangeState
trigger1=command="c" && statetype=S && (ctrl || (stateno=[870000+map(rimuru.form)*1000,870002+map(rimuru.form)*1000] && time>=16 && movecontact && 2>stateno%1000))
value=870000+map(rimuru.form)*1000+2

[State -1, rimuru_form]
type=ChangeState
triggerall=command="rimuru_form"
triggerall=power>=0
triggerall=statetype!=A
trigger1=ctrl
value=ifelse(map(rimuru.form)=0,7940,ifelse(map(rimuru.form)=1,7941,7942))
[State -1, rimuru_slash]
type=ChangeState
triggerall=command="rimuru_slash"
triggerall=power>=1000
triggerall=statetype!=A
trigger1=ctrl
value=7960
[State -1, rimuru_predator]
type=ChangeState
triggerall=command="rimuru_predator"
triggerall=power>=2000
triggerall=statetype!=A
trigger1=ctrl
value=7970
[State -1, rimuru_blackflame]
type=ChangeState
triggerall=command="rimuru_blackflame"
triggerall=power>=1500
triggerall=statetype!=A
trigger1=ctrl
value=1300
[State -1, rimuru_ranga]
type=ChangeState
triggerall=command="rimuru_ranga"
triggerall=power>=1500
triggerall=statetype!=A
trigger1=ctrl
value=1200
[State -1, rimuru_timestop]
type=ChangeState
triggerall=command="rimuru_timestop"
triggerall=power>=2000
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Illustrated quick command]
type=ChangeState
triggerall=command="rimuru_lightning"
triggerall=power>=2000
triggerall=statetype!=A
trigger1=ctrl
value=1400
[State -1, Illustrated quick command]
type=ChangeState
triggerall=command="rimuru_hell"
triggerall=power>=1000
triggerall=statetype!=A
trigger1=ctrl
value=1100
[State -1, Illustrated quick command]
type=ChangeState
triggerall=command="rimuru_flare"
triggerall=power>=1000
triggerall=statetype!=A
trigger1=ctrl
value=1000

;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
; Correr Adelante
[State -1, Dash Forward]
type = ChangeState
triggerall = statetype = A
triggerall = var(5) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 76
trigger1 = command = "FF"
trigger1 = ctrl

[State -1, Run]
type = ChangeState
triggerall = statetype = S
triggerall = var(5) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 60
trigger1 = command = "FF"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Dash Back]
type = ChangeState
triggerall = statetype = S
triggerall = var(5) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 70
trigger1 = command = "BB"
trigger1 = ctrl
[State -1, Dash Back Air]
type = ChangeState
triggerall = statetype = A
triggerall = var(5) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 75
trigger1 = command = "BB"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, Dodge]
type = ChangeState
value = 290
triggerall = ailevel = 0
trigger1 = command = "a+b"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;SUPERS:
;===========================================================================
; Titan Transformation
[State -1, Meggido]
type = ChangeState
Triggerall = power >= 3000
value = 4500
Triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0
;===========================================================================
;SPECIALS:
;===========================================================================
; Rifle Shot
[State -1, Gluttony]
type = ChangeState
Triggerall = power >= 1000
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------

[State -1, Hell Flare]
type = ChangeState
Triggerall = power >= 1000
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1, Tempest Star Wolf]
type = ChangeState
Triggerall = power >= 1500
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1, Black Flame]
type = ChangeState
Triggerall = power >= 1500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------

[State -1, Black Lightning]
type = ChangeState
Triggerall = power >= 2000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = numhelper(1401) = 0
;---------------------------------------------------------------------------

[State -1, Time Stop]
type = ChangeState
Triggerall = power >= 2000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = numhelper(1505) = 0
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
[State -1, Crouch A]
type = ChangeState
value = 330
triggerall = command = "a"
Triggerall = statetype = C
trigger1 = ctrl

[State -1, Crouch B]
type = ChangeState
value = 340
triggerall = command = "b"
Triggerall = statetype = C
trigger1 = ctrl

; A
[State -1, A]
type = ChangeState
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 220
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 250
triggerall = power  >250
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
triggerall = numhelper(1505) = 0
Triggerall = power < 3000
value = 500
triggerall = command = "hold_s"
Trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, Aire Dowm1]
type = ChangeState
value = 670
trigger1 = command = "a"
trigger2 = command = "b"
triggerall = command = "holddown"
Triggerall = statetype = A
triggerall = ctrl

[State -1, Aire Dowm2]
type = ChangeState
value = 660
trigger1 = command = "c"
triggerall = command = "holddown"
Triggerall = statetype = A
triggerall = ctrl

; A Aire
[State -1, A Aire]
type = ChangeState
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 620
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl

[State -1, C Aire]
type = ChangeState
value = 650
triggerall = power  >250
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
