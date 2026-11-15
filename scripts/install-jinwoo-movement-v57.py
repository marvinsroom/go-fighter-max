"""Install the generated v57 walk/jump banks and make charging non-locking."""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/movement-v57"
AIR = LIVE / "anim.air"
CNS = LIVE / "cns.cns"
SFF_PATH = LIVE / "spr.sff"
BACKUP = ART / "live-before-movement-v57"
REPORT = ART / "installation.json"
MARKER = "; JINWOO MOVEMENT V57"
WALK_GROUP, JUMP_GROUP = 61022, 61023
TARGET_SOURCE_HEIGHT = 47.097
X_TO_Y = 0.095218974 / 0.089829218


def encode(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {
        "image": image,
        "png": payload.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
    }


def split_sheet(path: Path) -> list[Image.Image]:
    sheet = Image.open(path).convert("RGBA")
    if sheet.width % 6:
        raise RuntimeError(f"sheet is not six equal cells: {path.name} {sheet.size}")
    cell_width = sheet.width // 6
    frames = []
    for index in range(6):
        cell = sheet.crop((index * cell_width, 0, (index + 1) * cell_width, sheet.height))
        alpha = cell.getchannel("A").point(lambda value: 0 if value < 24 else value)
        mask = (np.asarray(alpha) > 0).astype(np.uint8)
        count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        if count <= 1:
            raise RuntimeError(f"empty cell {index} in {path.name}")
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = Image.fromarray(np.where(labels == largest, np.asarray(alpha), 0).astype(np.uint8), mode="L")
        cell.putalpha(alpha)
        box = alpha.getbbox()
        if not box:
            raise RuntimeError(f"empty cell {index} in {path.name}")
        drawing = cell.crop(box)
        canvas = Image.new("RGBA", (drawing.width + 32, drawing.height + 32), (0, 0, 0, 0))
        canvas.alpha_composite(drawing, (16, 16))
        frames.append(canvas)
    return frames


def action(number: int, group: int, frames: list[int], durations: list[int], loop_at: int | None = None) -> str:
    lines = [f"[Begin Action {number}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
    for index, (frame, duration) in enumerate(zip(frames, durations, strict=True)):
        if loop_at == index:
            lines.append("LoopStart")
        lines.append(f"{group},{frame},0,0,{duration},,,{{SX}},{{SY}}")
    return "\n".join(lines)


def charge_action(number: int, duration: int = 8) -> str:
    # One approved body drawing, with only a two-pixel breathing arc. This
    # animates the hold without the chaotic identity/size swaps seen before.
    lines = [
        f"[Begin Action {number}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0", "LoopStart",
        f"61019,0,0,0,{duration},,,0.101895680,0.096128000",
        f"61019,0,0,-1,{duration},,,0.101895680,0.096128000",
        f"61019,0,0,-2,{duration},,,0.101895680,0.096128000",
        f"61019,0,0,-1,{duration},,,0.101895680,0.096128000",
    ]
    return "\n".join(lines)


def replace_action(text: str, number: int, replacement: str) -> str:
    found = re.search(
        rf"(?ims)^\[Begin Action\s+{number}\][ \t]*\r?\n.*?(?=^\[Begin Action\s+-?\d+\][ \t]*\r?\n|\Z)", text
    )
    if not found:
        raise RuntimeError(f"missing action {number}")
    return text[:found.start()] + replacement.rstrip() + "\n\n" + text[found.end():]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        for source in (AIR, CNS, SFF_PATH):
            shutil.copy2(source, BACKUP / source.name)

    walk = split_sheet(ART / "walk-sheet-v57.png")
    jump = split_sheet(ART / "jump-sheet-v57.png")
    walk_heights = [frame.getchannel("A").getbbox()[3] - frame.getchannel("A").getbbox()[1] for frame in walk]
    reference_height = sorted(walk_heights)[len(walk_heights) // 2]
    sy = TARGET_SOURCE_HEIGHT / reference_height
    sx = sy * X_TO_Y

    additions = {}
    frame_report = []
    normalized = ART / "normalized"
    normalized.mkdir(exist_ok=True)
    for group, bank in ((WALK_GROUP, walk), (JUMP_GROUP, jump)):
        for number, image in enumerate(bank):
            box = image.getchannel("A").getbbox()
            axis = (image.width // 2, box[3] - 18)
            image.save(normalized / f"{group}-{number}.png", optimize=True)
            additions[(group, number)] = encode(image, axis)
            frame_report.append({"key": [group, number], "size": list(image.size), "bbox": list(box), "axis": list(axis)})
    sff = Sff(SFF_PATH)
    replacements = {key: frame for key, frame in additions.items() if key in sff.keys}
    new = {key: frame for key, frame in additions.items() if key not in sff.keys}
    pending = SFF_PATH.with_suffix(".v57.pending")
    pending.write_bytes(sff.derive(replacements, new))
    pending.replace(SFF_PATH)

    templates = {
        20: action(20, WALK_GROUP, [0, 1, 2, 3, 4, 5], [4] * 6, 0),
        21: action(21, WALK_GROUP, [5, 4, 3, 2, 1, 0], [4] * 6, 0),
        40: action(40, JUMP_GROUP, [0, 1], [3, 3]),
        41: action(41, JUMP_GROUP, [1, 2, 3], [3, 5, 6], 1),
        42: action(42, JUMP_GROUP, [2, 3], [5, 6], 0),
        43: action(43, JUMP_GROUP, [3, 4], [5, 6], 0),
        44: action(44, JUMP_GROUP, [3, 4], [4, 6], 0),
        45: action(45, JUMP_GROUP, [3, 4], [4, 6], 0),
        47: action(47, JUMP_GROUP, [4, 5], [3, 5]),
        50: action(50, JUMP_GROUP, [1, 2, 3], [3, 5, 6], 1),
        52: action(52, JUMP_GROUP, [3, 4], [4, 6], 0),
    }
    air = AIR.read_text(encoding="latin1")
    for number, template in templates.items():
        air = replace_action(air, number, template.replace("{SX}", f"{sx:.9f}").replace("{SY}", f"{sy:.9f}"))
    for number in (500, 10500, 20500):
        air = replace_action(air, number, charge_action(number))
    AIR.write_text(air.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    cns = CNS.read_text(encoding="latin1")
    state = re.search(r"(?ims)^\[statedef 500\].*?(?=^\[statedef 501\])", cns)
    if not state:
        raise RuntimeError("missing charge state 500")
    block = state.group(0)
    old = 'trigger1 = ailevel = 0 && command != "hold_d" && command != "holdstart" || ailevel > 0 && power >= powermax'
    new_release = 'trigger1 = ailevel = 0 && !command = "our_holdcharge" || ailevel > 0 && power >= powermax\ntrigger3 = ailevel = 0 && time >= 300'
    if old not in block and new_release not in block:
        raise RuntimeError("charge release controller changed unexpectedly")
    block = block.replace(old, new_release)
    cns = cns[:state.start()] + block + cns[state.end():]
    CNS.write_text(cns, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "walk_group": WALK_GROUP,
        "jump_group": JUMP_GROUP,
        "air_scale": [sx, sy],
        "walk_height_spread_pixels": [min(walk_heights), max(walk_heights)],
        "charge_watchdog_ticks": 300,
        "charge_body_frames": 1,
        "frames": frame_report,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
