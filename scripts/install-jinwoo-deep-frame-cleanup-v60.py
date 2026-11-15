"""Deep-clean every active modern Jinwoo/summon frame and enforce safe padding."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/deep-frame-cleanup-v60"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
BACKUP, REPORT = ART / "live-before-deep-frame-cleanup-v60", ART / "installation.json"
MIN_MARGIN = 12
# Visual inspection confirmed these hoodie/full-meter sword frames contain
# neighbouring atlas fragments in addition to the real held-sword silhouette.
CONFIRMED_BLEED = {(61011, number) for number in range(124, 128)}


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def active_modern_keys() -> set[tuple[int, int]]:
    keys = set(); action = None
    for raw in AIR.read_text(encoding="latin1").splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            action = int(found.group(1)); continue
        fields = raw.split(";", 1)[0].split(",")
        if action is None or len(fields) < 2:
            continue
        try:
            key = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        if 61000 <= key[0] <= 61024 and key[1] >= 0:
            keys.add(key)
    return keys


def keep_dominant(image: Image.Image) -> tuple[Image.Image, int]:
    alpha = np.asarray(image.getchannel("A"))
    count, labels, stats, _ = cv2.connectedComponentsWithStats((alpha >= 24).astype(np.uint8), 8)
    if count <= 1:
        return image, 0
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    removed = count - 2
    image.putalpha(Image.fromarray(np.where(labels == largest, alpha, 0).astype(np.uint8), mode="L"))
    return image, removed


def safe_pad(image: Image.Image, axis: tuple[int, int]) -> tuple[Image.Image, tuple[int, int], list[int]]:
    box = image.getchannel("A").getbbox()
    if not box:
        raise RuntimeError("empty active sprite")
    margins = [box[0], box[1], image.width - box[2], image.height - box[3]]
    pads = [max(0, MIN_MARGIN - margin) for margin in margins]
    left, top, right, bottom = pads
    if not any(pads):
        return image, axis, pads
    canvas = Image.new("RGBA", (image.width + left + right, image.height + top + bottom), (0, 0, 0, 0))
    canvas.alpha_composite(image, (left, top))
    return canvas, (axis[0] + left, axis[1] + top), pads


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True); shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)
    sff = Sff(SFF_PATH); replacements = {}; details = []
    cleaned_dir = ART / "cleaned"; cleaned_dir.mkdir(exist_ok=True)
    for key in sorted(active_modern_keys()):
        if key not in sff.keys:
            raise RuntimeError(f"active key absent from SFF: {key}")
        index = sff.keys[key]; header = sff.headers[index]
        image = sff.decode(index).convert("RGBA")
        removed = 0
        if key in CONFIRMED_BLEED:
            image, removed = keep_dominant(image)
        image, axis, pads = safe_pad(image, tuple(header[4:6]))
        if removed or any(pads):
            replacements[key] = encoded(image, axis)
            image.save(cleaned_dir / f"{key[0]}-{key[1]}.png", optimize=True)
        details.append({"key": list(key), "removed_components": removed, "padding_ltrb": pads})
    pending = SFF_PATH.with_suffix(".v60.pending")
    pending.write_bytes(sff.derive(replacements, {}))
    try:
        pending.replace(SFF_PATH)
    except PermissionError:
        # Some Windows filter drivers deny an atomic replace of this large SFF
        # even after Ikemen exits. An exact-path overwrite is safe here because
        # the complete derived archive has already been materialized.
        shutil.copy2(pending, SFF_PATH)
        pending.unlink()
    report = {"status": "INSTALLED", "active_frames_checked": len(details),
              "frames_rewritten": len(replacements),
              "confirmed_bleed_frames": [list(key) for key in sorted(CONFIRMED_BLEED)],
              "components_removed": sum(item["removed_components"] for item in details),
              "frames_padded": sum(any(item["padding_ltrb"]) for item in details), "frames": details}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "frames"}, indent=2))


if __name__ == "__main__":
    main()
