"""Repair live Jinwoo jump phases, body-bank scale, and Igris animation routing."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/audit-v38"
BACKUP = OUT / "live-before-v38"
REPORT = OUT / "animation-fix-v38.json"
MARKER = "; JINWOO_ANIMATION_CONSISTENCY_V38"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_action(text: str, action: int, body: str) -> str:
    pattern = rf"(?ms)^\[Begin Action {action}\]\s*.*?(?=^\[Begin Action |\Z)"
    updated, count = re.subn(pattern, body.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"action {action} replacement count was {count}")
    return updated


def scale_banks(text: str) -> tuple[str, dict[str, int]]:
    factors = {61000: 1.194446, 61005: 1.185236, 61011: 1.159240}
    counts = {str(group): 0 for group in factors}
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        match = re.match(r"^(\s*)(61000|61005|61011)\s*,", line)
        if not match:
            output.append(line); continue
        fields = line.rstrip("\r\n").split(",")
        group = int(fields[0].strip())
        if len(fields) < 9 or not fields[7].strip() or not fields[8].strip():
            output.append(line); continue
        try:
            fields[7] = f"{float(fields[7]) * factors[group]:.9f}"
            fields[8] = f"{float(fields[8]) * factors[group]:.9f}"
        except ValueError:
            output.append(line); continue
        ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        output.append(",".join(fields) + ending)
        counts[str(group)] += 1
    return "".join(output), counts


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    air_path, cns_path = LIVE / "anim.air", LIVE / "cns.cns"
    air = air_path.read_text(encoding="latin1")
    if MARKER in air:
        print(REPORT.read_text(encoding="utf-8")); return

    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (air_path, cns_path):
        shutil.copy2(path, BACKUP / path.name)

    air, scale_counts = scale_banks(air)
    # The old Igris groups are visually obsolete. The accurate manga bank is 61001.
    air, old_knight_count = re.subn(r"(?m)^(\s*)100[01](\s*,)", r"\g<1>61001\2", air)

    jump_actions = {
        40: """[Begin Action 40]
Clsn2Default: 1
Clsn2[0] = -12,-44,14,0
300,119,0,0,2,,,0.032913216,0.031050203
300,120,0,0,2,,,0.032913216,0.031050203
300,118,0,0,2,,,0.032913216,0.031050203""",
        41: """[Begin Action 41]
Clsn2Default: 1
Clsn2[0] = -14,-54,14,0
300,118,0,0,3,,,0.032913216,0.031050203
LoopStart
300,115,0,0,6,,,0.032913216,0.031050203""",
        42: """[Begin Action 42]
Clsn2Default: 1
Clsn2[0] = -15,-52,17,0
LoopStart
300,115,0,0,5,,,0.032913216,0.031050203
300,116,0,0,5,,,0.032913216,0.031050203""",
        43: """[Begin Action 43]
Clsn2Default: 1
Clsn2[0] = -17,-52,15,0
LoopStart
300,128,0,0,5,,,0.032913216,0.031050203
300,127,0,0,5,,,0.032913216,0.031050203""",
        44: """[Begin Action 44]
Clsn2Default: 1
Clsn2[0] = -16,-54,19,0
300,116,0,0,4,,,0.032913216,0.031050203
LoopStart
300,117,0,0,6,,,0.032913216,0.031050203""",
        45: """[Begin Action 45]
Clsn2Default: 1
Clsn2[0] = -16,-54,19,0
300,115,0,0,4,,,0.032913216,0.031050203
300,116,0,0,4,,,0.032913216,0.031050203
LoopStart
300,117,0,0,6,,,0.032913216,0.031050203""",
        47: """[Begin Action 47]
Clsn2Default: 1
Clsn2[0] = -12,-48,13,0
300,129,0,0,2,,,0.032913216,0.031050203
300,130,0,0,2,,,0.032913216,0.031050203
300,131,0,0,2,,,0.032913216,0.031050203
300,101,0,0,2,,,0.032913216,0.031050203""",
        50: """[Begin Action 50]
Clsn2Default: 1
Clsn2[0] = -14,-54,14,0
300,118,0,0,3,,,0.032913216,0.031050203
LoopStart
300,115,0,0,6,,,0.032913216,0.031050203""",
        52: """[Begin Action 52]
Clsn2Default: 1
Clsn2[0] = -16,-54,19,0
300,116,0,0,4,,,0.032913216,0.031050203
LoopStart
300,117,0,0,6,,,0.032913216,0.031050203""",
    }
    for action, body in jump_actions.items():
        air = replace_action(air, action, body)

    knight_actions = {
        2210: """[Begin Action 2210]
61001,34,0,0,6,,AS0D0,0.238095238,0.238095238
61001,34,0,0,4,,,0.238095238,0.238095238
61001,35,0,0,8,,,0.238095238,0.238095238
LoopStart
61001,35,0,0,20,,,0.238095238,0.238095238""",
        2211: """[Begin Action 2211]
61001,34,0,0,6,,AS0D0,0.238095238,0.238095238
61001,34,0,0,4,,,0.238095238,0.238095238
61001,35,0,0,8,,,0.238095238,0.238095238
LoopStart
61001,35,0,0,20,,,0.238095238,0.238095238""",
        2215: """[Begin Action 2215]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -11,-79,18,-37
LoopStart
61001,35,0,0,18,,,0.238095238,0.238095238
61001,0,0,0,8,,,0.238095238,0.238095238
61001,35,0,0,18,,,0.238095238,0.238095238""",
        2216: """[Begin Action 2216]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -11,-79,18,-37
LoopStart
61001,35,0,0,18,,,0.238095238,0.238095238
61001,0,0,0,8,,,0.238095238,0.238095238
61001,35,0,0,18,,,0.238095238,0.238095238""",
        2220: """[Begin Action 2220]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -17,-75,12,-37
LoopStart
61001,0,0,0,5,,,0.238095238,0.238095238
61001,1,0,0,5,,,0.238095238,0.238095238
61001,2,0,0,5,,,0.238095238,0.238095238
61001,3,0,0,5,,,0.238095238,0.238095238
61001,4,0,0,5,,,0.238095238,0.238095238""",
        2221: """[Begin Action 2221]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -17,-75,12,-37
LoopStart
61001,0,0,0,5,,,0.238095238,0.238095238
61001,1,0,0,5,,,0.238095238,0.238095238
61001,2,0,0,5,,,0.238095238,0.238095238
61001,3,0,0,5,,,0.238095238,0.238095238
61001,4,0,0,5,,,0.238095238,0.238095238""",
        2225: """[Begin Action 2225]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -17,-75,12,-37
LoopStart
61001,4,0,0,6,H,,0.238095238,0.238095238
61001,3,0,0,6,H,,0.238095238,0.238095238
61001,2,0,0,6,H,,0.238095238,0.238095238
61001,1,0,0,6,H,,0.238095238,0.238095238
61001,0,0,0,6,H,,0.238095238,0.238095238""",
        2226: """[Begin Action 2226]
Clsn2Default: 2
Clsn2[0] = -26,-37,19,1
Clsn2[1] = -17,-75,12,-37
LoopStart
61001,4,0,0,6,H,,0.238095238,0.238095238
61001,3,0,0,6,H,,0.238095238,0.238095238
61001,2,0,0,6,H,,0.238095238,0.238095238
61001,1,0,0,6,H,,0.238095238,0.238095238
61001,0,0,0,6,H,,0.238095238,0.238095238""",
    }
    for action, body in knight_actions.items():
        air = replace_action(air, action, body)
    air = MARKER + "\n" + air

    cns = cns_path.read_text(encoding="latin1")
    match = re.search(r"(?ms)^\[Statedef 2220\].*?(?=^\[Statedef |\Z)", cns)
    if not match:
        raise RuntimeError("missing Statedef 2220")
    fixed_block, count = re.subn(r"\(2225\)", "(2220)", match.group(0))
    if count < 1:
        raise RuntimeError("Statedef 2220 did not contain backward animation routing")
    cns = cns[:match.start()] + fixed_block + cns[match.end():]

    air_path.write_text(air, encoding="latin1", newline="")
    cns_path.write_text(cns, encoding="latin1", newline="")
    report = {
        "status": "INSTALLED",
        "jump_actions_rebuilt": sorted(jump_actions),
        "knight_actions_rebuilt": sorted(knight_actions),
        "old_knight_frame_references_rerouted": old_knight_count,
        "normalized_body_frame_references": scale_counts,
        "state_2220_backward_routes_fixed": count,
        "runtime_sha256": {"anim.air": sha(air_path), "cns.cns": sha(cns_path)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
