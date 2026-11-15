"""Normalize v32 movement canvases without regenerating or cropping artwork."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SET = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = SET / "source-body"
RAW = SET / "raw-source-body"
PLAN = SET / "movement-plan-v32.json"
SCALE = 0.94


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    required = sorted({name for seq in plan["required_sequences"].values() for name in seq})
    RAW.mkdir(parents=True, exist_ok=True)
    processed = []
    for name in required:
        source = SOURCE / name
        raw = RAW / name
        if not source.exists() and not raw.exists():
            continue
        if source.exists() and not raw.exists():
            shutil.copy2(source, raw)
        with Image.open(raw) as im:
            rgba = im.convert("RGBA")
            if rgba.size != (1024, 1536):
                raise RuntimeError(f"unexpected canvas for {name}: {rgba.size}")
            resized = rgba.resize(
                (round(rgba.width * SCALE), round(rgba.height * SCALE)),
                Image.Resampling.LANCZOS,
            )
            out = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
            out.alpha_composite(
                resized,
                ((rgba.width - resized.width) // 2, (rgba.height - resized.height) // 2),
            )
            out.save(source)
            processed.append(name)
    print(json.dumps({"scale": SCALE, "processed": processed}, indent=2))


if __name__ == "__main__":
    main()
