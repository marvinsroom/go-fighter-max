"""Install canonical bare-hand normals into an isolated sprite group."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/bare-hands-v47"
SOURCE, NORMALIZED = ART / "generated", ART / "normalized"
OUT, BACKUP = ART / "install", ART / "install/live-before-v47"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
MARKER = "; JINWOO CANONICAL BARE HANDS V47"
GROUP = 61012
CANONICAL_HEIGHT = 43.657
X_RATIO = 0.032913216 / 0.031050203
TARGET_ACTIONS = {200, 210, 220, 260, 300, 310, 320, 350}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame_data(number: int, sff: Sff) -> tuple[dict, dict]:
    original_index = sff.keys[(61011, number)]
    original = sff.decode(original_index).convert("RGBA")
    old_box = original.getchannel("A").getbbox()
    old_axis = sff.headers[original_index][4:6]

    image = Image.open(SOURCE / f"bare-v47-{number}.png").convert("RGBA")
    image = image.resize((512, 512), Image.Resampling.LANCZOS)
    box = image.getchannel("A").getbbox()
    if not old_box or not box:
        raise RuntimeError(f"empty sprite {number}")
    rx = (old_axis[0] - old_box[0]) / (old_box[2] - old_box[0])
    ry = (old_axis[1] - old_box[1]) / (old_box[3] - old_box[1])
    axis = (round(box[0] + rx * (box[2] - box[0])), round(box[1] + ry * (box[3] - box[1])))
    sy = CANONICAL_HEIGHT / (box[3] - box[1])
    sx = sy * X_RATIO
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    image.save(NORMALIZED / f"bare-v47-{number}.png", optimize=True)
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    packed = {"image": image, "png": payload.getvalue(), "axis": axis,
              "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}
    detail = {"source_key": [61011, number], "target_key": [GROUP, number],
              "axis": list(axis), "bbox": list(box), "scale": [sx, sy],
              "world_height": round((box[3] - box[1]) * sy, 3)}
    return packed, detail


def rewrite_actions(text: str, scales: dict[int, tuple[float, float]]) -> tuple[str, int]:
    current = None
    changed = 0
    output = []
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            current = int(match.group(1))
        parts = line.split(",")
        if current in TARGET_ACTIONS and len(parts) >= 9:
            try:
                group, number = int(parts[0].strip()), int(parts[1].strip())
            except ValueError:
                group = number = -1
            if group == 61011 and number in scales:
                sx, sy = scales[number]
                parts[0] = str(GROUP)
                parts[7] = f"{sx:.9f}"
                parts[8] = f"{sy:.9f}"
                line = ",".join(parts)
                changed += 1
        output.append(line)
    return "\n".join(output).rstrip() + "\n\n" + MARKER + "\n", changed


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air = AIR.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8")); return
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AIR, BACKUP / AIR.name)
    shutil.copy2(SFF_PATH, BACKUP / SFF_PATH.name)

    sff = Sff(SFF_PATH)
    additions = {}
    details = {}
    scales = {}
    for number in range(8):
        packed, detail = frame_data(number, sff)
        additions[(GROUP, number)] = packed
        details[str(number)] = detail
        scales[number] = tuple(detail["scale"])
    SFF_PATH.write_bytes(sff.derive({}, additions))
    air, changed = rewrite_actions(air, scales)
    if changed < 20:
        raise RuntimeError(f"unexpected bare-hand AIR row count: {changed}")
    AIR.write_text(air, encoding="latin1", newline="")

    report = {"status": "INSTALLED", "revision": "bare-hands-v47",
              "target_group": GROUP, "rewritten_rows": changed,
              "actions": sorted(TARGET_ACTIONS), "frames": details,
              "runtime_sha256": {"anim.air": sha(AIR), "spr.sff": sha(SFF_PATH)},
              "backup": str(BACKUP.relative_to(ROOT))}
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
