"""Normalize jump, intro, and transformation scale around the v64 human baseline."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/full-pose-scale-v65"
AIR, CNS = LIVE / "anim.air", LIVE / "cns.cns"
TARGET = 50.4
CHAR_X, CHAR_Y = 1.39, 1.07
JUMP_ACTIONS = (40, 41, 42, 43, 44, 45, 47, 50, 52)


def block(text: str, action: int) -> re.Match[str]:
    found = re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)", text)
    if not found:
        raise RuntimeError(f"missing action {action}")
    return found


def rewrite_rows(source: str, scales: dict[tuple[int, int], tuple[float, float]]) -> tuple[str, int]:
    output, changed = [], 0
    for raw in source.splitlines():
        fields = raw.split(",")
        try:
            key = (int(fields[0].strip()), int(fields[1].strip()))
        except (ValueError, IndexError):
            output.append(raw)
            continue
        if key in scales:
            while len(fields) < 9:
                fields.append("")
            sx, sy = scales[key]
            fields[7], fields[8] = f"{sx:.9f}", f"{sy:.9f}"
            raw = ",".join(fields)
            changed += 1
        output.append(raw)
    return "\n".join(output) + ("\n" if source.endswith("\n") else ""), changed


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "live-before-v65"
    if not backup.exists():
        backup.mkdir()
        shutil.copy2(AIR, backup / AIR.name)
        shutil.copy2(CNS, backup / CNS.name)
    sff = Sff(LIVE / "spr.sff")

    def bbox(key: tuple[int, int]) -> tuple[int, int]:
        bounds = sff.decode(sff.keys[key]).convert("RGBA").getchannel("A").getbbox()
        return bounds[2] - bounds[0], bounds[3] - bounds[1]

    # Jump frames are curled/horizontal, so normalize the longest rendered
    # silhouette dimension rather than incorrectly forcing upright height.
    jump_scales = {}
    jump_metrics = []
    base_sx, base_sy = 0.094372063, 0.089030246
    for frame in range(6):
        key = (61023, frame)
        width, height = bbox(key)
        factor = TARGET / max(width * base_sx * CHAR_X, height * base_sy * CHAR_Y)
        jump_scales[key] = (base_sx * factor, base_sy * factor)
        jump_metrics.append({"frame": frame, "factor": round(factor, 5),
                             "scale": [round(base_sx * factor, 9), round(base_sy * factor, 9)]})

    # Intro exchange and the human side of every summon transformation use
    # the current v48 casting body, normalized per drawing to the same height.
    cast_scales = {}
    for frame in (0, 1, 2):
        width, height = bbox((61018, frame))
        sy = TARGET / (height * CHAR_Y)
        sx = sy * (0.095218974 / 0.089829218)
        cast_scales[(61018, frame)] = (sx, sy)

    text = AIR.read_text(encoding="latin1")
    changed = 0
    for action in JUMP_ACTIONS + (878500,):
        found = block(text, action)
        replacement, count = rewrite_rows(found.group(0), jump_scales if action in JUMP_ACTIONS else cast_scales)
        text = text[:found.start()] + replacement + text[found.end():]
        changed += count

    # Replace archived transformation art while preserving its timing.
    transform = """[Begin Action 870200]
Clsn2Default: 1
Clsn2[0] = -12,-59,12,0
61018,0,0,0,18,,,{sx0:.9f},{sy0:.9f}
61018,1,0,0,12,,,{sx1:.9f},{sy1:.9f}
61018,2,0,0,12,,,{sx2:.9f},{sy2:.9f}
""".format(
        sx0=cast_scales[(61018, 0)][0], sy0=cast_scales[(61018, 0)][1],
        sx1=cast_scales[(61018, 1)][0], sy1=cast_scales[(61018, 1)][1],
        sx2=cast_scales[(61018, 2)][0], sy2=cast_scales[(61018, 2)][1],
    )
    found = block(text, 870200)
    text = text[:found.start()] + transform + text[found.end():]

    pending = ART / "anim.v65.pending.air"
    pending.write_text(text, encoding="latin1", newline="")
    try:
        pending.replace(AIR)
    except (OSError, PermissionError):
        shutil.copy2(pending, AIR)
        pending.unlink()

    cns = CNS.read_text(encoding="latin1")
    intro = re.search(r"(?ims)^\[Statedef 191\].*?(?=^\[Statedef|\Z)", cns)
    if not intro:
        raise RuntimeError("missing intro state 191")
    intro_block = intro.group(0)
    helper = re.search(r'(?ims)^\[State 191, Shadow scout enters first\].*?(?=^\[State|^\[Statedef|\Z)', intro_block)
    if not helper:
        raise RuntimeError("missing intro scout helper")
    helper_block = re.sub(r"(?im)^\s*size\.xscale\s*=.*$", "size.xscale=1.0", helper.group(0))
    helper_block = re.sub(r"(?im)^\s*size\.yscale\s*=.*$", "size.yscale=1.0", helper_block)
    intro_block = intro_block[:helper.start()] + helper_block + intro_block[helper.end():]
    cns = cns[:intro.start()] + intro_block + cns[intro.end():]
    CNS.write_text(cns, encoding="latin1", newline="")

    report = {"status": "INSTALLED", "target_human_dimension": TARGET,
              "jump_rows_normalized": changed, "jump_frames": jump_metrics,
              "transform_action": 870200, "intro_exchange_action": 878500,
              "intro_summon_helper_scale": 1.0}
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
