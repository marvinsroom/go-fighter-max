from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFile, ImageFont

from edward_assets import read_v1


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "sprite-fighter/style-wave2/ben-10"
INV = json.loads((STYLE / "inventory.json").read_text())
SFF_PATH = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/ben-10" / INV["files"]["sprite"]
OUT = STYLE / "conversion-v1/form-references.png"
ImageFile.LOAD_TRUNCATED_IMAGES = True


def alpha_bbox_area(image):
    box = image.getchannel("A").getbbox()
    return 0 if box is None else (box[2] - box[0]) * (box[3] - box[1])


sprites = read_v1(SFF_PATH)
font = ImageFont.load_default()
cell_w, cell_h = 300, 260
board = Image.new("RGBA", (cell_w * 5, cell_h * 4), (27, 29, 35, 255))
draw = ImageDraw.Draw(board)

chosen = {}
for group in range(20):
    options = []
    for sprite in sprites:
        key = sprite["key"]
        if key[0] != group:
            continue
        image = sprite["image"]
        area = alpha_bbox_area(image)
        if area:
            options.append((area, key[1], image))
    if not options:
        continue
    # Prefer a substantial representative while avoiding enormous effect-heavy outliers.
    options.sort(key=lambda row: row[0])
    area, number, image = options[min(len(options) - 1, int(len(options) * 0.65))]
    chosen[str(group)] = {"number": number, "size": list(image.size), "opaque_bbox_area": area}
    x = (group % 5) * cell_w
    y = (group // 5) * cell_h
    draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline=(82, 87, 99, 255), width=2)
    draw.text((x + 10, y + 9), f"FORM GROUP {group}  sprite {number}", font=font, fill=(255, 255, 255, 255))
    box = image.getchannel("A").getbbox()
    crop = image.crop(box)
    crop.thumbnail((cell_w - 24, cell_h - 48), Image.Resampling.NEAREST)
    px = x + (cell_w - crop.width) // 2
    py = y + 36 + (cell_h - 42 - crop.height) // 2
    board.alpha_composite(crop, (px, py))

OUT.parent.mkdir(parents=True, exist_ok=True)
board.convert("RGB").save(OUT, quality=94)
(OUT.with_suffix(".json")).write_text(json.dumps({"source": str(SFF_PATH), "chosen": chosen}, indent=2))
print(OUT)
