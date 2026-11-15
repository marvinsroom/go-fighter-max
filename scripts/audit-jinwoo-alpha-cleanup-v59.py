"""Reject detached anatomy and edge bleed in active weapon/movement banks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/alpha-cleanup-v59/audit.json"
GROUP_COUNTS = {61016: 12, 61017: 12, 61022: 6, 61023: 6, 61024: 3}


def main() -> None:
    sff = Sff(LIVE / "spr.sff"); failures = []; frames = []
    for group, count_expected in GROUP_COUNTS.items():
        for number in range(count_expected):
            key = (group, number)
            if key not in sff.keys:
                failures.append(f"missing {key}"); continue
            image = sff.decode(sff.keys[key]).convert("RGBA")
            alpha = np.asarray(image.getchannel("A"))
            count, _, stats, _ = cv2.connectedComponentsWithStats((alpha >= 24).astype(np.uint8), 8)
            significant = sorted([int(stats[label, cv2.CC_STAT_AREA]) for label in range(1, count) if stats[label, cv2.CC_STAT_AREA] >= 80], reverse=True)
            frames.append({"key": list(key), "significant_components": significant})
            if len(significant) > 1:
                failures.append(f"{key} has detached significant components {significant[:6]}")
    report = {"status": "PASS" if not failures else "FAIL", "frames": frames, "failures": failures}
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "failures": failures, "report": str(OUT)}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
