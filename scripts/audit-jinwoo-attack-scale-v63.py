"""Verify effect helpers are bodyless and weapon attacks match punch stature."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/attack-scale-v63/audit.json"
DAGGER_SCALE = (0.167301691, 0.157831784)


def state(text: str, number: int) -> str:
    match = re.search(rf"(?ims)^\[Statedef\s+{number}\].*?(?=^\[Statedef\s+|\Z)", text)
    return match.group(0) if match else ""


def main() -> None:
    failures: list[str] = []
    air_text = (LIVE / "anim.air").read_text(encoding="latin1")
    config = (LIVE / "config.cns").read_text(encoding="latin1")
    shadows = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    sff = Sff(LIVE / "spr.sff")

    for number, text in ((879810, shadows), (98010, config), (30850, config)):
        block = state(text, number)
        if not block or not re.search(r"(?im)^\s*anim\s*=\s*99950\s*$", block):
            failures.append(f"VFX helper {number} can render a Jinwoo body")
        if "flag=invisible" not in block.replace(" ", ""):
            failures.append(f"VFX helper {number} lacks an immediate invisibility guard")

    rows = []
    for raw in air_text.splitlines():
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0]), int(fields[1])
        except ValueError:
            continue
        if group != 61016:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        rows.append((frame, sx, sy))
        if (round(sx, 9), round(sy, 9)) != DAGGER_SCALE:
            failures.append(f"dagger frame {frame} has attack-scale drift: {(sx, sy)}")

    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    char_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    char_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))

    def world_height(key: tuple[int, int], sy: float) -> float:
        box = sff.decode(sff.keys[key]).convert("RGBA").getchannel("A").getbbox()
        return (box[3] - box[1]) * sy * char_y

    punch_height = world_height((61013, 24), 0.096128000)
    dagger_standing = [world_height((61016, frame), DAGGER_SCALE[1]) for frame in (0, 1, 2)]
    ratios = [value / punch_height for value in dagger_standing]
    if any(not 0.96 <= ratio <= 1.02 for ratio in ratios):
        failures.append(f"standing dagger body does not match punch stature: {ratios}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "bodyless_vfx_helpers": [879810, 98010, 30850],
        "dagger_rows": len(rows),
        "punch_reference_height": round(punch_height, 3),
        "dagger_standing_heights": [round(value, 3) for value in dagger_standing],
        "ratios_to_punch": [round(value, 3) for value in ratios],
        "failures": failures,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
