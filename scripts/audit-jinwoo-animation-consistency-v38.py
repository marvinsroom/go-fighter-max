"""Audit live Jinwoo body scale/baselines and render key animation contact sheets."""
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
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/audit-v38"
BODY_GROUPS = {300, 400, *range(61000, 61014)}
SHEET_ACTIONS = (0, 10, 20, 21, 40, 41, 42, 43, 44, 45, 47, 2210, 2215, 2220, 2225, 2230, 2235, 2250, 2260, 2290)


def actions(path: Path) -> dict[int, list[dict[str, object]]]:
    result: dict[int, list[dict[str, object]]] = {}
    current: int | None = None
    for raw in path.read_text(encoding="latin1").splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if match:
            current = int(match.group(1)); result.setdefault(current, [])
            continue
        if current is None or not re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", raw):
            continue
        fields = [part.strip() for part in raw.split(",")]
        try:
            group, image = int(fields[0]), int(fields[1])
            sx = float(fields[7]) if len(fields) > 7 and fields[7] else 1.0
            sy = float(fields[8]) if len(fields) > 8 and fields[8] else 1.0
        except (ValueError, IndexError):
            continue
        result[current].append({"group": group, "image": image, "sx": sx, "sy": sy, "raw": raw})
    return result


def metric(sff: Sff, frame: dict[str, object]) -> dict[str, object] | None:
    key = (int(frame["group"]), int(frame["image"]))
    index = sff.keys.get(key)
    if index is None:
        return None
    image = sff.decode(index)
    box = image.getchannel("A").getbbox()
    if box is None:
        return None
    header = sff.headers[index]
    sx, sy = float(frame["sx"]), float(frame["sy"])
    return {
        "key": list(key), "scale": [sx, sy], "source_size": list(image.size),
        "axis": [header[4], header[5]], "bbox": list(box),
        "world_width": round((box[2] - box[0]) * sx, 3),
        "world_height": round((box[3] - box[1]) * sy, 3),
        "world_top": round((box[1] - header[5]) * sy, 3),
        "world_bottom": round((box[3] - header[5]) * sy, 3),
    }


def sheet(sff: Sff, parsed: dict[int, list[dict[str, object]]], action_ids: tuple[int, ...]) -> None:
    tiles: list[tuple[str, Image.Image]] = []
    seen: set[tuple[int, int, int]] = set()
    for action in action_ids:
        for frame in parsed.get(action, []):
            key = (int(frame["group"]), int(frame["image"]))
            identity = (action, *key)
            if key not in sff.keys or identity in seen:
                continue
            seen.add(identity)
            source = sff.decode(sff.keys[key])
            box = source.getchannel("A").getbbox()
            if not box:
                continue
            crop = source.crop(box)
            crop.thumbnail((180, 180), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (210, 225), (24, 26, 38, 255))
            tile.alpha_composite(crop, ((210 - crop.width) // 2, 8 + (180 - crop.height)))
            tiles.append((f"A{action} {key[0]},{key[1]} {frame['sx']:.4g}x{frame['sy']:.4g}", tile))
    columns = 5; rows = (len(tiles) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * 210, rows * 225), (16, 17, 26))
    draw = ImageDraw.Draw(canvas)
    for index, (label, tile) in enumerate(tiles):
        x, y = index % columns * 210, index // columns * 225
        canvas.paste(tile.convert("RGB"), (x, y))
        draw.text((x + 5, y + 205), label, fill=(235, 238, 255))
    canvas.save(OUT / "core-and-knight-contact-sheet.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parsed = actions(LIVE / "anim.air")
    sff = Sff(LIVE / "spr.sff")
    report: dict[str, object] = {"actions": {}, "scale_outliers": []}
    for action, frames in parsed.items():
        metrics = [value for frame in frames if int(frame["group"]) in BODY_GROUPS if (value := metric(sff, frame))]
        if not metrics:
            continue
        report["actions"][str(action)] = metrics
        heights = [float(item["world_height"]) for item in metrics]
        if len(heights) > 1 and min(heights) > 0 and max(heights) / min(heights) > 1.08:
            report["scale_outliers"].append({"action": action, "min": min(heights), "max": max(heights), "ratio": round(max(heights) / min(heights), 4)})
    report["jump_actions_identical"] = all(
        [(f["group"], f["image"], f["sx"], f["sy"]) for f in parsed.get(action, [])]
        == [(f["group"], f["image"], f["sx"], f["sy"]) for f in parsed.get(40, [])]
        for action in (41, 42, 43, 44, 45, 47)
    )
    report["knight_forward_state_uses_backward_action"] = bool(re.search(
        r"(?is)\[Statedef 2220\].*?\banim\s*=.*?\(2225\)",
        (LIVE / "cns.cns").read_text(encoding="latin1"),
    ))
    (OUT / "animation-consistency.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    sheet(sff, parsed, SHEET_ACTIONS)
    print(json.dumps({
        "jump_actions_identical": report["jump_actions_identical"],
        "knight_forward_state_uses_backward_action": report["knight_forward_state_uses_backward_action"],
        "scale_outlier_count": len(report["scale_outliers"]),
        "report": str(OUT / "animation-consistency.json"),
        "sheet": str(OUT / "core-and-knight-contact-sheet.png"),
    }, indent=2))


if __name__ == "__main__":
    main()
