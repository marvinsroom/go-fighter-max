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
name = "Elephant Gatling"
command = ~x
time = 30

[command]
name = "SnakeMan"
command = ~D,DF,F,x
time = 15

[command]
name = "BoundMan"
command = ~D,DB,B,x
time = 15

[command]
name = "Nightmare"
command = x
time = 1

;-| Specials |-------------------------------------------------------
[command]
name = "Red Hawk"
command = ~D,DF,F,a
time = 15

[command]
name = "Jet Pistol"
command = ~D,DB,B,a
time = 15

[command]
name = "Haoshoku Haki"
command = ~D,DF,F,b
time = 15

[command]
name = "Kenbunshoku Haki"
command = ~D,DB,B,b
time = 15

[command]
name = "Eagle Bazooka"
command = ~D,DF,F,c
time = 15

[command]
name = "Hawk Gatling"
command = ~D,DB,B,c
time = 15

[command]
name = "Python Deformed"
command = ~D,DF,F,z
time = 15

[command]
name = "Jet Culverin Gatling"
command = ~D,DB,B,z
time = 15

[command]
name = "Jet Python Left Arm"
command = ~D,DB,B,y
time = 15

[command]
name = "Sword MAX"
command = ~D,DF,F,y
time = 20

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
name = "Stay Away" ;Required (do not remove)
command = D,D
time = 15

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
Triggerall = var(13) = 0
Triggerall = var(14) = 0
Triggerall = var(16) = 0
triggerall = stateno != 2060
triggerall = stateno != 2070
value = 2060
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
Triggerall = var(13) = 0
Triggerall = var(14) = 0
Triggerall = var(16) = 0
triggerall = stateno != 2060
triggerall = stateno != 2070
value = 2070
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
Triggerall = var(13) >  0
triggerall = stateno != 4060
triggerall = stateno != 4070
value = 4060
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan Correr Atras
[State -1, Correr Atras]
type = ChangeState
Triggerall = var(13) >  0
triggerall = stateno != 4060
triggerall = stateno != 4070
value = 4070
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Correr Adelante
[State -1, Nightmare Correr Adelante]
type = ChangeState
Triggerall = var(14) >  0
triggerall = var(5) = 0
triggerall = stateno != 6060
triggerall = stateno != 6065
triggerall = stateno != 6070
value = ifelse(pos y >= 0,6060,6065)
trigger1 = command = "FF"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Correr Atras
[State -1, Nightmare Correr Atras]
type = ChangeState
Triggerall = var(14) >  0
triggerall = var(5) = 0
triggerall = stateno != 6060
triggerall = stateno != 6065
triggerall = stateno != 6070
value = 6070
trigger1 = command = "BB"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Correr Adelante
[State -1, Correr Adelante]
type = ChangeState
Triggerall = var(2) = 0
Triggerall = var(13) = 0
Triggerall = var(14) = 0
Triggerall = var(16) > 0
triggerall = stateno != 70060
triggerall = stateno != 70070
value = 70060
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Correr Atras
[State -1, Correr Atras]
type = ChangeState
Triggerall = var(2) = 0
Triggerall = var(13) = 0
Triggerall = var(14) = 0
Triggerall = var(16) > 0
triggerall = stateno != 70060
triggerall = stateno != 70070
value = 70070
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
value = 80
triggerall = var(13) =  0
triggerall = var(14) =  0
Triggerall = var(16) = 0
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan Super Jump
[State -1, SnakeMan Super Jump]
type = ChangeState
value = 4080
Triggerall = var(13) >  0
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Super Jump
[State -1, Nightmare Super Jump]
type = ChangeState
value = 6080
Triggerall = var(14) >  0
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Super Jump
[State -1, Gear 5 Super Jump]
type = ChangeState
value = 70080
Triggerall = var(16) >  0
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;----------------------------------------------------------------------------
; Nightmare Stay Away
[State -1, Nightmare Stay Away]
type = ChangeState
value = 6324
triggerall = var(14)>0
triggerall = command = "Stay Away"
Triggerall = statetype != A
trigger1 = ctrl
;----------------------------------------------------------------------------
; SnakeMan Stay Away
[State -1, Stay Away]
type = ChangeState
value = 4201
triggerall = var(13)>0
triggerall = command = "Stay Away"
Triggerall = statetype != A
trigger1 = ctrl
;----------------------------------------------------------------------------
; SnakeMan Stay Away Air
[State -1, Stay Away Air]
type = ChangeState
value = 4202
triggerall = var(13)>0
triggerall = command = "Stay Away"
Triggerall = statetype = A
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Supers-----------------------------
;===========================================================================
;---------------------------------------------------------------------------
; Gear4
[State -1, Gear4]
type = ChangeState
triggerall = life > 300
triggerall = power >= 3000
Triggerall = var(16) = 0
Triggerall = var(2) = 0
Triggerall = var(6) = 0
Triggerall = var(13) = 0
triggerall = var(14) = 0
value = 900
triggerall = command = "BoundMan"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear4 - SnakeMan
[State -1, Gear4 - SnakeMan]
type = ChangeState
triggerall = life > 300
triggerall = power >= 3000
Triggerall = var(16) = 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
Triggerall = var(6) = 0
triggerall = var(14) = 0
value = 901
triggerall = command = "SnakeMan"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 4 - TankMan
[State -1, Gear 5]
type = ChangeState
value = 13600
triggerall = power >= 1000
Triggerall = var(16) = 0
Triggerall = var(14) = 0
Triggerall = var(13) = 0
Triggerall = var(6) = 0
Triggerall = var(2) = 0
triggerall = command = "holddown"
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare
[State -1, Nightmare]
type = ChangeState
triggerall = power >= 3000
Triggerall = var(16) = 0
Triggerall = var(14) = 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
value = 5999
triggerall = command != "holddown"
triggerall = command = "Nightmare"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5
[State -1, Gear 5]
type = ChangeState
value = 69999
triggerall = power >= 3000
Triggerall = var(16) = 0
Triggerall = var(14) = 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; King Kong Gun
[State -1, King Kong Gun]
type = ChangeState
triggerall = var(6) = 0
triggerall = life > 200
triggerall = power >= 3000
Triggerall = var(2) > 0
value = 3300
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; King Cobra
[State -1, King Cobra]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = power >= 3000
value = 43005
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Elephant Gatling
[State -1, Nightmare Elephant Gatling]
type = ChangeState
Triggerall = var(16) = 0
Triggerall = var(14) > 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
triggerall = power >= 3000
value = 66300
triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Gear Third Gigant Gattling
[State -1, Nightmare Gear Third Gigant Gattling]
type = ChangeState
Triggerall = var(16) = 0
Triggerall = var(14) > 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
triggerall = power >= 3000
value = 66345
triggerall = command = "SnakeMan"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Ultra Slash
[State -1, Nightmare Ultra Slash]
type = ChangeState
Triggerall = var(16) = 0
Triggerall = var(14) > 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
triggerall = power >= 3000
value = 66315
triggerall = command = "BoundMan"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gomu Gomu Bajrang GUN!!
[State -1, Gomu Gomu Bajrang GUN!]
type = ChangeState
value = 73000
Triggerall = var(16) > 0
Triggerall = var(14) = 0
Triggerall = var(13) = 0
Triggerall = var(2) = 0
Triggerall = power >= 3000
triggerall = var(2)=0
triggerall = command = "x"
triggerall = Statetype != A
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Especiales-------------------------
;===========================================================================
; Red Hawk
[State -1, Red Hawk]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1000
triggerall = command = "Red Hawk"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Kong Gun
[State -1, Kong Gun]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) > 0
Triggerall = power >= 1000
value = 41000
triggerall = command = "Red Hawk"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Jet Culverin Short Distance
[State -1, Jet Culverin Short Distance]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41101
triggerall = command = "Red Hawk"
Triggerall = p2dist x < 255
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Jet Culverin
[State -1, Jet Culverin]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 4999
triggerall = command = "Red Hawk"
Triggerall = statetype != A
Triggerall = p2dist x >= 255
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Jet Culverin Air
[State -1, Jet Culverin Air]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41101
triggerall = command = "Red Hawk"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Gear Thrid Smash
[State -1, Gear Thrid Smash]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1800
triggerall = command = "Red Hawk"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Jet Riffle
[State -1, Jet Riffle]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1100
triggerall = command = "Jet Pistol"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Rino Schneide
[State -1, Rino Schneide]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) > 0
Triggerall = power >= 1000
value = 42000
triggerall = command = "Jet Pistol"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Leg Culverin
[State -1, Leg Culverin]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41499
triggerall = command = "Jet Pistol"
Triggerall = statetype != A
Triggerall = p2dist x >= 255
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Leg Culverin Short Distance
[State -1, Leg Culverin Short Distance]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41501
triggerall = command = "Jet Pistol"
Triggerall = p2dist x < 255
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Leg Culverin Air
[State -1, Leg Culverin Air]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41502
triggerall = command = "Jet Pistol"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Haoshoku Haki
[State -1, Haoshoku Haki]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
triggerall = numhelper(1260) = 0
Triggerall = power >= 1000
value = 1200
triggerall = command = "Haoshoku Haki"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Calverin
[State -1, Culverin]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) > 0
Triggerall = power >= 1000
value = 44000
triggerall = command = "Haoshoku Haki"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Double Culverins
[State -1, Double Culverins]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 41649
triggerall = command = "Haoshoku Haki"
Triggerall = statetype != A
Triggerall = p2dist x >= 255
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Double Culverins Short Distance
[State -1, Double Culverins Short Distance]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 41651
triggerall = command = "Haoshoku Haki"
Triggerall = p2dist x < 255
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Double Culverins Air
[State -1, Double Culverins Air]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 41651
triggerall = command = "Haoshoku Haki"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Kenbunshoku Haki
[State -1, Kenbunshoku Haki]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
triggerall = numhelper(1360) = 0
triggerall = numhelper(1350) = 0
Triggerall = power >= 1000
value = 1300
triggerall = command = "Kenbunshoku Haki"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Taunt
[State -1, Taunt]
type = ChangeState
triggerall = var(2) > 0
Triggerall = power >= 1000
value = 45000
triggerall = command = "Kenbunshoku Haki"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Jet Python Short Distance
[State -1, Jet Python Short Distance]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41851
triggerall = command = "Kenbunshoku Haki"
Triggerall = p2dist x < 255
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Jet Python
[State -1, Jet Python]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 41849
triggerall = command = "Kenbunshoku Haki"
Triggerall = statetype != A
Triggerall = p2dist x >= 255
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Jet Python Air
[State -1, Jet Python Air]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 41851
triggerall = command = "Kenbunshoku Haki"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Jet Hammer
[State -1, Jet Hammer]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1900
triggerall = command = "Kenbunshoku Haki"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Jet Gatoringu
[State -1, Jet Gatoringu]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1600
triggerall = command = "Hawk Gatling"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Kong Organ
[State -1, Kong Organ]
type = ChangeState
triggerall = var(2) > 0
Triggerall = power >= 1500
value = 46000
triggerall = command = "Hawk Gatling"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Black Mamba Short
[State -1, Black Mamba Short]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
Triggerall = power >= 2000
value = 42950
triggerall = command = "Hawk Gatling"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Eagle Bazooka
[State -1, Eagle Bazooka]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 1400
triggerall = command = "Eagle Bazooka"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Leo Bazooka
[State -1, Leo Bazooka]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2) > 0
Triggerall = power >= 2000
value = 43000
triggerall = command = "Eagle Bazooka"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Black Mamba
[State -1, Jet Python Short Distance]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
Triggerall = power >= 2500
value = 42500
triggerall = command = "Eagle Bazooka"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Jet Bazooka
[State -1, Jet Bazooka]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 1700
triggerall = command = "Eagle Bazooka"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Hawk Gatling
[State -1, Hawk Gatling]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 1500
triggerall = command = "Hawk Gatling"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Jet Culverin Gattling
[State -1, Jet Culverin Gattling]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 43550
triggerall = command = "Jet Culverin Gatling"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Jet Python Left Arm
[State -1, Jet Python Left Arm]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
Triggerall = power >= 2000
value = 41950
triggerall = command = "Jet Python Left Arm"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Python Deformed
[State -1, Python Deformed]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(6) = 0
triggerall = var(13) > 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power >= 2500
value = 43500
triggerall = command = "Python Deformed"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Nightmare Arrow
[State -1, Nightmare Arrow]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 641000
triggerall = command = "Red Hawk"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Nightmare FireBall
[State -1, Nightmare FireBall]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 644000
triggerall = command = "Jet Pistol"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Nightmare Dash Cut
[State -1, Nightmare Dash Cut]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 61204
triggerall = command = "Haoshoku Haki"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Nightmare Gattling Gun
[State -1, Nightmare Gattling Gun]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1850
value = 64998
triggerall = command = "Kenbunshoku Haki"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Nightmare Storm
[State -1, Nightmare Storm]
type = ChangeState
value = 64300
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Eagle Bazooka"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Elephant Gun 
[State -1, Nightmare Elephant Gun]
type = ChangeState
value = 640000
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Hawk Gatling"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Taunt
[State -1, Nightmare Taunt]
type = ChangeState
value = 6866
Triggerall = power >= 500
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Jet Python Left Arm"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Sword MAX
[State -1, Nightmare Sword MAX]
type = ChangeState
value = 6920
Triggerall = power >= 2300
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Sword MAX"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Gigant Riffle
[State -1, Nightmare Gigant Riffle]
type = ChangeState
value = 6925
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Jet Culverin Gatling"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Grizzly Magnum
[State -1, Nightmare Grizzly Magnum]
type = ChangeState
value = 6930
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "Python Deformed"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Arrow Air
[State -1, Nightmare Arrow Air]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1000
value = 6945
triggerall = command = "Red Hawk"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Gattling Gun Air
[State -1, Nightmare Gattling Gun Air]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power >= 1500
value = 6941
triggerall = command = "Kenbunshoku Haki"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Pistoru!
[State -1, Nightmare Pistoru!]
type = ChangeState
value = 6940
Triggerall = power >= 2400
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Rubber Ray
[State -1, Rubber Ray]
type = ChangeState
value = 71000
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Red Hawk"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gigant Stomp
[State -1, Gigant Stomp]
type = ChangeState
value = 71150
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Jet Pistol"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Rolling The World
[State -1, Rolling The World]
type = ChangeState
value = 71170
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Kenbunshoku Haki"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Giant Assault
[State -1, Giant Assault]
type = ChangeState
value = 71682
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Haoshoku Haki"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Giant Hand
[State -1, Giant Hand]
type = ChangeState
value = 71350
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Eagle Bazooka"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Sky Fury
[State -1, Sky Fury]
type = ChangeState
value = 71500
Triggerall = power >= 2000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Hawk Gatling"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Giant Throw
[State -1, Giant Throw]
type = ChangeState
value = 71550
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Sword MAX"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Giant Head
[State -1, Giant Head]
type = ChangeState
value = 71560
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Jet Python Left Arm"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Se Desconocieron
[State -1, Se Desconocieron]
type = ChangeState
value = 71570
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Jet Culverin Gatling"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Giant Lift Up
[State -1, Giant Lift Up]
type = ChangeState
value = 71615
Triggerall = power >= 1000
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "Python Deformed"
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 200
type = PlaySnd
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 A
[State -1, A]
type = ChangeState
value = 2200
type = PlaySnd
triggerall = var(2) > 0
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 A - Down 
[State -1, G4 A - Down]
type = ChangeState
value = 2221
triggerall = var(2) > 0
triggerall = command = "holddown"
triggerall = command = "a"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - A
[State -1, SnakeMan - A]
type = ChangeState
value = 4200
type = PlaySnd
triggerall = var(13) > 0
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A - Down SnakeMan
[State -1, A - Down SnakeMan]
type = ChangeState
value = 4510
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A - Down SnakeMan Air
[State -1, A - Down SnakeMan Air]
type = ChangeState
value = 4515
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 300
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 B
[State -1, B]
type = ChangeState
value = 2300
triggerall = var(2) > 0
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 B - Down 
[State -1, G4 B - Down]
type = ChangeState
value = 2321
triggerall = var(2) > 0
triggerall = command = "holddown"
triggerall = command = "b"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - B
[State -1, SnakeMan - B]
type = ChangeState
value = 4300
type = PlaySnd
triggerall = var(13) > 0
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B - Down SnakeMan
[State -1, B - Down SnakeMan]
type = ChangeState
value = 4520
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B - Down SnakeMan Air
[State -1, B - Down SnakeMan Air]
type = ChangeState
value = 4521
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 400
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 2400
triggerall = var(2) > 0
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - C
[State -1, SnakeMan - C]
type = ChangeState
value = 4400
triggerall = var(13) > 0
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C - Down SnakeMan
[State -1, C - Down SnakeMan]
type = ChangeState
value = 4412
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C - Down SnakeMan Air
[State -1, C - Down SnakeMan Air]
type = ChangeState
value = 4415
triggerall = var(13) > 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Y
[State -1, SnakeMan - Y]
type = ChangeState
value = 4632
type = PlaySnd
triggerall = var(13) > 0
triggerall = command != "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
Triggerall = power < 3000
value = 500
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Aire
[State -1, Aire]
type = ChangeState
triggerall = var(6) = 0
triggerall = var(2)=0
triggerall = var(5) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 Aire
[State -1, Aire]
type = ChangeState
triggerall = var(2) > 0
value = 2600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Aire - A
[State -1, SnakeMan - Aire - A]
type = ChangeState
triggerall = var(13) > 0
value = 4600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;----------------------------------------------------------------------------
; Aire 2
[State -1, Aire]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(5) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;----------------------------------------------------------------------------
; G4 Aire 2
[State -1, Aire]
type = ChangeState
triggerall = var(2) > 0
triggerall = var(5) = 0
value = 2610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Aire - B
[State -1, SnakeMan - Aire - B]
type = ChangeState
triggerall = var(13) > 0
value = 4610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Aire 2
[State -1, Aire]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(5) = 0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) = 0
value = 800
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; G4 Aire 2
[State -1, Aire]
type = ChangeState
triggerall = var(2) > 0
triggerall = var(5) = 0
value = 2620
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Aire - C
[State -1, SnakeMan - Aire - C]
type = ChangeState
triggerall = var(13) > 0
value = 4630
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Aire - Y
[State -1, SnakeMan - Aire - Y]
type = ChangeState
triggerall = var(13) > 0
value = 4632
triggerall = command = "y"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan - Aire - Z
[State -1, SnakeMan - Aire - Z]
type = ChangeState
triggerall = var(13) > 0
value = 4640
triggerall = command = "z"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare A - 1
[State -1, Nightmare A - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
value = 6200
triggerall = command != "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare A - Down 
[State -1, Nightmare A - Down]
type = ChangeState
value = 6425
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare B - 1
[State -1, Nightmare B - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
value = 6300
triggerall = command != "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare B - Down 
[State -1, Nightmare B - Down]
type = ChangeState
value = 6322
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare C - 1
[State -1, Nightmare C - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
value = 6400
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare C - Down 
[State -1, Nightmare C - Down]
type = ChangeState
value = 6405
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Y - 1
[State -1, Nightmare Y - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
value = 6444
triggerall = command != "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Y - Down 
[State -1, Nightmare Y - Down]
type = ChangeState
value = 6426
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "holddown"
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Z - 1
[State -1, Nightmare Z - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
value = 6410
triggerall = command != "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Z - Down 
[State -1, Nightmare Z - Down]
type = ChangeState
value = 6427
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Z - Aire - 1 
[State -1, Nightmare Aire - 1]
type = ChangeState
value = 6600
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Z - Aire - 2 
[State -1, Nightmare Aire - 2]
type = ChangeState
value = 6605
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Z - Aire - 3
[State -1, Nightmare Aire - 3]
type = ChangeState
value = 6610
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Nightmare Power Charge
[State -1, Nightmare Power Charge]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) > 0
triggerall = var(16) = 0
Triggerall = power < 3000
value = 6500
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; SnakeMan Power Charge
[State -1, Power Charge]
type = ChangeState
triggerall = var(13) > 0
Triggerall = power < 3000
value = 4500
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; SnakeMan Power Charge Air
[State -1, Power Charge Air]
type = ChangeState
triggerall = var(13) > 0
Triggerall = power < 3000
value = 4500
triggerall = command = "s"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 A - 1
[State -1, Gear 5 A - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70200
triggerall = command != "holddown"
triggerall = command = "a"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 A - Down 
[State -1, Gear 5 A - Down]
type = ChangeState
value = 70300
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "holddown"
triggerall = command = "a"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 B - 1
[State -1, Gear 5 B - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70220
triggerall = command != "holddown"
triggerall = command = "b"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 B - Down 
[State -1, Gear 5 B - Down]
type = ChangeState
value = 70310
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "holddown"
triggerall = command = "b"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 C - 1
[State -1, Gear 5 C - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70235
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 C - 1 - Air
[State -1, Gear 5 C - 1 - Air]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70236
triggerall = command != "holddown"
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 C - Down 
[State -1, Gear 5 C - Down]
type = ChangeState
value = 70315
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 C - Down  - Air
[State -1, Gear 5 C - Down - Air]
type = ChangeState
value = 70316
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Y - 1
[State -1, Gear 5 Y - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70245
triggerall = command != "holddown"
triggerall = command = "y"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Y - Down 
[State -1, Gear 5 Y - Down]
type = ChangeState
value = 70437
Triggerall = power >= 500
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
triggerall = var(28) = 0
triggerall = command = "holddown"
triggerall = command = "y"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Z - 1
[State -1, Gear 5 Z - 1]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
value = 70270
triggerall = command != "holddown"
triggerall = command = "z"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Z - Down 
[State -1, Gear 5 Z - Down]
type = ChangeState
value = 70318
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
Triggerall = p2dist x < 175
triggerall = command = "holddown"
triggerall = command = "z"
triggerall = Statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Gear 5 Z - Down  Air
[State -1, Gear 5 Z - Down Air]
type = ChangeState
value = 70319
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
Triggerall = p2dist x >= 175
triggerall = command = "holddown"
triggerall = command = "z"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
triggerall = var(2)=0
triggerall = var(13) = 0
triggerall = var(14) = 0
triggerall = var(16) > 0
Triggerall = power < 3000
value = 70499
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl