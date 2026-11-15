;===============================================================================
;-------------------------------Commands----------------------------------------
;===============================================================================
[Remap]
x = z
y = y
z = x
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
name = "ATOMIC"
command = ~x
time = 30

;-| Specials |-------------------------------------------------------
[command]
name = "SKILL 1"
command = ~D,DF,F,a
time = 15

[command]
name = "SKILL 2"
command = ~D,DB,B,a
time = 15

[command]
name = "SKILL 3"
command = ~D,DF,F,b
time = 15

[command]
name = "SKILL 4"
command = ~D,DB,B,b
time = 15

[command]
name = "SKILL 5"
command = ~D,DF,F,c
time = 15

[command]
name = "SKILL 6"
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
;===========================================================================
;----------------------------Skills-----------------------------------------
;---------------------------------------------------------------------------
[Command]
name="cid_taunt"
command=w
time=1

[Command]
name="cid_alpha"
command=/$D,y
time=12
[Command]
name="cid_beta"
command=/$B,y
time=12
[Command]
name="cid_garden"
command=/$D,~x
time=30
[Statedef -1]
[State -1, Seven Shadows ultimate]
type=ChangeState
triggerall=!AILevel && statetype!=A && ctrl
triggerall=power>=3000
triggerall=numhelper(7911)=0 && numhelper(7916)=0
trigger1=command="cid_garden"
value=7920

[State -1, alpha summon super]
type=ChangeState
triggerall=!AILevel && statetype!=A && ctrl
triggerall=power>=1000
triggerall=numhelper(7911)=0 && numhelper(7916)=0
trigger1=command="cid_alpha"
value=7910

[State -1, beta summon super]
type=ChangeState
triggerall=!AILevel && statetype!=A && ctrl
triggerall=power>=1000
triggerall=numhelper(7911)=0 && numhelper(7916)=0
trigger1=command="cid_beta"
value=7915


[State -1, Hood taunt]
type=ChangeState
triggerall=!AILevel
triggerall=statetype=S
triggerall=ctrl
trigger1=command="cid_taunt"
value=7900


[State -1, Spin]
Type = ChangeState
TriggerAll = !AiLevel
TriggerAll = RoundState = 2
TriggerAll = StateType = A
TriggerAll = Power >= 1100
TriggerAll = Command = "down_c"
Value = 630
Trigger1 = Ctrl

;=============================
;----------------------------
;Down - A
[State 0, Air Stab]
Type = ChangeState
Trigger1 = !AiLevel
Trigger1 = Ctrl
Trigger1 = StateType != A
TriggerAll = Power >= 500
Trigger1 = Command = "down_a"
Value = 250
;----------------------------
;Down - B
[State 0, Uppercut]
Type = ChangeState
Trigger1 = !AiLevel
Trigger1 = Ctrl
Trigger1 = StateNO != 900
Trigger1 = StateType != A
Trigger1 = Command = "b" && command = "holddown"
Value = 340

[State -1, Deflect]
Type = ChangeState
Trigger1 = !AiLevel
Trigger1 = StateType != A
Trigger1 = Command = "b" && command = "holddown"
Trigger1 = GetHitVar(Guarded) = 1
Trigger1 = EnemyNear,HitdefAttr = SC,NA,SA,NT,ST
Value = 340
IgnoreHitPause = 1
;----------------------------
;Down - C
[State 0]
Type = ChangeState
Trigger1 = !AiLevel
Trigger1 = Ctrl
Trigger1 = StateNO != 900
Trigger1 = StateType != A
TriggerAll = Power >= 400
Trigger1 = Command = "c" && command = "holddown"
Value = 455

[State -1, Deflect]
Type = ChangeState
Trigger1 = !AiLevel
Trigger1 = StateType != A
triggerall = power >= 400
Trigger1 = Command = "c" && command = "holddown"
Trigger1 = GetHitVar(Guarded) = 1
Trigger1 = EnemyNear,HitdefAttr = SC,NA,SA,NT,ST
Value = 455
IgnoreHitPause = 1

;----------------------------
;=============================

[state 0]
type = null
triggerall = (time % 3 = 0) && (alive)
trigger1 = (var(57) := 6)
trigger1 = (var(58) := 1 + ((random % 16) - (ailevel)))
trigger1 = (var(53) := 9) && ((fvar(35) := 64) && (fvar(36) := 0) && (fvar(37) := 128))
;===========================================================================
;-------------------------------Basics--------------------------------------
;---------------------------------------------------------------------------
; Dash Forward
[State -1, Dash Forward]
type = ChangeState
TriggerAll = !AiLevel
triggerall = stateno != 61
triggerall = stateno != 70
value = 61;60
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Dash Backward
[State -1, Dash bacc]
type = ChangeState
TriggerAll = !AiLevel
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
TriggerAll = !AiLevel
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;SUPERS:
;===========================================================================
; Atomic / All range Atomic
[State -1, Atomic]
type = ChangeState
triggerall = numhelper(3050) = 0
Triggerall = power >= 3000
TriggerAll = !AiLevel
triggerall = command = "ATOMIC"
Triggerall = statetype != A
value = 3000
trigger1 = ctrl
;===================================
;Final Atomic
[State -1, I'm Atomic]
Type = ChangeState
TriggerAll = !AiLevel
Triggerall = power >= 3000
triggerall = p2life <= lifemax/3
TriggerAll = Command = "ATOMIC"
TriggerAll = StateType = A
Value = 4000
Trigger1 = Ctrl
;===================================
; Atomic Sword Release
[State -1, Atomic Sword]
type = ChangeState
TriggerAll = !AiLevel
Triggerall = power >= 2000
value = 11230
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
;===========================================================================
;SPECIALS:
;===========================================================================
; Quite simple
[State -1, Simple Hit]
type = ChangeState
Triggerall = power >= 1000
TriggerAll = !AiLevel
value = 1000
triggerall = command = "SKILL 1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Watch your back
[State -1, Back Stab]
type = ChangeState
triggerall = numhelper(1150) = 0
Triggerall = power >= 1000
TriggerAll = !AiLevel
value = 1100
triggerall = command = "SKILL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Multiple hit
[State -1, Multi hit]
type = ChangeState
triggerall = numhelper(1250) = 0
Triggerall = power >= 1000
TriggerAll = !AiLevel
value = 1200
triggerall = command = "SKILL 3"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Walk Counter
[State -1, Counter]
type = ChangeState
Triggerall = power >= 500
TriggerAll = !AiLevel
value = 1500
triggerall = command = "SKILL 4"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Directional Slash
[State -1, Directional Slash]
type = ChangeState
TriggerAll = !AiLevel
Triggerall = power >= 1500
value = 1005
triggerall = command = "SKILL 5"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Shadow Garden
[State -1, Shadow Garden]
type = ChangeState
TriggerAll = !AiLevel
triggerall = var(3) = 0
triggerall = numhelper(1450) = 0
Triggerall = power >= 1700
value = 1400
triggerall = command = "SKILL 6"
Triggerall = statetype != A
trigger1 = ctrl
;===========================================================================
;---------------------------Normal skills-----------------------------------
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
TriggerAll = !AiLevel
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
TriggerAll = !AiLevel
value = 300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
TriggerAll = !AiLevel
value = 400
triggerall = power >= 500
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
TriggerAll = !AiLevel
Triggerall = power < 3000
value = 500
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Air
[State -1, A Air]
type = ChangeState
TriggerAll = !AiLevel
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Air
[State -1, B Air]
type = ChangeState
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Air
[State -1, C Air]
type = ChangeState
TriggerAll = !AiLevel
Triggerall = power >= 50
value = 620
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; The world 
[State -1, TP]
type = ChangeState
TriggerAll = !AiLevel
TriggerAll = Power >= 500
triggerall = command = "z"
trigger1 = ctrl
value = 1902
IgnoreHitPause = 1