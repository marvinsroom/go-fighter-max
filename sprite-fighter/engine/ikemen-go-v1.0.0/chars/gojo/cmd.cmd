[command]
name = "skill_1"
command = ~D, DF, F, a
time = 50
[command]
name = "skill_2"
command = ~D, DB, B, a
time = 50
[command]
name = "skill_3"
command = ~D, DF, F, b
time = 50
[command]
name = "skill_4"
command = ~D, DB, B, b
time = 50
[command]
name = "skill_5"
command = D,a
time = 50
[command]
name = "skill_6"
command = ~D, DB, B, c
time = 50
[command]
name = "skill_7"
command = ~D, DF, F, c
time = 50
[command]
name = "skill_8"
command = ~z
time = 50
[command]
name = "Muryokusho"
command = ~x
time = 50
[command]
name = "Clash"
command = ~D, x
time = 50
[command]
name = "Unlimited Hollow"
command = ~y
time = 50
[command]
name = "FF"
command = F, F
time = 50
[command]
name = "BB"
command = B, B
time = 50
[command]
name = "recovery"
command = x+y
time = 1
[command]
name = "recovery"
command = y+z
time = 1
[command]
name = "recovery"
command = x+z
time = 1
[command]
name = "recovery"
command = a+b
time = 1
[command]
name = "recovery"
command = b+c
time = 1
[command]
name = "recovery"
command = a+c
time = 1
[command]
name = "back_x"
command = /$B, x
time = 1
[command]
name = "back_y"
command = /$B, y
time = 1
[command]
name = "back_z"
command = /$B, z
time = 1
[command]
name = "down_x"
command = /$D, x
time = 1
[command]
name = "down_y"
command = /$D, y
time = 1
[command]
name = "down_z"
command = /$D, z
time = 1
[command]
name = "fwd_x"
command = /$F, x
time = 1
[command]
name = "fwd_y"
command = /$F, y
time = 1
[command]
name = "fwd_z"
command = /$F, z
time = 1
[command]
name = "up_x"
command = /$U, x
time = 1
[command]
name = "up_y"
command = /$U, y
time = 1
[command]
name = "up_z"
command = /$U, z
time = 1
[command]
name = "back_a"
command = /$B, a
time = 1
[command]
name = "back_b"
command = /$B, b
time = 1
[command]
name = "back_c"
command = /$B, c
time = 1
[command]
name = "down_a"
command = /$D, a
time = 1
[command]
name = "down_b"
command = /$D, b
time = 1
[command]
name = "down_c"
command = /$D, c
time = 1
[command]
name = "fwd_a"
command = /$F, a
time = 1
[command]
name = "fwd_b"
command = /$F, b
time = 1
[command]
name = "fwd_c"
command = /$F, c
time = 1
[command]
name = "up_a"
command = /$U, a
time = 1
[command]
name = "up_b"
command = /$U, b
time = 1
[command]
name = "up_c"
command = /$U, c
time = 1
[command]
name = "a"
command = a
time = 1
[command]
name = "b"
command = b
time = 1
[command]
name = "c"
command = c
time = 1
[command]
name = "x"
command = x
time = 1
[command]
name = "y"
command = y
time = 1
[command]
name = "z"
command = z
time = 1
[command]
name = "s"
command = s
time = 1
[command]
name = "fwd"
command = $F
time = 1
[command]
name = "downfwd"
command = $DF
time = 1
[command]
name = "down"
command = $D
time = 1
[command]
name = "downback"
command = $DB
time = 1
[command]
name = "back"
command = $B
time = 1
[command]
name = "upback"
command = $UB
time = 1
[command]
name = "up"
command = $U
time = 1
[command]
name = "upfwd"
command = $UF
time = 1
[command]
name = "hold_x"
command = /x
time = 1
[command]
name = "hold_y"
command = /y
time = 1
[command]
name = "hold_z"
command = /z
time = 1
[command]
name = "hold_a"
command = /a
time = 1
[command]
name = "hold_b"
command = /b
time = 1
[command]
name = "hold_c"
command = /c
time = 1
[command]
name = "hold_s"
command = /s
time = 1
[command]
name = "holdfwd"
command = /$F
time = 1
[command]
name = "holddownfwd"
command = /$DF
time = 1
[command]
name = "holddown"
command = /$D
time = 1
[command]
name = "holddownback"
command = /$DB
time = 1
[command]
name = "holdback"
command = /$B
time = 1
[command]
name = "holdupback"
command = /$UB
time = 1
[command]
name = "holdup"
command = /$U
time = 1
[command]
name = "holdupfwd"
command = /$UF
time = 1

[statedef -1]

[State 0]
type = ChangeState
triggerall = command = "FF"
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = ifelse(statetype = A,70,60)

[State 0]
type = ChangeState
triggerall = command = "BB"
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = ifelse(statetype = A,75,65)

[State 0]
type = ChangeState
triggerall = command = "s"
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
Triggerall = statetype != A
value = 500

[State 0]
type = ChangeState
;Triggerall = life <= 500
triggerall = command = "skill_2"
triggerall = statetype != A
triggerall = ailevel = 0
triggerall = !NumHelper(1050)
triggerall = power >= 1000
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 1000

[State 0]
type = ChangeState
triggerall = command = "skill_1"
triggerall = ailevel = 0
triggerall = power >= 1000
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1100

[State 0]
type = ChangeState
triggerall = statetype != A
triggerall = command = "skill_3"
triggerall = ailevel = 0
triggerall = power >= 500
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1200

[State 0]
type = ChangeState
triggerall = statetype != A
triggerall = command = "skill_4"
triggerall = ailevel = 0
triggerall = power >= 1000
triggerall = !NumHelper(1360)
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1300

[State 0]
type = ChangeState
triggerall = numhelper(1450) = 0
triggerall = !NumHelper(1410)
triggerall = statetype != A
triggerall = command = "skill_5"
triggerall = ailevel = 0
triggerall = power >= 1000
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1400

[State 0]
type = ChangeState
triggerall = statetype != A
triggerall = command = "skill_7"
triggerall = ailevel = 0
triggerall = power >= 1500
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1500

[State 0]
type = ChangeState
triggerall = statetype != A
triggerall = command = "skill_6"
triggerall = ailevel = 0
triggerall = power >= 1500
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 1600

[State 0]
type = ChangeState
triggerall = command = "skill_8"
triggerall = ailevel = 0
triggerall = power >= 1000
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = ifelse(statetype = A,2001,2000)

[State 0]
type = ChangeState
triggerall = numhelper(1901) = 0
triggerall = numhelper(1050) = 0
triggerall = statetype != A
triggerall = command = "Unlimited Hollow"
triggerall = ailevel = 0
triggerall = power >= 2000
triggerall = helper(30990),fvar(8) = 1
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 3300

[State 0]
type = ChangeState
triggerall = numhelper(1901) = 0
triggerall = numhelper(1050) = 0
triggerall = statetype != A
triggerall = command = "Clash"
triggerall = ailevel = 0
triggerall = power >= 2000
triggerall = helper(30990),fvar(8) = 1
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 3100
[State 0]
type = ChangeState
triggerall = numhelper(1901) = 0
triggerall = numhelper(1050) = 0
triggerall = statetype != A
triggerall = command = "Muryokusho"
triggerall = ailevel = 0
triggerall = power >= 2000
triggerall = helper(30990),fvar(8) = 1
trigger1 = ctrl
trigger2 = stateno = [60,75]
value = 3200

[State 0]
type = ChangeState
triggerall = command = "a"
triggerall = statetype != A
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 200

[State 0]
type = ChangeState
triggerall = numexplod(1840) = 0
triggerall = command = "b" && command = "holddown"
triggerall = statetype != A
triggerall = ailevel = 0
triggerall = power >= 1000 && !numhelper(1801)
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 1800

[State 0]
type = ChangeState
triggerall = command = "b"
triggerall = statetype = A
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 240

[State 0]
type = ChangeState
triggerall = command = "b"
triggerall = statetype != A
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 300

[State 0]
type = ChangeState
triggerall = command = "a"
triggerall = statetype = A
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 600

[State 0]
type = ChangeState
triggerall = command = "c" && command = "holddown"
triggerall = statetype != A
triggerall = ailevel = 0
triggerall = power >= 1000 && !numhelper(1701)
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 1700

[State 0]
type = ChangeState
triggerall = command = "c"
triggerall = statetype != A
triggerall = ailevel = 0
triggerall = power >= 700 && !numhelper(420)
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 400

[State 0]
type = ChangeState
triggerall = command = "c"
triggerall = statetype = A
triggerall = ailevel = 0
trigger1 = ctrl
trigger2 = stateno = [60,65]
value = 620