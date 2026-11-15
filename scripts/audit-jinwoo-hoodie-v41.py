"""Render candidate Jinwoo appearance banks for the full-charge hoodie audit."""
from pathlib import Path
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

SFF_PATH = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo/spr.sff"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/system-charge-v41"
KEYS = [(6000, 0), (6001, 0), (6002, 0)] + [(61011, n) for n in (72, 82, 83, 108, 109, 110, 111, 124, 125, 126, 127, 128, 129, 130, 131)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sff = Sff(SFF_PATH)
    cells = []
    for key in KEYS:
        if key not in sff.keys:
            continue
        image = sff.decode(sff.keys[key]).convert("RGBA")
        box = image.getchannel("A").getbbox()
        if box:
            image = image.crop(box)
        image.thumbnail((230, 260), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (260, 310), (18, 20, 30, 255))
        cell.alpha_composite(image, ((260 - image.width) // 2, 20 + 260 - image.height))
        draw = ImageDraw.Draw(cell)
        draw.text((10, 285), f"{key[0]},{key[1]}", fill=(220, 225, 255, 255))
        cells.append(cell)
    cols = 4
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 260, rows * 310), (8, 10, 18, 255))
    for i, cell in enumerate(cells):
        sheet.alpha_composite(cell, ((i % cols) * 260, (i // cols) * 310))
    path = OUT / "hoodie-bank-audit.png"
    sheet.convert("RGB").save(path, quality=92)
    print(path)


if __name__ == "__main__":
    main()
