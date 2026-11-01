"""Install v48 summon-call and ultimate body animations."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/summon-super-v54"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
BACKUP = ART / "live-before-v54"
REPORT = ART / "installation.json"
SX, SY = 0.095218974, 0.089829218
MARKER = "; JINWOO V48 SUMMON SUPER V54"


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def six_components(path: Path) -> list[Image.Image]:
    sheet = Image.open(path).convert("RGBA")
    alpha = np.asarray(sheet.getchannel("A"))
    count, labels, stats, centroids = cv2.connectedComponentsWithStats((alpha >= 80).astype(np.uint8), 8)
    candidates = sorted(range(1, count), key=lambda n: int(stats[n, cv2.CC_STAT_AREA]), reverse=True)[:6]
    if len(candidates) != 6 or stats[candidates[-1], cv2.CC_STAT_AREA] < 12000:
        raise RuntimeError(f"could not isolate six bodies from {path.name}")
    candidates.sort(key=lambda n: (centroids[n][1] // (sheet.height / 2), centroids[n][0]))
    output = []
    for label in candidates:
        x, y, width, height, _ = stats[label]
        pad = 20
        left, top = max(0, x-pad), max(0, y-pad)
        right, bottom = min(sheet.width, x+width+pad), min(sheet.height, y+height+pad)
        crop = sheet.crop((left, top, right, bottom))
        local_alpha = np.asarray(crop.getchannel("A"))
        kept = np.where(labels[top:bottom, left:right] == label, local_alpha, 0).astype(np.uint8)
        crop.putalpha(Image.fromarray(kept, mode="L"))
        canvas = Image.new("RGBA", (crop.width+20, crop.height+20), (0, 0, 0, 0))
        canvas.alpha_composite(crop, (10, 10)); output.append(canvas)
    return output


def action(number: int, group: int, frames: list[int], times: list[int],
           sx: float = SX, sy: float = SY) -> str:
    lines = [f"[Begin Action {number}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
    for index, frame in enumerate(frames):
        duration = times[min(index, len(times)-1)]
        lines.append(f"{group},{frame},0,0,{duration},,,{sx:.9f},{sy:.9f}")
    return "\n".join(lines)


def replace_action(text: str, number: int, replacement: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(?ims)^\[Begin Action\s+{number}\][ \t]*\r?\n.*?(?=^\[Begin Action\s+-?\d+\][ \t]*\r?\n|\Z)")
    changed, count = pattern.subn(replacement.rstrip()+"\n\n", text, count=1)
    return changed, count == 1


def main() -> None:
    text = AIR.read_text(encoding="latin1")
    force = "--force" in sys.argv
    if MARKER in text and not force:
        print(REPORT.read_text(encoding="utf-8")); return
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        shutil.copy2(AIR, BACKUP / AIR.name); shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)

    banks = {61020: six_components(ART / "summon-call-v54.png"),
             61021: six_components(ART / "ultimate-v54.png")}
    additions, replacements, frames_report = {}, {}, []
    for group, frames in banks.items():
        for number, image in enumerate(frames):
            box = image.getchannel("A").getbbox()
            axis = (image.width // 2, box[3]-20)
            image.save(ART / f"{group}-{number}.png", optimize=True)
            target = replacements if force else additions
            target[(group, number)] = encoded(image, axis)
            frames_report.append({"key": [group, number], "size": list(image.size),
                                  "bbox": list(box), "axis": list(axis)})
    sff = Sff(SFF_PATH); pending = SFF_PATH.with_suffix(".summon-super-v54.pending")
    pending.write_bytes(sff.derive(replacements, additions)); pending.replace(SFF_PATH)

    definitions = {
        870100: action(870100, 61020, [0, 1, 2], [14, 20, 32]),
        870101: action(870101, 61020, [0, 1, 2], [14, 20, 32]),
        870102: action(870102, 61020, [0, 3, 2], [14, 20, 32]),
        870103: action(870103, 61020, [0, 3, 2], [14, 20, 32]),
        1500: action(1500, 61020, [0, 4, 2, 4, 2], [5, 10, 5, 10, 30]),
        2200: action(2200, 61020, [0, 5, 2], [5, 20, 40]),
        2201: action(2201, 61020, [0, 5, 2], [5, 20, 40]),
        3000: action(3000, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        3010: action(3010, 61021, [3, 4, 5, 5], [10, 10, 10, 10]),
        3100: action(3100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        13100: action(13100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        23100: action(23100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        503100: action(503100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        513100: action(513100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        523100: action(523100, 61021, [0, 1, 2, 2], [25, 10, 10, 105]),
        3120: action(3120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                     [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        13120: action(13120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                      [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        23120: action(23120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                      [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        503120: action(503120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                       [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        513120: action(513120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                       [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        523120: action(523120, 61021, [3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
                       [10, 5, 30, 50, 30, 5, 67, 8, 35, 5]),
        # Antares Gambit is another playable super chain. Preserve its element
        # counts while moving every player-body row to the approved v48 dagger bank.
        3200: action(3200, 61016, [8, 9, 10, 11, 7, 8, 9],
                     [7, 5, 98, 20, 5, 5, 5], 0.156339262, 0.147489865),
        3210: action(3210, 61016, [8, 9, 10, 11, 7, 8, 9, 10, 11, 10, 9],
                     [30, 25, 9, 9, 9, 20, 10, 10, 140, 10, 10], 0.156339262, 0.147489865),
        3220: action(3220, 61016, [10, 11], [50, 190], 0.156339262, 0.147489865),
    }
    appendable = {23100, 523100, 23120, 523120}
    changed_actions, missing = [], []
    for number, definition in definitions.items():
        text, found = replace_action(text, number, definition)
        if not found and number in appendable:
            text = text.rstrip()+"\n\n"+definition+"\n"; found = True
        (changed_actions if found else missing).append(number)
    if missing:
        raise RuntimeError(f"missing required actions: {missing}")
    AIR.write_text(text.rstrip()+"\n\n"+MARKER+"\n", encoding="latin1", newline="")

    report = {"status": "INSTALLED", "locked_scale": [SX, SY],
              "groups": {"summon_calls": 61020, "ultimates": 61021},
              "actions_rewritten": changed_actions, "frames": frames_report}
    REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
