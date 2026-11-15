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

;-| Default Values |-------------------------------------------------------
[command]
name = "Suiton Suiryudan no Jutsu"
command = ~D,DF,F,a
time = 15

[command]
name = "Suiton Mizurappa"
command = ~D,DB,B,a
time = 15

[command]
name = "Bakushiki Shojin"
command = ~D,DF,F,b
time = 15

[command]
name = "Explosive Seal"
command = ~D,DB,B,b
time = 15

[command]
name = "Explosive Seal Detonante"
command = ~F,DF,D,DB,B,b
time = 40

[command]
name = "Suiton Shigure"
command = ~D,DF,F,c
time = 15

[command]
name = "Suiton Water Pillars"
command = ~D,DB,B,c
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

;---------- comandos para que la PC active la IA -------------------------
[command]
name = "AI1"
command = b,b,b,b,b,b,b,b,b,b,b
time = 1

[command]
name = "AI2"
command = b,c,b,c,b,c,b,c,b,c,b,c
time = 1

[command]
name = "AI3"
command = b,c,b,c,b,c,b,c,b,c,b
time = 1

[command]
name = "AI4"
command = a,b,a,b,a,b,a,b,a,b,a
time = 1

[command]
name = "AI5"
command = b,a,b,a,b,a,b,a,b,a,b
time = 1

[command]
name = "AI6"
command = b,b,b,b,z,b,z,b,z,z,z
time = 1

[command]
name = "AI7"
command = b,x,b,b,x,b,b,b,b,b,x
time = 1

[command]
name = "AI8"
command = b,y,b,b,b,y,b,b,b,b,y
time = 1

[command]
name = "AI9"
command = b,b,b,b,s,z,y,x,c,b,a
time = 1

[command]
name = "AI10"
command = z,b,x,y,b,b,c,b,b,b,a
time = 1

[command]
name = "AI11"
command = b,x,b,b,x,b,b,b,b,b,z
time = 1

[command]
name = "AI12"
command = b,y,b,s,b,y,b,b,b,b,y
time = 1

[command]
name = "AI13"
command = b,b,b,z,s,z,y,x,c,b,a
time = 1

[command]
name = "AI14"
command = z,b,x,y,b,b,c,b,b,c,a
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
triggerall = Var(9) = 0
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
trigger1 = Var(9) = 0
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Jump
[State -1, Super Jump]
type = ChangeState
value = 80
triggerall = Var(9) = 0
trigger1 = Var(9) = 0
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Supers-----------------------------
;---------------------------------------------------------------------------
; Ukojizai no Jutsu
[State -1, Ukojizai no Jutsu]
type = ChangeState
Triggerall = numhelper(3003) = 0
Triggerall = power >= 1500
value = 3000
triggerall = command = "holddown"
triggerall = Var(9) = 0
triggerall = command = "a"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Sword Rampage
[State -1, Sword Rampage]
type = ChangeState
Triggerall = power >= 2000
value = 3100
triggerall = command = "x"
triggerall = Var(9) = 0
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
;===========================================================================
;--------------------------------Ataques Especiales-------------------------
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; Suiton Suiryudan no Jutsu
[State -1, Suiton Suiryudan no Jutsu]
type = ChangeState
Triggerall = numhelper(1050) = 0
Triggerall = power >= 1000
value = 1000
triggerall = command = "Suiton Suiryudan no Jutsu"
trigger1 = statetype != A
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Suiton Mizurappa
[State -1, Suiton Mizurappa]
type = ChangeState
Triggerall = power >= 1000
value = 1100
triggerall = command = "Suiton Mizurappa"
trigger1 = statetype != A
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Bakushiki Shojin
[State -1, Bakushiki Shojin]
type = ChangeState
triggerall = pos y = 0
Triggerall = power >= 1000
value = 1200
triggerall = command = "Explosive Seal"
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Explosive Seal
[State -1, Explosive Seal]
type = ChangeState
Triggerall = power >= 1000
value = 1300
triggerall = command = "Bakushiki Shojin"
trigger1 = statetype != A
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Suiton Shigure
[State -1, Suiton Shigure]
type = ChangeState
Triggerall = power >= 1000
value = 1400
triggerall = command = "Suiton Shigure"
trigger1 = statetype != A
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

;---------------------------------------------------------------------------
; Suiton Water Pillars
[State -1, Suiton Water Pillars]
type = ChangeState
Triggerall = power >= 1500
value = 1500
triggerall = command = "Suiton Water Pillars"
trigger1 = statetype != A
trigger1 = ctrl
triggerall = Var(9) = 0
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)

[State -1,Suiton Goshokuzame]
type = ChangeState
triggerall = Power>=1000
triggerall = Numhelper(10252) = 0
triggerall = Stateno = 10000
trigger1 = command = "Suiton Suiryudan no Jutsu"
trigger1 = Var(9) = 0
trigger2 = var(9) = 1
trigger2 = P2bodydist x>=0
trigger2 = P2movetype!=A
trigger2 = !Win || !Lose|| !Drawgame
trigger2 = Var(3)>=50
trigger2 = (random<var(50)*1.1)*20
trigger2 = P2Movetype!=H
trigger2 = P2stateno!=[5000,5201]
value = 10251
ctrl = 0

[State -1,Hiraishin no Shark]
type = ChangeState
triggerall = Power>=2000
triggerall = Stateno = 10000
trigger1 = command = "Bakushiki Shojin"
trigger1 = Var(9) = 0
trigger2 = var(9) = 1
trigger2 = P2bodydist x>=0
trigger2 = P2bodydist x <150
trigger2 = P2movetype!=A
trigger2 = !Win || !Lose|| !Drawgame
trigger2 = Var(3)>=50
trigger2 = (random<var(50)*1.1)*20
trigger2 = P2Movetype!=H
trigger2 = P2stateno!=[5000,5201]
value = 10260
ctrl = 0

[State -1,Suiton Daikodan no Jutsu]
type = ChangeState
triggerall = Power>=3000
triggerall = Stateno = 10000
trigger1 = command = "Suiton Shigure"
trigger1 = Var(9) = 0
trigger2 = var(9) = 1
trigger2 = P2bodydist x>=0
trigger2 = P2movetype!=A
trigger2 = !Win || !Lose|| !Drawgame
trigger2 = Var(3)>=50
trigger2 = (random<var(50)*1.1)*20
trigger2 = P2Movetype!=H
trigger2 = P2stateno!=[5000,5201]
value = 10270
ctrl = 0

;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; Combo 1
[State -1, Combo 1]
type = ChangeState
value = 200
triggerall = command = "a"
triggerall = Var(9) = 0
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Combo 2
[State -1, Combo 2]
type = ChangeState
value = 300
triggerall = command = "b"
triggerall = Var(9) = 0
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Combo 3
[State -1, Combo 3]
type = ChangeState
value = 400
triggerall = command = "c"
triggerall = Var(9) = 0
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Air Combo
[State -1, Air Combo]
type = ChangeState
value = 600
triggerall = command = "a" || command = "b" || command = "c"
triggerall = Var(9) = 0
Triggerall = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command = "s"
triggerall = Var(9) = 0
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, Awakening]
type = ChangeState
Triggerall = var(2) = 0
Triggerall = life < lifemax /2
Triggerall = power = 3000
value = 550
triggerall = command = "s"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, >Inteligencia Artificial<]
Type=Null
Trigger1 = !time
;-------------------------------------------------------------------------------
; Activar IA
;-------------------------------------------------------------------------------
[State -2, Activar IA]
type = VarSet
trigger1 = Ailevel > 0
var(9) = 1

[State -2, Desactivar IA]
type = VarSet
trigger1 = Ailevel = 0 || Win || Lose || DrawGame
var(9) = 0

[State -1, AI Dificuldade]
Type=VarSet
Trigger1 = Ailevel>0
var(50)=(AILevel=1)*3+(AILevel=2)*7+(AILevel=3)*16+(AILevel=4)*30+(AILevel=5)*58+(AILevel=6)*90+(AILevel=7)*150+(AILevel=8)*300
;===============================================================================
; IA de Defensa
[State -3, IA de Defensa]
type = ChangeState
value = 132
triggerall = p2movetype = A || (enemy, NumProj >= 1) ;
triggerall = P2bodydist X <= 50 || (enemy, NumProj >= 1)
triggerall = statetype = A ; Activo unicamente si estas en el Aire
triggerall = (random<var(50)*1.1)*20 ; Aquí le ponemos un poco de aleteoriedad
triggerall = var(9) = 1 ; La variable que activa la AI
triggerall = ctrl
triggerall = stateno != 132
triggerall = Stateno !=[10000,15000]
trigger1 = p2statetype = A
trigger2 = (enemy, NumProj >= 1)

[State -3, IA de Defensa]
type = ChangeState
value = 130
triggerall = p2movetype = A || (enemy, NumProj >= 1)
triggerall = P2bodydist X <= 50 || (enemy, NumProj >= 1)
triggerall = (random<var(50)*1.1)*20
triggerall = Stateno !=[10000,15000]
triggerall = statetype != A
triggerall = var(9) = 1
triggerall = ctrl
triggerall = stateno != 120
trigger1 = p2statetype = S
trigger2 = (enemy, NumProj >= 1)

; Correr:
[State -3, Correr Adelante]
type = ChangeState
triggerall = var(9) = 1 && roundstate = 2
triggerall = ctrl
triggerall = Stateno !=[10000,15000]
triggerall = stateno !=60
triggerall = stateno !=70
trigger1 = P2bodydist X >= 100 && random<var(50)*1.1
value = 60

[State -3, Correr Atras]
type = ChangeState
triggerall = var(9) = 1 && roundstate = 2
triggerall = ctrl
triggerall = Stateno !=[10000,15000]
triggerall = stateno !=60
triggerall = stateno !=70
Triggerall = p2movetype = A
trigger1 = P2bodydist X = [0,100]
trigger1 =  random<var(50)*1.1
value = 70
;===============================================================================
;--------------------------Ataques IA-------------------------------------------
;===============================================================================
;-----------------------Supers--------------------------------------------------
;===============================================================================
[State -1, Ukojizai no Jutsu]
type = changestate
Triggerall = numhelper(3003) = 0
Triggerall = power >= 2000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X >= 80
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
value = 3000

[State -1, Sword Rampage]
type = changestate
Triggerall = power >= 2500
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X >= 60
trigger1 = p2bodydist x >= 100
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
value = 3100

[State -1, Suiton Double Daibakufu no Jutsu]
type = changestate
Triggerall = power >= 3000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X >= 100
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
value = 3200
;===============================================================================
;-------------------------Especiales--------------------------------------------
;===============================================================================
[State -1, Suiton Suiryudan no Jutsu]
type = changestate
Triggerall = power >= 1000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X = [0,200]
triggerall = Stateno !=[10000,15000]
trigger1 = ctrl
trigger1 = random<var(50)*1.1
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1000

[State -1, Suiton Mizurappa]
type = changestate
Triggerall = power >= 1000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = p2bodydist x >= -40
triggerall = Stateno !=[10000,15000]
trigger1 = p2bodydist x >= 40
trigger1 = random<var(50)*1.1
trigger1 = Ctrl
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1100

[State -1, Bakushiki Shojin] ;triggerall = StateType = S
type = changestate
triggerall = pos y = 0
Triggerall = power >= 1000
triggerall = RoundState = 2 && var(9)
triggerall = P2BodyDist X = [40,150]
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1200

[State -1, Explosive Seal]
type = changestate
Triggerall = power >= 1000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X >= 60
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
trigger1 = animelem = 8
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1300

[State -1, Suiton Shigure]
type = changestate
Triggerall = power >= 1500
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X = [100,200]
triggerall = Stateno !=[10000,15000]
trigger1 = ctrl
trigger1 = random<var(50)*1.1
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1400

[State -1, Suiton Water Pillars]
type = changestate
Triggerall = power >= 1500
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist x = [0,60]
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
trigger2 = movehit && (stateno = 200 || Stateno = 210 || Stateno = 220)
trigger3 = movehit && (stateno = 300 || Stateno = 310 || Stateno = 320)
trigger4 = movehit && (stateno = 400 || Stateno = 410)
value = 1500
;===============================================================================
;----------------Normales-------------------------------------------------------
;===============================================================================
[State -1, Combo 1 - 1]
type = changestate
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X = [0,20]
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
value = 200

[State -1, Combo 2 - 1]
type = changestate
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = P2BodyDist X = [0,25]
triggerall = Stateno !=[10000,15000]
trigger1 = ctrl = 1
trigger1 = random<var(50)*1.1
value = 300

[State -1, Combo 3 - 1]
type = changestate
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = Stateno !=[10000,15000]
triggerall = P2BodyDist X = [0,30]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
value = 400

[State -1, Power Charge]
type = changestate
triggerall = power < 3000
triggerall = RoundState = 2 && var(9)
triggerall = StateType = S
triggerall = Ctrl
triggerall = P2BodyDist X >= 50
triggerall = Stateno !=[10000,15000]
trigger1 = power < 1000 && random<var(50)*1.1
trigger2 = power < 2000 && power > 1000 && Random = [300,500]
trigger3 = power < 3000 && power > 2000 && Random = [100,200]
value = 500

[State -1, Combo Aire - 1]
type = changestate
triggerall = RoundState = 2 && var(9)
triggerall = StateType = A
triggerall = P2BodyDist X = [0,30]
triggerall = Stateno !=[10000,15000]
trigger1 = Ctrl
trigger1 = random<var(50)*1.1
trigger2 = time >= 62 && (stateno = 1200) && random < 20
value = 600

[State -1, Combo Aire - 2]
type = changestate
triggerall = RoundState = 2 && var(9)
triggerall = StateType = A
trigger1 = movecontact && stateno = 600
triggerall = Stateno !=[10000,15000]
trigger1 = random<var(50)*1.1
value = 610

