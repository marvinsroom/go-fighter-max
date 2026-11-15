"""Gate Jinwoo against missing sprites, frozen ultimates, and transform locks."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/runtime-integrity-v56/audit.json"
WATCHED = {3000, 3100, 13100, 23100, 503100, 513100, 523100, 3120, 13120, 23120, 503120, 513120, 523120, 3200, 3210, 3220}


def parse_actions(text: str) -> dict[int, list[tuple[int, int, int]]]:
    parsed: dict[int, list[tuple[int, int, int]]] = {}
    current = None
    for raw in text.splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); parsed.setdefault(current, []); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            group, image = int(fields[0].strip()), int(fields[1].strip())
            duration = int(fields[4].strip()) if len(fields) > 4 and fields[4].strip() else 1
        except (ValueError, IndexError):
            continue
        parsed[current].append((group, image, duration))
    return parsed


def main() -> None:
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    shadows = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    actions = parse_actions(air)
    sff = Sff(LIVE / "spr.sff")
    missing = []
    for action, rows in actions.items():
        for group, image, _ in rows:
            if group >= 0 and image >= 0 and (group, image) not in sff.keys:
                missing.append([action, group, image])

    failures = []
    if missing:
        failures.append(f"{len(missing)} AIR rows still reference absent SFF sprites")
    timing = {}
    for action in sorted(WATCHED):
        rows = actions.get(action, [])
        positive = [duration for _, _, duration in rows if duration > 0]
        max_hold = max(positive, default=0)
        timing[str(action)] = {"frames": len(rows), "total_ticks": sum(positive), "max_hold_ticks": max_hold}
        if not rows or max_hold > 10:
            failures.append(f"action {action} has a frozen hold of {max_hold} ticks")

    transform_watchdogs = {}
    for state in range(870201, 870207):
        match = re.search(rf"(?ims)^\[Statedef\s+{state}\].*?(?=^\[Statedef\s+\d+\]|\Z)", shadows)
        passed = bool(match and re.search(r"(?im)^trigger1\s*=\s*time\s*>=\s*36\s*$", match.group(0)))
        transform_watchdogs[str(state)] = passed
        if not passed:
            failures.append(f"transform {state} lacks the 36-tick recovery watchdog")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "missing_sprite_rows": missing,
        "ultimate_timing": timing,
        "transform_watchdogs": transform_watchdogs,
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "missing": len(missing), "failures": failures, "report": str(OUT)}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
