"""Audit every human Jinwoo gameplay bank against the locked v48 body."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/full-coverage.json"
V48 = 61013
V48_BODY_GROUPS = {61013, 61015, 61018, 61019}
DAGGER_GROUP = 61016
SWORD_GROUP = 61017

MOVEMENT = (0, 5, 6, 10, 11, 12, 20, 21, 40, 41, 42, 43, 44, 45, 47, 50, 52, 100, 105)
NORMALS = (200, 210, 220, 260, 300, 310, 320, 350, 400, 410, 420, 460,
           600, 610, 620, 630, 640, 650)
CHARGE = (500, 501, 510, 10500, 10501, 10510, 20500, 20501, 20510)
CUSTOM_BARE = (875200, 875210, 875220, 875400, 875410, 875600, 875610, 875620, 876290)
CUSTOM_DAGGER = (876300,)
CUSTOM_SWORD = (876310,)


def parse_air() -> dict[int, list[tuple[int, int]]]:
    actions: dict[int, list[tuple[int, int]]] = defaultdict(list)
    current: int | None = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if match:
            current = int(match.group(1))
            continue
        if current is None or not re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", raw):
            continue
        fields = raw.split(";", 1)[0].split(",")
        try:
            actions[current].append((int(fields[0].strip()), int(fields[1].strip())))
        except (ValueError, IndexError):
            pass
    return actions


def bank(actions: dict[int, list[tuple[int, int]]], ids: tuple[int, ...]) -> dict[str, object]:
    present = [action for action in ids if action in actions]
    keys = sorted({key for action in present for key in actions[action]})
    groups = sorted({group for group, _ in keys})
    return {
        "actions_expected": list(ids),
        "actions_present": present,
        "missing_actions": sorted(set(ids) - set(present)),
        "groups": groups,
        "keys": [list(key) for key in keys],
        "v48_only": groups == [V48],
    }


def main() -> None:
    actions = parse_air()
    core = MOVEMENT + NORMALS
    categories = {
        "bare_movement": bank(actions, MOVEMENT),
        "bare_normals": bank(actions, NORMALS),
        "bare_custom": bank(actions, CUSTOM_BARE),
        "charge": bank(actions, CHARGE),
        "dagger_movement": bank(actions, tuple(700000 + action for action in MOVEMENT)),
        "dagger_normals": bank(actions, tuple(700000 + action for action in NORMALS)),
        "dagger_custom": bank(actions, CUSTOM_DAGGER),
        "sword_movement": bank(actions, tuple(500000 + action for action in MOVEMENT)),
        "sword_normals": bank(actions, tuple(500000 + action for action in NORMALS)),
        "sword_custom": bank(actions, CUSTOM_SWORD),
    }
    categories["bare_core"] = bank(actions, core)
    failures = []
    for name, data in categories.items():
        if data["missing_actions"]:
            failures.append(f"{name}:missing-actions")
        groups = set(data["groups"])
        if name.startswith("bare_") and not groups.issubset(V48_BODY_GROUPS):
            failures.append(f"{name}:legacy-groups:{data['groups']}")
        if name == "charge" and groups != {61019}:
            failures.append(f"{name}:legacy-groups:{data['groups']}")
        if name.startswith("dagger_") and groups != {DAGGER_GROUP}:
            failures.append(f"{name}:wrong-groups:{data['groups']}")
        if name.startswith("sword_") and groups != {SWORD_GROUP}:
            failures.append(f"{name}:wrong-groups:{data['groups']}")
    report = {
        "status": "PASS" if not failures else "FAIL",
        "canonical_group": V48,
        "categories": categories,
        "failures": failures,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "failures": failures,
        "groups": {name: data["groups"] for name, data in categories.items()},
        "report": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
