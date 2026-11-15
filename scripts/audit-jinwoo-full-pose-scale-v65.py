"""Pose-aware scale audit for human, jump, intro, and transformed summons."""
from __future__ import annotations

import json
import re
import statistics
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/full-pose-scale-v65/audit.json"
TARGET = 50.4


def actions(text: str) -> dict[int, list[tuple[int, int, float, float]]]:
    result = {}; current = None
    for raw in text.splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); result.setdefault(current, []); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2: continue
        try: group, frame = int(fields[0]), int(fields[1])
        except ValueError: continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result[current].append((group, frame, sx, sy))
    return result


def main() -> None:
    bank = actions((LIVE / "anim.air").read_text(encoding="latin1"))
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    char_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    char_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))
    sff = Sff(LIVE / "spr.sff"); failures = []

    def dims(row):
        group, frame, sx, sy = row
        image = sff.decode(sff.keys[(group, frame)]).convert("RGBA")
        box = image.getchannel("A").getbbox()
        if group == 61023:
            rgba = np.asarray(image, dtype=np.uint16)
            r, g, b, a = (rgba[:, :, index] for index in range(4))
            purple = (b > g * 1.22 + 12) & (r > g * 1.12 + 8) & (b > 55)
            ys, xs = np.where((a >= 32) & ~purple)
            if len(xs):
                box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
        return (box[2]-box[0])*sx*char_x, (box[3]-box[1])*sy*char_y

    jump_actions = (40,41,42,43,44,45,47,50,52)
    jump_rows = [row for action in jump_actions for row in bank.get(action, [])]
    if not jump_rows or {row[0] for row in jump_rows} != {61023}:
        failures.append("jump actions escaped the approved 61023 bank")
    jump_longest = [max(dims(row)) for row in jump_rows]
    if any(not 0.98*TARGET <= value <= 1.02*TARGET for value in jump_longest):
        failures.append(f"jump body length drift: {jump_longest}")

    cast = {}
    for action in (870200, 878500):
        rows = bank.get(action, [])
        heights = [dims(row)[1] for row in rows]
        cast[str(action)] = [round(value, 3) for value in heights]
        if not rows or {row[0] for row in rows} != {61018} or any(not .98*TARGET <= value <= 1.02*TARGET for value in heights):
            failures.append(f"human transform/intro action {action} has scale drift")

    intro = re.search(r"(?ims)^\[Statedef 191\].*?(?=^\[Statedef|\Z)", cns)
    helper = re.search(r'(?ims)^\[State 191, Shadow scout enters first\].*?(?=^\[State|^\[Statedef|\Z)', intro.group(0) if intro else "")
    helper_scale = []
    if helper:
        helper_scale = [float(value) for value in re.findall(r"(?im)^\s*size\.[xy]scale\s*=\s*([0-9.]+)", helper.group(0))]
    if helper_scale != [1.0, 1.0]:
        failures.append(f"intro summon has stacked scale: {helper_scale}")
    scout_heights = [dims(row)[1] for row in bank.get(878511, [])]
    scout_ratio = statistics.median(scout_heights) / TARGET if scout_heights else 0
    if not 1.3 <= scout_ratio <= 1.6:
        failures.append(f"intro summon authored ratio is implausible: {scout_ratio}")

    form_actions = (870300,870400,870500,870600,879805,879806)
    form_medians = {str(action): round(statistics.median(dims(row)[1] for row in bank[action]),3) for action in form_actions}
    if any(value < TARGET*1.1 for value in form_medians.values()):
        failures.append(f"a transformed summon is smaller than the human baseline: {form_medians}")

    report = {"status":"PASS" if not failures else "FAIL", "human_target":TARGET,
              "jump_longest_dimension_range":[round(min(jump_longest),3),round(max(jump_longest),3)],
              "human_cast_heights":cast, "intro_helper_scale":helper_scale,
              "intro_summon_height_ratio":round(scout_ratio,3), "transformed_form_median_heights":form_medians,
              "failures":failures}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2)); raise SystemExit(0 if not failures else 1)


if __name__ == "__main__": main()
