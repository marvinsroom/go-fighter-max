[Defaults]
command.time = 1
command.buffer.time = 1
[Command]
name = "holdfwd"
command = /$F
time = 1
[Command]
name = "holdback"
command = /$B
time = 1
[Statedef -1]
[State -1, Walk forward]
type = ChangeState
triggerall = roundstate = 2
triggerall = stateno = 0
trigger1 = command = "holdfwd"
value = 20
ctrl = 0
[State -1, Walk backward]
type = ChangeState
triggerall = roundstate = 2
triggerall = stateno = 0
trigger1 = command = "holdback"
value = 21
ctrl = 0
