"""Install Jinwoo-style jump choreography and distinct weapon timelines.

This pass keeps the approved v48 identity and v68 anatomy scales.  It changes
only animation choreography, replaces the six bare jump drawings with the
reference-preserving shadow-step strip, and removes the last live legacy human
banks (61005/61011) from weapon switches, grabs, guards, and dormant actions.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import cv2
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/motion-style-v69"
AIR = LIVE / "anim.air"
SFF_PATH = LIVE / "spr.sff"
JUMP_SHEET = ART / "jump-shadow-step-v69.png"

BASE_SCALE = (0.101895680, 0.096128000)
DAGGER_SCALE = (0.167301691, 0.157831784)
SWORD_SCALE = (0.208072691, 0.196294992)
JUMP_SCALES = {
    0: (0.106331357, 0.100312599),
    1: (0.117724003, 0.111060377),
    2: (0.111910472, 0.105575914),
    3: (0.103893962, 0.098013170),
    4: (0.100162964, 0.094493360),
    5: (0.106020447, 0.100019287),
}
JUMP_BASES = {40, 41, 42, 43, 44, 45, 47, 50, 52}
TARGET_HUMAN_DIMENSION = 50.4
CHAR_X, CHAR_Y = 1.39, 1.07
JUMP_BASE_SCALE = (0.094372063, 0.089030246)


def encode(image: Image.Image, axis: tuple[int, int]) -> dict[str, object]:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {
        "image": image,
        "png": payload.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
    }


def nonpurple_body_mask(image: Image.Image) -> np.ndarray:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint16)
    r, g, b, a = (rgba[:, :, index] for index in range(4))
    purple = (b > g * 1.22 + 12) & (r > g * 1.12 + 8) & (b > 55)
    return (a >= 32) & ~purple


def bounds(mask: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.where(mask)
    if not len(xs):
        raise RuntimeError("empty sprite mask")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def split_jump_sheet(path: Path) -> tuple[list[Image.Image], list[tuple[int, int]], list[dict[str, object]]]:
    sheet = Image.open(path).convert("RGBA")
    if sheet.width % 6:
        raise RuntimeError(f"jump strip is not six equal cells: {sheet.size}")
    width = sheet.width // 6
    frames: list[Image.Image] = []
    axes: list[tuple[int, int]] = []
    metrics: list[dict[str, object]] = []
    for number in range(6):
        cell = sheet.crop((number * width, 0, (number + 1) * width, sheet.height))
        alpha_array = np.asarray(cell.getchannel("A"), dtype=np.uint8)
        alpha_mask = alpha_array >= 24
        component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
            alpha_mask.astype(np.uint8), 8
        )
        if component_count <= 1:
            raise RuntimeError(f"empty generated jump cell {number}")
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha_array = np.where(labels == largest, alpha_array, 0).astype(np.uint8)
        cell.putalpha(Image.fromarray(alpha_array, mode="L"))
        alpha_mask = alpha_array >= 24
        alpha_box = bounds(alpha_mask)
        body_mask = nonpurple_body_mask(cell)
        body_box = bounds(body_mask)
        body_width = body_box[2] - body_box[0]
        body_height = body_box[3] - body_box[1]
        factor = TARGET_HUMAN_DIMENSION / max(
            body_width * JUMP_BASE_SCALE[0] * CHAR_X,
            body_height * JUMP_BASE_SCALE[1] * CHAR_Y,
        )
        JUMP_SCALES[number] = (
            JUMP_BASE_SCALE[0] * factor,
            JUMP_BASE_SCALE[1] * factor,
        )
        drawing = cell.crop(alpha_box)
        canvas = Image.new("RGBA", (drawing.width + 32, drawing.height + 32), (0, 0, 0, 0))
        canvas.alpha_composite(drawing, (16, 16))
        # Root from the non-effect anatomy, never from a trailing shadow wisp.
        axis_x = round((body_box[0] + body_box[2]) / 2 - alpha_box[0]) + 16
        axis_y = body_box[3] - alpha_box[1] + 14
        frames.append(canvas)
        axes.append((axis_x, axis_y))
        metrics.append({
            "frame": number,
            "source_alpha_bbox": list(alpha_box),
            "source_body_bbox": list(body_box),
            "size": list(canvas.size),
            "axis": [axis_x, axis_y],
            "scale": [round(value, 9) for value in JUMP_SCALES[number]],
            "body_world_longest_dimension": TARGET_HUMAN_DIMENSION,
        })
    return frames, axes, metrics


def block(text: str, action: int) -> re.Match[str]:
    found = re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)", text)
    if not found:
        raise RuntimeError(f"missing action {action}")
    return found


def replace_block(text: str, action: int, replacement: str) -> str:
    found = block(text, action)
    return text[:found.start()] + replacement.rstrip() + "\n\n" + text[found.end():]


def rows_in(source: str) -> list[tuple[int, list[str]]]:
    rows = []
    for index, raw in enumerate(source.splitlines()):
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) < 2:
            continue
        try:
            int(fields[0].strip()); int(fields[1].strip())
        except ValueError:
            continue
        rows.append((index, fields))
    return rows


def rewrite_action_rows(
    text: str,
    action: int,
    group: int,
    frames: list[int],
    scale: tuple[float, float],
) -> tuple[str, int]:
    found = block(text, action)
    lines = found.group(0).splitlines()
    candidates = []
    for index, raw in enumerate(lines):
        fields = raw.split(";", 1)[0].split(",")
        try:
            row_group = int(fields[0].strip())
            int(fields[1].strip())
        except (ValueError, IndexError):
            continue
        if row_group == group:
            candidates.append(index)
    if len(candidates) != len(frames):
        raise RuntimeError(f"action {action} expected {len(frames)} group {group} rows, found {len(candidates)}")
    for index, frame in zip(candidates, frames, strict=True):
        fields = lines[index].split(",")
        while len(fields) < 9:
            fields.append("")
        fields[1] = str(frame)
        fields[7], fields[8] = f"{scale[0]:.9f}", f"{scale[1]:.9f}"
        lines[index] = ",".join(fields)
    replacement = "\n".join(lines) + ("\n" if found.group(0).endswith("\n") else "")
    return text[:found.start()] + replacement + text[found.end():], len(candidates)


def resample(sequence: list[int], count: int) -> list[int]:
    if count <= 0:
        return []
    if count == 1:
        return [sequence[len(sequence) // 2]]
    return [sequence[round(index * (len(sequence) - 1) / (count - 1))] for index in range(count)]


def weapon_jump_sequence(base: int) -> list[int]:
    return {
        40: [5, 3],
        41: [3, 4, 4],
        42: [4],
        43: [4, 3],
        44: [4, 3],
        45: [4, 3],
        47: [3, 5],
        50: [3, 4, 4],
        52: [4, 3],
    }[base]


def motion_action(action: int, rows: list[tuple[int, int, int, int]]) -> str:
    lines = [f"[Begin Action {action}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
    for group, frame, duration, flip in rows:
        scale = BASE_SCALE if group == 61013 else DAGGER_SCALE if group == 61016 else SWORD_SCALE
        lines.append(f"{group},{frame},{flip},0,{duration},,,{scale[0]:.9f},{scale[1]:.9f}")
    return "\n".join(lines)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "live-before-v69"
    if not backup.exists():
        backup.mkdir()
        shutil.copy2(AIR, backup / AIR.name)
        shutil.copy2(SFF_PATH, backup / SFF_PATH.name)

    frames, axes, frame_metrics = split_jump_sheet(JUMP_SHEET)
    normalized = ART / "normalized"
    normalized.mkdir(exist_ok=True)
    additions = {}
    for number, (image, axis) in enumerate(zip(frames, axes, strict=True)):
        image.save(normalized / f"61023-{number}.png", optimize=True)
        additions[(61023, number)] = encode(image, axis)
    sff = Sff(SFF_PATH)
    replacements = {key: value for key, value in additions.items() if key in sff.keys}
    pending_sff = SFF_PATH.with_suffix(".v69.pending")
    pending_sff.write_bytes(sff.derive(replacements, {}))
    pending_sff.replace(SFF_PATH)

    text = AIR.read_text(encoding="latin1")
    changed: Counter[str] = Counter()

    # Faster, controlled bare jump: explode upward, compact apex, clean landing.
    jump_templates = {
        40: [(0, 2), (1, 2)],
        41: [(1, 2), (2, 2), (3, 3)],
        42: [(2, 2), (3, 3)],
        43: [(3, 2), (4, 3)],
        44: [(3, 2), (4, 3)],
        45: [(3, 2), (4, 3)],
        47: [(4, 2), (5, 4)],
        50: [(1, 2), (2, 2), (3, 3)],
        52: [(3, 2), (4, 3)],
    }
    for action, sequence in jump_templates.items():
        lines = [f"[Begin Action {action}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
        for frame, duration in sequence:
            sx, sy = JUMP_SCALES[frame]
            lines.append(f"61023,{frame},0,0,{duration},,,{sx:.9f},{sy:.9f}")
        text = replace_block(text, action, "\n".join(lines))
        changed["bare_jump_actions"] += 1

    # Every weapon jump gets the same fast phase timing as the bare jump.
    # Rebuilding these movement-only blocks removes the old eight-frame holds
    # that made daggers float and the one-frame sword jumps that looked frozen.
    action_headers = [int(value) for value in re.findall(r"(?im)^\[Begin Action\s+(-?\d+)\]", text)]
    for action in action_headers:
        base = action % 10000
        if base not in JUMP_BASES:
            continue
        found = block(text, action)
        groups = []
        for _, fields in rows_in(found.group(0)):
            groups.append(int(fields[0].strip()))
        family = 61016 if 61016 in groups else 61017 if 61017 in groups else None
        if family is None:
            continue
        sequence = weapon_jump_sequence(base)
        durations = {
            40: [2, 2], 41: [2, 3, 3], 42: [3],
            43: [2, 3], 44: [2, 3], 45: [2, 3],
            47: [2, 4], 50: [2, 3, 3], 52: [2, 3],
        }[base]
        scale = DAGGER_SCALE if family == 61016 else SWORD_SCALE
        lines = [f"[Begin Action {action}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
        for frame, duration in zip(sequence, durations, strict=True):
            lines.append(f"{family},{frame},0,0,{duration},,,{scale[0]:.9f},{scale[1]:.9f}")
        text = replace_block(text, action, "\n".join(lines))
        changed[f"weapon_jump_actions:{family}"] += 1

    # Give each normal a distinct silhouette instead of recycling one combo.
    normal_sequences = {
        (61013, 200): [18, 18, 19, 23, 23],
        (61013, 210): [18, 20, 20, 21, 23],
        (61013, 220): [18, 20, 21, 20, 23],
        (61016, 700200): [0, 7, 8, 9, 0],
        (61016, 700210): [0, 8, 9, 11, 0],
        (61016, 700220): [0, 10, 11, 9, 0],
        (61016, 700300): [0, 7, 8, 9, 0],
        (61016, 700310): [0, 8, 9, 11, 0],
        (61016, 700320): [0, 10, 11, 9, 0],
        (61016, 700350): [0, 6, 9, 11, 0],
        (61017, 500200): [0, 7, 9, 11, 6],
        (61017, 500210): [0, 8, 10, 11, 6],
        (61017, 500220): [0, 7, 8, 10, 6],
        (61017, 500300): [0, 7, 8, 9, 6],
        (61017, 500310): [0, 8, 10, 11, 6],
        (61017, 500320): [0, 7, 9, 10, 6],
        (61017, 500350): [0, 8, 9, 11, 6],
    }
    for (group, action), sequence in normal_sequences.items():
        scale = BASE_SCALE if group == 61013 else DAGGER_SCALE if group == 61016 else SWORD_SCALE
        text, count = rewrite_action_rows(text, action, group, sequence, scale)
        changed[f"distinct_normal_rows:{group}"] += count

    # Air normals read as deliberate forward cuts instead of one held pose.
    aerial_sequences = {
        600: [3, 4, 7, 9], 610: [4, 8, 9, 11],
        620: [3, 4, 9, 10, 11], 630: [4, 9, 11],
        640: [4, 7, 10, 11], 650: [4, 9],
    }
    for family, scale in ((61016, DAGGER_SCALE), (61017, SWORD_SCALE)):
        headers = [int(value) for value in re.findall(r"(?im)^\[Begin Action\s+(-?\d+)\]", text)]
        for action in headers:
            base = action % 10000
            if base not in aerial_sequences:
                continue
            found = block(text, action)
            count = sum(1 for _, fields in rows_in(found.group(0)) if int(fields[0].strip()) == family)
            if not count:
                continue
            sequence = resample(aerial_sequences[base], count)
            text, row_count = rewrite_action_rows(text, action, family, sequence, scale)
            changed[f"weapon_aerial_rows:{family}"] += row_count

    # Weapon changes now use only current v48 body/weapon banks and hand off at tick 20.
    text = replace_block(text, 876322, motion_action(876322, [
        (61013, 24, 4, 0), (61013, 18, 4, 0), (61013, 19, 4, 0),
        (61013, 20, 4, 0), (61013, 23, 4, 0),
        (61016, 6, 4, 0), (61016, 7, 4, 0), (61016, 0, 10, 0),
    ]))
    text = replace_block(text, 876323, motion_action(876323, [
        (61016, 0, 4, 0), (61016, 6, 4, 0), (61016, 9, 4, 0),
        (61016, 11, 4, 0), (61016, 0, 4, 0),
        (61017, 7, 3, 0), (61017, 8, 3, 0), (61017, 9, 3, 0),
        (61017, 10, 3, 0), (61017, 11, 3, 0), (61017, 0, 3, 0),
    ]))
    text = replace_block(text, 876324, motion_action(876324, [
        (61017, 0, 4, 0), (61017, 11, 4, 0), (61017, 9, 4, 0),
        (61017, 7, 4, 0), (61017, 6, 4, 0),
        (61013, 18, 4, 0), (61013, 20, 4, 0), (61013, 23, 6, 0),
        (61013, 24, 4, 0),
    ]))
    changed["weapon_switch_actions"] = 3

    # Replace the live legacy grab body with current v48 bare-hand poses.
    text = replace_block(text, 879920, motion_action(879920, [
        (61013, 18, 4, 0), (61013, 19, 6, 0), (61013, 21, 8, 0),
    ]).replace("Clsn2[0] = -12,-59,12,0", "Clsn2[0] = -14,-57,14,0\nClsn1: 1\nClsn1[0] = 0,-55,55,-4"))
    text = replace_block(text, 879921, motion_action(879921, [
        (61013, 19, 6, 0), (61013, 20, 8, 0), (61013, 21, 10, 0), (61013, 23, 12, 0),
    ]))
    changed["grab_actions"] = 2

    # Convert every remaining archived human row while preserving collisions/timing.
    legacy_map = {
        0: 24, 1: 18, 4: 18, 5: 19, 6: 21, 7: 18, 8: 19, 9: 20, 10: 21,
        12: 12, 13: 13, 14: 14, 15: 15, 24: 18, 25: 19, 26: 20, 27: 21,
        28: 23, 29: 20, 30: 19, 31: 18, 48: 23, 60: 18, 61: 19, 62: 20,
        63: 23, 83: 24,
    }
    output = []
    legacy_rows = 0
    for raw in text.splitlines():
        fields = raw.split(",")
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except (ValueError, IndexError):
            output.append(raw)
            continue
        if group == 61011:
            while len(fields) < 9:
                fields.append("")
            fields[0], fields[1] = "61013", str(legacy_map.get(frame, 24))
            fields[7], fields[8] = f"{BASE_SCALE[0]:.9f}", f"{BASE_SCALE[1]:.9f}"
            raw = ",".join(fields)
            legacy_rows += 1
        output.append(raw)
    text = "\n".join(output).rstrip() + "\n"
    changed["legacy_61011_rows"] = legacy_rows

    pending_air = ART / "anim.v69.pending.air"
    pending_air.write_text(text, encoding="latin1", newline="")
    pending_air.replace(AIR)

    report = {
        "status": "INSTALLED",
        "identity_reference": "unified v48",
        "jump_sheet": str(JUMP_SHEET.relative_to(ROOT)),
        "jump_frames": frame_metrics,
        "changed": dict(sorted(changed.items())),
        "weapon_switch_handoff_tick": 20,
        "legacy_human_group_removed": 61011,
    }
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
