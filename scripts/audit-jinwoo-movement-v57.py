"""Verify v57 movement exclusivity, cadence, completeness, and charge release."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/movement-v57/audit.json"
WALK_ACTIONS = (20, 21)
JUMP_ACTIONS = (40, 41, 42, 43, 44, 45, 47, 50, 52)


def actions(text: str) -> dict[int, list[tuple[int, int, int, int, int]]]:
    result = {}
    current = None
    for raw in text.splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); result.setdefault(current, []); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 5:
            continue
        try:
            result[current].append(tuple(int(fields[index].strip() or 0) for index in range(5)))
        except ValueError:
            pass
    return result


def main() -> None:
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    bank = actions(air)
    sff = Sff(LIVE / "spr.sff")
    failures = []
    for number in WALK_ACTIONS:
        rows = bank.get(number, [])
        if len(rows) != 6 or {row[0] for row in rows} != {61022} or {row[1] for row in rows} != set(range(6)):
            failures.append(f"walk action {number} is not the exclusive six-phase v57 cycle")
    for number in JUMP_ACTIONS:
        rows = bank.get(number, [])
        if not rows or {row[0] for row in rows} != {61023}:
            failures.append(f"jump action {number} escaped the v57 jump bank")
    missing = [list(key) for key in [(61022, n) for n in range(6)] + [(61023, n) for n in range(6)] if key not in sff.keys]
    if missing:
        failures.append(f"missing v57 SFF keys: {missing}")
    for number in (500, 10500, 20500):
        rows = bank.get(number, [])
        if len(rows) != 4 or {(row[0], row[1]) for row in rows} != {(61019, 0)}:
            failures.append(f"charge action {number} changes body identity")
        if [row[3] for row in rows] != [0, -1, -2, -1]:
            failures.append(f"charge action {number} lacks the subtle breathing arc")
    state = re.search(r"(?ims)^\[statedef 500\].*?(?=^\[statedef 501\])", cns)
    release_ok = bool(state and '!command = "our_holdcharge"' in state.group(0) and 'time >= 300' in state.group(0))
    if not release_ok:
        failures.append("charge state lacks release detection or hard watchdog")
    report = {"status": "PASS" if not failures else "FAIL", "missing": missing, "charge_release": release_ok, "failures": failures}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
