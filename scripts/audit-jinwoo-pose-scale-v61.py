"""Fail when locomotion poses change Jinwoo's apparent body size.

This is deliberately pose-aware: a crouch should be shorter than idle, but it
must not become a much wider or differently scaled character.  Pixel clipping
and component audits cannot detect that class of visual regression.
"""
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
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/pose-scale-v61/audit.json"
IDLE_KEY = (61013, 24)
CROUCH_ACTIONS = (10, 11, 12)


def actions(text: str) -> dict[int, list[dict[str, float | int]]]:
    result: dict[int, list[dict[str, float | int]]] = {}
    current = None
    for raw in text.splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1))
            result.setdefault(current, [])
            continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result[current].append({"group": group, "frame": frame, "sx": sx, "sy": sy})
    return result


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    air = actions((LIVE / "anim.air").read_text(encoding="latin1"))
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    char_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    char_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))
    sff = Sff(LIVE / "spr.sff")
    failures: list[str] = []

    # Use the canonical idle AIR scale rather than assuming a magic number.
    idle_rows = [row for row in air.get(0, []) if (row["group"], row["frame"]) == IDLE_KEY]
    if not idle_rows or IDLE_KEY not in sff.keys:
        raise RuntimeError(f"canonical idle frame is unavailable: {IDLE_KEY}")
    idle_row = idle_rows[0]

    def metric(key: tuple[int, int], sx: float, sy: float) -> dict[str, object]:
        image = sff.decode(sff.keys[key]).convert("RGBA")
        box = image.getchannel("A").getbbox()
        if not box:
            return {"key": list(key), "bbox": None, "world_width": 0.0, "world_height": 0.0}
        return {
            "key": list(key),
            "bbox": list(box),
            "air_scale": [sx, sy],
            "world_width": round((box[2] - box[0]) * sx * char_x, 3),
            "world_height": round((box[3] - box[1]) * sy * char_y, 3),
        }

    idle = metric(IDLE_KEY, float(idle_row["sx"]), float(idle_row["sy"]))
    idle_w, idle_h = float(idle["world_width"]), float(idle["world_height"])
    crouch: list[dict[str, object]] = []
    expected = {10: [0, 1], 11: [1], 12: [1, 2]}
    for action in CROUCH_ACTIONS:
        rows = air.get(action, [])
        actual = [(int(row["group"]), int(row["frame"])) for row in rows]
        wanted = [(61024, frame) for frame in expected[action]]
        if actual != wanted:
            failures.append(f"crouch action {action} is not exclusive to the approved bank: {actual}")
        for row in rows:
            key = (int(row["group"]), int(row["frame"]))
            if key not in sff.keys:
                failures.append(f"crouch action {action} references missing sprite {key}")
                continue
            item = metric(key, float(row["sx"]), float(row["sy"]))
            item["action"] = action
            item["width_ratio_to_idle"] = round(float(item["world_width"]) / idle_w, 3)
            item["height_ratio_to_idle"] = round(float(item["world_height"]) / idle_h, 3)
            crouch.append(item)

    # Deduplicate repeated held frames before evaluating/reporting bounds.
    unique = {(tuple(item["key"]), tuple(item["air_scale"])): item for item in crouch}.values()
    max_width_ratio = max((float(item["width_ratio_to_idle"]) for item in unique), default=999.0)
    if max_width_ratio > 1.27:
        failures.append(f"crouch becomes too wide: {max_width_ratio:.3f}x idle (limit 1.27x)")
    held = [item for item in unique if item["key"] == [61024, 1]]
    held_height_ratio = float(held[0]["height_ratio_to_idle"]) if held else 0.0
    if not 0.65 <= held_height_ratio <= 0.78:
        failures.append(f"held crouch height is implausible: {held_height_ratio:.3f}x idle")
    transition_heights = [float(item["height_ratio_to_idle"]) for item in unique if item["key"] != [61024, 1]]
    if any(not 0.82 <= ratio <= 0.95 for ratio in transition_heights):
        failures.append(f"crouch transition height drift: {transition_heights}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "character_scale": [char_x, char_y],
        "idle": idle,
        "crouch": list(unique),
        "max_crouch_width_ratio": round(max_width_ratio, 3),
        "held_crouch_height_ratio": round(held_height_ratio, 3),
        "limits": {"max_width_ratio": 1.27, "held_height_ratio": [0.65, 0.78], "transition_height_ratio": [0.82, 0.95]},
        "failures": failures,
    }
    # Render the same SFF sprites at their effective runtime scales so a human
    # review sees exactly what the numeric gate is measuring.
    preview_items = [("idle", IDLE_KEY, float(idle_row["sx"]), float(idle_row["sy"]))]
    for item in unique:
        preview_items.append((f"crouch {item['key'][1]}", tuple(item["key"]), float(item["air_scale"][0]), float(item["air_scale"][1])))
    cell_w, cell_h, zoom = 240, 180, 3.0
    sheet = Image.new("RGBA", (cell_w * len(preview_items), cell_h), (18, 25, 48, 255))
    draw = ImageDraw.Draw(sheet)
    for slot, (label, key, sx, sy) in enumerate(preview_items):
        index = sff.keys[key]
        source = sff.decode(index).convert("RGBA")
        px, py = sx * char_x * zoom, sy * char_y * zoom
        rendered = source.resize((max(1, round(source.width * px)), max(1, round(source.height * py))), Image.Resampling.LANCZOS)
        axis_x, axis_y = sff.headers[index][4:6]
        root_x, root_y = slot * cell_w + cell_w // 2, 154
        sheet.alpha_composite(rendered, (root_x - round(axis_x * px), root_y - round(axis_y * py)))
        draw.line((slot * cell_w + 8, root_y, (slot + 1) * cell_w - 8, root_y), fill=(70, 105, 180, 255), width=1)
        draw.text((slot * cell_w + 8, 8), label, fill="white")
    preview = OUT.parent / "idle-vs-crouch-runtime-scale.png"
    sheet.save(preview, optimize=True)
    report["preview"] = str(preview)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
