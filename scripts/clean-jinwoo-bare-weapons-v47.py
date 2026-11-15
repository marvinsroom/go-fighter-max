"""Remove weapon-colored pixels from the eight bare-hand normal frames."""
from __future__ import annotations

import colorsys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/bare-hands-v47/source"
OUT = SOURCE.parent / "cleaned"

# Tight regions containing daggers and detached energy. The color test inside
# each region preserves skin, black clothing, and the coat lining.
REGIONS = {
    0: [(35, 125, 110, 215), (150, 120, 245, 210)],
    1: [(15, 135, 105, 225), (140, 80, 256, 175)],
    2: [(25, 140, 115, 225), (140, 75, 256, 180)],
    3: [(25, 135, 115, 230), (135, 85, 256, 190)],
    4: [(35, 55, 165, 180), (150, 80, 256, 195)],
    5: [(15, 75, 256, 225)],
    6: [(10, 65, 256, 205)],
    7: [(45, 90, 165, 200), (140, 115, 250, 235)],
}


def weapon_pixel(r: int, g: int, b: int, a: int) -> bool:
    if a == 0:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    # Violet/magenta/cyan energy and blade colors. Dark purple coat lining is
    # protected by the value/chroma floors.
    violet = .62 <= h <= .94 and s >= .42 and v >= .24
    magenta = (h >= .94 or h <= .04) and s >= .55 and b >= 70
    cyan = .48 <= h < .62 and s >= .55 and v >= .34
    return violet or magenta or cyan


def clean(number: int) -> Image.Image:
    image = Image.open(SOURCE / f"bare-source-{number}.png").convert("RGBA")
    pixels = image.load()
    mask = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask)
    for region in REGIONS[number]:
        draw.rectangle(region, fill=255)
    allowed = mask.load()
    remove = Image.new("L", image.size)
    removed = remove.load()
    for y in range(image.height):
        for x in range(image.width):
            if allowed[x, y] and weapon_pixel(*pixels[x, y]):
                removed[x, y] = 255
    # Grow from the colored cores through their white/dark antialiased edges.
    # Restrict the result back to the hand-authored weapon regions so coat and
    # face pixels elsewhere remain byte-identical.
    remove = remove.filter(ImageFilter.MaxFilter(9))
    grown = Image.new("L", image.size)
    grown_pixels, remove_pixels = grown.load(), remove.load()
    for y in range(image.height):
        for x in range(image.width):
            if allowed[x, y] and remove_pixels[x, y]:
                grown_pixels[x, y] = 255
    remove = grown
    alpha = image.getchannel("A")
    alpha.paste(0, mask=remove)
    image.putalpha(alpha)
    return image


def contact_sheet(images: list[Image.Image]) -> Image.Image:
    canvas = Image.new("RGBA", (4 * 256, 2 * 256), (24, 26, 38, 255))
    for index, image in enumerate(images):
        x, y = index % 4 * 256, index // 4 * 256
        canvas.alpha_composite(image, (x, y))
    return canvas.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    images = []
    for number in range(8):
        image = clean(number)
        image.save(OUT / f"bare-clean-{number}.png")
        images.append(image)
    contact_sheet(images).save(OUT / "bare-clean-contact-sheet.png")
    print(OUT)


if __name__ == "__main__":
    main()
