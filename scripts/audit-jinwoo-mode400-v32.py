"""Audit Jinwoo's complete v32 mode-400 sword locomotion set."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = BASE / "mode-400-normalized"
REPORT = BASE / "mode-400-audit-v32.json"
MIN_MARGIN = 16
FILES = {
    "400,2": "400-002-idle-anchor.png",
    "400,3": "400-003-idle-2.png",
    "400,4": "400-004-idle-3.png",
    "400,5": "400-005-idle-2-return.png",
    "400,6": "400-006-idle-1-return.png",
    "400,7": "400-007-walk-anchor.png",
    "400,8": "400-008-walk-2.png",
    "400,9": "400-009-walk-3.png",
    "400,10": "400-010-walk-4.png",
    "400,11": "400-011-walk-5.png",
    "400,12": "400-012-walk-6.png",
    "400,14": "400-014-air-anchor.png",
    "400,15": "400-015-jump-apex.png",
    "400,16": "400-016-jump-fall.png",
    "400,17": "400-017-jump-start.png",
    "400,18": "400-018-crouch-transition-1.png",
    "400,19": "400-019-crouch-transition-2.png",
    "400,20": "400-020-crouch-hold.png",
    "400,21": "400-021-run-4.png",
    "400,22": "400-022-run-5.png",
    "400,23": "400-023-backdash-2.png",
    "400,24": "400-024-backdash-3.png",
    "400,25": "400-025-backdash-4.png",
    "400,26": "400-026-backdash-5.png",
    "400,27": "400-027-backdash-6.png",
    "400,28": "400-028-run-stop-1.png",
    "400,29": "400-029-air-dash-forward.png",
    "400,54": "400-054-backdash-1.png",
    "400,59": "400-059-run-1.png",
    "400,67": "400-067-run-2.png",
    "400,68": "400-068-run-3.png",
}


def main() -> None:
    review = json.loads((BASE / "mode-400-review-v32.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    rows = {}
    hashes = {}
    for key, name in FILES.items():
        path = SOURCE / name
        row = {"file": name, "exists": path.is_file()}
        rows[key] = row
        if not path.is_file():
            errors.append(f"missing:{key}:{name}")
            continue
        image = Image.open(path).convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.point(lambda value: 255 if value >= 96 else 0).getbbox()
        digest = hashlib.sha256(image.tobytes()).hexdigest()
        hashes[key] = digest
        row.update({"size": list(image.size), "opaque_bbox": list(bbox) if bbox else None, "sha256": digest})
        if image.size != (1024, 1536):
            errors.append(f"wrong_size:{key}:{image.size}")
        if not bbox:
            errors.append(f"empty:{key}")
        else:
            left, top, right, bottom = bbox
            margins = (left, top, image.width - right, image.height - bottom)
            row["opaque_margins"] = list(margins)
            if min(margins) < MIN_MARGIN:
                errors.append(f"unsafe_margin:{key}:{margins}")
        manual = review["manual_review"].get(key, {})
        row["manual_anatomy"] = manual
        if manual.get("arms") != 2 or manual.get("hands") != 2:
            errors.append(f"anatomy_not_approved:{key}")
        if manual.get("grip_hand") != "forward-right":
            errors.append(f"wrong_or_unreviewed_grip_hand:{key}")
        if manual.get("weapons") != 1:
            errors.append(f"weapon_count_not_approved:{key}")
        if manual.get("facing") != "screen-right":
            errors.append(f"facing_not_approved:{key}")

    walk_keys = [f"400,{number}" for number in range(7, 13)]
    if all(key in hashes for key in walk_keys) and len({hashes[key] for key in walk_keys}) != 6:
        errors.append("duplicate_walk_frames")
    if not (BASE / "weapon-masters/long-sword-approved-v32.png").is_file():
        errors.append("missing_approved_long_sword_master")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "completed_unique_mode400_keys": len(rows),
        "required_total_mode400_keys": 31,
        "walk_cycle_complete": all(rows[key]["exists"] for key in walk_keys),
        "errors": errors,
        "frames": rows,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "completed_unique_mode400_keys", "required_total_mode400_keys", "walk_cycle_complete", "errors")}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
