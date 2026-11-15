;---------------------------------------------------------------------------
; Configuration
[Statedef 5901]
type = S

;Character Setting
;
; var(57) = Set to 1 to have inifinte Super Shredder mode timer. Timer never depletes. 
; var(58) = Set to 1 to automatically begin in Super Shredder mode in the Final Round. 
; var(59) = Set value to play as Super Shredder by default- negates all other settings.



[State 5901, INFINITE SUPER SHREDDER TIMER] 
type = VarSet
trigger1 = 1
v = 57
value = 0 ;Set to 1 to have infinite Super Shredder timer. Defaults to 0. 


[State 5901, FINAL ROUND START AS SUPER SHREDDER] 
type = VarSet
trigger1 = 1
v = 58
value = 0 ;Set to 1 to begin in Super Shredder mode in Final Round. Defaults to 0. 


[State 5901, ALWAYS SUPER SHREDDER] 
type = VarSet
trigger1 = 1
v = 59
value = 0 ;Set value to play as Super Shredder by default. (Negates previous settings if set to 1)
          ; Defaults to 0. 


;Don't Change
[State 5901, 3] 
type = ChangeState
trigger1 = roundno = 1                                             ;Intro for round 1
trigger2 = Var(54)>=1&&var(58)=1&&RoundsExisted >=2 && roundno>=2  ;Intro for round 2 and up
value = 190

;Don't Change
[State 5901,4]
type = PowerSet
triggerall=var(56)=1&&var(59)=0
trigger1=1
value=0
ignorehitpause=1
persistent=0

;Don't Change
[State 5901,4]
type = VarSet
triggerall=1
trigger1=var(56)=2
v = 13
value=4000
ignorehitpause=1
persistent=0

;Don't Change
[State 5901, 5] 
type = ChangeAnim
triggerall= fvar(38) = 1&&prevstateno=197&&stateno=0  ;Change to Splinter Captured Anim
trigger1=1
value = 180
elem=4


;Don't Change
[State 5901, 5] 
type = ChangeAnim
trigger1 = var(59) = 1&&roundno >=2   ;Change to SUPER SHREDDER anim for round 2 and up
trigger2 = Var(54)>=1 && var(58)=1 && RoundsExisted >=2&& roundno>=2
value = 3301
