"""Install v48-derived Antares and longsword banks into every weapon action."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/weapons-v52"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
BACKUP = ART / "live-before-weapons-v52"
REPORT = ART / "installation.json"
MARKER = "; JINWOO V48 WEAPON BANKS V52"
TARGET_HEIGHT = 43.657
X_RATIO = 0.095218974 / 0.089829218

BANKS = {
    "dagger": {"file": "antares-v48-bank-v52-padded.png", "group": 61016, "offset": 700000},
    "sword": {"file": "longsword-v48-bank-v52-padded.png", "group": 61017, "offset": 500000},
}
MOVEMENT = (0, 5, 6, 10, 11, 12, 20, 21, 40, 41, 42, 43, 44, 45, 47, 50, 52, 100, 105)
NORMALS = (200, 210, 220, 260, 300, 310, 320, 350, 400, 410, 420, 460, 600, 610, 620, 630, 640, 650)


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def clean_cell(sheet: Image.Image, slot: int) -> Image.Image:
    column, row = slot % 4, slot // 4
    xs = [round(sheet.width * index / 4) for index in range(5)]
    ys = [round(sheet.height * index / 3) for index in range(4)]
    cell = sheet.crop((xs[column], ys[row], xs[column + 1], ys[row + 1])).convert("RGBA")
    alpha = np.asarray(cell.getchannel("A"))
    mask = (alpha >= 96).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    # Generated atlas cells can contain sizeable pieces of their neighbours
    # (duplicate shoes, hands and blade tips). The complete fighter and held
    # weapon form one connected silhouette; keep only that dominant component.
    if count <= 1:
        raise RuntimeError(f"empty weapon cell {slot}")
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    keep = labels == largest
    clean_alpha = np.where(keep, alpha, 0).astype(np.uint8)
    cell.putalpha(Image.fromarray(clean_alpha, mode="L"))
    box = cell.getchannel("A").getbbox()
    if not box:
        raise RuntimeError(f"empty weapon cell {slot}")
    crop = cell.crop(box)
    canvas = Image.new("RGBA", (crop.width + 24, crop.height + 24), (0, 0, 0, 0))
    canvas.alpha_composite(crop, (12, 12))
    return canvas


def split_actions(text: str) -> tuple[str, dict[int, list[str]], list[int]]:
    blocks: dict[int, list[str]] = {}; order = []
    # Never use \s* here: it can consume the preceding newline, making the
    # first list item blank and preventing cloned action headers from being
    # renumbered.
    matches = list(re.finditer(r"(?im)^[ \t]*\[Begin Action\s+(-?\d+)\].*$", text))
    preamble = text[:matches[0].start()].rstrip() if matches else text
    for index, match in enumerate(matches):
        action = int(match.group(1)); end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks[action] = text[match.start():end].rstrip().splitlines(); order.append(action)
    return preamble, blocks, order


def pose_sequence(base: int) -> list[int]:
    if base == 500: return [6]
    if base == 501: return [7]
    if base in (0, 5, 6): return [0]
    if base in (10, 11, 12): return [5]
    if base == 20: return [1, 2]
    if base == 21: return [2, 1]
    if base in (40, 41, 42, 43, 44, 45, 47, 50, 52): return [4]
    if base == 100: return [3]
    if base == 105: return [7]
    if base in (260, 400, 410, 420, 460): return [5, 10, 11, 7]
    if base in (600, 610, 620, 630, 640, 650): return [4, 9, 11, 4]
    return [7, 8, 9, 10, 11, 7]


def rewrite_block(lines: list[str], action: int, group: int, poses: list[int], sx: float, sy: float) -> list[str]:
    result = []; row = 0
    for raw in lines:
        if re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", raw):
            fields = raw.split(",")
            try:
                int(fields[0].strip()); int(fields[1].strip())
            except (ValueError, IndexError):
                result.append(raw); continue
            pose = poses[row % len(poses)]
            while len(fields) < 9: fields.append("")
            fields[0], fields[1] = str(group), str(pose)
            fields[7], fields[8] = f"{sx:.9f}", f"{sy:.9f}"
            raw = ",".join(fields); row += 1
        result.append(raw)
    result[0] = re.sub(r"(?i)(\[Begin Action\s+)-?\d+", rf"\g<1>{action}", result[0])
    return result


def main() -> None:
    text = AIR.read_text(encoding="latin1")
    if MARKER in text:
        print(REPORT.read_text(encoding="utf-8")); return
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name); shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)

    additions = {}; scales = {}; frame_report = []
    for name, config in BANKS.items():
        sheet = Image.open(ART / config["file"]).convert("RGBA")
        images = [clean_cell(sheet, slot) for slot in range(12)]
        reference = images[1].getchannel("A").getbbox()
        sy = TARGET_HEIGHT / (reference[3] - reference[1]); sx = sy * X_RATIO
        scales[name] = [sx, sy]
        foot_pixels = round(1.62 / sy)
        for slot, image in enumerate(images):
            box = image.getchannel("A").getbbox(); axis = (image.width // 2, box[3] - foot_pixels)
            image.save(ART / f"{config['group']}-{slot}.png", optimize=True)
            additions[(config["group"], slot)] = encoded(image, axis)
            frame_report.append({"bank": name, "key": [config["group"], slot], "size": list(image.size),
                                 "bbox": list(box), "axis": list(axis)})

    sff = Sff(SFF_PATH); pending = SFF_PATH.with_suffix(".weapons-v52.pending")
    pending.write_bytes(sff.derive({}, additions)); pending.replace(SFF_PATH)

    preamble, blocks, order = split_actions(text)
    changed_actions = []
    for name, config in BANKS.items():
        group, offset = config["group"], config["offset"]
        sx, sy = scales[name]
        for base in MOVEMENT + NORMALS + (500, 501):
            target = offset + base
            if target in blocks:
                source = blocks[target]
            elif base in blocks:
                source = blocks[base]
                blocks[target] = source.copy(); order.append(target)
            else:
                continue
            blocks[target] = rewrite_block(source, target, group, pose_sequence(base), sx, sy)
            changed_actions.append(target)

    # Weapon-specific custom actions and the sword-specific charge/recovery.
    for action, name, poses in ((876300, "dagger", [8, 9, 10, 11, 7]),
                                (876310, "sword", [8, 9, 10, 11, 7]),
                                (20500, "sword", [6]), (20501, "sword", [7])):
        if action in blocks:
            group = BANKS[name]["group"]; sx, sy = scales[name]
            blocks[action] = rewrite_block(blocks[action], action, group, poses, sx, sy)
            changed_actions.append(action)

    rebuilt = preamble + "\n\n" + "\n\n".join("\n".join(blocks[action]) for action in order)
    AIR.write_text(rebuilt.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")
    report = {"status": "INSTALLED", "banks": BANKS, "scales": scales,
              "frames_added": len(additions), "actions_rewritten": sorted(set(changed_actions)),
              "frames": frame_report}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "INSTALLED", "frames_added": len(additions),
                      "actions_rewritten": len(set(changed_actions)), "scales": scales}, indent=2))


if __name__ == "__main__":
    main()
