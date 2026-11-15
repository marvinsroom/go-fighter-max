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
command = z
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
; Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 60
trigger1 = command = "FF"
trigger1 = ctrl
triggerall = ailevel = 0 
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
triggerall = var(5) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
value = 70
trigger1 = command = "BB"
trigger1 = ctrl
triggerall = ailevel = 0 

;===========================================================================
;SUPERS:

;===========================================================================
;SPECIALS:
;===========================================================================
;raikou
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0 

;===========================================================================
; sokatui
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 1000
value = 1050
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0 
;===========================================================================
;kurohitsuki
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 1500
value = 1100
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0 
;===========================================================================
; bunshin dash
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 1000
value = 1150
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl
;===========================================================================
;Rei atsu
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 1000
value = 1200
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0 
;===========================================================================
;Dunku
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 500
value = 1250
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
triggerall = ailevel = 0 
;===========================================================================
; 
[State -1, Hadou number 31 Shakahou]
type = ChangeState
Triggerall = power >= 3000
value = 2000
triggerall = command = "x"
Triggerall = statetype != A
Triggerall = enemy,statetype != L
triggerall = ailevel = 0 
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, ]
type = ChangeState
Triggerall = power >= 500
trigger1 = numhelper(4000) = 0
value = 1300
triggerall = command != "holddown"
triggerall = command != "holdfwd"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
triggerall = var(3) = 0
triggerall = command != "holddown"
triggerall = command != "holdfwd"
value = 200
triggerall = command = "a"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
triggerall = var(3) = 0
triggerall = command != "holddown"
triggerall = command != "holdfwd"
value = 300
triggerall = command = "b"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 400
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl

;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
triggerall = var(3) = 0
triggerall = command = "holdfwd" ;"holdback"
triggerall = command = "a"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl
value = 230
; B
[State -1, B]
type = ChangeState
triggerall = var(3) = 0
triggerall = command = "holdfwd" ;"holdback"
triggerall = command = "b"
Triggerall = statetype != A
triggerall = ailevel = 0 
trigger1 = ctrl
value = 330
;;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command = "s"
triggerall = ailevel = 0 
Triggerall = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 600
triggerall = command = "a"
Triggerall = statetype = A
triggerall = ailevel = 0 
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 610
triggerall = command = "b"
Triggerall = statetype = A
triggerall = ailevel = 0 
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
value = 620
triggerall = command = "c"
Triggerall = statetype = A
triggerall = ailevel = 0 
trigger1 = ctrl



;===========================================================================
; Danku
[State -1, Danku]
type = ChangeState
Triggerall = numhelper(10050) = 0
Triggerall = power >= 500
value = 1000
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;-------------------------------------
;---------------------------------------------------------------------------
[State -1, ]
type = ChangeState
Triggerall = power >= 500
value = 10800
triggerall = command != "holddown"
triggerall = command != "holdfwd"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
;trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1, ]
type = ChangeState
Triggerall = power >= 500
value = 10801
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl
;trigger2 = numhelper(700) > 0
;===========================================================================
[State -1, ]
type = ChangeState
triggerall = numhelper(10350) = 0
Triggerall = power >= 500
value = 13000
triggerall = command = "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;trigger2 = numhelper(700) > 0
[State -1, ]
type = ChangeState
value = 2620
triggerall = power >= 300
triggerall = command = "y"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, ]
type = ChangeState
trigger1 = numhelper(4000) = 0
Triggerall = power >= 500
value = 10700
triggerall = command = "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Raikohou
[State -1, Raikohou]
type = ChangeState
trigger1 = numhelper(4000) = 0
Triggerall = power >= 1000
value = 1900
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Shunpo
[State -1, Shunpo]
type = ChangeState
Triggerall = power >= 400
value = 480
triggerall = command = "z"
trigger1 = ctrl
;---------------------------------------------------------------------------
;;---------------------------------------------------------------------------
; Reatsu Crushing
[State -1, Reatsu Crushing]
type = ChangeState
;trigger1 = numhelper(1660) = 0
Triggerall = power >= 1500
value = 2200
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; S Aire
[State -1, S Aire]
type = ChangeState
triggerall = numhelper(835) = 0
value = 830
triggerall = command = "s"
Triggerall = statetype = A
trigger1 = ctrl
;