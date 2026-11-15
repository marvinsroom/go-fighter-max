"""Lock Jinwoo's runtime proportions and remove pose-to-pose size pops."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/scale-lock-v55"
AIR = LIVE / "anim.air"
CNS = LIVE / "cns.cns"
BACKUP = ART / "live-before-scale-lock-v55"
REPORT = ART / "installation.json"
MARKER = "; JINWOO V48 SCALE LOCK V55"
SX, SY = 0.095218974, 0.089829218
CHARACTER_XSCALE = 1.39
CHARACTER_YSCALE = 1.07

# Crouching attacks previously started on a low pose and then jumped into the
# upright punch bank. Keep every frame in the same crouched body family.
CROUCH_ACTIONS = {
    400: ([12, 12, 17, 16, 17, 12, 12, 12], [3, 3, 5, 5, 5, 4, 4, 7]),
    410: ([12, 17, 16, 17, 12, 12], [3, 4, 5, 5, 4, 7]),
    420: ([12, 17, 16, 17, 16, 17, 12, 12], [3, 4, 5, 5, 5, 5, 4, 8]),
    460: ([12, 13, 14, 16, 12], [3, 3, 4, 5, 8]),
}

CHARGE_ACTIONS = {
    # Never swap the character body while the button is held. The integrated
    # System screens remain visible without making Jinwoo jitter between poses.
    500: ([0], [-1], False),
    10500: ([0], [-1], False),
    20500: ([0], [-1], False),
    501: ([0], [5], False),
    10501: ([0], [5], False),
    20501: ([0], [5], False),
    # Full charge is one deliberate stronger silhouette, not another loop.
    510: ([3], [20], False),
    10510: ([3], [20], False),
    20510: ([3], [20], False),
}


def action_block(text: str, number: int) -> tuple[re.Match[str], str]:
    pattern = re.compile(
        rf"(?ims)^\[Begin Action\s+{number}\][ \t]*\r?\n.*?(?=^\[Begin Action\s+-?\d+\][ \t]*\r?\n|\Z)"
    )
    found = pattern.search(text)
    if not found:
        raise RuntimeError(f"missing AIR action {number}")
    return found, found.group(0)


def replace_sprite_rows(block: str, group: int, frames: list[int], times: list[int]) -> str:
    cursor = 0
    output = []
    for raw in block.splitlines():
        fields = raw.split(";", 1)[0].split(",")
        is_row = False
        if len(fields) >= 2:
            try:
                int(fields[0].strip()); int(fields[1].strip()); is_row = True
            except ValueError:
                pass
        if is_row:
            if cursor >= len(frames):
                raise RuntimeError("replacement has fewer frames than the live action")
            while len(fields) < 9:
                fields.append("")
            fields[0] = str(group)
            fields[1] = str(frames[cursor])
            fields[4] = str(times[cursor])
            fields[7] = f"{SX:.9f}"
            fields[8] = f"{SY:.9f}"
            raw = ",".join(fields)
            cursor += 1
        output.append(raw)
    if cursor != len(frames):
        raise RuntimeError(f"replacement has {len(frames)} frames but live action has {cursor}")
    return "\n".join(output).rstrip() + "\n\n"


def charge_action(number: int, frames: list[int], times: list[int], loop: bool) -> str:
    lines = [f"[Begin Action {number}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
    if loop:
        lines.append("LoopStart")
    for frame, duration in zip(frames, times, strict=True):
        lines.append(f"61019,{frame},0,0,{duration},,,{SX:.9f},{SY:.9f}")
    return "\n".join(lines) + "\n\n"


def replace_action(text: str, number: int, replacement: str) -> str:
    found, _ = action_block(text, number)
    return text[:found.start()] + replacement + text[found.end():]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    force = "--force" in sys.argv
    air_text = AIR.read_text(encoding="latin1")
    if MARKER in air_text and not force:
        print(REPORT.read_text(encoding="utf-8"))
        return
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        shutil.copy2(AIR, BACKUP / AIR.name)
        shutil.copy2(CNS, BACKUP / CNS.name)

    rewritten = air_text
    for number, (frames, times) in CROUCH_ACTIONS.items():
        found, block = action_block(rewritten, number)
        replacement = replace_sprite_rows(block, 61013, list(frames), list(times))
        rewritten = rewritten[:found.start()] + replacement + rewritten[found.end():]
    for number, (frames, times, loop) in CHARGE_ACTIONS.items():
        rewritten = replace_action(rewritten, number, charge_action(number, list(frames), list(times), loop))
    # Replacing the final 20510 block can consume the older marker that sat
    # between it and the next action. Preserve installer idempotence explicitly.
    if "; JINWOO V48 PRESENTATION V53" not in rewritten:
        rewritten = rewritten.rstrip() + "\n\n; JINWOO V48 PRESENTATION V53\n"
    AIR.write_text(rewritten.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    cns_text = CNS.read_text(encoding="latin1")
    updated, count = re.subn(
        r"(?im)^(\s*xscale\s*=\s*)[0-9.]+\s*$",
        rf"\g<1>{CHARACTER_XSCALE:.2f}",
        cns_text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("could not lock the character-wide xscale")
    updated, y_count = re.subn(
        r"(?im)^(\s*yscale\s*=\s*)[0-9.]+\s*$",
        rf"\g<1>{CHARACTER_YSCALE:.2f}",
        updated,
        count=1,
    )
    if y_count != 1:
        raise RuntimeError("could not lock the character-wide yscale")
    updated = re.sub(
        r"(?im)^; Base art is already normalized.*\r?\n; Jinwoo.*\r?\n",
        "; V48 frames are normalized in AIR. Keep the character-wide transform\n"
        "; close to uniform so horizontal poses do not balloon across the screen.\n",
        updated,
        count=1,
    )
    CNS.write_text(updated, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "character_scale": [CHARACTER_XSCALE, CHARACTER_YSCALE],
        "air_scale": [SX, SY],
        "crouch_actions": sorted(CROUCH_ACTIONS),
        "charge_actions": sorted(CHARGE_ACTIONS),
        "static_charge_frame": 0,
        "full_charge_frame": 3,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
