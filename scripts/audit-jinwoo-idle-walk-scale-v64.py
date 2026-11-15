"""Verify idle and walking have the same apparent height and width."""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/idle-walk-scale-v64/audit.json"


def rows(text: str, action: int) -> list[tuple[int, int, float, float]]:
    match = re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)", text)
    result = []
    for raw in match.group(0).splitlines() if match else []:
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0]), int(fields[1])
        except ValueError:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result.append((group, frame, sx, sy))
    return result


def main() -> None:
    text = (LIVE / "anim.air").read_text(encoding="latin1")
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    char_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    char_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))
    sff = Sff(LIVE / "spr.sff")

    def dimensions(row: tuple[int, int, float, float]) -> tuple[float, float]:
        group, frame, sx, sy = row
        box = sff.decode(sff.keys[(group, frame)]).convert("RGBA").getchannel("A").getbbox()
        return (box[2] - box[0]) * sx * char_x, (box[3] - box[1]) * sy * char_y

    idle_rows = rows(text, 0)
    walk_rows = rows(text, 20)
    idle_dims = [dimensions(row) for row in idle_rows]
    walk_dims = [dimensions(row) for row in walk_rows]
    idle = [statistics.median(value[index] for value in idle_dims) for index in (0, 1)]
    walk = [statistics.median(value[index] for value in walk_dims) for index in (0, 1)]
    ratios = [idle[index] / walk[index] for index in (0, 1)]
    failures = []
    if any(not 0.97 <= ratio <= 1.03 for ratio in ratios):
        failures.append(f"idle does not match approved walk size: ratios={ratios}")
    for action in (0, 5, 6):
        if {(row[0], row[1]) for row in rows(text, action)} != {(61013, 24)}:
            failures.append(f"idle action {action} escaped canonical frame 61013,24")
    report = {"status": "PASS" if not failures else "FAIL",
              "idle_world_size": [round(value, 3) for value in idle],
              "walk_median_world_size": [round(value, 3) for value in walk],
              "idle_to_walk_ratios": [round(value, 3) for value in ratios], "failures": failures}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
