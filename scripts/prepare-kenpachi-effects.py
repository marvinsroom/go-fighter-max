"""Export Kenpachi's five effect groups as labeled visual references."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from edward_assets import read_v1

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "sprite-fighter/style-wave2/kenpachi/conversion-v1"
SOURCE = ART / "before/kenpachi_sff.sff"
sprites = [s for s in read_v1(SOURCE) if 6000 <= s["key"][0] < 9000]
out = ART / "effect-references"
out.mkdir(parents=True, exist_ok=True)

manifest = []
for group in sorted({s["key"][0] for s in sprites}):
    rows = [s for s in sprites if s["key"][0] == group]
    cols = 4
    cell_w, cell_h = 320, 230
    sheet = Image.new("RGB", (cols * cell_w, ((len(rows) + cols - 1) // cols) * cell_h), (27, 34, 48))
    draw = ImageDraw.Draw(sheet)
    for index, sprite in enumerate(rows):
        image = sprite["image"].convert("RGBA")
        image.thumbnail((cell_w - 24, cell_h - 42), Image.Resampling.LANCZOS)
        x = (index % cols) * cell_w + (cell_w - image.width) // 2
        y = (index // cols) * cell_h + (cell_h - 28 - image.height) // 2
        sheet.paste(image, (x, y), image)
        draw.text(((index % cols) * cell_w + 8, (index // cols + 1) * cell_h - 24), f"{sprite['key'][0]},{sprite['key'][1]}", fill="white")
        manifest.append({"key": list(sprite["key"]), "size": list(sprite["image"].size), "axis": list(sprite["axis"]), "group_cell": index})
    sheet.save(out / f"group-{group}.png")
(out / "manifest.json").write_text(json.dumps(manifest, indent=2))
print("EFFECT_REFERENCES", len(sprites), "sprites", len({s['key'][0] for s in sprites}), "groups")
