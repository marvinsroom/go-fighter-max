"""Pad v32 attack candidates onto the standard 1536-square review canvas."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "attack-candidates"
OUTPUT = BASE / "attack-normalized"
CANVAS = (1536, 1536)
MARGIN = 16


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(SOURCE.glob("*.png")):
        image = Image.open(path).convert("RGBA")
        bbox = image.getchannel("A").point(lambda value: 255 if value >= 8 else 0).getbbox()
        if not bbox:
            raise RuntimeError(f"empty attack candidate: {path.name}")
        visible = image.crop(bbox)
        scale = min(1.0, (CANVAS[0] - 2 * MARGIN) / visible.width, (CANVAS[1] - 2 * MARGIN) / visible.height)
        if scale < 1.0:
            visible = visible.resize(
                (round(visible.width * scale), round(visible.height * scale)),
                Image.Resampling.LANCZOS,
            )
        canvas = Image.new("RGBA", CANVAS)
        x = (CANVAS[0] - visible.width) // 2
        y = (CANVAS[1] - visible.height) // 2
        canvas.alpha_composite(visible, (x, y))
        destination = OUTPUT / path.name
        canvas.save(destination)
        print(destination.name, visible.size, (x, y))


if __name__ == "__main__":
    main()
