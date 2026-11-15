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
name = "SUPER1"
command = ~D,DF,F,D,DF,F,a+b
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
[Statedef -1]
;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 0||var(2) = 1||var(2) = 5||var(2) = 6
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = ifelse(pos y >= 0,60,65)
trigger1 = command = "FF"
trigger1 = ctrl

; Correr atras
[State -1, Correr atras]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 0||var(2) = 1||var(2) = 5||var(2) = 6
triggerall = stateno != 70
triggerall = stateno != 75
triggerall = stateno != 60
value = ifelse(pos y >= 0,70,75)
trigger1 = command = "BB"
trigger1 = ctrl
;=============
; ASHURA
; Run Ashura
[State -1, Run Ashura]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 2||var(2) = 3||var(2) = 4
triggerall = stateno != 2100
triggerall = stateno != 2105
value = 2100
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Run Back Ashura
[State -1, Run Back Ashura]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 2||var(2) = 3||var(2) = 4
triggerall = stateno != 2100
triggerall = stateno != 2105
value = 2105
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
triggerall = ailevel = 0
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;SUPERS:
;===========================================================================
; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 0
Triggerall = power >= 3000
value = 3000
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Senpo Cho Bijuu Rasen Shuriken
[State -1, Senpo Cho Bijuu Rasen Shuriken]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 3100
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Cho odama rasengan
[State -1,  Cho odama rasengan]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 1
Triggerall = power >= 3000
value = 3300
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Cho odama rasen shuriken
[State -1, Cho odama rasen shuriken]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 3
Triggerall = power >= 3000
value = 3400
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Cho odama bijuu  rasen shuriken
[State -1, Cho odama bijuu rasen shuriken]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 4
Triggerall = power >= 3000
value = 3500
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Cho Bijuu dama
[State -1,  Cho Bijuu dama]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 5
Triggerall = power >= 3000
value = 3600
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Cho cannon Bijuu dama
[State -1,  Cho cannon Bijuu dama]
type = ChangeState
triggerall = ailevel = 0
triggerall = var(2) = 6
Triggerall = power >= 3000
value = 3700
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;SPECIALS:
;===========================================================================
;BASE
; Rasengan
[State -1, Rasengan]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Shuriken kage buushin
[State -1, Shuriken kage buushin]
type = ChangeState
triggerall = numhelper(1140) < 3
triggerall = var(2) = 0
Triggerall = power >= 500
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = numhelper(4002) = 0
triggerall = numhelper(20002) = 0
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin CHARGE
[State -1, Kage buushin CHARGE]
type = ChangeState
triggerall = numhelper(1350) = 0
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin barrage
[State -1, Kage buushin barrage]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasengan Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = numhelper(1510) = 0
triggerall = numhelper(1520) = 0
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;Sennin
; Rasenegan
[State -1, Rasenegan]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 31000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Shuriken kage buushin
[State -1, Shuriken kage buushin]
type = ChangeState
triggerall = numhelper(32150) < 3
triggerall = var(2) = 1
Triggerall = power >= 500
value = 31100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = numhelper(4002) = 0
triggerall = numhelper(20002) = 0
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 31200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin CHARGE
[State -1, Kage buushin CHARGE]
type = ChangeState
triggerall = numhelper(31350) = 0
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 31300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; rasengan barrage
[State -1, rasengan barrage]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 31400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 31500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;4 tails mode
; 4 tails mode
[State -1, Rasengan]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 34000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; BIjuu senkoodan
[State -1, BIjuu senkoodan]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 500
value = 34100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 34200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Bijuu bomb
[State -1, Bijuu bomb]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 34300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; bijuu dama
[State -1, bijuu dama]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 34400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = numhelper(34550) = 0
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 34500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;6 tails mode
; 6 tails mode
[State -1, Rasengan]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; BIjuu senkoodan
[State -1, BIjuu senkoodan]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 500
value = 35100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Bijuu bomb
[State -1, Bijuu bomb]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; bijuu dama
[State -1, bijuu dama]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = numhelper(34550) = 0
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;Sennin
; Rasenegan
[State -1, Rasenegan]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 32000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Bijuu senkoodan
[State -1, Bijuu senkoodan]
type = ChangeState
triggerall = numhelper(32150) < 3
triggerall = var(2) = 3
Triggerall = power >= 500
value = 32500
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = numhelper(4002) = 0
triggerall = numhelper(20002) = 0
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 32200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Bijuu bomb
[State -1, Bijuu bomb]
type = ChangeState
triggerall = numhelper(31350) = 0
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 32300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; KCM rasengan barrage
[State -1, rasengan barrage]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 32400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 32100
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;KCM 2
; Rasengan
[State -1, Rasengan]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 33000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; BIjuu senkoodan
[State -1, BIjuu senkoodan]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 500
value = 33100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Kage buushin
[State -1, Kage buushin]
type = ChangeState
triggerall = numhelper(4002) = 0
triggerall = numhelper(20002) = 0
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 33200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Bijuu bomb
[State -1, Bijuu bomb]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 33300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; bijuu dama
[State -1, bijuu dama]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 30400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = numhelper(33550) = 0
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 33500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;ASHURA
; Rasengan
[State -1, Rasengan]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 30000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Naruto Ittai Rendan
[State -1, Naruto Ittai Rendan]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1400
value = 30500
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Bijuu Kage buushin
[State -1, Bijuu Kage buushin]
type = ChangeState
triggerall = numhelper(4002) = 0
triggerall = numhelper(20002) = 0
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 30100
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Black Shoot
[State -1, Black Shoot]
type = ChangeState
triggerall = numhelper(2450) = 0
triggerall = numhelper(30350) = 0
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 30300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Bijuu dama
[State -1, Bijuu dama]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1200
value = 30400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Rasen Shuriken
[State -1, Rasen Shuriken]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1500
value = 30200
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
;=============================
;BASE
;---------------------------------------------------------------------------
; A BASE
[State -1, A BASE]
type = ChangeState
triggerall = var(2) = 0
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B BASE
[State -1, B BASE]
type = ChangeState
triggerall = var(2) = 0
value = 300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A BASE AIR
[State -1, A BASE AIR]
type = ChangeState
triggerall = var(2) = 0
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B BASE AIR
[State -1, B BASE AIR]
type = ChangeState
triggerall = var(2) = 0
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C BASE
[State -1, C BASE]
type = ChangeState
triggerall = power >= 300
triggerall = var(2) != 2
value = 400
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl

; C BASE AIR
[State -1, C BASE AIR]
type = ChangeState
triggerall = power >= 300
triggerall = var(2) != 2
value = 405
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl

;=============================
;Sennin
;---------------------------------------------------------------------------
; A Sennin
[State -1, A Sennin]
type = ChangeState
triggerall = var(2) = 1
value = 11200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Sennin
[State -1, B Sennin]
type = ChangeState
triggerall = var(2) = 1
value = 11300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Sennin AIR
[State -1, A Sennin AIR]
type = ChangeState
triggerall = var(2) = 1
value = 11600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Sennin AIR
[State -1, B Sennin AIR]
type = ChangeState
triggerall = var(2) = 1
value = 11610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;=============================
;4 tails
;---------------------------------------------------------------------------
; A 4 tails
[State -1, A 4 tails]
type = ChangeState
triggerall = var(2) = 5
value = 17200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B 4 tails
[State -1, B 4 tails]
type = ChangeState
triggerall = var(2) = 5
value = 17300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A 4 tails AIR
[State -1, A 4 tails AIR]
type = ChangeState
triggerall = var(2) = 5
value = 17600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B 4 tails AIR
[State -1, B 4 tails AIR]
type = ChangeState
triggerall = var(2) = 5
value = 17610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;=============================
;6 tails
;---------------------------------------------------------------------------
; A 6 tails
[State -1, A 6 tails]
type = ChangeState
triggerall = var(2) = 6
value = 19200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B 6 tails
[State -1, B 6 tails]
type = ChangeState
triggerall = var(2) = 6
value = 19300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A 6 tails AIR
[State -1, A 6 tails AIR]
type = ChangeState
triggerall = var(2) = 6
value = 19600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B 6 tails AIR
[State -1, B 6 tails AIR]
type = ChangeState
triggerall = var(2) = 6
value = 19610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;=============================
;KCM 1
;---------------------------------------------------------------------------
; A KCM 1
[State -1, A KCM 1]
type = ChangeState
triggerall = var(2) = 3
value = 13200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B KCM 1
[State -1, B KCM 1]
type = ChangeState
triggerall = var(2) = 3
value = 13300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A KCM 1 AIR
[State -1, A KCM 1 AIR]
type = ChangeState
triggerall = var(2) = 3
value = 13600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B KCM 1 AIR
[State -1, B KCM 1 AIR]
type = ChangeState
triggerall = var(2) = 3
value = 13610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;=============================
;KCM 2
;---------------------------------------------------------------------------
; A KCM 2
[State -1, A KCM 2]
type = ChangeState
triggerall = var(2) = 4
value = 15200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B KCM 2
[State -1, B KCM 2]
type = ChangeState
triggerall = var(2) = 4
value = 15300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A KCM 2 AIR
[State -1, A KCM 2 AIR]
type = ChangeState
triggerall = var(2) = 4
value = 15600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B KCM 2 AIR
[State -1, B KCM 2 AIR]
type = ChangeState
triggerall = var(2) = 4
value = 15610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;=============================
;ASHURA
;---------------------------------------------------------------------------
; A Ashura
[State -1, A Ashura]
type = ChangeState
triggerall = var(2) = 2
value = 2200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Ashura
[State -1, B Ashura]
type = ChangeState
triggerall = var(2) = 2
value = 2300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Ashura
[State -1, C Ashura]
type = ChangeState
triggerall = power >= 300
Triggerall = numhelper(2450) = 0
Triggerall = numhelper(30350) = 0
triggerall = var(2) = 2
value = 2400
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command != "holddown"
triggerall = command = "s"
Trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire Ashura
[State -1, A Aire Ashura]
type = ChangeState
triggerall = var(2) = 2
value = 2600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire Ashura
[State -1, B Aire Ashura]
type = ChangeState
Triggerall = numhelper(2650) = 0
triggerall = var(2) = 2
value = 2620
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire Ashura
[State -1, C Aire Ashura]
type = ChangeState
Triggerall = numhelper(30350) = 0
triggerall = power >= 300
Triggerall = numhelper(2450) = 0
triggerall = var(2) = 2
value = 2405
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;============================================================================
;TRANSFORM 

; Sennin 
[State -1, Sennin]
type = ChangeState
triggerall = var(2) < 1
Triggerall = numhelper(942) = 0
value = 811
triggerall = command != "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl

; 4 tails mode
[State -1, 4 tails mode]
type = ChangeState
triggerall = var(5) >= 300
triggerall = var(2) = 0|| var(2) = 1
value = 850
triggerall = command != "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl
; 6 tails mode
[State -1, 6 tails mode]
type = ChangeState
triggerall = var(5) >= 900
triggerall = var(2) = 0|| var(2) = 1|| var(2) = 5
value = 860
triggerall = command = "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl

; KCM 1 
[State -1, KCM 1]
type = ChangeState
triggerall = var(5) >= 500
triggerall = var(2) = 0|| var(2) = 1
value = 830
triggerall = command != "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl

; KCM 2 
[State -1, KCM 2]
type = ChangeState
triggerall = var(5) >= 900
triggerall = var(2) = 0|| var(2) = 1|| var(2) = 3
value = 840
triggerall = command = "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl

; KURAMA MODE
[State -1, KURAMA MODE]
type = ChangeState
triggerall = numhelper(10000) = 0
triggerall = ailevel = 0
triggerall = power >= 1500
Triggerall = var(2) > 1
Triggerall = var(2) < 5
value = 10001
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl

; Ashura 
[State -1, Ashura]
type = ChangeState
triggerall = var(5) >= 900
triggerall = var(2) = 0|| var(2) = 1|| var(2) = 3|| var(2) = 4
value = 810
triggerall = command = "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl


; Destransformar 
[State -1, Destransformar]
type = ChangeState
triggerall = var(2) > 1
value = 815
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

; Destransformar KCM
[State -1, Destransformar KCM]
type = ChangeState
triggerall = var(2) > 1
triggerall = var(5) <= 0
value = 815
Triggerall = statetype != A
trigger1 = ctrl


