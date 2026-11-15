from pathlib import Path
from PIL import Image, ImageDraw, ImageFile, ImageFont
import json, math, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edward_assets import read_v1

ImageFile.LOAD_TRUNCATED_IMAGES = True
root = Path(__file__).resolve().parents[1]
style = root / "sprite-fighter/style-wave2/ben-10"
inv = json.loads((style / "inventory.json").read_text())
source = root / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/ben-10" / inv["files"]["sprite"]
out = style / "conversion-v1/group-pages"
out.mkdir(parents=True, exist_ok=True)
sprites = read_v1(source)
groups = {}
for sprite in sprites:
    if sprite["key"][0] >= 9000:
        continue
    box = sprite["image"].getchannel("A").getbbox()
    if box:
        groups.setdefault(sprite["key"][0], []).append(sprite)

font = ImageFont.load_default()
for page in range(math.ceil(len(groups) / 30)):
    entries = sorted(groups.items())[page * 30:(page + 1) * 30]
    board = Image.new("RGB", (1500, 900), (26, 29, 35))
    draw = ImageDraw.Draw(board)
    for i, (group, choices) in enumerate(entries):
        choices.sort(key=lambda s: (s["image"].getchannel("A").getbbox()[2]-s["image"].getchannel("A").getbbox()[0])*(s["image"].getchannel("A").getbbox()[3]-s["image"].getchannel("A").getbbox()[1]))
        sprite = choices[min(len(choices)-1, int(len(choices)*.55))]
        image = sprite["image"].crop(sprite["image"].getchannel("A").getbbox())
        image.thumbnail((220, 120), Image.Resampling.NEAREST)
        x=(i%6)*250; y=(i//6)*180
        draw.rectangle((x,y,x+249,y+179),outline=(75,80,90),width=2)
        draw.text((x+8,y+7),f"G{group} N{sprite['key'][1]} ({len(choices)})",font=font,fill="white")
        board.paste(image,(x+(250-image.width)//2,y+35+(130-image.height)//2),image)
    board.save(out/f"groups-{page+1:02d}.jpg", quality=92)
print(len(groups), "groups", math.ceil(len(groups)/30), "pages")
