"""Replace base Jinwoo with one single-sheet identity and prune v48 drawings."""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import struct
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-master-v49"
SOURCE = ART / "jinwoo-master-sheet-v49-neck-hair-fixed.png"
NORMALIZED = ART / "normalized"
BACKUP = ART / "live-before-v49"
AIR, SFF_PATH, CNS = LIVE / "anim.air", LIVE / "spr.sff", LIVE / "cns.cns"
REPORT = ART / "installation.json"
MARKER = "; JINWOO SINGLE MASTER V49"
GROUP = 61014
OLD_GROUP = 61013
REJECTED_ART = True
NARUTO_EFFECTIVE_HEIGHT = 226 * 0.18
TARGET_RATIO = 1.18
TARGET_HEIGHT = NARUTO_EFFECTIVE_HEIGHT * TARGET_RATIO

# v48 frame -> v49 pose. Every live base row is routed to the same source sheet.
FRAME_MAP = {
    24: 0,
    0: 1, 1: 2, 2: 3, 3: 2, 4: 1, 5: 0,
    6: 4, 7: 5, 8: 4, 9: 5, 10: 4, 11: 5,
    # Cell 7 reaches the sheet edge, so the crouch transition reuses the
    # complete coiled crouch in cell 6 instead of installing a clipped hand.
    12: 6, 13: 5, 14: 5, 15: 5, 16: 6, 17: 6,
    18: 0, 19: 8, 20: 9, 21: 10, 22: 9, 23: 0,
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def clean_cell(sheet: Image.Image, column: int, row: int) -> Image.Image:
    # Image edits may preserve the logical 4x3 sheet while changing its pixel
    # dimensions. Derive the cell boundaries from the actual canvas so the
    # artwork is cropped, never stretched.
    xs = [round(sheet.width * index / 4) for index in range(5)]
    ys = [round(sheet.height * index / 3) for index in range(4)]
    cell = sheet.crop((xs[column], ys[row], xs[column + 1], ys[row + 1])).convert("RGBA")
    alpha = cell.getchannel("A").point(lambda value: 0 if value < 128 else value)
    mask = np.asarray(alpha) > 0
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if count > 1:
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = Image.fromarray(np.where(labels == largest, np.asarray(alpha), 0).astype(np.uint8), mode="L")
    cell.putalpha(alpha)
    box = alpha.getbbox()
    if not box:
        raise RuntimeError(f"empty master cell {column},{row}")
    cell = cell.crop(box)
    canvas = Image.new("RGBA", (cell.width + 24, cell.height + 24), (0, 0, 0, 0))
    canvas.alpha_composite(cell, (12, 12))
    return canvas


def prepare() -> tuple[dict, float, list[dict]]:
    sheet = Image.open(SOURCE).convert("RGBA")
    if sheet.width < 1200 or sheet.height < 900:
        raise RuntimeError(f"master sheet is too small {sheet.size}")
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    images = {slot: clean_cell(sheet, slot % 4, slot // 4) for slot in range(11)}
    idle_box = images[0].getchannel("A").getbbox()
    idle_height = idle_box[3] - idle_box[1]
    scale = TARGET_HEIGHT / idle_height
    foot_pixels = round(1.62 / scale)
    additions, details = {}, []
    for number, image in images.items():
        box = image.getchannel("A").getbbox()
        axis = (image.width // 2, box[3] - foot_pixels)
        image.save(NORMALIZED / f"61014-{number}.png", optimize=True)
        additions[(GROUP, number)] = encoded(image, axis)
        details.append({"key": [GROUP, number], "size": list(image.size), "bbox": list(box), "axis": list(axis)})
    return additions, scale, details


def rewrite_air(text: str, scale: float) -> tuple[str, int]:
    output, changed = [], 0
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                group, number = int(parts[0].strip()), int(parts[1].strip())
            except ValueError:
                group = number = -1
            if group == OLD_GROUP and number in FRAME_MAP:
                parts[0], parts[1] = str(GROUP), str(FRAME_MAP[number])
                while len(parts) < 9:
                    parts.append("")
                parts[7] = parts[8] = f"{scale:.9f}"
                line = ",".join(parts); changed += 1
        output.append(line)
    return "\n".join(output).rstrip() + "\n\n" + MARKER + "\n", changed


def materialize_link_dependents(path: Path, remove_keys: set[tuple[int, int]]) -> None:
    sff = Sff(path); remove_indices = {sff.keys[key] for key in remove_keys if key in sff.keys}; replacements = {}
    for index, header in enumerate(sff.headers):
        key = header[:2]
        if index in remove_indices or header[10] != 0:
            continue
        target, seen = header[6], set()
        while sff.headers[target][10] == 0 and target not in seen:
            seen.add(target); target = sff.headers[target][6]
        if target in remove_indices:
            replacements[key] = encoded(sff.decode(index).convert("RGBA"), tuple(header[4:6]))
    if replacements:
        pending = path.with_suffix(".v49-materialized.pending")
        pending.write_bytes(sff.derive(replacements, {})); pending.replace(path)


def prune_keys(path: Path, remove_keys: set[tuple[int, int]]) -> int:
    sff = Sff(path); remove = {index for key, index in sff.keys.items() if key in remove_keys}
    keep = [index for index in range(sff.count) if index not in remove]
    remap = {old: new for new, old in enumerate(keep)}; headers = []
    for old in keep:
        values = list(sff.headers[old])
        if values[10] == 0:
            if values[6] not in remap:
                raise RuntimeError(f"retained linked sprite targets removed index {values[6]}")
            values[6] = remap[values[6]]
        headers.append(struct.pack("<HHHHhhHBBIIHH", *values))
    old_end = sff.offset + sff.count * 28
    data = bytearray(sff.data[:sff.offset] + b"".join(headers) + sff.data[old_end:])
    new_lo = sff.lo - len(remove) * 28
    struct.pack_into("<I", data, 40, len(keep)); struct.pack_into("<IIII", data, 52, new_lo, sff.ls, len(data), 0)
    pending = path.with_suffix(".v49-pruned.pending"); pending.write_bytes(data); pending.replace(path)
    return len(remove)


def main() -> None:
    if REJECTED_ART:
        raise RuntimeError(
            "v49 art was rejected for Jinwoo identity drift; do not install it"
        )
    air_text = AIR.read_text(encoding="latin1")
    if MARKER in air_text:
        print(REPORT.read_text(encoding="utf-8")); return
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (AIR, SFF_PATH, CNS): shutil.copy2(path, BACKUP / path.name)
    additions, scale, details = prepare()
    source = Sff(SFF_PATH); pending = SFF_PATH.with_suffix(".v49.pending")
    pending.write_bytes(source.derive({}, additions)); pending.replace(SFF_PATH)
    air_text, changed = rewrite_air(air_text, scale)
    if changed < 200: raise RuntimeError(f"only {changed} v48 rows rerouted")
    AIR.write_text(air_text, encoding="latin1", newline="")
    cns = CNS.read_text(encoding="latin1")
    cns = re.sub(r"(?im)^\s*xscale\s*=.*$", "xscale=1.10", cns, count=1)
    cns = re.sub(r"(?im)^\s*yscale\s*=.*$", "yscale=1.0", cns, count=1)
    CNS.write_text(cns, encoding="latin1", newline="")
    remove_keys = {(OLD_GROUP, number) for number in range(25)}
    materialize_link_dependents(SFF_PATH, remove_keys)
    removed = prune_keys(SFF_PATH, remove_keys)
    proof = Sff(SFF_PATH)
    surviving = sorted(key for key in remove_keys if key in proof.keys)
    if surviving: raise RuntimeError(f"v48 keys survived: {surviving}")
    report = {"status": "INSTALLED", "revision": "unified-master-v49", "group": GROUP,
              "source_sheet": str(SOURCE.relative_to(ROOT)), "frames_added": len(additions),
              "air_rows_rerouted": changed, "obsolete_v48_sprites_deleted": removed,
              "target_height_ratio": TARGET_RATIO, "locked_air_scale": scale,
              "character_scale": [1.10, 1.0], "frames": details,
              "runtime_sha256": {"anim.air": sha(AIR), "spr.sff": sha(SFF_PATH), "cns.cns": sha(CNS)},
              "backup": str(BACKUP.relative_to(ROOT))}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__": main()
