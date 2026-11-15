"""Verify isolated canonical bare-hand normal frames and routing."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
TARGET_ACTIONS = {200, 210, 220, 260, 300, 310, 320, 350}


def main() -> None:
    text = (LIVE / "anim.air").read_text(encoding="latin1")
    sff = Sff(LIVE / "spr.sff")
    failures = []
    current = None
    rows = 0
    heights = []
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current = int(match.group(1))
        if current not in TARGET_ACTIONS or not re.match(r"\s*\d+\s*,\s*\d+\s*,", line):
            continue
        fields = [part.strip() for part in line.split(";")[0].split(",")]
        fields += [""] * (9 - len(fields))
        group, number = int(fields[0]), int(fields[1])
        if group != 61012:
            failures.append(f"action {current} legacy body {group},{number}")
            continue
        rows += 1
        image = sff.decode(sff.keys[(group, number)])
        box = image.getchannel("A").getbbox()
        height = (box[3] - box[1]) * float(fields[8])
        heights.append(round(height, 3))
        if abs(height - 43.657) > .02:
            failures.append(f"action {current} frame {number} height {height}")
    if rows != 40:
        failures.append(f"expected 40 routed rows, found {rows}")
    report = {"status": "PASS" if not failures else "FAIL", "routed_rows": rows,
              "sprite_keys": [[61012, number] for number in range(8)],
              "world_heights": sorted(set(heights)), "failures": failures}
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
