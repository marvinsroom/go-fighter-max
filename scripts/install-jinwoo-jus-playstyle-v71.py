"""Install the JUS-style Jinwoo playstyle pass (v71).

Reference: Protozoark's "Solo Leveling Sung Jin-Woo [JUS MUGEN]" showcase
(youtube.com/watch?v=0gBpCa72pSc), studied frame by frame.  Nothing from that
video is copied; this pass only re-choreographs our own build to match it:

* No bare-hand style.  The longsword is the default and the weapon swap only
  alternates longsword <-> Antares daggers.
* Video intro: sword planted at his side, palm opens a blue inventory portal,
  sword thrust out, second portal, sword rests on the shoulder.
* Heavier hit physics: longer hit pause, screen shake, more push, higher
  launchers, bigger ground bounce on spikes.
* Launcher air chase: hold up when a launcher connects to super-jump after
  the opponent, then continue with air attacks.
* Shadow escort: summoning also leaves an Igris shadow on the field for ~12 s
  that follows Jinwoo and attacks in tandem with him.

Every run restores the live files from live-before-v71 first, so the pass is
idempotent and can be reverted by copying that folder back.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/jus-playstyle-v71"
BACKUP = ART / "live-before-v71"
FILES = ["anim.air", "cns.cns", "-2.cns", "our-shadows.cns", "cmd.cmd", "spr.sff"]

SWORD = "0.208072691,0.196294992"
SHADOW = "0.238095238,0.238095238"
PORTAL_GROUP = 61090
PORTAL_FRAMES = 8
PORTAL_SCALE = "0.17,0.17"

# Sword / dagger normals whose HitDefs get the heavier physics.
PHYSICS_STATES = {200, 210, 220, 230, 240, 241, 242, 300, 310, 320, 330, 340,
                  350, 410, 415, 420, 450, 600, 610, 620, 640}
LAUNCHERS = {340, 415}


# --------------------------------------------------------------------------
# Portal artwork
# --------------------------------------------------------------------------
def portal_frame(index: int) -> Image.Image:
    """Tall blue swirl, like the inventory gate in the reference intro."""
    w, h = 384, 512
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    nx, ny = (xx - cx) / (w * 0.30), (yy - cy) / (h * 0.44)
    r = np.sqrt(nx * nx + ny * ny)
    theta = np.arctan2(ny, nx)
    phase = index / PORTAL_FRAMES * 2 * math.pi
    swirl = 0.5 + 0.5 * np.sin(theta * 3 + r * 9 - phase * 3)
    streak = np.clip(swirl ** 3, 0, 1)
    ring = np.exp(-((r - 0.82) ** 2) / 0.02)
    body = np.clip(1.05 - r, 0, 1) ** 0.6
    alpha = np.clip(ring * 1.0 + body * (0.25 + 0.65 * streak), 0, 1)
    alpha *= np.clip((1.15 - r) * 4, 0, 1)
    core = np.exp(-(r ** 2) / 0.10)
    red = 40 + 140 * streak * body + 180 * ring
    green = 110 + 120 * streak * body + 140 * ring
    blue = np.full_like(r, 255)
    dark = core * 0.55
    rgb = np.stack([red * (1 - dark), green * (1 - dark), blue * (1 - dark * 0.6)], -1)
    rgba = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    image = Image.fromarray(rgba, "RGBA").filter(ImageFilter.GaussianBlur(1.2))
    return image


def encode(image: Image.Image, axis: tuple[int, int]) -> dict[str, object]:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


# --------------------------------------------------------------------------
# AIR
# --------------------------------------------------------------------------
NEW_ACTIONS = f"""
; JINWOO JUS PLAYSTYLE V71
; Reference intro: planted sword, inventory portal, thrust, shoulder rest.
[Begin Action 879970]
Clsn2Default: 1
Clsn2[0] = -12,-59,12,0
61017,6,0,0,26,,,{SWORD}
61017,8,0,0,30,,,{SWORD}
61017,9,0,0,26,,,{SWORD}
61017,6,0,0,20,,,{SWORD}
61017,8,0,0,26,,,{SWORD}
61017,11,0,0,6,,,{SWORD}
61017,0,0,0,-1,,,{SWORD}

; Inventory portal
[Begin Action 879971]
""" + "\n".join(f"{PORTAL_GROUP},{i},0,0,3,,,{PORTAL_SCALE}" for i in range(PORTAL_FRAMES)) + f"""

; Longsword -> daggers swap (no bare-hand frames)
[Begin Action 879972]
Clsn2Default: 1
Clsn2[0] = -12,-59,12,0
61017,0,0,0,4,,,{SWORD}
61017,8,0,0,6,,,{SWORD}
61017,11,0,0,4,,,{SWORD}
61016,6,0,0,4,,,0.167301691,0.157831784
61016,7,0,0,4,,,0.167301691,0.157831784
61016,0,0,0,16,,,0.167301691,0.157831784

; Igris escort idle
[Begin Action 879975]
Clsn2Default: 1
Clsn2[0] = -14,-80,14,0
61001,0,0,0,-1,,,{SHADOW}

; Igris escort walk
[Begin Action 879976]
Clsn2Default: 1
Clsn2[0] = -14,-80,14,0
""" + "\n".join(f"61001,{i},0,0,5,,,{SHADOW}" for i in range(1, 7)) + "\n"


# --------------------------------------------------------------------------
# CNS
# --------------------------------------------------------------------------
INTRO = """[Statedef 191]
type=S
physics=N
movetype=I
ctrl=0
velset=0,0
anim=879970
sprpriority=1
[State 191, Hold the introduction]
type=AssertSpecial
trigger1=1
flag=intro
[State 191, Feet on the floor]
type=PosSet
trigger1=1
y=0
[State 191, Longsword drawn]
type=VarSet
trigger1=!time
var(10)=20000
[State 191, First inventory portal]
type=Explod
trigger1=time=26
anim=879971
ID=879971
pos=30,-44
postype=p1
bindtime=-1
removetime=30
sprpriority=3
ownpal=1
[State 191, Second inventory portal]
type=Explod
trigger1=time=102
anim=879971
ID=879971
pos=30,-44
postype=p1
bindtime=-1
removetime=26
sprpriority=3
ownpal=1
[State 191, Portal sound]
type=PlaySnd
trigger1=time=26 || time=102
value=S5,52
volumescale=80
[State 191, Blade drawn]
type=PlaySnd
trigger1=time=56
value=S5,54
[State 191, Blade flash]
type=PalFX
trigger1=time=56 || time=128
time=8
add=30,40,90
[State 191, Ready line]
type=PlaySnd
trigger1=time=130
value=S0,61
channel=0
[State 191, Clean up an intro skip]
type=RemoveExplod
trigger1=roundstate=2
id=879971
[State 191, Finish arrival]
type=ChangeState
trigger1=time>=160 || roundstate=2
value=0
ctrl=1
"""

TOGGLE = """[Statedef 870220]
type=S
movetype=I
physics=S
anim=-1
ctrl=0
velset=0,0
[State 870220, Choose visible transition]
type=ChangeAnim
trigger1=time=0
; V71: no bare hands.  Daggers -> longsword, longsword -> daggers.
value=cond(var(10)>=20000,879972,876323)
[State 870220, Equip]
type=VarSet
trigger1=time=20
var(10)=cond(var(10)>=20000,10000,20000)
"""

GUARD = """[State -2, V71 longsword is the default weapon]
type=VarSet
triggerall=!ishelper && var(45)=0
triggerall=var(10)=0
triggerall=!(stateno=[180,199])
trigger1=movetype!=A
var(10)=20000
ignorehitpause=1
[State -2, V71 launcher air chase]
type=ChangeState
triggerall=!ishelper && var(45)=0 && !AILevel
triggerall=stateno=340 || stateno=415
triggerall=movehit && roundstate=2
trigger1=command="holdup"
value=879960
[State -2, V71 CPU air chase]
type=ChangeState
triggerall=!ishelper && var(45)=0 && AILevel
triggerall=stateno=340 || stateno=415
triggerall=movehit=[4,8] && roundstate=2
trigger1=random<600
value=879960

"""

ESCORT_ATTACKS = [
    # (state, source anim, contact times, damages, ground velocity, rush)
    (870791, 870700, [6], [60], ["-4,-5"], "x=4.5\ntrigger1=time=[1,14]"),
    (870792, 870720, [10], [70], ["-6,-7"], "x=3.0\ny=-2.2\ntrigger1=time=[1,10]"),
    (870793, 870740, [8, 16], [30, 55], ["-1,0", "-4,-5"], "x=2.4\ntrigger1=time=[1,16]"),
]


def escort_states() -> str:
    out = ["""
; JINWOO JUS PLAYSTYLE V71 - SHADOW ESCORT
; A summoned Igris shadow stays beside Jinwoo and attacks with him.
[Statedef 870790]
type=S
movetype=I
physics=N
ctrl=0
anim=879975
velset=0,0
sprpriority=-1
[State 870790, Age]
type=VarAdd
trigger1=1
var(3)=1
[State 870790, Escort leaves]
type=DestroySelf
trigger1=var(3)>=720
trigger2=root,var(45)>0
trigger3=!root,alive || roundstate>2
[State 870790, Cooldown]
type=VarAdd
trigger1=var(1)>0
var(1)=-1
[State 870790, Ground]
type=PosSet
trigger1=1
y=0
[State 870790, Face like Jinwoo]
type=Turn
trigger1=facing!=root,facing
[State 870790, Body width]
type=Width
trigger1=1
player=10,10
[State 870790, Follow Jinwoo]
type=VelSet
trigger1=1
x=facing*max(-3.6,min(3.6,((root,pos x)-30*(root,facing)-pos x)*0.14))
[State 870790, Stand]
type=ChangeAnim
trigger1=abs(vel x)<0.6 && anim!=879975
value=879975
[State 870790, Walk]
type=ChangeAnim
trigger1=abs(vel x)>=0.6 && anim!=879976
value=879976
[State 870790, Fade in]
type=Trans
trigger1=var(3)<14
trans=addalpha
alpha=var(3)*18,256-var(3)*18
[State 870790, Tandem strike with Jinwoo]
type=ChangeState
triggerall=var(1)=0 && roundstate=2 && numenemy
triggerall=enemynear,statetype!=L
triggerall=p2bodydist x<cond(root,movetype=A,95,45)
trigger1=root,movetype=A && root,stateno!=870100
trigger2=random<25
value=870791+(var(3)/7)%3
"""]
    for state, anim, times, damages, vels, rush in ESCORT_ATTACKS:
        lines = [f"""[Statedef {state}]
type=S
movetype=A
physics=N
ctrl=0
anim={anim}
velset=0,0
sprpriority=-1
[State {state}, Age]
type=VarAdd
trigger1=1
var(3)=1
[State {state}, Ground]
type=PosSet
trigger1=1
y=0
[State {state}, Shadow rush]
type=VelSet
{rush}
[State {state}, Brake]
type=VelSet
trigger1=time>18
x=0
y=0"""]
        for t, d, v in zip(times, damages, vels):
            fall = "1" if v.split(",")[1].strip() not in ("0",) else "0"
            lines.append(f"""[State {state}, Tandem contact]
type=HitDef
trigger1=time={t}
attr=S,SA
damage={d},0
hitflag=MAFD
guardflag=MA
priority=4,Hit
pausetime=8,10
sparkno=2
sparkxy=0,-35
hitsound=S5,13
guardsound=S5,13
ground.type=High
ground.hittime=18
ground.velocity={v}
air.velocity=-3,-4
air.juggle=2
fall={fall}
envshake.time=6
envshake.ampl=2
getpower=0,0
givepower=10,4""")
        lines.append(f"""[State {state}, Return to Jinwoo's side]
type=ChangeState
trigger1=time>=34
value=870790
[State {state}, Cooldown]
type=VarSet
trigger1=time>=34
var(1)=50
""")
        out.append("\n".join(lines))
    return "\n".join(out)


CHASE = """
; JINWOO JUS PLAYSTYLE V71 - LAUNCHER AIR CHASE
[Statedef 879960]
type=A
movetype=I
physics=N
ctrl=0
anim=41
velset=2.4,-10.2
[State 879960, Leap]
type=PlaySnd
trigger1=!time
value=S5,52
volumescale=60
[State 879960, Afterimage]
type=AfterImage
trigger1=!time
time=10
length=6
palbright=0,10,40
palcontrast=120,120,220
[State 879960, Rise]
type=VelAdd
trigger1=time>0
y=0.42
[State 879960, Air control]
type=ChangeState
trigger1=time>=5
value=50
ctrl=1
"""


def replace_statedef(text: str, number: int, body: str, keep_from: str | None = None) -> str:
    pattern = re.compile(r"(?ims)^\[Statedef\s+%d\].*?(?=^\[Statedef|\Z)" % number)
    match = pattern.search(text)
    assert match, number
    old = match.group(0)
    tail = ""
    if keep_from:
        idx = old.find(keep_from)
        assert idx >= 0, (number, keep_from)
        tail = old[idx:]
    return text[:match.start()] + body + ("\n" + tail if tail else "\n") + text[match.end():]


def tune_hitdef(block: str, state: int) -> str:
    def get(key: str) -> str | None:
        m = re.search(r"(?im)^\s*%s\s*=\s*([^\n;]*)" % re.escape(key), block)
        return m.group(1).strip() if m else None

    def put(key: str, value: str) -> None:
        nonlocal block
        pat = re.compile(r"(?im)^(\s*)%s\s*=\s*[^\n]*" % re.escape(key))
        if pat.search(block):
            block = pat.sub(lambda m: f"{m.group(1)}{key}={value}", block, count=1)
        else:
            block = block.rstrip("\n") + f"\n{key}={value}\n"

    def num(text: str | None, idx: int, default: float) -> float | None:
        if text is None:
            return default
        parts = [p.strip() for p in text.split(",")]
        if idx >= len(parts) or parts[idx] == "":
            return default
        try:
            return float(parts[idx])
        except ValueError:
            return None  # expression: leave alone

    falls = (get("fall") or "0").strip() == "1"
    p1, p2 = num(get("pausetime"), 0, 0), num(get("pausetime"), 1, 0)
    if p1 is not None and p2 is not None:
        want = (13, 15) if falls else (9, 11)
        put("pausetime", f"{int(max(p1, want[0]))},{int(max(p2, want[1]))}")

    gx, gy = num(get("ground.velocity"), 0, 0), num(get("ground.velocity"), 1, 0)
    if gx is not None and gy is not None:
        if state in LAUNCHERS or (falls and gy <= -7):
            put("ground.velocity", "-1.2,-10.6")
            put("air.velocity", "-1.2,-10.6")
        elif falls and gy > 0:
            put("fall.yvelocity", "-7.5")
            put("fall.envshake.time", "14")
            put("fall.envshake.ampl", "6")
        elif gy == 0 or not falls:
            put("ground.velocity", f"{round(gx * 1.5, 2)},{gy:g}" if gy else f"{round(gx * 1.5, 2)}")

    if get("envshake.time") is None:
        put("envshake.time", "12" if falls else "5")
        put("envshake.ampl", "4" if falls else "2")
        put("envshake.freq", "120")
    return block


def tune_physics(text: str) -> tuple[str, list[str]]:
    report = []
    pieces = re.split(r"(?im)^(?=\[Statedef )", text)
    for i, piece in enumerate(pieces):
        m = re.match(r"\[Statedef\s+(-?\d+)", piece, re.I)
        if not m or int(m.group(1)) not in PHYSICS_STATES:
            continue
        state = int(m.group(1))
        parts = re.split(r"(?im)^(?=\[State )", piece)
        for j, part in enumerate(parts):
            if re.search(r"(?im)^\s*type\s*=\s*hitdef\s*$", part):
                new = tune_hitdef(part, state)
                if new != part:
                    report.append(f"{state}")
                parts[j] = new
        pieces[i] = "".join(parts)
    return "".join(pieces), report


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(exist_ok=True)
    for name in FILES:
        if not (BACKUP / name).exists():
            shutil.copy2(LIVE / name, BACKUP / name)
    for name in FILES:
        shutil.copy2(BACKUP / name, LIVE / name)

    # Portal sprites.
    frames = {}
    for i in range(PORTAL_FRAMES):
        image = portal_frame(i)
        image.save(ART / f"portal-{i}.png")
        frames[(PORTAL_GROUP, i)] = encode(image, (192, 256))
    sff = Sff(LIVE / "spr.sff")
    assert not any(h[0] == PORTAL_GROUP for h in sff.headers)
    (LIVE / "spr.sff").write_bytes(sff.derive({}, frames))

    air = (LIVE / "anim.air").read_text(encoding="latin1")
    assert "[Begin Action 879970]" not in air
    (LIVE / "anim.air").write_text(air.rstrip() + "\n" + NEW_ACTIONS, encoding="latin1")

    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    cns = replace_statedef(cns, 191, INTRO)
    cns, tuned = tune_physics(cns)
    (LIVE / "cns.cns").write_text(cns, encoding="latin1")

    shadows = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    shadows = replace_statedef(shadows, 870220, TOGGLE, keep_from="[State 870220, Reset domain]")
    summon_escort = """[State 870100, Shadow escort stays to fight]
type=Helper
trigger1=time=14 && !numhelper(870790)
helpertype=normal
name="Igris escort"
ID=870790
stateno=870790
postype=p1
pos=-30,0
ownpal=1
keyctrl=0
size.xscale=1
size.yscale=1
"""
    marker = "[State 870100, Recover]"
    assert shadows.count(marker) == 1
    shadows = shadows.replace(marker, summon_escort + "\n" + marker)
    shadows = shadows.rstrip() + "\n" + escort_states() + CHASE
    (LIVE / "our-shadows.cns").write_text(shadows, encoding="latin1")

    neg2 = (LIVE / "-2.cns").read_text(encoding="latin1")
    marker = "[State -2, No double Jinwoo afterimage]"
    assert neg2.count(marker) == 1
    neg2 = neg2.replace(marker, GUARD + marker)
    (LIVE / "-2.cns").write_text(neg2, encoding="latin1")

    report = {
        "revision": "jus-playstyle-v71",
        "reference": "https://www.youtube.com/watch?v=0gBpCa72pSc (studied, nothing copied)",
        "portal_group": PORTAL_GROUP,
        "new_actions": [879970, 879971, 879972, 879975, 879976],
        "new_states": [879960, 870790, 870791, 870792, 870793],
        "physics_hitdefs_tuned": tuned,
        "hashes": {n: hashlib.sha256((LIVE / n).read_bytes()).hexdigest() for n in FILES},
    }
    (ART / "installation.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "hashes"}, indent=2))


if __name__ == "__main__":
    main()
