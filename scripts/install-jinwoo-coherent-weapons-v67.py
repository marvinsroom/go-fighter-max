"""Rebuild archived sword routes as coherent, non-looping v52 sequences."""
from __future__ import annotations

import json
import math
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/coherent-weapons-v67"
SOURCE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/weapon-exclusivity-v66/anim.before-v66.air"
AIR = LIVE / "anim.air"
SX, SY = 0.208072691, 0.196294992


def sequence(base: int) -> list[int]:
    if base in (0, 5, 6): return [0]
    if base in (10, 11, 12): return [5]
    if base == 20: return [1, 2]
    if base == 21: return [2, 1]
    if base in (40, 41, 42, 43, 44, 45, 47, 50, 52): return [4]
    if base in (100, 105): return [3, 6]
    if base in (500, 501, 510): return [6]
    if base in (600, 610, 620, 630, 640, 650): return [4, 7, 9, 11, 6]
    if base in (260, 400, 410, 420, 460): return [5, 10, 11, 6]
    # One cinematic arc, never modulo-looped inside a long imported action.
    return [0, 7, 8, 9, 10, 11, 6]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file(): raise RuntimeError("missing pre-v66 AIR recovery source")
    current_backup = ART / "anim.before-v67.air"
    if not current_backup.exists(): shutil.copy2(AIR, current_backup)
    text = SOURCE.read_text(encoding="latin1")
    matches = list(re.finditer(r"(?ims)^\[Begin Action\s+(-?\d+)\].*?(?=^\[Begin Action|\Z)",text))
    output=[];cursor=0;rows_changed=0;actions_changed=[];action_sequences={}
    for match in matches:
        action=int(match.group(1))
        if not 500000<=action<=529999: continue
        raw_lines=match.group(0).splitlines()
        old_indices=[]
        for index,raw in enumerate(raw_lines):
            fields=raw.split(",")
            try: group=int(fields[0].strip())
            except (ValueError,IndexError): continue
            if group==61011: old_indices.append(index)
        if not old_indices: continue
        seq=sequence(action%10000); count=len(old_indices); chosen=[]
        for ordinal,line_index in enumerate(old_indices):
            # Centered bucket sampling distributes long holds evenly without
            # ever wrapping back to the beginning of the attack.
            pose=seq[min(len(seq)-1, math.floor((ordinal+.5)*len(seq)/count))]
            fields=raw_lines[line_index].split(",")
            while len(fields)<9:fields.append("")
            fields[0],fields[1]=str(61017),str(pose)
            fields[7],fields[8]=f"{SX:.9f}",f"{SY:.9f}"
            raw_lines[line_index]=",".join(fields);chosen.append(pose)
        replacement="\n".join(raw_lines)+( "\n" if match.group(0).endswith("\n") else "")
        output.append(text[cursor:match.start()]);output.append(replacement);cursor=match.end()
        rows_changed+=count;actions_changed.append(action);action_sequences[str(action)]=chosen
    output.append(text[cursor:]); rebuilt="".join(output)
    if rows_changed!=1085: raise RuntimeError(f"expected 1085 archived rows, rebuilt {rows_changed}")
    pending=ART/"anim.v67.pending.air";pending.write_text(rebuilt,encoding="latin1",newline="")
    try:pending.replace(AIR)
    except (OSError,PermissionError):shutil.copy2(pending,AIR);pending.unlink()
    report={"status":"INSTALLED","source":"pre-v66 AIR","rows_rebuilt":rows_changed,
            "actions_rebuilt":len(actions_changed),"action_sequences":action_sequences}
    (ART/"installation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"INSTALLED","rows_rebuilt":rows_changed,"actions_rebuilt":len(actions_changed)},indent=2))


if __name__=="__main__":main()
