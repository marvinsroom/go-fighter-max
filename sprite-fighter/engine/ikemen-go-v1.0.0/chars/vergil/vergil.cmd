
[Remap]
x = x      ;Ｘボタンの入力判定を実際に押すボタンに割り当てる。
y = y      ;Ｙボタン　　　　　　　　　〃
z = z      ;Ｚボタン　　　　　　　　　〃
a = a      ;Ａボタン　　　　　　　　　〃
b = b      ;Ｂボタン　　　　　　　　　〃
c = c      ;Ｃボタン　　　　　　　　　〃
s = s      ;スタートボタン　　　　　　〃



[Defaults]
command.time = 15  ;標準のコマンド入力受付時間。
                   ;各コマンドで省略している場合に有効。
                   ;このパラメータを消した場合、デフォルトは１フレームになる。
                   ;（　M.U.G.E.Nでの１フレーム　＝　１／６０秒　）

command.buffer.time = 1  ;標準のコマンド入力記憶時間。
                         ;入力した直後にコマンドを記憶し、
                         ;指を離してもコマンドが成功している状態を
                         ;ここで設定した時間の分維持する。
                         ;１～３０フレームまでの間で設定可能。
                         ;デフォルトは１フレーム。

;============================================================================== 第３部
; コマンド定義パート（入力キーを設定する）
;==============================================================================
;------------------------------------------------------------------------------
; ここがキーとボタンの組み合わせで格闘ゲームにおける
;『入力コマンド』を直接設定・編集するパート。
;
; 一つずつコマンドに名前を付けて入力キーを組み合わせる単純な作業になるけど、
; 組み合わせが独特だから覚えるのは難易度が少し高い。
;
; 下記で「書式の決まり」と「組み合わせに必要なアルファベットと記号」を
; 全て説明しましょう。
;------------------------------------------------------------------------------
;■書式の決まり■
;
; [Command]         ：入力コマンドを１個定義する。
; name = "***"      ：コマンド名を決める。大文字と小文字も区別される。
; command = ###     ：実際に入力するキーを組み合わせる。詳細は後述。
; time = &&&        ：入力受付時間を設定（オプション）。
; buffer.time = @@@ ：入力記憶時間を設定（オプション）。
;
; 小ネタでも説明している通り、登録が可能な数は最大『１２８個』まで。
;
;
;※『必須コマンド名』と書いてるコマンドは、システム側で処理してます。
;　コマンド名を変えたり、消してはいけません。キーの変更は出来ます。
;------------------------------------------------------------------------------
;■必要なアルファベットと記号■
;
; 上記の「command = ###」の『###』に該当する部分で、
; 組み合わせるキーとボタンを設定しなければならない。
;
; ※設定したキーやボタンはM.U.G.E.Nのオプションモードにある
;  「キーコンフィグ」にて設定したキーなどに対応しています。
;
; ★方向キー★（全て必ず大文字で）
;
; 　B 　：「後方」にキーを入れる（ Backward ）
; 　D 　：「下方」にキーを入れる（ Downward ）
; 　F 　：「前方」にキーを入れる（ Forward ）
; 　U 　：「上方」にキーを入れる（ Upward ）
;
; 　DB　：「後ろ斜め下」にキーを入れる（「D」と「B」が同時に入力された事を認識）
; 　UB　：「後ろ斜め上」にキーを入れる（「U」と「B」が同時に入力された事を認識）
; 　DF　：「前斜め下」にキーを入れる（「D」と「F」が同時に入力された事を認識）
; 　UF　：「前斜め上」にキーを入れる（「U」と「F」が同時に入力された事を認識）
;
; ★ボタン★（全て必ず小文字で）
;
; 　a 　：「Ａボタン」を押す
; 　b 　：「Ｂボタン」を押す
; 　c 　：「Ｃボタン」を押す
; 　x 　：「Ｘボタン」を押す
; 　y 　：「Ｙボタン」を押す
; 　z 　：「Ｚボタン」を押す
; 　s 　：「スタートボタン」を押す
;
; ★記号★（入力効果を変化させる命令）
;
; 　/ 　：（スラッシュ）キーやボタンを「押しっぱなし」にしている事を認識する場合に追加する
;
; 　　（例）：　/b       = Ｂボタンを押したままにする
; 　　　　　　　/F       = 前キーを押したままにする
; 　　　　　　　/U,z     = 上キーを押したままＺボタンを入力する
;
;　　━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;
; 　~ 　：（チルダ）キーやボタンが「離された時」を認識する場合に追加する
;
; 　　（例）：　~x       = Ｘボタンを離す
; 　　　　　　　~DF      =「前斜め下」のキーを離す
; 　　　　　　　~DB,F,c  =「後ろ斜め下」を離した後に前キー・Ｃボタンの順番に入力する
;
; 　　　　　　※「ボタンを離すまでの時間（溜め時間）」も設定する事が出来る
;
; 　　　　　　　~30x     = Ｘボタンを押したままにして、３０フレーム以上経ったら離す
; 　　　　　　　~50B,F,a = 後ろキーを５０フレームまで溜めて前キー・Ａボタンの順番に入力する
;
;　　━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;
; 　$ 　：（ドル）方向キーの「複数の内どれかが入力されている事」を認識する場合に追加する
;
; 　　（例）：　$B       =「後方」「後ろ斜め下」「後ろ斜め上」のどれかが入力されている状態
; 　　　　　　　$UF      =「前」「上」「前斜め上」のどれかが入力されている状態
;
; 　　　　　　※この記号は「方向キー」でしか使えません。
;
;　　━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;
; 　+ 　：（プラス）ボタンを「同時押し」している事を認識する場合に追加する
;
; 　　（例）：　x+y      = ＸボタンとＹボタンを同時押しする
; 　　　　　　　a+b+c    = ＡボタンとＢボタンとＣボタンを同時押しする
;
; 　　　　　　※この記号は「ボタン」でしか使えません。
;
;　　━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;
; 　> 　：（グレーターザン）大なり（Win版で追加された記号）
; 　　　　　　　　　　　　「他のキーが入力されていない事を確認して、そのキーを押す」場合
;
; 　　（例）：　a,>~a    = Ａボタン以外が入力されていない状態でＡボタンを離す
; 　　　　　　　F,>~F,>F = 前キー以外が入力されていない状態で前キーを離し、
;　　　　　　　　　　　　　もう一度前キーを入力する
;
;-------------------------------------------------------------------------------
; ●これらの記号は全て組み合わせて使う事が出来る●
;
; 　　（例）：　~80$DB,DF,F,/a+y+c
; 　　　　　　　
; 　　　　　　「後方」「下」「後ろ斜め下」のどれかを８０フレームまで溜めて
; 　　　　　　「前斜め下」→「前」を入力した後、ＡとＹとＣを同時押ししたままにする
;

;━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
;コピペ用
;━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Command]
name = "AI0"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 0
[Command]
name = "AI1"
command = b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b
time = 0
[Command]
name = "AI2"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 0
[Command]
name = "AI3"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 0
[Command]
name = "AI4"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 0
[Command]
name = "AI5"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI6"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 0
[Command]
name = "AI7"
command = F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F
time = 0
[Command]
name = "AI8"
command = D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D
time = 0
[Command]
name = "AI9"
command = B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B
time = 0
[Command]
name = "AI10"
command = U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U
time = 0
[Command]
name = "AI11"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 0
[Command]
name = "AI12"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 0
[Command]
name = "AI13"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 0
[Command]
name = "AI14"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 0
[Command]
name = "AI15"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI16"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 0
[Command]
name = "AI17"
command = a,B,c,x,y,z,s,B,D,F,U,a,b,c,x,y,z,s,s
time = 0
[Command]
name = "AI18"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 0
[Command]
name = "AI19"
command = b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b
time = 0
[Command]
name = "AI20"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 0
[Command]
name = "AI21"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 0
[Command]
name = "AI22"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 0
[Command]
name = "AI23"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI24"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 0
[Command]
name = "AI25"
command = F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F
time = 0
[Command]
name = "AI26"
command = D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D,D
time = 0
[Command]
name = "AI27"
command = B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B
time = 0
[Command]
name = "AI28"
command = U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U,U
time = 0
[Command]
name = "AI29"
command = a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a
time = 0
[Command]
name = "AI30"
command = c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c
time = 0
[Command]
name = "AI31"
command = x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x
time = 0
[Command]
name = "AI32"
command = y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y
time = 0
[Command]
name = "AI33"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI34"
command = s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s
time = 0
[Command]
name = "AI35"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI36"
command = z,z,z,z,z,z,a,a,a,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI37"
command = z,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,z,z,z
time = 0
[Command]
name = "AI38"
command = z,z,z,z,z,a,a,a,z,z,z,z,z,a,a,a,z,z,z
time = 0
[Command]
name = "AI39"
command = z,z,z,z,z,a,a,a,z,z,z,z,z,z,a,a,z,z,z
time = 0
[Command]
name = "AI40"
command = z,z,z,z,a,a,a,z,z,z,z,a,z,z,a,a,z,z,z
time = 0
[Command]
name = "AI41"
command = z,z,z,a,z,z,z,z,z,z,z,z,z,a,a,z,z,z,z
time = 0
[Command]
name = "AI42"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI43"
command = z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,z,a,a,z
time = 0
[Command]
name = "AI44"
command = z,z,a,a,a,a,z,z,z,z,z,z,z,z,z,a,a,a,z
time = 0
[Command]
name = "AI45"
command = z,z,z,z,z,z,a,a,z,z,z,z,z,a,a,a,a,z,z
time = 0
[Command]
name = "AI46"
command = z,z,z,z,z,z,z,z,a,a,a,a,a,a,z,z,z,z,z
time = 0
[Command]
name = "AI47"
command = z,z,z,a,a,a,a,z,z,z,z,z,z,z,z,z,z,z,z
time = 0
[Command]
name = "AI48"
command = z,z,z,z,z,a,a,a,z,z,z,a,a,a,z,z,a,z,a
time = 0
[Command]
name = "AI49"
command = z,z,z,z,a,a,a,z,z,z,z,z,a,a,a,z,z,z,z
time = 0
[Command]
name = "AI50"
command = z,z,z,a,a,z,z,z,z,z,z,z,z,z,a,a,z,z,z
time = 0

;------------------------------------------------------------------------------
;-| 超必殺技 |-----------------------------------------------------------------

;※名前が同じならば、違うコマンドでも同じステートの技を出す事が可能。
[Command]
name = "DTsissou"
command = ~D, DB, B, DB, F, x
time = 25

[Command]
name = "DTsissou"
command = ~D, DB, B, DB, F, ~x
time = 25

[Command]
name = "ESryusei"
command = ~D, DF, F, DF, D, DB, B, b
time = 30

[Command]
name = "ESryusei"
command = ~D, DF, F, DF, D, DB, B, ~b
time = 30

[Command]
name = "ESryusei"
command = ~D, F, D, B, b
time = 30

[Command]
name = "ESryusei"
command = ~D, F, D, B, ~b
time = 30

[Command]
name = "Zettou"
command = ~D, DF, F, D, DF, F, b
time = 30

[Command]
name = "DTkabuto"
command = ~D, DF, F, D, DF, F, y
time = 30

[Command]
name = "DTkabuto"
command = ~D, DF, F, D, DF, F, ~y
time = 30

[Command]
name = "TripleKFPalm"
command = ~D, DF, F, D, DF, F, x
time = 20


[Command]
name = "TyouhatuEnjin"
command = ~D, DB, B, D, DB, B, z
time = 20

[Command]
name = "Enjin"
command = ~30z

[Command]
name = "trip"
command = ~D, DF, F, DF, D, DB, B , x
time = 30

[Command]
name = "trip"
command = ~D, F, D, B , x
time = 30

[Command]
name = "trip"
command = ~D, DF, F, DF, D, DB, B , ~x
time = 30

[Command]
name = "trip"
command = ~D, F, D, B , ~x
time = 30
;------------------------------------------------------------------------------
;-| 必殺技 |-------------------------------------------------------------------

[Command]
name = "cutter1"
command = ~F, D, DF, a
time = 12

[Command]
name = "cutter1"
command = ~F, D, DF, ~a
time = 12

[Command]
name = "cutter2"
command = ~F, D, DF, b
time = 12

[Command]
name = "cutter2"
command = ~F, D, DF, ~b
time = 12

[Command]
name = "upper_x"
command = ~F, D, DF, x

[Command]
name = "upper_y"
command = ~F, D, DF, y

[Command]
name = "upper_xy"
command = ~F, D, DF, x+y

[Command]
name = "QCF_x"
command = ~D, DF, F, x

[Command]
name = "QCF_y"
command = ~D, DF, F, y

[Command]
name = "QCF_x"
command = ~D, DF, F, ~x

[Command]
name = "QCF_y"
command = ~D, DF, F, ~y

[Command]
name = "QCF_xy"
command = ~D, DF, F, x+y

[Command]
name = "ryusei1"
command = ~D, DF, F, a
time = 12

[Command]
name = "ryusei1"
command = ~D, DF, F, ~a
time = 12

[Command]
name = "ryusei2"
command = ~D, DF, F, b
time = 12

[Command]
name = "ryusei2"
command = ~D, DF, F, ~b
time = 12

[Command]
name = "trickup"
command = ~D, DF, F, c
time = 12

[Command]
name = "trickup"
command = ~D, DF, F, ~c
time = 12

[Command]
name = "QCB_x"
command = ~D, DB, B, x

[Command]
name = "QCB_y"
command = ~D, DB, B, y

[Command]
name = "geturin1"
command = ~D, DB, B, a

[Command]
name = "geturin2"
command = ~D, DB, B, b

[Command]
name = "QCB_xy"
command = ~D, DB, B, x+y

[Command]
name = "kyusyu"
command = ~D, DB, B, z

[Command]
name = "kyusyu"
command = ~D, DB, B, ~z

[Command]
name = "FF_ab"
command = F, F, a+b

[Command]
name = "FF_a"
command = F, F, a

[Command]
name = "FF_b"
command = F, F, b

;---------------------------

[Command]
name = "board"
command = ~D, DF, F, b

;------------------------------------------------------------------------------
;-| キー２回連続入力 |---------------------------------------------------------
[Command]
name = "longjump"
command = D, $U
time = 18

[Command]
name = "FF"       ;必須コマンド名
command = F, F
time = 10

[Command]
name = "BB"       ;必須コマンド名
command = B, B
time = 10

;------------------------------------------------------------------------------
;-| 同時押し |-----------------------------------------------------------------

[Command]
name = "recovery" ;必須コマンド名
command = a+x
time = 1

[Command]
name = "c+z" ;必須コマンド名
command = c+z
time = 1

[Command]
name = "b+y" ;必須コマンド名
command = b+y
time = 1

[Command]
name = "a+b" ;必須コマンド名
command = a+b
time = 1

[Command]
name = "x+y" ;必須コマンド名
command = x+y
time = 1
;------------------------------------------------------------------------------
;-| 方向キー＋ボタン |---------------------------------------------------------

[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
time = 1

[Command]
name = "down_y"
command = /$D,y
time = 1

[Command]
name = "front_c"
command = /$F,c
time = 1

[Command]
name = "front_z"
command = /$F,z
time = 1


[Command]
name = "front_x"
command = /$F,x
time = 1

[Command]
name = "back_c"
command = /$B,c
time = 1

[Command]
name = "down_x"
command = /$D,x
time = 1
;------------------------------------------------------------------------------
;-| ボタン単発 |---------------------------------------------------------------

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
name = "up"
command = U
time = 1

[Command]
name = "down"
command = D
time = 1

[Command]
name = "back"
command = B
time = 1

[Command]
name = "fwd"
command = F
time = 1

[Command]
name = "start"
command = s
time = 1

[Command]
name = "hold_b+y" ;必須コマンド名
command = /b+y
time = 1

[Command]
name = "hold_c"
command = /c
time = 1

[Command]
name = "hold_z"
command = /z
time = 1

[Command]
name = "hold_x"
command = /x
time = 1

;------------------------------------------------------------------------------
;-| 方向キー |-----------------------------------------------------------------

[Command]
name = "holdfwd"   ;必須コマンド名
command = /$F
time = 1

[Command]
name = "holdback"  ;必須コマンド名
command = /$B
time = 1

[Command]
name = "holdup"    ;必須コマンド名
command = /$U
time = 1

[Command]
name = "holddown"  ;必須コマンド名
command = /$D
time = 1

;============================================================================== 第４部
; ステートエントリーパート（技などを出せるようにするための条件を設定）
;==============================================================================
;------------------------------------------------------------------------------
; コマンド名と入力するコマンドを設定しただけじゃ意味が無いので、ここから
;「実際に入力したコマンドでどの番号のステートをどういう条件で出せるか」
; を決めなければならない。
;
; ステートコントローラ「ChangeState」しか使わないけど、
; そんなに難しくないのでトリガーを覚えてたらすぐ出来る。
;
; ここさえ押さえておけば簡単なトリガー設定の流れは覚えられるかと。
;
; エントリーの順番にはある程度の法則があるけど、
; おまけフォルダの「小ネタ.txt」を参照。（波動拳が暴発ﾅﾝﾀﾗｶﾝﾀﾗ）
;
; ChangeStateなどステートコントローラの基本的な設置例は
; おまけフォルダの「テンプレート.txt」を参照。
;------------------------------------------------------------------------------
; ■準常時監視ステート（－１）■
; コマンドファイル（のステートエントリーパート）に必要な項目です。
; 絶対に消してはいけないので要注意。
;
; 通常の食らい状態以外の「P2StateNo」や「TargetState」等で制御された、
; 作成者が任意に指定した相手側の食らいステートに限り、
; 登録したステートコントローラが有効にはなりません。
;------------------------------------------------------------------------------

[Statedef -1] ;←この行は絶対に消さないでね。必須項目です。
;AI用

;------------------------------------------------------------------------------
[State -1, 何もしない]
type = ChangeState
triggerall = var(59)
triggerall = roundstate = 2
trigger1 = stateno = 2003
trigger1 = enemynear,statetype = A && enemynear,movetype = H
trigger1 = var(55) && numhelper(8510)
trigger1 = animtime = 0
trigger2 = stateno = 1002
trigger2 = enemynear,statetype = A && enemynear,movetype = H
trigger2 = var(55)
trigger2 = animtime = 0
trigger3 = stateno = 2003
trigger3 = enemynear,statetype = A && enemynear,movetype = H
trigger3 = prevstateno = 2610
trigger3 = animtime = 0
trigger4 = stateno = 1002
trigger4 = enemynear,movetype = H
trigger4 = animtime = 0
value = 0
ctrl = 0

;------------------------------------------------------------------------------


[State -1, 絶刀]
type = ChangeState
value = 3500
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 3000
triggerall = p2statetype = L || p2movetype = H
triggerall = P2bodydist X >= 180
triggerall = statetype != A
triggerall = ctrl
trigger1 = numhelper(1401)
trigger1 = helper(1401),stateno = 1402
trigger1 = enemynear,movetype = H
trigger2 = numhelper(8510)
trigger2 = helper(8510),stateno = 8511
trigger2 = enemynear,movetype = H


[State -1, DT兜割り]
type = ChangeState
value = 3300
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 2000
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
triggerall = statetype != A
trigger1 = ctrl || stateno = 100 || var(18)
trigger1 = P2MoveType = A
trigger1 = enemynear,time = [0+(10-var(59)),10+(10-var(59))]
trigger1 = random < 35 * var(59)
trigger1 = p2life <= 329
trigger2 = ctrl || stateno = 100 || var(18)
trigger2 = P2MoveType = A
trigger2 = enemynear,time = [0+(10-var(59)),10+(10-var(59))]
trigger2 = random < 40
trigger2 = p2life >= 330

[State -1, DT疾走居合い]
type = ChangeState
value = 3200
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 1000
triggerall = statetype != A
trigger1 = ctrl || stateno = 100
trigger1 = P2MoveType = A
trigger1 = enemynear,time = [0+(10-var(59)),10+(10-var(59))]
trigger1 = P2bodydist X = [10,70]
trigger1 = random < 130
trigger2 = stateno = 901
trigger2 = time = 10
trigger3 = (stateno = 201) && animelemtime(7) >= 0
trigger3 = movehit && p2movetype = H
trigger3 = random%20 = [17,19] 
trigger4 = (stateno = 430)
trigger4 = movehit  && p2movetype = H
trigger4 = random%20 = [0,1]
trigger4 = P2bodydist X >= 45
trigger5 = var(18) || ctrl || stateno = 100
trigger5 = P2MoveType = A
trigger5 = enemynear,animtime = [-15,5]
trigger5 = P2bodydist X = [70,150]
trigger6 = enemynear,statetype = A && enemynear,movetype = H
trigger6 = prevstateno = 1002
trigger6 = stateno = 0 && p2bodydist y > -55
trigger6 = var(55) = 1 && enemynear,vel Y > 1
trigger7 = enemynear,statetype = A && enemynear,movetype = H
trigger7 = ctrl || stateno = 0
trigger7 = enemynear,vel Y > 0
trigger7 = p2bodydist y < -150
trigger7 = random < 500
trigger7 = var(55) = 0
trigger8 = enemynear,movetype = H
trigger8 = ctrl || stateno = 0
trigger8 = enemynear,vel X > 2
trigger8 = random < 500
trigger8 = prevstateno = 1002
trigger8 = var(55) = 0


[State -1, エネステ流星脚]
type = ChangeState
value = 3050
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 1000
triggerall = statetype = A
trigger1 = stateno = [1500,1501]
trigger1 = movehit && var(15) > 4
trigger1 = Pos Y < -15
trigger1 = random < 150
value = 1501

[State -1, 1ゲージ絶刀]
type = ChangeState
value = 3000
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 1000
triggerall = statetype = A
trigger1 = stateno = 610
trigger1 = Pos Y < -100
trigger1 = movehit = 5 && enemynear,movetype = H
trigger1 = random < 500

[State -1, 挑発→円陣展開]
type = ChangeState
value = 2900
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = power >= 1000
triggerall = var(56) = 0
triggerall = statetype = S
triggerall = P2bodydist X >= 200
triggerall = !(enemynear,vel X > 0)
triggerall = ctrl
triggerall = prevstateno != 2900
triggerall = numhelper(8500) = 0
triggerall = numhelper(8510) = 0
trigger1 = random = [980,999]


[State -3,ｶﾞｰﾄﾞ]
Type=ChangeState
Value=120
triggerall = var(59)
triggerall = var(52) = 0
triggerall = (stateno!=[120,159])
triggerall = inguarddist || (p2statetype=A && p2dist x<70 && p2movetype=A)
triggerall = !(enemynear,hitdefattr=,AT)
triggerall = ctrl || stateno=100
triggerall = random <= var(59) * 80
trigger1 = RoundState = 2

;------------------------------------------------------------------------------
[State -1, 弾き]
type = ChangeState
value = 900
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = EnemyNear,numproj = 0
trigger1 = ctrl || stateno = 100
trigger1 = EnemyNear,HitDefAttr=SA,AA
trigger1 = p2bodydist X = [25,90]
trigger2 = ctrl || stateno = 100
trigger2 = p2bodydist X = [25,90]
trigger2 = p2movetype = A && random = [850,880]
;==============================================================================
; 必殺技
;==============================================================================
[State -1, ラウンドトリップ]
type = ChangeState
value = 1400
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
triggerall = P2moveType = H || P2moveType = I
triggerall = P2stateType != A
trigger1 = P2bodydist X >= 180
trigger1 = ctrl && random = [350,500]
trigger1 = !(enemynear,vel X > 0)
trigger1 = var(55) = 0
ignorehitpause = 0

;------------------------------------------------------------------------------

[State -1, 次元斬]
type = ChangeState
value = 1000
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = prevstateno != [1000,1002]
trigger1 = enemynear,statetype = A && enemynear,movetype = H
trigger1 = stateno = 0 && time = 20
trigger1 = var(55) = 1
trigger2 = var(18) && p2bodydist X > 170
trigger3 = numhelper(1401)
trigger3 = helper(1401),stateno = 1402
trigger3 = enemynear,movetype = H
trigger4 = numhelper(8510)
trigger4 = helper(8510),stateno = 8511
trigger4 = enemynear,movetype = H
trigger4 = var(55) = 0

;------------------------------------------------------------------------------

[State -1, 日輪脚弱]
type = ChangeState
value = 2600
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
trigger1 = ctrl
Trigger1 = enemynear,Time >= 50-(var(59)*5)
trigger1 = P2bodydist X = [-10,30]
trigger1 = P2bodydist Y = [-40,0]
trigger1 = P2StateType = A
trigger1 = P2MoveType = A
trigger1 = random < 65 * var(59)
ignorehitpause = 0

[State -1, 日輪脚強]
type = ChangeState
value = 2610
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = P2bodydist X = [0,80]
triggerall = prevstateno != 801
triggerall = p2stateno != 821
trigger1 = ctrl
Trigger1 = enemynear,Time >= 60-(var(59)*5)
trigger1 = P2bodydist X = [15,45]
trigger1 = P2bodydist Y = [-60,-20]
trigger1 = P2StateType = A
trigger1 = P2MoveType = A
trigger1 = random < 30 * var(59)
trigger2 = stateno = 410 && time >= 21
trigger2 = movehit && p2movetype = H
trigger2 = enemynear,life > 40
trigger2 = random%10 = [1,9]
trigger3 = stateno = 231 && animelemtime(8) >= 0
trigger3 = movehit && p2movetype = H
trigger3 = random%10 = [0,1]
trigger4 = p2movetype = H
trigger4 = ctrl || stateno = 0
trigger4 = enemynear,vel X > 1
trigger4 = random < 500
trigger4 = prevstateno = 1002
ignorehitpause = 0

[State 410, ステート変更];追加入力
type = ChangeState
triggerall = var(59)
triggerall = roundstate = 2
triggerall = stateno = 410
trigger1 = animelemtime(11) >= 2
trigger1 = movehit && p2movetype = H
trigger1 = enemynear,life < 80*(1-(fvar(10))) || P2bodydist X = [81,110]
trigger2 = animelemtime(11) >= 2
trigger2 = movehit && p2movetype = H
trigger2 = random%10 = [0,1]
trigger3 = animelemtime(11) >= 0
trigger3 = prevstateno = 901
trigger4 = animelemtime(8) >= 0
trigger4 = moveguarded
value = 412

;------------------------------------------------------------------------------

;流星脚
[State -1, 流星脚]
type = ChangeState
value = 1500
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = pos Y < -30
triggerall = statetype = A
trigger1 = ctrl && P2bodydist Y = [10,30]
trigger1 = p2movetype = H && random < 200
trigger2 = stateno = 2610 && P2bodydist Y = [10,30]
trigger2 = movecontact
trigger2 = time > 38
trigger3 = ctrl && P2bodydist Y >= 85
trigger3 = ceil(abs(P2bodydist Y)/(abs(P2bodydist X))+0.1) = [0.5,1.8]
trigger3 = enemynear,animtime = [-20,-5]
ignorehitpause = 0

;------------------------------------------------------------------------------

;月輪脚弱
[State -1, 月輪脚弱]
type = ChangeState
value = 2500
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = P2bodydist X = [0,50]
triggerall = p2statetype != L
trigger1 = ctrl && enemynear,time = [0,5]
trigger1 = p2statetype = C
trigger1 = p2movetype = A || p2stateno = 400

ignorehitpause = 0
;------------------------------------------------------------------------------
;月輪脚強
[State -1, 月輪脚強]
type = ChangeState
value = 2505
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = p2statetype != C
trigger1 = stateno = 231 && animelemtime(8) >= 0
trigger1 = movehit && p2movetype = H
trigger1 = random%10 = [2,3]
trigger2 = stateno = 231 && animelemtime(8) >= 0
trigger2 = movehit && p2movetype = H
trigger2 = enemynear,life<142
ignorehitpause = 0


;------------------------------------------------------------------------------
[State -1, 飛び道具かき消し]
type = ChangeState
value = 950
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = ctrl
triggerall = P2bodydist X >= 50
trigger1 = enemynear,NumProj >= 1
trigger2 = enemynear,HitDefAttr = SCA, AP
ignorehitpause = 0



;------------------------------------------------------------------------------

[State -1, 疾走居合い切り]
type = ChangeState
value = 1200
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = p2statetype != L
trigger1 = stateno = 901
trigger1 = time = 10
trigger1 =  p2bodydist X > 75
trigger2 = (stateno = 201) && animelemtime(6) = 1
trigger2 = movehit && p2movetype = H
trigger2 = random%20 = [15,19] 
trigger3 = enemynear,statetype = A && enemynear,movetype = H
trigger3 = var(55) && stateno = 0
trigger3 = enemynear,vel Y > 1
trigger3 = prevstateno = 1002 && time > 15
trigger4 = enemynear,statetype = A && enemynear,movetype = H
trigger4 = ctrl || stateno = 0
trigger4 = enemynear,vel Y > 0
trigger4 = p2bodydist y < -220
trigger4 = random < 500
trigger5 = stateno = 901
trigger5 = time = 10
trigger5 = p2bodydist X <= 75
trigger5 = random%10 = [0,5]
trigger6 = enemynear,movetype = H
trigger6 = ctrl || stateno = 0
trigger6 = enemynear,vel X > 2
trigger6 = random < 500
trigger6 = prevstateno = 1002
trigger6 = var(55) = 0
trigger7 = ctrl
trigger7 = p2bodydist X > 120
trigger7 = p2movetype = I
trigger7 = random < 100
trigger8 = ctrl
trigger8 = p2bodydist X > 120
trigger8 = p2movetype = A && enemynear,animtime >= -10
trigger8 = random < 100

;------------------------------------------------------------------------------

[State -1, スティンガー]
type = ChangeState
value = 1100
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
triggerall = p2statetype != L
trigger1 = ctrl
trigger1 = p2bodydist X > 120
trigger1 = p2movetype = I
trigger1 = random < 250
trigger2 = ctrl
trigger2 = p2bodydist X > 120
trigger2 = p2movetype = A && enemynear,animtime >= -10
trigger2 = random < 250
trigger3 = stateno = 300 && time > 30
trigger3 = movecontact
trigger3 = p2bodydist X > 65
trigger4 = stateno = 430
trigger4 = movehit  && p2movetype = H
trigger4 = random%10 = [2,3]
trigger4 = P2bodydist X >= 45
trigger5 = var(18) = 1
trigger6 = enemynear,statetype = A && enemynear,movetype = H
trigger6 = ctrl || stateno = 0
trigger6 = enemynear,vel Y > 0
trigger6 = p2bodydist y < -190
trigger6 = var(55) = 0


;------------------------------------------------------------------------------

[State -1, 兜割り]
type = ChangeState
value = 1300
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = pos Y < -30
triggerall = roundstate = 2
triggerall = statetype = A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
triggerall = P2BodyDist Y >= 20 && P2BodyDist X = [-15,80]
trigger1 = stateno = 600
trigger1 = movecontact && P2BodyDist X >= 50
trigger2 = stateno = 600
trigger2 = movecontact && P2BodyDist y >= 30
trigger3 = stateno = 1501 && var(15) > 4
trigger3 = AnimElemTime(6) < 0
trigger3 = p2statetype = A
trigger4 = stateno = 2013  && time > 5
trigger4 = P2BodyDist X = [-5,80]
trigger4 = !(P2BodyDist X < 0  && enemynear,vel X > 2)
ignorehitpause = 0




[State -1, ジャンプ弱パンチ]
type = ChangeState
value = 600
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = A
triggerall = p2statetype = A
triggera1 = P2BodyDist Y = [-69,-10]
triggera1 = P2BodyDist X = [-10,60]
trigger1 = time >= 5 && stateno = 2013
trigger2 = stateno = 600 && P2BodyDist X = [-10,45]
trigger2 = movehit

[State -1, ジャンプ強パンチ]
type = ChangeState
value = 610
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = A
triggerall = P2BodyDist X = [49,110]
triggerall = P2BodyDist Y = [-40,50]
triggerall = p2statetype = A
trigger1 = stateno = 600
trigger1 = movecontact
trigger2 = ctrl && p2statetype = A
;==============================================================================
; 特殊技
;==============================================================================

[State -1, フォースエッジコンボ１]
type = ChangeState
value = 300
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
triggerall = p2statetype != L
triggerall = statetype ! = A
triggerall = P2BodyDist Y = [-30,0]
triggerall = P2BodyDist X = [70,110]
trigger1 = ctrl || stateno = 100
trigger1 = random < 100


;==============================================================================
; 移動関連
;==============================================================================
;------------------------------------------------------------------------------


[State -1, トリックアップ]
type = ChangeState
value = 2020
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = var(16) = 0
trigger1 = ctrl
trigger1 = P2BodyDist X = [50,150]
trigger1 = enemynear,movetype = A
trigger1 = random < 100
trigger2 = ctrl
trigger2 = P2BodyDist X = [50,150]
trigger2 = enemynear,numproj != 0
trigger2 = random < 100
trigger3 = ctrl
trigger3 = p2statetype = C || p2movetype = I
trigger3 = P2BodyDist X = [50,200]
trigger3 = random < 100


[State -1, トリックアップ空中]
type = ChangeState
value = 2030
triggerall = var(16) = 0
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
trigger1 = stateno = 2610 && animelemtime(24) = 2
trigger1 = movehit && enemynear,movetype = H
trigger1 = p2bodydist Y < -150
trigger1 = numhelper(8510) = 0
trigger2 = stateno = 50
trigger2 = p2bodydist X > 150
trigger2 = enemynear,numproj != 0||random < 350




[State -1, トリックダウン空中]
type = ChangeState
value = 2050
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = enemynear,numproj = 0
trigger1 = stateno = 2610 && animelemtime(21) = 0
trigger1 = movehit && enemynear,movetype = H
trigger1 = prevstateno = [410,411]
trigger1 = numhelper(8510)
trigger2 = stateno = 2610 && animelemtime(23) = 0
trigger2 = movehit && enemynear,movetype = H
trigger2 = prevstateno = [410,411]
trigger2 = random = [601,999] 
trigger3 = ctrl
trigger3 = p2movetype = A && enemynear,vel Y < 0
trigger3 = enemynear,numproj = 0
trigger3 = random < 100




;==============================================================================
; 特殊技
;==============================================================================
;------------------------------------------------------------------------------

[State -1, カンフースルー];投げ技
type = ChangeState
value = 800
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = S
triggerall = ctrl
triggerall = p2bodydist X = [0,22]
triggerall = p2statetype != A
TriggerAll = EnemyNear,StateType != L
TriggerAll = !(EnemyNear,prevStateno = 5120 && time < 14)
trigger1 = p2movetype != H
trigger1 = random <= 300




;受身
[State -1]
type = ChangeState
value = 702
triggerall = var(59)
triggerall = roundstate = 2
triggerall = Alive
triggerall = StateNo = 5050 || StateNo = 5071 || StateNo = 5101
triggerall = Vel Y >= 0
triggerall = Pos Y >= -15
triggerall = CanRecover
trigger1 = random = [0,400]
persistent = 0

;==============================================================================
; 通常攻撃技
;==============================================================================
;------------------------------------------------------------------------------
[State -1, しゃがみ強パンチ]
type = ChangeState
value = 410
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
TriggerAll= EnemyNear,StateType != L
TriggerAll= prevstateno != 801
triggerall= p2stateno != 821
trigger1 = ctrl
trigger1 = P2bodydist X = [5,70]
trigger1 = P2bodydist Y = [-100,-50]
trigger1 = P2StateType = A
trigger1 = random < 30 * var(59)
trigger1 = stateno != 411 
trigger2 = stateno = 430 && movecontact
trigger2 = P2bodydist X >= 30
trigger2 = random%10 = [4,9]
trigger3 = stateno = 201 && animelemtime(8) >= 1
trigger3 = movehit && p2movetype = H
trigger3 = random%20 = [1,11] 
trigger4 = stateno = 901
trigger4 = time = 10
trigger4 = p2bodydist X = [0,75]

[State -1, フォースエッジコンボ４]
type = ChangeState
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
TriggerAll=EnemyNear,StateType != L
trigger1 = (stateno = 201) && animelemtime(7) >= 1
trigger1 = movehit && p2movetype = H
trigger1 = random%20 = [12,14]
trigger2 = (stateno = 201) && animelemtime(7) >= 1
trigger2 = movehit && p2movetype = H
trigger2 = enemynear,life<80
value = 330
ctrl = 0

[State -1, 立ち弱パンチ]
type = ChangeState
value = 200
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
TriggerAll=EnemyNear,StateType != L
TriggerAll=EnemyNear,StateType != A
trigger1 = ctrl || stateno = 100
trigger1 = P2bodydist X = [40,60]
trigger1 = P2MoveType = I
trigger1 = statetype = S
trigger1 = random = [200,600]
trigger2 = stateno = 231 && animelemtime(8) >= 0
trigger2 = movehit && p2movetype = H
trigger2 = random%10 = [4,8]
trigger3 = stateno = 300 && time > 30
trigger3 = movecontact
trigger3 = p2bodydist X <= 65
trigger4 = prevstateno = 630
trigger4 = ctrl
trigger4 = p2movetype = H

[State -1, 立ち強パンチ]
type = ChangeState
value = 210
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
TriggerAll=StateType != A
TriggerAll=EnemyNear,StateType != L
Trigger1 = P2BodyDist X = [100,110]
Trigger1 = P2BodyDist Y >= -70
Trigger1 = (EnemyNear,StateNo != [120,159])||EnemyNear,StateType=A
Trigger1 = Ctrl || stateno = 100
Trigger1 = random = [0,200]
trigger2 = (stateno = 201) && animelemtime(7) >= 1
trigger2 = movehit && p2movetype = H
trigger2 = random%20 = 0
trigger3 = (stateno = 201) && animelemtime(7) >= 1
trigger3 = movehit && p2movetype = H
trigger3 = enemynear,life<80

[State -1, 立ち弱キック]
type = ChangeState
value = 230
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
TriggerAll = EnemyNear,StateType != L
TriggerAll = EnemyNear,StateType != A
TriggerAll = prevstateno != 801
trigger1 = ctrl || stateno = 100
trigger1 = P2bodydist X = [61,90]
trigger1 = P2MoveType = I || P2MoveType = H
trigger1 = random = [0,350]
trigger2 = prevstateno = 640 || prevstateno = 1510
trigger2 = prevstateno != 630
trigger2 = ctrl
trigger2 = EnemyNear,movetype = H
trigger2 = random = [300,999]


[State -1, 立ち強キック]
type = ChangeState
value = 240
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
TriggerAll=EnemyNear,StateType != L
trigger1 = stateno = 231 && animelemtime(8) >= 0
trigger1 = movehit && p2movetype = H
trigger1 = random%10 = 9
trigger2 = stateno = 231 && animelemtime(8) >= 0
trigger2 = movehit && p2movetype = H
trigger2 = enemynear,life<110

;------------------------------------------------------------------------------

[State -1, 挑発]
type = ChangeState
value = 195
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = enemynear,stateno != [120,159]
trigger1 = P2bodydist X >= 200
trigger1 = P2MoveType = H
trigger1 = P2statetype = L
trigger1 = ctrl && random = [500,550]
trigger2 = numhelper(1401)
trigger2 = helper(1401),stateno = 1402
trigger2 = enemynear,movetype = H
trigger2 = enemynear,life < 80
trigger3 = numhelper(8510)
trigger3 = helper(8510),stateno = 8511
trigger3 = enemynear,movetype = H
trigger3 = enemynear,life < 60

;------------------------------------------------------------------------------

[State -1, しゃがみ弱キック]
type = ChangeState
value = 430
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
Triggerall =EnemyNear,StateType != L
triggerall = P2statetype != A
trigger1 = ctrl || stateno = 100
trigger1 = P2bodydist X = [0,35]
trigger1 = P2MoveType = I && P2movetype != A
trigger1 = random = [0,400]
trigger2 = stateno = 430
trigger2 = movecontact && time > 7
trigger2 = P2bodydist X = [0,35]
trigger3 = stateno = 400
trigger3 = movecontact
trigger3 = P2bodydist X = [0,40]

;------------------------------------------------------------------------------
[State -1, しゃがみ弱パンチ]
type = ChangeState
value = 400
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
TriggerAll=EnemyNear,StateType != L
trigger1 = ctrl || stateno = 100
trigger1 = P2bodydist X = [0,50]
trigger1 = P2MoveType = I && P2statetype != A
trigger1 = random = [700,999]
trigger2 = prevstateno = 630
trigger2 = ctrl
trigger2 = EnemyNear,movetype = H
trigger2 = random = [500,999]

;------------------------------------------------------------------------------
[State -1, しゃがみ強キック]
type = ChangeState
value = 440
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = P2statetype = S
triggerall = P2bodydist X = [50,80]
TriggerAll=EnemyNear,StateType != L
trigger1 = statetype = C
trigger1 = ctrl 
trigger1 = random = [990,999]

;------------------------------------------------------------------------------



[State -1, ジャンプ弱キック]
type = ChangeState
value = 630
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = A
triggerall = p2statetype != A
triggerall = P2BodyDist X = [-40,30]
triggerall = P2BodyDist Y = [90,110]
triggerall = vel Y > 1
trigger1 = ctrl
trigger2 = p2statetype != A
trigger2 = time >= 5 && stateno = 2013

[State -1, ジャンプ強キック]
type = ChangeState
value = 640
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = A
trigger1 = p2statetype != A
trigger1 = P2BodyDist X = [-40,46]
trigger1 = P2BodyDist Y = [20,90]
trigger1 = vel Y > 1
trigger1 = ctrl
trigger2 = stateno = 630
trigger2 = movecontact
trigger2 = P2BodyDist X >= 0
trigger3 = p2statetype != A
trigger3 = P2BodyDist X = [-40,46]
trigger3 = P2BodyDist Y = [20,90]
trigger3 = vel Y > 1
trigger3 = p2statetype != A
trigger3 = time >= 5 && stateno = 2013

[State -1, エアトリック]
type = ChangeState
value = 2001
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = p2movetype != A
trigger1 = ctrl
trigger1 = random = [820,835]

[State -1, エアトリック]
type = ChangeState
value = 2000
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = p2movetype != A
trigger1 = ctrl
trigger1 = random = [800,815]


[State -1, トリックダウン]
type = ChangeState
value = 2040
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = ctrl
triggerall = enemynear,numproj = 0
trigger1 = enemynear,HitDefAttr = SCA, AA,AT
trigger1 = P2BodyDist X = [0,50]
trigger1 = random < 50

[State -3,ジャンプ]
Type     = ChangeState
Value    = 40
TriggerAll=var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
TriggerAll=StateType!=A
TriggerAll=Ctrl||stateno = 100
TriggerAll=EnemyNear,HitDefAttr=SCA,AT
TriggerAll=Random<=var(59)*60||var(59)>9
TriggerAll=EnemyNear,Time>=30||(!Time&&var(59)>9)||var(59)>10
Trigger1 = EnemyNear,Time>=50||var(59)>10
Trigger2 = (PrevStateNo=[5000,5270])
Trigger3 = (PrevStateNo=[120,159])

[State -1, バックステップ]
type = ChangeState
value = 105
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = ctrl
triggerall = enemynear,numproj = 0
trigger1 = enemynear,HitDefAttr = SCA, AA,AT
trigger1 = P2BodyDist X = [0,50]
trigger1 = random < 50

[State -1, エアトリック空中]
type = ChangeState
value = 2010
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype = A
trigger1 = ctrl
trigger1 = random = [500,820]
trigger1 = enemynear,vel Y < 0


[State -1, 走る]
type = ChangeState
value = 100
triggerall = var(59)
triggerall = var(52) = 0
triggerall = roundstate = 2
triggerall = statetype != A
triggerall = stateno != [100,101]
trigger1 = ctrl
trigger1 = P2BodyDist X >=150
trigger1 = enemynear,movetype != A
trigger1 = random = [600,820]
trigger2 = ctrl
trigger2 = numhelper(1401)
trigger2 = helper(1401),stateno = 1402

;------------------------------------------------------------------------------
;Ｍ２０モード時限定
[State -1, 兜割り５連]
type = ChangeState
value = 4010
triggerall = var(52)
triggerall = roundstate = 2
triggerall = helper(4101),var(13) > 40
trigger1 = stateno = 4100 || stateno = 4120
trigger1 = life >= 150
trigger1 = random%10 = [0,2]
trigger2 = stateno = 4100 || stateno = 4120
trigger2 = life < 150
trigger2 = random%20 = 0

[State -1, 切り上げコンボ]
type = ChangeState
value = 4020
triggerall = var(52)
triggerall = roundstate = 2
triggerall = helper(4101),var(13) > 40
trigger1 = stateno = 4100 || stateno = 4120
trigger1 = P2BodyDist X <=40
trigger1 = random%10 = [2,3]

[State -1, 絶刀]
type = ChangeState
value = 4050
triggerall = var(52)
triggerall = roundstate = 2
triggerall = helper(4101),var(13) > 40
trigger1 = stateno = 4100 || stateno = 4120
trigger1 = random%10 = [7,9]
trigger2 = stateno = 4100 || stateno = 4120
trigger2 = life < 150
trigger2 = random%10 = [3,9]

[State -1, 幻影剣]
type = ChangeState
value = 4040
triggerall = var(52)
triggerall = roundstate = 2
triggerall = numhelper(8500) = 0
triggerall = numhelper(8510) = 0
triggerall = helper(4101),var(13) > 40
trigger1 = stateno = 4100 || stateno = 4120
trigger1 = random%10 = [4,7]

[State -1, 歩く]
type = ChangeState
value = 4120
triggerall = var(52)
triggerall = roundstate = 2
trigger1 = stateno = 4100
trigger1 = P2BodyDist X >=100
trigger1 = random = [800,820]

[State -1, エアトリック]
type = ChangeState
value = 4130
triggerall = var(52)
triggerall = roundstate = 2
trigger1 = stateno = 4100 || stateno = 4120
trigger1 = P2BodyDist X >=100
trigger1 = random = [800,815]
;------------------------------------------------------------------------------
;------------------------------------------------------------------------------
;人操作
;==============================================================================
; 超必殺技
;==============================================================================
;------------------------------------------------------------------------------
[State -1, 絶刀]
type = ChangeState
value = 3500
triggerall = var(59) = 0
triggerall = command = "TripleKFPalm"
triggerall = power >= 3000
trigger1 = statetype != A
trigger1 = ctrl

[State -1, DT兜割り]
type = ChangeState
value = 3300
triggerall = var(59) = 0
triggerall = command = "DTkabuto"
triggerall = power >= 2000
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = var(18) = 1

[State -1, DT疾走居合い]
type = ChangeState
value = 3200
triggerall = var(59) = 0
triggerall = command = "DTsissou"
triggerall = power >= 1000
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = stateno = 901
trigger2 = time > 10
trigger3 = (stateno = 201) && time > 5
trigger3 = movecontact
trigger4 = (stateno = 300) && time > 30
trigger4 = movecontact
trigger5 = (stateno = 430)
trigger5 = movecontact
trigger6 = var(18) = 1

[State -1, 1ゲージ絶刀]
type = ChangeState
value = 3000
triggerall = var(59) = 0
triggerall = command = "Zettou"
triggerall = power >= 1000
trigger1 = ctrl
trigger2 = (stateno = 201) && time > 5
trigger2 = movecontact
trigger3 = (stateno = 300) && time > 30
trigger3 = movecontact
trigger4 = stateno = [600,610]
trigger4 = movecontact
trigger5 = stateno = 2600
trigger5 = movecontact
trigger6 = stateno = 2610 && time > 38
trigger6 = movecontact


[State -1, エネステ流星脚]
type = ChangeState
value = 3050
triggerall = var(59) = 0
triggerall = command = "ESryusei"
triggerall = power >= 1000
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = [1500,1501)
trigger2 = movehit

[State -1, 挑発→円陣展開]
type = ChangeState
value = 2900
triggerall = var(59) = 0
triggerall = command = "TyouhatuEnjin"
triggerall = power >= 1000
triggerall = var(56) = 0
trigger1 = statetype = S
trigger1 = ctrl

;==============================================================================
; 必殺技
;==============================================================================
[State -1, ラウンドトリップ]
type = ChangeState
value = 1400
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "trip"
triggerall = statetype != A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
trigger1 = ctrl
ignorehitpause = 0

;------------------------------------------------------------------------------

[State -1, 日輪脚弱]
type = ChangeState
value = 2600
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "cutter1"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 410 || stateno = 231
trigger2 = movecontact
ignorehitpause = 0

;------------------------------------------------------------------------------

[State -1, 日輪脚強]
type = ChangeState
value = 2610
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "cutter2"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 410 || stateno = 231
trigger2 = movecontact
ignorehitpause = 0

;------------------------------------------------------------------------------
[State -1, 飛び道具かき消し]
type = ChangeState
value = 950
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "upper_x"
triggerall = statetype != A
trigger1 = ctrl
ignorehitpause = 0

;------------------------------------------------------------------------------

[State -1, 次元斬]
type = ChangeState
value = 1000
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "QCF_x" || Command = "QCF_y"|| Command = "ryusei1"|| Command = "ryusei2"
trigger1 = ctrl
trigger1 = statetype != A
trigger2 = var(18) = 1

;------------------------------------------------------------------------------

[State -1, スティンガー]
type = ChangeState
value = 1100
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "QCB_x"
triggerall = statetype != A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
trigger1 = ctrl
trigger2 = stateno = [200,201]
trigger2 = time > 10
trigger3 = (stateno = 300) && time > 30
trigger3 = movecontact
trigger4 = (stateno = 430) || (stateno = 440)
trigger4 = movecontact && time > 5
trigger5 = var(18) = 1

;------------------------------------------------------------------------------

[State -1, 疾走居合い切り]
type = ChangeState
value = 1200
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "QCB_y"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 901
trigger2 = time > 10
trigger3 = (stateno = 201) && time > 5
trigger3 = movecontact
trigger4 = (stateno = 300) && time > 30
trigger4 = movecontact
trigger5 = var(18) = 1

;------------------------------------------------------------------------------

[State -1, 兜割り]
type = ChangeState
value = 1300
triggerall = command = "down_x"
triggerall = var(59) = 0
triggerall = pos Y < -30
triggerall = roundstate = 2
triggerall = statetype = A
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = movecontact
trigger3 = stateno = 1501
trigger3 = AnimElemTime(6) < 0
ignorehitpause = 0

;------------------------------------------------------------------------------

;流星脚
[State -1, Hadousho]
type = ChangeState
value = 1500
triggerall = var(59) = 0
triggerall = pos Y < -30
triggerall = roundstate = 2
triggerall = Command = "ryusei1" || Command = "ryusei2"
triggerall = statetype = A
trigger1 = ctrl
trigger2 = stateno = 2610
trigger2 = movecontact
trigger2 = time > 38
ignorehitpause = 0

;------------------------------------------------------------------------------

;月輪脚弱
[State -1, Hadousho]
type = ChangeState
value = 2500
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "geturin1"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 410 || stateno = 231 || stateno = 440
trigger2 = movecontact
ignorehitpause = 0
;------------------------------------------------------------------------------
;月輪脚強
[State -1, Hadousho]
type = ChangeState
value = 2505
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = Command = "geturin2"
triggerall = statetype != A
trigger1 = ctrl
trigger2 = stateno = 410 || stateno = 231 || stateno = 440
trigger2 = movecontact
ignorehitpause = 0



;==============================================================================
; 特殊技
;==============================================================================

[State -1, フォースエッジコンボ１]
type = ChangeState
value = 300
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "front_x"
triggerall = command != "holddown"
triggerall = numhelper(1401) = 0
triggerall = var(10) = 0
trigger1 = statetype = S
trigger1 = ctrl


;==============================================================================
; 移動関連
;==============================================================================
;------------------------------------------------------------------------------

[State -1, 走る]
type = ChangeState
value = 100
triggerall = Var(59) = 0
trigger1 = command = "FF"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, バックステップ]
type = ChangeState
value = 105
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "BB"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, トリックアップ]
type = ChangeState
value = 2020
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "trickup"
trigger1 = statetype = S
trigger1 = var(16) = 0
trigger1 = ctrl

[State -1, トリックアップ空中]
type = ChangeState
value = 2030
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = var(16) = 0
triggerall = command = "trickup"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = [2600,2610]
trigger2 = movehit


[State -1, エアトリック]
type = ChangeState
value = 2000
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "front_c"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, エアトリック空中]
type = ChangeState
value = 2010
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "front_c"
trigger1 = statetype = A
trigger1 = ctrl


[State -1, トリックダウン]
type = ChangeState
value = 2040
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "back_c"
trigger1 = statetype = S
trigger1 = ctrl

[State -1, トリックダウン空中]
type = ChangeState
value = 2050
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "back_c"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = [2600,2610]
trigger2 = movehit && time > 20

[State -1, エアトリック]
type = ChangeState
value = 2001
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "c"
trigger1 = statetype = S
trigger1 = ctrl
;==============================================================================
; 特殊技
;==============================================================================
;------------------------------------------------------------------------------

[State -1, カンフースルー];投げ技
type = ChangeState
value = 800
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "b+y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = command = "holdfwd"
trigger1 = p2bodydist X < 20
trigger1 = (p2statetype = S) || (p2statetype = C)
trigger1 = p2movetype != H
trigger2 = command = "holdback"
trigger2 = p2bodydist X < 20
trigger2 = (p2statetype = S) || (p2statetype = C)
trigger2 = p2movetype != H

;------------------------------------------------------------------------------
[State -1, 弾き]
type = ChangeState
value = 900
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "front_z"
triggerall = statetype != A
trigger1 = ctrl


;受身
[State -1]
type = ChangeState
value = 702
triggerall = var(59) = 0
triggerall = Alive
triggerall = StateNo = 5050 || StateNo = 5071 || StateNo = 5101
triggerall = Vel Y >= 0
triggerall = Pos Y >= -15
triggerall = CanRecover
trigger1 = command = "recovery"
persistent = 0

;==============================================================================
; 通常攻撃技
;==============================================================================
;------------------------------------------------------------------------------

[State -1, 立ち弱パンチ]
type = ChangeState
value = 200
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "x"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = stateno = 231
trigger2 = movecontact && time > 20

[State -1, 立ち強パンチ]
type = ChangeState
value = 210
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "y"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = (stateno = 201) && time > 14
trigger4 = (stateno = 230) && time > 6

[State -1, 立ち弱キック]
type = ChangeState
value = 230
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "a"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl


[State -1, 立ち強キック]
type = ChangeState
value = 240
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "b"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl
trigger2 = (stateno = 231) && time > 15

;------------------------------------------------------------------------------

[State -1, 挑発]
type = ChangeState
value = 195
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "start"
trigger1 = statetype != A
trigger1 = ctrl

;------------------------------------------------------------------------------

[State -1, しゃがみ弱パンチ]
type = ChangeState
value = 430
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "x"
trigger1 = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 430
trigger2 = var(7) = 1 && time > 7

[State -1, しゃがみ強パンチ]
type = ChangeState
value = 410
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "y"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger1 = stateno != 411 
trigger2 = (stateno = 400) || (stateno = 430) || (stateno = 440)
trigger2 = movecontact
trigger3 = stateno = 201
trigger3 = movecontact && time > 15
trigger4 = stateno = 901
trigger4 = time > 10

[State -1, しゃがみ弱キック]
type = ChangeState
value = 430
triggerall = var(59) = 0
triggerall = roundstate = 2
trigger1 = command = "a"
trigger1 = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = stateno = 430
trigger2 = var(7) = 1 && time > 7

[State -1, しゃがみ強キック]
type = ChangeState
value = 440
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "b"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl
trigger2 = (stateno = 400) || (stateno = 430)
trigger2 = movecontact || time > 7

;------------------------------------------------------------------------------

[State -1, ジャンプ弱パンチ]
type = ChangeState
value = 600
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "x"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600
trigger2 = statetime >= 10
trigger2 = movehit
trigger2 = P2BodyDist X <= 40

[State -1, ジャンプ強パンチ]
type = ChangeState
value = 610
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "y"
trigger1 = stateno = 600
trigger1 = movecontact
trigger2 = statetype = A
trigger2 = ctrl

[State -1, ジャンプ弱キック]
type = ChangeState
value = 630
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "a"
trigger1 = statetype = A
trigger1 = ctrl

[State -1, ジャンプ強キック]
type = ChangeState
value = 640
triggerall = var(59) = 0
triggerall = roundstate = 2
triggerall = command = "b"
trigger1 = statetype = A
trigger1 = ctrl
trigger2 = stateno = 600 || stateno = 630
trigger2 = movecontact

;------------------------------------------------------------------------------
;------------------------------------------------------------------------------
;------------------------------------------------------------------------------
