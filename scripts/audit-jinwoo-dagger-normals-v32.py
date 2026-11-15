"""Mechanically gate the eight v32 dual-dagger ground-normal drawings."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "attack-normalized"
REPORT = BASE / "dagger-normal-audit-v32.json"
SHEET = BASE / "dagger-normal-sheet-v32.png"
EXPECTED = [
    "61010-000-dagger-stance-v32.png",
    "61010-001-dagger-anticipation-v32.png",
    "61010-002-dagger-lunge-v32.png",
    "61010-003-dagger-slash-v32.png",
    "61010-004-dagger-thrust-v32.png",
    "61010-005-dagger-followthrough-v32.png",
    "61010-006-dagger-recovery-v32.png",
    "61010-007-dagger-return-v32.png",
]
TARGET_WORLD_HEIGHT = 54.8192771084
DAGGER_SCALE = 0.04783532


def main() -> None:
    errors: list[str] = []
    rows: list[dict] = []
    thumbs: list[Image.Image] = []
    for number, name in enumerate(EXPECTED):
        path = SOURCE / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        image = Image.open(path).convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.point(lambda value: 255 if value >= 8 else 0).getbbox()
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
    if rows:
        upright_height = rows[0]["visible_size"][1]
        world_height = upright_height * DAGGER_SCALE
        if abs(world_height - TARGET_WORLD_HEIGHT) > 0.1:
            errors.append(f"standing world height {world_height:.4f} != {TARGET_WORLD_HEIGHT:.4f}")
    else:
        world_height = None

    if len(thumbs) == 8:
        sheet = Image.new("RGBA", (1536, 768), (18, 20, 28, 255))
        for index, thumb in enumerate(thumbs):
            sheet.alpha_composite(thumb, ((index % 4) * 384, (index // 4) * 384))
        sheet.save(SHEET)

    report = {
        "status": "PASS" if not errors else "FAIL",
        "family": "dual-dagger ground normals",
        "keys": [[61010, index] for index in range(8)],
        "frame_count": len(rows),
        "canvas": [1536, 1536],
        "air_scale": DAGGER_SCALE,
        "standing_world_height": world_height,
        "naruto_relative_height_ratio": TARGET_WORLD_HEIGHT / 50.0,
        "manual_visual_requirements": [
            "exactly two arms and hands",
            "exactly two matching violet-black daggers, one gripped in each hand",
            "two complete legs and low black dress shoes",
            "visible eyes aimed at the screen-right opponent",
            "no long sword, missing body part, or full-canvas opaque effect",
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
