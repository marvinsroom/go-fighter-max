"""Verify Jinwoo's active v48 scale lock, crouch family, and charge cadence."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/scale-lock-v55"
SX, SY = 0.101895680, 0.096128000
CROUCH_ACTIONS = (400, 410, 420, 460)
CHARGE_ACTIONS = (500, 501, 510, 10500, 10501, 10510, 20500, 20501, 20510)


def actions() -> dict[int, list[dict[str, float | int]]]:
    result: dict[int, list[dict[str, float | int]]] = {}
    current = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); result.setdefault(current, []); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        duration = int(fields[4].strip()) if len(fields) > 4 and fields[4].strip() else 1
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result[current].append({"group": group, "frame": frame, "duration": duration, "sx": sx, "sy": sy})
    return result


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    parsed = actions()
    failures = []
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    match_x = re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns)
    match_y = re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns)
    scale = (float(match_x.group(1)), float(match_y.group(1))) if match_x and match_y else None
    if scale != (1.39, 1.07):
        failures.append(f"character scale is not locked to (1.39, 1.07): {scale}")

    report_actions = {}
    for number in CROUCH_ACTIONS:
        rows = parsed.get(number, [])
        groups = {row["group"] for row in rows}
        frames = {row["frame"] for row in rows}
        report_actions[str(number)] = rows
        if not rows or groups != {61013}:
            failures.append(f"crouch action {number} escaped group 61013: {groups}")
        if not frames.issubset(set(range(12, 18))):
            failures.append(f"crouch action {number} uses upright frames: {sorted(frames)}")
        if {(round(row['sx'], 9), round(row['sy'], 9)) for row in rows} != {(SX, SY)}:
            failures.append(f"crouch action {number} has AIR scale drift")

    for number in CHARGE_ACTIONS:
        rows = parsed.get(number, [])
        report_actions[str(number)] = rows
        if not rows or {row["group"] for row in rows} != {61019}:
            failures.append(f"charge action {number} escaped group 61019")
        if {(round(row['sx'], 9), round(row['sy'], 9)) for row in rows} != {(SX, SY)}:
            failures.append(f"charge action {number} has AIR scale drift")
        expected_frame = 3 if number in (510, 10510, 20510) else 0
        # Multiple rows are allowed when they repeat one approved drawing for
        # subtle offset-only breathing; identity must never change mid-charge.
        if not rows or {row["frame"] for row in rows} != {expected_frame}:
            failures.append(f"charge action {number} swaps body sprites: {rows}")

    # Character-wide dynamic AngleDraw scaling must never affect the root body.
    state = None
    root_scale_controllers = []
    lines = cns.splitlines()
    for index, raw in enumerate(lines):
        found = re.match(r"\s*\[\s*statedef\s+(-?\d+)\s*\]", raw, re.I)
        if found:
            state = int(found.group(1))
        if not re.match(r"(?i)^\s*type\s*=\s*angledraw\b", raw):
            continue
        block = "\n".join(lines[index:index + 10])
        if re.search(r"(?im)^\s*scale\s*=", block) and not re.search(r"(?im)^\s*triggerall\s*=\s*ishelper\b", block):
            root_scale_controllers.append({"state": state, "line": index + 1})
    if root_scale_controllers:
        failures.append(f"root AngleDraw scale controllers remain: {root_scale_controllers}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "character_scale": list(scale) if scale else None,
        "actions": report_actions,
        "root_dynamic_scale_controllers": root_scale_controllers,
        "failures": failures,
    }
    target = ART / "audit.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "failures": failures, "report": str(target)}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
