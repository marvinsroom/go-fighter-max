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
command = x
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
;---------- Comandos de la Inteligencia Artificial-----------------
; Comandos activadores
[Command]
name = "AI Prueba"
command = y+z ; con el botón A+B activamos la AI
time = 1

[Command]
name = "AI desactivado"
command = b+c ; Con el boton B+C desactivamos la AI
time = 1
;---------------------------------------------------------------------------

[Command]
name="goku_super1"
command=z
time=1

[Command]
name="goku_special_1"
command=x
time=1

[Command]
name="goku_special_2"
command=/$B,x
time=1

[Command]
name="goku_special_3"
command=/$F,x
time=1

[Command]
name="goku_special_4"
command=/$D,x
time=1

[Command]
name="goku_special_5"
command=y
time=1

[Command]
name="goku_special_6"
command=/$D,/$F,x
time=1

[Command]
name="goku_full_power"
command=/$D,d
time=1

[Command]
name="goku_form"
command=w
time=1

[Command]
name="goku_revert"
command=/$D,w
time=1

[Command]
name="goku_charge"
command=/s
time=1

[Command]
name="goku_hold_bomb"
command=/z
time=1

[Statedef -1]

[State -1, Cycle forms]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_form" || command="goku_revert"
trigger1=ctrl
value=900800
[State -1, Charge]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_charge" && power<3000
trigger1=ctrl
value=900810

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=27500

[State -1, Metteor impact]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1100
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=29500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=31500

[State -1, Genkidama]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=1100

[State -1, Super Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Super Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Super Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=29100

[State -1, Meteor Smash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=1200

[State -1, Meteor Smash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=25200

[State -1, barrier]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=27200

[State -1, Bakurikimaha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=29200

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=500
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=500
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=500
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=500
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=500
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Taiyoken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=31100

[State -1, Super Dragon Fist]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=31200

[State -1, Full Power]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_full_power"
triggerall=statetype!=A
triggerall=var(3)=0
trigger1=ctrl
value=31600

[State -1, Super Cho Genkidama]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
triggerall=life<=lifemax/2 && enemynear,life<=enemynear,lifemax/2
trigger1=ctrl
value=3000

[State -1, Super Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
triggerall=life>lifemax/2 || enemynear,life>enemynear,lifemax/2
trigger1=ctrl
value=4000

[State -1, Instant Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=26000

[State -1, Super Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=28000

[State -1, punho do dragão]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=30000

[State -1, Ryu Ken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=32000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=31000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=700
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=29000

[State -1, Kamehameha SS3]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=29400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Super Kamehameha SS1]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1500
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=25400

[State -1, Super Kamehameha SS1]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1500
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=27400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=31400

;===========================================================================
;---------------------------Basicos-----------------------------------------
;---------------------------------------------------------------------------
; Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 70
value = 60
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 70
value = 70
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;SUPERS:
;===========================================================================
;===========================================================================
;SUPERS:
;===========================================================================
;Super Cho Genkidama
[State -1, Super Cho Genkidama]
type = ChangeState
triggerall = var(2) = 0
Triggerall = life <= lifemax/2
Triggerall = p2life <= lifemax/2
Triggerall = power >= 3000
value = 3000
triggerall = command = "SUPER1"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Super Kamehameha
[State -1, Super Kamehameha]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 3000
value = 4000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;--------------------------------------------------------------------------
; Instant Kamehameha
[State -1, Instant Kamehameha]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 3000
value = 26000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Kamehameha
[State -1, Super Kamehameha]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 28000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; punho do dragão
[State -1, punho do dragão]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 3000
value = 30000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Ryu Ken
[State -1, Ryu Ken]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 3000
value = 32000
triggerall = command = "SUPER1"
trigger1 = ctrl
;===========================================================================
;SPECIALS:
;===========================================================================
; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 500
value = 31000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 500
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl

; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 500
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl

; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 500
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl

; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 700
value = 29000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Genkidama
[State -1, Genkidama]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl

; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 1 
Triggerall = power >= 1500
value = 25100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl

; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1500
value = 25100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl

; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1500
value = 29100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Full Power
[State -1, Full Power]
type = ChangeState
triggerall = var(2) = 4
triggerall = var(3) = 0
Triggerall = power >= 1500
value = 31600
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Meteor Smash
[State -1, Meteor Smash]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl

; Meteor Smash
[State -1, Meteor Smash]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 25200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl

; kicks combo
[State -1, barrier]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 27200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl

; SUPER Bakurikimaha
[State -1, Bakurikimaha]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1000
value = 29200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl

; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl

; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl

; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl

; Kamehameha SS3
[State -1, Kamehameha SS3]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1500
value = 29400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 500
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
;----------------------------------------------------------------------------
; Kamehameha
[State -1, Kamehameha]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl

; Super Kamehameha SS1
[State -1, Super Kamehameha SS1]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1500
value = 25400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl

; Super Kamehameha SS2
[State -1, Super Kamehameha SS1]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1500
value = 27400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Taiyoken
[State -1, Taiyoken]
type = ChangeState
triggerall = var(2) = 4
Triggerall = numhelper(31160) = 0
Triggerall = power >= 500
value = 31100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Dragon Fist
[State -1, Super Dragon Fist]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Kamehameha
[State -1, Kamehameha]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Super Energy Blast
[State -1, Super Energy Blast]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

; Super Energy Blast
[State -1, Super Energy Blast]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

; Super Energy Blast
[State -1, Super Energy Blast]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 27500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

; Metteor impact
[State -1, Metteor impact]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1100
value = 29500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Super Energy Blast
[State -1, Super Energy Blast]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS1
[State -1, SS1]
type = ChangeState
triggerall = power >= 500
triggerall = var(2) = 0
Triggerall = var(3) = 0
value = 700
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl

; SS2
[State -1, SS2]
type = ChangeState
triggerall = power >= 500
triggerall = var(2) = 1
Triggerall = var(3) = 0
value = 800
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl

; SS3
[State -1, SS3]
type = ChangeState
triggerall = ailevel = 0
triggerall = power >= 500
triggerall = var(2) = 2
value = 900
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl

; SS4
[State -1, SS4]
type = ChangeState
triggerall = power >= 500
triggerall = var(2) = 3
Triggerall = var(3) = 0
value = 1900
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS1 Cancelar
[State -1, SS1 Cancelar]
type = ChangeState
triggerall = var(2) = 1
value = 705
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

; SS2 Cancelar
[State -1, SS2 Cancelar]
type = ChangeState
triggerall = var(2) = 2
value = 805
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

; SS3 Cancelar
[State -1, SS3 Cancelar]
type = ChangeState
triggerall = var(2) = 3
value = 905
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

; SS4 Cancelar
[State -1, SS4 Cancelar]
type = ChangeState
triggerall = var(2) = 4
value = 1905
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
triggerall = var(2) = 0
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
triggerall = var(2) = 0
value = 300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 400
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
triggerall = var(2) = 0
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
triggerall = var(2) = 0
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
value = 620
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A SS1
[State -1, A SS1]
type = ChangeState
triggerall = var(2) = 1
value = 2200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B SS1
[State -1, B SS1]
type = ChangeState
triggerall = var(2) = 1
value = 2300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;--------------------------------------------------------------------------
; A SS2
[State -1, A SS2]
type = ChangeState
triggerall = var(2) = 2
value = 11200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;--------------------------------------------------------------------------
; B SS2
[State -1, B SS2]
type = ChangeState
triggerall = var(2) = 2
value = 11300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A SS3
[State -1, A SS3]
type = ChangeState
triggerall = var(2) = 3
value = 13200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Ss3
[State -1, B Ss3]
type = ChangeState
triggerall = var(2) = 3
value = 13300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A SS4
[State -1, A SS4]
type = ChangeState
triggerall = var(2) = 4
value = 15200
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B SS4
[State -1, B SS4]
type = ChangeState
triggerall = var(2) = 4
value = 15300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SS1
[State -1, A Aire SS1]
type = ChangeState
triggerall = var(2) = 1
value = 2600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SS4
[State -1, A Aire SS4]
type = ChangeState
triggerall = var(2) = 4
value = 15600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;-----------------------------------------------------------------------------
; A Aire SS2
[State -1, A Aire SS2]
type = ChangeState
triggerall = var(2) = 2
value = 11600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;----------------------------------------------------------------------------
; A Aire SS3
[State -1, A Aire SS3]
type = ChangeState
triggerall = var(2) = 3
value = 13600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire SS1
[State -1, B Aire SS1]
type = ChangeState
triggerall = var(2) = 1
value = 2610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;------------------------------------------------------------------------------
; B Aire SS2
[State -1, B Aire SS2]
type = ChangeState
triggerall = var(2) = 2
value = 11610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;-------------------------------------------------------------------------------
; B Aire SS3
[State -1, B Aire SS3]
type = ChangeState
triggerall = var(2) = 3
value = 13610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire SS4
[State -1, B Aire SS4]
type = ChangeState
triggerall = var(2) = 4
value = 15610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
