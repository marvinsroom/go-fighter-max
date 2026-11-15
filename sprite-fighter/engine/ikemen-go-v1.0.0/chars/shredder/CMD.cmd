
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
command.time = 30

; Default value for the "buffer.time" parameter of a Command. Minimum 1,
; maximum 30.
command.buffer.time = 1

;-| Super Motions |--------------------------------------------------------

[Command]
name="SUPER"
command=~D,DF,F,D,DF,F,x
time=30
[Command]
name="SUPER"
command=~D,DF,F,D,DF,F,y
time=30
[Command]
name="SUPER"
command=~D,DF,F,D,DF,F,z
time=30

[Command]
name="SUPER2"
command=~D,DB,B,D,DB,B,a
time=30
[Command]
name="SUPER2"
command=~D,DB,B,D,DB,B,b
time=30
[Command]
name="SUPER2"
command=~D,DB,B,D,DB,B,c
time=30

[Command]
name="SUPER3"
command=~D,DF,F,D,DF,F,a
time=30
[Command]
name="SUPER3"
command=~D,DF,F,D,DF,F,b
time=30
[Command]
name="SUPER3"
command=~D,DF,F,D,DF,F,c
time=30


[Command]
name="HYPER"
command=~D, B, F, x
time=30
[Command]
name="HYPER"
command=~D, B, F, y
time=30
[Command]
name="HYPER"
command=~D, B, F, z
time=30

[Command]
name="HYPER"
command=~D, B, F, a
time=30
[Command]
name="HYPER"
command=~D, B, F, b
time=30
[Command]
name="HYPER"
command=~D, B, F, c
time=30

;-| Special Motions |------------------------------------------------------

[Command]
name = "GAUNTLET"
command = x,x,x
time = 60

[Command]
name = "GAUNTLET"
command = y,y,y
time = 60

[Command]
name = "GAUNTLET"
command = z,z,z
time = 60

[Command]
name = "GAUNTLET"
command = x,x,x,x,x
time = 60

[Command]
name = "GAUNTLET"
command = y,y,y,y,y
time = 60

[Command]
name = "GAUNTLET"
command = z,z,z,z,z
time = 60

[Command]
name = "GAUNTLET"
command = x,x,x
time = 15


[Command]
name = "GAUNTLET"
command = y,y,y
time = 15

[Command]
name = "GAUNTLET"
command = z,z,z
time = 15

[Command]
name = "QCF_x"
command = ~D, DF, F, x
time=30

[Command]
name = "QCF_y"
command = ~D, DF, F, y
time=30

[Command]
name = "QCF_z"
command = ~D, DF, F, z
time=30

; AURA CRUSHER
[Command]
name = "QCB_x"
command = ~D, B, x
time=15

[Command]
name = "QCB_y"
command = ~D, B, y
time=15

[Command]
name = "QCB_z"
command = ~D, B, z
time=15

[Command]
name = "EX_BLAST"
command = ~D, DF, F, x+y
time=20

[Command]
name = "EX_BLAST2"
command = ~D, DF, F, y+z
time=20

[Command]
name = "EX_BLAST3"
command = ~D, DF, F,x+z
time=20



[Command]
name = "QCF_a"
command = ~D, DF, F, a
time=15

[Command]
name = "QCF_b"
command = ~D, DF, F, b
time=15

[Command]
name = "QCF_c"
command = ~D, DF, F, c
time=15

[Command]
name = "QCB_a"
command = ~D, B, a
time=15

[Command]
name = "QCB_b"
command = ~D, B, b
time=15

[Command]
name = "QCB_c"
command = ~D, B, c
time=15

[Command]
name = "FOOT"
command = ~D, F, a+b
time=30
[Command]
name = "FOOT2"
command = ~D, F, b+c
time=30

[Command]
name = "FOOT3"
command = ~D, B, a+b
time=30

[Command]
name = "FOOT4"
command = ~D, B, b+c
time=30

[Command]
name = "FOOT5"
command = ~D, F, a+c
time=30

[Command]
name = "FOOT6"
command = ~D, B, a+c
time=30


[Command]
name = "FOOT1-"
command = $F, a+b
time=30
[Command]
name = "FOOT1-"
command = $F, a+c
time=30
[Command]
name = "FOOT1-"
command = /F, a+b
time=30
[Command]
name = "FOOT1-"
command = /F, a+c
time=30
[Command]
name = "FOOT2-"
command = $F, b+c
time=30
[Command]
name = "FOOT2-"
command = /F, b+c
time=30



; DIVE KICK
;================
[command]
name = "DiveKick"
command = /D, c
time = 15
[command]
name = "DiveKick"
command =~D,F,c
time = 15
[command]
name = "DiveKick"
command = ~D, DF, F, c
time = 15

;-| Double Tap |-----------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10

[Command]
name = "super jump"
command = $D, $U
time = 15

;-| 2/3 Button Combination |-----------------------------------------------


[Command]
name = "guardpush"
command = x+y
time = 4

[Command]
name = "guardpush"
command = y+z
time = 4

[Command]
name = "guardpush"
command = x+z
time = 4

[Command]
name = "guardpush"
command = x+y+z
time = 4 


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


[Command]
name = "x+a" 
command = $UF,x+a
time = 1
[Command]
name = "x+a" 
command = $U,x+a
time = 1
[Command]
name = "x+a" 
command = $F,x+a
time = 1
[Command]
name = "x+a" 
command = x+a
time = 1

[Command]
name = "y+b" 
command = $UF,y+b
time = 1
[Command]
name = "y+b" 
command = $U,y+b
time = 1
[Command]
name = "y+b" 
command = $F,y+b
time = 1
[command]
name = "y+b" 
command = y+b
time = 1

[Command]
name = "z+c" 
command = $UF,z+c
time = 1
[Command]
name = "z+c" 
command = $U,z+c
time = 1
[Command]
name = "z+c" 
command = $F,z+c
time = 1
[Command]
name = "z+c" 
command = z+c
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
; Don't remove the following line. It's required by the CMD standard.
[Statedef -1]
[State ]
type=helper
trigger1=(stateno=0||stateno=5900)&&!ctrl&&!numhelper(20)
id=20
stateno=5150
keyctrl=1
ignorehitpause=1
pausemovetime=9999999
supermovetime=9999999
[State ]
type = NotHitBy
trigger1=ishelper(20)
value = SCA
ignorehitpause=1
time = 1
[State ]
type=assertspecial
trigger1=ishelper(20)
flag=invisible
ignorehitpause=1

[State ]
type=statetypeset
trigger1=ishelper(20)
movetype=i
ignorehitpause=1

[State ]
type=changeanim
trigger1=ishelper(20)
value=root,anim
ignorehitpause=1

[State ]
type=ctrlset
trigger1=ishelper(20)
value=0
ignorehitpause=1

[State ]
type=velset
trigger1=ishelper(20)
x=rootdist x
y=rootdist y
ignorehitpause=1

[State ]
type=parentvarset
trigger1=ishelper(20)
trigger1=stateno=5120
var(22)=1
ignorehitpause=1

[State ]
type=destroyself
trigger1=ishelper(20)
trigger1=time=100
ignorehitpause=1

[State ]
type=displaytoclipboard
trigger1=!ishelper
text="Training Mode = %d 0=No 1=Yes"
params=var(22)
ignorehitpause=1
;================

;---------------------------------------------------------------------------
;===========================================================================
;=================================< SUPER SHREDDER A.I. >===================
;===========================================================================

; SUPER SHREDDER LIGHTNING PRESSURE COMBO BREAKER
[State -1, LIGHTNING PRESSURE COMBO BREAKER]
type = ChangeState 
value = 33330
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall =  statetype!= A
triggerall= ctrl
trigger1 = Random < (100 * (AILevel ** 2 / 64.0))
trigger2 = p2bodydist x <= 75
trigger2 = p2movetype = A
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
ignorehitpause=1

;---------------------------------------------------------------------------
; SUPER SHREDDER Stand Light Punch
[State -1, Stand Light Punch]
type = ChangeState
value = 33200
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = AIlevel
triggerall = p2statetype != L
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 98
trigger1 = Random < (100 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER Stand Medium Punch
[State -1, Stand Medium Punch]
type = ChangeState
value = 33210
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 80
trigger1 = Random < (150 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER Stand Heavy Punch
[State -1, Stand Heavy Punch]
type = ChangeState
value = 33220
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 105
trigger1 = Random < (200 * (AILevel ** 2 / 64.0))
trigger1= ctrl
;---------------------------------------------------------------------------
; SUPER SHREDDER Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = 33230
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 80
trigger1 = Random < (250 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER Stand Medium Kick
[State -1, Stand Medium Kick]
type = ChangeState
value = 33240
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 60
trigger1 = Random < (300 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER Stand Heavy Kick
[State -1, Stand Medium Kick]
type = ChangeState
value = 33250
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
trigger1 =  statetype!= A
trigger1 = p2bodydist x <= 75
trigger1 = Random < (350 * (AILevel ** 2 / 64.0))
trigger1= ctrl
;---------------------------------------------------------------------------
; SUPER SHREDDER ENERGY FLAME FLOOR
[State -1, ENERGY FLAME FLOOR]
type = ChangeState
value = 33300
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 =  statetype!= A
trigger1 = Random < (500 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER ENERGY RETROMUTAGEN BLAST
[State -1, ENERGY RETROMUTAGEN BLAST]
type = ChangeState
value = 33310
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 =  statetype!= A
trigger1 = Random < (500 * (AILevel ** 2 / 64.0))
trigger1= ctrl

; SUPER SHREDDER ENERGY ICE BLAST
[State -1, ENERGY ICE BLAST]
type = ChangeState
value = 33320
triggerall = var(13)>0&& numhelper(3301)>0
triggerall=  numhelper(33302)<=0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2statetype = A
trigger1 =  statetype!= A
trigger1= ctrl

; SUPER SHREDDER GAUNTLET BLUR SUPER
[State -1, GAUNTLET BLUR SUPER]
type = ChangeState
value = 33380
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = stateno!=33380
triggerall = numhelper(33302)<=0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall = p2bodydist x <= 110
triggerall =  statetype!= A
triggerall= ctrl
trigger1 = Random < (600 * (AILevel ** 2 / 64.0))

; SUPER SHREDDER THUNDER WAVE SUPER
[State -1, THUNDER WAVE SUPER]
type = ChangeState
value = 33360
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = stateno!=33360
triggerall = numhelper(33302)<=0
triggerall = roundstate = 2
triggerall = AIlevel
triggerall = p2statetype != L
triggerall =  statetype!= A
triggerall= ctrl
trigger1 = Random < (700 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
;===========================================================================
;=================================< NORMAL SHREDDER A.I. >==================
;===========================================================================
[State -1]
Type=Changestate
Triggerall=Inguarddist ; Guard when in guard distance
triggerall = AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 94 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999 ; and the AI is on
trigger1 = stateno!=[120,160]
Trigger1=ctrl ; and we have control
value=120

;Guard Push
[State -1]
type = ChangeState
value = 720
triggerall = var(10) != 1&&statetype = S&&p2life!=0
triggerall = AIlevel = 1 && random <= 6 || AIlevel = 2 && random <= 16 || AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 94 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999
trigger1 = stateno = [150,153]
;-------------------------------------
[State -1]
type =ChangeState
value = 725
triggerall = var(10) != 1&&statetype = C&&p2life!=0
triggerall = AIlevel = 1 && random <= 6 || AIlevel = 2 && random <= 16 || AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 150 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999
trigger1 = stateno = [150,153]
;-------------------------------------
[State -1]
type =ChangeState
value = 730
triggerall = var(10) != 1&&statetype = A&&p2life!=0
triggerall = AIlevel = 1 && random <= 6 || AIlevel = 2 && random <= 16 || AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 150 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999
trigger1 = stateno = [154,155]
;===========================================================================
;---------------------------------------------------------------------------
; Taunt
[State -1, Taunt]
type = ChangeState
value = 195
triggerall = var(13)=0
triggerall = AILevel
triggerall = roundstate!=[3,4]
triggerall = statetype != A
triggerall = ctrl
triggerall = enemynear, numproj = 0
triggerall = enemynear, movetype != A
triggerall = life >= 400
trigger1 = p2bodydist x >= 150
trigger1 = life >= enemynear, life
trigger1 = random <= 6 && AILevel >= 6 || random <= 20 && AILevel >= 3 && AILevel <= 5 || random <= 40 && AILevel >= 1 && AILevel <= 2
trigger2 = p2bodydist x >= 150
trigger2 = p2statetype = L
trigger2 = random <= 12 && AILevel >= 6 || random <= 32 && AILevel >= 3 && AILevel <= 5 || random <= 56 && AILevel >= 1 && AILevel <= 2
trigger3 = win && random <= 57

; SUPER SHREDDER HYPER
[State -1, SUPER SHREDDER HYPER]
type = ChangeState
value = 3300
triggerall = roundstate = 2 
triggerall = AIlevel
triggerall = var(58)=0&&var(59)=0
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = power>=3000
triggerall =statetype!=A
trigger1 =statetype=S
trigger1 = ctrl

;---------------------------------------------------------------------------
; VORPAL CUTTER SUPER
[State -1, VORPAL CUTTER]
type = ChangeState
value = ifelse((movehit&&p2BodyDist X<=70 && Random <(500 * (AILevel ** 2 / 64.0))),3000,3100)
triggerall = roundstate = 2 
triggerall = AIlevel&&power>=1000
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = p2statetype != L
triggerall = statetype != A
trigger1 = ctrl
trigger1 = Random < (12 * (AILevel ** 2 / 64.0))
trigger1 = p2statetype != A
trigger2 = stateno = 250 || stateno = 420 || stateno = 220 && numhelper(216)=0 || stateno = 1400
trigger2 = movehit
trigger2 = Random < (200 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
[State -1, AI RETROMUTAGEN RAY]
type = ChangeState
value = 3010
triggerall = roundstate = 2 
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = power>=1000
triggerall =statetype!=A
triggerall = p2statetype !=L
triggerall = p2bodydist x >= 100
trigger1 = ctrl
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))
trigger2 = enemynear, ctrl = 0 &&var(18)=0 && var(19)=0
trigger2 = Random < (100 * (AILevel ** 2 / 64.0))
trigger2 = ctrl

;---------------------------------------------------------------------------
[State -1, AI AURA CRUSHER]
type = ChangeState
value = 1400
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall= numhelper(1001)=0
triggerall = roundstate = 2 
triggerall =statetype!=A
triggerall = p2bodydist x <= 230
triggerall = p2statetype != L
triggerall = p2movetype != A
trigger1 = ctrl
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))
trigger2 = ctrl
trigger2 = p2statetype = S
trigger2 = Random < (24 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 250 || stateno = 260&&animelemtime(6)>=1 ||stateno = 410 || stateno = 440
trigger3 = movehit
trigger3 = Random < (200 * (AILevel ** 2 / 64.0))
trigger4 = stateno = 420
trigger4 = movehit
trigger4 = Random < (500 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
[State -1, AI TSUKI NAGE]
type = ChangeState
value = 1300
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = numhelper(1001)=0
triggerall =  prevstateno!=1300&&stateno!=260&&stateno != 890&&stateno!=[1300,1400]
triggerall = roundstate = 2 
triggerall = statetype!=A
triggerall = p2bodydist x <= 210
triggerall = p2statetype != L
triggerall = p2movetype != A
trigger1 = ctrl
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))
trigger2 = ctrl
trigger2 = p2statetype = S
trigger2 = Random < (18 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 250&&movehit  || stateno = 410&&movehit || stateno = 440&&movehit
trigger3 = Random < (100 * (AILevel ** 2 / 64.0))
trigger3 = p2bodydist x <=130
trigger4 = stateno = 420 && movehit && p2bodydist x =[200,210]  
trigger4 = Random < (100 * (AILevel ** 2 / 64.0))
trigger5 = enemynear,stateno = 822
trigger5 = Random < (500 * (AILevel ** 2 / 64.0))
trigger5 = ctrl
trigger6 = enemynear,movetype = H &&p2bodydist x <=30&&enemynear, Vel Y>=1
trigger6 = Random < (200 * (AILevel ** 2 / 64.0))
trigger6 = ctrl
trigger7 = enemynear,movetype = H &&p2bodydist x <=30&&numtarget(216)>=1
trigger7 = Random < (200 * (AILevel ** 2 / 64.0))
trigger7 = ctrl

;---------------------------------------------------------------------------
; Dive Kick
[State -1, Dive Kick]
type = ChangeState
value = 1020
triggerall = AILevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = roundstate = 2 
triggerall = numtarget(1020)<=0
triggerall = statetype=A
triggerall = p2statetype != L
trigger1 = ctrl
trigger1 = p2bodydist x <= 100
trigger1 = p2statetype != A
trigger1 = Random < (100 * (AILevel ** 2 / 64.0))
trigger2 = p2bodydist x <= 65
trigger2 = p2statetype = C
trigger2 = ctrl
trigger2 = AIlevel >= 6
trigger3 = stateno=620 || stateno=650
trigger3 = movehit

;---------------------------------------------------------------------------
[State -1,AI ENERGY WAVE]
type = ChangeState
value = 1000
triggerall = AIlevel
triggerall = var(13)=0&&numhelper(3301)=0&&numhelper(1001)=0
triggerall = statetype!=A
triggerall = roundstate = 2
triggerall = p2statetype != L
trigger1 = ctrl
trigger1 = p2bodydist x >= 100
trigger1 = Random < (50 * (AILevel ** 2 / 64.0))
trigger1 = AILevel >= 6
trigger2 = stateno = 421 && movehit||stateno = 251 && movehit||stateno=220 && movecontact||stateno = 230 &&movecontact
trigger2 = p2bodydist x >=35
trigger2 = Random < (200 * (AILevel ** 2 / 64.0))
trigger2 = AILevel >= 6
trigger3 = var(18)=1||var(18)=1&&var(19)=1
trigger3 = (enemynear,stateno=[1501,1544])&&(enemynear, statetype!=A)
trigger3 = Random < (100 * (AILevel ** 2 / 64.0)) && AILevel >= 6
trigger3 = p2bodydist x >= 50
trigger3 = ctrl

;---------------------------------------------------------------------------
[State -1,AI SHURIKEN]
type = ChangeState
value = 1010
triggerall = AIlevel
triggerall = var(13)=0&&numhelper(3301)=0&&var(18)=0&&var(19)=0
triggerall = numhelper(1001)=0&&numhelper(1011)=0&&numhelper(1022)=0
triggerall = statetype!=A
triggerall = roundstate = 2
triggerall = p2statetype != L
trigger1 = ctrl
trigger1 = p2bodydist x >= 130
trigger1 = Random < (10 * (AILevel ** 2 / 64.0))
trigger2 = p2bodydist x >= 100 && enemynear, statetype!=A
trigger2 = Random < (20 * (AILevel ** 2 / 64.0))
trigger2 = ctrl
trigger3 = stateno = 250 && movehit && p2bodydist x <=90  
trigger3 = Random < (200 * (AILevel ** 2 / 64.0))
;---------------------------------------------------------------------------
;AI Throw
[State -1, AI Throw]
type = ChangeState
value = 800
triggerall = var(13)=0
triggerall = Random < (100 * (AILevel ** 2 / 64.0))
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = ctrl
triggerall = p2statetype != L
trigger1 = p2bodydist x <= 32 && p2movetype != H && p2statetype != A
trigger2 = enemynear, anim >= 120 && enemynear, anim <= 152 && p2bodydist x <= 10
trigger2 = p2statetype != A

;---------------------------------------------------------------------------
;AI Throw
[State -1, AI Throw]
type = ChangeState
value = 810
triggerall = var(13)=0
triggerall = Random < (100 * (AILevel ** 2 / 64.0))
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = ctrl
triggerall = p2statetype != L
trigger1 = p2bodydist x <= 32 && p2movetype != H && p2statetype != A
trigger2 = enemynear, anim >= 120 && enemynear, anim <= 152 && p2bodydist x <= 10
trigger2 = p2statetype != A

;---------------------------------------------------------------------------
[State -1, AI Levitating Dodge Forward]
type = ChangeState
value = 700
triggerall = enemynear,stateno != 822
triggerall = roundstate = 2 
triggerall = AIlevel
triggerall = numhelper(715)!=1
triggerall = statetype!=A
triggerall = ctrl
trigger1 = p2bodydist x >= 150
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))
trigger2 = p2bodydist x > 100
trigger2 = enemynear, ctrl = 0
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = AILevel >= 6
trigger2 = enemynear,stateno != 700 
trigger2 = enemynear,stateno != 710
trigger2 = enemynear,stateno != 100
;---------------------------------------------------------------------------
[State -1, AI Levitating Dodge Back]
type = ChangeState
value = 710
triggerall = enemynear,stateno != 822
triggerall = roundstate = 2 
triggerall = AIlevel
triggerall = numhelper(715)!=1
triggerall = statetype!=A
triggerall = ctrl
trigger1 = p2statetype = L
trigger1 = p2bodydist x <= 50
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))
trigger2 = p2bodydist x <= 100
trigger2 = p2movetype = A
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = AILevel >= 4

;---------------------------------------------------------------------------
[State -1, AI]
type = ChangeState
value = 620
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = statetype=A
trigger1 = stateno = 640;600
trigger1 = movecontact

;---------------------------------------------------------------------------
[State -1, AI]
type = ChangeState
value = 640
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = statetype=A
trigger1 = stateno = 610;611
trigger1 = movecontact

;---------------------------------------------------------------------------
[State -1, AI]
type = ChangeState
value = 610
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = statetype=A
trigger1 = stateno = 630 || stateno = 640
trigger1 = movecontact

;---------------------------------------------------------------------------
[State -1, AI]
type = ChangeState
value = 630
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = statetype=A
trigger1 = stateno = 600 
trigger1 = movecontact

;---------------------------------------------------------------------------
[State -1, AI Jump Light Punch]
type = ChangeState
value = ifelse((prevstateno!=640&&random<(300* (AILevel ** 2 / 64.0))), 640,600)
triggerall = AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
trigger1 = p2statetype = A
trigger1 = statetype=A
trigger1 = ctrl
trigger1 = p2bodydist x <= 80
trigger1 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = stateno=630
trigger2 = movecontact

;---------------------------------------------------------------------------
[State -1, AI wallbounce kick]
type = ChangeState
value = 231
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
triggerall = p2bodydist x <= 120
trigger1 = ctrl
trigger1 = Random < (50 * (AILevel ** 2 / 64.0))
trigger2 = stateno = 200 || stateno = 250 || stateno = 210 ||stateno = 440 || stateno = 220
trigger2 = movehit && p2bodydist x <= 50
trigger2 = Random < (100 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 420
trigger3 = movehit
trigger3 = Random < (300 * (AILevel ** 2 / 64.0))
trigger4 = stateno = 430
trigger4 = movehit
trigger4 = Random < (250 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
[State -1, AI Stand hard command kick]
type = ChangeState
value = 250
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = p2bodydist x <= 100
trigger1 = Random < (50 * (AILevel ** 2 / 64.0))
trigger1 = p2movetype != A
trigger2 = stateno = 210 && movehit
trigger2 = p2bodydist x >= 100
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 220 && movecontact
trigger3 = p2bodydist x >= 70
trigger3 = Random < (100 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
[State -1, AI Stand Light Kick]
type = ChangeState
value = ifelse((p2bodydist x >=20),200,230)
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = p2bodydist x <= 117
trigger1 = Random < (60 * (AILevel ** 2 / 64.0))
trigger2 = ctrl
trigger2 = p2bodydist x <= 45
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 220
trigger3 = p2bodydist x <= 30 && p2bodydist x >=15 
trigger3 = Random < (100 * (AILevel ** 2 / 64.0))
trigger4 = enemynear,stateno = 822
trigger4 = Random < (200 * (AILevel ** 2 / 64.0))
trigger4 = ctrl
;---------------------------------------------------------------------------
[State -1, AI Crouching Light Punch]
type = ChangeState
value = 400
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel 
triggerall = Pos Y=0
triggerall = roundstate = 2 
triggerall = p2statetype = s
trigger1 =  statetype!= A
trigger1 = ctrl
trigger1 = p2bodydist x <= 60
trigger1 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = stateno = 230 
trigger2 = p2bodydist x <= 40 
trigger2 = Random < (200 * (AILevel ** 2 / 64.0))
trigger2 = movecontact
trigger3 = stateno = 430
trigger3 = p2bodydist x <= 20 
trigger3 = movehit
trigger3 = Random < (100 * (AILevel ** 2 / 64.0))
;---------------------------------------------------------------------------
[State -1, AI Crouching Light Punch]
type = ChangeState
value = 410
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel 
triggerall = Pos Y=0
triggerall = roundstate = 2 
triggerall = p2statetype = s
trigger1 =  statetype!= A
trigger1 = ctrl
trigger1 = p2bodydist x <= 70
trigger1 = Random < (100 * (AILevel ** 2 / 64.0))
trigger2 = stateno = 400|| stateno = 230 || stateno = 430 || stateno = 440
trigger2 = p2bodydist x <= 40
trigger2 = Random < (500 * (AILevel ** 2 / 64.0)) 
trigger2 = movecontact
;---------------------------------------------------------------------------
[State -1, AI Stand Light Punch]
type = ChangeState
value = 200
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel && numenemy
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = p2bodydist x <= 117
trigger1 = Random < (60 * (AILevel ** 2 / 64.0))
trigger2 = ctrl
trigger2 = p2bodydist x <= 40
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger3 = stateno = 220 && numhelper(216)=0
trigger3 = p2bodydist x <= 30
trigger3 = Random < (100 * (AILevel ** 2 / 64.0))
trigger4 = enemynear,stateno = 822
trigger4 = Random < (500 * (AILevel ** 2 / 64.0))
trigger4 = ctrl
;---------------------------------------------------------------------------
[State -1, AI Stand med Punch]
type = ChangeState
value = 210
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = p2bodydist x <= 148
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = Random < (65 * (AILevel ** 2 / 64.0))
trigger2 = stateno = 200 || stateno = 230 || stateno = 400 || stateno = 410 ||stateno = 430
trigger2 = movecontact

;---------------------------------------------------------------------------
[State -1, AI crouch med kick]
type = ChangeState
value = 440
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = p2bodydist x <= 88
trigger1 = Random < (50 * (AILevel ** 2 / 64.0))
trigger1 = p2movetype != A
trigger2 = p2bodydist x <=40
trigger2 = stateno = 210 && movecontact

;---------------------------------------------------------------------------
[State -1, AI Stand hard Punch]
type = ChangeState
value = ifelse((!time&&p2bodydist x <=40),420,220)
Triggerall=!Inguarddist
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = p2bodydist x <= 125
triggerall = statetype != A
triggerall = p2statetype != L
triggerall = p2statetype != A
trigger1 = ctrl
trigger1 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = stateno = 210 || stateno = 240 || stateno = 410 || stateno = 440
trigger2 = p2bodydist x <= 70
trigger2 = movecontact
trigger3 = ctrl
trigger3 = p2bodydist x <= 30
trigger3 = Random < (14 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
; Crouching Strong Punch
[State -1, Crouching Strong Punch]
type = ChangeState
value = 420
triggerall = AIlevel 
triggerall =  statetype!= A
triggerall = roundstate = 2 
trigger1 = numhelper(216)<=1&&stateno = 220 && movehit&&p2bodydist x <=40 || stateno = 250 && movehit && p2bodydist x <= 50|| stateno = 210 && movehit&&p2bodydist x <=40||stateno = 410 && movehit
Trigger2=!Inguarddist
trigger2 = Random < (500 * (AILevel ** 2 / 64.0))
trigger2 = statetype!= A
trigger2 = ctrl
trigger2 = enemynear, numproj = 0
trigger2 = enemynear, movetype != H
trigger2 = p2bodydist x <= 30
trigger2 = p2bodydist y <= -50
trigger2 = random <= 30

[State -1, AI Follow up]
type = ChangeState
value = 421
trigger1 = AIlevel
trigger1 = stateno = 420
trigger1 = movecontact

;---------------------------------------------------------------------------
[State -1, AI Crouching Light Kick]
type = ChangeState
value = 430
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel 
triggerall = Pos Y=0
triggerall = roundstate = 2 
triggerall = p2statetype = s
trigger1 =  statetype!= A
trigger1 = ctrl
trigger1 = p2bodydist x <= 50
trigger1 = Random < (100 * (AILevel ** 2 / 64.0))

;==============
; Super Jump
;===============
[State -1, Super Jump]
type = ChangeState
value = 56
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = roundstate = 2 
triggerall = AIlevel = 1 && random <= 6 || AIlevel = 2 && random <= 16 || AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 150 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999
triggerall = statetype != A
trigger1 = stateno = 421 && movehit
trigger2 = ctrl && p2movetype = A && p2statetype != A && p2bodydist x >= 100 && random <= 16
trigger3 = ctrl && p2statetype = A && p2bodydist x >= 71 && random <= 16
trigger4 = ctrl && random <= 2

[State -1, normal Jump]
type = ChangeState
value = 40
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = roundstate = 2 
triggerall = AIlevel = 1 && random <= 6 || AIlevel = 2 && random <= 16 || AIlevel = 3 && random <= 32 || AIlevel = 4 && random <= 64 || AIlevel = 5 && random <= 72 || AIlevel = 6 && random <= 150 || AIlevel = 7 && random <=250 || AIlevel = 8 && random <= 999
triggerall = statetype != A
trigger1 = p2bodydist x <= 50 && p2movetype = H && p2statetype = A
trigger1 = ctrl
trigger2 = ctrl
trigger2 = enemynear, stateno = 822

;---------------------------------------------------------------------------
[State -1, AI Leap Back]
type = ChangeState
value = 105
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = ctrl
trigger1 = p2statetype = L && p2bodydist X <= 60
trigger1 = Random < (6 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
;AI Run Fwd
[State -1, AI Run Fwd]
type = ChangeState
value = 100
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = AIlevel
triggerall = roundstate = 2 
triggerall = statetype != A
triggerall = ctrl
triggerall = stateno != 100
triggerall = p2movetype != A
triggerall = p2bodydist x >= 100
trigger1 = Random < (12 * (AILevel ** 2 / 64.0))
trigger2 = p2statetype = L
trigger2 = Random < (64 * (AILevel ** 2 / 64.0))

;---------------------------------------------------------------------------
;===============================HUMAN=======================================
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------

;===========================================================================
;---------------------------------------------------------------------------
; SUPER SHREDDER HYPER
[State -1, SUPER SHREDDER HYPER]
type = ChangeState
value = 3300
triggerall = !AIlevel 
triggerall = var(59)=0
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = (command="HYPER")&&power>=3000
triggerall = command != "holddown"
triggerall =statetype!=A
trigger1 =statetype=S
trigger1 = ctrl
; SUPER SHREDDER END
[State -1, SUPER SHREDDER END]
type = ChangeState
value = 33529
triggerall = !AIlevel 
triggerall = var(59)=0
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = numhelper(3303)=0
triggerall = (command="HYPER")
triggerall = command != "holddown"
triggerall =statetype!=A
trigger1 = statetype=S
trigger1 = ctrl
;---------------------------------------------------------------------------
;SUPERS
;---------------------------------------------------------------------------
; SHADOW CLONE SUPER (KAGE BUNSHIN)
[State -1, SUPER1]
type = ChangeState
value = 3000
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = (command="SUPER3")&&power>=1000
triggerall = command!="FOOT"&&command!="FOOT2"
triggerall = command!="SUPER2"
triggerall =statetype!=A
trigger1 =statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&animelemtime(4)>=1&&movecontact
trigger4 = stateno=220&&animelemtime(4)>=1&&movecontact
trigger5 = stateno=230&&animelemtime(2)>=1&&movecontact
trigger6 = stateno=231&&animelemtime(7)>=2&&movecontact
trigger7 = stateno=240&&animelemtime(4)>=1&&movecontact
trigger8 = stateno=241&&animelemtime(5)>=1&&movecontact
trigger9 = stateno=250&&movecontact
trigger10= stateno=251&&animelemtime(3)>=1&&movecontact
trigger11= stateno=260&&animelemtime(7)>=3&&movecontact
trigger12= stateno=400&&animelemtime(4)>=1&&movecontact
trigger13= stateno=410&&animelemtime(2)>=1&&movecontact
trigger14= stateno=420&&animelemtime(4)>=1&&movecontact
trigger15= stateno=421&&movecontact
trigger16= stateno=430&&animelemtime(2)>=1&&movecontact
trigger17= stateno=440&&animelemtime(3)>=1&&movecontact
trigger18= stateno=1205&&movecontact
trigger19= stateno=1400&&animelemtime(9)>=1&&movecontact

;---------------------------------------------------------------------------
; RETROMUTAGEN RAY SUPER
[State -1, RETROMUTAGEN RAY]
type = ChangeState
value = 3010
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = (command="SUPER")&&power>=1000
triggerall = command!= "holddown"
triggerall = command!= "HYPER"
triggerall =statetype!=A
trigger1 =statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&animelemtime(4)>=1&&movecontact
trigger4 = stateno=220&&animelemtime(4)>=1&&movecontact
trigger5 = stateno=230&&animelemtime(2)>=1&&movecontact
trigger6 = stateno=231&&animelemtime(7)>=2&&movecontact
trigger7 = stateno=240&&animelemtime(4)>=1&&movecontact
trigger8 = stateno=241&&animelemtime(5)>=1&&movecontact
trigger9 = stateno=250&&movecontact
trigger10= stateno=251&&animelemtime(3)>=1&&movecontact
trigger11= stateno=260&&animelemtime(7)>=3&&movecontact
trigger12= stateno=400&&animelemtime(4)>=1&&movecontact
trigger13= stateno=410&&animelemtime(2)>=1&&movecontact
trigger14= stateno=420&&animelemtime(4)>=1&&movecontact
trigger15= stateno=421&&movecontact
trigger16= stateno=430&&animelemtime(2)>=1&&movecontact
trigger17= stateno=440&&animelemtime(3)>=1&&movecontact
trigger18= stateno=1205&&movecontact
trigger19= stateno=1400&&animelemtime(9)>=1&&movecontact
;---------------------------------------------------------------------------
; VORPAL CUTTER SUPER
[State -1, VORPAL CUTTER]
type = ChangeState
value = 3100
triggerall = !AIlevel&&power>=1000 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = command ="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!= "holddown"
triggerall =!(command="QCB_a"&&command="QCB_b"&&command="QCB_c")
triggerall = command!="FOOT4"&&command!="FOOT6"
trigger1 = statetype!=A
trigger1 = ctrl
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger7 = stateno=231&&animelemtime(7)>=2&&movecontact
trigger8 = stateno=240&&movecontact
trigger9 = stateno=241&&movecontact
trigger10= stateno=250&&movecontact
trigger11= stateno=251&&movecontact
trigger12= stateno=260&&animelemtime(7)>=3&&movehit;contact
trigger13= stateno=400&&animelemtime(4)>=1&&movecontact
trigger14= stateno=410&&animelemtime(2)>=1&&movecontact
trigger15= stateno=420&&animelemtime(4)>=1&&movecontact
trigger16= stateno=421&&movecontact
trigger17= stateno=430&&animelemtime(2)>=1&&movecontact
trigger18= stateno=440&&animelemtime(3)>=1&&movecontact
trigger19= stateno=1205&&movecontact
trigger20= stateno=1400&&animelemtime(9)>=1&&movecontact
;---------------------------------------------------------------------------
;
[State -1, SUPER3]
type = ChangeState
value =ifelse((prevstateno=55&&time<=20||stateno=56&&time<=14||prevstateno=56&&time<=20),1020,3200)
triggerall = !AIlevel&&command= "SUPER" && power>=1000 
triggerall!= command= "DiveKick"
triggerall!= command= "EX_DiveKick"
triggerall= statetype!=S&&statetype!=C
trigger1 = statetype =A
trigger1 = ctrl
trigger2 = (stateno=[600,651])&&movecontact
;=============================================================
;SPECIALs
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; ENERGY WAVE
[State -1, ENERGY WAVE]
type = ChangeState
value = ifelse(((command="EX_BLAST"||command="EX_BLAST2"||command!="EX_BLAST3")&&power<500),1000,1000)
triggerall = !AIlevel 
triggerall = var(13)=0&&numhelper(3301)=0&&numhelper(1001)=0
triggerall = (command="QCF_x"||command="QCF_y"||command="QCF_z")
;triggerall = (command!="EX_BLAST"&&command!="EX_BLAST2"&&command!="EX_BLAST3")
triggerall = command!= "SUPER"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&animelemtime(3)>=1&&movecontact
trigger10= stateno=260&&animelemtime(7)>=3&&movecontact
trigger11= stateno=400&&animelemtime(4)>=1&&movecontact
trigger12= stateno=410&&animelemtime(2)>=1&&movecontact
trigger13= stateno=420&&animelemtime(4)>=1&&movecontact
trigger14= stateno=421&&movecontact
trigger15= stateno=430&&animelemtime(2)>=1&&movecontact
trigger16= stateno=440&&animelemtime(3)>=1&&movecontact
;---------------------------------------------------------------------------
; EX ENERGY WAVE 
[State -1,EX ENERGY WAVE]
type = ChangeState
value = 1000
triggerall = !AIlevel 
triggerall = var(13)=0&&numhelper(3301)=0
triggerall = numhelper(1001)=0&&numhelper(1012)=0&&numhelper(1022)=0
triggerall = (command="EX_BLAST"||command="EX_BLAST2"||command="EX_BLAST3")
triggerall = command!= "SUPER"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&animelemtime(3)>=1&&movecontact
trigger10= stateno=260&&animelemtime(7)>=3&&movecontact
trigger11= stateno=400&&animelemtime(4)>=1&&movecontact
trigger12= stateno=410&&animelemtime(2)>=1&&movecontact
trigger13= stateno=420&&animelemtime(4)>=1&&movecontact
trigger14= stateno=421&&movecontact
trigger15= stateno=430&&animelemtime(2)>=1&&movecontact
trigger16= stateno=440&&animelemtime(3)>=1&&movecontact
;---------------------------------------------------------------------------
; SHURIKEN
[State -1, SHURIKEN]
type = ChangeState
value = 1010
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = numhelper(1001)=0&&numhelper(1011)=0&&numhelper(1022)=0
triggerall = command ="z+c"
triggerall = command!= "SUPER"
triggerall =statetype!=A
trigger1 =statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&animelemtime(3)>=1&&movecontact
trigger10= stateno=400&&animelemtime(4)>=1&&movecontact
trigger11= stateno=410&&animelemtime(2)>=1&&movecontact
trigger12= stateno=420&&animelemtime(4)>=1&&movecontact
trigger13= stateno=430&&animelemtime(2)>=1&&movecontact
trigger14= stateno=440&&animelemtime(3)>=1&&movecontact
;---------------------------------------------------------------------------
; GAUNTLET BLUR
[State -1, GAUNTLET BLUR]
type = ChangeState
value = 1200
triggerall = !AIlevel 
triggerall = var(13)=0&&numhelper(3301)=0
triggerall = command="GAUNTLET"
triggerall = command!="EX_BLAST"&&command!="EX_BLAST2"&&command!="EX_BLAST3"
triggerall = command!="holddown"
triggerall = command!= "SUPER"
trigger1 =statetype!=A
trigger1 = ctrl
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&movecontact
trigger10= stateno=260&&animelemtime(7)>=3&&movecontact
trigger11= stateno=400&&movecontact
trigger12= stateno=410&&movecontact
trigger13= stateno=420&&movecontact
trigger14= stateno=430&&movecontact
trigger15= stateno=440&&movecontact

;---------------------------------------------------------------------------
; TSUKI GIRI (SEN NO SEN)
[State -1, TSUKI GIRI]
type = ChangeState
value = 1300
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall= numhelper(1001)=0
triggerall =(command="QCB_a"||command="QCB_b"||command="QCB_c")
triggerall =(command!="QCF_a"&&command!="QCF_b"&&command!="QCF_c")
triggerall = command!="FOOT3"&&command!="FOOT4"&&command!="FOOT6"
triggerall = command!= "SUPER2"
triggerall = command!= "SUPER3"
trigger1 =statetype!=A
trigger1 = ctrl
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&anim=250&&movecontact
trigger9 = stateno=250&&anim=252&&animelemtime(9)>=1
trigger10= stateno=251&&movecontact
trigger11= stateno=260&&animelemtime(7)>=3&&movecontact
trigger12= stateno=400&&movecontact
trigger13= stateno=410&&movecontact
trigger14= stateno=420&&movecontact
trigger15= stateno=430&&movecontact
trigger16= stateno=440&&movecontact
;---------------------------------------------------------------------------
; AURA CRUSHER
[State -1, AURA CRUSHER]
type = ChangeState
value = 1400
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall= numhelper(1001)=0
triggerall =(command="QCB_x"||command="QCB_y"||command="QCB_z")
triggerall =(command!="QCF_x"&&command!="QCF_y"&&command!="QCF_z")
triggerall = command!= "SUPER"
triggerall = command!= "HYPER"
trigger1 =statetype!=A
trigger1 = ctrl
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&movecontact
trigger10= stateno=260&&animelemtime(7)>=2&&movecontact
trigger11= stateno=400&&movecontact
trigger12= stateno=410&&movecontact
trigger13= stateno=420&&movecontact
trigger14= stateno=430&&movecontact
trigger15= stateno=440&&movecontact
;---------------------------------------------------------------------------
; FOOT SOLDIERS
[State -1, FOOT SOLDIERS]
type = ChangeState
value = 1600
triggerall = !AIlevel 
triggerall = var(17)=0&&power>=500
triggerall = var(13)=0&&numhelper(3301)=0&&numhelper(1601)=0
triggerall = (command="FOOT"||command="FOOT2"||command="FOOT3"||command="FOOT4"||command="FOOT5"||command="FOOT6")
triggerall = command!= "HYPER"
triggerall = command!= "SUPER3"
triggerall = command!= "SUPER2"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl
trigger2 = (stateno=200&&anim=205&&animelemtime(3)>=1)||(stateno=200&&anim=200&&animelemtime(4)>=1)
trigger2 = movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&movecontact
trigger9 = stateno=251&&animelemtime(3)>=1&&movecontact
trigger10= stateno=260&&animelemtime(7)>=3&&movecontact
trigger11= stateno=400&&animelemtime(4)>=1&&movecontact
trigger12= stateno=410&&animelemtime(2)>=1&&movecontact
trigger13= stateno=420&&animelemtime(4)>=1&&movecontact
trigger14= stateno=421&&movecontact
trigger15= stateno=430&&animelemtime(2)>=1&&movecontact
trigger16= stateno=440&&animelemtime(3)>=1&&movecontact
;---------------------------------------------------------------------------
; Dive Kick
[State -1, Dive Kick]
type = ChangeState
value = 1020
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0&&var(18)=0 && var(19)=0
triggerall = command = "DiveKick"||command ="z+c"
triggerall= pos y <= -40
triggerall = statetype!=S
trigger1 =   statetype!=C
trigger1 = ctrl
trigger2 = stateno=600&&movecontact
trigger3 = stateno=610&&movecontact
trigger4 = stateno=620&&movecontact
trigger5 = stateno=630&&movecontact
trigger6 = stateno=640&&movecontact
;------------------------------------
;====================================
;------------------------------------
;Guard Push
[State -1]
type = ChangeState
value = 720
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = var(10) != 1&&command = "guardpush"&&statetype = S&&p2life!=0
trigger1 = stateno = [150,153]
;-------------------------------------
[State -1]
type =ChangeState
value = 725
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = var(10) != 1&&command = "guardpush"&&statetype = C&&p2life!=0
trigger1 = stateno = [150,153]
;-------------------------------------
[State -1]
type =ChangeState
value = 730 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = var(10) != 1&&command = "guardpush"&&statetype = A&&p2life!=0
trigger1 = stateno = [154,155]
;---------------------------------------------------------------------------
; Levitating Dodge Forward
[State -1, Levitating Dodge Forward]
type = ChangeState
value = 700
;triggerall = !AIlevel 
triggerall = numhelper(715)!=1
triggerall = command = "x+a"&&command="holddown" ||command="x+a" && command!="holddown" 
triggerall = command != "holdback"
trigger1 = statetype!=A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Levitating Dodge Back
[State -1, Levitating Dodge Back]
type = ChangeState
value = 710
;triggerall = !AIlevel 
triggerall = numhelper(715)!=1
triggerall = command = "holdback" && (command = "x+a")
triggerall = command != "holdfwd"
triggerall = command != "holddown"
trigger1 = statetype!=A
trigger1 = ctrl
;trigger2 = anim=21&&command = "holdback"
;trigger2 = command = "x+a"
;===========================================================================
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; Run Fwd
[State -1, Run Fwd]
type = ChangeState
value = 100
triggerall = var(13)=0&& numhelper(3301)=0; NOT SUPER SHREDDER MODE
triggerall = !AIlevel 
trigger1 = command = "FF"
trigger1 = statetype!=A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Run Back
[State -1, Run Back]
type = ChangeState
value = 105
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
trigger1 = command = "BB"
trigger1 = statetype!=A
trigger1 = ctrl

;==============
; Jump
;===============
[State -1, Jump]
type = ChangeState
value = 40
triggerall = var(13)=0&&numhelper(3301)=0 
triggerall = (command = "up"||command ="upfwd"||command = "upback")&&command!="super jump"
trigger1 = statetype != A
trigger1 = ctrl = 1
;==============
; Super Jump
;===============
[State -1, Super Jump]
type = ChangeState
value = 55
triggerall = var(13)=0&& numhelper(3301)=0 
triggerall = command = "super jump"
trigger1 = statetype != A
trigger1 = ctrl = 1
;---------------------------------------------------------------------------
; Throw
[State -1, Throw]
type = ChangeState
value = 800
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "y" || command = "z"
triggerall = statetype!=A
triggerall = statetype!=C
triggerall = ctrl
triggerall = stateno != 100
trigger1 = command = "holdfwd"
trigger1 = p2bodydist X < 10
trigger1 = (p2statetype != A)
trigger1 = p2movetype != H
trigger2 = command = "holdback"
trigger2 = p2bodydist X < 10
trigger2 = (p2statetype != A)
trigger2 = p2movetype != H
;---------------------------------------------------------------------------
; Throw
[State -1, Throw]
type = ChangeState
value = 810
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "b"||command = "c"
triggerall = statetype!=A
triggerall = statetype!=C
triggerall = ctrl
triggerall = stateno != 100
trigger1 = command = "holdfwd"
trigger1 = p2bodydist X < 10
trigger1 = (p2statetype != A)
trigger1 = p2movetype != H
trigger2 = command = "holdback"
trigger2 = p2bodydist X < 10
trigger2 = (p2statetype != A)
trigger2 = p2movetype != H
;===========================================================================
;---------------------------------------------------------------------------
; Taunt
[State -1, Taunt]
type = ChangeState
value = 195
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "s"
trigger1 = statetype != A
trigger1 = ctrl
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=230&&movecontact
trigger5 = stateno=240&&movecontact
trigger6 = stateno=241&&movecontact
trigger7 = stateno=250&&movecontact
trigger7 = animelemtime(10)>=1
;---------------------------------------------------------------------------
; Stand Light Punch
[State -1, Stand Light Punch]
type = ChangeState
value = 200
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "x"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_x"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl || (stateno=[100,101])
trigger2 = stateno=220&&movecontact
;---------------------------------------------------------------------------
; Stand Medium Punch
[State -1, Stand Medium Punch]
type = ChangeState
value = 210
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "y"
triggerall = command!="b"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_y"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=230&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=240&&movecontact
trigger6 = stateno=241&&movecontact
trigger7 = stateno=400&&movecontact
trigger8 = stateno=410&&movecontact
trigger9 = stateno=430&&movecontact
trigger10= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Stand Strong Punch
[State -1, Stand Strong Punch]
type = ChangeState
value = 220
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "z"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_z"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl || (stateno=[100,101])
trigger2 = numhelper(216)<=1
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=230&&movecontact
trigger5 = numhelper(216)<=1
trigger5 = stateno=240&&movecontact
trigger6 = numhelper(216)<=1
trigger6 = stateno=241&&movecontact
trigger7 = numhelper(216)<=1
trigger7 = stateno=250&&anim=250&&movecontact
trigger7 = animelemtime(9)>=1
trigger8 = numhelper(216)<=1
trigger8 = stateno=400&&movecontact
trigger9 = numhelper(216)<=1
trigger9 = stateno=410&&movecontact
trigger10= stateno=430&&movecontact
trigger11= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = ifelse((numhelper(242)=0&&p2bodydist X >= 10&&command="holdfwd"||(stateno=[100,101])&&command="holdback"||(prevstateno=[100,101])&&command="holdback"),241,ifelse((numhelper(242)>0&&p2bodydist x >=30),251,230))
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "a"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_a"
triggerall = command != "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=202&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=201&&movecontact
trigger6 = stateno=210&&movecontact
trigger7 = stateno=400&&movecontact
trigger8 = stateno=410&&movecontact
trigger9 = stateno=420&&movecontact
trigger10= stateno=430&&movecontact
trigger11= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Stand Light Kick 2
[State -1, Stand Light Kick 2]
type = ChangeState
value = ifelse((numhelper(232)=0),231,240)
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = numhelper(232)=0
triggerall = command = "b"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_b"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= (stateno=[100,101])
;---------------------------------------------------------------------------
; Stand Light Kick 2
[State -1, Stand Light Kick 2]
type = ChangeState
value = ifelse((var(18)<=0&&var(19)<=0&&hitcount<=3&&numhelper(232)=0&&numhelper(242)=0||var(18)<=0&&var(19)<=0&&prevstateno=251),231,ifelse((var(18)<=0&&var(19)<=0&&random<=500||var(18)<=0&&var(19)<=0&&random>500&&Enemynear(0),Pos Y=0)||(var(18)>=1)||(var(19)>=1),251,260))
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = numhelper(232)=0
triggerall = command = "y+b"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_b"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1 = ctrl
trigger2= (stateno=[200,230])&&movecontact
trigger3= (stateno=[240,241])&&movecontact
trigger4= (stateno=[400,420])&&movecontact
trigger5= (stateno=[430,440])&&movecontact
;---------------------------------------------------------------------------
; Stand Front Boot Kick
[State -1, Front Boot Kick]
type = ChangeState
value = 251
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "a" 
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_a"
triggerall = command!= "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1 =  stateno=230&&movehit&&numhelper(242)>0||stateno=241 && movehit

; Stand Front Boot Kick
[State -1, Front Boot Kick]
type = ChangeState
value = 251
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "QCF_c"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_c"
triggerall = Pos Y = 0
trigger1 =  statetype!= A
trigger1 = ctrl 
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=250&&numtarget(252)=0&&movecontact
trigger8 = stateno=400&&movecontact
trigger9 = stateno=410&&movecontact
trigger10= stateno=420&&movecontact
trigger11= stateno=430&&movecontact
trigger12= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Standing Medium Kick
[State -1, Standing Medium Kick]
type = ChangeState
value = ifelse((numtarget&&numhelper(243)>=1||numtarget&&numhelper(242)>=1||p2bodydist X >= 10&&command="holdback"),260,ifelse((numhelper(243)=0||!numtarget&&numhelper(243)>=1||numhelper(242)=0&&p2bodydist X >= 10&&command="holdfwd"),240,240))
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "b"
triggerall = command!= "QCF_b"
triggerall = command!="y"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_b"
triggerall = command != "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl ||numhelper(232)=1&&(stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=400&&movecontact
trigger7 = stateno=410&&movecontact
trigger8 = stateno=430&&movecontact
trigger9 = stateno=440&&movecontact
;---------------------------------------------------------------------------
; Standing Medium Kick 2
[State -1, Standing Medium Kick 2]
type = ChangeState
value = 260
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "QCF_b"
triggerall = command!="y"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_b"
triggerall = Pos Y = 0
trigger1 =  statetype!= A
trigger1 = ctrl 
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=400&&movecontact
trigger7 = stateno=410&&movecontact
trigger8 = stateno=430&&movecontact
trigger9 = stateno=440&&movecontact
;---------------------------------------------------------------------------
; Standing Strong Kick
[State -1, Standing Strong Kick]
type = ChangeState
value = 250 
;ifelse((!numtarget&&p2bodydist X >= 10&&command="holdfwd"||numtarget&&command="holdfwd"||(stateno=[100,101])||prevstateno=100||prevstateno=101),251,ifelse((!numtarget&&p2bodydist X >= 10&&command="holdback"||numtarget&&command="holdback"),251,250))
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "c"
triggerall = command!="SUPER2"
triggerall = command!="SUPER3"
triggerall = command!="QCB_c"
triggerall = command != "holddown"
trigger1 =  statetype!= A||statetype!=C
trigger1 =  statetype = S
trigger1= ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=400&&movecontact
trigger9 = stateno=410&&movecontact
trigger10= stateno=420&&movecontact
trigger11= stateno=430&&movecontact
trigger12= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Crouching Light Punch
[State -1, Crouching Light Punch]
type = ChangeState
value = 400
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "x"&&command = "holddown"
triggerall = command!="GAUNTLET"
triggerall = command!="EX_BLAST"
triggerall = command!="QCF_x"&&command!="QCB_x"
triggerall = command!="SUPER"
triggerall = Pos Y=0
trigger1 =  statetype!= A||statetype!=S
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=400&&movecontact
;---------------------------------------------------------------------------
; Crouching Medium Punch
[State -1, Crouching Medium Punch]
type = ChangeState
value = 410
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "y"&&command = "holddown"
triggerall = command!="b"
triggerall = command!="GAUNTLET"
triggerall = command!="EX_BLAST2"
triggerall = command!="QCF_y"&&command!="QCB_y"
triggerall = command!="SUPER"
triggerall = Pos Y=0
trigger1 =  statetype!= A||statetype!=S
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=400&&movecontact
trigger9 = stateno=430&&movecontact
trigger10= stateno=440&&movecontact

;---------------------------------------------------------------------------
; Crouching Strong Punch
[State -1, Crouching Strong Punch]
type = ChangeState
value = 420
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "z"&&command = "holddown"
triggerall = command!="GAUNTLET"
triggerall = command!="EX_BLAST3"
triggerall = command!="QCF_z"
triggerall = command!="QCB_z"
triggerall = command!="SUPER"
triggerall = Pos Y=0
trigger1 =  statetype!= A||statetype!=S
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&anim=250&&movecontact
trigger9 = stateno=400&&movecontact
trigger10= stateno=410&&movecontact
trigger11= stateno=430&&movecontact
trigger12= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Crouching Strong Punch
[State -1, Crouching Strong Punch]
type = ChangeState
value = 421
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = stateno=420&&movecontact
triggerall = command = "z"&&command = "holddown"
triggerall = command!="GAUNTLET"
triggerall = command!="EX_BLAST3"
triggerall = command!="QCF_z"
triggerall = command!="QCB_z"
triggerall = command!="SUPER"
trigger1   =  statetype!= A
;---------------------------------------------------------------------------
; Crouching Light Kick
[State -1, Crouching Light Kick]
type = ChangeState
value = 430
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "a"
triggerall = command!="SUPER3"
triggerall = command = "holddown"
triggerall = command!="HYPER"
triggerall = command!="QCF_a"
triggerall = command!="QCB_a"
triggerall = Pos Y=0
trigger1 =  statetype!= A
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=400&&movecontact
trigger9 = stateno=410&&movecontact
trigger10= stateno=430&&time>=4&&movecontact
;---------------------------------------------------------------------------
; Crouching Medium Kick
[State -1, Crouching Medium Kick]
type = ChangeState
value = 440
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "b"&&command = "holddown"
triggerall = command!="y"
triggerall = command!="QCF_b"
triggerall = command!="QCB_b"
triggerall = command!="SUPER3"
triggerall = Pos Y=0
trigger1 =  statetype!= A||statetype!=S
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=400&&movecontact
trigger9 = stateno=410&&movecontact
trigger10= stateno=420&&movecontact
trigger11= stateno=430&&movecontact
;---------------------------------------------------------------------------
; Crouching Strong Kick
[State -1, Crouching Strong Kick]
type = ChangeState
value = 450
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = !AIlevel 
triggerall = command = "c"&&command = "holddown"
triggerall = command!="QCF_c"
triggerall = command!="QCB_c"
triggerall = command!="SUPER3"
triggerall = command!="HYPER"
triggerall = Pos Y=0
trigger1 =  statetype!= A||statetype!=S
trigger1 = ctrl || (stateno=[100,101])
trigger2 = stateno=200&&movecontact
trigger3 = stateno=210&&movecontact
trigger4 = numhelper(216)<=1
trigger4 = stateno=220&&movecontact
trigger5 = stateno=230&&movecontact
trigger6 = stateno=240&&movecontact
trigger7 = stateno=241&&movecontact
trigger8 = stateno=250&&anim=250&&animelemtime(4)>=1&&movehit
trigger9 = stateno=400&&movecontact
trigger10= stateno=410&&movecontact
trigger11= stateno=420&&movecontact
trigger12= stateno=430&&movecontact
trigger13= stateno=440&&movecontact
;---------------------------------------------------------------------------
; Jump Light Punch
[State -1, Jump Light Punch]
type = ChangeState
value = 600
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = command = "x"
trigger1 = statetype!=S&&statetype!=C
trigger1 = ctrl
trigger2 = pos y <= -40&&stateno=610&&movecontact
trigger3 = pos y <= -40&&stateno=630&&movecontact
trigger4 = pos y <= -40&&stateno=640&&movecontact
;---------------------------------------------------------------------------
; Jump Medium Punch
[State -1, Jump Medium Punch]
type = ChangeState
value = 610
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = command = "y"
trigger1 = statetype!=S&&statetype!=C
trigger1 = ctrl
trigger2 = pos y <= -40&&stateno=600&&movecontact
trigger3 = pos y <= -50&&stateno=620&&movecontact
trigger4 = pos y <= -40&&stateno=630&&movecontact
trigger5 = pos y <= -40&&stateno=640&&movecontact

; Jump Medium Punch2
[State -1, Jump Medium Punch2]
type = ChangeState
value = 611
triggerall = !AIlevel
triggerall = var(13)=0&& numhelper(3301)=0
triggerall=Pos Y<=-70
triggerall=anim=610&&animelemtime(3)>=1&&movecontact
triggerall= command="y"&&command != "holddown"
trigger1 = statetype!=S&&statetype!=C
trigger1 = ctrl
;---------------------------------------------------------------------------
; Jump Strong Punch
[State -1, Jump Strong Punch]
type = ChangeState
value = ifelse((numhelper(622)>0||numhelper(622)>=0&&command="holddown"),621,620)
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = command = "z"
trigger1 = statetype!=S&&statetype!=C
trigger1 = ctrl
trigger2 = stateno=600&&movecontact
trigger3 = stateno=610&&movecontact
trigger4 = stateno=611&&movecontact
trigger5 = stateno=630&&movecontact
trigger6 = stateno=640&&movecontact

;---------------------------------------------------------------------------
; Jump Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 630
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = command = "a"
trigger1 = statetype!=S
trigger1 = ctrl
trigger2 = pos y <= -40&&stateno=600&&movecontact
trigger3 = pos y <= -40&&stateno=610&&movecontact
trigger4 = pos y <= -40&&stateno=611&&movecontact
trigger5 = pos y <= -50&&stateno=620&&movecontact
trigger6 = pos y <= -40&&stateno=640&&movecontact

;---------------------------------------------------------------------------
; Jump Medium Kick
[State -1, Jump Medium Kick]
type = ChangeState
value = 640
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = pos y <= -40
triggerall = command = "b"
trigger1 = statetype!=S
trigger1 = ctrl
trigger2 = pos y <= -40&&stateno=600&&movecontact
trigger3 = pos y <= -40&&stateno=610&&movecontact
trigger4 = pos y <= -40&&stateno=611&&movecontact
trigger5 = pos y <= -50&&stateno=620&&movecontact
trigger6 = pos y <= -40&&stateno=630&&movecontact
;---------------------------------------------------------------------------
; Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 650
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall=pos y <= -50
triggerall=command!="holdfwd"
triggerall=command!="holddown"
triggerall=command!= "SUPER3"
triggerall=command = "c"
trigger1 = statetype!= S
trigger1 = ctrl
trigger2 = stateno=600&&movecontact
trigger3 = stateno=610&&movecontact
trigger4 = stateno=611&&movecontact
trigger5 = stateno=620&&movecontact
trigger6 = stateno=630&&movecontact
trigger7 = stateno=640&&movecontact
;------------------------------------
; Jump Strong Kick2
[State -1, Jump Strong Kick2]
type = ChangeState
value = 660
triggerall = !AIlevel 
triggerall = var(13)=0&& numhelper(3301)=0
triggerall = pos y <= -50
triggerall = command="fwd_c"||command="c"&&command="holdfwd"
triggerall = command!="z"
triggerall = command!= "DiveKick"
triggerall = command!= "SUPER2"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno=600&&movecontact
trigger3 = stateno=610&&movecontact
trigger4 = stateno=611&&movecontact
trigger5 = stateno=620&&movecontact
trigger6 = stateno=630&&movecontact
trigger7 = stateno=640&&movecontact
;---------------------------------------------------------------------------
; SUPER SHREDDER Stand Light Punch
[State -1, Stand Light Punch]
type = ChangeState
value = 33200
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = !AIlevel 
triggerall = command = "x"
triggerall = command!= "a"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_x"
trigger1 =  statetype!= A
trigger1= ctrl

; SUPER SHREDDER Stand Medium Punch
[State -1, Stand Medium Punch]
type = ChangeState
value = 33210
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = !AIlevel 
triggerall = command = "y"
triggerall = command!= "b"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_y"
trigger1 =  statetype!= A
trigger1= ctrl

; SUPER SHREDDER Stand Heavy Punch
[State -1, Stand Heavy Punch]
type = ChangeState
value = 33220
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = !AIlevel 
triggerall = command = "z"
triggerall = command!= "c"
triggerall = command!="GAUNTLET"
triggerall = command!="QCF_z"
trigger1 =  statetype!= A
trigger1= ctrl
;---------------------------------------------------------------------------
; SUPER SHREDDER Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = 33230
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0 
triggerall = command = "a"
triggerall = command!= "x"
triggerall = command!= "SUPER3"
trigger1 =  statetype!= A
trigger1= ctrl

; SUPER SHREDDER Stand Medium Kick
[State -1, Stand Medium Kick]
type = ChangeState
value = 33240
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0 
triggerall = command = "b"
triggerall = command!= "y"
triggerall = command!= "SUPER3"
trigger1 =  statetype!= A
trigger1= ctrl

; SUPER SHREDDER Stand Heavy Kick
[State -1, Stand Medium Kick]
type = ChangeState
value = 33250
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0 
triggerall = command = "c"
triggerall = command!= "z"
triggerall = command!= "SUPER3"
trigger1 =  statetype!= A
trigger1= ctrl
;---------------------------------------------------------------------------
; SUPER SHREDDER ENERGY FLAME FLOOR
[State -1, ENERGY FLAME FLOOR]
type = ChangeState
value = 33300
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = (command="QCF_x")
triggerall = command!="GAUNTLET"
triggerall = command!= "SUPER"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl

; SUPER SHREDDER ENERGY RETROMUTAGEN BLAST
[State -1, ENERGY RETROMUTAGEN BLAST]
type = ChangeState
value = 33310
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = (command="QCF_y")
triggerall = command!="GAUNTLET"
triggerall = command!= "SUPER"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl

; SUPER SHREDDER ENERGY ICE BLAST
[State -1, ENERGY ICE BLAST]
type = ChangeState
value = 33320
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0
triggerall=  numhelper(33302)<=0
triggerall = (command="QCF_z")
triggerall = command!="GAUNTLET"
triggerall = command!= "SUPER"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl

; SUPER SHREDDER GAUNTLET BLUR SUPER
[State -1, GAUNTLET BLUR SUPER]
type = ChangeState
value = 33380
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = stateno!=33380
triggerall =  numhelper(33302)<=0
triggerall = (command= "SUPER"||command ="GAUNTLET" ||command = "x" && command ="GAUNTLET" ||command = "y" && command ="GAUNTLET"||command = "z" && command ="GAUNTLET")
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl

; SUPER SHREDDER LIGHTNING PRESSURE COMBO BREAKER
[State -1, LIGHTNING PRESSURE COMBO BREAKER]
type = ChangeState 
value = 33330;ifelse((random<500),33330,ifelse((BackedgeDist<=60),700,710))
triggerall = !AIlevel
triggerall = Alive
triggerall = (stateno=[0,20])||(stateno=[33200,33250])||(stateno=[33300,33320])&&numexplod(3303)=0
triggerall = (stateno!=[700,710])&&(stateno!=33330)&&(stateno!=33360)
triggerall = var(13)>0&& numhelper(3301)>0
triggerall =statetype!=A
triggerall = statetype=S
trigger1 = ctrl
trigger1 = (command="z+c"||command="s")
trigger2 = EnemyNear(0),hitcount>15
trigger2 = EnemyNear(0), HitDefAttr = SCA, NA, NP||EnemyNear(0), HitDefAttr = SCA, SA, SP||EnemyNear(0), HitDefAttr = SCA, HA, HP
trigger2 = (helper(3301),movetype=H)||(helper(3301),gethitvar(damage))
ignorehitpause=1

; SUPER SHREDDER THUNDER WAVE SUPER
[State -1, THUNDER WAVE SUPER]
type = ChangeState
value = 33360
triggerall = !AIlevel
triggerall = var(13)>0&& numhelper(3301)>0
triggerall = command= "SUPER3"
triggerall = command!="SUPER"
triggerall = command!="SUPER2"
triggerall = statetype!=A
trigger1 = statetype=S
trigger1 = ctrl

;---------------------------------------------------------------------------
