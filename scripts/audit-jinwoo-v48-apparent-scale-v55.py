"""Audit active Jinwoo art at one fixed render scale and expose camera-size drift."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/scale-lock-v55"
GROUPS = (61013, 61015, 61016, 61017, 61018, 61019, 61020, 61021,
          61022, 61023, 61024)


def air_scales() -> dict[tuple[int, int], set[tuple[float, float]]]:
    result: dict[tuple[int, int], set[tuple[float, float]]] = defaultdict(set)
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) < 2:
            continue
        try:
            key = (int(fields[0].strip()), int(fields[1].strip()))
        except ValueError:
            continue
        if key[0] not in GROUPS:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result[key].add((sx, sy))
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sff = Sff(LIVE / "spr.sff")
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    character_xscale = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    character_yscale = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))
    scales = air_scales()
    keys = [key for key in sorted(scales) if key in sff.keys]
    cell_w, cell_h, columns = 260, 190, 6
    rows = (len(keys) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), (17, 20, 29, 255))
    draw = ImageDraw.Draw(sheet)
    metrics = []
    for slot, key in enumerate(keys):
        index = sff.keys[key]
        image = sff.decode(index).convert("RGBA")
        box = image.getchannel("A").getbbox()
        axis_x, axis_y = sff.headers[index][4:6]
        sx, sy = sorted(scales[key])[0]
        # Display at the real runtime ratio, enlarged only for readability.
        preview_x = sx * character_xscale * 3.0
        preview_y = sy * character_yscale * 3.0
        rendered = image.resize(
            (max(1, round(image.width * preview_x)), max(1, round(image.height * preview_y))),
            Image.Resampling.LANCZOS,
        )
        x0 = (slot % columns) * cell_w
        y0 = (slot // columns) * cell_h
        root_x, root_y = x0 + cell_w // 2, y0 + 155
        paste_x = root_x - round(axis_x * preview_x)
        paste_y = root_y - round(axis_y * preview_y)
        sheet.alpha_composite(rendered, (paste_x, paste_y))
        draw.line((x0 + 8, root_y, x0 + cell_w - 8, root_y), fill=(58, 74, 100, 255))
        draw.text((x0 + 8, y0 + 6), f"{key[0]},{key[1]}", fill="white")
        world_w = (box[2] - box[0]) * sx * character_xscale if box else 0.0
        world_h = (box[3] - box[1]) * sy * character_yscale if box else 0.0
        metrics.append({
            "key": list(key), "bbox": list(box) if box else None,
            "air_scale": [sx, sy], "world_bbox": [round(world_w, 3), round(world_h, 3)],
        })
    preview = OUT / "active-v48-fixed-scale-contact-sheet.png"
    sheet.save(preview, optimize=True)
    report = {
        "groups": list(GROUPS), "frame_count": len(keys),
        "character_scale": [character_xscale, character_yscale],
        "metrics": metrics, "preview": str(preview),
    }
    (OUT / "apparent-scale-audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"frame_count": len(keys), "preview": str(preview)}, indent=2))


if __name__ == "__main__":
    main()
