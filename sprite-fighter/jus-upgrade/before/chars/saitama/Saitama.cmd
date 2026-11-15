; The CMD file.
;
; Two parts: 1. Command definition and  2. State entry
; (state entry is after the commands def section)
;
; 1. Command definition
; ---------------------
; Note: The commands are CASE-SENSITIVE, and so are the command names.
; The eight directions are:
;   B, DB, D, DF, F, UF, U, UB     (all CAPS)
;   corresponding to back, down-back, down, downforward, etc.
; The six buttons are:
;   a, b, c, x, y, z               (all lower case)
;   In default key config, abc are are the bottom, and xyz are on the
;   top row. For 2 button characters, we recommend you use a and b.
;   For 6 button characters, use abc for kicks and xyz for punches.
;
; Each [Command] section defines a command that you can use for
; state entry, as well as in the CNS file.
; The command section should look like:
;
;   [Command]
;   name = some_name
;   command = the_command
;   time = time (optional)
;   buffer.time = time (optional)
;
; - some_name
;   A name to give that command. You'll use this name to refer to
;   that command in the state entry, as well as the CNS. It is case-
;   sensitive (QCB_a is NOT the same as Qcb_a or QCB_A).
;
; - command
;   list of buttons or directions, separated by commas. Each of these
;   buttons or directions is referred to as a "symbol".
;   Directions and buttons can be preceded by special characters:
;   slash (/) - means the key must be held down
;          egs. command = /D       ;hold the down direction
;               command = /DB, a   ;hold down-back while you press a
;   tilde (~) - to detect key releases
;          egs. command = ~a       ;release the a button
;               command = ~D, F, a ;release down, press fwd, then a
;          If you want to detect "charge moves", you can specify
;          the time the key must be held down for (in game-ticks)
;          egs. command = ~30a     ;hold a for at least 30 ticks, then release
;   dollar ($) - Direction-only: detect as 4-way
;          egs. command = $D       ;will detect if D, DB or DF is held
;               command = $B       ;will detect if B, DB or UB is held
;   plus (+) - Buttons only: simultaneous press
;          egs. command = a+b      ;press a and b at the same time
;               command = x+y+z    ;press x, y and z at the same time
;   greater-than (>) - means there must be no other keys pressed or released
;                      between the previous and the current symbol.
;          egs. command = a, >~a   ;press a and release it without having hit
;                                  ;or released any other keys in between
;   You can combine the symbols:
;     eg. command = ~30$D, a+b     ;hold D, DB or DF for 30 ticks, release,
;                                  ;then press a and b together
;
;   Note: Successive direction symbols are always expanded in a manner similar
;         to this example:
;           command = F, F
;         is expanded when MUGEN reads it, to become equivalent to:
;           command = F, >~F, >F
;
;   It is recommended that for most "motion" commads, eg. quarter-circle-fwd,
;   you start off with a "release direction". This makes the command easier
;   to do.
;
; - time (optional)
;   Time allowed to do the command, given in game-ticks. The default
;   value for this is set in the [Defaults] section below. A typical
;   value is 15.
;
; - buffer.time (optional)
;   Time that the command will be buffered for. If the command is done
;   successfully, then it will be valid for this time. The simplest
;   case is to set this to 1. That means that the command is valid
;   only in the same tick it is performed. With a higher value, such
;   as 3 or 4, you can get a "looser" feel to the command. The result
;   is that combos can become easier to do because you can perform
;   the command early. Attacks just as you regain control (eg. from
;   getting up) also become easier to do. The side effect of this is
;   that the command is continuously asserted, so it will seem as if
;   you had performed the move rapidly in succession during the valid
;   time. To understand this, try setting buffer.time to 30 and hit
;   a fast attack, such as KFM's light punch.
;   The default value for this is set in the [Defaults] section below.
;   This parameter does not affect hold-only commands (eg. /F). It
;   will be assumed to be 1 for those commands.
;
; If you have two or more commands with the same name, all of them will
; work. You can use it to allow multiple motions for the same move.
;
; Some common commands examples are given below.
;
; [Command] ;Quarter circle forward + x
; name = "QCF_x"
; command = ~D, DF, F, x
;
; [Command] ;Half circle back + a
; name = "HCB_a"
; command = ~F, DF, D, DB, B, a
;
; [Command] ;Two quarter circles forward + y
; name = "2QCF_y"
; command = ~D, DF, F, D, DF, F, y
;
; [Command] ;Tap b rapidly
; name = "5b"
; command = b, b, b, b, b
; time = 30
;
; [Command] ;Charge back, then forward + z
; name = "charge_B_F_z"
; command = ~60$B, F, z
; time = 10
;
; [Command] ;Charge down, then up + c
; name = "charge_D_U_c"
; command = ~60$D, U, c
; time = 10


;-| Button Remapping |-----------------------------------------------------
; This section lets you remap the player's buttons (to easily change the
; button configuration). The format is:
;   old_button = new_button
; If new_button is left blank, the button cannot be pressed.
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
; Default value for the "time" parameter of a Command. Minimum 1.
command.time = 15

; Default value for the "buffer.time" parameter of a Command. Minimum 1,
; maximum 30.
command.buffer.time = 1



;-| AI |------------------------------------------------------
[Command]
name = "AI0"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 1
[Command]
name = "AI1"
command = b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b
time = 1
[Command]
name = "AI2"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 1
[Command]
name = "AI3"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 1
[Command]
name = "AI4"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 1
[Command]
name = "AI5"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI6"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time =1
[Command]
name = "AI7"
command = F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F
time = 1
[Command]
name = "AI8"
command = D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D
time = 1
[Command]
name = "AI9"
command = B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B
time = 1
[Command]
name = "AI10"
command = U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U
time = 1
[Command]
name = "AI11"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 1
[Command]
name = "AI12"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 1
[Command]
name = "AI13"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 1
[Command]
name = "AI14"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 1
[Command]
name = "AI15"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI16"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 1
[Command]
name = "AI17"
command = a,B,c,x,y,z,s,B,D,F,U,a,b,c,x,y,z,s,s
time = 1
[Command]
name = "AI18"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 1
[Command]
name = "AI19"
command = b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b
time = 1
[Command]
name = "AI20"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 1
[Command]
name = "AI21"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 1
[Command]
name = "AI22"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 1
[Command]
name = "AI23"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI24"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 1
[Command]
name = "AI25"
command = F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F
time = 1
[Command]
name = "AI26"
command = D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D
time = 1
[Command]
name = "AI27"
command = B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B
time = 1
[Command]
name = "AI28"
command = U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U
time = 1
[Command]
name = "AI29"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 1
[Command]
name = "AI30"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 1
[Command]
name = "AI31"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 1
[Command]
name = "AI32"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 1
[Command]
name = "AI33"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI34"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 1
[Command]
name = "AI35"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI36"
command = z,z,z,z,z,z,a,a,a,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI37"
command = z,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,z,z,z
time = 1
[Command]
name = "AI38"
command = z,z,z,z,z,a,a,a,z,z,z,z,z,a,a,a,z,z,z
time = 1
[Command]
name = "AI39"
command = z,z,z,z,z,a,a,a,z,z,z,z,z,z,a,a,z,z,z
time = 1
[Command]
name = "AI40"
command = z,z,z,z,a,a,a,z,z,z,z,a,z,z,a,a,z,z,z
time = 1
[Command]
name = "AI41"
command = z,z,z,a,z,z,z,z,z,z,z,z,z,a,a,z,z,z,z
time = 1
[Command]
name = "AI42"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI43"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,a,a,z
time = 1
[Command]
name = "AI44"
command = z,z,a,a,a,a,z,z,z,z,z,z,z,z,z,a,a,a,z
time = 1
[Command]
name = "AI45"
command = z,z,z,z,z,z,a,a,z,z,z,z,z,a,a,a,a,z,z
time = 1
[Command]
name = "AI46"
command = z,z,z,z,z,z,z,z,a,a,a,a,a,a,z,z,z,z,z
time = 1
[Command]
name = "AI47"
command = z,z,z,a,a,a,a,z,z,z,z,z,z,z,z,z,z,z,z
time = 1
[Command]
name = "AI48"
command = z,z,z,z,z,a,a,a,z,z,z,a,a,a,z,z,a,z,a
time = 1
[Command]
name = "AI49"
command = z,z,z,z,a,a,a,z,z,z,z,z,a,a,a,z,z,z,z
time = 1
[Command]
name = "AI50"
command = z,z,z,a,a,z,z,z,z,z,z,z,z,z,a,a,z,z,z
time = 1

;-| Super Motions |--------------------------------------------------------
;The following two have the same name, but different motion.
;Either one will be detected by a "command = TripleKFPalm" trigger.
;Time is set to 20 (instead of default of 15) to make the move
;easier to do.
;
[Command]
name = "Death Punch"
command = ~D, DF, F, x
time = 20

[Command]
name = "Two-Handed Consecutive Punches"
command = ~D, DF, F, y
time = 20

[Command]
name = "Serious Punch"
command = ~D, DF, F, z
time = 20

[Command]
name = "Serious Table Flip"
command = ~D, DF, F, a
time = 20

[Command]
name = "Serious Headbutt"
command = ~D, DF, F, b
time = 20

[Command]
name = "Serious Sidehops"
command = ~D, DF, F, c
time = 20

[Command]
name = "Serious Sidehops 2"
command = ~D, DB, B, c
time = 20

[Command]
name = "Meteor Punch"
command = ~D, DB, B, z
time = 20

[Command]
name = "Checkmate"
command = ~D, DB, B, y
time = 20

[Command]
name = "Punch Rain"
command = ~D, DB, B, b
time = 20

[Command]
name = "Saturday Sale Uppercut"
command = ~D, DB, B, x
time = 20

[Command]
name = "Whirling Butt Attack"
command = ~D, DB, B, a
time = 20

;-| Special Motions |------------------------------------------------------

[Command]
name = "Genos"
command = B, z
time = 20

[Command]
name = "Tatsumaki"
command = B, c
time = 20

[Command]
name = "King"
command = B, y
time = 20

[Command]
name = "Silver Fang"
command = B, b
time = 20

[Command]
name = "Teleport Forward Short"
command = ~D, D, x
time = 20

[Command]
name = "Teleport Forward"
command = ~D, D, y
time = 20

[Command]
name = "Teleport Back Short"
command = ~D, D, a
time = 20

[Command]
name = "Teleport Back"
command = ~D, D, b
time = 20

[Command]
name = "SuperJumpUp"
command = D, U

[Command]
name = "SuperJumpFwd"
command = D, UF

[Command]
name = "SuperJumpBck"
command = D, UB

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

[Command]
name = "hold_a"
command = /$a
time = 1

[Command]
name = "hold_b"
command = /$b
time = 1

[Command]
name = "hold_c"
command = /$c
time = 1

[Command]
name = "hold_x"
command = /$x
time = 1

[Command]
name = "hold_y"
command = /$y
time = 1

[Command]
name = "hold_z"
command = /$z
time = 1

[Command]
name = "hold_start"
command = /$s
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

[State -1]
type = VarSet
triggerall = var(59) = 0
triggerall = roundstate = [1,2]
trigger1 = AIlevel > 0
var(59) = 1
ignorehitpause = 1
;===========================================================================
;---------------------------------------------------------------------------
;Death Punch
[State -1, Death Punch]
type = ChangeState
value = 1000
triggerall = command = "Death Punch"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Two-Handed Consecutive Punches
[State -1, Two-Handed Consecutive Punches]
type = ChangeState
value = 1100
triggerall = command = "Two-Handed Consecutive Punches"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Two-Handed Consecutive Punches
[State -1, Two-Handed Consecutive Punches]
type = ChangeState
value = 1110
triggerall = command = "Two-Handed Consecutive Punches"
triggerall = power >= 1000
trigger1 = statetype = A
trigger1 = ctrl

;Serious Table Flip
[State -1, Serious Table Flip]
type = ChangeState
value = 1200
triggerall = command = "Serious Table Flip"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Serious Headbutt
[State -1, Serious Headbutt]
type = ChangeState
value = 1300
triggerall = command = "Serious Headbutt"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Serious Sidehops
[State -1, Serious Sidehops]
type = ChangeState
value = 1400
triggerall = command = "Serious Sidehops"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Serious Sidehops 2
[State -1, Serious Sidehops 2]
type = ChangeState
value = 1410
triggerall = command = "Serious Sidehops 2"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Serious Punch
[State -1, Serious Punch]
type = ChangeState
value = 1500
triggerall = command = "Serious Punch"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Meteor Punch
[State -1, Meteor Punch]
type = ChangeState
value = 1700
triggerall = command = "Meteor Punch"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Checkmate
[State -1, Checkmate]
type = ChangeState
value = 1800
triggerall = command = "Checkmate"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Punch Rain
[State -1, Punch Rain]
type = ChangeState
value = 1900
triggerall = command = "Punch Rain"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Saturday Sale Uppercut
[State -1, Saturday Sale Uppercut]
type = ChangeState
value = 2000
triggerall = command = "Saturday Sale Uppercut"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;Whirling Butt Attack
[State -1, Whirling Butt Attack]
type = ChangeState
value = 2005
triggerall = command = "Whirling Butt Attack"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
;Teleport Forward
[State -1, Teleport Forward]
type = ChangeState
value = 1600
triggerall = command = "Teleport Forward"
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Teleport Forward Short
[State -1, Teleport Forward Short]
type = ChangeState
value = 1605
triggerall = command = "Teleport Forward Short"
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Teleport Back
[State -1, Teleport Back]
type = ChangeState
value = 1610
triggerall = command = "Teleport Back"
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Teleport Back Short
[State -1, Teleport Back Short]
type = ChangeState
value = 1615
triggerall = command = "Teleport Back Short"
trigger1 = statetype != A
trigger1 = ctrl
;===========================================================================
;This is not a move, but it sets up var(1) to be 1 if conditions are right
;for a combo into a special move (used below).
;Since a lot of special moves rely on the same conditions, this reduces
;redundant logic.
[State -1, Combo condition Reset]
type = VarSet
trigger1 = 1
var(1) = 0

[State -1, Combo condition Check]
type = VarSet
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = (stateno = [200,299]) || (stateno = [400,499])
trigger2 = stateno != 440 ;Except for sweep kick
trigger2 = movecontact
var(1) = 1

;===========================================================================
;---------------------------------------------------------------------------
;Run Fwd
[State -1, Run Fwd]
type = ChangeState
value = 100
trigger1 = command = "FF"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
;Hop Back
[State -1, Hop Back]
type = ChangeState
value = 105
trigger1 = command = "BB"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
;Throw
[State -1, Throw]
type = ChangeState
value = 800
triggerall = command = "y" || command = "b"
triggerall = statetype = S
triggerall = ctrl
triggerall = stateno != 100
trigger1 = command = "holdfwd"
trigger1 = p2bodydist X < 12
trigger1 = (p2statetype = S) || (p2statetype = C)
trigger1 = p2movetype != H
trigger2 = command = "holdback"
trigger2 = p2bodydist X < 12
trigger2 = (p2statetype = S) || (p2statetype = C)
trigger2 = p2movetype != H

;===========================================================================
;Genos
[State -1, Genos]
type = ChangeState
value = 300
triggerall = command = "Genos"
triggerall = numhelper(351) = 0
trigger1 = statetype = S
trigger1 = ctrl

;===========================================================================
;Tatsumaki
[State -1, Tatsumaki]
type = ChangeState
value = 301
triggerall = command = "Tatsumaki"
triggerall = numhelper(806) = 0
trigger1 = statetype = S
trigger1 = ctrl

;===========================================================================
;King
[State -1, King]
type = ChangeState
value = 302
triggerall = command = "King"
triggerall = numhelper(303) = 0
triggerall = numhelper(305) = 0
trigger1 = statetype = S
trigger1 = ctrl

;===========================================================================
;Silver Fang
[State -1, Silver Fang]
type = ChangeState
value = 309
triggerall = command = "Silver Fang"
triggerall = numhelper(310) = 0
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
;Normal Punch
[State -1, Normal Punch]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;One Inch Punch
[State -1, One Inch Punch]
type = ChangeState
value = 205
triggerall = command = "x"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;Mosquito Slap
[State -1, Double Punch]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = command != "holddown"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;Uppercut
[State -1, Double Punch]
type = ChangeState
value = 220
triggerall = command = "z"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = 230
triggerall = command = "a"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5

;---------------------------------------------------------------------------
;Uppercut
[State -1, Standing Medium Kick]
type = ChangeState
value = 220
triggerall = command = "z"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;Drill Punch
[State -1, Drill Punch]
type = ChangeState
value = 250
triggerall = command = "c"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;Standing Medium Kick
[State -1, Standing Strong Kick]
type = ChangeState
value = 260
triggerall = command = "b"
triggerall = command != "holddown"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13


;---------------------------------------------------------------------------
;Launch Kick
[State -1, Launch Kick]
type = ChangeState
value = 270
triggerall = command = "c"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13

;---------------------------------------------------------------------------
;Air Chop
[State -1, Air Chop]
type = ChangeState
value = 280
triggerall = command = "y"
triggerall = command = "holddown"
trigger1 = statetype != S
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13
trigger4 = (stateno = 270) && time > 8

;---------------------------------------------------------------------------
;Moon Crash
[State -1, Moon Crash]
type = ChangeState
value = 600
triggerall = command = "x"
triggerall = command = "holddown"
triggerall = pos y <= -50
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Elbow on Hammerhead
[State -1, Elbow]
type = ChangeState
value = 290
triggerall = command = "b"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = (stateno = 200) && time > 5
trigger3 = (stateno = 230) && time > 13
;---------------------------------------------------------------------------

;Guard Cancel
[State -1, Guard Cancel]
type = Null;ChangeState
value = 299
triggerall = command = "b"
triggerall = power >= 200
triggerall = statetype != A
trigger1 = stateno = 150 || stateno = 151 || stateno = 152
trigger2 = stateno = 140 || stateno = 141 || stateno = 142
trigger3 = stateno = 130 || stateno = 131 || stateno = 132
trigger4 = stateno = 120 || stateno = 121 || stateno = 122

;---------------------------------------------------------------------------
;Taunt
[State -1, Taunt]
type = ChangeState
value = 196
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl


;---------------------------------------------------------------------------
;Jump Light Punch
[State -1, Jump Light Punch]
type = ChangeState
value = 610
triggerall = command = "x"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Jump Strong Punch
[State -1, Jump Strong Punch]
type = ChangeState
value = 610
triggerall = command = "y"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Jump Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 630
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
;Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 630
triggerall = command = "b"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Superjump Up
[State -1, Superjump Up]
type = ChangeState
value = 690
trigger1 = command = "SuperJumpUp"
trigger1 = statetype = S || statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Superjump Fwd
[State -1, Superjump Fwd]
type = ChangeState
value = 700
trigger1 = command = "SuperJumpFwd"
trigger1 = statetype = S || statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Superjump Back
[State -1, Superjump Back]
type = ChangeState
value = 710
trigger1 = command = "SuperJumpBck"
trigger1 = statetype = S || statetype = C
trigger1 = ctrl
