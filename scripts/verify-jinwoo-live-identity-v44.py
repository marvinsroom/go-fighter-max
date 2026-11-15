"""Gate live visual identity, source hashes, scale, and charge consistency."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/live-identity-audit-v44/verification.json"
FILES = {
    (1000,20): "tusk-neutral-normalized-v32.png", (1000,21): "tusk-charge-normalized-v32.png",
    (1000,22): "tusk-recovery-normalized-v32.png", (1000,222): "tusk-release-normalized-v32.png",
    (1000,27): "kaisel-flight-up-27-normalized-v32.png", (1000,28): "kaisel-flight-down-28-normalized-v32.png",
    (1000,29): "kaisel-attack-dive-29-normalized-v32.png", (1000,30): "kaisel-flight-up-30-normalized-v32.png",
    (1000,31): "kaisel-flight-down-31-normalized-v32.png", (1000,32): "kaisel-attack-dive-32-normalized-v32.png",
}


def rgba_hash(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def action_blocks(text: str) -> dict[int,str]:
    matches=list(re.finditer(r"(?im)^\[Begin Action\s+(\d+)\]\s*$",text))
    return {int(m[1]):text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)] for i,m in enumerate(matches)}


def main() -> None:
    air=(LIVE/"anim.air").read_text(encoding="latin1")
    cns=(LIVE/"cns.cns").read_text(encoding="latin1")
    minus2=(LIVE/"-2.cns").read_text(encoding="latin1")
    blocks=action_blocks(air); sff=Sff(LIVE/"spr.sff"); failures=[]; hashes={}
    source=ART/"tusk-kaisel-restyle-v32"
    for key,name in FILES.items():
        packed=rgba_hash(sff.decode(sff.keys[key])); expected=rgba_hash(Image.open(source/name))
        hashes[str(key)]={"packed":packed,"source":expected,"match":packed==expected}
        if packed!=expected: failures.append(f"raster mismatch {key}")
    identity={"Tusk":{"range":(5_000_000,6_000_000),"frames":{20,21,22,222},"scale":"0.075000000"},"Kaisel":{"range":(6_000_000,7_000_000),"frames":{27,28,29},"scale":"0.060000000"}}
    rows={}
    for name,spec in identity.items():
        seen=set(); legacy=[]; wrong=[]; scales=set()
        for number,block in blocks.items():
            if not(spec["range"][0]<=number<spec["range"][1]): continue
            for line in block.splitlines():
                parts=line.split(",")
                if len(parts)>=2 and parts[0].strip().lstrip("-").isdigit():
                    group=int(parts[0]); frame=int(parts[1])
                    if group==61001: legacy.append([number,group,frame])
                    if group==1000:
                        seen.add(frame)
                        if frame not in spec["frames"]: wrong.append([number,group,frame])
                        if len(parts)>=9: scales.add((parts[7].strip(),parts[8].strip()))
        if legacy: failures.append(f"{name} still contains legacy group 61001")
        if wrong: failures.append(f"{name} contains wrong identity frames")
        if seen!=spec["frames"]: failures.append(f"{name} phase coverage {sorted(seen)}")
        if scales!={(spec["scale"],spec["scale"])}: failures.append(f"{name} inconsistent scales {sorted(scales)}")
        rows[name]={"frames":sorted(seen),"legacy_rows":len(legacy),"wrong_rows":len(wrong),"scales":[list(v) for v in sorted(scales)]}
    charge={"hoodie_flag_absent":"Full meter enables hoodie form" not in cns,"hoodie_idle_absent":"FULL-METER HOODIE" not in minus2,"state501_override_absent":"anim=ifelse(var(30)=1,61902" not in cns,"system_enclosure_present":"System enclosure around Jinwoo" in cns}
    failures.extend(name for name,passed in charge.items() if not passed)
    report={"status":"PASS" if not failures else "FAIL","forms":rows,"source_rasters":hashes,"charge":charge,"failures":failures}
    OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    if failures: raise SystemExit(1)


if __name__=="__main__": main()
