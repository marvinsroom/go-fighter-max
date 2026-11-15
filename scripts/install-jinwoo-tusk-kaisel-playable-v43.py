"""Add complete playable Tusk and Kaisel form routes from the proven form template."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/playable-tusk-kaisel-v43"
BACKUP = OUT / "live-before-v43"
AIR = LIVE / "anim.air"
SHADOWS = LIVE / "our-shadows.cns"
CMD = LIVE / "cmd.cmd"
MINUS2 = LIVE / "-2.cns"
BRIDGE = ROOT / "scripts/jinwoo-dpad-bridge.ps1"
CONTROLS = ROOT / "sprite-fighter/characters/jinwoo-mugen/CONTROLS.md"
MARKER = "; JINWOO PLAYABLE TUSK AND KAISEL V43"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def action_chunks(text: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"(?im)^\[Begin Action\s+(-?\d+)\]\s*$", text))
    return [(int(m.group(1)), text[m.start(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]) for i, m in enumerate(matches)]


def form_action(source: str, old_number: int, new_number: int, frames: list[int]) -> str:
    source = re.sub(rf"(?im)^\[Begin Action\s+{old_number}\]", f"[Begin Action {new_number}]", source, count=1)
    counter = 0
    lines = []
    for line in source.splitlines():
        match = re.match(r"^(\s*)61001\s*,\s*(-?\d+)(\s*,.*)$", line)
        if match:
            frame = frames[(int(match.group(2)) + counter) % len(frames)]
            line = f"{match.group(1)}61001,{frame}{match.group(3)}"
            counter += 1
        lines.append(line)
    return "\n".join(lines).rstrip() + "\n\n"


def shift_form_state(block: str, delta: int) -> str:
    def replace(match: re.Match[str]) -> str:
        value = int(match.group(0))
        return str(value + delta)
    return re.sub(r"(?<!\d)89\d{4}(?!\d)", replace, block)


def transformation_state(template: str, state: int, target: int, action: int, name: str) -> str:
    result = template.replace("870201", str(state)).replace("igris", name.lower()).replace("Igris", name)
    result = result.replace("anim=870200+var(45)*100", f"anim=ifelse(var(45)={target},{action},870200)")
    result = result.replace("var(45)=cond(var(46)=1,0,1)", f"var(45)=cond(var(46)={target},0,{target})")
    result = result.replace("value=870200+var(45)*100", f"value=ifelse(var(45)={target},{action},870200)")
    return result.rstrip() + "\n\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "installation.json"
    air = AIR.read_text(encoding="latin1")
    if MARKER in air:
        print(report_path.read_text(encoding="utf-8")); return

    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (AIR, SHADOWS, CMD, MINUS2, BRIDGE, CONTROLS):
        shutil.copy2(path, BACKUP / path.name)

    chunks = action_chunks(air)
    igris = [(number, block) for number, block in chunks if 1_000_000 <= number < 2_000_000]
    if len(igris) != 444:
        raise RuntimeError(f"expected 444 Igris actions, found {len(igris)}")
    tusk_actions = [form_action(block, number, number + 4_000_000, [20, 21, 22, 21]) for number, block in igris]
    kaisel_actions = [form_action(block, number, number + 5_000_000, [27, 28, 29, 28]) for number, block in igris]
    transform_actions = """
[Begin Action 879805]
Clsn2: 2
Clsn2[0] = -22,-57,22,0
Clsn2[1] = -16,-66,16,-38
61001,20,0,0,18,,,0.238095238,0.238095238
61001,21,0,0,12,,,0.238095238,0.238095238
61001,22,0,0,12,,,0.238095238,0.238095238

[Begin Action 879806]
Clsn2: 2
Clsn2[0] = -38,-38,38,0
Clsn2[1] = -24,-58,24,-20
61001,27,0,0,18,,,0.238095238,0.238095238
61001,28,0,0,12,,,0.238095238,0.238095238
61001,29,0,0,12,,,0.238095238,0.238095238
"""
    air = air.rstrip() + f"\n\n{MARKER}\n" + transform_actions + "\n" + "".join(tusk_actions + kaisel_actions)
    AIR.write_text(air, encoding="latin1", newline="")

    shadows = SHADOWS.read_text(encoding="latin1")
    state_matches = list(re.finditer(r"(?im)^\[Statedef\s+(\d+)\]\s*$", shadows))
    state_blocks = []
    transform_template = ""
    for i, match in enumerate(state_matches):
        number = int(match.group(1))
        end = state_matches[i + 1].start() if i + 1 < len(state_matches) else len(shadows)
        block = shadows[match.start():end]
        if number == 870201:
            transform_template = block
        if 890000 <= number < 900000:
            state_blocks.append(block)
    if len(state_blocks) != 16 or not transform_template:
        raise RuntimeError(f"form template mismatch: {len(state_blocks)} states")
    additions = transformation_state(transform_template, 870205, 5, 879805, "Tusk")
    additions += transformation_state(transform_template, 870206, 6, 879806, "Kaisel")
    additions += "; PLAYABLE TUSK FORM STATES\n" + "".join(shift_form_state(block, 40_000) for block in state_blocks)
    additions += "; PLAYABLE KAISEL FORM STATES\n" + "".join(shift_form_state(block, 50_000) for block in state_blocks)
    SHADOWS.write_text(shadows.rstrip() + "\n\n" + MARKER + "\n" + additions, encoding="latin1", newline="")

    cmd = CMD.read_text(encoding="latin1")
    command_needle = '[Command]\nname="pad_summon_kaisel"'
    commands = '''[Command]
name="pad_tf_kaisel"
command=a+c+x
time=1
[Command]
name="pad_tf_tusk"
command=b+c+x
time=1
'''
    if command_needle not in cmd:
        raise RuntimeError("v42 controller command insertion point missing")
    cmd = cmd.replace(command_needle, commands + command_needle, 1)
    route_needle = "[State -1, Controller summon Kaisel]"
    routes = '''[State -1, Controller transform Kaisel]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="pad_tf_kaisel"
value=870206
ctrl=0
[State -1, Controller transform Tusk]
type=ChangeState
triggerall=!AILevel && roundstate=2 && ctrl && statetype!=A
trigger1=command="pad_tf_tusk"
value=870205
ctrl=0
'''
    cmd = cmd.replace(route_needle, routes + route_needle, 1)
    CMD.write_text(cmd, encoding="latin1", newline="")

    minus2 = MINUS2.read_text(encoding="latin1")
    width_needle = "[State -2, Equipped dagger artwork]"
    widths = '''[State -2, Tusk body push width]
type=Width
triggerall=!ishelper
trigger1=var(45)=5
player=30,30
edge=30,30
ignorehitpause=1
[State -2, Kaisel body push width]
type=Width
triggerall=!ishelper
trigger1=var(45)=6
player=42,42
edge=42,42
ignorehitpause=1

'''
    if width_needle not in minus2:
        raise RuntimeError("form width insertion point missing")
    MINUS2.write_text(minus2.replace(width_needle, widths + width_needle, 1), encoding="latin1", newline="")

    bridge = BRIDGE.read_text(encoding="utf-8")
    bridge = bridge.replace("function Send-Chord([byte]$First,[byte]$Second) {", """function Send-Triple([byte]$First,[byte]$Second,[byte]$Third) {
 [JinwooPad]::Key($First,$true); [JinwooPad]::Key($Second,$true); [JinwooPad]::Key($Third,$true)
 Start-Sleep -Milliseconds 150
 [JinwooPad]::Key($Third,$false); [JinwooPad]::Key($Second,$false); [JinwooPad]::Key($First,$false)
}
function Send-Chord([byte]$First,[byte]$Second) {""", 1)
    old = """  $summonModifier=$state.Pad.LT -gt 80
  if($key -and $summonModifier -and $elapsed -ge 350 -and ($key-eq 0x21 -or $key-eq 0x22)){"""
    new = """  $summonModifier=$state.Pad.LT -gt 80
  $transformModifier=$state.Pad.RT -gt 80
  if($key -and $transformModifier -and $elapsed -ge 350 -and ($key-eq 0x21 -or $key-eq 0x22)){
   $lastAcceptedPress=Get-Date
   if($key-eq 0x21){
    Write-BridgeLog 'RT + D-pad up / transform Kaisel dragon'
    Send-Triple 0x21 0x23 0x13
   } else {
    Write-BridgeLog 'RT + D-pad right / transform Tusk'
    Send-Triple 0x22 0x23 0x13
   }
  } elseif($key -and $summonModifier -and $elapsed -ge 350 -and ($key-eq 0x21 -or $key-eq 0x22)){"""
    if old not in bridge:
        raise RuntimeError("v42 bridge insertion point missing")
    BRIDGE.write_text(bridge.replace(old, new, 1), encoding="utf-8")

    controls = CONTROLS.read_text(encoding="utf-8")
    controls = controls.replace("- LT + D-pad right: summon Tusk, the red mage\n", "- LT + D-pad right: summon Tusk, the red mage\n- RT + D-pad up: transform into or return from Kaisel\n- RT + D-pad right: transform into or return from Tusk\n")
    controls = controls.replace("Tusk and Kaisel are summon characters, not playable transformation banks. The\navailable playable transformations are Igris, Beru, Iron, and Tank.\n", "Playable transformations are Igris, Beru, Iron, Tank, Tusk, and Kaisel. Tusk and\nKaisel retain their separate summon shortcuts, so transforming does not consume\nor replace an active summon.\n")
    CONTROLS.write_text(controls, encoding="utf-8")

    report = {
        "status": "INSTALLED",
        "revision": "playable-tusk-kaisel-v43",
        "new_forms": {"5": "Tusk", "6": "Kaisel"},
        "actions_per_form": 444,
        "states_per_form": 16,
        "controller": {"RT+D-pad up": "toggle Kaisel", "RT+D-pad right": "toggle Tusk", "LT+D-pad up": "summon Kaisel", "LT+D-pad right": "summon Tusk"},
        "body_keys": {"Tusk": [[61001, 20], [61001, 21], [61001, 22]], "Kaisel": [[61001, 27], [61001, 28], [61001, 29]]},
        "runtime_sha256": {path.name: sha(path) for path in (AIR, SHADOWS, CMD, MINUS2, BRIDGE, CONTROLS)},
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
