
[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s

[Defaults]
command.time = 15
command.buffer.time = 1

[Command]
name = "BSG"
command = ~D, DB, B, a+b
time = 20

[Command]
name = "BSG"
command = ~D, DB, B, a+c
time = 20

[Command]
name = "BSG"
command = ~D, DB, B, b+c
time = 20

[Command]
name = "slice-super"
command = ~D, DF, F, b+c
time = 20
[Command]
name = "slice-super"
command = ~D, DF, F, a+c
time = 20

[Command]
name = "slice-super"
command = ~D, DF, F, a+b
time = 20

[Command]
name = "slice-super"
command = ~D, DF, F, b+c
time = 20
[Command]
name = "slice-super"
command = ~D, DF, F, a+c
time = 20


[Command]
name =  "teleport-super"
command = ~D, DF, F, x+y
time = 20

[Command]
name =  "teleport-super"
command = ~D, DF, F, x+z
time = 20

[Command]
name =  "teleport-super"
command = ~D, DF, F, y+z
time = 20

;-| Special Motions |------------------------------------------------------
[Command]
name = "upper_x"
command = ~F, D, DF, x

[Command]
name = "upper_y"
command = ~F, D, DF, y

[Command]
name = "upper_xy"
command = ~F, D, DF, x+y

[Command]
name = "QCF_x"
command = ~D, DF, F, x

[Command]
name = "QCF_y"
command = ~D, DF, F, y
[Command]
name = "QCF_z"
command = ~D, DF, F, z

[Command]
name = "QCF_a"
command = ~D, DF, F, a
[Command]
name = "QCF_a"
command = ~D, DF, F, b

[Command]
name = "QCF_a"
command = ~D, DF, F, c


[Command]
name = "comboA"
command = ~D, DB, B, x
time = 25
[Command]
name = "comboA"
command = ~D, DB, B, y

[Command]
name = "comboA"
command = ~D, DB, B, z

[Command]
name = "comboB"
command = ~D, DB, B, a

[Command]
name = "comboB"
command = ~D, DB, B, b
[Command]
name = "comboB"
command = ~D, DB, B, c


[Command]
name = "forward"     ;Required (do not remove)
command = F
time = 5
[Command]
name = "backward"     ;Required (do not remove)
command = B
time = 5
[Command]
name = "up"     ;Required (do not remove)
command = U
time = 5
[Command]
name = "down"     ;Required (do not remove)
command = D
time = 5


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
name = "recovery";Required (do not remove)
command = x+y
time = 1

;-| Dir + Button |---------------------------------------------------------
[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
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
name = "start"
command = s
time = 1

;-| Hold Dir |--------------------------------------------------------------
[Command]
name = "holdfwd";Required (do not remove)
command = /$F
time = 1

[Command]
name = "holdback";Required (do not remove)
command = /$B
time = 1

[Command]
name = "holdup" ;Required (do not remove)
command = /$U
time = 1

[Command]
name = "holddown";Required (do not remove)
command = /$D
time = 1








;---------------------------------------------------------------------------
;-| AI Command |--------------------------------
[Command]
name = "AI1"
command = a, a, a
time = 1

[Command]
name = "AI2"
command = c, c, c
time = 1

[Command]
name = "AI3"
command = x, x, x
time = 1

[Command]
name = "AI4"
command = z, z, z
time = 1

[Command]
name = "AI5"
command = a, c
time = 1

[Command]
name = "AI6"
command = c, a
time = 1

[Command]
name = "AI7"
command = x, z
time = 1

[Command]
name = "AI8"
command = z, x
time = 1

[Command]
name = "AI9"
command = a, c, a
time = 1

[Command]
name = "AI10"
command = c, a, c
time = 1

[Command]
name = "AI11"
command = x, z, x
time = 1

[Command]
name = "AI12"
command = z, x, z
time = 1

[Command]
name = "AI13"
command = D, DB, B ,a, a, a
time = 1

[Command]
name = "AI14"
command = D, DB, B ,c, c, c
time = 1

[Command]
name = "AI15"
command = D, DB, B ,x, x, x
time = 1

[Command]
name = "AI16"
command = D, DB, B ,z, z, z
time = 1

[Command]
name = "AI17"
command = D, DB, B ,a, c
time = 1

[Command]
name = "AI18"
command = D, DB, B ,c, a
time = 1

[Command]
name = "AI19"
command = D, DB, B ,x, z
time = 1

[Command]
name = "AI20"
command = D, DB, B ,z, x
time = 1

[Command]
name = "AI21"
command = D, DB, B ,a, c, a
time = 1

[Command]
name = "AI22"
command = D, DB, B ,c, a, c
time = 1

[Command]
name = "AI23"
command = D, DB, B ,x, z, x
time = 1

[Command]
name = "AI24"
command = D, DB, B ,z, x, z
time = 1

[Command]
name = "AI25"
command = a, a, a+b
time = 1

[Command]
name = "AI26"
command = b, c, a+b
time = 1

[Command]
name = "AI27"
command = a, c, a+b
time = 1

[Command]
name = "AI28"
command = c, a, a+b
time = 1

[Command]
name = "AI29"
command = x, x, x+y
time = 1

[Command]
name = "AI30"
command = y, y, x+y
time = 1

[Command]
name = "AI31"
command = x, y, x+y
time = 1

[Command]
name = "AI32"
command = z, x, x+y
time = 1

[Command]
name = "AI33"
command = a, a, a, a+b
time = 1

[Command]
name = "AI34"
command = x, x, x, x+y
time = 1






















;---------------------------------------------------------------------------
; 2. State entry
; --------------
[Statedef -1]



[State -1, AI]
type = Varset
trigger1 = command = "AI1"
trigger2 = command = "AI2"
trigger3 = command = "AI3"
trigger4 = command = "AI4"
trigger5 = command = "AI5"
trigger6 = command = "AI6"
trigger7 = command = "AI7"
trigger8 = command = "AI8"
trigger9 = command = "AI9"
trigger10 = command = "AI10"
trigger11 = command = "AI11"
trigger12 = command = "AI12"
trigger13 = command = "AI13"
trigger14 = command = "AI14"
trigger15 = command = "AI15"
trigger16 = command = "AI16"
trigger17 = command = "AI17"
trigger18 = command = "AI18"
trigger19 = command = "AI19"
trigger20 = command = "AI20"
trigger21 = command = "AI21"
trigger22 = command = "AI22"
trigger23 = command = "AI23"
trigger24 = command = "AI24"
trigger25 = command = "AI25"
trigger26 = command = "AI26"
trigger27 = command = "AI27"
trigger28 = command = "AI28"
trigger29 = command = "AI29"
trigger30 = command = "AI30"
trigger31 = command = "AI31"
trigger32 = command = "AI32"
trigger33 = command = "AI33"
trigger34 = command = "AI34"
v = 59
value = 1

[State -1, AI]
type = Varset
trigger1 = IsHomeTeam
trigger1 = TeamSide = 2
v = 59
value = 1

[State -1,AI deactivation]
type = VarSet
trigger1= win = 1
trigger2= lose
trigger3= life <=0
v = 59
value = 0


[State -1, AI]
type=changestate
value = 50
triggerall = var(59) =1
triggerall = pos Y < 0 && stateno != [2000,3000]
triggerall = stateno != 100 || stateno != 101 || stateno != 102
triggerall = stateno != [5000,5500]
trigger1 = 1


[State -1, AI teleport-super]
type=changestate
value = 1999
triggerall= var(59) = 1
triggerall= power>=1000
triggerall = random < 300
triggerall = p2stateno = [5000,5500]
trigger1 = stateno=220 && movehit
trigger2 = stateno=250 && movehit
trigger3 = stateno=420 && movehit
trigger4 = stateno=450 && movehit
trigger5 = stateno = 1200 && movehit
trigger6 = stateno = 1212 && movehit
trigger7= ctrl


[State -1, AI teleport-super]
type=changestate
value = 2500
triggerall= var(59) = 1
triggerall= power>=1000
triggerall = random < 300
triggerall = p2stateno = [5000,5500]
trigger1 = stateno=220 && movehit
trigger2 = stateno=250 && movehit
trigger3 = stateno=420 && movehit
trigger4 = stateno=450 && movehit
trigger5 = stateno = 1200 && movehit
trigger6 = stateno = 1212 && movehit
trigger7= ctrl



[State -1, AI BSG]
type = ChangeState
value = 3000
triggerall = var(59) = 1
triggerall = power >= 3000
triggerall = statetype != A
triggerall = p2statetype !=A
trigger1 = stateno = 1200 && movehit
trigger2 = stateno = 1210 && movehit
trigger3 = stateno = 1500 && movehit
trigger4 = stateno = 1300 && movehit
trigger5 = stateno = 220 && movehit
trigger6 = stateno = 210 && movehit
trigger7 = stateno = 400 && movehit
trigger8 = stateno = 410 && movehit
trigger9 = stateno = 430 && movehit
ignorehitpause =1

[State -1, AI Jump Strong Punch]
type = ChangeState
value = 610
triggerall = var(59) = 1 && p2bodydist x < 40
trigger1 = ctrl && random < 500
trigger2 = stateno = 50 && movecontact
trigger3 = stateno = 620 && movecontact


[State -1, AI Jump Strong Punch]
type = ChangeState
value = 620
triggerall = var(59) = 1 && p2bodydist x < 40
trigger1 = ctrl && random < 500
trigger2 = stateno = 610 && movecontact

[State -1, AI Run Fwd]
type = ChangeState
value = 100
triggerall = var(59) = 1
triggerall = stateno != 22 && stateno != 100
trigger1 = p2movetype != A && statetype != A
trigger1 = ctrl
trigger1 = p2bodydist x = [60,200]
trigger1 = random < 300 && enemy,vel x <= 0

[State -1, AI flashstep]
type=changestate
value=240
triggerall = var(59) = 1
triggerall = stateno != 240
triggerall = p2movetype =A
triggerall = random < 50
trigger1=ctrl
trigger2 = enemy,numproj >= 1

[State -1, AI block]
type=changestate
value=120
triggerall = var(59) = 1
triggerall = p2movetype = A
trigger1=ctrl
trigger2 = enemy,numproj >= 1




[State -1, AI run fwd]
type = ChangeState
value = 100
triggerall = var(59) = 1
triggerall = p2dist X >= 80
trigger1 = stateno = 0


[State -1, AI Stand Light Punch]
type = ChangeState
value = 200
triggerall = var(59) = 1
triggerall = statetype =S && statetype != A
triggerall = stateno != 200 && stateno != [1999,3000]
trigger1 = ctrl
trigger1 = random < 300
trigger1 = p2bodydist x <= 27
trigger2 = stateno = 210 && movecontact
trigger3 = stateno = 230 && movecontact
trigger4 = stateno = 220 && movecontact
trigger5 = stateno = 400 && movecontact
trigger6 = stateno = 410 && movecontact
trigger7 = stateno = 420 && movecontact


[State -1,AI Stand Medium Punch]
type = ChangeState
value = 210
triggerall = var(59) = 1
triggerall = statetype =S && statetype != A
triggerall = stateno != 210 && stateno != [1999,3000]
trigger1 = ctrl
trigger1 = random < 300
trigger1 = p2bodydist x <= 27
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 230 && movecontact
trigger4 = stateno = 220 && movecontact
trigger5 = stateno = 400 && movecontact
trigger6 = stateno = 410 && movecontact
trigger7 = stateno = 420 && movecontact


[State -1,AI Stand Strong Punch]
type = ChangeState
value = 230
triggerall = var(59) = 1
triggerall = statetype =S && statetype != A
triggerall = stateno != 230 && stateno != [1999,3000]
trigger1 = ctrl
trigger1 = random < 300
trigger1 = p2bodydist x <= 27
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 210 && movecontact
trigger4 = stateno = 220 && movecontact
trigger5 = stateno = 400 && movecontact
trigger6 = stateno = 410 && movecontact
trigger7 = stateno = 420 && movecontact



[State -1,AI Crouch Strong Kick]
type = ChangeState
value = 400
triggerall = var(59) = 1
triggerall = p2bodydist x = [-2,44]
triggerall = P2MoveType != A
triggerall = stateno != 400 && stateno != [1999,3000]
trigger1 = stateno = 410
trigger1 = movehit
trigger1 = random < 100
trigger2 = stateno = 210
trigger2 = movehit
trigger2 = random < 50



[State -1,AI Crouch Medium Punch]
type = ChangeState
value = 410
triggerall = var(59) = 1
triggerall = p2statetype != A && p2statetype != L
trigger1 = stateno = 400 || stateno = 430
trigger1 = movehit && random < 200


[State -1, AI crouch punch]
type = ChangeState
value = 420
triggerall = var(59) = 1
triggerall = statetype != A
triggerall = p2movetype != A
triggerall = stateno != 420 && stateno != [1999,3000]
triggerall = random < 600
trigger1 = ctrl
trigger2 = stateno = 210 && movehit
trigger3 = stateno =  200 && movehit
trigger4 = stateno = 230 && movehit
trigger5 = stateno = 400 && movehit
trigger6 = stateno = 410 && movehit

[State -1, AI Crouching Medium Kick]
type = ChangeState
value = 1200
triggerall = var(59) = 1
triggerall = statetype != A
triggerall = p2statetype != A
triggerall = stateno =0
triggerall = P2bodydist X <= 110
trigger1 = random < 300
trigger1 = ctrl

[State -1, AI Crouching Medium Kick]
type = ChangeState
value = 1202
triggerall = var(59) = 1
triggerall = statetype != A
triggerall = p2statetype != A
triggerall = stateno = 1200 && movehit
trigger1 = random < 600

[State -1, AI Crouching Medium Kick]
type = ChangeState
value = 1204
triggerall = var(59) = 1
triggerall = statetype != A
triggerall = p2statetype != A
triggerall = stateno = 1202
trigger1 = random < 600

[State -1, AI backrun]
type=changestate
value=102
trigger1= var(59) = 1
trigger1= statetype = S
trigger1= random < ifelse((enemynear,hitdefattr=SC,AT), 150, 50)
trigger1= ctrl

[State -1, AI]
type = ChangeState
value = 1210
triggerall = var(59) = 1
triggerall = stateno =0
triggerall = P2bodydist X <= 110
trigger1 = random < 300
trigger1 = ctrl

[State -1, AI]
type = ChangeState
value = 1212
triggerall = var(59) = 1
triggerall = stateno = 1210 && movehit
trigger1 = random < 600

[State -1, AI]
type = ChangeState
value = 1214
triggerall = var(59) = 1
triggerall = stateno = 1212 && movehit
trigger1 = random < 600

[State -1, AI Jump]
type=changestate
value=40
trigger1= var(59) = 1
trigger1= statetype!=A
trigger1 = ctrl
trigger1= enemynear,movetype=A && p2bodydist x<160 && enemynear,hitdefattr=SC,AT
trigger2 = stateno = 420 && movecontact


;---------------------------------------------------------------------------
;===========================================================================
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
;===========================================================================
;---------------------------------------------------------------------------
;---------------------------HUMAN-FRIENDLY-ATTACKS--------------------------
;===========================================================================
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
;===========================================================================
;hyper move - BSG
[State -1, BloodySG]
type = ChangeState
value = 3000
triggerall = command = "BSG"
triggerall = power >= 3000
triggerall = var(59) !=1
trigger1 = ctrl
trigger1 = statetype != A
trigger2 = hitdefattr = SC, NA, SA, HA
trigger2 = stateno != [3050,3100]
trigger2 = stateno != [1999,2014]
trigger3 = stateno = 200 && movecontact
trigger4 = stateno = 210 && movecontact
trigger6 = stateno = 230 && movecontact
trigger7 = stateno = 600 && movecontact
trigger8 = stateno = 610 && movecontact
trigger9 = stateno = 620 && movecontact
trigger10 = stateno = 1210 && movecontact
trigger11 = stateno = 1212 && movecontact
trigger12 = stateno = 1214 && movecontact
trigger13 = stateno = 1200 && movecontact
trigger14 = stateno = 1210 && movecontact
trigger15 = stateno = 1212 && movecontact
trigger16 = stateno = 1214 && movecontact

;super move - flash step
[State -1, flash attack]
type = ChangeState
value = 2500
triggerall = command = "slice-super"
triggerall = power >= 1000
triggerall = var(59) !=1
trigger1 = ctrl
trigger2 = stateno != [3050,3100]
trigger2 = stateno != [1999,2014]
trigger3 = stateno = 200 && movecontact
trigger4 = stateno = 210 && movecontact
trigger6 = stateno = 230 && movecontact
trigger7 = stateno = 600 && movecontact
trigger8 = stateno = 610 && movecontact
trigger9 = stateno = 620 && movecontact
trigger10 = stateno = 1210 && movecontact
trigger11 = stateno = 1212 && movecontact
trigger12 = stateno = 1214 && movecontact
trigger13 = stateno = 1200 && movecontact
trigger14 = stateno = 1210 && movecontact
trigger15 = stateno = 1212 && movecontact
trigger16 = stateno = 1214 && movecontact

;===========================================================================
;super move - teleport
[State -1, teleport super (A)]
type = ChangeState
value = 1999
triggerall = command = "teleport-super"
triggerall = power >= 1000
triggerall = var(59) !=1
triggerall = stateno != 1999
triggerall = stateno != 2000
triggerall = stateno != 2002
triggerall = stateno != 2004
trigger1 = ctrl
trigger2 = stateno = 620 && movecontact
trigger3 = stateno = 1200 && movecontact
trigger4 = stateno = 1202 && movecontact
trigger5 = stateno = 1204 && movecontact
trigger6 = stateno = 1210 && movecontact
trigger7 = stateno = 1212 && movecontact
trigger8 = stateno = 1214 && movecontact

;=============================================
;combo condition
;=============================================
[State -1, Combo condition Reset]
type = VarSet
trigger1 = 1
var(1) = 0

[State -1, Combo condition Check]
type = VarSet
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = (stateno = [200,299]) || (stateno = [400,499])
trigger2 = stateno != 440
var(1) = 1
;============================================================================
;Special (x)
[State -1, strike (X)]
type = ChangeState
value = 1300
triggerall = var(59) !=1
triggerall = command = "QCF_x"
trigger1 = var(1)

;Special (y)
[State -1, strike (X)]
type = ChangeState
value = 1300
triggerall = var(59) !=1
triggerall = command = "QCF_y"
trigger1 = var(1)

;Special (z)
[State -1, strike (X)]
type = ChangeState
value = 1300
triggerall = var(59) !=1
triggerall = command = "QCF_z"
trigger1 = var(1)
;============================================================================
;Special (c)  comboB 1
[State -1, spec (A) comboB1 + air]
type = ChangeState
value = 1210
triggerall = command = "comboB"
triggerall = var(59) !=1
trigger1 = ctrl
trigger2 = stateno = 100 || stateno = 52
trigger3 = stateno = 200 && movecontact
trigger4 = stateno = 210 && movecontact
trigger5 = stateno = 230 && movecontact
trigger6 = stateno = 400 && movecontact
trigger7 = stateno = 410 && movecontact
trigger8 = stateno = 420 && movecontact
trigger9 = stateno = 1220 && movecontact

;Special (c)  comboB 2
[State -1, spec (A) comboB2 + air]
type = ChangeState
value = 1212
triggerall = command = "comboB"
triggerall = var(59) !=1
trigger1 = ctrl
trigger2 = stateno = 1210 && movecontact

;Special (c)  comboB 3
[State -1, spec (A) comboB3 + air]
type = ChangeState
value = 1214
triggerall = command = "comboB"
triggerall = var(59) !=1
trigger1 = ctrl
trigger2 = stateno = 1212 && movecontact

;=============================================================================
;Special (c)
[State -1, uppercut (A)]
type = ChangeState
value = 1500
triggerall = command = "QCF_a"
triggerall = var(59) !=1
trigger1 = var(1)
trigger1 = (statetype = S) && (ctrl);Special (c)
trigger2 = stateno = 200 && movecontact
GOKU

;=============================================================================
;Special (A) ComboA1
[State -1, spec(A) ComboA1]
type = ChangeState
value = 1200
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = stateno = 101
trigger3 = stateno = 600 && movecontact
trigger4 = stateno = 610 && movecontact
trigger5 = stateno = 620 && movecontact
;---------------------------------------------------------------------------
;Special (A) ComboA2
[State -1, spec(A) ComboA2]
type = ChangeState
value = 1202
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1= statetype != A
trigger1 = ctrl
trigger2 = stateno = 1200 && movecontact

;Special (A) ComboA3
[State -1, spec(A) Combo3A]
type = ChangeState
value = 1204
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1= statetype != A
trigger1 = ctrl
trigger2 = stateno = 1202 && movecontact

;---------------------------------------------------------------------------
;Special (A) ComboA1  + AIR
[State -1, Spec(A) ComboA1 + air]
type = ChangeState
value = 1210
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1 = statetype != S
trigger1 = ctrl
trigger2 = stateno = 101
trigger6 = stateno = 600 && movecontact
trigger7 = stateno = 610 && movecontact
trigger8 = stateno = 620 && movecontact

;Special (A) ComboA2 + AIR
[State -1, Spec(A) ComboA2 +air]
type = ChangeState
value = 1212
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1= statetype != S
trigger1 = ctrl
trigger2 = stateno = 1210 && movecontact

;Special (A) ComboA3 + AIR
[State -1, Spec(A) Combo3A +air]
type = ChangeState
value = 1214
triggerall = command = "comboA"
triggerall = var(59) !=1
trigger1 = statetype != S
trigger1 = ctrl
trigger2 = stateno = 1212 && movecontact

;===========================================================================
;---------------------------------------------------------------------------
;Run Fwd
[State -1, Run Fwd]
type = ChangeState
value = 100
triggerall = var(59) !=1
trigger1 = command = "FF"
trigger1 = statetype = S
trigger1 = statetype !=A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Run Back AIR
[State -1, Run Back]
type = ChangeState
value = 102
triggerall = var(59) !=1
trigger1 = command = "BB"
trigger1 = statetype = A
trigger1 = statetype != S
trigger1 = ctrl
;---------------------------------------------------------------------------
;Run FWD AIR
[State -1, Run Back]
type = ChangeState
value = 101
triggerall = var(59) !=1
trigger1 = command = "FF"
trigger1 = statetype = A
trigger1 = statetype != S
trigger1 = ctrl

;---------------------------------------------------------------------------
;Run Back
[State -1, Run Back]
type = ChangeState
value = 105
trigger1 = command = "BB"
triggerall = var(59) !=1
trigger1 = statetype = S
trigger1 = ctrl



;---------------------------------------------------------------------------
;Kung Fu Throw
;;[State -1, Kung Fu Throw]
;;type = ChangeState
;;value = 800
;;triggerall = Var(9) !=1
;;triggerall = command = "y"
;;triggerall = statetype = S
;;triggerall = ctrl
;;triggerall = stateno != 100
;;trigger1 = command = "holdfwd"
;;trigger1 = p2bodydist X < 3
;;trigger1 = (p2statetype = S) || (p2statetype = C)
;;trigger1 = p2movetype != H
;;trigger2 = command = "holdback"
;;trigger2 = p2bodydist X < 5
;;trigger2 = (p2statetype = S) || (p2statetype = C)
;;trigger2 = p2movetype != H


;===========================================================================
;---------------------------------------------------------------------------
;===========================================================================
[State -1, stand light punch (x)]
type = ChangeState
value = 230
triggerall = (command = "x") && (command != "holddown")
triggerall = var(59) !=1
trigger1 = (statetype = S)  && ctrl
trigger2 = stateno = 400 && movecontact
trigger3 = stateno = 410 && movecontact
trigger4 = stateno = 200 && movecontact
trigger5 = stateno = 210 && movecontact

;---------------------------------------------------------------------------
[State -1, stand medium punch (y)]
type = ChangeState
value = 200
triggerall = (command = "y") && (command != "holddown")
triggerall = var(59) !=1
trigger1 = (statetype = S) && (ctrl)
trigger2 = stateno = 210 && movecontact
trigger3 = stateno = 230 && movecontact
trigger4 = stateno = 400 && movecontact
trigger5 = stateno = 410 && movecontact
trigger6 = stateno = 430 && movecontact


;---------------------------------------------------------------------------
[State -1, stand strong punch (z)]
type = ChangeState
value = 210
triggerall = (command = "z") && (command != "holddown")
triggerall = var(59) !=1
trigger1 = (statetype = S) && (ctrl)
trigger2 = stateno = 230 && movecontact
trigger3 = stateno = 200 && movecontact
trigger4 = stateno = 400 && movecontact
trigger5 = stateno = 410 && movecontact
trigger6 = stateno = 420 && movecontact


;---------------------------------------------------------------------------
[State -1, stand light kick (a)]
type = ChangeState
value = 240
triggerall = (command = "a") && (command != "holddown")
triggerall = var(59) !=1
trigger1 = (statetype = S) && (ctrl)
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 210 && movecontact


;---------------------------------------------------------------------------
[State -1, Stand medium kick (b)]
type = ChangeState
value = 240
triggerall = (command = "b") && (command != "holddown")
triggerall = var(59) !=1
trigger1 = (statetype = S) && (ctrl)

;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
;Taunt--none yet
[State -1, Taunt]
type = ChangeState
value = 195
triggerall = command = "start"
triggerall = var(59) !=1
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Crouching Light Punch
[State -1, crouching Light Punch (x)]
type = ChangeState
value = 400
triggerall = command = "x"
triggerall = command = "holddown"
triggerall = var(59) !=1
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 200 && movecontact
trigger3 = stateno = 210 && movecontact
trigger4 = stateno = 230 && movecontact

;---------------------------------------------------------------------------
;Crouching medium Punch
[State -1, crouching medium Punch (y)]
type = ChangeState
value = 410
triggerall = var(59) !=1
triggerall = command = "y"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 400  && movecontact
trigger3 = stateno = 210  && movecontact
trigger4 = stateno = 230  && movecontact
trigger5 = stateno = 200  && movecontact

;---------------------------------------------------------------------------
;Crouching Strong Punch
[State -1, crouching Strong Punch (z)]
type = ChangeState
value = 420
triggerall = var(59) !=1
triggerall = command = "z"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 400 && movecontact
trigger3 = stateno = 410 && movecontact
trigger4 = stateno = 420 && movecontact
trigger5 = stateno = 200 && movecontact
trigger6 = stateno = 210 && movecontact
trigger7 = stateno = 230 && movecontact

;---------------------------------------------------------------------------
;Crouching Light Kick
[State -1, Crouching Light Kick]
type = ChangeState
value = 230
triggerall = var(59) !=1
triggerall = command = "a"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 400 && movecontact
trigger3 = stateno = 410 && movecontact
trigger4 = stateno = 420 && movecontact
;---------------------------------------------------------------------------
;Crouching Strong Kick
[State -1, Crouching Strong Kick]
type = ChangeState
value = 230
triggerall = var(59) !=1
triggerall = command = "b"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 400 && movecontact
trigger3 = stateno = 410 && movecontact
trigger4 = stateno = 420 && movecontact
;---------------------------------------------------------------------------

;Jump Light Punch
[State -1, Jump Light Punch]
type = ChangeState
value = 600
triggerall = var(59) !=1
triggerall = command = "x"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = statetime >= 7
trigger3 = stateno = 1350 ;Air blocking
trigger1 = ctrl
trigger4 = stateno = 630 && movecontact
;---------------------------------------------------------------------------
;Jump medium Punch
[State -1, Jump medium Punch]
type = ChangeState
value = 610
triggerall = var(59) !=1
triggerall = command = "y"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 || stateno = 630 ;jump_x or jump_a
trigger2 = movecontact
trigger3 = stateno = 1350 ;Air blocking

;---------------------------------------------------------------------------
;Jump Strong Punch
[State -1, Jump strong Punch]
type = ChangeState
value = 620
triggerall = var(59) !=1
triggerall = command = "z"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 610 || stateno = 610
trigger2 = movecontact
trigger3 = stateno = 630 ;jump_x or jump_a
trigger3 = movecontact
trigger4 = stateno = 1350 ;Air blocking

;---------------------------------------------------------------------------
;Jump Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 630
triggerall = var(59) !=1
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 1350 ;Air blocking

;---------------------------------------------------------------------------
[State -1, flashstep (air)]
type = ChangeState
value = 640
triggerall = var(59) !=1
triggerall = var(9) !=1
triggerall = command = "b"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 || stateno = 630 ;jump_x or jump_a
trigger2 = movecontact
trigger3 = stateno = 1350 ;Air blocking

;----------------
;parry CMD by pots
[State -1, standing parry]
type = hitoverride
triggerall = roundstate = 2 && statetype = S
triggerall = command = "forward" && command != "backward" && command!= "up" && command != "down"
trigger1 = ctrl ;|| ((stateno = 700 || stateno = 701) && time >= 8)
attr = SA,AA,AP
stateno = 700
value= 700
slot = 0
time = 8

[State -1, air parry]
type=hitoverride
triggerall = roundstate = 2 && statetype = A
triggerall = command = "forward" && command!="backward" && command!="up" && command!="down"
trigger1 = ctrl || stateno = 702
trigger1 = ctrl || (stateno = 702 && time >= 8)
attr = SA,AA,AP
stateno = 702
forceair = 1
slot = 0
time = 8
