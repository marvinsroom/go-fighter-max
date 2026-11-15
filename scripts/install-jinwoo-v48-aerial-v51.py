"""Install the missing v48 bare-hand aerial attack family."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/aerial-v51"
SOURCE = ART / "bare-aerial-sheet-v51.png"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
BACKUP = ART / "live-before-aerial-v51"
REPORT = ART / "installation.json"
GROUP = 61015
SX, SY = 0.095218974, 0.089829218
MARKER = "; JINWOO V48 AERIAL V51"

ACTION_POSES = {
    600: [0, 1, 0], 610: [2, 3, 2], 620: [4, 5, 4],
    630: [0, 1, 0], 640: [2, 3, 2], 650: [4, 5, 4],
    875600: [0, 1, 0], 875610: [2, 3, 2], 875620: [4, 5, 4],
    876290: [4, 5, 3, 5, 4],
}


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def clean_cell(sheet: Image.Image, slot: int) -> Image.Image:
    column, row = slot % 3, slot // 3
    xs = [round(sheet.width * index / 3) for index in range(4)]
    ys = [round(sheet.height * index / 2) for index in range(3)]
    cell = sheet.crop((xs[column], ys[row], xs[column + 1], ys[row + 1])).convert("RGBA")
    alpha = np.asarray(cell.getchannel("A"))
    mask = (alpha >= 128).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if count <= 1:
        raise RuntimeError(f"empty aerial cell {slot}")
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    clean_alpha = np.where(labels == largest, alpha, 0).astype(np.uint8)
    cell.putalpha(Image.fromarray(clean_alpha, mode="L"))
    box = cell.getchannel("A").getbbox()
    if not box:
        raise RuntimeError(f"empty aerial cell {slot}")
    crop = cell.crop(box)
    canvas = Image.new("RGBA", (crop.width + 24, crop.height + 24), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (12, 12))
    return canvas


def rewrite_air(text: str) -> tuple[str, int]:
    current = None; row = 0; changed = 0; output = []
    for raw in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if match:
            current = int(match.group(1)); row = 0
        if current in ACTION_POSES and re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", raw):
            fields = raw.split(",")
            try:
                int(fields[0].strip()); int(fields[1].strip())
            except (ValueError, IndexError):
                output.append(raw); continue
            poses = ACTION_POSES[current]
            pose = poses[min(row, len(poses) - 1)]
            while len(fields) < 9:
                fields.append("")
            fields[0], fields[1] = str(GROUP), str(pose)
            fields[7], fields[8] = f"{SX:.9f}", f"{SY:.9f}"
            raw = ",".join(fields); row += 1; changed += 1
        output.append(raw)
    return "\n".join(output).rstrip() + "\n\n" + MARKER + "\n", changed


def main() -> None:
    text = AIR.read_text(encoding="latin1")
    if MARKER in text:
        print(REPORT.read_text(encoding="utf-8")); return
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name); shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)
    sheet = Image.open(SOURCE).convert("RGBA")
    additions = {}
    frames = []
    for slot in range(6):
        image = clean_cell(sheet, slot)
        box = image.getchannel("A").getbbox()
        axis = (image.width // 2, box[3] - 18)
        image.save(ART / f"{GROUP}-{slot}.png", optimize=True)
        additions[(GROUP, slot)] = encoded(image, axis)
        frames.append({"key": [GROUP, slot], "size": list(image.size), "bbox": list(box), "axis": list(axis)})
    sff = Sff(SFF_PATH); pending = SFF_PATH.with_suffix(".aerial-v51.pending")
    pending.write_bytes(sff.derive({}, additions)); pending.replace(SFF_PATH)
    rewritten, changed = rewrite_air(text)
    if changed < 38:
        raise RuntimeError(f"too few aerial rows rerouted: {changed}")
    AIR.write_text(rewritten, encoding="latin1", newline="")
    report = {"status": "INSTALLED", "group": GROUP, "rows_rerouted": changed,
              "actions": sorted(ACTION_POSES), "locked_scale": [SX, SY], "frames": frames}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
