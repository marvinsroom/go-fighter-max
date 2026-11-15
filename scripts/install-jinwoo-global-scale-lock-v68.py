"""Lock every approved human Jinwoo art bank to the v64 walk/idle anatomy.

The v64 locomotion pass established the approved 50.4-world-unit human scale,
but older attack, weapon, charge, summon-call, and ultimate AIR rows still used
the pre-v64 scale.  That made the same drawing shrink whenever an attack began.
This pass replaces those stale bank scales without touching pose-specific walk,
jump, crouch, transformation, or summon-form calibration.
"""
from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/global-scale-lock-v68"
AIR = LIVE / "anim.air"

OLD_BASE = (0.095218974, 0.089829218)
NEW_BASE = (0.101895680, 0.096128000)
OLD_DAGGER = (0.156339262, 0.147489865)
NEW_DAGGER = (0.167301691, 0.157831784)
OLD_SWORD = (0.194438745, 0.183432773)
NEW_SWORD = (0.208072691, 0.196294992)

BASE_BANKS = {61013, 61015, 61018, 61019, 61020, 61021}


def pair(fields: list[str]) -> tuple[float, float]:
    sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
    sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
    return round(sx, 9), round(sy, 9)


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "anim.before-v68.air"
    if not backup.exists():
        shutil.copy2(AIR, backup)

    current_action: int | None = None
    changed: Counter[str] = Counter()
    output: list[str] = []
    for raw in AIR.read_text(encoding="latin1").splitlines(keepends=True):
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current_action = int(found.group(1))

        body, separator, comment = raw.partition(";")
        newline = "\r\n" if body.endswith("\r\n") else "\n" if body.endswith("\n") else ""
        core = body[:-len(newline)] if newline else body
        fields = core.split(",")
        try:
            group = int(fields[0].strip())
            int(fields[1].strip())
        except (ValueError, IndexError):
            output.append(raw)
            continue

        while len(fields) < 9:
            fields.append("")
        scale = pair(fields)
        replacement: tuple[float, float] | None = None
        family = ""
        if group in BASE_BANKS and scale == OLD_BASE:
            replacement, family = NEW_BASE, f"base:{group}"
        elif group == 61016 and scale == OLD_DAGGER:
            replacement, family = NEW_DAGGER, "dagger:61016"
        elif group == 61017 and scale == OLD_SWORD:
            replacement, family = NEW_SWORD, "sword:61017"

        if replacement is None:
            output.append(raw)
            continue

        fields[7], fields[8] = f"{replacement[0]:.9f}", f"{replacement[1]:.9f}"
        rebuilt = ",".join(fields) + newline
        if separator:
            rebuilt = rebuilt[:-len(newline)] + ";" + comment if newline else rebuilt + ";" + comment
        output.append(rebuilt)
        changed[family] += 1

    expected_minimums = {
        "base:61013": 200, "base:61015": 30, "dagger:61016": 200,
        "sword:61017": 1000, "base:61018": 4, "base:61019": 15,
        "base:61020": 20, "base:61021": 200,
    }
    missing = {name: [changed[name], minimum] for name, minimum in expected_minimums.items()
               if changed[name] < minimum}
    if missing:
        raise RuntimeError(f"scale migration was incomplete: {missing}")

    pending = ART / "anim.v68.pending.air"
    pending.write_text("".join(output), encoding="latin1", newline="")
    try:
        pending.replace(AIR)
    except (OSError, PermissionError):
        shutil.copy2(pending, AIR)
        pending.unlink()

    report = {
        "status": "INSTALLED",
        "human_world_height_target": 50.4,
        "old_base_scale": list(OLD_BASE),
        "new_base_scale": list(NEW_BASE),
        "new_dagger_scale": list(NEW_DAGGER),
        "new_sword_scale": list(NEW_SWORD),
        "rows_changed": sum(changed.values()),
        "rows_by_family": dict(sorted(changed.items())),
        "pose_specific_banks_preserved": [61022, 61023, 61024],
    }
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
