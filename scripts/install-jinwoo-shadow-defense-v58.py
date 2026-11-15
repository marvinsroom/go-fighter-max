"""Install v58 crouch art, shadow locomotion FX, Tank guard, and Tusk routing."""
from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/shadow-defense-v58"
AIR, SFF_PATH = LIVE / "anim.air", LIVE / "spr.sff"
BASE, NEGATIVE, CMD = LIVE / "base.cns", LIVE / "-2.cns", LIVE / "cmd.cmd"
CONTROLS = ROOT / "sprite-fighter/characters/jinwoo-mugen/CONTROLS.md"
BACKUP, REPORT = ART / "live-before-shadow-defense-v58", ART / "installation.json"
GROUP = 61024
# The generated crouch drawings are substantially wider than the canonical
# upright body.  Keep their vertical scale (and therefore crouch height), but
# correct the horizontal scale so the widest crouch silhouette is no more than
# 1.25x idle.  Using one uniform X scale across all three frames also prevents
# the body from "breathing" wider during the transition.
SX, SY = 0.077450000, 0.089030246
MARKER = "; JINWOO SHADOW DEFENSE V58"


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO(); image.save(payload, format="PNG", optimize=True)
    return {"image": image, "png": payload.getvalue(), "axis": axis,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


def crouch_frames() -> list[Image.Image]:
    sheet = Image.open(ART / "crouch-sheet-v58.png").convert("RGBA")
    if sheet.width % 3:
        raise RuntimeError(f"crouch sheet is not three equal cells: {sheet.size}")
    width = sheet.width // 3
    frames = []
    for index in range(3):
        cell = sheet.crop((index * width, 0, (index + 1) * width, sheet.height))
        alpha = cell.getchannel("A").point(lambda value: 0 if value < 24 else value)
        mask = (np.asarray(alpha) > 0).astype(np.uint8)
        count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        if count <= 1:
            raise RuntimeError(f"empty crouch cell {index}")
        largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = Image.fromarray(np.where(labels == largest, np.asarray(alpha), 0).astype(np.uint8), mode="L")
        cell.putalpha(alpha); box = alpha.getbbox()
        if not box:
            raise RuntimeError(f"empty crouch cell {index}")
        drawing = cell.crop(box)
        drawing = drawing.resize((round(drawing.width * .72), round(drawing.height * .72)), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (drawing.width + 32, drawing.height + 32), (0, 0, 0, 0))
        canvas.alpha_composite(drawing, (16, 16)); frames.append(canvas)
    return frames


def replace_action(text: str, number: int, replacement: str) -> str:
    match = re.search(rf"(?ims)^\[Begin Action\s+{number}\]\s*\r?\n.*?(?=^\[Begin Action\s+-?\d+\]\s*\r?\n|\Z)", text)
    if not match:
        raise RuntimeError(f"missing action {number}")
    return text[:match.start()] + replacement.rstrip() + "\n\n" + text[match.end():]


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.mkdir(parents=True)
        for source in (AIR, SFF_PATH, BASE, NEGATIVE, CMD, CONTROLS):
            shutil.copy2(source, BACKUP / source.name)

    additions = {}; details = []
    normalized = ART / "normalized"; normalized.mkdir(exist_ok=True)
    for number, image in enumerate(crouch_frames()):
        box = image.getchannel("A").getbbox(); axis = (image.width // 2, box[3] - 18)
        image.save(normalized / f"{GROUP}-{number}.png", optimize=True)
        additions[(GROUP, number)] = encoded(image, axis)
        details.append({"key": [GROUP, number], "size": list(image.size), "bbox": list(box), "axis": list(axis),
                        "world_width_before_character_scale": round((box[2] - box[0]) * SX, 3),
                        "world_height_before_character_scale": round((box[3] - box[1]) * SY, 3)})
    sff = Sff(SFF_PATH)
    replacements = {key: frame for key, frame in additions.items() if key in sff.keys}
    new = {key: frame for key, frame in additions.items() if key not in sff.keys}
    pending = SFF_PATH.with_suffix(".v58.pending")
    pending.write_bytes(sff.derive(replacements, new))
    try:
        pending.replace(SFF_PATH)
    except PermissionError:
        # Windows can briefly reject an atomic rename after Ikemen exits even
        # though the file is no longer actively locked.  A direct overwrite is
        # safe here because the complete derived SFF already exists on disk.
        shutil.copy2(pending, SFF_PATH)
        pending.unlink()

    actions = {
        10: f"""[Begin Action 10]
Clsn2Default: 1
Clsn2[0] = -15,-43,15,0
{GROUP},0,0,0,4,,,{SX:.9f},{SY:.9f}
{GROUP},1,0,0,4,,,{SX:.9f},{SY:.9f}""",
        11: f"""[Begin Action 11]
Clsn2Default: 1
Clsn2[0] = -16,-34,16,0
LoopStart
{GROUP},1,0,0,8,,,{SX:.9f},{SY:.9f}""",
        12: f"""[Begin Action 12]
Clsn2Default: 1
Clsn2[0] = -15,-43,15,0
{GROUP},1,0,0,4,,,{SX:.9f},{SY:.9f}
{GROUP},2,0,0,4,,,{SX:.9f},{SY:.9f}""",
    }
    air = AIR.read_text(encoding="latin1")
    for number, replacement in actions.items():
        air = replace_action(air, number, replacement)
    AIR.write_text(air.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    # Correct the second-jump animation and preserve the requested direction
    # through the velocity assignment that occurs two ticks later.
    base = BASE.read_text(encoding="latin1")
    state45 = re.search(r"(?ims)^\[Statedef 45\].*?(?=^\[Statedef 50\])", base)
    if not state45:
        raise RuntimeError("missing double-jump state 45")
    block = state45.group(0)
    injection = """
[State 45, V58 human double-jump rise]
type = ChangeAnim
triggerall = !ishelper && var(45) = 0
trigger1 = time = 0
value = 41

[State 45, V58 remember air-jump direction]
type = VarSet
trigger1 = time = 0
sysvar(1) = ifelse(command = "holdfwd",1,ifelse(command = "holdback",-1,0))
"""
    anchor = "[State 0]\ntype = VelSet\ntrigger1 = Time = 2"
    if "V58 human double-jump rise" not in block:
        if anchor not in block:
            raise RuntimeError("double-jump velocity anchor changed")
        block = block.replace(anchor, injection + "\n" + anchor, 1)
    base = base[:state45.start()] + block + base[state45.end():]
    BASE.write_text(base, encoding="latin1", newline="")

    # Centralized visuals avoid editing every individual guard state. Tank is
    # defensive only; it has no HitDef and disappears immediately after guard.
    negative = NEGATIVE.read_text(encoding="latin1")
    controllers = """

; JINWOO SHADOW DEFENSE V58
[State -2, V58 Tank guard body]
type = Explod
triggerall = !ishelper && var(45) = 0
triggerall = stateno = [120,155]
triggerall = !numexplod(879904)
trigger1 = 1
anim = 2130
id = 879904
postype = p1
pos = 24,0
bindtime = -1
removetime = -2
scale = 1.2,1.2
sprpriority = 4
ownpal = 1
removeongethit = 0
ignorehitpause = 1

[State -2, V58 dismiss Tank after guard]
type = RemoveExplod
triggerall = numexplod(879904)
trigger1 = stateno != [120,155]
id = 879904
ignorehitpause = 1

"""
    # Remove the rejected movement overlays if an earlier v58 run installed
    # them. Tank guard remains; ordinary locomotion stays visually clean.
    for title in ("V58 walking shadow wisps", "V58 jump shadow burst", "V58 crouch shadow pool"):
        negative = re.sub(
            rf"(?ims)^\[State -2, {re.escape(title)}\].*?(?=^\[State|^\[Statedef|\Z)",
            "",
            negative,
        )
    if "; JINWOO SHADOW DEFENSE V58" not in negative:
        negative = negative.rstrip() + controllers + "\n"
    NEGATIVE.write_text(negative, encoding="latin1", newline="")

    cmd = CMD.read_text(encoding="latin1")
    tank_summon = re.search(
        r'(?ims)^\[State -1, Preserve assigned shadow\]\s*\n(?:(?!^\[State).)*?triggerall=command="holddown"(?:(?!^\[State).)*?value=870103\s*', cmd
    )
    if not tank_summon and "V58 Tusk replaces Tank summon" not in cmd:
        raise RuntimeError("could not find the directional Tank summon route")
    if tank_summon:
        replacement = """[State -1, V58 Tusk replaces Tank summon]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
triggerall=var(45)=0 && power>=500 && !numhelper(1510)
triggerall=command="holddown"
trigger1=command="our_summon"
value=1500
ctrl=0
"""
        cmd = cmd[:tank_summon.start()] + replacement + cmd[tank_summon.end():]
    CMD.write_text(cmd, encoding="latin1", newline="")

    controls = CONTROLS.read_text(encoding="utf-8")
    note = "- Hold down + summon: call Tusk (Tank is now the automatic guard shadow)"
    if note not in controls:
        controls = controls.rstrip() + "\n" + note + "\n"
    CONTROLS.write_text(controls, encoding="utf-8", newline="")

    report = {"status": "INSTALLED", "crouch_group": GROUP, "frames": details,
              "double_jump": "v57 rise/apex with preserved direction", "guard_shadow": "Tank",
              "down_summon": "Tusk", "shadow_effects": "removed after visual review"}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
