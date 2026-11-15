;
; 1. 按键定义
; ---------------------
; 注意: 按键和招式名分大小写。
; 八个方向分别是:
;   B, DB, D, DF, F, UF, U, UB     (全大写)
;   对应后，下后，下，下前，前，前上，上，上后。
; 六个按键是:
;   a, b, c, x, y, z               (全小写)
;   在默认按键的情况下，xyz在上排，abc在下排。
;   推荐使用xyz作为拳，abc作为脚。
;
; 每一个[Command]定义一个操作指令。
; 这些操作指令可以在cmd和cns里被调用。
; 操作指令的语法规范如下:
;
;   [Command]
;   name = "指令名"
;   command = 按键输入
;   time = 接受指令输入的时间 (可选)
;   buffer.time = 输入缓存的时间 (可选)
;
; - 指令名
;   指令的名字，在调用时需要输入同样的名字，比如trigger1=command="指令名"。
;   指令名区分大小写。(QCB_a和Qcb_a或者QCB_A不同)。
;
; - 按键输入
;   输入的按键的列表。每一个键由逗号隔开。一个方向键或者一个攻击键叫为一个符号。
;   方向键和攻击键之前可以用特殊符号来达到一些效果:
;   斜杠 (/) - 表示之后的一个键必须被按住不放
;          举例, command = /D       ;按住不放下方向键
;               command = /DB, a   ;按住不放下后方向键的时候按a
;   波浪号 (~) - 表示按键被松开
;          举例, command = ~a       ;松开a键
;               command = ~D, F, a ;松开下方向键，按前方向键，再按a
;          如果你想让某个键蓄力一段时间再放开，可以再波浪号之后加入你想保持蓄力的时间(以帧为单位)
;          举例, command = ~30a     ;按住a30帧，再松开
;   美金 ($) - 仅限上下左右方向键。表示包括正和斜方向
;          举例, command = $D       ;包括下，下后和下前
;               command = $B       ;包括后，下后和上后
;   加号 (+) - 仅限攻击键。表示同时按多个键。
;          举例, command = a+b      ;同时按a和b
;               command = x+y+z    ;同时按x，y和z
;   大于号 (>) - 表示上一次按键和这一次按键之中不能掺杂其他的按键
;          举例, command = a, >~a   ;按下a再松开a，而其中不按下或者松开其他键
;   这些符号可以组合使用:
;     举例, command = ~30$D, a+b     ;按住下，下后或者下前30帧，松开，然后同时按a和b
;
;   注意: 连续按方向键的指令会被MUGEN引擎自动理解如下:
;         举例，cmd文件中的定义:
;           command = F, F
;         会被引擎理解成:
;           command = F, >~F, >F
;
;   对于有多个方向键的定义，例如四分之一圈下前，为了让招数能更容易的使出，最好在定义由一个"松开方向键"起始。
;
; - 指令输入时间 (可选)
;   接受指令输入的时间，以帧为单位。默认值可以在[Defaults]条目修改，通常为15。
;
; - 指令缓存时间 (可选)
;   输入的指令被缓存的时间。当一个指令被输入时，它在这段时间里都是有效的。
;   最基本的情况是设置成值为1。这种情况下只有在这一帧输入指令才会执行。如果值更高，比如3或4，输入会提前进入缓存，然后当可以执行时就被执行。这样人物的操作会松快一些，因为玩家可以提前输入指令，比如在还没有击中敌人时就开始取消，或者从受击状态还没有获得控制时就切反。
;   但这也有副作用，因为在缓存的期间会认为一直在输入这个指令。举例来说，把这个值设成30，然后发一个很快的招式，比如功夫人的站轻拳，看它的效果。
;   默认值可以在[Defaults]条目修改。
;   这个参数对蓄力指令不起作用，参数的值会自动当作1。
;
; 如果有多种输入有同样的名子，每一种输入都会读出这个指令。你可以用这个技巧来让一个招式接受不同的输入。
;
; 以下是一些常用指令的输入示例:
;
; [Command] ;下前 + x
; name = "下前x"
; command = ~D, DF, F, x
;
; [Command] ;向后半圈 + a
; name = "后半圈a"
; command = ~F, DF, D, DB, B, a
;
; [Command] ;下前下前 + y
; name = "下前下前y"
; command = ~D, DF, F, D, DF, F, y
;
; [Command] ;连打b
; name = "连打b"
; command = b, b, b, b, b
; time = 30
;
; [Command] ;蓄后，前 + z
; name = "蓄后前z"
; command = ~60$B, F, z
; time = 10
;
; [Command] ;蓄下，上 + c
; name = "蓄下上c"
; command = ~60$D, U, c
; time = 10


;-| 重新排列按键 |-----------------------------------------------------
; 这一段可以让玩家简单的重新排列攻击按键。格式是:
;  以前对应的键 = 修改后的键
; 如果不填写修改后的键，则以前对应的键将失效。
[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s
;-| 超必杀技 |--------------------------------------------------------
;下面有两个技能是一样的，但是输入不同。
;两种输入都会触发command = 三连功夫掌"。
;为了方便玩家操作，指令接受时间不是默认的15，而是20。
;

;-| 按两次 |-----------------------------------------------------------
[Command]
name = "FF"     ;必须包括 (不要删除)
command = F, F
time = 10

[Command]
name = "BB"     ;必须包括 (不要删除)
command = B, B
time = 10

[Command]
name = "前前"
command = F, F
time = 10

[Command]
name = "后后"
command = B, B
time = 10

[Command]
name = "B"
command = B
time = 1

;-| 同时按键 |-----------------------------------------------
[Command]
name = "recovery";必须包括 (不要删除)
command = x+y
time = 1

[Command]
name = "a+b+c"
command = a+b+c
time = 10

[Command]
name = "x+y+z"
command = x+y+z
time = 10
;-| 方向＋攻击键 |---------------------------------------------------------
[Command]
name = "下+a"
command = /$D,a
time = 1

[Command]
name = "下+b"
command = /$D,b
time = 1

[Command]
name = "下+x"
command = /$D,x
time = 1

[Command]
name = "下+c"
command = /$D,c
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
name = "fwd_x"
command = /$F,x
time = 1

[Command]
name = "fwd_y"
command = /$F,y
time = 1

[Command]
name = "fwd_s"
command = /$F,s
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
name = "back_x"
command = /$B,x
time = 1

[Command]
name = "back_y"
command = /$B,y
time = 1

[Command]
name = "back_s"
command = /$B,s
time = 1

[command]
name = "下前a"
command = ~D,DF,F,a
time = 15

[command]
name = "下后a"
command = ~D,DB,B,a
time = 15

[command]
name = "下前b"
command = ~D,DF,F,b
time = 15

[command]
name = "下后b"
command = ~D,DB,B,b
time = 15

[command]
name = "下前c"
command = ~D,DF,F,c
time = 15

[command]
name = "下后c"
command = ~D,DB,B,c
time = 15

[command]
name = "下前x"
command = ~D,DF,F,x
time = 15

[command]
name = "下后x"
command = ~D,DB,B,x
time = 15

[command]
name = "下前y"
command = ~D,DF,F,y
time = 15

[command]
name = "下后y"
command = ~D,DB,B,y
time = 15

;-| 单攻击键 |---------------------------------------------------------
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
name = "hold_x"
command = /x
time = 1

[Command]
name = "hold_y"
command = /y
time = 1

[Command]
name = "s"
command = s
time = 1

[Command]
name = "start"
command = s
time = 1

;-| 蓄方向键 |--------------------------------------------------------------
[Command]
name = "holdfwd";必须包括 (不要删除)
command = /$F
time = 1

[Command]
name = "holdback";必须包括 (不要删除)
command = /$B
time = 1

[Command]
name = "holdup" ;必须包括 (不要删除)
command = /$U
time = 1

[Command]
name = "holddown";必须包括 (不要删除)
command = /$D
time = 1

[Command]
name = "蓄上方向"
command = /$F
time = 1

[Command]
name = "蓄后方向"
command = /$B
time = 1

[Command]
name = "蓄前方向"
command = /$U
time = 1

[Command]
name = "up" ;Required (do not remove)
command = $U
time = 1

[Command]
name = "蓄下方向"
command = /$D
time = 1

[Command]
name = "hold_a"
command = /a
time = 1

[Command]
name = "hold_17"
command = /x
time = 17

[Command]
name = "hold_18"
command = /y
time = 1

[Command]
name = "hold_b"
command = /b
time = 10

[Command]
name = "hold_c"
command = /c
time = 1

[Command]
name = "hold_s"
command = /s
time = 1
[Command]
name = "hold_z"
command = /z
time = 1

[Command]
name = "hold_B"
time = 1
command = /B


;---------------------------------------------------------------------------
; 2. state入口
; --------------
; 在这一段里，人物会依据输入来转到相应的state里。
;
; 入口示例如下:
;   [State -1, 标签]           ;标签可以是任意你想要来标注这个入口的名字
;   type = ChangeState          ;不要改
;   value = 要跳转到的state
;   trigger1 = command = "招式名"
;   . . .  (其他trigger)
;
; - 一些常用的trigger:
;   - statetype
;       S, C or A : 现在人物的状态 (站立, 下蹲, 空中)
;   - ctrl
;       0 or 1 : 如果人物可控，则值为1，否则为0。除非取消另一个招数，否则出招是一般要求ctrl=1
;   - stateno
;       现在人物的state号 - 在取消招数时常用。
;   - movecontact
;       0 or 1 : 如果上一个招数接触到了敌人，则值为1，否则为0。在取消招数时常用。
;
; 注意: 入口的顺序很重要。
;   如果指令A是指令B的一部分，则指令B的入口应排在指令A前。
;   比如说，下前下前XY应该排在下前XY之前，下前XY应该排在下前X之前，下前X应该排在X之前。
;
; 关于trigger的详细解释，请参阅MUGEN自带的cns参考说明。
;
; 提示:
; 这部分是cns的延伸。-1这个state是一个特殊state，无论人物实际上在哪个state，-1这个state每一帧都会执行。


; 不要删除下面这行。语法标准要求CMD文件必须包括这行。
[Statedef -1]

;===========================================================================
;---------------------------------------------------------------------------

;===========================================================================


;---------------------------------------------------------------------------
;前跑
[State -1, 前跑]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
triggerall = stateno != 75
value = ifelse(pos y >= 0,60,65)
trigger1 = command = "前前"
trigger1 = ctrl
;---------------------------------------------------------------------------
;后跑
[State -1, 后跑]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = stateno != 60
triggerall = stateno != 65
triggerall = stateno != 70
triggerall = stateno != 75
value = ifelse(pos y >= 0,70,75)
trigger1 = command = "后后"
trigger1 = ctrl
;---------------------------------------------------------------------------
; 六道模式前跑
[State -1, Correr Adelante Rikudou Mode]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11060
trigger1 = command = "前前"
trigger1 = ctrl
;---------------------------------------------------------------------------
; 六道模式后跑
[State -1, Correr Atras Rikudou Mode]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11070
trigger1 = command = "后后"
trigger1 = ctrl
;===========================================================================
; SUPERS:
;===========================================================================
; 威装须佐
[State -1, 威装须佐]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(59) = 0
triggerall = numhelper(12001) = 0
Triggerall = power >= 5000
value = 8000
Triggerall = command = "x"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; 写轮眼:
;===========================================================================
; 豪火球
[State -1, 豪火球]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = numhelper(1001) = 0
Triggerall = power >= 200
value = 1000
Triggerall = command = "下+a"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 龙炎放歌]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1000
value = 1100
Triggerall = command = "下前a"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 灰尘隐]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1500
value = 1200
Triggerall = command = "下后a"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 替身]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = POWER >= 100
value = 3000
trigger1 = numhelper(3001) <= 0
triggerall = command = "c"
Triggerall = stateno = 0
trigger1 = ctrl

[State 0, HitOverride]
type = HitOverride
triggerall = stateno != [6000,6041] ; Susanoo Kage Bunshin
triggerall = stateno != [15000,15999] ; Limbo Clones
trigger1 = numhelper(3001) > 0
attr = SCA,NA,SA,NP,SP
stateno = 3004
time = 5

[State -1, 宇智波反弹]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1000
value = 3100
triggerall = command = "fwd_c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 替身]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
value = 3010
triggerall = POWER >= 50
Trigger1 = command = "c"
trigger1 = movetype = H

[State -1, 豪火灭失]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1500
value = 6100
Triggerall = command = "fwd_b"
Triggerall = statetype = S
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 空中豪火灭失]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1500
value = 6110
Triggerall = command = "y"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 豪火灭却]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 1500
value = 6200
Triggerall = command = "back_b"
Triggerall = statetype = S
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 通灵九尾]
type = ChangeState
triggerall = var(2) = [0,2]
triggerall = var(59) = 0
triggerall = numhelper(12001) = 0
Triggerall = power >= 1500
value = 12000
Triggerall = command = "back_c"
Triggerall = statetype = S
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; EMS SUPERS:
;===========================================================================
[State -1,开启完全体须佐能乎 ]
type = ChangeState
value = 8100
triggerall = var(2) = 1
triggerall = var(59) = 0
triggerall = power >= 5000
triggerall = command = "z"
trigger1 = statetype = S
trigger1 = ctrl
;===========================================================================
; 万花筒:
;===========================================================================

[State -1, 撑杆跳]
type = ChangeState
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = POWER >= 500
value = 2000
triggerall = command = "hold_b"
trigger1 = stateno = 0
trigger1 = ctrl

[State -1, 空中撑杆跳]
type = ChangeState
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
value = 2020
triggerall = command = "b"
Triggerall = statetype = A
trigger1 = ctrl

[State -1,木龙]
type = ChangeState
value = 2100
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = power >= 1500
triggerall = command = "b"
trigger1 = statetype = c
trigger1 = ctrl

[State -1, 须佐]
type = ChangeState
triggerall = POWER >= 800
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = command = "x"
value = 4000
Triggerall = stateno = 0
trigger1 = ctrl

[State -1, 完全体须佐]
type = ChangeState
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
triggerall = POWER >= 2500
value = 4100
triggerall = command = "x"
trigger1 = statetype = C
trigger1 = ctrl

[State -1, 木分身须佐]
type = ChangeState
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = numhelper(6001) = 0
Triggerall = numhelper(6002) = 0
Triggerall = numhelper(6003) = 0
Triggerall = numhelper(6004) = 0
Triggerall = numhelper(6005) = 0
Triggerall = numhelper(6006) = 0
Triggerall = numhelper(6007) = 0
Triggerall = numhelper(6008) = 0
Triggerall = numhelper(6010) = 0
Triggerall = power >= 4000
value = 6000
triggerall = command = "y"
Triggerall = stateno = 0
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 须佐火遁]
type = ChangeState
triggerall = var(2) >= 1
triggerall = var(2) <= 2
triggerall = var(59) = 0
Triggerall = power >= 3000
value = 6300
triggerall = command = "y"
Triggerall = statetype = c
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; Rinnegan SUPERS:
;===========================================================================
[State -1, 地爆天星]
type = ChangeState
triggerall = numhelper(8231) = 0
trigger2 = p2dist x = [300,1000]
trigger2 = p2dist y = [-150,150]
triggerall = var(2) = 2
triggerall = var(59) = 0
Triggerall = power >= 5000
value = 8200
Triggerall = command = "z"
Triggerall = statetype = S
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 天碍震星]
type = ChangeState
Triggerall = var(2) = 2
triggerall = var(59) = 0
Triggerall = power >= 5000
value = 8300
Triggerall = command = "z"
Triggerall = statetype = c
trigger1 = ctrl

[State -1, 超神罗天征]
type = ChangeState
triggerall = POWER >= 5000
triggerall = var(2)= 2
triggerall = var(59) = 0
value = 8400
triggerall = command = "z"
trigger1 = statetype = A
trigger1 = ctrl
;===========================================================================
; 轮回眼:
;===========================================================================
[State -1, 树界降临]
type = ChangeState
value = 2200
trigger1 = command = "fwd_b"
triggerall = var(2) = 2
triggerall = var(59) = 0
triggerall = power >= 2500
Triggerall = statetype != A
triggerall = numhelper(2201) = 0
triggerall = numhelper(2202) = 0
triggerall = numhelper(2203) = 0
triggerall = numhelper(2301) = 0
trigger1 = ctrl

[State -1, 花树界降临]
type = ChangeState
value = 2300
trigger1 = command = "back_b"
triggerall = var(2) = 2
triggerall = var(59) = 0
triggerall = power >= 2500
Triggerall = statetype != A
triggerall = numhelper(2201) != 0
triggerall = numhelper(2202) != 0
triggerall = numhelper(2301) = 1
triggerall = helper(2301), stateno = 2301

[State -1,黑棒]
type = ChangeState
value = 3200
triggerall = var(2) >= 2
triggerall = var(59) = 0
triggerall = command = "fwd_c"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, 封术吸印]
type = ChangeState
triggerall = POWER >= 1000
triggerall = var(2) = 2
triggerall = var(59) = 0
value = 3300
triggerall = command = "back_c"
trigger1 = statetype != A
trigger1 = ctrl

[State -1, 神罗天征]
type = ChangeState
value = cond(enemy, pos y + pos y > -20,4200,4210)
triggerall = command = "fwd_x"
triggerall = stateno != cond(enemy, pos y + pos y > -20,4200,4210)
trigger1 = stateno = 20
triggerall = var(33)<= 0
triggerall = var(2)= 2
triggerall = power >= 1000
trigger1 = ctrl

[State -1,万象天引]
type = ChangeState
value = 4300
triggerall = command = "back_x"
triggerall = p2bodydist x >= 78
Triggerall = power >= 300
trigger1 = statetype = S
triggerall = var(33)<= 0
triggerall = var(2)= 2
trigger1 = ctrl

[State -1, 近距离神罗天征]
type = ChangeState
value = 4310
triggerall = command = "back_x"
triggerall = p2bodydist x = [-77,77]
Triggerall = power >= 500
trigger1 = statetype = S
triggerall = var(33)<= 0
triggerall = var(2)= 2
trigger1 = ctrl

[State -1, 空中神罗天征]
type = ChangeState
triggerall = var(2) = 2
triggerall = var(59) = 0
value = 4320
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl

[State -1,开启完全体须佐能乎 ]
type = ChangeState
value = 8100
triggerall = var(2) = 2
triggerall = var(59) = 0
triggerall = power >= 3000
triggerall = command = "holddown"
triggerall = command = "c"
Triggerall = statetype = C
trigger1 = ctrl

[State -1,通灵外道魔像]
type = ChangeState
value = 14000
triggerall = var(2) = 2
triggerall = var(59) = 0
triggerall = power >= 3000
triggerall = command = "back_s"
trigger1 = statetype = s
trigger1 = ctrl
;===========================================================================
; Rikudou Mode SUPERS:
;===========================================================================
[State -1, 地爆天星]
type = ChangeState
triggerall = numhelper(8231) = 0
trigger2 = p2dist x = [300,1000]
trigger2 = p2dist y = [-150,150]
triggerall = var(2) = 5
triggerall = var(59) = 0
Triggerall = power >= 4000
value = 22200
Triggerall = command = "z"
Triggerall = statetype = S
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 天涯流星]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(59) = 0
Triggerall = power >= 4500
value = 11700
Triggerall = command = "z"
Triggerall = statetype = C
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 无限月读]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(59) = 0
Triggerall = power >= 6000
value = 27501
Triggerall = command = "z"
Triggerall = statetype = A
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;===========================================================================
; 六道模式:
;===========================================================================
[State -1, 扔求道玉]
type = ChangeState
triggerall = numhelper(11480) = 0
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11400
triggerall = command = "a"
Triggerall = statetype = C
trigger1 = ctrl

[State -1, 万象黑引]
type = ChangeState
triggerall = var(2) = [3,5]
Triggerall = power >= 2000
value = 27000
Triggerall = command = "下前a"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 求道玉包围]
type = ChangeState
triggerall = var(2) = [3,5]
Triggerall = power >= 1000
value = 27100
Triggerall = command = "下后a"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 阴遁雷派]
type = ChangeState
triggerall = var(2) = [3,5]
Triggerall = power >= 1500
value = 27200
Triggerall = command = "b"
Triggerall = statetype != S
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 近距离雷派]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11402
triggerall = command = "b"
Triggerall = stateno = 0
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 轮墓雷传]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(59) = 0
triggerall = numhelper(11420) = 0
value = 11401
triggerall = command = "fwd_b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 大范围阴遁雷派]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
Triggerall = power >= 3000
value = 11403
triggerall = command = "back_b"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1,岚遁光牙]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11200
triggerall = power >= 650
triggerall = command = "c"
Triggerall = statetype = C
trigger1 = ctrl

[State -1, 空中岚遁光牙]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11620
triggerall = command = "c"
Triggerall = statetype = A
trigger1 = ctrl

[State -1, 求道玉盾]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11520
triggerall = command = "c"
Triggerall = stateno = 0
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 树界降临]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
Triggerall = power >= 3000
value = 27400
Triggerall = command = "back_c"
Triggerall = statetype != A
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 轮墓换位（替身）]
type = ChangeState
triggerall = var(2) >= 3
triggerall = var(59) = 0
value = 22680
triggerall = POWER >= 50
Trigger1 = command = "c"
trigger1 = movetype = H

[State -1, 封术吸印]
type = ChangeState
triggerall = POWER >= 1000
triggerall = var(2) >= 3
triggerall = var(59) = 0
value = 3300
triggerall = command = "x"
trigger1 = stateno = 0
trigger1 = ctrl

[State -1, 完全体须佐]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(59) = 0
value = 85803
triggerall = command = "x"
Triggerall = power > 3000
Triggerall = statetype = C
trigger1 = ctrl

[State -1, 神罗天征]
type = ChangeState
value = cond(enemy, pos y + pos y > -20,4200,4210)
triggerall = command = "fwd_x"
triggerall = stateno != cond(enemy, pos y + pos y > -20,4200,4210)
trigger1 = statetype = S
triggerall = var(33)<= 0
triggerall = var(2)= 5
trigger1 = ctrl
triggerall = power >= 1000

[State -1,万象天引]
type = ChangeState
value = 4300
triggerall = command = "back_x"
triggerall = p2bodydist x >= 78
Triggerall = power >= 300
trigger1 = statetype = S
triggerall = var(33)<= 0
triggerall = var(2)= 5
trigger1 = ctrl

[State -1, 近距离神罗天征]
type = ChangeState
value = 4310
triggerall = command = "back_x"
triggerall = p2bodydist x = [-77,77]
Triggerall = power >= 500
trigger1 = statetype = S
triggerall = var(33)<= 0
triggerall = var(2)= 5
trigger1 = ctrl

[State -1, 空中神罗天征]
type = ChangeState
triggerall = var(2) = 5
triggerall = var(59) = 0
value = 11610
triggerall = command = "x"
Triggerall = statetype = A
trigger1 = ctrl

[State -1, 召唤轮墓]
type = ChangeState
Triggerall = numhelper(15000) = 0
triggerall = var(2) >= 3
triggerall = var(59) = 0
Triggerall = power >= 500
value = 27300
Triggerall = command = "y"
Triggerall = statetype = C
trigger1 = ctrl
trigger2 = numhelper(700) > 0

[State -1, 轮墓禁锢]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 22310
trigger1 = command = "y"
triggerall = power >= 250
Triggerall = statetype = S
trigger1 = ctrl

[State -1,开启完全体须佐能乎 ]
type = ChangeState
value = 8100
triggerall = var(2) = 5
triggerall = var(59) = 0
triggerall = power >= 3000
triggerall = command = "s"
Triggerall = statetype = C
trigger1 = ctrl
;===========================================================================
;--------------------------------Ataques Normales---------------------------
;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
; EMS
[State -1, EMS]
type = ChangeState
triggerall = var(2) = 0
triggerall = var(59) = 0
value = 11000
triggerall = command = "s"
Triggerall = statetype = C
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Rinnegan
[State -1, Rinnegan]
type = ChangeState
triggerall = var(2) = 1
triggerall = var(59) = 0
value = 11010
triggerall = command = "s"
Triggerall = statetype = C
trigger1 = ctrl
trigger2 = numhelper(700) > 0
;---------------------------------------------------------------------------
; Rikudou Mode
[State -1, Rikudou Mode]
type = ChangeState
triggerall = var(2) = 2
triggerall = var(59) = 0
value = 11020
triggerall = command = "holddown"
trigger1 = command = "s"
Triggerall = statetype != A
trigger1 = ctrl

[State -1, Rikudou Mode]
type = ChangeState
trigger1 = var(2) = 2
triggerall = life <= 10
value = 11020
trigger1 = ctrl
;---------------------------------------------------------------------------
; Rinne Sharingan
[State -1, Rinne Sharingan]
type = ChangeState
triggerall = var(2) = 3
triggerall = var(59) = 0
value = 11030
triggerall = command = "holddown"
triggerall = command = "s"
Triggerall = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; Power Charge
[State -1, Power Charge]
type = ChangeState
triggerall = var(59) = 0
Triggerall = power < 6000
value = 10000
triggerall = command = "s"
Triggerall = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; 幻术
[State -1, 幻术]
type = ChangeState
triggerall = var(2) = [0,2]
triggerall = var(59) = 0
value = 16000
trigger1 = command = "hold_s"
trigger1 = command = "a"
triggerall = power >= 250
Triggerall = statetype != A
trigger1 = ctrl

[State -1, 幻术反击]
type = ChangeState
triggerall = var(2) = [1,2]
triggerall = var(59) = 0
Triggerall = power >= 300
value = 17000
trigger1 = command = "hold_s"
trigger1 = command = "c"
Triggerall = statetype != A
trigger1 = ctrl
trigger1 = numhelper(3001) > 0


[State -1, 再生之术]
type = ChangeState
value = 21080
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
triggerall = power >= 3000
triggerall = life <= lifemax*.5
trigger1 = command = "hold_s"
trigger1 = command = "hold_x"
trigger1 = statetype != A
trigger1 = ctrl

[State -1, 轮回眼幻术]
type = ChangeState
value = 21081
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
triggerall = life > lifemax*.5
trigger1 = command = "hold_s"
trigger1 = command = "hold_x"
trigger1 = statetype != A
trigger1 = ctrl
;---------------------------------------------------------------------------
; 普通A
[State -1, A1]
type = ChangeState
triggerall = VAR(2) = 0
triggerall = var(59) = 0
value = 200
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; 万花筒A
[State -1, A2]
type = ChangeState
triggerall = VAR(2) = 1
triggerall = var(59) = 0
value = 300
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; 轮回眼A
[State -1, A3]
type = ChangeState
triggerall = VAR(2) = 2
triggerall = var(59) = 0
value = 400
triggerall = command = "a"
trigger1 = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; 空中A
[State -1, 空中A]
type = ChangeState
triggerall = var(2) <= 2
triggerall = var(59) = 0
value = 210
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------
; 六道A
[State -1, A4]
type = ChangeState
triggerall = var(2) >= 3
triggerall = var(59) = 0
value = 11300
triggerall = command = "a"
Triggerall = statetype = S
trigger1 = ctrl
;---------------------------------------------------------------------------
; 六道空中A
[State -1, A Aire Rikudou Mode]
type = ChangeState
triggerall = var(2) = [3,5]
triggerall = var(59) = 0
value = 11600
triggerall = command = "a"
Triggerall = statetype = A
trigger1 = ctrl
;---------------------------------------------------------------------------

[State -1, 伊邪那岐]
type = ChangeState
trigger1 = var(2) = 1
trigger1 = var(8) = 0
trigger1 = life <= lifemax*0.2
value = 20000
trigger1 = stateno = [5000,5210]


[State -1, AI on]
type = VarSet
triggerAll = Var(59) < 1
triggerAll = RoundState = 2
trigger1 = AILevel > 0
v = 59
value = 1
Ignorehitpause = 1

[State -1, AI OFF]
type=VarSet
trigger1 = var(59) > 0
trigger1 = RoundState != 2
trigger2 = AILevel = 0
v = 59
value = 0
Ignorehitpause = 1