"""Translate mode-400 candidates to safe canvas margins without rescaling art."""
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "mode-400-candidates"
TARGET = BASE / "mode-400-normalized"
MIN_MARGIN = 16


def axis_shift(start: int, end: int, limit: int) -> int:
    low = MIN_MARGIN - start
    high = limit - MIN_MARGIN - end
    if low > high:
        raise ValueError(f"content cannot fit with {MIN_MARGIN}px margins: {start}-{end}/{limit}")
    return min(max(0, low), high)


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for path in sorted(SOURCE.glob("*.png")):
        image = Image.open(path).convert("RGBA")
        solid = image.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
        bbox = solid.getbbox()
        if bbox is None:
            raise ValueError(f"empty candidate: {path.name}")
        left, top, right, bottom = bbox
        available_w = image.width - 2 * MIN_MARGIN
        available_h = image.height - 2 * MIN_MARGIN
        content_w = right - left
        content_h = bottom - top
        scale = min(1.0, available_w / content_w, available_h / content_h)
        if scale < 1.0:
            scale *= 0.997
            new_size = (round(image.width * scale), round(image.height * scale))
            resized = image.resize(new_size, Image.Resampling.LANCZOS)
            fitted = Image.new("RGBA", image.size, (0, 0, 0, 0))
            fitted.alpha_composite(
                resized,
                ((image.width - new_size[0]) // 2, (image.height - new_size[1]) // 2),
            )
            image = fitted
            solid = image.getchannel("A").point(lambda value: 255 if value >= 96 else 0)
            bbox = solid.getbbox()
            if bbox is None:
                raise ValueError(f"empty candidate after fit: {path.name}")
            left, top, right, bottom = bbox
        dx = axis_shift(left, right, image.width)
        dy = axis_shift(top, bottom, image.height)
        canvas = Image.new("RGBA", image.size, (0, 0, 0, 0))
        canvas.alpha_composite(image, (dx, dy))
        out = TARGET / path.name
        canvas.save(out)
        moved = tuple(value + (dx if index % 2 == 0 else dy) for index, value in enumerate(bbox))
        print({"file": path.name, "scale": round(scale, 6), "shift": [dx, dy], "opaque_bbox": moved})


if __name__ == "__main__":
    main()
