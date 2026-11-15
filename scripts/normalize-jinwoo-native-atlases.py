"""Inset each generated atlas cell so no artwork touches a frame boundary."""
from pathlib import Path
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen-reskin/art/native-comic-v4"
requests = json.loads((ART / "requests.json").read_text(encoding="utf-8"))

for request in requests:
    path = ART / f"{request['kind']}.png"
    image = Image.open(path).convert("RGBA")
    output = Image.new("RGBA", image.size)
    columns, rows = request["columns"], request["rows"]
    for index in range(request["count"]):
        column, row = index % columns, index // columns
        left = round(column * image.width / columns)
        right = round((column + 1) * image.width / columns)
        top = round(row * image.height / rows)
        bottom = round((row + 1) * image.height / rows)
        tile = image.crop((left, top, right, bottom))
        bounds = tile.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
        if bounds is None:
            raise AssertionError(f"Empty cell {request['kind']} {index}")
        content = tile.crop(bounds)
        fitted = ImageOps.contain(content, (right-left-32, bottom-top-32), Image.Resampling.LANCZOS)
        x = left + (right-left-fitted.width)//2
        y = top + (bottom-top-fitted.height)//2
        output.alpha_composite(fitted, (x, y))
    output.save(path)
    print("NORMALIZED", request["kind"])
