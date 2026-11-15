"""Verify canonical high-resolution scale and charge identity."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
AIR = LIVE / "anim.air"
SX, SY = 0.032913216, 0.031050203


def actions(text: str) -> dict[int, list[tuple[int, int, float, float]]]:
    result: dict[int, list[tuple[int, int, float, float]]] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current = int(match.group(1)); result.setdefault(current, [])
            continue
        if current is None or not re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", line):
            continue
        fields = [part.strip() for part in line.split(";")[0].split(",")]
        fields += [""] * (9 - len(fields))
        try:
            result[current].append((int(fields[0]), int(fields[1]),
                                    float(fields[7] or 1), float(fields[8] or 1)))
        except ValueError:
            pass
    return result


def main() -> None:
    text = AIR.read_text(encoding="latin1")
    parsed = actions(text)
    failures: list[str] = []
    checked = 0
    for action, frames in parsed.items():
        for group, number, sx, sy in frames:
            if group == 300 and 101 <= number <= 136:
                checked += 1
                if abs(sx - SX) > 1e-9 or abs(sy - SY) > 1e-9:
                    failures.append(f"action {action} frame {group},{number} scale {sx},{sy}")

    expected_charge = {
        500: [(300, 101), (300, 102), (300, 103), (300, 104), (300, 105)],
        501: [(300, 104), (300, 105)],
    }
    sff = Sff(LIVE / "spr.sff")
    charge_heights: dict[str, list[float]] = {}
    for action, expected in expected_charge.items():
        actual = [(g, n) for g, n, _, _ in parsed.get(action, [])]
        if actual != expected:
            failures.append(f"action {action} keys {actual}")
            continue
        heights = []
        for group, number, _, sy in parsed[action]:
            image: Image.Image = sff.decode(sff.keys[(group, number)])
            box = image.getchannel("A").getbbox()
            heights.append(round((box[3] - box[1]) * sy, 3))
        charge_heights[str(action)] = heights
        if any(abs(height - 43.657) > 0.05 for height in heights):
            failures.append(f"action {action} heights {heights}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "high_resolution_rows_checked": checked,
        "charge_world_heights": charge_heights,
        "canonical_scale": [SX, SY],
        "failures": failures,
    }
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
