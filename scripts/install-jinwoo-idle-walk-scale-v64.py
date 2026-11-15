"""Match Jinwoo's idle silhouette to the approved forward/back walk size."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/idle-walk-scale-v64"
AIR = LIVE / "anim.air"
IDLE_ACTIONS = (0, 5, 6)
SX, SY = 0.101895680, 0.096128000


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "anim.before-v64.air"
    if not backup.exists():
        shutil.copy2(AIR, backup)
    text = AIR.read_text(encoding="latin1")
    changed = 0
    for action in IDLE_ACTIONS:
        match = re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)", text)
        if not match:
            raise RuntimeError(f"missing idle action {action}")
        block = match.group(0)
        block, count = re.subn(
            r"(?m)^([ \t]*61013\s*,\s*24\s*,[^\r\n]*?,,,)[0-9.]+,[0-9.]+[ \t]*$",
            rf"\g<1>{SX:.9f},{SY:.9f}",
            block,
        )
        if not count:
            raise RuntimeError(f"idle action {action} has no canonical body row")
        changed += count
        text = text[:match.start()] + block + text[match.end():]
    pending = ART / "anim.v64.pending.air"
    pending.write_text(text, encoding="latin1", newline="")
    try:
        pending.replace(AIR)
    except (OSError, PermissionError):
        shutil.copy2(pending, AIR)
        pending.unlink()
    report = {"status": "INSTALLED", "actions": list(IDLE_ACTIONS), "rows": changed,
              "idle_scale": [SX, SY], "baseline": "forward/back walk 61022"}
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
