"""Remove live identity leaks from charge, Tusk, and Kaisel action banks."""
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
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/live-identity-audit-v44"
BACKUP = OUT / "live-before-v44"
AIR, CNS, MINUS2, SFF_PATH = (LIVE / "anim.air", LIVE / "cns.cns", LIVE / "-2.cns", LIVE / "spr.sff")
MARKER = "; JINWOO LIVE IDENTITY FIX V44"

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


def packed(path: Path, axis: tuple[int, int]) -> dict:
    image = Image.open(path).convert("RGBA")
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis, "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def split_actions(text: str) -> tuple[str, list[tuple[int, str]]]:
    matches = list(re.finditer(r"(?im)^\[Begin Action\s+(-?\d+)\]\s*$", text))
    prefix = text[:matches[0].start()]
    return prefix, [(int(m.group(1)), text[m.start():matches[i+1].start() if i+1 < len(matches) else len(text)]) for i,m in enumerate(matches)]


def replace_body_rows(block: str, source_group: int, target_group: int, sequence: list[int], scale: float, preserve_number: bool = False) -> str:
    count = 0
    output = []
    for line in block.splitlines():
        parts = line.split(",")
        if len(parts) >= 5 and re.fullmatch(r"\s*-?\d+\s*", parts[0]) and int(parts[0]) == source_group:
            old_number = int(parts[1])
            number = old_number if preserve_number else sequence[count % len(sequence)]
            parts[0] = str(target_group)
            parts[1] = str(number)
            while len(parts) < 9:
                parts.append("")
            parts[7] = f"{scale:.9f}"
            parts[8] = f"{scale:.9f}"
            line = ",".join(parts)
            count += 1
        output.append(line)
    return "\n".join(output).rstrip() + "\n\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air = AIR.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8")); return
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (AIR, CNS, MINUS2, SFF_PATH):
        shutil.copy2(path, BACKUP / path.name)

    sff = Sff(SFF_PATH)
    replacements = {}
    for number, (name, axis) in {**TUSK, **KAISEL}.items():
        replacements[(1000, number)] = packed(SOURCE / name, axis)
    existing = {key: frame for key, frame in replacements.items() if key in sff.keys}
    additions = {key: frame for key, frame in replacements.items() if key not in sff.keys}
    SFF_PATH.write_bytes(sff.derive(existing, additions))

    prefix, chunks = split_actions(air)
    rewritten = []
    changed_actions = []
    tusk_summon = {1510,1511,1520,1521,1522,1530,1531}
    kaisel_summon = {2410,2411,2420,2421,2430,2431,2470,2471,2480,2481,2490}
    for number, block in chunks:
        original = block
        if number in tusk_summon:
            block = replace_body_rows(block, 61001, 1000, [], .075, preserve_number=True)
        elif number in kaisel_summon:
            block = replace_body_rows(block, 61001, 1000, [], .060, preserve_number=True)
        elif 5_000_000 <= number < 6_000_000:
            block = replace_body_rows(block, 61001, 1000, [20,21,222,22], .075)
        elif 6_000_000 <= number < 7_000_000:
            block = replace_body_rows(block, 61001, 1000, [27,28,29,28], .060)
        elif number == 879805:
            block = replace_body_rows(block, 61001, 1000, [20,21,222,22], .075)
        elif number == 879806:
            block = replace_body_rows(block, 61001, 1000, [27,28,29,28], .060)
        if block != original:
            changed_actions.append(number)
        rewritten.append(block)
    AIR.write_text(prefix + "".join(rewritten).rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    cns = CNS.read_text(encoding="latin1")
    hoodie_flag = '''[State 500, Full meter enables hoodie form]
type = VarSet
trigger1 = power >= powermax
v = 30
value = 1
ignorehitpause = 1
'''
    if hoodie_flag not in cns:
        raise RuntimeError("full-meter hoodie flag block missing")
    cns = cns.replace(hoodie_flag, "", 1)
    state501 = cns.index("[statedef 501]")
    state510 = cns.index("[statedef 510]", state501)
    section = cns[state501:state510]
    match = re.search(r"(?m)^anim=ifelse\(var\(30\)=1,61902,(.*)\)$", section)
    if not match:
        raise RuntimeError("single-pose hoodie state501 override missing")
    section = section[:match.start()] + "anim=" + match.group(1) + section[match.end():]
    CNS.write_text(cns[:state501] + section + cns[state510:], encoding="latin1", newline="")

    minus2 = MINUS2.read_text(encoding="latin1")
    minus2 = re.sub(r"\n; JINWOO FULL-METER HOODIE V41\n.*?\n(?=\Z)", "\n", minus2, flags=re.S)
    MINUS2.write_text(minus2, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "revision": "live-identity-v44",
        "corrected_actions": len(changed_actions),
        "corrected_action_ids": changed_actions,
        "restored_sprite_keys": [list(k) for k in sorted(replacements)],
        "identity_policy": {"human_charge": "approved coat Jinwoo; incomplete one-pose hoodie runtime disabled", "Tusk": "group 1000 frames 20,21,22,222 only", "Kaisel": "group 1000 frames 27-32 only"},
        "runtime_sha256": {path.name: sha(path) for path in (AIR,CNS,MINUS2,SFF_PATH)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
