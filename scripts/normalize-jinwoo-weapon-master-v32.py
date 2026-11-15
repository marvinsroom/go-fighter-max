"""Add a guaranteed transparent safety margin to the v32 long-sword candidate."""
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/weapon-masters"
SOURCE = DIRECTORY / "long-sword-candidate-v32.png"
TARGET = DIRECTORY / "long-sword-candidate-v32-normalized.png"
SCALE = 0.84


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    alpha_box = image.getchannel("A").getbbox()
    if alpha_box is None:
        raise SystemExit("candidate has no visible pixels")
    cropped = image.crop(alpha_box)
    limit_w = int(image.width * SCALE)
    limit_h = int(image.height * SCALE)
    factor = min(limit_w / cropped.width, limit_h / cropped.height)
    size = (max(1, round(cropped.width * factor)), max(1, round(cropped.height * factor)))
    resized = cropped.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
    position = ((image.width - size[0]) // 2, (image.height - size[1]) // 2)
    canvas.alpha_composite(resized, position)
    canvas.save(TARGET)
    print({"target": str(TARGET), "canvas": image.size, "content": size, "position": position})


if __name__ == "__main__":
    main()
