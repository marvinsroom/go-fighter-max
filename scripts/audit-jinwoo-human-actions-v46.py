"""Render human Jinwoo gameplay actions for identity and stature review."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/human-action-audit-v46"
ACTION_IDS = (0, 200, 500, 501)


def parse_actions(text: str) -> dict[int, list[tuple[int, int, float, float]]]:
    result: dict[int, list[tuple[int, int, float, float]]] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current = int(match.group(1)); result.setdefault(current, [])
            continue
        if current is None or not re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", line):
            continue
        fields = [value.strip() for value in line.split(";")[0].split(",")]
        fields += [""] * (9 - len(fields))
        try:
            result[current].append((int(fields[0]), int(fields[1]),
                                    float(fields[7] or 1), float(fields[8] or 1)))
        except ValueError:
            pass
    return result


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parsed = parse_actions((LIVE / "anim.air").read_text(encoding="latin1"))
    sff = Sff(LIVE / "spr.sff")
    cache: dict[tuple[int, int], Image.Image] = {}
    tiles: list[tuple[str, Image.Image]] = []
    report: dict[str, list[dict[str, object]]] = {}
    for action in ACTION_IDS:
        rows = []
        seen = set()
        for group, number, sx, sy in parsed.get(action, []):
            key = (group, number)
            if key not in sff.keys:
                continue
            if key not in cache:
                cache[key] = sff.decode(sff.keys[key])
            source = cache[key]
            box = source.getchannel("A").getbbox()
            if not box:
                continue
            height = (box[3] - box[1]) * sy
            rows.append({"key": list(key), "scale": [sx, sy], "world_height": round(height, 3)})
            identity = (key, sx, sy)
            if identity in seen:
                continue
            seen.add(identity)
            crop = source.crop(box)
            display_height = max(1, round((box[3] - box[1]) * sy * 4))
            display_width = max(1, round((box[2] - box[0]) * sx * 4))
            crop = crop.resize((display_width, display_height), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (240, 240), (22, 24, 36, 255))
            tile.alpha_composite(crop, ((240 - crop.width) // 2, 208 - crop.height))
            tiles.append((f"A{action} {group},{number} H={height:.1f}", tile))
        if rows:
            report[str(action)] = rows

    columns = 5
    rows = (len(tiles) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * 240, rows * 240), (14, 15, 24))
    draw = ImageDraw.Draw(canvas)
    for index, (label, tile) in enumerate(tiles):
        x, y = (index % columns) * 240, (index // columns) * 240
        canvas.paste(tile.convert("RGB"), (x, y))
        draw.text((x + 5, y + 218), label, fill=(240, 242, 255))
    canvas.save(OUT / "human-actions.png")
    (OUT / "human-actions.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"actions": len(report), "unique_sprites": len(cache),
                      "sheet": str(OUT / "human-actions.png")}, indent=2))


if __name__ == "__main__":
    main()
