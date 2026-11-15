[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s

;-| Default Values |-------------------------------------------------------
[Defaults]
command.time = 30
command.buffer.time = 1

;-| Super Motions |--------------------------------------------------------


[command]
name = "SPECIAL 1"
command = ~D,B,a
time = 6


[command]
name = "SPECIAL 7"
command = ~D,B,b
time = 30

[command]
name = "SPECIAL 6"
command = ~D,B,c
time =30

[command]
name = "SPECIAL 12"
command = ~D,F,a
time =30

[command]
name = "SPECIAL 2"
command = ~D,F,b
time =30

[command]
name = "SPECIAL 3"
command = ~D,F,c
time =30


;-| Special Motions |------------------------------------------------------

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
; 2. State entry
; --------------
; This is where you define what commands bring you to what states.
;
; Each state entry block looks like:
;   [State -1, Label]           ;Change Label to any name you want to use to
;                               ;identify the state with.
;   type = ChangeState          ;Don't change this
;   value = new_state_number
;   trigger1 = command = command_name
;   . . .  (any additional triggers)
;
; - new_state_number is the number of the state to change to
; - command_name is the name of the command (from the section above)
; - Useful triggers to know:
;   - statetype
;       S, C or A : current state-type of player (stand, crouch, air)
;   - ctrl
;       0 or 1 : 1 if player has control. Unless "interrupting" another
;                move, you'll want ctrl = 1
;   - stateno
;       number of state player is in - useful for "move interrupts"
;   - movecontact
;       0 or 1 : 1 if player's last attack touched the opponent
;                useful for "move interrupts"
;
; Note: The order of state entry is important.
;   State entry with a certain command must come before another state
;   entry with a command that is the subset of the first.  
;   For example, command "fwd_a" must be listed before "a", and
;   "fwd_ab" should come before both of the others.
;
; For reference on triggers, see CNS documentation.
;
; Just for your information (skip if you're not interested):
; This part is an extension of the CNS. "State -1" is a special state
; that is executed once every game-tick, regardless of what other state
; you are in.


; Don't remove the following line. It's required by the CMD standard.
[Statedef -1]

;===========================================================================
;---------------------------------------------------------------------------

;===========================================================================
;---------------------------------------------------------------------------
; Run Fwd
[State -1, Correr Adelante]
type = ChangeState
triggerall = stateno != 1605
triggerall = stateno != 70
value = 1605
trigger1 = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl



;---------------------------------------------------------------------------
; Run Back
[State -1, Run Back]
type = ChangeState
triggerall = stateno != 1606
triggerall = stateno != 70
value = 1606
trigger1 = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl


;---------------------------------------------------------------------------

[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 1"
trigger1 = statetype !=a
trigger1 = ctrl
; Throw


[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 1000
value = 1050
triggerall = command = "SPECIAL 12"
trigger1 = statetype !=a
trigger1 = ctrl
; Throw

; Time Slowing
[State -1, Time Slowing]
type = ChangeState
triggerall=numhelper(1150)=0
triggerall = var(4) = 0
Triggerall = power >= 1500
value = 11000
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, Susano O perfect]
type = ChangeState
Triggerall = power >= 100
value = 4800
triggerall = command = "holddown"
triggerall = command = "z"
Triggerall = statetype != A
trigger1 = ctrl

[State -1, Susano O perfect]
type = null
triggerall = numhelper(39001) = 0
triggerall = var(6) =0
Triggerall = power >= 2000
value = 39000
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

[State -1, Time Slowing]
type = null
triggerall = var(5) < 5
Triggerall = power >= 1000
value = 630
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, Time Slowing]
type = ChangeState
Triggerall = power >= 1000
value = 13000
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

;---------------------------------------------------------------------------


[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 100
value =660
triggerall = command = "SPECIAL 3"
trigger1 = statetype !=a
trigger1 = ctrl


; Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 200
triggerall = command = "a"
trigger1 = statetype = s
trigger1 = ctrl

[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 100
value = 440
triggerall = command = "z"
trigger1 = statetype !=a
trigger1 = ctrl


[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 3000
value =30000
triggerall = command = "x"
trigger1 = statetype !=a
trigger1 = ctrl

[State -1, Jump Strong Kick]
type = ChangeState
;triggerall = numhelper(4002) < 20
triggerall=var(19)<20
Triggerall = power >= 1000
value = 1100
triggerall = command = "SPECIAL 7"
trigger1 = statetype = s
trigger1 = ctrl




[State -1, Jump Strong Kick]
type = ChangeState
value = 333
triggerall = command = "y"
trigger1 = statetype = s
trigger1 = ctrl


; Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 210
triggerall = command = "a"
trigger1 = statetype = s
trigger1 = ctrl

; Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 240
triggerall = command = "b"
trigger1 = statetype = s
trigger1 = ctrl

[State -1, Jump Strong Kick]
type = ChangeState
Triggerall = power >= 1000
value = 820
triggerall = command = "c"
trigger1 = statetype !=a
trigger1 = ctrl


[State -1, Power Charge]
type = ChangeState
Triggerall = power < 10000
value = 500
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
