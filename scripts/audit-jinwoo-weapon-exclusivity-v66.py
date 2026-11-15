"""Fail if active weapon actions render archived or cross-weapon Jinwoo bodies."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/weapon-exclusivity-v66/audit.json"
BODY_GROUPS = set(range(61011, 61025))


def main() -> None:
    text = (LIVE / "anim.air").read_text(encoding="latin1")
    failures=[]; summary={}; archived=[]
    for low, high, label, approved in ((500000,529999,"sword",{61017,61021}),
                                       (700000,729999,"dagger",{61016})):
        actions=0; rows=0; groups=Counter(); wrong=[]
        for match in re.finditer(r"(?ims)^\[Begin Action\s+(-?\d+)\].*?(?=^\[Begin Action|\Z)",text):
            action=int(match.group(1))
            if not low<=action<=high: continue
            actions+=1
            for group in map(int,re.findall(r"(?m)^\s*(-?\d+)\s*,\s*-?\d+\s*,",match.group(0))):
                if group not in BODY_GROUPS: continue
                rows+=1; groups[group]+=1
                if group not in approved: wrong.append([action,group])
                if group==61011: archived.append([action,group])
        summary[label]={"actions":actions,"body_rows":rows,"groups":dict(groups),"wrong_rows":wrong[:30]}
        if wrong: failures.append(f"{label} actions contain {len(wrong)} cross-bank/archived body rows")
    # Direct Antares supers are intentionally outside the 700xxx clone range.
    for action in (3200,3210,3220):
        match=re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)",text)
        groups=set(map(int,re.findall(r"(?m)^\s*(-?\d+)\s*,\s*-?\d+\s*,",match.group(0) if match else ""))) & BODY_GROUPS
        if groups!={61016}: failures.append(f"Antares action {action} escaped dagger bank: {groups}")
    if archived: failures.append(f"archived group 61011 remains in weapon routes: {archived[:20]}")
    report={"status":"PASS" if not failures else "FAIL","weapon_ranges":summary,
            "archived_rows":len(archived),"failures":failures}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2));raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":main()
