"""Lock every approved high-resolution Jinwoo body frame to canonical scale."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/human-scale-v46"
BACKUP = OUT / "live-before-v46"
AIR = LIVE / "anim.air"
MARKER = "; JINWOO HUMAN SCALE AND CHARGE FIX V46"
SX = "0.032913216"
SY = "0.031050203"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_action(text: str, number: int, body: str) -> str:
    pattern = rf"(?ms)^\[Begin Action {number}\]\s*.*?(?=^\[Begin Action |\Z)"
    updated, count = re.subn(pattern, body.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"action {number} replacement count was {count}")
    return updated


def normalize_body_rows(text: str) -> tuple[str, int, list[int]]:
    changed = 0
    actions: set[int] = set()
    current_action = -1
    output: list[str] = []
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current_action = int(match.group(1))
        parts = line.split(",")
        if len(parts) >= 9:
            try:
                group = int(parts[0].strip())
                number = int(parts[1].strip())
            except ValueError:
                group = number = -1
            if group == 300 and 101 <= number <= 136:
                if parts[7].strip() != SX or parts[8].strip() != SY:
                    parts[7] = SX
                    parts[8] = SY
                    line = ",".join(parts)
                    changed += 1
                    actions.add(current_action)
        output.append(line)
    return "\n".join(output).rstrip() + "\n", changed, sorted(actions)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air = AIR.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8"))
        return

    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name)

    air, changed, affected_actions = normalize_body_rows(air)
    charge = f"""[Begin Action 500]
Clsn2Default: 1
Clsn2[0] = -10,-60,9,0
LoopStart
300,101,0,0,7,,,{SX},{SY}
300,102,0,0,7,,,{SX},{SY}
300,103,0,0,7,,,{SX},{SY}
300,104,0,0,7,,,{SX},{SY}
300,105,0,0,7,,,{SX},{SY}"""
    release = f"""[Begin Action 501]
Clsn2Default: 1
Clsn2[0] = -9,-60,8,0
300,104,0,0,4,,,{SX},{SY}
300,105,0,0,4,,,{SX},{SY}"""
    air = replace_action(air, 500, charge)
    air = replace_action(air, 501, release)
    AIR.write_text(MARKER + "\n" + air, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "revision": "human-scale-v46",
        "corrected_high_resolution_rows": changed,
        "affected_actions": affected_actions,
        "charge_actions_rebuilt": [500, 501],
        "canonical_scale": [float(SX), float(SY)],
        "runtime_sha256": {"anim.air": sha(AIR)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
