"""Verify the v48 unified base bank and Naruto portrait replacement."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48"
AIR = LIVE / "anim.air"
SFF_PATH = LIVE / "spr.sff"
GROUP = 61013
EXPECTED_ACTIONS = {0, 10, 11, 12, 20, 21, 40, 41, 42, 43, 44, 45, 47, 50, 52, 100, 105,
                    200, 210, 220, 260, 300, 310, 320, 350}
DELETED_KEYS = {
    *( (300, n) for n in [2, 89, 90, 91, *range(101, 106), *range(108, 114), *range(115, 122),
                           124, 125, 127, 128, 129, 130, 131] ),
    *( (61012, n) for n in range(8) ),
}


def parse_air(text: str) -> dict[int, list[tuple[int, int, float, float]]]:
    actions = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current = int(match.group(1)); actions.setdefault(current, []); continue
        parts = line.split(",")
        if current is not None and len(parts) >= 2:
            try:
                group, number = int(parts[0].strip()), int(parts[1].strip())
            except ValueError:
                continue
            sx = float(parts[7]) if len(parts) > 8 and parts[7].strip() else 1.0
            sy = float(parts[8]) if len(parts) > 8 and parts[8].strip() else 1.0
            actions[current].append((group, number, sx, sy))
    return actions


def main() -> None:
    failures = []
    text = AIR.read_text(encoding="latin1")
    actions = parse_air(text)
    sff = Sff(SFF_PATH)

    jinwoo_cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    size_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", jinwoo_cns).group(1))
    size_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", jinwoo_cns).group(1))
    if (size_x, size_y) != (1.5, 1.0):
        failures.append(f"hidden character-wide scale remains: {(size_x, size_y)}")

    scales = set()
    used_numbers = set()
    for action in EXPECTED_ACTIONS:
        rows = actions.get(action, [])
        if not rows:
            failures.append(f"action {action} has no sprite rows")
            continue
        bad = [(g, n) for g, n, _, _ in rows if g != GROUP]
        if bad:
            failures.append(f"action {action} escaped unified group: {bad}")
        for group, number, sx, sy in rows:
            if group == GROUP:
                used_numbers.add(number); scales.add((round(sx, 9), round(sy, 9)))

    if len(scales) != 1:
        failures.append(f"base actions do not share one locked scale: {sorted(scales)}")
    stale_refs = []
    for action, rows in actions.items():
        for group, number, _, _ in rows:
            if (group, number) in DELETED_KEYS:
                stale_refs.append((action, group, number))
    if stale_refs:
        failures.append(f"AIR still references deleted sprites: {stale_refs[:20]}")
    surviving = sorted(key for key in DELETED_KEYS if key in sff.keys)
    if surviving:
        failures.append(f"obsolete SFF sprites survived: {surviving}")

    frame_metrics = []
    thumbs = []
    sy = next(iter(scales))[1] if len(scales) == 1 else 0.0
    for number in range(25):
        key = (GROUP, number)
        if key not in sff.keys:
            failures.append(f"missing {key}"); continue
        image = sff.decode(sff.keys[key]).convert("RGBA")
        box = image.getchannel("A").getbbox()
        if not box:
            failures.append(f"empty {key}"); continue
        if min(box[0], box[1], image.width - box[2], image.height - box[3]) < 1:
            failures.append(f"clipped {key}: {box} in {image.size}")
        world_height = round((box[3] - box[1]) * sy, 3)
        frame_metrics.append({"key": list(key), "size": list(image.size), "bbox": list(box), "world_height": world_height})
        thumb = image.copy(); thumb.thumbnail((190, 190), Image.Resampling.LANCZOS); thumbs.append((number, thumb))

    sheet = Image.new("RGBA", (5 * 220, 5 * 225), (20, 22, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for slot, (number, thumb) in enumerate(thumbs):
        x = (slot % 5) * 220 + (220 - thumb.width) // 2
        y = (slot // 5) * 225 + 8 + (190 - thumb.height)
        sheet.alpha_composite(thumb, (x, y))
        draw.text(((slot % 5) * 220 + 8, (slot // 5) * 225 + 202), f"61013,{number}", fill="white")
    preview = ART / "unified-base-v48-contact-sheet.png"
    sheet.save(preview, optimize=True)

    naruto = Sff(ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto/Naruto_Ashura_JUS.sff")
    naruto_cns = (ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto/Naruto.cns").read_text(encoding="latin1")
    naruto_size_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", naruto_cns).group(1))
    naruto_idle = naruto.decode(naruto.keys[(0, 0)]).convert("RGBA")
    naruto_box = naruto_idle.getchannel("A").getbbox()
    naruto_height = (naruto_box[3] - naruto_box[1]) * naruto_size_y
    jinwoo_idle = sff.decode(sff.keys[(GROUP, 24)]).convert("RGBA")
    jinwoo_box = jinwoo_idle.getchannel("A").getbbox()
    jinwoo_height = (jinwoo_box[3] - jinwoo_box[1]) * sy * size_y
    idle_ratio = jinwoo_height / naruto_height
    if not 1.05 <= idle_ratio <= 1.12:
        failures.append(f"Jinwoo/Naruto effective idle ratio outside 1.05-1.12: {idle_ratio:.3f}")
    jinwoo_axis_y = sff.headers[sff.keys[(GROUP, 24)]][5]
    naruto_axis_y = naruto.headers[naruto.keys[(0, 0)]][5]
    jinwoo_foot_offset = (jinwoo_box[3] - jinwoo_axis_y) * sy * size_y
    naruto_foot_offset = (naruto_box[3] - naruto_axis_y) * naruto_size_y
    if abs(jinwoo_foot_offset - naruto_foot_offset) > 0.1:
        failures.append(f"foot baseline mismatch: Jinwoo {jinwoo_foot_offset:.3f}, Naruto {naruto_foot_offset:.3f}")
    portrait_slots = {}
    for key in ((9000, 0), (9000, 1)):
        portrait = naruto.decode(naruto.keys[key]).convert("RGBA")
        portrait_slots[f"{key[0]},{key[1]}"] = {"size": list(portrait.size), "bbox": list(portrait.getchannel("A").getbbox())}
        if portrait.size != (100, 100) or portrait.getchannel("A").getbbox() != (0, 0, 100, 100):
            failures.append(f"Naruto portrait {key} not frame-fitted: size={portrait.size}, bbox={portrait.getchannel('A').getbbox()}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "unified_group": GROUP,
        "base_actions_checked": sorted(EXPECTED_ACTIONS),
        "used_frame_numbers": sorted(used_numbers),
        "locked_scales": [list(value) for value in sorted(scales)],
        "deleted_sprite_keys_verified_absent": len(DELETED_KEYS),
        "effective_idle_height": {"jinwoo": round(jinwoo_height, 3), "naruto": round(naruto_height, 3),
                                  "ratio": round(idle_ratio, 3)},
        "effective_width_multiplier": size_x,
        "foot_axis_offset": {"jinwoo": round(jinwoo_foot_offset, 3), "naruto": round(naruto_foot_offset, 3)},
        "frame_metrics": frame_metrics,
        "naruto_portraits": portrait_slots,
        "preview": str(preview.relative_to(ROOT)),
        "failures": failures,
    }
    (ART / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
