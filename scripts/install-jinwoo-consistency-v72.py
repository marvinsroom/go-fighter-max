"""Jinwoo consistency pass (v72), applied on top of jus-playstyle-v71.

* Removes the old round-1 "academy" splash helper (30120) that covered the
  first ~40 ticks of the intro with a tall light column.
* Intro sword: he opens the portal empty-handed, the longsword spins out of
  it and he catches it in his front hand (no more sword trailing in the
  back hand during the portal pose).
* Size / art consistency: the engine sweep found 155 move runs still showing
  the original small pixel-art bare-hand bodies.  Causes and fixes:
    - supers zero var(10); the sword remap now also covers var(10)=0;
    - legacy actions whose unified sword twin matches frame-for-frame are
      rewritten in place, so not even the first tick shows old art;
    - dagger mode had unified art for only ~40 actions; every sword action
      without a dagger twin gets one (same pose index, dagger bank scale).
* Summons: the leaping intercept (87072x) no longer hops off the floor;
  it is a grounded lunge with an afterimage.

Every run restores from live-before-v72 first.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/consistency-v72"
BACKUP = ART / "live-before-v72"
FILES = ["anim.air", "base.cns", "-2.cns", "our-shadows.cns", "cns.cns", "Mode.cns", "config.cns", "spr.sff"]

SWORD_GROUP, DAGGER_GROUP = 61017, 61016
SWORD_SCALE = "0.208072691,0.196294992"
DAGGER_SCALE = "0.167301691,0.157831784"
LEGACY_BODY = {0, 20, 180, 200, 300, 400, 600}
INTRO_GROUP = 61091
SPIN_FRAMES = 16


# --------------------------------------------------------------------------
# Intro sprites: empty-handed portal pose + spinning longsword
# --------------------------------------------------------------------------
def blade_coords(shape):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    c = np.array([84.42, 112.47])          # PCA of the blade's cyan pixels
    d = np.array([0.95725, 0.28925])
    n = np.array([-d[1], d[0]])
    t = (xx - c[0]) * d[0] + (yy - c[1]) * d[1]
    p = (xx - c[0]) * n[0] + (yy - c[1]) * n[1]
    return t, p, c, d


def intro_sprites(sff: Sff) -> dict:
    index = sff.keys[(SWORD_GROUP, 8)]
    axis = sff.headers[index][4:6]
    pose = np.array(sff.decode(index))
    t, p, c, d = blade_coords(pose.shape[:2])
    body = pose.copy()
    body[(t > -90) & (t < 100) & (np.abs(p) < 26), 3] = 0

    r, g, b = (pose[..., k].astype(int) for k in range(3))
    skin = (r > 150) & (g > 100) & (r > b + 30)
    blade = pose.copy()
    blade[~((t > -90) & (t < 84) & (np.abs(p) < 24)) | skin, 3] = 0
    # Re-create the grip and pommel hidden in his hand.
    img = Image.fromarray(blade).copy()
    px = img.load()
    for s in np.arange(84, 112, 0.5):
        for q in np.arange(-4.5, 4.5, 0.5):
            x = c[0] + d[0] * s - d[1] * q
            y = c[1] + d[1] * s + d[0] * q
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < img.width and 0 <= yi < img.height:
                shade = 28 + int(10 * abs(q))
                px[xi, yi] = (shade, shade, shade + 14, 255)
    for s in np.arange(108, 116, 0.5):
        for q in np.arange(-6.5, 6.5, 0.5):
            x = c[0] + d[0] * s - d[1] * q
            y = c[1] + d[1] * s + d[0] * q
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < img.width and 0 <= yi < img.height and q * q + (s - 112) ** 2 < 40:
                px[xi, yi] = (60, 140, 200, 255)
    # Centre the weapon on its midpoint and rotate.
    mid = c + d * 13
    size = 300
    canvas = Image.new("RGBA", (size, size))
    canvas.paste(img, (int(size / 2 - mid[0]), int(size / 2 - mid[1])), img)
    angle0 = np.degrees(np.arctan2(d[1], d[0]))
    frames = {(INTRO_GROUP, 0): (Image.fromarray(body), axis)}
    for k in range(SPIN_FRAMES):
        rotated = canvas.rotate(angle0 - k * 360 / SPIN_FRAMES, resample=Image.BICUBIC)
        frames[(INTRO_GROUP, 10 + k)] = (rotated, (size // 2, size // 2))
    for key, (image, _) in frames.items():
        image.save(ART / f"intro-{key[0]}-{key[1]}.png")
    return frames


def encode(image: Image.Image, axis) -> dict:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": tuple(int(v) for v in axis),
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


# --------------------------------------------------------------------------
# AIR helpers
# --------------------------------------------------------------------------
ACTION_RE = re.compile(r"(?ims)^\[Begin Action\s+(-?\d+)\][^\n]*\n(.*?)(?=^\[Begin Action|\Z)")


def parse(air: str) -> dict[int, tuple[int, int, str]]:
    return {int(m.group(1)): (m.start(), m.end(), m.group(2)) for m in ACTION_RE.finditer(air)}


def frame_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        fields = [f.strip() for f in line.split(";", 1)[0].split(",")]
        if len(fields) >= 5 and re.fullmatch(r"-?\d+", fields[0] or "x") and re.fullmatch(r"-?\d+", fields[1] or "x"):
            rows.append(fields)
    return rows


def to_dagger(body: str) -> str:
    out = []
    for line in body.splitlines():
        fields = line.split(",")
        if len(fields) >= 2 and fields[0].strip() == str(SWORD_GROUP):
            fields[0] = str(DAGGER_GROUP)
            while len(fields) < 9:
                fields.append("")
            fields[7], fields[8] = DAGGER_SCALE.split(",")
            line = ",".join(fields)
        out.append(line)
    return "\n".join(out)


INTRO_ACTIONS = f"""[Begin Action 879970]
Clsn2Default: 1
Clsn2[0] = -12,-59,12,0
{INTRO_GROUP},0,0,0,36,,,{SWORD_SCALE}
{SWORD_GROUP},9,0,0,26,,,{SWORD_SCALE}
{SWORD_GROUP},6,0,0,22,,,{SWORD_SCALE}
{SWORD_GROUP},11,0,0,8,,,{SWORD_SCALE}
{SWORD_GROUP},0,0,0,-1,,,{SWORD_SCALE}

"""
SPIN_ACTION = "; Longsword spinning out of the inventory portal\n[Begin Action 879973]\n" + "\n".join(
    f"{INTRO_GROUP},{10 + k},0,0,1,,,{SWORD_SCALE}" for k in range(SPIN_FRAMES)) + "\n"

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
[State 191, Inventory portal]
type=Explod
trigger1=time=4
anim=879971
ID=879971
pos=36,-34
postype=p1
bindtime=-1
removetime=36
scale=0.78,0.78
sprpriority=3
ownpal=1
[State 191, Sword spins in the portal]
type=Explod
trigger1=time=8
anim=879973
ID=879973
pos=36,-34
postype=p1
bindtime=-1
removetime=22
sprpriority=4
ownpal=1
[State 191, Sword flies to his hand]
type=Explod
trigger1=time=30
anim=879973
ID=879974
pos=36,-34
postype=p1
vel=-5.6,0
removetime=6
sprpriority=4
ownpal=1
[State 191, Portal sound]
type=PlaySnd
trigger1=time=4
value=S5,52
volumescale=80
[State 191, Catch]
type=PlaySnd
trigger1=time=36
value=S5,54
[State 191, Catch flash]
type=PalFX
trigger1=time=36 || time=84
time=4
add=70,80,110
mul=256,256,256
[State 191, Ready line]
type=PlaySnd
trigger1=time=96
value=S0,61
channel=0
[State 191, Clean up an intro skip]
type=RemoveExplod
trigger1=roundstate=2
[State 191, Finish arrival]
type=ChangeState
trigger1=time>=130 || roundstate=2
value=0
ctrl=1
"""


def replace_statedef(text: str, number: int, body: str) -> str:
    m = re.search(r"(?ims)^\[Statedef\s+%d\].*?(?=^\[Statedef|\Z)" % number, text)
    assert m, number
    return text[:m.start()] + body + "\n" + text[m.end():]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(exist_ok=True)
    for name in FILES:
        if not (BACKUP / name).exists():
            shutil.copy2(LIVE / name, BACKUP / name)
    for name in FILES:
        shutil.copy2(BACKUP / name, LIVE / name)
    report: dict[str, object] = {"revision": "consistency-v72"}

    # Sprites.
    sff = Sff(LIVE / "spr.sff")
    assert not any(h[0] == INTRO_GROUP for h in sff.headers)
    frames = {k: encode(img, axis) for k, (img, axis) in intro_sprites(sff).items()}
    (LIVE / "spr.sff").write_bytes(sff.derive({}, frames))

    # Animations.
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    actions = parse(air)
    replacements: dict[int, str] = {}
    rewritten, skipped = [], []
    for number, (_, _, body) in actions.items():
        if not 0 <= number < 500000:
            continue
        rows = frame_rows(body)
        if not any(int(r[0]) in LEGACY_BODY for r in rows):
            continue
        twin = actions.get(500000 + number % 10000)
        if twin is None:
            skipped.append(number); continue
        trows = frame_rows(twin[2])
        if [r[4] for r in rows] == [r[4] for r in trows]:
            replacements[number] = twin[2]
            rewritten.append(number)
            continue
        # Timing differs: keep this action's rows and only swap each legacy
        # sprite for the twin's sprite at the same (or nearest) index.
        lines, k = [], 0
        for line in body.splitlines():
            fields = [f.strip() for f in line.split(";", 1)[0].split(",")]
            if len(fields) >= 5 and re.fullmatch(r"-?\d+", fields[0] or "x") and re.fullmatch(r"-?\d+", fields[1] or "x"):
                if int(fields[0]) in LEGACY_BODY:
                    src = trows[min(k, len(trows) - 1)]
                    fields += [""] * (9 - len(fields))
                    fields[0], fields[1] = src[0], src[1]
                    fields[7], fields[8] = (src + ["", "", "", ""])[7:9]
                    line = ",".join(fields)
                k += 1
            lines.append(line)
        replacements[number] = "\n".join(lines) + "\n"
        skipped.append(number)
    pieces, cursor = [], 0
    for number, (start, end, body) in sorted(actions.items(), key=lambda kv: kv[1][0]):
        if number in replacements:
            header = air[start:air.index("\n", start) + 1]
            pieces += [air[cursor:start], header, replacements[number].rstrip("\n") + "\n\n"]
            cursor = end
    pieces.append(air[cursor:])
    air = "".join(pieces)

    actions = parse(air)
    mirrored = []
    extra = ["\n; JINWOO CONSISTENCY V72 - dagger twins of unified sword actions\n"]
    for number, (_, _, body) in sorted(actions.items()):
        if 500000 <= number < 510000 and (700000 + number - 500000) not in actions:
            if not any(int(r[0]) == SWORD_GROUP for r in frame_rows(body)):
                continue
            extra.append(f"[Begin Action {700000 + number - 500000}]\n{to_dagger(body).rstrip()}\n\n")
            mirrored.append(700000 + number - 500000)
    # Intro.
    start, end, _ = actions[879970]
    air = air[:start] + INTRO_ACTIONS + air[end:]
    air = air.rstrip() + "\n" + "".join(extra) + SPIN_ACTION
    (LIVE / "anim.air").write_text(air, encoding="latin1")
    report.update(rewritten_in_place=rewritten, sprite_swapped=skipped, dagger_twins=len(mirrored))

    # Round-1 splash helper.
    base = (LIVE / "base.cns").read_text(encoding="latin1")
    blocks = re.split(r"(?im)^(?=\[state )", base)
    hits = 0
    for i, block in enumerate(blocks):
        if re.search(r"(?im)^\s*stateno\s*=\s*30120\s*$", block) and re.search(r"(?im)^\s*type\s*=\s*helper", block):
            blocks[i] = re.sub(r"(?im)^(\s*type\s*=\s*helper\s*\n)",
                               r"\1triggerall = 0 ; v72: old round-1 splash covered the intro\n", block, count=1)
            hits += 1
    assert hits == 2, hits
    (LIVE / "base.cns").write_text("".join(blocks), encoding="latin1")

    # Old supers zero var(10) ("bare hands").  var(48) remembers the equipped
    # weapon so those moves keep showing the longsword or the daggers.
    neg2 = (LIVE / "-2.cns").read_text(encoding="latin1")
    pattern = "triggerall=!ishelper && var(45)=0 && var(10)>=20000"
    count = neg2.count(pattern)
    assert count == 3, count
    neg2 = neg2.replace(pattern, "triggerall=!ishelper && var(45)=0 && (var(10)>=20000 || (var(10)=0 && var(48)!=10000))")
    pattern = "triggerall=!ishelper && var(45)=0 && var(10)=10000"
    assert neg2.count(pattern) == 1
    neg2 = neg2.replace(pattern, "triggerall=!ishelper && var(45)=0 && (var(10)=10000 || (var(10)=0 && var(48)=10000))")
    guard = "trigger1=movetype!=A\nvar(10)=20000\n"
    assert neg2.count(guard) == 1
    neg2 = neg2.replace(guard, "trigger1=movetype!=A\nvar(10)=cond(var(48)=10000,10000,20000)\n")
    memory = """[State -2, V72 remember the equipped weapon]
type=VarSet
triggerall=!ishelper && var(45)=0
trigger1=var(10)>0
var(48)=cond(var(10)>=20000,20000,10000)
ignorehitpause=1
"""
    marker = "[State -2, V71 longsword is the default weapon]"
    assert neg2.count(marker) == 1
    neg2 = neg2.replace(marker, memory + marker)
    (LIVE / "-2.cns").write_text(neg2, encoding="latin1")

    # Intro state.
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    (LIVE / "cns.cns").write_text(replace_statedef(cns, 191, INTRO), encoding="latin1")

    # The shared animation-choice template only knew "sword or legacy", so
    # dagger mode showed one tick of sword art before the -2 remap.  Give it
    # a dagger branch and make the sword branch honour the remembered weapon.
    template = re.compile(
        r"var\(10\)>=20000 && selfanimexist\(500000\+\((.+?)\)\),500000\+\(\1\),cond\(selfanimexist\(\1\),\(\1\)")

    def weapon_choice(m: re.Match) -> str:
        x = m.group(1)
        sword = "(var(10)>=20000 || (var(10)=0 && var(48)!=10000))"
        dagger = f"((var(10)>=10000 && var(10)<20000) || (var(10)=0 && var(48)=10000)) && selfanimexist(700000+(({x})%10000))"
        # Same nesting depth as the original: the weapon pick happens inside
        # the value of the existing branch.
        return (f"(({sword} && selfanimexist(500000+({x}))) || ({dagger})),"
                f"cond({dagger},700000+(({x})%10000),500000+({x})),cond(selfanimexist({x}),({x})")

    templated = {}
    for name in ("cns.cns", "Mode.cns", "config.cns", "base.cns", "our-shadows.cns"):
        text = (LIVE / name).read_text(encoding="latin1")
        text, count = template.subn(weapon_choice, text)
        templated[name] = count
        (LIVE / name).write_text(text, encoding="latin1")
    report["weapon_template_sites"] = templated

    # Grounded summon lunges.
    shadows = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    parts = re.split(r"(?im)^(?=\[Statedef )", shadows)
    lunges = []
    for i, part in enumerate(parts):
        m = re.match(r"\[Statedef\s+(8707[0-9]{2})\]", part)
        if not m:
            continue
        number = int(m.group(1))
        if number in (870720, 870721, 870722, 870723):
            part = re.sub(r"(?im)^y\s*=\s*-2\.4\s*$", "y=0", part)
            part = re.sub(r"(?im)^\[State (\d+), Intercept gravity\]\ntype=VelAdd\ntrigger1=time>12\ny=0\.45\n",
                          "", part)
            part = part.rstrip("\n") + f"""
[State {number}, Grounded lunge]
type=PosSet
trigger1=1
y=0
[State {number}, Lunge afterimage]
type=AfterImage
trigger1=!time
time=14
length=8
trans=add
palbright=0,0,40
"""
            lunges.append(number)
        if number == 870792:
            part = part.replace("x=3.0\ny=-2.2\n", "x=4.0\n")
        parts[i] = part
    assert len(lunges) == 4, lunges
    (LIVE / "our-shadows.cns").write_text("".join(parts), encoding="latin1")
    report["grounded_lunges"] = lunges

    report["hashes"] = {n: hashlib.sha256((LIVE / n).read_bytes()).hexdigest() for n in FILES}
    (ART / "installation.json").write_text(json.dumps(report, indent=1))
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 12 else f"{len(v)} items")
                      for k, v in report.items() if k != "hashes"}, indent=1))


if __name__ == "__main__":
    main()
