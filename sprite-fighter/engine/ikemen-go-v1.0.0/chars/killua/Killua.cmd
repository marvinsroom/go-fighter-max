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
s = s

[Command]
name = "Super Jump"
command = ~D,U
time = 10

;-| Supers |-------------------------------------------------------

[command]
name = "ULTIMATE 1"
command = ~F,DF,D,DB,B,b
time = 30

[command]
name = "SUPER1"
command = ~D,DF,F,a+b
time = 30

[command]
name = "SUPER2"
command = ~D,DF,F,b+c
time = 30

[command]
name = "SUPER3"
command = ~D,DF,F,a+c
time = 30

[command]
name = "CANCELSUPER2"
command = ~D,DF,F,D,DF,F,b+c
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
command = ~D,DF,F,D,DF,F,a
time = 50

[command]
name = "SPECIAL 8"
command = ~D,DF,F,D,DF,F,b
time = 50

[command]
name = "SPECIAL 9"
command = ~D,DF,F,D,DF,F,c
time = 50

[command]
name = "DF"
command = ~D,DF,F
time = 15

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

[Command]
name = "holda+b"
command = /a+b
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
;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
[Statedef -1]

[State -1, String Reset]
type = ChangeState
triggerall = (var(48) != 5) && (var(54) = 0) && (power >= 1500) && (command = "z") && (statetype != A) && (stateno = [200,499]) && (!ailevel)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 515

;[State -1, Guard Break]
;type = ChangeState
;triggerall = (numexplod(500520) = 0) && (command = "z") && (command = "holddown") && (statetype != A) && (!ailevel)
;trigger1 = ctrl
;value = 520

[State -1, Push Block (Stand)]
type = ChangeState
triggerall = (power >= 1000)
triggerall = (command = "a" && command = "b") || (command = "b" && command = "c") && (!ailevel)
trigger1 = stateno = [150,151]
value = 500130

[State -1, Push Block (Crouching)]
type = ChangeState
triggerall = (power >= 1000)
triggerall = (command = "a" && command = "b") || (command = "b" && command = "c") && (!ailevel)
trigger1 = stateno = [152,153]
value = 500131

[State -1, Push Block (Air)]
type = ChangeState
triggerall = (power >= 1000)
triggerall = (command = "a" && command = "b") || (command = "b" && command = "c") && (!ailevel)
trigger1 = stateno = 154
trigger2 = stateno = 155 && time <= 10
value = 500132

[State -1, Combo Breaker]
type = ChangeState
triggerall = (var(49) != 3) && (power >= 3000) && (stateno=[5000,5300]) && (enemynear,hitdefattr != SCA,HA,HT,HP,NT,ST) && (command = "a") && (command = "b") && (command = "c") && (roundstate = 2) && (!ailevel)
trigger1 = (movetype = H) 
value = 510

[State -1, Dash]
type = ChangeState
triggerall = (var(5) = 0) && (statetype != A) && (stateno != 60) && (stateno != 65) && (stateno != 66) && (stateno != 70) && (roundstate = 2) && (!ailevel)
trigger1 = (ctrl) && (command = "FF")
value = 60

[State -1, Air Dash]
type = ChangeState
triggerall = (numexplod(99999) = 0) && (statetype = A) && (stateno != 60) && (stateno != 66)  && (stateno != 70) && (roundstate = 2) && (!ailevel)
trigger1 = (ctrl) && (command = "FF")
value = 65

[State -1, Back Dash]
type = ChangeState
triggerall = (numexplod(99999) = 0) && (var(5) = 0) && (statetype != A) && (stateno != 60) && (stateno != 65) && (stateno != 66)  && (stateno != 70) && (roundstate = 2) && (!ailevel)
trigger1 = (ctrl) && (command = "BB")
value = 70

[State -1, Air Back Dash]
type = ChangeState
triggerall = (numexplod(99999) = 0) && (statetype = A) && (stateno != 60) && (stateno != 65) && (stateno != 70) && (roundstate = 2) && (!ailevel)
trigger1 = (ctrl) && (command = "BB")
value = 66

[State -1, Super Jump]
type = ChangeState
trigger1 = (command = "Super Jump") && (statetype = S) && (ctrl) && (roundstate = 2) && (!ailevel)
value = 80

;===========================================================================
;SUPERS:
;===========================================================================

[State -1, Godspeed Bolt]
type = ChangeState
triggerall = (power >= 3000) && (command = "ULTIMATE 1") && (statetype != A) && (p2life <= lifemax/3) && (teammode != simul)
trigger1 = ctrl
value = 3000

[State -1, Rhythm Echo]
type = ChangeState
triggerall = (power >= 2000) && (command = "SUPER1") && (statetype != A) && (teammode != simul)
trigger1 = ctrl
value = 2500

[State -1, Raiouken]
type = ChangeState
triggerall = (power >= 2000) && (command = "SUPER2") && (statetype != A) && (teammode != simul)
trigger1 = ctrl
value = 2600

[State -1, If you get near here, i'll kill you]
type = ChangeState
triggerall = (var(25) = 1) && (power >= 2000) && (command = "SUPER3") && (statetype != A) && (teammode != simul) 
trigger1 = ctrl
value = 2700
;===========================================================================
;SPECIALS:
;===========================================================================

[State -1, Assassin Mode]
type = ChangeState
triggerall = (power >= 500) && (command = "SPECIAL 1") && (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1000

[State -1, The Snake Awakens]
type = ChangeState
triggerall = (power >= 500) && (command = "SPECIAL 2") && (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1200

[State -1, Raikoken]
type = ChangeState
triggerall = (power >= 1000) && (command = "SPECIAL 3") ;&& (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1600

[State -1, You know what?]
type = ChangeState
triggerall = (power >= 1000) && (command = "SPECIAL 4") && (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1300

[State -1, Thunderbolt]
type = ChangeState
triggerall = (power >= 1500) && (command = "SPECIAL 5") ;&& (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1400

[State -1, Lightning Palm]
type = ChangeState
triggerall = (power >= 1500) && (command = "SPECIAL 6") && (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1500

[State -1, Godspeed]
type = ChangeState
triggerall = ailevel=0
triggerall = !numexplod(1650)
triggerall = !ishelper
triggerall = (power >= 1500) && (command = "holddown") && (command = "s") && (statetype != A)
trigger1 = ctrl
trigger2 = numhelper(700) > 0
value = 1800
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------

[State -1, Speed of Lightning AIR]
type = ChangeState
triggerall = var(25) = 1
triggerall = power >= 250
triggerall = numhelper(473) = 0
triggerall = ailevel = 0
triggerall = command = "y"
triggerall = statetype = A
trigger1 = ctrl
value = 470

[State -1, Speed of Lightning]
type = ChangeState
triggerall = var(25) = 1
triggerall = power >= 250
triggerall = command = "y"
triggerall = ailevel = 0
triggerall = statetype != A
trigger1 = ctrl
value = 460

[State -1, Whirlwind]
type = ChangeState
triggerall = var(25) = 1
triggerall = !numhelper(452)
;triggerall = power >= 400
triggerall = command = "holdfwd"
triggerall = command = "c"
triggerall = ailevel = 0
triggerall = power >= 400
Triggerall = statetype != A
trigger1 = ctrl
value = 450

[State -1, Fwd B]
type = ChangeState
triggerall = (command = "b") && (command = "holdfwd") && (statetype != A)
trigger1 = ctrl
value = 370

[State -1, Down A]
type = ChangeState
triggerall = (command = "a") && (command = "holddown") && (statetype != A)
trigger1 = ctrl
value = 240

[State -1, Down B]
type = ChangeState
triggerall = (command = "b") && (command = "holddown") && (statetype != A)
trigger1 = ctrl
value = 340

[State -1, Down C]
type = ChangeState
triggerall = (command = "c") && (command = "holddown") && (statetype != A)
trigger1 = ctrl
value = 430

[State -1, Down A Aire]
type = ChangeState
triggerall = (command = "a") && (command = "holddown") && (statetype = A)
trigger1 = ctrl
value = 605

[State -1, Down B Aire]
type = ChangeState
triggerall = (var(5) = 0) && (command = "b") && (command = "holddown") && (statetype = A)
trigger1 = ctrl
value = 615

[State -1, Down C Aire]
type = ChangeState
triggerall = (command = "c") && (command = "holddown") && (statetype = A)
trigger1 = ctrl
value = 625

[State -1, A+C]
type = ChangeState
triggerall = ailevel=0
triggerall = !numexplod(449)
triggerall = (power >= 400) && (command = "a") && (command = "c") && (statetype != A)
trigger1 = ctrl
value = 440

[State -1, A+B]
type = ChangeState
triggerall = (power >= 250) && (command = "a") && (command = "b") ;&& (statetype != A)
trigger1 = ctrl
value = 250

[State -1, B+C]
type = ChangeState
triggerall = (power >= 250) && (command = "b") && (command = "c") && (statetype != A)
trigger1 = ctrl
value = 350

[State -1, A]
type = ChangeState
triggerall = (command = "a") && (statetype != A)
trigger1 = ctrl
value = 200

[State -1, B]
type = ChangeState
triggerall = (command = "b") && (statetype != A)
trigger1 = ctrl
value = 300

[State -1, C]
type = ChangeState
triggerall = (command = "c") && (statetype != A)
trigger1 = ctrl
value = 400

[State -1, Power Charge]
type = ChangeState
triggerall = (power < 3000) && (command = "s") && (command != "holddown") && (statetype != A)
trigger1 = ctrl
value = 500

[State -1, A Aire]
type = ChangeState
triggerall = (command = "a") && (statetype = A)
trigger1 = ctrl
value = 600

[State -1, B Aire]
type = ChangeState
triggerall = (command = "b") && (statetype = A)
trigger1 = ctrl
value = 610

[State -1, C Aire]
type = ChangeState
triggerall = (command = "c") && (statetype = A)
trigger1 = ctrl
value = 620
