"""Remove miniature VFX-helper bodies and normalize Antares attack scale."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/attack-scale-v63"
AIR = LIVE / "anim.air"
CONFIG = LIVE / "config.cns"
SHADOWS = LIVE / "our-shadows.cns"
DAGGER_SX, DAGGER_SY = 0.167301691, 0.157831784
OLD_SX, OLD_SY = 0.095218974, 0.089829218


def hide_helper_body(text: str, state: int) -> tuple[str, int]:
    match = re.search(rf"(?ims)^\[Statedef\s+{state}\].*?(?=^\[Statedef\s+|\Z)", text)
    if not match:
        raise RuntimeError(f"missing helper state {state}")
    block = match.group(0)
    block, count = re.subn(r"(?im)^\s*anim\s*=.*$", "anim=99950", block, count=1)
    if not count:
        raise RuntimeError(f"helper state {state} has no default animation")
    marker = f"[State {state}, V63 no miniature Jinwoo]"
    if marker not in block:
        header_end = block.find("\n") + 1
        guard = (
            f"{marker}\n"
            "type=AssertSpecial\n"
            "trigger1=1\n"
            "flag=invisible\n"
            "ignorehitpause=1\n\n"
        )
        block = block[:header_end] + guard + block[header_end:]
    return text[:match.start()] + block + text[match.end():], count


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "live-before-v63"
    if not backup.exists():
        backup.mkdir()
        for source in (AIR, CONFIG, SHADOWS):
            shutil.copy2(source, backup / source.name)

    air = AIR.read_text(encoding="latin1")
    pattern = re.compile(
        rf"(?m)^(\s*61016\s*,[^\r\n]*?,,,){OLD_SX:.9f},{OLD_SY:.9f}\s*$"
    )
    air, dagger_rows = pattern.subn(rf"\g<1>{DAGGER_SX:.9f},{DAGGER_SY:.9f}", air)
    if dagger_rows < 3:
        raise RuntimeError(f"expected underscaled dagger rows, found {dagger_rows}")
    AIR.write_text(air, encoding="latin1", newline="")

    config = CONFIG.read_text(encoding="latin1")
    config, _ = hide_helper_body(config, 98010)
    config, _ = hide_helper_body(config, 30850)
    CONFIG.write_text(config, encoding="latin1", newline="")

    shadows = SHADOWS.read_text(encoding="latin1")
    shadows, _ = hide_helper_body(shadows, 879810)
    SHADOWS.write_text(shadows, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "dagger_rows_corrected": dagger_rows,
        "dagger_scale": [DAGGER_SX, DAGGER_SY],
        "invisible_vfx_helpers": [879810, 98010, 30850],
        "punch_reference": [61013, 24],
    }
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
