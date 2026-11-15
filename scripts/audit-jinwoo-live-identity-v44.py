"""Render representative live body keys across charge, attacks, weapons and forms."""
from pathlib import Path
import json
import re
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/live-identity-audit-v44"
AIR = (LIVE / "anim.air").read_text(encoding="latin1")
SFF = Sff(LIVE / "spr.sff")
ACTION_IDS = [0, 20, 40, 100, 200, 210, 220, 300, 400, 500, 501, 600, 610, 620, 10000, 10200, 10400, 20000, 20200, 20400, 500000, 500020, 500200, 700200, 61902, 5000000, 5000200, 5000500, 5001000, 6000000, 6000200, 6000500, 6001000]


def action(number: int) -> str:
    match = re.search(rf"(?ims)^\[Begin Action\s+{number}\]\s*$\n(.*?)(?=^\[Begin Action|\Z)", AIR)
    return match.group(1) if match else ""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for number in ACTION_IDS:
        keys = []
        for match in re.finditer(r"(?m)^\s*(-?\d+)\s*,\s*(-?\d+)\s*,", action(number)):
            key = tuple(map(int, match.groups()))
            if key[0] >= 0 and key in SFF.keys and key not in keys:
                keys.append(key)
        for key in keys[:6]:
            image = SFF.decode(SFF.keys[key]).convert("RGBA")
            box = image.getchannel("A").getbbox()
            if not box:
                continue
            image = image.crop(box)
            image.thumbnail((190, 220), Image.Resampling.LANCZOS)
            cell = Image.new("RGBA", (220, 270), (15, 17, 26, 255))
            cell.alpha_composite(image, ((220-image.width)//2, 225-image.height))
            draw = ImageDraw.Draw(cell)
            draw.text((8, 235), f"action {number}", fill=(210,220,255,255))
            draw.text((8, 250), f"sprite {key[0]},{key[1]}", fill=(160,180,220,255))
            rows.append((number, key, cell))
    cols = 6
    sheet = Image.new("RGBA", (cols*220, ((len(rows)+cols-1)//cols)*270), (7,8,14,255))
    for i, (_, _, cell) in enumerate(rows):
        sheet.alpha_composite(cell, ((i%cols)*220, (i//cols)*270))
    sheet.convert("RGB").save(OUT / "representative-actions.jpg", quality=92)
    (OUT / "inventory.json").write_text(json.dumps([{"action": n, "key": list(k)} for n,k,_ in rows], indent=2)+"\n")
    print(OUT / "representative-actions.jpg")


if __name__ == "__main__":
    main()
