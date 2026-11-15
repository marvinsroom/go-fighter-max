"""Install the transparent System HUD into live Jinwoo's charge state."""
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
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "system-charge-v40-source.png"
ASSET = BASE / "system-charge-v40.png"
OUT = BASE / "system-charge-v40"
BACKUP = OUT / "live-before-v40"
REPORT = OUT / "installation.json"
SPRITE_KEY = (61900, 0)
AIR_MARKER = "; JINWOO_SYSTEM_CHARGE_V40"
CNS_MARKER = "; BEGIN JINWOO SYSTEM CHARGE V40"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_asset() -> Image.Image:
    image = Image.open(SOURCE).convert("RGBA")
    box = image.getchannel("A").getbbox()
    if not box:
        raise RuntimeError("generated System artwork has no visible alpha")
    image = image.crop(box)
    width = 768
    height = max(1, round(image.height * width / image.width))
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    image.save(ASSET, optimize=True)
    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    air_path, cns_path, sff_path = LIVE / "anim.air", LIVE / "cns.cns", LIVE / "spr.sff"
    air = air_path.read_text(encoding="latin1")
    if AIR_MARKER in air:
        print(REPORT.read_text(encoding="utf-8")); return

    image = prepare_asset()
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (air_path, cns_path, sff_path):
        shutil.copy2(path, BACKUP / path.name)

    sff = Sff(sff_path)
    if SPRITE_KEY in sff.keys:
        raise RuntimeError(f"sprite key {SPRITE_KEY} is already occupied")
    png = io.BytesIO(); image.save(png, format="PNG", optimize=True)
    frame = {
        "image": image,
        "png": png.getvalue(),
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
        "axis": (image.width // 2, image.height // 2),
    }
    sff_path.write_bytes(sff.derive({}, {SPRITE_KEY: frame}))

    action = f"""
{AIR_MARKER}
[Begin Action 61900]
LoopStart
61900,0,0,0,5,,AS160D96,1,1
Interpolate Blend
61900,0,0,0,5,,AS256D0,1.015,1.015
Interpolate Blend
61900,0,0,0,5,,AS210D46,1,1
Interpolate Blend
61900,0,0,0,5,,AS256D0,0.985,0.985
"""
    air = air.rstrip() + "\n" + action
    air_path.write_text(air, encoding="latin1", newline="")

    cns = cns_path.read_text(encoding="latin1")
    state500 = cns.index("[statedef 500]")
    state501 = cns.index("[statedef 501]", state500)
    block = cns[state500:state501]
    needle = "[State 0]\ntype = PosAdd"
    if needle not in block:
        needle = "[State 0]\r\ntype = PosAdd"
    overlay = f"""{CNS_MARKER}
[State 500, System charge interface]
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
    if needle not in block:
        raise RuntimeError("could not find charge-state insertion point")
    block = block.replace(needle, overlay + needle, 1)
    cns = cns[:state500] + block + cns[state501:]

    cleanup = """[State 501, Remove System charge interface]
type = RemoveExplod
trigger1 = 1
id = 61900
ignorehitpause = 1

"""
    state501 = cns.index("[statedef 501]")
    insertion = cns.index("\n", state501) + 1
    cns = cns[:insertion] + cleanup + cns[insertion:]
    cns_path.write_text(cns, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "runtime": "chars/jinwoo/jinwoo.def",
        "state": 500,
        "sprite_key": list(SPRITE_KEY),
        "action": 61900,
        "asset": str(ASSET.relative_to(ROOT)),
        "asset_size": list(image.size),
        "asset_alpha_bbox": list(image.getchannel("A").getbbox() or ()),
        "runtime_sha256": {name: sha(LIVE / name) for name in ("anim.air", "cns.cns", "spr.sff")},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
