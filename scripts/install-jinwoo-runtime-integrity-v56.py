"""Repair invalid AIR references and remove frozen-looking Jinwoo ultimates."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/runtime-integrity-v56"
AIR = LIVE / "anim.air"
SHADOWS = LIVE / "our-shadows.cns"
BACKUP = ART / "live-before-runtime-integrity-v56"
REPORT = ART / "installation.json"
MARKER = "; JINWOO V48 RUNTIME INTEGRITY V56"
SX, SY = 0.095218974, 0.089829218

# These source images are absent from the live SFF. Preserve the owning
# animation's intent with the closest valid phase instead of letting Ikemen
# display nothing (and repeatedly warn at runtime).
MISSING_KEY_REPAIRS = {
    (61001, 50): (61001, 33),
    (61001, 51): (61001, 34),
    (61001, 52): (61001, 35),
    (61001, 260): (61001, 24),
    (61001, 261): (61001, 26),
    (61001, 36): (61001, 35),
    (61001, 37): (61001, 35),
    (2045, 8): (2045, 7),
    (7012, 5): (7012, 4),
    (30500, 8): (30500, 7),
    (30802, 13): (30802, 9),
    (30802, 15): (30802, 11),
    (30802, 17): (30802, 9),
    (30802, 19): (30802, 11),
}


def action_match(text: str, number: int) -> re.Match[str]:
    found = re.search(
        rf"(?ims)^\[Begin Action\s+{number}\][ \t]*\r?\n.*?(?=^\[Begin Action\s+-?\d+\][ \t]*\r?\n|\Z)",
        text,
    )
    if not found:
        raise RuntimeError(f"missing AIR action {number}")
    return found


def replace_action(text: str, number: int, body: str) -> str:
    found = action_match(text, number)
    return text[:found.start()] + body.rstrip() + "\n\n" + text[found.end():]


def rows_action(number: int, group: int, frames: list[int], total: int, step: int = 10) -> str:
    """Build a moving body cycle whose exact duration still matches state logic."""
    durations = [step] * (total // step)
    if total % step:
        durations.append(total % step)
    lines = [
        f"[Begin Action {number}]",
        "Clsn2Default: 1",
        "Clsn2[0] = -12,-59,12,0",
    ]
    for index, duration in enumerate(durations):
        frame = frames[index % len(frames)]
        scale = f",,,{SX:.9f},{SY:.9f}" if group in (61016, 61021) else ""
        lines.append(f"{group},{frame},0,0,{duration}{scale}")
    return "\n".join(lines)


def repair_missing_rows(text: str) -> tuple[str, int]:
    changed = 0
    output = []
    for raw in text.splitlines():
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) >= 2:
            try:
                key = (int(fields[0].strip()), int(fields[1].strip()))
            except ValueError:
                key = None
            if key in MISSING_KEY_REPAIRS:
                new_group, new_frame = MISSING_KEY_REPAIRS[key]
                prefix = raw[: len(raw) - len(raw.lstrip())]
                fields[0], fields[1] = str(new_group), str(new_frame)
                raw = prefix + ",".join(part.strip() for part in fields)
                changed += 1
        output.append(raw)
    return "\n".join(output) + "\n", changed


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    force = "--force" in sys.argv
    original = AIR.read_text(encoding="latin1")
    if MARKER in original and not force:
        print(REPORT.read_text(encoding="utf-8"))
        return
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        shutil.copy2(AIR, BACKUP / AIR.name)
        shutil.copy2(SHADOWS, BACKUP / SHADOWS.name)

    rewritten, repaired = repair_missing_rows(original)
    # Group 30206 was wholly removed from the SFF. Reuse the intact adjacent
    # eight-phase VFX bank; this is an effect animation, never Jinwoo's body.
    effect = "[Begin Action 30206]\n" + "\n".join(
        f"30300,{min(frame, 6)},0,0,1,,S" for frame in range(8)
    )
    rewritten = replace_action(rewritten, 30206, effect)

    # Preserve all state deadlines while ensuring no body image is held longer
    # than ten ticks. This removes the 98-190 tick visual freezes in supers.
    specs = {
        3000: (61021, [0, 1, 2, 1], 150),
        3100: (61021, [0, 1, 2, 1], 150),
        13100: (61021, [0, 1, 2, 1], 150),
        23100: (61021, [0, 1, 2, 1], 150),
        503100: (61021, [0, 1, 2, 1], 150),
        513100: (61021, [0, 1, 2, 1], 150),
        523100: (61021, [0, 1, 2, 1], 150),
        3120: (61021, [3, 4, 5, 4], 245),
        13120: (61021, [3, 4, 5, 4], 245),
        23120: (61021, [3, 4, 5, 4], 245),
        503120: (61021, [3, 4, 5, 4], 245),
        513120: (61021, [3, 4, 5, 4], 245),
        523120: (61021, [3, 4, 5, 4], 245),
        3200: (61016, [8, 9, 10, 11, 7], 145),
        3210: (61016, [8, 9, 10, 11, 7], 300),
        3220: (61016, [10, 11, 9, 8], 240),
    }
    for number, (group, frames, total) in specs.items():
        rewritten = replace_action(rewritten, number, rows_action(number, group, frames, total))
    AIR.write_text(rewritten.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    # Transform states already have explicit recovery; make that recovery
    # independent of animation completion and fast enough to avoid a lock-up.
    shadows = SHADOWS.read_text(encoding="latin1")
    updated = shadows
    for state in range(870201, 870207):
        match = re.search(
            rf"(?ims)(^\[Statedef\s+{state}\].*?)(?=^\[Statedef\s+\d+\]|\Z)", updated
        )
        if not match:
            raise RuntimeError(f"missing transform state {state}")
        block = re.sub(r"(?im)^trigger1\s*=\s*time\s*>=\s*41\s*$", "trigger1 = time >= 36", match.group(1), count=1)
        updated = updated[:match.start()] + block + updated[match.end():]
    SHADOWS.write_text(updated, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "repaired_missing_rows": repaired + 8,
        "retimed_actions": sorted(specs),
        "maximum_body_hold_ticks": 10,
        "transform_states_with_36_tick_watchdog": list(range(870201, 870207)),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
