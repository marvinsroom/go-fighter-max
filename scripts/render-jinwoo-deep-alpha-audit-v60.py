"""Render suspicious active Jinwoo sprites for visual alpha-component review."""
from pathlib import Path
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/alpha-cleanup-v59/deep-audit-v60.png"
KEYS = [(61011, n) for n in (6, 8, 9, 10, 29, 30, 31, 73, 79, 124, 125, 126, 127)] + [(61018, 0), (61019, 0), (61019, 3)]

sff = Sff(LIVE / "spr.sff")
sheet = Image.new("RGBA", (1000, ((len(KEYS) + 3) // 4) * 300), (12, 15, 24, 255))
draw = ImageDraw.Draw(sheet)
for slot, key in enumerate(KEYS):
    image = sff.decode(sff.keys[key]).convert("RGBA")
    image.thumbnail((230, 250), Image.Resampling.LANCZOS)
    x = (slot % 4) * 250 + (250 - image.width) // 2
    y = (slot // 4) * 300 + 28 + (250 - image.height) // 2
    sheet.alpha_composite(image, (x, y))
    draw.text(((slot % 4) * 250 + 8, (slot // 4) * 300 + 6), f"{key[0]},{key[1]}", fill="white")
OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT, optimize=True)
print(OUT)
