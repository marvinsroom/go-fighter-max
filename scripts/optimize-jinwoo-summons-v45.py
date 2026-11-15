"""Reduce Tusk/Kaisel decode memory without changing their in-game size."""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
SOURCE = ART / "tusk-kaisel-restyle-v32"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/summon-memory-v45"
BACKUP = OUT / "live-before-v45"
AIR = LIVE / "anim.air"
SFF_PATH = LIVE / "spr.sff"
MARKER = "; JINWOO SUMMON MEMORY FIX V45"
FACTOR = 4

TUSK = {
    20: ("tusk-neutral-normalized-v32.png", (768, 1236)),
    21: ("tusk-charge-normalized-v32.png", (768, 1236)),
    22: ("tusk-recovery-normalized-v32.png", (768, 1236)),
    222: ("tusk-release-normalized-v32.png", (768, 1236)),
}
KAISEL = {
    27: ("kaisel-flight-up-27-normalized-v32.png", (1024, 1344)),
    28: ("kaisel-flight-down-28-normalized-v32.png", (1024, 1344)),
    29: ("kaisel-attack-dive-29-normalized-v32.png", (1024, 1344)),
    30: ("kaisel-flight-up-30-normalized-v32.png", (1024, 1344)),
    31: ("kaisel-flight-down-31-normalized-v32.png", (1024, 1344)),
    32: ("kaisel-attack-dive-32-normalized-v32.png", (1024, 1344)),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packed(path: Path, axis: tuple[int, int]) -> tuple[dict, dict]:
    original = Image.open(path).convert("RGBA")
    size = (original.width // FACTOR, original.height // FACTOR)
    image = original.resize(size, Image.Resampling.LANCZOS)
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    scaled_axis = (axis[0] // FACTOR, axis[1] // FACTOR)
    frame = {"image": image, "png": payload.getvalue(), "axis": scaled_axis,
             "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}
    detail = {"source": path.name, "source_size": list(original.size),
              "packed_size": list(size), "axis": list(scaled_axis),
              "decoded_bytes": size[0] * size[1] * 4}
    return frame, detail


def rescale_summon_rows(text: str) -> tuple[str, int]:
    tusk_numbers = set(TUSK)
    kaisel_numbers = set(KAISEL)
    changed = 0
    output: list[str] = []
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) >= 9:
            try:
                group = int(parts[0].strip())
                number = int(parts[1].strip())
            except ValueError:
                group = number = -1
            if group == 1000 and number in tusk_numbers:
                parts[7] = "0.300000000"
                parts[8] = "0.300000000"
                line = ",".join(parts)
                changed += 1
            elif group == 1000 and number in kaisel_numbers:
                parts[7] = "0.240000000"
                parts[8] = "0.240000000"
                line = ",".join(parts)
                changed += 1
        output.append(line)
    return "\n".join(output).rstrip() + "\n\n" + MARKER + "\n", changed


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air = AIR.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8"))
        return

    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name)
    shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)
    before_size = SFF_PATH.stat().st_size

    sff = Sff(SFF_PATH)
    replacements: dict[tuple[int, int], dict] = {}
    details: dict[str, dict] = {}
    for number, (name, axis) in {**TUSK, **KAISEL}.items():
        frame, detail = packed(SOURCE / name, axis)
        replacements[(1000, number)] = frame
        details[f"1000,{number}"] = detail
    missing = sorted(set(replacements) - set(sff.keys))
    if missing:
        raise RuntimeError(f"missing live summon sprite keys: {missing}")
    SFF_PATH.write_bytes(sff.derive(replacements, {}))

    air, changed_rows = rescale_summon_rows(air)
    if changed_rows < 10:
        raise RuntimeError(f"unexpectedly few summon rows rescaled: {changed_rows}")
    AIR.write_text(air, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "revision": "summon-memory-v45",
        "changed_animation_rows": changed_rows,
        "sff_bytes_before": before_size,
        "sff_bytes_after": SFF_PATH.stat().st_size,
        "summon_frames": details,
        "visual_size_policy": "quarter raster dimensions with four-times AIR scale",
        "runtime_sha256": {"anim.air": sha(AIR), "spr.sff": sha(SFF_PATH)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
