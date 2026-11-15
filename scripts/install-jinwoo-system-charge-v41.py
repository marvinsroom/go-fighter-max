"""Install the body-centered System enclosure and full-meter hoodie reveal."""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/system-charge-v41"
BACKUP = OUT / "live-before-v41"
FIELD_SOURCE = OUT / "system-enclosure-v41-source.png"
HOOD_SOURCE = OUT / "hoodie-full-charge-v41-source.png"
FIELD_ASSET = OUT / "system-enclosure-v41.png"
HOOD_ASSET = OUT / "hoodie-full-charge-v41.png"
MARKER = "; JINWOO_SYSTEM_CHARGE_V41"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(source: Path, target: Path, height: int) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    box = image.getchannel("A").getbbox()
    if not box:
        raise RuntimeError(f"{source.name} has no alpha")
    image = image.crop(box)
    width = max(1, round(image.width * height / image.height))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(target, optimize=True)
    return image


def frame(image: Image.Image, bottom_axis: bool) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {
        "image": image,
        "png": payload.getvalue(),
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
        "axis": (image.width // 2, image.height - 1 if bottom_axis else image.height // 2),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air_path, cns_path, sff_path = LIVE / "anim.air", LIVE / "cns.cns", LIVE / "spr.sff"
    air = air_path.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8")); return

    field = normalized(FIELD_SOURCE, FIELD_ASSET, 640)
    hoodie = normalized(HOOD_SOURCE, HOOD_ASSET, 256)
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (air_path, cns_path, sff_path):
        shutil.copy2(path, BACKUP / path.name)

    sff = Sff(sff_path)
    additions = {(61900, 1): frame(field, True), (61901, 0): frame(hoodie, True)}
    occupied = [key for key in additions if key in sff.keys]
    if occupied:
        raise RuntimeError(f"occupied v41 sprite keys: {occupied}")
    sff_path.write_bytes(sff.derive({}, additions))

    air += f"""
{MARKER}
[Begin Action 61901]
LoopStart
61900,1,0,0,4,,AS150D106,.125,.125
Interpolate Blend
61900,1,0,0,4,,AS230D26,.13,.125
Interpolate Blend
61900,1,0,0,4,,AS180D76,.125,.13
Interpolate Blend
61900,1,0,0,4,,AS256D0,.13,.13

[Begin Action 61902]
Clsn2: 1
  Clsn2[0] = -13,-63,13,0
61901,0,0,0,6,,,0.170535156,0.170535156
61901,0,0,0,6,,AS220D36,0.170535156,0.170535156
61901,0,0,0,6,,,0.170535156,0.170535156
61901,0,0,0,6,,AS240D16,0.170535156,0.170535156

[Begin Action 61903]
Clsn2: 1
  Clsn2[0] = -13,-63,13,0
LoopStart
61901,0,0,0,12,,,0.170535156,0.170535156
61901,0,0,0,12,,AS235D21,0.170535156,0.170535156
"""
    air_path.write_text(air, encoding="latin1", newline="")

    cns = cns_path.read_text(encoding="latin1")
    old = """[State 500, System charge interface]
type = Explod
triggerall = !numexplod(61900)
trigger1 = time = 5
anim = 61900
id = 61900
pos = 0,-82
postype = p1
bindtime = -1
removetime = -2
scale = .16,.16
sprpriority = 7
ownpal = 1
removeongethit = 1
ignorehitpause = 1
supermovetime = 999
pausemovetime = 999
; END JINWOO SYSTEM CHARGE V40
"""
    new = """[State 500, System enclosure around Jinwoo]
type = Explod
triggerall = !numexplod(61901)
trigger1 = time = 2
anim = 61901
id = 61901
pos = 0,1
postype = p1
bindtime = -1
removetime = -2
scale = 1,1
sprpriority = -1
ownpal = 1
removeongethit = 1
ignorehitpause = 1
supermovetime = 999
pausemovetime = 999

[State 500, System status header]
type = Explod
triggerall = !numexplod(61900)
trigger1 = time = 5
anim = 61900
id = 61900
pos = 0,-78
postype = p1
bindtime = -1
removetime = -2
scale = .11,.11
sprpriority = 7
ownpal = 1
removeongethit = 1
ignorehitpause = 1
supermovetime = 999
pausemovetime = 999

[State 500, Full meter enables hoodie form]
type = VarSet
trigger1 = power >= powermax
v = 30
value = 1
ignorehitpause = 1
; END JINWOO SYSTEM CHARGE V41
"""
    if old not in cns:
        raise RuntimeError("v40 charge block not found")
    cns = cns.replace(old, new, 1)
    cns = cns.replace("[State 501, Remove System charge interface]\ntype = RemoveExplod\ntrigger1 = 1\nid = 61900\nignorehitpause = 1\n", "[State 501, Remove System charge interface]\ntype = RemoveExplod\ntrigger1 = 1\nid = 61900\nignorehitpause = 1\n\n[State 501, Remove System enclosure]\ntype = RemoveExplod\ntrigger1 = 1\nid = 61901\nignorehitpause = 1\n", 1)
    state501 = cns.index("[statedef 501]")
    next_state = cns.index("[statedef 510]", state501)
    section = cns[state501:next_state]
    anim_line = next(line for line in section.splitlines() if line.startswith("anim="))
    section = section.replace(anim_line, f"anim=ifelse(var(30)=1,61902,{anim_line[5:]})", 1)
    cns = cns[:state501] + section + cns[next_state:]
    cns_path.write_text(cns, encoding="latin1", newline="")

    minus2 = LIVE / "-2.cns"
    minus2_text = minus2.read_text(encoding="latin1")
    backup_minus2 = BACKUP / minus2.name
    shutil.copy2(minus2, backup_minus2)
    hoodie_idle = """
; JINWOO FULL-METER HOODIE V41
[State -2, Full meter hoodie idle]
type = ChangeAnim
triggerall = !ishelper && var(45) = 0 && var(30) = 1
trigger1 = stateno = 0 && anim != 61903
value = 61903
ignorehitpause = 1

[State -2, Clear hoodie flag after meter is spent]
type = VarSet
triggerall = !ishelper && var(30) = 1
trigger1 = power < powermax
v = 30
value = 0
ignorehitpause = 1
"""
    minus2.write_text(minus2_text.rstrip() + "\n" + hoodie_idle, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "revision": "system-charge-v41",
        "behavior": ["System enclosure surrounds Jinwoo during charge", "full meter enters hoodie reveal", "hoodie idle remains while meter is full", "weapon variable var(10) is unchanged"],
        "sprite_keys": [[61900, 1], [61901, 0]],
        "actions": [61901, 61902, 61903],
        "assets": {"enclosure": str(FIELD_ASSET.relative_to(ROOT)), "hoodie": str(HOOD_ASSET.relative_to(ROOT))},
        "runtime_sha256": {name: sha(LIVE / name) for name in ("anim.air", "cns.cns", "-2.cns", "spr.sff")},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
