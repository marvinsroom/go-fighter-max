"""Build Zoro on the fixed-scale authored-fighter runtime used by older Game1 fighters."""
from pathlib import Path
from PIL import Image
import hashlib, json, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
LIVE = GAME / "engine/ikemen-go-v1.0.0/chars/zoro"
ART = GAME / "style-expansion/zoro/conversion-v1"
OUT = GAME / "characters/zoro/refactor-v2"
POSES = OUT / "poses"
POSES.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "scripts"))
from edward_assets import write_v2

def cells(path):
    sheet = Image.open(path).convert("RGBA")
    result = []
    for row in range(4):
        for col in range(4):
            # Generated poses routinely cross the visual grid line (especially boots
            # and airborne legs).  Give every cell overlap, then keep only connected
            # artwork whose component reaches that cell's original core.
            x0, x1 = round(col*sheet.width/4), round((col+1)*sheet.width/4)
            y0, y1 = round(row*sheet.height/4), round((row+1)*sheet.height/4)
            pad = 72
            left, top = max(0, x0-pad), max(0, y0-pad)
            right, bottom = min(sheet.width, x1+pad), min(sheet.height, y1+pad)
            expanded = sheet.crop((left, top, right, bottom))
            alpha = expanded.getchannel("A")
            mask = alpha.point(lambda value: 255 if value else 0)
            pixels = mask.load(); width, height = mask.size
            seen = bytearray(width*height); kept = Image.new("L", mask.size)
            kept_pixels = kept.load()
            core = (x0-left, y0-top, x1-left, y1-top)
            for sy in range(height):
                for sx in range(width):
                    key = sy*width+sx
                    if seen[key] or not pixels[sx,sy]: continue
                    stack=[(sx,sy)]; seen[key]=1; component=[]; touches_core=False
                    while stack:
                        px,py=stack.pop(); component.append((px,py))
                        if core[0] <= px < core[2] and core[1] <= py < core[3]: touches_core=True
                        for nx,ny in ((px-1,py),(px+1,py),(px,py-1),(px,py+1)):
                            if 0 <= nx < width and 0 <= ny < height:
                                nk=ny*width+nx
                                if not seen[nk] and pixels[nx,ny]: seen[nk]=1; stack.append((nx,ny))
                    if touches_core and len(component) >= 12:
                        for px,py in component: kept_pixels[px,py]=255
            expanded.putalpha(Image.composite(alpha, Image.new("L", alpha.size), kept))
            tile = expanded
            box = tile.getchannel("A").getbbox()
            if not box:
                raise RuntimeError(f"Empty cell {row},{col} in {path}")
            # Preserve the original cell center as the fighter pivot. Effects may
            # widen a frame, but must never drag the character sideways.
            pivot_x = ((x0+x1)//2-left)-box[0]
            result.append((tile.crop(box), pivot_x))
    return result

body, supers, effects = cells(ART/"body-v2.png"), cells(ART/"supers-v3.png"), cells(ART/"effects-v1.png")
sprites=[]; meta={}
def visible_height(item):
    image,_ = item
    box=image.getchannel("A").getbbox()
    return max(1,box[3]-box[1])

# One pixels-to-world ratio for every pose. This is the key difference from
# per-frame normalization, which made crouches swell and tall attacks shrink.
fighter_scale = 160/visible_height(body[0])

def add(name, group, number, item, scale, axis_y=True):
    image,pivot_x=item
    path=POSES/f"{name}.png"; image.save(path)
    box=image.getchannel("A").getbbox()
    axis=(max(0,min(image.width-1,pivot_x)),box[3] if axis_y else image.height//2)
    sprites.append(dict(key=(group,number),axis=axis,image=image))
    meta[name]=dict(group=group,number=number,axis=axis,source_size=image.size,scale=scale,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
for i,item in enumerate(body): add(f"body-{i:02d}",0,i,item,fighter_scale)
for i,item in enumerate(supers): add(f"super-{i:02d}",1,i,item,fighter_scale)
for i,item in enumerate(effects): add(f"effect-{i:02d}",7000,i,item,fighter_scale,False)
portrait=Image.open(GAME/"style-expansion/zoro/design-reference-v1.png").convert("RGBA"); portrait=portrait.crop(portrait.getchannel("A").getbbox())
for number,size in ((0,200),(1,900)):
    canvas=Image.new("RGBA",(size,size)); fit=portrait.copy()
    if number==0:
        fit=fit.crop((int(fit.width*.18),0,int(fit.width*.82),int(fit.height*.42)))
    fit.thumbnail((int(size*.86),int(size*.86)),Image.Resampling.LANCZOS); canvas.alpha_composite(fit,((size-fit.width)//2,(size-fit.height)//2))
    add(f"portrait-{number}",9000,number,(canvas,canvas.width//2),1,False)
write_v2(LIVE/"Zoro.sff",sprites)

def frame(bank,index,ticks):
    m=meta[f"{bank}-{index:02d}"]; return f'{m["group"]},{m["number"]},0,0,{ticks},,,{m["scale"]:.7f},{m["scale"]:.7f}'
air=[]
def action(number, sequence, active=(), kind="S", attack=(-10,-150,190,-20), hurt=True):
    air.append(f"\n[Begin Action {number}]")
    for i,(bank,pose,ticks) in enumerate(sequence):
        if hurt:
            box=(-34,-105,34,0) if kind!="C" else (-38,-78,38,0)
            air.extend(["Clsn2: 1","Clsn2[0] = "+",".join(map(str,box))])
        if i in active: air.extend(["Clsn1: 1","Clsn1[0] = "+",".join(map(str,attack))])
        air.append(frame(bank,pose,ticks))
common={0:[("body",0,8),("body",1,8),("body",2,8),("body",3,8)],5:[("body",0,-1)],10:[("body",15,4)],11:[("body",15,-1)],12:[("body",15,4),("body",0,5)],20:[("body",4,5),("body",5,5),("body",6,5),("body",7,5)],21:[("body",7,5),("body",6,5),("body",5,5),("body",4,5)],40:[("body",4,4)],41:[("body",5,4)],42:[("body",6,4)],43:[("body",7,4)],47:[("body",6,4)],50:[("body",6,-1)],51:[("body",6,-1)],52:[("body",7,4),("body",0,5)],100:[("body",4,3),("body",5,3),("body",6,3),("body",7,3)],105:[("body",7,3),("body",6,3),("body",5,3),("body",4,3)],120:[("body",8,3)],130:[("body",8,-1)],131:[("body",8,3)],132:[("body",8,3)],140:[("body",15,-1)],141:[("body",15,3)],142:[("body",15,3)],150:[("body",13,-1)],151:[("body",13,3)],152:[("body",13,3)],170:[("body",14,-1)],175:[("body",14,-1)],180:[("body",0,-1)],181:[("body",0,-1)],190:[("body",0,50)],191:[("body",0,1)]}
for n,seq in common.items(): action(n,seq,kind="C" if n in (10,11,12,140,141,142) else "A" if n in (41,42,43,47,50,51,52,150,151,152) else "S")
for n in (5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090,5100,5110,5120,5140,5150,5160,5170,5200,5210,5220,5300,5500,5510): action(n,[("body",12 if n<5100 else 13,8),("body",14,8),("body",15,-1)],kind="A" if n in (5030,5040,5050) else "S")
action(200,[("body",8,4),("body",9,4),("body",11,8)],(1,),attack=(0,-120,115,-45))
action(210,[("body",8,5),("body",10,5),("body",11,9)],(1,),attack=(0,-145,170,-20))
action(220,[("body",8,6),("body",9,4),("body",10,5),("body",11,10)],(1,2),attack=(-15,-175,185,-10))
action(400,[("body",15,5),("body",9,5),("body",15,9)],(1,),kind="C",attack=(0,-75,120,-5))
action(600,[("body",8,5),("body",9,5),("body",11,9)],(1,),kind="A",attack=(0,-150,145,-25))
action(700,[("body",1,8),("body",0,8)])
action(1000,[("body",8,6),("body",9,5),("body",11,8),("body",0,10)],(1,),attack=(0,-160,210,-15))
action(1100,[("body",8,7),("body",10,6),("body",11,9),("body",0,10)],(1,),attack=(-20,-190,190,-10))
action(1200,[("body",8,7),("body",9,5),("body",10,5),("body",11,9),("body",0,11)],(1,2),attack=(-100,-150,150,-5))
action(3000,[("super",0,10),("super",1,5),("super",2,6),("super",3,15)],(1,2),attack=(-20,-170,250,-5))
action(3100,[("super",4,12),("super",5,7),("super",6,7),("super",7,18)],(1,2),attack=(-150,-210,180,10))
action(3200,[("super",8,18),("super",9,5),("super",10,7),("super",11,12),("super",12,6),("super",13,5),("super",14,8),("super",15,22)],(1,2,4,5,6),attack=(-90,-210,300,5))
for i in range(16): action(9000+i,[("effect",i,-1)],hurt=False)
(LIVE/"Zoro.air").write_text("\n".join(air)+"\n",encoding="utf-8")

def state(n,anim=None,stype="S",move="I",physics=None,**values):
    global cns
    cns+=f"\n[Statedef {n}]\ntype={stype}\nmovetype={move}\nphysics={physics or ('A' if stype=='A' else 'C' if stype=='C' else 'S')}\nctrl=0\n"
    if anim is not None:cns+=f"anim={anim}\n"
    cns+="".join(f"{k}={v}\n" for k,v in values.items())
def ctl(n,label,kind,triggers="1",**values):
    global cns
    cns+=f"\n[State {n}, {label}]\ntype={kind}\n"+"".join(f"trigger1={t}\n" for t in ([triggers] if isinstance(triggers,str) else triggers))+"".join(f"{k.replace('__','.')}={v}\n" for k,v in values.items())
def finish(n,air=False,crouch=False):
    ctl(n,"Land","ChangeState",["vel y>0","pos y>=0"],value=52,ctrl=1) if air else None
    ctl(n,"Recover","ChangeState","animtime=0",value=11 if crouch else 0,ctrl=1)
def hit(n,t,damage,attr="S,NA",guard="MA",fall=0,velocity="1,0"):
    ctl(n,"Contact","HitDef",f"time={t}",attr=attr,damage=f"{damage},5",guardflag=guard,hitflag="MAF",pausetime="4,7",animtype="Hard" if fall else "Medium",ground__type="High",ground__hittime=24,ground__slidetime=12,ground__velocity=velocity,air__velocity="2,-4",fall=fall,sparkno=2,guard__sparkno=40,hitsound="S1,0",guardsound="S1,1",getpower="0,0" if attr.endswith("HA") else "20,5",givepower="10,5")
cns='''[Data]\nlife=1000\npower=3000\nattack=100\ndefence=100\nfall.defence_up=50\nliedown.time=40\nairjuggle=15\nsparkno=2\nguard.sparkno=40\nKO.echo=0\nvolume=0\n[Size]\nxscale=1\nyscale=1\nground.back=38\nground.front=38\nair.back=34\nair.front=34\nheight=150\nattack.dist=180\nproj.attack.dist=220\nproj.doscale=1\nhead.pos=0,-135\nmid.pos=0,-75\nshadowoffset=0\ndraw.offset=0,0\n[Velocity]\nwalk.fwd=4.5\nwalk.back=-3.5\njump.neu=0,-10.5\njump.fwd=4,-10.5\njump.back=-3.5,-10.5\n[Movement]\nyaccel=.55\nstand.friction=.85\ncrouch.friction=.82\nairjump.num=0\nstand.friction.threshold=.1\n'''
state(-2,physics="N");ctl(-2,"Face opponent","Turn",["ctrl","statetype!=A","p2dist x<0"]);ctl(-2,"Authored movement","AssertSpecial",flag="nowalk",flag2="nobrake",flag3="noautoturn")
state(0,0,velset="0,0");ctl(0,"Control","CtrlSet",value=1);ctl(0,"Crouch","ChangeState","command=\"holddown\"",value=10);ctl(0,"Jump","ChangeState","command=\"holdup\"",value=40);ctl(0,"Walk","ChangeState","command=\"holdfwd\" || command=\"holdback\"",value=20)
state(10,10,stype="C");ctl(10,"Settle","ChangeState","animtime=0",value=11,ctrl=1);state(11,11,stype="C");ctl(11,"Control","CtrlSet",value=1);ctl(11,"Stand","ChangeState","command!=\"holddown\"",value=12);state(12,12,stype="C");ctl(12,"Stand","ChangeState","animtime=0",value=0,ctrl=1)
state(20,20,velset="0,0");ctl(20,"Control","CtrlSet",value=1);ctl(20,"Move","VelSet",x="ifelse(command=\"holdback\",-3.5,4.5)",y=0);ctl(20,"Back art","ChangeAnim","command=\"holdback\" && anim!=21",value=21);ctl(20,"Forward art","ChangeAnim","command=\"holdfwd\" && anim!=20",value=20);ctl(20,"Stop","ChangeState","command!=\"holdfwd\" && command!=\"holdback\"",value=0,ctrl=1)
state(40,40);ctl(40,"Launch","VelSet","time=3",x="ifelse(command=\"holdback\",-3.5,ifelse(command=\"holdfwd\",4,0))",y=-10.5);ctl(40,"Air","ChangeState","time>=3",value=50)
state(50,50,stype="A",physics="A");ctl(50,"Control","CtrlSet",value=1);ctl(50,"Land","ChangeState",["vel y>0","pos y>=0"],value=52);state(52,52);ctl(52,"Ground","PosSet",y=0);finish(52)
for n,speed in ((100,12),(105,-10)):
    state(n,n,velset="0,0");ctl(n,"Dash","VelSet","time<8",x=speed);ctl(n,"Stop","VelSet","time=8",x=0);finish(n)
state(190,190,velset="0,0");ctl(190,"Intro","AssertSpecial","roundstate<2 && time<45",flag="intro");finish(190)
for n in (180,181):state(n,180,velset="0,0");ctl(n,"Victory","NotHitBy",value="SCA",time=1)
for n,anim,t,damage in ((200,200,5,35),(210,210,6,55),(220,220,7,80),(400,400,5,42)):
    state(n,anim,stype="C" if n==400 else "S",move="A",velset="0,0");hit(n,t,damage,guard="L" if n==400 else "MA",fall=int(n==220),velocity="3,-4" if n==220 else "1,0");finish(n,crouch=n==400)
state(600,600,stype="A",move="A",physics="A");hit(600,5,50,guard="H",fall=1,velocity="2,-4");finish(600,air=True)
state(700,700,velset="0,0");ctl(700,"Charge","PowerAdd",value=18);ctl(700,"Release","ChangeState","command!=\"holdcharge\" || power>=3000",value=0,ctrl=1)
for n,t,damage,cost in ((1000,6,85,250),(1100,7,105,500),(1200,7,125,750)):
    state(n,n,move="A",poweradd=-cost,velset="0,0");ctl(n,"Advance","VelSet",f"time=[{t-2},{t+3}]",x=8 if n==1000 else 3);hit(n,t,damage,attr="S,SA",fall=int(n!=1000),velocity="4,-5" if n!=1000 else "2,0");finish(n)
for n,cost,times,damages in ((3000,1000,(10,15),(70,80)),(3100,2000,(12,19,26),(65,65,120)),(3200,3000,(18,25,37,49,58),(45,45,55,55,160))):
    state(n,n,move="A",poweradd=-cost,velset="0,0");ctl(n,"Super pause","SuperPause","time=0",time=12 if n<3200 else 20,movetime=12 if n<3200 else 20,anim=-1,sound="S1,2",darken=1,poweradd=0)
    for i,t in enumerate(times):
        hit(n,t,damages[i],attr="S,HA",fall=int(i==len(times)-1),velocity="5,-7" if i==len(times)-1 else "0,0");ctl(n,"Impact","EnvShake",f"movehit && time={t}",time=4 if n<3200 else 7,freq=90,ampl=3 if n<3200 else 5)
    ctl(n,"Drive","VelSet",f"time=[{times[0]-3},{times[-1]}]",x=8 if n==3000 else 2);ctl(n,"Stop","VelSet",f"time={times[-1]+1}",x=0);finish(n)
(LIVE/"Zoro.cns").write_text(cns,encoding="utf-8")

commands={"L":"a","M":"b","H":"c","skill":"x","rising":"/$D,x","cyclone":"/$B,x","super":"y","tatsumaki":"/$B,y","ultimate":"z","holdcharge":"/s","FF":"F,F","BB":"B,B","holdfwd":"/$F","holdback":"/$B","holddown":"/$D","holdup":"/$U"}
cmd="[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=15\ncommand.buffer.time=4\n"
for name,value in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={value}\ntime={15 if "," in value else 1}\n'
cmd+="\n[Statedef -1]\n"
def route(label,name,n,conditions):
    global cmd
    cmd+=f"\n[State -1, {label}]\ntype=ChangeState\n"+"".join(f"triggerall={c}\n" for c in conditions)+f'trigger1=command="{name}"\nvalue={n}\nctrl=0\n'
ground=["roundstate=2","statetype!=A","ctrl","ailevel=0"]
route("San Zen Sekai","ultimate",3200,ground+["power>=3000"]);route("Kokujou Oo Tatsumaki","tatsumaki",3100,ground+["power>=2000"]);route("Rokudou no Tsuji","super",3000,ground+["power>=1000","command!=\"holdback\""])
route("Three Sword Cyclone","cyclone",1200,ground+["power>=750"]);route("Rising Dragon","rising",1100,ground+["power>=500"]);route("Oni Giri","skill",1000,ground+["power>=250","command!=\"holdback\"","command!=\"holddown\""])
route("Charge","holdcharge",700,ground+["power<3000"]);route("Forward dash","FF",100,ground);route("Back dash","BB",105,ground)
for label,name,n in (("Crouching cut","L",400),("Heavy cut","H",220),("Sword cut","M",210),("Quick strike","L",200)): route(label,name,n,ground+(["command=\"holddown\""] if n==400 else ["command!=\"holddown\""]))
route("Air cut","L",600,["roundstate=2","statetype=A","ctrl","ailevel=0"])
for n,conditions in ((3200,["power>=3000","p2bodydist x<230","random<15"]),(3000,["power>=1000","p2bodydist x<260","random<30"]),(1000,["power>=250","p2bodydist x<220","random<40"]),(210,["p2bodydist x<160","random<60"]),(20,["p2bodydist x>=160"])):
    cmd+=f"\n[State -1, CPU]\ntype=ChangeState\ntriggerall=roundstate=2\ntriggerall=ctrl\ntriggerall=statetype!=A\ntriggerall=ailevel>0\n"+"".join(f"triggerall={c}\n" for c in conditions)+f"trigger1=1\nvalue={n}\nctrl=0\n"
(LIVE/"Zoro.cmd").write_text(cmd,encoding="utf-8")

(LIVE/"zoro.def").write_text('''[Info]\nname="Roronoa Zoro"\ndisplayname="Zoro"\nauthor="CobraG6; Game1 fixed-scale refactor"\nmugenversion=1.1\nlocalcoord=533,399.75\nportraitscale=.125\n[Files]\nsprite=Zoro.sff\nanim=Zoro.air\nsound=Zoro.snd\ncmd=Zoro.cmd\ncns=Zoro.cns\nst=Zoro.cns\nstcommon=common1.cns.zss\n[Arcade]\n''',encoding="utf-8")
common=GAME/"engine/ikemen-go-v1.0.0/data/common1.cns.zss"
shutil.copy2(common,LIVE/"common1.cns.zss")
report={"status":"BUILT","revision":"zoro-jinwoo-parity-refactor-v3","coordinate_space":[533,399.75],"body_world_height":160,"fixed_fighter_scale":fighter_scale,"sprite_count":len(sprites),"audit":{"reference":"jinwoo","fixed_sequence_scale":True,"body_centered_pivots":True,"coherent_body_rows":True,"dedicated_super_rows":True,"duplicate_effect_overlays":False},"moves":{"1000":"Oni Giri","1100":"Rising Dragon","1200":"Three Sword Cyclone","3000":"Rokudou no Tsuji","3100":"Kokujou Oo Tatsumaki","3200":"San Zen Sekai"},"runtime_sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [LIVE/"zoro.def",LIVE/"Zoro.sff",LIVE/"Zoro.air",LIVE/"Zoro.cns",LIVE/"Zoro.cmd",LIVE/"Zoro.snd"]},"art":meta,"preserved_audio":"Original CobraG6 Zoro.snd"}
(OUT/"build-report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"status":report["status"],"sprites":len(sprites),"body_world_height":160,"moves":report["moves"]},indent=2))
