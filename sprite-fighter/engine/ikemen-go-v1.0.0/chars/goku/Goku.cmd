;#ADD004BASIC PIEs#
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
command = z
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
command = ~D,DB,B,b
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

[Command]
name="goku_super1"
command=z
time=1

[Command]
name="goku_super2"
command=/$D,z
time=1

[Command]
name="goku_special_7"
command=d
time=1

[Command]
name="goku_special_1"
command=x
time=1

[Command]
name="goku_special_2"
command=/$B,x
time=1

[Command]
name="goku_special_3"
command=/$F,x
time=1

[Command]
name="goku_special_4"
command=/$D,x
time=1

[Command]
name="goku_special_5"
command=y
time=1

[Command]
name="goku_special_6"
command=/$D,/$F,x
time=1

[Command]
name="goku_meteor_rush"
command=/$B,d
time=1

[Command]
name="goku_form"
command=w
time=1

[Command]
name="goku_revert"
command=/$D,w
time=1

[Command]
name="goku_charge"
command=/s
time=1

[Command]
name="goku_hold_bomb"
command=/z
time=1

[Statedef -1]

[State -1, Cycle forms]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_form" || command="goku_revert"
trigger1=ctrl
value=900800
[State -1, Charge]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_charge" && power<3000
trigger1=ctrl
value=900810

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=1500

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Super Energy Blast Air]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype=A
trigger1=ctrl
value=1580

[State -1, Meteor Impact]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=29500

[State -1, Twin Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=31500

[State -1, Wind barrage]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1500
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=35500

[State -1, Mastered Blast]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1000
triggerall=command="goku_special_6"
triggerall=statetype!=A
trigger1=ctrl
value=37500

[State -1, Angry Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=3000
triggerall=command="goku_super2"
triggerall=statetype!=A
trigger1=ctrl
value=3300

[State -1, Meteor Impact]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=3000
triggerall=command="goku_super2"
triggerall=statetype!=A
trigger1=ctrl
value=3500

[State -1, Honba no Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=3000
triggerall=command="goku_super2"
triggerall=statetype!=A
trigger1=ctrl
value=3900

[State -1, Taiyoken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=1100

[State -1, Taiyoken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=1100

[State -1, Kaioken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=1200

[State -1, Kaioken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=1200

[State -1, Kaiokenx10]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=33200

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Shunkan Ido]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=300
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=1300

[State -1, Meteor Smash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=1800

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Explosive Wave]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=25100

[State -1, Meteor Smash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=25200

[State -1, Meteor Impact]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=27200

[State -1, Super God Fist - Start]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=29200

[State -1, Ki Machinegun]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=31200

[State -1, Meteor Rush God KameHameHa]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1500
triggerall=command="goku_meteor_rush"
triggerall=statetype!=A
trigger1=ctrl
value=33700

[State -1, Meteor Rush God KameHameHa]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1500
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=33700

[State -1, Egoist Counter]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1000
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=35100

[State -1, Ultra Slash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=35200

[State -1, Power Explosion]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1000
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=35600

[State -1, Power Explosion]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1000
triggerall=command="goku_special_4"
triggerall=statetype!=A
trigger1=ctrl
value=35600

[State -1, Invisible Blows]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1500
triggerall=command="goku_special_2"
triggerall=statetype!=A
trigger1=ctrl
value=37100

[State -1, Mastred Slash]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=2000
triggerall=command="goku_special_3"
triggerall=statetype!=A
trigger1=ctrl
value=37200

[State -1, Super Spirit Bomb: gather energy]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=500
triggerall=command="goku_super1"
triggerall=statetype!=A
triggerall=numhelper(3054)=0
trigger1=ctrl
value=3000

[State -1, Super Genkidama]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=0
triggerall=command="goku_super1"
triggerall=statetype!=A
triggerall=numhelper(3054)=1
trigger1=ctrl
value=3001

[State -1, Meteor Smash Kamehamehax20]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=3100

[State -1, Instant Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=3200

[State -1, Super Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=3400

[State -1, Ryu Ken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=3600

[State -1, Super Kamehameha SSGOD]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=3700

[State -1, Honba no Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=4000

[State -1, Honba no Kamehameha Kaioken]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=4100

[State -1, Last Resor]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=4250

[State -1, Ultra Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=4300

[State -1, Im Not A Hero]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=3000
triggerall=command="goku_super1"
triggerall=statetype!=A
trigger1=ctrl
value=4400

[State -1, Genkidama]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=1600

[State -1, Meteor Fall]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=1001

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Meteor Smash Conbination]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=25600

[State -1, Essence Raid]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=2000
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=37300

[State -1, Meteor Rush]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1500
triggerall=command="goku_special_7"
triggerall=statetype!=A
trigger1=ctrl
value=29600

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=1000

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype!=A
trigger1=ctrl
value=1400

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=0 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=1 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=2 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=3 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Kamehameha Aire]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1000
triggerall=command="goku_special_5"
triggerall=statetype=A
trigger1=ctrl
value=1700

[State -1, Ki Liberation]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=4 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=29000

[State -1, Godly ki share]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=5 && power>=1000
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=31000

[State -1, One Inch Punch]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=6 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=33000

[State -1, One Inch Punch]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=7 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=33000

[State -1, One Inch Punch]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=8 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=33000

[State -1, Ultra Kiai]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=9 && power>=500
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=35000

[State -1, Soaring Fist]
type=ChangeState
triggerall=!AILevel && roundstate=2
triggerall=map(goku.form)=10 && power>=1000
triggerall=command="goku_special_1"
triggerall=statetype!=A
trigger1=ctrl
value=37000

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
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
triggerall = stateno != 60
triggerall = stateno != 70
value = 70
trigger1 = command = "BB"
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
;---------------------------------------------------------------------------
; Genkidama Charge
[State -1, Genkidama Charge]
type = ChangeState
triggerall = numhelper(3054)= 0
Triggerall = power >= 500
triggerall = var(3) = 0
triggerall = var(2) = 0
value = 3000
triggerall = command = "x"
triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Genkidama
[State -1, Super Genkidama]
type = ChangeState
value = 3001
triggerall = numhelper(3054)= 1
triggerall = var(3) = 0
triggerall = var(2)=0
triggerall = command = "SUPER1"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Meteor Smash Kamehamehax20
[State -1, Meteor Smash Kamehamehax20]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(3) = 1
Triggerall = power >= 3000
value = 3100
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;--------------------------------------------------------------------------
; Instant Kamehameha
[State -1, Instant Kamehameha]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 3000
value = 3200
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;--------------------------------------------------------------------------
; Angry Kamehameha
[State -1, Angry Kamehameha]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 3000
value = 3300
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Kamehameha
[State -1, Super Kamehameha]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 3400
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
; Meteor Impact
[State -1, Meteor Impact]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 3000
value = 3500
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Ryu Ken
[State -1, Ryu Ken]
type = ChangeState
Triggerall = teammode != simul && enemynear, teammode != simul
triggerall = var(2) = 3
Triggerall = power >= 3000
value = 3600
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Kamehameha SSGOD
[State -1, Super Kamehameha SSGOD]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 3000
value = 3700
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Hakai!
;[State -1, Hakai!]
;type = ChangeState
;triggerall = var(2) = 5
;Triggerall = teammode != simul && enemynear, teammode != simul
;Triggerall = power >= 3000
;triggerall = command ="SUPER2"
;Triggerall = statetype != A
;value = 3800
;trigger1 = ctrl
;---------------------------------------------------------------------------
; Honba no Kamehameha
[State -1, Honba no Kamehameha]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 3000
value = 3900
triggerall = command ="SUPER2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Honba no Kamehameha
[State -1, Honba no Kamehameha]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(3) = 0
Triggerall = power >= 3000
value = 4000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Honba no Kamehameha Kaioken
[State -1, Honba no Kamehameha Kaioken]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(3) = 1
Triggerall = power >= 3000
value = 4100
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;  Last Resor
[State -1,  Last Resor]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(3) = 2
Triggerall = power >= 3000
value = 4250
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Ultra Kamehameha
[State -1, Ultra Kamehameha]
type = ChangeState
triggerall = var(2) = 6
value = 4300
Triggerall = power >= 3000
triggerall = command = "SUPER1"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Im Not A Hero
[State -1, Im Not A Hero]
type = ChangeState
triggerall = var(2) = 7
value = 4400
Triggerall = power >= 3000
triggerall = command = "SUPER1"
trigger1 = ctrl
;===========================================================================
;SPECIALS:
;===========================================================================
; Genkidama
[State -1, Genkidama]
type = ChangeState
triggerall = var(3) = 0
triggerall = var(2) = 0
Triggerall = power >= 1500
value = 1600
triggerall = command = "SPECIAL 7"
trigger1 = ctrl
Triggerall = statetype != A
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Fall
[State -1, Meteor Fall]
type = ChangeState
triggerall = var(3) >= 1
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1001
triggerall = command = "SPECIAL 7"
trigger1 = ctrl
Triggerall = statetype != A
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Smash Conbination
[State -1, Meteor Smash Conbination]
type = ChangeState
triggerall = var(2) = 1 || var(2) = 2 || var(2) = 4 || var(2) = 5 || var(2) = 6
Triggerall = power >= 1500
value = 25600
triggerall = command = "SPECIAL 7"
Triggerall = statetype != C
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Essence Raid
[State -1, Essence Raid]
type = ChangeState
triggerall = var(2) = 7
Triggerall = power >= 2000
value = 37300
triggerall = command = "SPECIAL 7"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Rush
[State -1, Meteor Rush]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1500
value = 29600
triggerall = command = "SPECIAL 7"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = [0,2]
Triggerall = power >= 500
value = 1000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
;Taiyoken
[State -1, Taiyoken]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 500
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Kaioken
[State -1, Kaioken]
type = ChangeState
triggerall = var(2) = 0 || var(2) = 5
triggerall = var(3) = 0
triggerall = var(3) != 1
Triggerall = power >= 1500
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
[State -1, Kaiokenx10]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(3) = 1
Triggerall = power >= 1500
value = 33200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Shunkan Ido
[State -1, Shunkan Ido]
type = ChangeState
triggerall = var(2) = 0 || var(2) = 1 || var(2) = 2 || var(2) = 3  || var(2) = 4 || var(2) = 5
Triggerall = power >= 300
value = 1300
triggerall = command = "SPECIAL 4"
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Kamehameha
[State -1, Kamehameha]
type = ChangeState
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Kamehameha Aire
[State -1, Kamehameha Aire]
type = ChangeState
Triggerall = power >= 1000
value = 1700
triggerall = command = "SPECIAL 5"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Super Energy Blast
[State -1, Super Energy Blast]
type = ChangeState
triggerall = var(2) != 3
triggerall = var(2) != 4
triggerall = var(2) != 6
triggerall = var(2) != 7
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
; Super Energy Blast
[State -1, Super Energy Blast Air]
type = ChangeState
triggerall = var(2) = [0,5]
Triggerall = power >= 1500
value = 1580
triggerall = command = "SPECIAL 6"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Smash
[State -1, Meteor Smash]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(3) = 1
Triggerall = power >= 1500
value = 1800
triggerall = command = "SPECIAL 3"
Triggerall = statetype != C
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Explosive Wave
[State -1, Explosive Wave]
type = ChangeState
triggerall = var(2) = [1,5]
Triggerall = power >= 1500
value = 25100
triggerall = command = "SPECIAL 2"
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Smash
[State -1, Meteor Smash]
type = ChangeState
triggerall = var(2) = 1
Triggerall = power >= 1000
value = 25200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Impact
[State -1, Meteor Impact ]
type = ChangeState
triggerall = var(2) = 2
Triggerall = power >= 1500
value = 27200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Ki Liberation
[State -1, Ki Liberation]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 500
value = 29000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
;  Super God Fist - Start
[State -1,  Super God Fist - Start]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1500
value = 29200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Meteor Impact
[State -1, Meteor Impact]
type = ChangeState
triggerall = var(2) = 3
Triggerall = power >= 1500
value = 29500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Godly ki share
[State -1, Godly ki share]
type = ChangeState
triggerall = enemy,stateno != 31005
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31000
triggerall = command = "SPECIAL 1"
trigger1 = ctrl
Triggerall = statetype != A
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Ki Machinegun
[State -1, Ki Machinegun]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Twin Kamehameha
[State -1, Twin Kamehameha]
type = ChangeState
triggerall = var(2) = 4
Triggerall = power >= 1000
value = 31500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; One Inch Punch
[State -1, One Inch Punch]
type = ChangeState
triggerall = var(2) = 5
Triggerall = power >= 500
value = 33000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
;Meteor Rush God KameHameHa
[State -1,Meteor Rush God KameHameHa ]
type = ChangeState
triggerall = var(3) >= 1
triggerall = var(2) = 5
Triggerall = power >= 1500
value = 33700
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Ultra Kiai
[State -1, Ultra Kiai]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 500
value = 35000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Egoist Counter
[State -1,Egoist Counter]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Ultra Slash
[State -1, Ultra Slash]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 35200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Power Explosion
[State -1, Power Explosion]
type = ChangeState
triggerall = var(2) = 6 || var(2) = 7
Triggerall = power >= 1000
value = 35600
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Wind barrage
[State -1, Wind barrage]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = 35500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Soaring Fist
[State -1, Soaring Fist]
type = ChangeState
triggerall = var(2) = 7
Triggerall = power >= 1000
value = 37000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Invisible Blows
[State -1, Invisible Blows]
type = ChangeState
triggerall = var(2) = 7
Triggerall = power >= 1500
value = 37100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Mastred Slash
[State -1, Mastred Slash]
type = ChangeState
triggerall = var(2) = 7
Triggerall = power >= 2000
value = 37200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;---------------------------------------------------------------------------
; Mastered Blast
[State -1, Mastered Blast]
type = ChangeState
triggerall = var(2) = 7
Triggerall = power >= 1000
value = 37500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(7777) > 0
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; MUI
[State -1, MUI]
type = ChangeState
triggerall = numhelper(1968) = 0
triggerall = power >= 1000
triggerall = var(2) = 6
Triggerall = var(3) = 0
value = 1906
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;MG
[State -1, MG]
type = ChangeState
triggerall = numhelper(1968) = 0
triggerall = life < lifemax/2
triggerall = var(2) < 6
triggerall = power >= 2700-var(2)*2000
Triggerall = var(3) = 0
value = 1903
triggerall = command = "holddown"
triggerall = command = "a"
triggerall = command = "c"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SSGSS
[State -1, SSGSS]
type = ChangeState
triggerall = power >= 2500-var(2)*2000
triggerall = var(2) < 5
Triggerall = var(3) = 0
value = 1901
triggerall = command = "holddown"
triggerall = command = "b"
triggerall = command = "c"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SSGOD
[State -1, SSGOD]
type = ChangeState
triggerall = power >= 200-var(2)*1500
triggerall = var(2) < 4
Triggerall = var(3) = 0
value = 1900
triggerall = command = "holddown"
triggerall = command = "b"
triggerall = command = "a"
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
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS1 Cancelar
[State -1, SS1 Cancelar]
type = ChangeState
triggerall = var(2) = 1
value = 705
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS2
[State -1, SS2]
type = ChangeState
triggerall = power >= 1000-var(2)*500
triggerall = var(2) < 2
Triggerall = var(3) = 0
value = 800
triggerall = command = "holddown"
triggerall = command = "b"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS2 Cancelar
[State -1, SS2 Cancelar]
type = ChangeState
triggerall = var(2) = 2
value = 805
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS3
[State -1, SS3]
type = ChangeState
triggerall = power >= 1500-var(2)*1000
triggerall = var(2) < 3
Triggerall = var(3) = 0
value = 900
triggerall = command = "holddown"
triggerall = command = "c"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SS3 Cancelar
[State -1, SS3 Cancelar]
type = ChangeState
triggerall = var(2) = 3
value = 905
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SSGOD Cancelar
[State -1, SSGOD Cancelar]
type = ChangeState
triggerall = var(2) = 4
value = 1905
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; SSGSS Cancelar
[State -1, SSGSS Cancelar]
type = ChangeState
triggerall = var(2) = 5
value = 1902
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; MG Cancelar
[State -1, MG Cancelar]
type = ChangeState
triggerall = var(2) = 6|| var(2) = 7
value = 1904
triggerall = command = "holddown"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 200
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 300
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
; Super Dash
[State -1, Super Dash]
type = ChangeState
value = 650
triggerall = power >= 200
triggerall = command = "holdfwd"
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < 3000
value = 500
triggerall = command = "s"
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire BASE
[State -1, A Aire BASE]
type = ChangeState
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire BASE
[State -1, B Aire BASE]
type = ChangeState
value = 610
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
