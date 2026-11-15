"""Route every grounded bare-hand gameplay action through v48 body frames."""
from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
AIR = LIVE / "anim.air"
BACKUP = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/live-before-ground-coverage-v51.air"
GROUP = 61013
SX = "0.095218974"
SY = "0.089829218"
MARKER = "; JINWOO V48 GROUNDED COVERAGE V51"

# Each list is a semantic pose sequence. Extra animation rows reuse the final
# recovery pose, preserving the original timing and collision/event layout.
POSES = {
    400: [12, 18, 20, 21, 23],
    410: [18, 20, 21, 23],
    420: [18, 20, 21, 23],
    460: [18, 20, 21, 23],
    875200: [18, 19, 23],
    875210: [18, 20, 19, 23],
    875220: [18, 20, 21, 23],
    875400: [12, 21, 12],
    875410: [12, 21, 12],
}


def main() -> None:
    text = AIR.read_text(encoding="latin1")
    if MARKER in text:
        print("v48 grounded coverage already installed")
        return
    shutil.copy2(AIR, BACKUP)
    current = None
    row = 0
    changed = 0
    output = []
    for raw in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if match:
            current = int(match.group(1))
            row = 0
        if current in POSES and re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", raw):
            fields = raw.split(",")
            try:
                int(fields[0].strip()); int(fields[1].strip())
            except (ValueError, IndexError):
                output.append(raw)
                continue
            pose_list = POSES[current]
            pose = pose_list[min(row, len(pose_list) - 1)]
            while len(fields) < 9:
                fields.append("")
            fields[0], fields[1] = str(GROUP), str(pose)
            fields[7], fields[8] = SX, SY
            raw = ",".join(fields)
            row += 1
            changed += 1
        output.append(raw)
    if changed < 35:
        raise RuntimeError(f"expected at least 35 grounded rows, changed {changed}")
    AIR.write_text("\n".join(output).rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")
    print({"status": "INSTALLED", "rows_rerouted": changed, "actions": sorted(POSES)})


if __name__ == "__main__":
    main()
