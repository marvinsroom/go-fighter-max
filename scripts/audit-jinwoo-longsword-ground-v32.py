"""Mechanically gate the eight v32 long-sword ground-normal drawings."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "attack-normalized"
REPORT = BASE / "longsword-ground-audit-v32.json"
SHEET = BASE / "longsword-ground-sheet-v32.png"
EXPECTED = [
    "61010-008-longsword-ready-v32.png",
    "61010-009-longsword-windup-v32.png",
    "61010-010-longsword-raised-v32.png",
    "61010-011-longsword-midswing-v32.png",
    "61010-012-longsword-impact-v32.png",
    "61010-013-longsword-followthrough-v32.png",
    "61010-014-longsword-recovery-v32.png",
    "61010-015-longsword-return-v32.png",
]
TARGET_WORLD_HEIGHT = 54.8192771084
SCALE = 0.037342832


def main() -> None:
    errors: list[str] = []
    rows: list[dict] = []
    thumbs: list[Image.Image] = []
    for offset, name in enumerate(EXPECTED):
        number = 8 + offset
        path = SOURCE / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        image = Image.open(path).convert("RGBA")
        bbox = image.getchannel("A").point(lambda value: 255 if value >= 8 else 0).getbbox()
        if image.size != (1536, 1536):
            errors.append(f"{name}: wrong canvas {image.size}")
        if not bbox:
            errors.append(f"{name}: empty alpha")
            continue
        margins = [bbox[0], bbox[1], 1536 - bbox[2], 1536 - bbox[3]]
        if min(margins) < 16:
            errors.append(f"{name}: unsafe alpha margin {margins}")
        rows.append(
            {
                "key": [61010, number],
                "file": name,
                "bbox": list(bbox),
                "margins": margins,
                "visible_size": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
        thumb = Image.new("RGBA", (384, 384), (28, 31, 42, 255))
        visible = image.crop(bbox)
        visible.thumbnail((352, 330), Image.Resampling.LANCZOS)
        thumb.alpha_composite(visible, ((384 - visible.width) // 2, 28 + (330 - visible.height) // 2))
        ImageDraw.Draw(thumb).text((12, 356), f"61010,{number}", fill="white")
        thumbs.append(thumb)

    if len(rows) != 8:
        errors.append(f"expected 8 frames, found {len(rows)}")
    world_height = rows[0]["visible_size"][1] * SCALE if rows else None
    if world_height is not None and abs(world_height - TARGET_WORLD_HEIGHT) > 0.2:
        errors.append(f"ready world height {world_height:.4f} != {TARGET_WORLD_HEIGHT:.4f}")
    if len(thumbs) == 8:
        sheet = Image.new("RGBA", (1536, 768), (18, 20, 28, 255))
        for index, thumb in enumerate(thumbs):
            sheet.alpha_composite(thumb, ((index % 4) * 384, (index // 4) * 384))
        sheet.save(SHEET)
    report = {
        "status": "PASS" if not errors else "FAIL",
        "family": "long-sword ground normals",
        "keys": [[61010, number] for number in range(8, 16)],
        "frame_count": len(rows),
        "canvas": [1536, 1536],
        "air_scale": SCALE,
        "ready_world_height": world_height,
        "naruto_relative_height_ratio": TARGET_WORLD_HEIGHT / 50.0,
        "manual_visual_requirements": [
            "exactly two arms and hands",
            "exactly one cyan-aura black long sword",
            "sword remains in right hand through the sequence",
            "two complete legs and low black dress shoes",
            "visible eyes aimed at the screen-right opponent",
            "no daggers, missing body part, or opaque canvas background",
        ],
        "frames": rows,
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
