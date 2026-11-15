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
command = x
time = 30

[command]
name = "SUPER2"
command = y
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
command = ~D,DB,B,b
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
command = ~B,DB,D,DF,F,a
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
command = d
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
command = y+z ; con el botÃƒÆ’Ã‚Â³n A+B activamos la AI
time = 1

[Command]
name = "AI desactivado"
command = b+c ; Con el boton B+C desactivamos la AI
time = 1
;---------------------------------------------------------------------------

[Command]
name="ichigo_form"
command=w
time=1

[Command]
name="ichigo_revert"
command=/$D,w
time=1

[Command]
name="ichigo_skill1"
command=x
time=1

[Command]
name="ichigo_skill2"
command=/$B,x
time=1

[Command]
name="ichigo_skill3"
command=/$F,x
time=1

[Command]
name="ichigo_skill4"
command=/$D,x
time=1

[Command]
name="ichigo_skill5"
command=/$D,/$F,x
time=1

[Command]
name="ichigo_skill6"
command=/$D,/$B,x
time=1

[Command]
name="ichigo_super"
command=y
time=1

[Command]
name="ichigo_ultimate"
command=z
time=1

[Command]
name="ichigo_charge"
command=/s
time=1

[Statedef -1]

[State -1, Charge spiritual pressure]
type=ChangeState
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
triggerall=power<10000
trigger1=command="ichigo_charge"
value=900810
[State -1, Choose next form]
type=MapSet
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
trigger1=command="ichigo_form" || command="ichigo_revert"
map="ichigo.next"
value=ifelse(command="ichigo_revert",0,ifelse(var(2)=0,2,ifelse(var(2)=2,3,ifelse(var(2)=3,5,ifelse(var(2)=5,4,ifelse(var(2)=4,6,ifelse(var(2)=6,7,ifelse(var(2)=7,8,ifelse(var(2)=8,9,ifelse(var(2)=9,10,ifelse(var(2)=10,11,0)))))))))))
[State -1, Transform]
type=ChangeState
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
trigger1=command="ichigo_form" || command="ichigo_revert"
value=900800

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=1400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=1500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=111400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=111500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=131400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=131500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1500
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=171400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=171500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=1500
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=151400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=2000
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=151500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=2000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=191400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=191500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1500
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=211400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=211500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1500
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=231400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1000
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=231500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=251400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1000
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=251500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=271200

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=271500

[State -1, ichigo_skill5]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=2000
triggerall=command="ichigo_skill5"
trigger1=ctrl
value=291400

[State -1, ichigo_skill6]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=1500
triggerall=command="ichigo_skill6"
trigger1=ctrl
value=291500

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=1100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=1200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=1300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=111200

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=111300

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=111700

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=131200

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1500
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=131300

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=131700

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=500
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=171100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=171200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1500
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=171300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=500
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=151100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=1500
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=151200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=151300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=191100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=1500
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=191200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=191300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=211100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=2000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=211200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1500
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=211300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=231100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=231200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1500
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=231300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=251100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1500
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=251200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1500
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=251300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=271100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=271400

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=271300

[State -1, ichigo_skill2]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=1000
triggerall=command="ichigo_skill2"
trigger1=ctrl
value=291100

[State -1, ichigo_skill3]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=1000
triggerall=command="ichigo_skill3"
trigger1=ctrl
value=291200

[State -1, ichigo_skill4]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=1500
triggerall=command="ichigo_skill4"
trigger1=ctrl
value=291300

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=1000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=3000
triggerall=command="ichigo_super"
trigger1=ctrl
value=3200

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=0 && Power>=3000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=3000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=111100

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=1000
triggerall=command="ichigo_super"
trigger1=ctrl
value=111400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=2 && Power>=3000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=112000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=131100

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=1000
triggerall=command="ichigo_super"
trigger1=ctrl
value=131400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=3 && Power>=5000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=132000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=171000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=1500
triggerall=command="ichigo_super"
trigger1=ctrl
value=171400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=5 && Power>=5000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=173000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=151000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=1500
triggerall=command="ichigo_super"
trigger1=ctrl
value=151400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=4 && Power>=10000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=153000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=191000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=2000
triggerall=command="ichigo_super"
trigger1=ctrl
value=191400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=6 && Power>=5000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=193000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=211000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=1500
triggerall=command="ichigo_super"
trigger1=ctrl
value=211400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=7 && Power>=6000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=213100

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=231000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=1500
triggerall=command="ichigo_super"
trigger1=ctrl
value=231400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=8 && Power>=7000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=233000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=251000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=1000
triggerall=command="ichigo_super"
trigger1=ctrl
value=251400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=9 && Power>=8500
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=253000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=271000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=1000
triggerall=command="ichigo_super"
trigger1=ctrl
value=271200

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=10 && Power>=8500
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=273000

[State -1, ichigo_skill1]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=1500
triggerall=command="ichigo_skill1"
trigger1=ctrl
value=291000

[State -1, ichigo_super]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=2000
triggerall=command="ichigo_super"
trigger1=ctrl
value=291400

[State -1, ichigo_ultimate]
type=ChangeState
triggerall=!AILevel && RoundState=2 && StateType!=A
triggerall=var(2)=11 && Power>=10000
triggerall=command="ichigo_ultimate"
trigger1=ctrl
value=293000


;//==========================
;// add004-1-sctrls-start
;//==========================
;--- partner_standby
[state 0]
	type=selfstate
	value=190190
	ctrl=0
	trigger1=ctrl && numpartner && !ishelper && roundstate=2 && pos y=0
	trigger1=(sysfvar(4)>0) && (sysfvar(0)>0) && playeridexist(floor(sysfvar(0)))
	trigger1=(playerid(floor(sysfvar(0))),var(0)=90900) && (playerid(floor(sysfvar(0))),var(22)=4)
	ignorehitpause=1
;##Add.List01##
;//==========================
;// add004-1-sctrls-end
;//==========================



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
trigger1 = statetype != C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Correr Atras
[State -1, Correr Atras]
type = ChangeState
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
value = 80
trigger1 = command = "Super Jump"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
;SUPERS:
;===========================================================================
; Saigo no Getsuga Tenshou
[State -1, Saigo no Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(3050) = 0
Triggerall = power >= 3000
triggerall = var(2) = 0
value = 3000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Double Getsuga Tenshou
[State -1, Double Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 3000
triggerall = var(2) = 0
value = 3200
triggerall = command = "SUPER2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Black Getsuga Tenshou
[State -1, Black Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(112050) = 0
Triggerall = power >= 3000
triggerall = var(2) = 2
value = 112000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Double Saigo no Getsuga Tenshou
[State -1, Double Saigo no Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(3050) = 0
Triggerall = power >= 5000
triggerall = var(2) = 3
value = 132000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Final Getsuga Tenshou
[State -1, Final Getsuga Tenshou]
type = ChangeState 
Triggerall = numhelper(3050) = 0
Triggerall = power >= 10000
triggerall = var(2) = 4
value = 153000
Triggerall = life <= lifemax/2
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Ulra Cero
[State -1, Ulra Cero]
type = ChangeState
Triggerall = power >= 5000
triggerall = var(2) = 5
value = 173000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(193050) = 0
Triggerall = power >= 5000
triggerall = var(2) = 6
value = 193000
triggerall = command = "SUPER1"
triggerall = command != "holddown"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 6
Triggerall = numhelper(191650) = 0
Triggerall = power >= 4000
value = 191600
triggerall = command = "SUPER1"
triggerall = command = "holddown"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(213150) = 0
Triggerall = numhelper(213160) = 0
Triggerall = power >= 6000
triggerall = var(2) = 7
value = 213100
triggerall = command = "SUPER1"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Gran Ray Cero
[State -1, Gran Ray Cero]
type = ChangeState 
triggerall = var(2) = 8
Triggerall = numhelper(233050) = 0
Triggerall = power >= 7000
value = 233000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS Gran Ray Cero
[State -1,HOS Gran Ray Cero]
type = ChangeState 
triggerall = var(2) = 9
Triggerall = numhelper(233050) = 0
Triggerall = power >= 8500
value = 253000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; BANKAI Ultimate Getsuga Tenshou
[State -1,BANKAI Ultimate Getsuga Tenshou]
type = ChangeState
Triggerall = var(2) = 10
Triggerall = power >= 8500
value = 273000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS + BANKAI Cero + Ultimate Getsuga Tenshou
[State -1, HOS + BANKAI Cero + Ultimate Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(293030) = 0
Triggerall = power >= 10000
triggerall = var(2) = 11
value = 293000
triggerall = command = "SUPER1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;SPECIALS:
;===========================================================================
;---------------------------------------------------------------------------
;HOS + BANKAI Getsuga Tenshou
[State -1,HOS + BANKAI Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 1500
value = 291000
triggerall = var(2) = 11
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS + BANKAI Speed Attack
[State -1,HOS + BANKAI Speed Attack]
type = ChangeState
triggerall = var(2) = 11
Triggerall = power >= 1000
value = 291100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI Cero
[State -1,HOS + BANKAI Cero]
type = ChangeState
triggerall = var(2) = 11
Triggerall = numhelper(291250) = 0
Triggerall = power >= 1000
value = 291200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS + BANKAI Ichigo Raid Speed Attack
[State -1,HOS + BANKAI Ichigo Raid Speed Attack]
type = ChangeState
Triggerall = power >= 1500
value = 291300
triggerall = var(2) = 11
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
;HOS + BANKAI  Gran Rey Cero
[State -1,HOS + BANKAI Gran Rey Cero]
type = ChangeState
triggerall = var(2) = 11
Triggerall = numhelper(291420) = 0
Triggerall = power >= 2000
value = 291400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS + BANKAI Sword Tornado Getsuga Tenshou
[State -1,HOS + BANKAI Sword Tornado Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 1500
value = 291500
triggerall = var(2) = 11
triggerall = command = "SPECIAL 6"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;BANKAI Cut
[State -1,BANKAI Cut]
type = ChangeState
Triggerall = power >= 1000
value = 271000
triggerall = var(2) = 10
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; BANKAI Speed Attack
[State -1,BANKAI Dark Speed Attack]
type = ChangeState
triggerall = var(2) = 10
Triggerall = power >= 1000
value = 271100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;BANKAI Sword Waves
[State -1,BANKAI Sword Waves]
type = ChangeState
Triggerall = power >= 1000
value = 271400
triggerall = var(2) = 10
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
;BANKAI Ichigo Raid Speed Attack
[State -1,BANKAI Ichigo Raid Speed Attack]
type = ChangeState
Triggerall = power >= 1000
value = 271300
triggerall = var(2) = 10
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
;BANKAI Ushi Bari
[State -1,BANKAI Ushi Bari]
type = ChangeState
triggerall = var(2) = 10
Triggerall = power >= 1000
value = 271200
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;BANKAI Sword Tornado Getsuga Tenshou
[State -1,BANKAI Sword Tornado Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 1500
value = 271500
triggerall = var(2) = 10
triggerall = command = "SPECIAL 6"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
;HOS Ushi Bari
[State -1, Ushi Bari]
type = ChangeState
triggerall = var(2) = 9
Triggerall = power >= 1000
value = 251000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS Counter
[State -1,HOS Counter]
type = ChangeState
triggerall = var(2) = 9
Triggerall = power >= 1000
value = 251100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS Getsugo Juujishou
[State -1,HOS Getsugo Juujishou]
type = ChangeState
triggerall = var(2) = 9
Triggerall = numhelper(251450) = 0
Triggerall = power >= 1500
value = 251200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS Sword Tornado Getsuga Tenshou
[State -1,HOS Sword Tornado Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 9
Triggerall = power >= 1500
value = 251300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; HOS Cero
[State -1, HOS Cero]
type = ChangeState
triggerall = var(2) = 9
Triggerall = power >= 1000
value = 251400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
;HOS Reiatsu Explosion
[State -1,HOS Reiatsu Explosion]
type = ChangeState
triggerall = var(2) = 9
Triggerall = power >= 1000
value = 251500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Ushi Bari
[State -1, Ushi Bari]
type = ChangeState
triggerall = var(2) = 8
Triggerall = power >= 1000
value = 231000
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Counter
[State -1, Counter]
type = ChangeState
triggerall = var(2) = 8
Triggerall = power >= 1000
value = 231100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Ichigo Raid Speed Attack
[State -1, Ichigo Raid Speed Attack]
type = ChangeState
triggerall = var(2) = 8
Triggerall = power >= 1000
value = 231200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
triggerall = var(2) = 8
Triggerall = power >= 1500
value = 231300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Getsuga Juujishou
[State -1, Getsuga Juujishou]
type = ChangeState
triggerall = var(2) = 8
Triggerall = numhelper(231450) = 0
Triggerall = power >= 1500
value = 231400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Sword Tornado Getsuga Tenshou
[State -1, Sword Tornado Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 8
Triggerall = power >= 1000
value = 231500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Instant Attack
[State -1, Instant Attack]
type = ChangeState
Triggerall = power >= 1000
value = 211000
triggerall = var(2) = 7
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Waves
[State -1, Waves]
type = ChangeState
Triggerall = power >= 1000
value = ifelse(statetype = A,211101,211100)
triggerall = var(2) = 7
triggerall = command = "SPECIAL 2"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Raid
[State -1, Raid]
type = ChangeState
Triggerall = power >= 2000
value = ifelse(statetype = A,211207,211200)
triggerall = var(2) = 7
triggerall = command = "SPECIAL 3"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
[State -1,]
type = ChangeState
Triggerall = power >= 1500
value = 211300
triggerall = var(2) = 7
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(211450) = 0
Triggerall = power >= 1500
value = 211400
triggerall = var(2) = 7
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
Triggerall = power >= 1500
value = ifelse(statetype = A,211503,211500)
triggerall = var(2) = 7
triggerall = command = "SPECIAL 6"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Cut
[State -1, Cut]
type = ChangeState
Triggerall = power >= 1000
value = 191000
triggerall = var(2) = 6
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Counter
[State -1, Counter]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1000
value = 191100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Sword
[State -1, Sword]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = 191200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Crescend Getsuga Tenshou
[State -1, Crescend Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 6
Triggerall = numhelper(191350) = 0
Triggerall = power >= 1000
value = 191300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 6
Triggerall = numhelper(191450) = 0
Triggerall = power >= 2000
value = 191400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
triggerall = var(2) = 6
Triggerall = power >= 1500
value = 191500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Sword curse
[State -1, Sword curse]
type = ChangeState
Triggerall = numhelper(1060) = 0
Triggerall = power >= 1000
value = 171000
triggerall = var(2) = 5
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Sonido
[State -1, Sonido]
type = ChangeState
Triggerall = power >= 500
value = 171100
triggerall = var(2) = 5
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Brutal Voice
[State -1, Brutal Voice]
type = ChangeState
Triggerall = numhelper(1250) = 0
Triggerall = power >= 1000
value = 171200
triggerall = command = "SPECIAL 3"
triggerall = var(2) = 5
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Super Slach
[State -1, Super Slach]
type = ChangeState
Triggerall = power >= 1500
value = 171300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
triggerall = var(2) = 5
trigger1 = ctrl
;---------------------------------------------------------------------------
; Cero
[State -1, Cero]
type = ChangeState
Triggerall = power >= 1500
value = 171400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
triggerall = var(2) = 5
trigger1 = ctrl
;---------------------------------------------------------------------------
; Saigo no Getsuga Tenshou
[State -1, Saigo no Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(1550) = 0
Triggerall = power >= 1500
value = 171500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
triggerall = var(2) = 5
trigger1 = ctrl
;---------------------------------------------------------------------------
; Ushi Bari
[State -1, Ushi Bari]
type = ChangeState
Triggerall = power >= 1000
value = 151000
triggerall = var(2) = 4
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Counter
[State -1, Counter]
type = ChangeState
Triggerall = power >= 500
value = 151100
triggerall = var(2) = 4
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Ichigo Raid Speed Attack
[State -1, Ichigo Raid Speed Attack]
type = ChangeState
Triggerall = power >= 1500
value = 151200
triggerall = var(2) = 4
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
Triggerall = power >= 1000
value = 151300
triggerall = var(2) = 4
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Saigo no Getsuga Tenshou
[State -1, Saigo no Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(1450) = 0
Triggerall = power >= 1500
value = 151400
triggerall = command = "SPECIAL 5"
triggerall = var(2) = 4
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Sword Tornado Getsuga Tenshou
[State -1, Sword Tornado Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 2000
value = 151500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
triggerall = var(2) = 4
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Speed High Attack
[State -1, Speed High Attack]
type = ChangeState
Triggerall = power >= 1000
value = 131100
triggerall = var(2) = 3
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Sword Speed Attack
[State -1, Sword Speed Attack]
type = ChangeState
Triggerall = power >= 1000
value = 131200
triggerall = var(2) = 3
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Instant Getsuga Tenshou
[State -1, Instant Getsuga Tenshou]
type = ChangeState
Triggerall = power >= 1500
value = 131300
triggerall = var(2) = 3
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Sword Waves
[State -1, Sword Waves]
type = ChangeState
Triggerall = power >= 1000
value = 131700
triggerall = var(2) = 3
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(111450) = 0
Triggerall = power >= 1000
value = 131400
triggerall = var(2) = 3
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
Triggerall = power >= 1500
value = 131500
triggerall = var(2) = 3
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Speed High Attack
[State -1, Speed High Attack]
type = ChangeState
Triggerall = power >= 1000
value = 111100
triggerall = var(2) = 2
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Sword Speed Attack
[State -1, Sword Speed Attack]
type = ChangeState
Triggerall = power >= 1000
value = 111200
triggerall = var(2) = 2
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Ichigo Raid Speed Attack
[State -1, Ichigo Raid Speed Attack]
type = ChangeState
Triggerall = numhelper(1250) = 0
Triggerall = power >= 1000
value = 111300
triggerall = var(2) = 2
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Sword Waves
[State -1, Sword Waves]
type = ChangeState
Triggerall = power >= 1000
value = 111700
triggerall = var(2) = 2
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
Triggerall = numhelper(111450) = 0
Triggerall = power >= 1000
value = 111400
triggerall = var(2) = 2
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
Triggerall = power >= 1500
value = 111500
triggerall = var(2) = 2
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Strong Cut
[State -1, Strong Cut]
type = ChangeState
Triggerall = power >= 1000
value = 1000
triggerall = var(2) = 0
triggerall = command = "SPECIAL 1"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Counter
[State -1, Counter]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1100
triggerall = command = "SPECIAL 2"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Crescend Getsuga Tenshou
[State -1, Crescend Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 0
Triggerall = numhelper(1250) = 0
Triggerall = power >= 1000
value = 1200
triggerall = command = "SPECIAL 3"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Giratory Sword
[State -1, Giratory Sword]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1300
triggerall = command = "SPECIAL 4"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Getsuga Tenshou
[State -1, Getsuga Tenshou]
type = ChangeState
triggerall = var(2) = 0
Triggerall = numhelper(1450) = 0
Triggerall = power >= 1000
value = 1400
triggerall = command = "SPECIAL 5"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
; Reiatsu Explosion
[State -1, Reiatsu Explosion]
type = ChangeState
triggerall = var(2) = 0
Triggerall = power >= 1000
value = 1500
triggerall = command = "SPECIAL 6"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = movecontact
;---------------------------------------------------------------------------
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
; Bankai
[State -1, Bankai]
type = ChangeState
triggerall = power >= 2000
triggerall = var(2) = 0
triggerall = palno = 1
value = 900
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Bankai Cancelar
[State -1, Bankai Cancelar]
type = ChangeState
triggerall = var(2) = 2
triggerall= palno = 1
value = 11905
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Mask
[State -1, Mask]
type = ChangeState
triggerall = power >= 4000
triggerall = life <= lifemax * 3/5
triggerall = var(2) = 2
triggerall = palno = 1
value = 910
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Mask Cancelar
[State -1, Mask Cancelar]
type = ChangeState
triggerall = var(2) = 3
triggerall = palno = 1
value = 915
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Mugetsu
[State -1, Mugetsu Bankai]
type = ChangeState
triggerall = power >= 7000
triggerall = life <= lifemax*2/5
triggerall = var(2) = 5
triggerall = palno = 1
value = 920
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Fullbring Bankai
[State -1, Fullbring Bankai]
type = ChangeState
Triggerall = numhelper(19405) = 0
Triggerall = numhelper(19406) = 0
Triggerall = numhelper(19550) = 0
Triggerall = numhelper(19555) = 0
Triggerall = numhelper(19557) = 0
Triggerall = numhelper(19625) = 0
triggerall = power >= 1500
triggerall = var(2) = 6
triggerall = palno = 1 || palno = 4
value = 21900
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Fullbring Bankai Cancelar
[State -1, Fullbring Bankai Cancelar]
type = ChangeState
Triggerall = numhelper(19405) = 0
Triggerall = numhelper(19406) = 0
Triggerall = numhelper(19550) = 0
Triggerall = numhelper(19555) = 0
Triggerall = numhelper(19557) = 0
Triggerall = numhelper(19625) = 0
triggerall = var(2) = 7
triggerall = palno = 1 || palno = 4
value = 21905
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; HOS
[State -1, HOS]
type = ChangeState
Triggerall = var(2) = 8
triggerall = Power >= 1500
value = 23900
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; HOS Cancelar
[State -1, HOS Cancelar]
type = ChangeState
triggerall = var(2) = 9
value = 23906
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; True Bankai
[State -1, True Bankai]
type = ChangeState
Triggerall = var(2) = 8
triggerall = Power >= 1500
value = 23910
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; True Bankai Cancelar
[State -1, True Bankai Cancelar]
type = ChangeState
triggerall = var(2) = 10
value = 23915
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI 
[State -1,HOS + BANKAI]
type = ChangeState
Triggerall = var(2) = 9
triggerall = Power >= 5000
value = 23920
triggerall = command = "holddown"
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI (HOS) Cancelar
[State -1,HOS + BANKAI (HOS) Cancelar]
type = ChangeState
Triggerall = var(2) = 11
triggerall = numhelper(23980) > 0
value = 23925
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;BANKAI + HOS 
[State -1, BANKAI + HOS ]
type = ChangeState
Triggerall = var(2) = 10
triggerall = Power >= 5000
value = 23930
triggerall = command = "holddown"
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;BANKAI + HOS Cancelar
[State -1, BANKAI + HOS Cancelar]
type = ChangeState
triggerall = var(2) = 11
triggerall = numhelper(23990) > 0
value = 23935
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Mugetsu Cancelar
;[State -1, Mask Cancelar]
;type = ChangeState
;triggerall = var(2) = 4
;value = 925
;triggerall = command = "holddown"
;triggerall = command = "s"
;Triggerall = statetype != A
;trigger1 = ctrl
;---------------------------------------------------------------------------
; Vaste Lorde
;[State -1, Vasto Lorde]
;type = ChangeState
;triggerall = power >= 2000
;triggerall = var(2) = 2
;value = 930
;triggerall = command = "z"
;Triggerall = statetype != A
;trigger1 = ctrl
;---------------------------------------------------------------------------
; Mugetsu Cancelar
;[State -1, Mask Cancelar]
;type = ChangeState
;triggerall = var(2) = 5
;value = 935
;triggerall = command = "holddown"
;triggerall = command = "s"
;Triggerall = statetype != A
;trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI A
[State -1, A]
type = ChangeState
value = 29200
triggerall = var(2) = 11
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI B
[State -1, B]
type = ChangeState
value = 29300
triggerall = var(2) = 11
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1,HOS + BANKAI C]
type = ChangeState
value = 29400
triggerall = var(2) = 11
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
triggerall = ctrl
Trigger1 = numhelper(405) = 0
;---------------------------------------------------------------------------
;HOS + BANKAI A Aire
[State -1, A Aire]
type = ChangeState
value = 29600
triggerall = var(2) = 11
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI B Aire
[State -1, B Aire]
type = ChangeState
value = 29610
triggerall = var(2) = 11
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS + BANKAI C Aire
[State -1, C Aire]
type = ChangeState
value = 29620
triggerall = var(2) = 11
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;TRUE BANKAI A
[State -1, A]
type = ChangeState
value = 27200
triggerall = var(2) = 10
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;TRUE BANKAI B
[State -1, B]
type = ChangeState
value = 27300
triggerall = var(2) = 10
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;TRUE BANKAI C
[State -1,BANKAI C]
type = ChangeState
value = 27400
triggerall = var(2) = 10
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
triggerall = ctrl
Trigger1 = numhelper(27405) = 0
;---------------------------------------------------------------------------
;TRUE BANKAI A Aire
[State -1, A Aire]
type = ChangeState
value = 27600
triggerall = var(2) = 10
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;TRUE BANKAI B Aire
[State -1, B Aire]
type = ChangeState
value = 27610
triggerall = var(2) = 10
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;TRUE BANKAI C Aire
[State -1, C Aire]
type = ChangeState
value = 27620
triggerall = var(2) = 10
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS A
[State -1, A]
type = ChangeState
value = 25200
triggerall = var(2) = 9
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS B
[State -1, A]
type = ChangeState
value = 25300
triggerall = var(2) = 9
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1,HOS C]
type = ChangeState
value = 25400
triggerall = var(2) = 9
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
triggerall = ctrl
Trigger1 = numhelper(25405) = 0
;---------------------------------------------------------------------------
;HOS A Aire
[State -1, A Aire]
type = ChangeState
value = 25600
triggerall = var(2) = 9
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS B Aire
[State -1, B Aire]
type = ChangeState
value = 25610
triggerall = var(2) = 9
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
;HOS C Aire
[State -1, C Aire]
type = ChangeState
value = 25620
triggerall = var(2) = 9
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 23200
Triggerall = var(2) = 8
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 23300
Triggerall = var(2) = 8
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
value = 23400
triggerall = var(2) = 8
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
triggerall = ctrl
Trigger1 = numhelper(23405) = 0
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 23600
triggerall = var(2) = 8
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 23610
triggerall = var(2) = 8
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
value = 23620
;Triggerall = numhelper(23405) = 0
triggerall = var(2) = 8
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
triggerall = var(2) = [6,7]
value = 200+var(11)
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
triggerall = var(2) = [6,7]
value = 300+var(11)
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
triggerall = var(2) = [6,7]
triggerall = power >= 200
Triggerall = numhelper(405) = 0
Triggerall = numhelper(406) = 0
value = 19400
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Y
[State -1, Y]
type = ChangeState
triggerall = var(2) = [6,7]
value = 800+var(11)
triggerall = command = "y"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Shunpo
[State -1, Shunpo]
triggerall = !(map(jus.enabled) && statetype = A && command = "jus.up")
type = ChangeState
Triggerall = power >= 400
value = 19480
triggerall = command = "z"
trigger1 = ctrl
trigger2 = numhelper(700) > 0
trigger2 = var(2) >= 8
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
triggerall = var(2) = [6,7]
value = 600+var(11)
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
triggerall = var(2) = [6,7]
value = 610+var(11)
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
triggerall = var(2) = [6,7]
triggerall = power >= 200
Triggerall = numhelper(625) = 0
value = 19620
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Y
[State -1, Y]
type = ChangeState
triggerall = var(2) = [6,7]
value = 810+var(11)
triggerall = command = "y"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 17200
triggerall = var(2) = 5
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 17300
triggerall = var(2) = 5
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
Triggerall = numhelper(11405) = 0
value = 17400
triggerall = var(2) = 5
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 17600
triggerall = var(2) = 5
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 17610
triggerall = var(2) = 5
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
Triggerall = numhelper(405) = 0
value = 17620
triggerall = var(2) = 5
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 15200
triggerall = var(2) = 4
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 15300
triggerall = var(2) = 4
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
Triggerall = numhelper(11405) = 0
value = 15400
triggerall = var(2) = 4
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 15600
triggerall = var(2) = 4
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 15610
triggerall = var(2) = 4
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
Triggerall = numhelper(11625) = 0
value = 15620
triggerall = var(2) = 4
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 13200
triggerall = var(2) = 3
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 13300
triggerall = var(2) = 3
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
Triggerall = numhelper(11405) = 0
value = 13400
triggerall = var(2) = 3
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 13600
triggerall = var(2) = 3
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 13610
triggerall = var(2) = 3
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
Triggerall = numhelper(11625) = 0
value = 13620
triggerall = var(2) = 3
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 11200
triggerall = var(2) = 2
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
value = 11300
triggerall = var(2) = 2
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
Triggerall = numhelper(11405) = 0
value = 11400
triggerall = var(2) = 2
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
value = 11600
triggerall = var(2) = 2
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
value = 11610
triggerall = var(2) = 2
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
Triggerall = numhelper(11625) = 0
value = 11620
triggerall = var(2) = 2
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A
[State -1, A]
type = ChangeState
value = 200
triggerall = var(2) = 0
triggerall = command = "a"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B
[State -1, B]
type = ChangeState
triggerall = var(2) = 0
value = 300
triggerall = command = "b"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C
[State -1, C]
type = ChangeState
Triggerall = numhelper(405) = 0
triggerall = var(2) = 0
value = 400
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
Triggerall = power < powermax
triggerall = !var(47)
value = 500
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; A Aire
[State -1, A Aire]
type = ChangeState
triggerall = var(2) = 0
value = 600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; B Aire
[State -1, B Aire]
type = ChangeState
triggerall = var(2) = 0
value = 610
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; C Aire
[State -1, C Aire]
type = ChangeState
triggerall = var(2) = 0
Triggerall = numhelper(405) = 0
value = 620
triggerall = power >= 200
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl

