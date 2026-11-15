"""Install one locked Jinwoo base model and physically prune replaced live sprites."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48"
NORMALIZED = ART / "normalized"
BACKUP = ART / "live-before-v48"
AIR = LIVE / "anim.air"
SFF_PATH = LIVE / "spr.sff"
REPORT = ART / "installation.json"
MARKER = "; JINWOO UNIFIED BASE V48"
GROUP = 61013
TARGET_WORLD_HEIGHT = 43.657
X_RATIO = 0.032913216 / 0.031050203

SHEETS = {
    "walk": ("walk-sheet-v48.png", 0),
    "run": ("run-sheet-v48.png", 6),
    "jump": ("jump-sheet-v48.png", 12),
    "punch": ("punch-sheet-v48.png", 18),
}

# Every mapped key is removed from the final SFF after all AIR references move.
OLD_TO_NEW = {
    **{(300, n): (GROUP, 24) for n in range(101, 106)},
    **{(300, n): (GROUP, n - 108) for n in range(108, 114)},
    (300, 2): (GROUP, 6), (300, 89): (GROUP, 7),
    (300, 90): (GROUP, 8), (300, 91): (GROUP, 9),
    (300, 124): (GROUP, 10), (300, 125): (GROUP, 11),
    (300, 119): (GROUP, 12), (300, 120): (GROUP, 13),
    (300, 118): (GROUP, 14), (300, 115): (GROUP, 15),
    (300, 116): (GROUP, 16), (300, 117): (GROUP, 17),
    (300, 128): (GROUP, 16), (300, 127): (GROUP, 17),
    (300, 121): (GROUP, 12), (300, 129): (GROUP, 16),
    (300, 130): (GROUP, 17), (300, 131): (GROUP, 24),
    (61012, 0): (GROUP, 18), (61012, 1): (GROUP, 19),
    (61012, 2): (GROUP, 20), (61012, 3): (GROUP, 23),
    (61012, 4): (GROUP, 18), (61012, 5): (GROUP, 20),
    (61012, 6): (GROUP, 21), (61012, 7): (GROUP, 23),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_cell(sheet: Image.Image, column: int, row: int) -> Image.Image:
    cell = sheet.crop((column * 512, row * 512, (column + 1) * 512, (row + 1) * 512)).convert("RGBA")
    alpha = cell.getchannel("A")
    alpha = alpha.point(lambda value: 0 if value < 128 else value)
    mask = np.asarray(alpha) > 0
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    if component_count > 1:
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        cleaned = np.where(labels == largest, np.asarray(alpha), 0).astype(np.uint8)
        alpha = Image.fromarray(cleaned, mode="L")
    cell.putalpha(alpha)
    box = alpha.getbbox()
    if not box:
        raise RuntimeError(f"empty generated cell {column},{row}")
    cell = cell.crop(box)
    canvas = Image.new("RGBA", (cell.width + 24, cell.height + 24), (0, 0, 0, 0))
    canvas.alpha_composite(cell, (12, 12))
    return canvas


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {
        "image": image,
        "png": payload.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
    }


def prepare_frames() -> tuple[dict, float, list[dict]]:
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    images: dict[int, Image.Image] = {}
    for _, (filename, start) in SHEETS.items():
        sheet = Image.open(ART / filename).convert("RGBA")
        if sheet.size != (1536, 1024):
            raise RuntimeError(f"unexpected sheet size for {filename}: {sheet.size}")
        for slot in range(6):
            images[start + slot] = clean_cell(sheet, slot % 3, slot // 3)

    canonical = Image.open(
        ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/bare-hands-v47/source/canonical-idle-300-101.png"
    ).convert("RGBA")
    canonical_box = canonical.getchannel("A").getbbox()
    if not canonical_box:
        raise RuntimeError("empty canonical idle")
    canonical = canonical.crop(canonical_box)
    idle = Image.new("RGBA", (canonical.width + 24, canonical.height + 24), (0, 0, 0, 0))
    idle.alpha_composite(canonical, (12, 12))
    # The walk frames are upright and share one generated camera scale. One AIR
    # scale is deliberately applied to every frame so crouches/jumps cannot grow.
    walk_heights = [images[n].getchannel("A").getbbox()[3] - images[n].getchannel("A").getbbox()[1] for n in range(6)]
    reference_height = sorted(walk_heights)[len(walk_heights) // 2]
    idle_box = idle.getchannel("A").getbbox()
    idle_height = idle_box[3] - idle_box[1]
    resize_ratio = reference_height / idle_height
    idle = idle.resize(
        (round(idle.width * resize_ratio), round(idle.height * resize_ratio)),
        Image.Resampling.LANCZOS,
    )
    images[24] = idle
    sy = TARGET_WORLD_HEIGHT / reference_height
    sx = sy * X_RATIO

    additions = {}
    details = []
    for number, image in sorted(images.items()):
        box = image.getchannel("A").getbbox()
        # Naruto's visible shoes extend 1.62 local units below his root axis.
        # With the locked v48 y scale, 18 source pixels gives the same offset,
        # so both fighters visibly stand on the same stage line.
        axis = (image.width // 2, box[3] - 18)
        image.save(NORMALIZED / f"61013-{number}.png", optimize=True)
        additions[(GROUP, number)] = encoded(image, axis)
        details.append({"key": [GROUP, number], "size": list(image.size), "bbox": list(box), "axis": list(axis)})
    return additions, sx, sy, details


def rewrite_air(text: str, sx: float, sy: float) -> tuple[str, int]:
    changed = 0
    output = []
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                key = (int(parts[0].strip()), int(parts[1].strip()))
            except ValueError:
                key = None
            if key in OLD_TO_NEW:
                new_group, new_number = OLD_TO_NEW[key]
                parts[0], parts[1] = str(new_group), str(new_number)
                while len(parts) < 9:
                    parts.append("")
                parts[7], parts[8] = f"{sx:.9f}", f"{sy:.9f}"
                line = ",".join(parts)
                changed += 1
        output.append(line)
    return "\n".join(output).rstrip() + "\n\n" + MARKER + "\n", changed


def materialize_link_dependents(path: Path, remove_keys: set[tuple[int, int]]) -> None:
    sff = Sff(path)
    remove_indices = {sff.keys[key] for key in remove_keys if key in sff.keys}
    replacements = {}
    for index, header in enumerate(sff.headers):
        key = header[:2]
        if index in remove_indices or header[10] != 0:
            continue
        target = header[6]
        seen = set()
        while sff.headers[target][10] == 0 and target not in seen:
            seen.add(target)
            target = sff.headers[target][6]
        if target in remove_indices:
            image = sff.decode(index).convert("RGBA")
            replacements[key] = encoded(image, tuple(header[4:6]))
    if replacements:
        pending = path.with_suffix(".materialized.pending")
        pending.write_bytes(sff.derive(replacements, {}))
        pending.replace(path)


def prune_keys(path: Path, remove_keys: set[tuple[int, int]]) -> int:
    """Remove SFF v2 headers and reindex retained linked sprites."""
    sff = Sff(path)
    remove_indices = {index for key, index in sff.keys.items() if key in remove_keys}
    if not remove_indices:
        return 0
    keep_indices = [index for index in range(sff.count) if index not in remove_indices]
    old_to_new = {old: new for new, old in enumerate(keep_indices)}
    headers = []
    for old in keep_indices:
        values = list(sff.headers[old])
        if values[10] == 0:
            if values[6] not in old_to_new:
                raise RuntimeError(f"retained sprite {values[:2]} still links to removed index {values[6]}")
            values[6] = old_to_new[values[6]]
        headers.append(struct.pack("<HHHHhhHBBIIHH", *values))
    old_table_end = sff.offset + sff.count * 28
    data = bytearray(sff.data[:sff.offset] + b"".join(headers) + sff.data[old_table_end:])
    removed_bytes = len(remove_indices) * 28
    new_lo = sff.lo - removed_bytes
    struct.pack_into("<I", data, 40, len(keep_indices))
    struct.pack_into("<IIII", data, 52, new_lo, sff.ls, len(data), 0)
    pending = path.with_suffix(".pruned.pending")
    pending.write_bytes(data)
    pending.replace(path)
    return len(remove_indices)


def main() -> None:
    if MARKER in AIR.read_text(encoding="latin1"):
        additions, sx, sy, details = prepare_frames()
        source = Sff(SFF_PATH)
        pending = SFF_PATH.with_suffix(".v48-refresh.pending")
        pending.write_bytes(source.derive(additions, {}))
        pending.replace(SFF_PATH)
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        report["status"] = "INSTALLED_REFRESHED"
        report["locked_air_scale"] = [sx, sy]
        report["frames"] = details
        report["runtime_sha256"]["spr.sff"] = sha(SFF_PATH)
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name)
    shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)

    additions, sx, sy, details = prepare_frames()
    source = Sff(SFF_PATH)
    pending = SFF_PATH.with_suffix(".v48.pending")
    pending.write_bytes(source.derive({}, additions))
    pending.replace(SFF_PATH)

    air, changed = rewrite_air(AIR.read_text(encoding="latin1"), sx, sy)
    if changed < 100:
        raise RuntimeError(f"too few obsolete AIR rows rerouted: {changed}")
    AIR.write_text(air, encoding="latin1", newline="")

    remove_keys = set(OLD_TO_NEW)
    materialize_link_dependents(SFF_PATH, remove_keys)
    removed = prune_keys(SFF_PATH, remove_keys)

    proof = Sff(SFF_PATH)
    air_proof = AIR.read_text(encoding="latin1")
    stale_refs = []
    for line in air_proof.splitlines():
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                key = (int(parts[0].strip()), int(parts[1].strip()))
            except ValueError:
                continue
            if key in remove_keys:
                stale_refs.append(key)
    missing_new = [key for key in additions if key not in proof.keys]
    surviving_old = [key for key in remove_keys if key in proof.keys]
    if stale_refs or missing_new or surviving_old:
        raise RuntimeError({"stale_refs": stale_refs, "missing_new": missing_new, "surviving_old": surviving_old})

    report = {
        "status": "INSTALLED",
        "revision": "unified-base-v48",
        "canonical_group": GROUP,
        "frames_added": len(additions),
        "air_rows_rerouted": changed,
        "obsolete_sprite_headers_deleted": removed,
        "deleted_keys": [list(key) for key in sorted(remove_keys)],
        "locked_air_scale": [sx, sy],
        "frames": details,
        "runtime_sha256": {"anim.air": sha(AIR), "spr.sff": sha(SFF_PATH)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
