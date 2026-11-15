"""Remove atlas-neighbour bleed from active dagger and greatsword sprites."""
from __future__ import annotations

import hashlib
import io
import json
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/alpha-cleanup-v59"
SFF_PATH = LIVE / "spr.sff"
BACKUP = ART / "live-before-alpha-cleanup-v59"
REPORT = ART / "installation.json"
GROUPS = (61016, 61017)


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def dominant(image: Image.Image) -> tuple[Image.Image, int, list[int]]:
    image = image.convert("RGBA")
    alpha = np.asarray(image.getchannel("A"))
    mask = (alpha >= 24).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if count <= 1:
        return image, 0, []
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    removed = [int(stats[label, cv2.CC_STAT_AREA]) for label in range(1, count) if label != largest]
    clean = np.where(labels == largest, alpha, 0).astype(np.uint8)
    image.putalpha(Image.fromarray(clean, mode="L"))
    return image, len(removed), sorted(removed, reverse=True)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True); shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)
    sff = Sff(SFF_PATH); replacements = {}; details = []
    normalized = ART / "cleaned"; normalized.mkdir(exist_ok=True)
    for group in GROUPS:
        for number in range(12):
            key = (group, number)
            if key not in sff.keys:
                raise RuntimeError(f"missing weapon key {key}")
            index = sff.keys[key]; header = sff.headers[index]
            image, removed_count, removed_areas = dominant(sff.decode(index))
            image.save(normalized / f"{group}-{number}.png", optimize=True)
            replacements[key] = encoded(image, tuple(header[4:6]))
            details.append({"key": list(key), "removed_components": removed_count, "removed_areas": removed_areas[:8]})
    pending = SFF_PATH.with_suffix(".v59.pending")
    pending.write_bytes(sff.derive(replacements, {})); pending.replace(SFF_PATH)
    report = {"status": "INSTALLED", "groups": list(GROUPS),
              "frames_cleaned": sum(item["removed_components"] > 0 for item in details),
              "components_removed": sum(item["removed_components"] for item in details), "frames": details}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
