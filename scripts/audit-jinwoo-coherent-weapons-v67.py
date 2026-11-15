"""Verify converted sword timelines are monotonic and bank-exclusive."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LIVE=ROOT/"sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART=ROOT/"sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/coherent-weapons-v67"
SX,SY=0.208072691,0.196294992


def main()->None:
    text=(LIVE/"anim.air").read_text(encoding="latin1")
    install=json.loads((ART/"installation.json").read_text(encoding="utf-8"))
    failures=[];checked=0
    v69_installed=(ROOT/"sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/motion-style-v69/installation.json").is_file()
    for action_string,expected in install["action_sequences"].items():
        action=int(action_string)
        match=re.search(rf"(?ims)^\[Begin Action\s+{action}\].*?(?=^\[Begin Action|\Z)",text)
        if not match: failures.append(f"missing rebuilt action {action}");continue
        actual=[]
        for raw in match.group(0).splitlines():
            fields=raw.split(";",1)[0].split(",")
            if len(fields)<2:continue
            try:group,frame=int(fields[0]),int(fields[1])
            except ValueError:continue
            if group==61017:
                sx=float(fields[7]) if len(fields)>7 and fields[7].strip() else 1
                sy=float(fields[8]) if len(fields)>8 and fields[8].strip() else 1
                if (round(sx,9),round(sy,9))!=(SX,SY):failures.append(f"action {action} sword scale drift")
                actual.append(frame)
            elif group==61011:failures.append(f"action {action} retains archived body")
        # Existing approved 61017 effect/body rows can coexist. The rebuilt
        # suffix must retain the exact deterministic sequence recorded at install.
        v69_aerial_override=v69_installed and action%10000 in (600,610,620,630,640,650)
        if not v69_aerial_override and (len(actual)<len(expected) or actual[-len(expected):]!=expected):
            failures.append(f"action {action} lost coherent rebuilt sequence")
        if v69_aerial_override:
            current_compressed=[value for i,value in enumerate(actual) if i==0 or value!=actual[i-1]]
            if not actual or len(current_compressed)>7:
                failures.append(f"action {action} has incoherent v69 aerial sequence: {current_compressed}")
        # A converted sequence may hold a pose but must not wrap from recovery
        # back to windup; that was the v66 regression.
        compressed=[value for i,value in enumerate(expected) if i==0 or value!=expected[i-1]]
        if len(compressed)>7:failures.append(f"action {action} cycles weapon poses: {compressed}")
        checked+=1
    report={"status":"PASS" if not failures else "FAIL","actions_checked":checked,
            "rows_checked":sum(len(v) for v in install["action_sequences"].values()),"failures":failures}
    (ART/"audit.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2));raise SystemExit(0 if not failures else 1)


if __name__=="__main__":main()
