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
command = ~x
time = 30

[command]
name = "SUPER2"
command = ~y
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
[Statedef -1]
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
; Super Galick Gun
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 3000
value = 3000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

; Big Bang
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 3000
value = 3200
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

;---------------------------------------------------------------------------
; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 3000
value = 30100
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Final Flash
[State -1, Final Flash]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 30000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Gamma Burst Flash
[State -1, Gamma Burst Flash]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 3000
value = 32000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Final Flash
[State -1, Final Flash]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 3000
value = 34000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact

; Final Sacrifice
[State -1, Final Sacrifice]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 5000
Triggerall = life < lifemax /2 ;triggerall = Life > 250
value = 35666
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Super Gallick Gun
[State -1, Super Gallick Gun]
type = Null;ChangeState
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 3100
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;===========================================================================
; Hakai
[State -1, Hakai]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 2500
triggerall = Life > 250
value = 3300
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl

; Final Sacrifice
[State -1, Final Sacrifice]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 4000
Triggerall = life < lifemax /2
value = 36000
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl

; Destruction Ball
[State -1, Final Sacrifice]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 3500
value = 3400
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl

;===========================================================================
;SPECIALS:
;===========================================================================
; Ki Palm
[State -1, Ki Palm]
type = ChangeState
Triggerall = power >= 500
triggerall = var(2) <3
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;===========================================================================
; Super Ki Palm
[State -1, Super Ki Palm]
type = ChangeState
Triggerall = power >= 500
triggerall = var(2) >= 3
value = 31000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Explosive Wave
[State -1, Explosive Wave]
type = ChangeState
triggerall = var(2) < 2
Triggerall = power >= 1000
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1500
value = 27100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Explosive Wave
[State -1, Explosive Wave]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1000
value = 33100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Super Explosive Wave
[State -1, Super Explosive Wave]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Double Garlick Gun
[State -1, Double Garlick Gun]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1500
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Big Bang Attack
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) > 0 && var(2) < 4
Triggerall = power >= 1500
value = 25200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Big Bang Attack
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31200
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Big Bang Attack
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 1500
value = 33200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Big Bang Attack
[State -1, Big Bang Attack]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = 35200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Prince Pride
[State -1, Price Pride]
type = ChangeState
triggerall = var(2) < 3
triggerall = var(3) = 0
Triggerall = power >= 1500
value = 1300
triggerall = command = "SPECIAL 4"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Wild Sense
[State -1, Wild Sense]
type = ChangeState
triggerall = var(2) >= 3
triggerall = var(4) = 0
Triggerall = power >= 1500
value = 33300
triggerall = command = "SPECIAL 4"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Garlick Gun
[State -1, Garlick Gun]
type = ChangeState
triggerall = var(2) = 0 || var(2) = 5
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Final Flash
[State -1, Final Flash]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1500
value = 25400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Maxiumum Flasher
[State -1, Maximum Flasher]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 27400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Final Flash
[State -1, Final Flash]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Maxiumum Flasher
[State -1, Maximum Flasher]
type = Null;ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 32400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Final Flash
[State -1, Maximum Flasher]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = 35400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Maxiumum Flasher
[State -1, Maximum Flasher]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1000
value = 27400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Super Energy Wave Volley
[State -1, Super Energy Wave Volley]
type = ChangeState
Triggerall = power >= 1000
triggerall = var(2) < 4
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Super Energy Wave Volley
[State -1, Super Energy Wave Volley]
type = ChangeState
Triggerall = power >= 1000
triggerall = var(2) = 4
value = 31500
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Galick Crash
[State -1, Galick Crash]
type = ChangeState
Triggerall = power >= 1000
triggerall = var(2) = 5
value = 33500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Energy Hakai Punish
[State -1, Energy Hakai Punish]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 2000
value = 36100
triggerall = command = "SPECIAL 6"
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Big Bang Fireworks
[State -1, Big Bang Fireworks]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = ifelse(pos y < 0,35580,35500)
triggerall = command = "holddown"
triggerall = command = "c"
trigger1 = ctrl
trigger2 = numhelper(700) > 0

;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; HAKAI
[State -1, SSBE]
type = ChangeState
triggerall = power >= 2000
triggerall = var(2) < 6
Triggerall = var(3) = 0
value = 1700
triggerall = command = "holddown"
triggerall = command = "b" || command = "z"
triggerall = ifelse(var(2)<5,command="holdback",1)
Triggerall = statetype != A
trigger1 = ctrl

; HAKAI
[State -1, SSB]
type = ChangeState
triggerall = power >= 2500
triggerall = var(2) < 6
;Triggerall = var(3) = 0
value = 1700
triggerall = command = "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
; SSB
[State -1, SSB]
type = ChangeState
triggerall = power >= 2000
triggerall = var(2) < 5
Triggerall = var(3) = 0
value = 1800
triggerall = command = "holddown"
triggerall = command = "b"
triggerall = ifelse(var(2)<4,command="holdfwd",1)
Triggerall = statetype != A
trigger1 = ctrl

; SSB
[State -1, SSB]
type = ChangeState
triggerall = power >= 2500
triggerall = var(2) < 5
;Triggerall = var(3) = 0
value = 1800
triggerall = command != "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
; SSG
[State -1, SS2]
type = ChangeState
triggerall = power >= 1500
triggerall = var(2) < 4
;Triggerall = var(3) = 0
value = 1900
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS2
[State -1, SS2]
type = ChangeState
triggerall = power >= 1000
triggerall = var(2) < 2
Triggerall = var(3) = 0
value = 800
triggerall = command = "holddown"
triggerall = command = "a"
triggerall = ifelse(var(2)=0,command="holdfwd",1)
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS1
[State -1, SS1]
type = ChangeState
triggerall = power >= 500
triggerall = var(2) = 0
Triggerall = var(3) = 0
value = 700
triggerall = command = "holddown"
triggerall = command = "a"
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
;---------------------------------------------------------------------------
; SS2 Cancelar
[State -1, SS2 Cancelar]
type = ChangeState
triggerall = var(2) = 2
value = 805
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SSG Cancelar
[State -1, SS1 Cancelar]
type = ChangeState
triggerall = var(2) = 4
;triggerall = var(3) = 0
value = 1905
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl 
;---------------------------------------------------------------------------
; SSB Cancelar
[State -1, SS1 Cancelar]
type = ChangeState
triggerall = var(2) = 5
;triggerall = var(3) = 0
value = 1805
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl 
;---------------------------------------------------------------------------
; SSBE Cancelar
[State -1, SS1 Cancelar]
type = ChangeState
triggerall = var(2) = 6
;triggerall = var(3) = 0
value = 1705
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl 
;---------------------------------------------------------------------------
; A BASE || SS1
[State -1, A BASE || SS1]
type = ChangeState
value = 200+ifelse(var(2)>1,var(11),0)
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 300
triggerall = var(2) != 4 && var(2) != 6
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 15300
triggerall = var(2) = 4
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 19300
triggerall = var(2) = 6
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
Triggerall = power < powermax
value = 500
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire BASE
[State -1, A Aire BASE]
type = ChangeState
triggerall = var(2) = 0
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SS1 || SS2
[State -1, A Aire SS1 || SS2]
type = ChangeState
triggerall = var(2) > 0 && var(2) < 4
value = 2600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SS1
[State -1, A Aire SSG]
type = ChangeState
triggerall = var(2) = 4
value = 15600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SS2
[State -1, A Aire SSB]
type = ChangeState
triggerall = var(2) = 5
value = 17600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire SSB2
[State -1, A Aire SSB]
type = ChangeState
triggerall = var(2) = 6
value = 19600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire BASE
[State -1, B Aire BASE]
type = ChangeState
triggerall = var(2) < 2
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire BASE
[State -1, B Aire BASE]
type = ChangeState
triggerall = var(2) = 2
value = 11610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire SS1
[State -1, B Aire SS1]
type = ChangeState
triggerall = var(2) = 4
value = 15610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire SS2
[State -1, B Aire SS2]
type = ChangeState
triggerall = var(2) = 5
value = 17610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire SSB2
[State -1, B Aire SSB2]
type = ChangeState
triggerall = var(2) = 6
value = 19610
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
