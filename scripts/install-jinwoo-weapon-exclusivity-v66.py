"""Remove archived Jinwoo bodies from every active sword action."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/weapon-exclusivity-v66"
AIR = LIVE / "anim.air"
SWORD_GROUP = 61017
SWORD_SX, SWORD_SY = 0.194438745, 0.183432773


def poses(base: int) -> list[int]:
    if base == 500: return [6]
    if base == 501: return [7]
    if base in (0, 5, 6): return [0]
    if base in (10, 11, 12): return [5]
    if base == 20: return [1, 2]
    if base == 21: return [2, 1]
    if base in (40, 41, 42, 43, 44, 45, 47, 50, 52): return [4]
    if base == 100: return [3]
    if base == 105: return [7]
    if base in (260, 400, 410, 420, 460): return [5, 10, 11, 7]
    if base in (600, 610, 620, 630, 640, 650): return [4, 9, 11, 4]
    return [7, 8, 9, 10, 11, 7]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    backup = ART / "anim.before-v66.air"
    if not backup.exists(): shutil.copy2(AIR, backup)
    text = AIR.read_text(encoding="latin1")
    matches = list(re.finditer(r"(?ims)^\[Begin Action\s+(-?\d+)\].*?(?=^\[Begin Action|\Z)", text))
    output = []; cursor = 0; changed_rows = 0; changed_actions = []
    for match in matches:
        action = int(match.group(1))
        if not 500000 <= action <= 529999:
            continue
        body_poses = poses(action % 10000); body_index = 0; lines = []; action_changed = 0
        for raw in match.group(0).splitlines():
            fields = raw.split(",")
            try: group = int(fields[0].strip())
            except (ValueError, IndexError):
                lines.append(raw); continue
            if group == 61011:
                while len(fields) < 9: fields.append("")
                fields[0] = str(SWORD_GROUP)
                fields[1] = str(body_poses[body_index % len(body_poses)])
                fields[7], fields[8] = f"{SWORD_SX:.9f}", f"{SWORD_SY:.9f}"
                raw = ",".join(fields); body_index += 1; action_changed += 1
            lines.append(raw)
        if action_changed:
            replacement = "\n".join(lines) + ("\n" if match.group(0).endswith("\n") else "")
            output.append(text[cursor:match.start()]); output.append(replacement); cursor = match.end()
            changed_rows += action_changed; changed_actions.append(action)
    output.append(text[cursor:])
    if changed_rows < 1000:
        raise RuntimeError(f"expected comprehensive archived sword bank, found only {changed_rows} rows")
    pending = ART / "anim.v66.pending.air"
    pending.write_text("".join(output), encoding="latin1", newline="")
    try: pending.replace(AIR)
    except (OSError, PermissionError):
        shutil.copy2(pending, AIR); pending.unlink()
    report = {"status":"INSTALLED", "archived_group_removed":61011,
              "approved_sword_group":SWORD_GROUP, "rows_rewritten":changed_rows,
              "actions_rewritten":len(changed_actions), "action_numbers":changed_actions}
    (ART / "installation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:value for key,value in report.items() if key!="action_numbers"},indent=2))


if __name__ == "__main__": main()
