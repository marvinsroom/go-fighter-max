;---------------------------------------------------------------------------
[command]
name = "adelante"
command = F
time = 1
[command]
name = "atras"
command = B
time = 1
[command]
name = "arriba"
command = U
time = 1
[command]
name = "abajo"
command = D
time = 1
[command]
name = "SPECIAL 7"
command = ~B,DB,D,DF,F,a
time = 30
[Command]
name = "Da"     ;Required (do not remove)
command = D,a
time = 20

[Command]
name = "DFa"     ;Required (do not remove)
command = ~D,DF,F,a
time = 15

[Command]
name = "DBa"     ;Required (do not remove)
command = ~D,DB,B,a
time = 15
[Command]
name = "Db"     ;Required (do not remove)
command = D,b
time = 20

[Command]
name = "DFb"     ;Required (do not remove)
command = ~D,DF,F,b
time =15

[Command]
name = "DBb"     ;Required (do not remove)
command = ~D,DB,B,b
time = 15

[Command]
name = "Dc"     ;Required (do not remove)
command = D,c
time = 20

[Command]
name = "DFc"     ;Required (do not remove)
command = ~D,DF,F,c
time = 15

[Command]
name = "DBc"     ;Required (do not remove)
command = ~D,DB,B,a
time = 15

[Command]
name = "Dx"     ;Required (do not remove)
command = D,x
time = 20

[Command]
name = "DFx"     ;Required (do not remove)
command = D,F,x
time = 20

[Command]
name = "DBx"     ;Required (do not remove)
command = D,B,x
time = 20

[Command]
name = "Dy"     ;Required (do not remove)
command = D,y
time = 20

[Command]
name = "DFy"     ;Required (do not remove)
command = D,F,y
time = 20

[Command]
name = "DBy"     ;Required (do not remove)
command = D,B,y
time = 20



[command]
name = "b+a"
command = a+b
time = 1

[command]
name = "b+c"
command = /$b,/$c
time = 1
[command]
name = "a+c"
command = a+c
time = 1

[command]
name = "S+a"
command = /$a,/$s
time = 1

[Command]
name = "S+b"     ;Required (do not remove)
command = /$b,/$s
time = 1


[command]
name = "DA"
command = /$B+a
time = 1

[Command]
name = "hold_a"
command = /a
time = 1

[Command]
name = "hold_c"
command = /c
time = 1
;---------------------------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10

[Command]
name = "recovery";Required (do not remove)
command = x+y
time = 1
;---------------------------------------------------------------------------
[Command]
name = "a"
command = a
time = 3

[Command]
name = "b"
command = b
time = 2

[Command]
name = "c"
command = c
time = 2

[Command]
name = "x"
command = x
time = 2

[Command]
name = "y"
command = y
time = 2

[Command]
name = "z"
command = z
time = 2

[Command]
name = "start"
command = s
time = 1





;---------------------------------------------------------------------------
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
name = "holds";Required (do not remove)
command = /$s
time = 1
[command]
name = "Ds"
command = D,s
time = 20
; Don't remove the following line. It's required by the CMD standard.
[Statedef -1]
;---------------------------------
[State -1,MASTER CONTROL]
type = ChangeState
triggerall = var(33) = 0
triggerall = var(53) = 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
Triggerall = power >= 3000
value = 9111
triggerall = command = "SPECIAL 7"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
;---------------------------------------------------
;--------------------------------------------------
[State -1,GOLPE 1 BEN]
type = ChangeState
value =200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 BEN]
type = ChangeState
value = 300
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 BEN]
type = ChangeState
value =400
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------
[State -1,MASTER CONTROL]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
Triggerall = power >= 3000
value = 9111
triggerall = command = "SPECIAL 7"
Triggerall = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 BESTIA]
type = ChangeState
value =1020
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 BESTIA]
type = ChangeState
value = 1030
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 BESTIA]
type = ChangeState
value = 1040
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,MORDIZCO BESTIA]
type = ChangeState
value = 1000
trigger1 = POWER >= 2000
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,INSTINTO  BESTIA]
type = ChangeState
value = 1100
TRIGGERALL = FVAR(4)= 0
trigger1 = POWER >= 1000
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,RUGIDO BESTIA]
type = ChangeState
value = 1200
trigger1 = POWER >= 1500
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 BESTIA SUPREMO]
type = ChangeState
value =110020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 BESTIA SUPREMO]
type = ChangeState
value = 110030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 BESTIA SUPREMO]
type = ChangeState
value = 110040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,RODAR BESTIA SUPREMO]
type = ChangeState
value = 110110
trigger1 = POWER >= 800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,MORDIZCO BESTIA SUPREMO]
type = ChangeState
value = 110200
trigger1 = POWER >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,RUGIDO BESTIA SUPREMO]
type = ChangeState
value = 110300
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, INSTINTO BESTIA SUPREMO]
type = ChangeState
value = 1100
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = Fvar(4) = 0
triggerall =  var(10) = 1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0
triggerall = var(50) = 0
triggerall = power >=1000
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 CANONBALL]
type = ChangeState
value =2020
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 CANONBALL]
type = ChangeState
value = 2030
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 CANONBALL]
type = ChangeState
value = 2040
triggerall = var(2) =0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL DASH]
type = ChangeState
value = 2000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL CAÑON]
type = ChangeState
value = 2100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL DIAMANTE]
type = ChangeState
value = 2200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 CANONBALL SUPREMO]
type = ChangeState
value =22020
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 CANONBALL SUPREMO]
type = ChangeState
value = 22030
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 CANONBALL SUPREMO]
type = ChangeState
value = 22040
triggerall = var(2) =0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL APLASTE RODANTE]
type = ChangeState
value = 22000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL ESPINAS DE HIERRO]
type = ChangeState
value = 22100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CANONBALL RUEDA ESPINOSA]
type = ChangeState
value = 22200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 CUATROBRAZOS]
type = ChangeState
value =3020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 CUATROBRAZOS]
type = ChangeState
value = 3030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 CUATROBRAZOS]
type = ChangeState
value = 3040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,CUATROBRAZOS AGARRE]
type = ChangeState
value = 3000
trigger1 = POWER >= 800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CUATROBRAZOS PUÑOS]
type = ChangeState
value = 3100
trigger1 = POWER >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,CUATROBRAZOS LANZA ROCA]
type = ChangeState
value = 3200
trigger1 = POWER >= 2400
triggerall = numhelper(3250) =0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 DIAMANTE]
type = ChangeState
value =4020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 DIAMANTE]
type = ChangeState
value = 4030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 DIAMANTE]
type = ChangeState
value = 4040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,DIAMANTE DISPARO]
type = ChangeState
value = 4000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,DIAMANTE PICOS DE DIAMANTE]
type = ChangeState
value = 4100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,DIAMANTE ROCA DE FUEGO]
type = ChangeState
value = 4200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ESCUDO DE DIAMANTE]
type = ChangeState
value = 4900
trigger1 = POWER >= 1200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 FUEGO]
type = ChangeState
value =6020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 FUEGO]
type = ChangeState
value = 6030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 FUEGO]
type = ChangeState
value = 6040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,FUEGO FLAMA DE FUEGO]
type = ChangeState
value =6100
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FUEGO ONDA DE FUEG0]
type = ChangeState
value = 6000
trigger1 = POWER >= 1900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FUEGO OLA DE FUEGO]
type = ChangeState
value = 6200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
[State -1, FUEGO VOLAR]
type = ChangeState
value = 62000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 1 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=0
triggerall = command = "c"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,FUEGO SUPER NOVA]
type = ChangeState
value = 6300
triggerall = life < lifemax/4
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 1 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=3000
triggerall = var(53) >=500
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 BEN LOBO]
type = ChangeState
value =7020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) =1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 BEN LOBO]
type = ChangeState
value = 7030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 BEN LOBO]
type = ChangeState
value = 7040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,BEN LOBO GARRAZO]
type = ChangeState
value =7000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,BEN LOBO AGARRE]
type = ChangeState
value = 7100
trigger1 = POWER >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,BEN LOBO AULLIDO ULTRASONICO]
type = ChangeState
value = 7200
trigger1 = POWER >= 2400
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 MULTIOJOS]
type = ChangeState
value =8020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 MULTIOJOS]
type = ChangeState
value =8030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 MULTIOJOS]
type = ChangeState
value = 8040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,MULTIOJOS MULTIRAFAGAS]
type = ChangeState
value =8000
trigger1 = POWER >= 1200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,MULTIOJOS RAFAGA GRANDE]
type = ChangeState
value = 8100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,MULTIOJOS SUPER RAYO]
type = ChangeState
value = 8200
trigger1 = POWER >= 2600
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 HUMUNGOSARIO]
type = ChangeState
value =9020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 HUMUNGOSARIO]
type = ChangeState
value =9030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 HUMUNGOSARIO]
type = ChangeState
value = 9040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO PUÑO DESTRUCTIVO]
type = ChangeState
value =9000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO ROCA GIGANTE]
type = ChangeState
value = 9100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO MANO DE FUEGO ]
type = ChangeState
value = 9200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 HUMUNGOSARIO SUPREMO]
type = ChangeState
value =9520
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 HUMUNGOSARIO SUPREMO]
type = ChangeState
value =9530
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 HUMUNGOSARIO SUPREMO]
type = ChangeState
value = 9540
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 HUMUNGOSARIO GUARD]
type = ChangeState
value = 9254
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "holdback"
trigger1 = statetype != a  &&  P2MOVEtype = A |numproj>=1
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO SUPREMO AGARRE]
type = ChangeState
value =9700
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO SUPREMO BOMBARDEO DE MISILES]
type = ChangeState
value = 9720
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,HUMUNGOSARIO SUPREMO TERREMOTO]
type = ChangeState
value = 9730
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl

--------------------------------------------------
[State -1,GOLPE 1 ECO ECO]
type = ChangeState
value =13020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0  && var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 ECO ECO]
type = ChangeState
value =13030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 ECO ECO]
type = ChangeState
value = 13040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO SUPER ECO ECO]
type = ChangeState
value =13000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO MULTIECOS ]
type = ChangeState
value =13100
trigger1 = POWER >= 1600
triggerall = numhelper(15000) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO CAMARA ULTRASONICA]
type = ChangeState
value =13200
trigger1 = POWER >= 2200
triggerall = numhelper(13201) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 ECO ECO SUPREMO]
type = ChangeState
value =133020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0  && var(11) =2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 ECO ECO SUPREMO]
type = ChangeState
value =133030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 ECO ECO SUPREMO]
type = ChangeState
value = 133040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) =2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO SUPER ECO ECO SUPREMO]
type = ChangeState
value =133200
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO MULTIECOS SUPREMO]
type = ChangeState
value =133000
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ECO ECO CAMARA ULTRASONICA SUPREMO]
type = ChangeState
value =133100
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ECO ECO SUPREMO DISCO 1]
type = ChangeState
value = 133900
triggerall = numhelper(133950) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ECO ECO SUPREMO DISCO 2]
type = ChangeState
value = 133901
triggerall = numhelper(133951) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ECO ECO SUPREMO DISCO 3]
type = ChangeState
value = 133902
triggerall = numhelper(133952) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ECO ECO SUPREMO DISCO 4]
type = ChangeState
value = 133903
triggerall = numhelper(133953) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
 --------------------------------------------------
[State -1,GOLPE 1 ULTRA-T]
type = ChangeState
value =14020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12)=1
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 ULTRA-T]
type = ChangeState
value =14030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12)=1
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 ULTRA-T]
type = ChangeState
value = 14040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,ULTRA-T MULTIRAFAGAS]
type = ChangeState
value =14000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ULTRA-T RAFAGA GRANDE]
type = ChangeState
value = 14100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ULTRA-T SUPER RAYO]
type = ChangeState
value = 14200
trigger1 = POWER >= 2600
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 RATH]
type = ChangeState
value =150020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 RATH]
type = ChangeState
value = 150030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 RATH]
type = ChangeState
value = 150040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,ATAQUE AEREO RATH]
type = ChangeState
value = 150000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,TACLEADA RATH]
type = ChangeState
value = 150100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GARRAZOS RATH]
type = ChangeState
value = 150200
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 XLR8]
type = ChangeState
value =160020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 XLR8]
type = ChangeState
value = 160030
triggerall = stateno !=160030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 XLR8]
type = ChangeState
value = 160040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,ATAQUE AEREO XLR8]
type = ChangeState
value = 160000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,TACLEADA XLR8]
type = ChangeState
value = 160100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GARRAZOS XLR8]
type = ChangeState
value = 160200
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 WILDVINE]
type = ChangeState
value =170020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 WILDVINE]
type = ChangeState
value = 170030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 WILDVINE]
type = ChangeState
value = 170040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,BOMBAS WILDVINE]
type = ChangeState
value = 170000
TRIGGERALL = NUMHELPER(170050) <=10
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GIRO WILDVINE]
type = ChangeState
value = 170100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,PUAS DEL SUELO WILDVINE]
type = ChangeState
value = 170200
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) =1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 ARTICGUANA]
type = ChangeState
value =180020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 ARTICGUANA]
type = ChangeState
value = 180030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 ARTICGUANA]
type = ChangeState
value = 180040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,VIENTO CONGELANTE ARTICGUANA]
type = ChangeState
value = 180000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,COLUMNAS DE HIELO ARTICGUANA]
type = ChangeState
value = 180100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ESFERAS DE CONGELANTES ARTICGUANA]
type = ChangeState
value = 180200
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,COMBO AEREO ARTICGUANA]
type = ChangeState
value = 180010
triggerall = var(16) = 1
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,COLGARSE WILDVINE]
type = ChangeState
value =170900
trigger1 = POWER >= 100
triggerall = var(15) = 1
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 FEEDBACK]
type = ChangeState
value =316020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 FEEDBACK]
type = ChangeState
value = 316030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 FEEDBACK]
type = ChangeState
value = 316040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1, AGARRE FEEDBACK]
type = ChangeState
value = 316000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,AURA DE CHOQUE FEEDBACK]
type = ChangeState
value = 316100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,SUPER VOLTAJE FEEDBACK]
type = ChangeState
value = 316200
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 FANTASMATICO]
type = ChangeState
value =326020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 FANTASMATICO]
type = ChangeState
value = 326030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 FANTASMATICO]
type = ChangeState
value = 326040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1, FANTASMATICO INTANGIBLE]
type = ChangeState
value = 320000
triggerall = Fvar(18) = 0
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FANTASMATICO SUSTO]
type = ChangeState
value = 321000
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FANTASMATICO TENTACULOS EN EL SUELO]
type = ChangeState
value = 322000

trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 FANTASMATICO]
type = ChangeState
value =336020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 FANTASMATICO]
type = ChangeState
value = 336030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 FANTASMATICO]
type = ChangeState
value = 336040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1&&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1, FANTASMATICO INTANGIBLE]
type = ChangeState
value = 331000
triggerall = Fvar(18) = 0
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FANTASMATICO SUSTO]
type = ChangeState
value = 332000
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0&& var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,FANTASMATICO TENTACULOS EN EL SUELO]
type = ChangeState
value = 333000
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 ALIEN X]
type = ChangeState
value =190019
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 ALIEN X]
type = ChangeState
value = 190000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "b"
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 ALIEN X]
type = ChangeState
value = 1760
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "c"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,ALIEN X MANO GIGANTE]
type = ChangeState
value = 191000
triggerall = var(40) = 0
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ALIEN X CUCHILLAS]
type = ChangeState
value = 192000
triggerall = var(40) = 0
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ALIEN X RAYOS CELESTIAL]
type = ChangeState
value = 193000
triggerall = var(40) = 0
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ALIEN X ESPACIO ONDA DE ARIRE]
type = ChangeState
value = 1900000
triggerall = var(40) = 1
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Da"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ALIEN X ESPACIO METEORIOS]
type = ChangeState
value = 1910000
triggerall = var(40) = 1
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Db"
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,ALIEN X ESPACIO AGUJERO NEGRO]
type = ChangeState
value = 1920000
triggerall = var(40) = 1
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "Dc"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,MUNDOS ]
type = ChangeState
value = 190100
trigger1 = POWER >= 0
triggerall = var(40) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) =0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,COMBO AERE0 1]
type = ChangeState
value = 1010
triggerall = var(18) = 0
triggerall = var(16) = 0
triggerall = var(50) = 0
triggerall = var(19) = 0
triggerall = var(22) = 0
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,VOLAR FANTASMATICO]
type = ChangeState
value =323000
triggerall = var(18) = 1 |var(19) = 1
triggerall = var(16) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,FF]
type = ChangeState
value = 60
triggerall = var(14) = 1
triggerall = var(50) = 0
triggerall = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,BB]
type = ChangeState
value = 70
triggerall = var(14) = 1
triggerall = var(50) = 0
triggerall = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,FF]
type = ChangeState
value = 31660
triggerall = var(17) = 1
triggerall = var(50) = 0
triggerall = command = "FF"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,BB]
type = ChangeState
value = 31670
triggerall = var(17) = 1
triggerall = var(50) = 0
triggerall = command = "BB"
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,FF]
type = ChangeState
value = 100
triggerall = var(14) = 0
triggerall = var(17) = 0
triggerall = var(8) != 2
triggerall = var(50) = 0
triggerall = command = "FF"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,BB]
type = ChangeState
value = 105
triggerall = var(14) = 0
triggerall = var(17) = 0
triggerall = var(50) = 0
triggerall = command = "BB"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,AFF]
type = ChangeState
value = 6005
triggerall = var(14) = 0
triggerall = var(50) = 0
triggerall = command = "FF"
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ABB]
type = ChangeState
value = 6006
triggerall = var(14) = 0
triggerall = var(50) = 0
triggerall = command = "BB"
trigger1 = statetype = A
trigger1 = ctrl
trigger1 = ctrl


;---------------------------------------------------------------------------
[State -1,ACTIVAR OMONITRIX]
type = ChangeState
value = 10000
trigger1 = POWER >= 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, HUMUNGOSARIO SUPREMO]
type = ChangeState
value = 9800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=2000
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, BESTIA SUPREMO]
type = ChangeState
value = 1001
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=1000
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, CANONBALL SUPREMO]
type = ChangeState
value = 2001
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = power >=1000
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ECO ECO SUPREMO]
type = ChangeState
value = 13001
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = power >=500
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,FANTASMATICO COMPLETO]
type = ChangeState
value = 330000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = power >=500
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
[State -1,FANTASMATICO COMPLETO INTAGIBILIDAD]
type = ChangeState
value = 320000
triggerall = Fvar(18) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = power >=500
triggerall = command = "holddown"
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, ALIENIGENAS RANDOM]
type = ChangeState
value = 9900
triggerall = var(56) = 1
triggerall = var(8) != 2
triggerall = var(3) != 2
triggerall = var(11) != 2
triggerall = var(9) != 2
triggerall = var(10) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = var(18) = 0
triggerall = var(19) = 0
triggerall = var(20) = 0
triggerall = var(21) = 0
triggerall = power >= 0
triggerall = command = "x"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1, ALIENIGENAS RANDOM]
type = ChangeState
value = 9902
triggerall = var(56) = 1
triggerall = var(8) != 2
triggerall = var(3) != 2
triggerall = var(11) != 2
triggerall = var(9) != 2
triggerall = var(2) = 0
triggerall = var(10) = 0
triggerall = var(50) = 0
triggerall = var(22) = 0
triggerall = var(20) = 0
triggerall = var(21) = 0
triggerall = power >= 0
triggerall = command = "y"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,CARGA]
type = ChangeState
value = 6010
triggerall = power < 3000
triggerall = var(50) = 0
triggerall = command = "holds"
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA GOLPE 1 BEN]
type = ChangeState
value =200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
trigger1 = random <=500
trigger1 = p2dist x < 50
--------------------------------------------------
[State -1,IA GOLPE 2 BEN]
type = ChangeState
value = 300
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
trigger1 = random <=10
trigger1 = p2dist x >= 30
--------------------------------------------------
[State -1,IA GOLPE 3 BEN]
type = ChangeState
value =400
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 =  statetype = s
trigger1 = ctrl
trigger1 = random <=500
trigger1 = p2dist x < 50
--------------------------------------------------
[State -1,IA master control]
type = ChangeState
value =9111
triggerall = var(53) = 1000
triggerall = power >= 3000
triggerall = var(33) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 =  statetype = s
trigger1 = ctrl
trigger1 = random <=500

--------------------------------------------------
[State -1,IA GOLPE 1 BESTIA]
type = ChangeState
value =1020
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
trigger1 = random <=900
trigger1 = p2dist x < 50
--------------------------------------------------
[State -1,IA GOLPE 2 BESTIA]
type = ChangeState
value = 1030
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 BESTIA]
type = ChangeState
value = 1040
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 60
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA RUGIDO BESTIA]
type = ChangeState
value = 1000
triggerall = power >= 2000
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA APLASTAR BESTIA]
type = ChangeState
value = 1100
triggerall = power >= 1500
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GARRAZO BESTIA]
type = ChangeState
value = 1200
triggerall = power >= 1000
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 BESTIA SUPREMO]
type = ChangeState
value =110020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 BESTIA SUPREMO]
type = ChangeState
value = 110030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 BESTIA SUPREMO]
type = ChangeState
value = 110040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA APLASTAR BESTIA SUPREMO]
type = ChangeState
value = 110110
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) =1
trigger1 = random <=100
trigger1 = p2dist x >70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA MORDIZCO BESTIA SUPREMO]
type = ChangeState
value = 110200
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 30
trigger1 = p2dist x < 200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA RUGIDO BESTIA SUPREMO]
type = ChangeState
value = 110300
trigger1 = POWER >= 2300
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 1
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA INSTINTO BESTIA SUPREMO]
type = ChangeState
value = 1100
triggerall = Fvar(4) = 0
triggerall = var(10) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0
triggerall = var(50) = 1
triggerall = power = 1000
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 CANONBALL]
type = ChangeState
value =2020
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 CANONBALL]
type = ChangeState
value = 2030
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 CANONBALL]
type = ChangeState
value = 2040
triggerall = var(2) =0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL DASH]
type = ChangeState
value = 2000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL CAÑON]
type = ChangeState
value = 2100
triggerall = power >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=300
trigger1 = p2dist x > 30
trigger1 = p2dist x <200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL DIAMANTE]
type = ChangeState
value = 2200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1, IA GOLPE 1 CANONBALL SUPREMO]
type = ChangeState
value =22020
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 CANONBALL SUPREMO]
type = ChangeState
value = 22030
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 CANONBALL SUPREMO]
type = ChangeState
value = 22040
triggerall = var(2) =0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL APLASTE RODANTE]
type = ChangeState
value = 22000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL ESPINAS DE HIERRO]
type = ChangeState
value = 22100
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=800
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CANONBALL RUEDA ESPINOSA]
type = ChangeState
value = 22200
trigger1 = POWER >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 2
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=999
trigger1 = p2dist x > 50
trigger1 = p2dist x < 200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 CUATROBRAZOS]
type = ChangeState
value =3020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 CUATROBRAZOS]
type = ChangeState
value = 3030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 CUATROBRAZOS]
type = ChangeState
value = 3040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <60
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CUATROBRAZOS AGARRE]
type = ChangeState
value = 3000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CUATROBRAZOS PUÑOS]
type = ChangeState
value = 3100
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA CUATROBRAZOS PUÑOS]
type = ChangeState
value = 3200
triggerall = power >= 2500
triggerall = numhelper(3250) =0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =1
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 DIAMANTE]
type = ChangeState
value =4020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 DIAMANTE]
type = ChangeState
value = 4030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 40
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 DIAMANTE]
type = ChangeState
value = 4040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA DIAMANTE AGARRE]
type = ChangeState
value = 4000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA DIAMANTE  PUÑOS]
type = ChangeState
value = 4100
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA DIAMANTE PUÑOS]
type = ChangeState
value = 4200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA ESCUDO DE DIAMANTE]
type = ChangeState
value = 4900
trigger1 = POWER >= 1200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 1
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1= enemy,movetype = a
trigger1 = p2dist x <50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 FUEGO]
type = ChangeState
value =6020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = (random%100) < 10
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 FUEGO]
type = ChangeState
value = 6030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 FUEGO]
type = ChangeState
value = 6040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = random <=5
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FUEGO AGARRE]
type = ChangeState
value =6100
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 30
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FUEGO  PUÑOS]
type = ChangeState
value = 6000
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 30
trigger1 = p2dist x < 100
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FUEGO PUÑOS]
type = ChangeState
value = 6200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall = var(9) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 30
trigger1 = p2dist x < 100
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
[State -1,IA FUEGO SUPER NOVA]
type = ChangeState
value = 6300
triggerall = life < lifemax/4
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 1 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >=3000
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 BEN LOBO]
type = ChangeState
value =7020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) =1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 BEN LOBO]
type = ChangeState
value = 7030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 BEN LOBO]
type = ChangeState
value = 7040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA BEN LOBOAGARRE]
type = ChangeState
value =7000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA BEN LOBO PUÑOS]
type = ChangeState
value = 7100
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 80
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA BEN LOBO PUÑOS]
type = ChangeState
value = 7200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 1
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x > 30
trigger1 = p2dist x < 200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 MULTIOJOS]
type = ChangeState
value =8020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 MULTIOJOS]
type = ChangeState
value =8030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 MULTIOJOS]
type = ChangeState
value = 8040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=5
trigger1 = p2dist x > 30
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA MULTIOJOS AGARRE]
type = ChangeState
value =8000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=200
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA MULTIOJOS  PUÑOS]
type = ChangeState
value = 8100
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA MULTIOJOS PUÑOS]
type = ChangeState
value = 8200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) = 1
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 HUMUNGOSARIO]
type = ChangeState
value =9020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <30
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 HUMUNGOSARIO]
type = ChangeState
value =9030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <30
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 HUMUNGOSARIO]
type = ChangeState
value = 9040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >50
trigger1 = p2dist x < 130
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO AGARRE]
type = ChangeState
value =9000
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = p2dist x <80
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO  PUÑOS]
type = ChangeState
value = 9100
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO PUÑOS]
type = ChangeState
value = 9200
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=999
trigger1 = p2dist x >30
trigger1 = p2dist x <200
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 HUMUNGOSARIO SUPREMO]
type = ChangeState
value =9520
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 HUMUNGOSARIO SUPREMO]
type = ChangeState
value =9530
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = p2dist x <100
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 HUMUNGOSARIO SUPREMO]
type = ChangeState
value = 9540
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = ctrl
--------------------------------------------------
[State -1,IA Guard HUMUNGOSARIO SUPREMO]
type = ChangeState
value = 9254
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x >30
trigger1 = statetype != a  &&  P2MOVEtype = A |numproj>=1
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO SUPREMO AGARRE]
type = ChangeState
value =9700
triggerall = power >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO SUPREMO PUÑOS]
type = ChangeState
value = 9720
triggerall = power >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA HUMUNGOSARIO SUPREMO PUÑOS]
type = ChangeState
value = 9730
triggerall = power >= 2500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 2
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x <30
trigger1 = statetype != A
trigger1 = ctrl

--------------------------------------------------
[State -1,IA GOLPE 1 ECO ECO]
type = ChangeState
value =13020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 40
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 ECO ECO]
type = ChangeState
value =13030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 40
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 ECO ECO]
type = ChangeState
value = 13040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 40
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO SUPER ECO ECO]
type = ChangeState
value =13000
triggerall = power >= 1200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x > 30
trigger1 = p2dist x < 200
trigger1 = random <=500
trigger1 = statetype =S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO MULTIECOS ]
type = ChangeState
value =13100
triggerall = power >= 2000
triggerall = numhelper(15000) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=700
trigger1 = p2dist x > 30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO CAMARA ULTRASONICA]
type = ChangeState
value =13200
triggerall = power >= 2500
triggerall = numhelper(13201) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 1 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=990
trigger1 = p2dist x > 30
trigger1 = p2dist x < 250
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 ECO ECO SUPREMO]
type = ChangeState
value =133020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0  && var(11) =2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 ECO ECO SUPREMO]
type = ChangeState
value =133030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 ECO ECO SUPREMO]
type = ChangeState
value = 133040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) =2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x < 50
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO SUPER ECO ECO SUPREMO]
type = ChangeState
value =133000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO MULTIECOS SUPREMO]
type = ChangeState
value =133100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x > 50
trigger1 = p2dist x <300
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ECO ECO CAMARA ULTRASONICA SUPREMO]
type = ChangeState
value =133200
triggerall = p2movetype = a || enemy, NumProj >= 1
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) =0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  ECO ECO SUPREMO DISCO 1]
type = ChangeState
value = 133900
triggerall = numhelper(133950) = 0
triggerall = numhelper(133951) = 0
triggerall = numhelper(133952) = 0
triggerall = numhelper(133953) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >=1000
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA ECO ECO SUPREMO DISCO 2]
type = ChangeState
value = 133901
triggerall = numhelper(133950) = 1
triggerall = numhelper(133951) = 0
triggerall = numhelper(133952) = 0
triggerall = numhelper(133953) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >=1000
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA ECO ECO SUPREMO DISCO 3]
type = ChangeState
value = 133902
triggerall = numhelper(133950) = 1
triggerall = numhelper(133951) = 1
triggerall = numhelper(133952) = 0
triggerall = numhelper(133953) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >=1000
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA ECO ECO SUPREMO DISCO 4]
type = ChangeState
value = 133903
triggerall = numhelper(133950) = 1
triggerall = numhelper(133951) = 1
triggerall = numhelper(133952) = 1
triggerall = numhelper(133953) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 2 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >=1000
trigger1 = random <=500
trigger1 = p2dist x > 50
trigger1 = statetype != A
trigger1 = ctrl
 --------------------------------------------------
[State -1,IA GOLPE 1 ULTRA-T]
type = ChangeState
value =14020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) =0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x <30
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 ULTRA-T]
type = ChangeState
value =14030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12)=1
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x <30
trigger1 = enemy,statetype = S | enemy,statetype = c
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 ULTRA-T]
type = ChangeState
value = 14040
triggerall = var(2) =0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=5
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ULTRA-T MULTIRAFAGAS]
type = ChangeState
value =14000
triggerall = power >= 1200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ULTRA-T RAFAGA GRANDE]
type = ChangeState
triggerall = power >= 2000
value = 14100
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ULTRA-T SUPER RAYO]
type = ChangeState
value = 14200
triggerall = power >= 2700
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) =0
triggerall = var(6) = 0
triggerall = var(7) =0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 && var(12)=1 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x >30
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 RATH]
type = ChangeState
value =150020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 RATH]
type = ChangeState
value = 150030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 RATH]
type = ChangeState
value = 150040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA ATAQUE AEREO RATH]
type = ChangeState
value = 150000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA TACLEADA RATH]
type = ChangeState
value = 150100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GARRAZOS RATH]
type = ChangeState
value = 150200
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 1 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) =1
trigger1 = random <=900
trigger1 = p2dist x <70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 XLR8]
type = ChangeState
value =160020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 XLR8]
type = ChangeState
value = 160030
triggerall = stateno !=160030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 XLR8]
type = ChangeState
value = 160040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA ATAQUE AEREO XLR8]
type = ChangeState
value = 160000
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA TACLEADA XLR8]
type = ChangeState
value = 160100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GARRAZOS XLR8]
type = ChangeState
value = 160200
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 1 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x >70
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 WILDVINE]
type = ChangeState
value =170020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=200
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 WILDVINE]
type = ChangeState
value = 170030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=200
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 WILDVINE]
type = ChangeState
value = 170040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >70
trigger1 = random <=100
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA BOMBAS WILDVINE]
type = ChangeState
value = 170000
TRIGGERALL = NUMHELPER(170050) <=10
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = p2dist x <300
trigger1 = random <=600
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GIRO WILDVINE]
type = ChangeState
value = 170100
trigger1 = POWER >= 1500
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=400
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA PUAS DEL SUELO WILDVINE]
type = ChangeState
value = 170200
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) =1 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=900
trigger1 = p2dist x >50
trigger1 = p2dist x <500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 ARTICGUANA]
type = ChangeState
value =180020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 ARTICGUANA]
type = ChangeState
value = 180030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random   <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 ARTICGUANA]
type = ChangeState
value = 180040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random   <=500
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA VIENTO CONGELANTE ARTICGUANA]
type = ChangeState
value = 180000
TRIGGERALL = NUMHELPER(170050) <=10
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random   <=500
trigger1 = p2dist x >50
trigger1 = p2dist x <300
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA COLUMNAS DE HIELO ARTICGUANA]
type = ChangeState
value = 180100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random   <=500
trigger1 = p2dist x >50
trigger1 = p2dist x <300
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ESFERAS DE CONGELANTES ARTICGUANA]
type = ChangeState
value = 180200
trigger1 = POWER >= 2300
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 1  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=999
trigger1 = p2dist x >50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA COMBO AEREO ARTICGUANA]
type = ChangeState
value = 180010
triggerall = var(16) = 1
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = p2dist x <50
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA COMBO AERE0 1]
type = ChangeState
value = 1010
triggerall = var(50) = 1
triggerall = var(22) = 0
triggerall = var(16) = 0
triggerall = var(18) = 0
trigger1 = random <=500
trigger1 = p2dist x <50
trigger1 = statetype = A
trigger1= p2statetype = a
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA FANTASMATICO VOLAR]
type = ChangeState
value = 323000
triggerall = var(50) = 1
triggerall = var(22) = 0
triggerall = var(16) = 0
triggerall = var(18) = 1
trigger1 = random <=500
trigger1 = p2dist x <50
trigger1 = statetype = A
trigger1= p2statetype = a
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 1 FEEDBACK]
type = ChangeState
value =316020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 2 FEEDBACK]
type = ChangeState
value = 316030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,GOLPE 3 FEEDBACK]
type = ChangeState
value = 316040
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1, AGARRE FEEDBACK]
type = ChangeState
value = 316000
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=100
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,AURA DE CHOQUE FEEDBACK]
type = ChangeState
value = 316100
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <70
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,SUPER VOLTAJE FEEDBACK]
type = ChangeState
value = 316200
trigger1 = POWER >= 2300
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 1 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >80
trigger1 = random <=999
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 FANTASMATICO]
type = ChangeState
value =326020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 FANTASMATICO]
type = ChangeState
value = 326030
triggerall = ENEMY,STATENO != 260
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x > 50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 FANTASMATICO]
type = ChangeState
value = 326040
triggerall = ENEMY,STATENO != 260
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA  FANTASMATICO INTANGIBLE]
type = ChangeState
value = 320000
triggerall = Fvar(18) = 0
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FANTASMATICO SUSTO]
type = ChangeState
value = 321000
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <100
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FANTASMATICO TENTACULOS EN EL SUELO]
type = ChangeState
value = 322000
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 FANTASMATICO]
type = ChangeState
value =336020
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 FANTASMATICO]
type = ChangeState
value = 336030
triggerall = STATENO != 336030
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 FANTASMATICO]
type = ChangeState
value = 336040
triggerall = ENEMY,STATENO != 260
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1&&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA  FANTASMATICO INTANGIBLE]
type = ChangeState
value = 331000
triggerall = Fvar(18) = 0
trigger1 = POWER >= 1000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) =0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FANTASMATICO SUSTO]
type = ChangeState
value = 332000
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0&& var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x <70
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA FANTASMATICO TENTACULOS EN EL SUELO]
type = ChangeState
value = 333000
trigger1 = POWER >= 2200
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 1 ALIEN X]
type = ChangeState
value =190019
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 2 ALIEN X]
type = ChangeState
value = 190000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = random <=10
trigger1 = statetype = S
trigger1 = ctrl
--------------------------------------------------
[State -1,IA GOLPE 3 ALIEN X]
type = ChangeState
value = 1760
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >70
trigger1 = random <=99
trigger1 = statetype = S
trigger1 = ctrl

--------------------------------------------------
[State -1,IA ALIEN X MANO GIGANTE]
type = ChangeState
value = 191000
triggerall = var(40) = 0
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ALIEN X CUCHILLAS]
type = ChangeState
value = 192000
triggerall = var(40) = 0
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ALIEN X RAYOS CELESTIAL]
type = ChangeState
value = 193000
triggerall = var(40) = 0
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ALIEN X ESPACIO ONDA DE ARIRE]
type = ChangeState
value = 1900000
triggerall = var(40) = 1
trigger1 = POWER >= 900
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = p2dist x <40
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ALIEN X ESPACIO METEORIOS]
type = ChangeState
value = 1910000
triggerall = var(40) = 1
trigger1 = POWER >= 1800
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) =1
trigger1 = p2dist x >50
trigger1 = p2dist x <40
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
--------------------------------------------------
[State -1,IA ALIEN X ESPACIO AGUJERO NEGRO]
type = ChangeState
value = 1920000
triggerall = var(40) = 1
trigger1 = POWER >= 2000
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) =0 && var(14) = 0&& var(15) = 0 && var(16) = 0  && var(17) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 1
trigger1 = p2dist x >50
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA MUNDOS ]
type = ChangeState
value = 190100
trigger1 = POWER >= 3000
triggerall = var(40) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) =0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 1&& var(10) = 0
triggerall = var(50) = 1
trigger1 = random <=500
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA FF]
type = ChangeState
value = 60
TRIGGERALL = STATENO!=100
triggerall = var(14) = 1
triggerall = var(50) = 1
trigger1 = random <=200
trigger1 = p2dist x >100
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA BB]
type = ChangeState
value = 70
triggerall = var(14) = 1
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x <50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA FF]
type = ChangeState
value = 31660
TRIGGERALL = STATENO!=100
triggerall = var(17) = 1
triggerall = var(50) = 1
trigger1 = random <=200
trigger1 = p2dist x >100
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA BB]
type = ChangeState
value = 31670
triggerall = var(17) = 1
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x <50
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
[State -1,IA FF]
type = ChangeState
value = 100
triggerall = var(8) != 2
TRIGGERALL = STATENO!=100
triggerall = var(14) = 0
triggerall = var(17) = 0
triggerall = var(50) = 1
trigger1 = random <=200
trigger1 = p2dist x >100
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA BB]
type = ChangeState
value = 105
triggerall = var(14) = 0
triggerall = var(17) = 0
triggerall = var(50) = 1
trigger1 = random <=100
trigger1 = p2dist x <50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,AFF]
type = ChangeState
value = 6005
triggerall = var(6) = 0
triggerall = var(14) = 0
triggerall = var(50) = 1
trigger1 = random <=20
trigger1 = p2dist x >200
trigger1 = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,ABB]
type = ChangeState
value = 6006
triggerall = var(6) = 0
triggerall = var(14) = 0
triggerall = var(50) = 1
trigger1 = random <=10
trigger1 = p2dist x <50
trigger1 = statetype = A
trigger1 = ctrl
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA BB]
type = ChangeState
value = 120
triggerall = var(50) = 1
trigger1 = random <=900
trigger1= enemy,movetype = a
trigger1 = p2dist x <50
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA ACTIVAR OMNITRIX]
type = ChangeState
value = 10001
triggerall = stateno != 10001
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >= 0
trigger1 = random <=999
trigger1 = statetype != A
trigger1 = ctrl
;----------------
-----------------------------------------------------------
[State -1,IA  HUMUNGOSARIO SUPREMO]
type = ChangeState
value = 9800
triggerall = life < lifemax/2
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 1
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >= 2000
trigger1 = random <=900
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  BESTIA SUPREMO]
type = ChangeState
value = 1001
triggerall = var(2) = 1
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power = 3000
trigger1 = random <=999
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  ECO ECO SUPREMO]
type = ChangeState
value =13001
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 1&&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >= 1000
trigger1 = random <=999
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  CANONBALL SUPREMO]
type = ChangeState
value = 2001
triggerall = var(2) = 0
triggerall = var(3) = 1
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 0 &&    var(20) = 0 && var(21) = 0 && var(22) = 0&& var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = power >= 1000
trigger1 = random <=999
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA FANTASMATICO COMPLETO]
type = ChangeState
value = 330000
TRIGGERALL = LIFE = LIFEMAX <=4
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 1 && var(19) = 0 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = var(22) = 0
triggerall = power >=500
trigger1 = random <=900
trigger1 = p2dist x >70
trigger1 = statetype != A
trigger1 = ctrl

;---------------------------------------------------------------------------
[State -1,IA FANTASMATICO COMPLETO INTAGIBILIDAD]
type = ChangeState
value = 320000
triggerall = Fvar(18) = 0
triggerall = var(2) = 0
triggerall = var(3) = 0
triggerall = var(4) = 0
triggerall = var(5) = 0
triggerall = var(6) = 0
triggerall = var(7) = 0
triggerall = var(8) = 0
triggerall =  var(9) = 0 &&  var(11) = 0 &&  var(12) = 0 && var(13) = 0 && var(14) = 0 && var(15) = 0 && var(16) = 0  && var(17) = 0 && var(18) = 0 && var(19) = 1 &&   var(20) = 0 && var(21) = 0 && var(22) = 0&& var(10) = 0
triggerall = var(50) = 1
triggerall = var(22) = 0
triggerall = power >=500
trigger1 = random <=500
trigger1 = p2dist x >70
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  ALIENIGENAS RANDOM]
type = ChangeState
value = 9900
triggerall = power >=500
triggerall = stateno  = 9900
triggerall = var(56) = 1
triggerall = var(8) != 2
triggerall = var(3) != 2
triggerall = var(11) != 2
triggerall = var(9) != 2
triggerall = var(10) = 0
triggerall = var(50) = 1
triggerall = var(18) = 0
triggerall = var(22) = 0
triggerall = var(20) = 0
triggerall = var(21) = 0
triggerall =  var(19) = 0
trigger1 = random =[10,50]
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA  ALIENIGENAS RANDOM]
type = ChangeState
value = 9902
triggerall = power >=500
triggerall = stateno  != 9902
triggerall = var(56) = 1
triggerall = var(8) != 2
triggerall = var(3) != 2
triggerall = var(11) != 2
triggerall = var(9) != 2
triggerall = var(22) = 0
triggerall = var(10) = 0
triggerall = var(2) = 0
triggerall = var(20) = 0
triggerall = var(21) = 0
triggerall =  var(19) = 0
triggerall = var(50) = 1
trigger1 = random =[10,50]
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
[State -1,IA CARGA]
type = ChangeState
value = 6010
triggerall =  var(50) = 1
triggerall = power < 3000
trigger1 = statetype != A
trigger1 = ctrl
trigger1 = random <=300
trigger1 = p2dist x >220

