"""Broad gate for missing, clipped, or confirmed-bleed modern AIR frames."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/deep-frame-cleanup-v60/audit.json"
SINGLE_SILHOUETTE_GROUPS = {61013, 61015, 61016, 61017, 61020, 61021, 61022, 61023, 61024}
SINGLE_KEYS = {(61011, number) for number in range(124, 128)}


def active_keys() -> set[tuple[int, int]]:
    result = set(); current = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            key = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        if 61000 <= key[0] <= 61024 and key[1] >= 0:
            result.add(key)
    return result


def main() -> None:
    sff = Sff(LIVE / "spr.sff"); failures = []; details = []
    for key in sorted(active_keys()):
        if key not in sff.keys:
            failures.append(f"missing active sprite {key}"); continue
        image = sff.decode(sff.keys[key]).convert("RGBA")
        alpha = np.asarray(image.getchannel("A")); mask = (alpha >= 24).astype(np.uint8)
        ys, xs = np.where(mask > 0)
        if not len(xs):
            failures.append(f"empty active sprite {key}"); continue
        margins = [int(xs.min()), int(ys.min()), int(image.width - 1 - xs.max()), int(image.height - 1 - ys.max())]
        if min(margins) < 12:
            failures.append(f"active sprite {key} lacks safe padding: {margins}")
        count, _, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        significant = sorted([int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, count) if stats[i, cv2.CC_STAT_AREA] >= 80], reverse=True)
        if (key[0] in SINGLE_SILHOUETTE_GROUPS or key in SINGLE_KEYS) and len(significant) > 1:
            failures.append(f"body sprite {key} has detached components: {significant[:6]}")
        details.append({"key": list(key), "margins_ltrb": margins, "significant_components": significant})
    report = {"status": "PASS" if not failures else "FAIL", "active_frames": len(details), "failures": failures, "frames": details}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "active_frames": len(details), "failures": failures, "report": str(OUT)}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
