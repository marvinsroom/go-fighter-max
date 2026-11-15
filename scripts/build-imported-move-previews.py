"""Render installed MUGEN AIR actions as browser-viewable move GIFs."""
from pathlib import Path
from PIL import Image
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff

GENERIC_NAMES = {"a", "b", "c", "x", "y", "z", "s", "fwd", "back", "up", "down", "hold_a", "hold_b", "hold_c", "hold_x", "hold_y", "hold_z", "hold_s"}

def text(path):
    for encoding in ("utf-8", "cp1252", "latin1"):
        try: return path.read_text(encoding=encoding)
        except UnicodeDecodeError: pass
    return path.read_text(errors="replace")

def ref(definition, field):
    found = re.search(rf"(?im)^\s*{field}\s*=\s*([^;\r\n]+)", text(definition))
    return found.group(1).strip() if found else None

def actions(path):
    result = {}
    for match in re.finditer(r"(?ims)^\s*\[Begin Action\s+(-?\d+)\](.*?)(?=^\s*\[Begin Action|\Z)", text(path)):
        frames = []
        for line in match.group(2).splitlines():
            clean = line.split(";", 1)[0].strip()
            if not re.match(r"^-?\d+\s*,\s*-?\d+", clean): continue
            parts = [part.strip() for part in clean.split(",")]
            try:
                group, image, x, y, ticks = map(int, parts[:5])
            except (ValueError, IndexError):
                continue
            def scale_at(index):
                try: return float(parts[index]) if len(parts) > index and parts[index] else 1.0
                except ValueError: return 1.0
            if group >= 0 and image >= 0:
                frames.append({"key": (group, image), "x": x, "y": y, "ticks": ticks, "flip": len(parts) > 5 and "H" in parts[5].upper(), "scale_x": scale_at(7), "scale_y": scale_at(8)})
        if frames: result[int(match.group(1))] = frames
    return result

def action_labels(path):
    labels = {}
    pending = ""
    for line in text(path).splitlines():
        stripped = line.strip()
        if stripped.startswith(";") and stripped[1:].strip():
            pending = stripped[1:].strip(" *;-")
        match = re.match(r"(?i)^\[Begin Action\s+(-?\d+)\]", stripped)
        if match:
            if pending: labels[int(match.group(1))] = pending
            pending = ""
        elif stripped and not stripped.startswith(";") and not re.match(r"(?i)^(clsn|loopstart|interpolate)", stripped):
            pending = ""
    return labels

def state_animations(live):
    mapping = {}
    files = [p for p in live.rglob("*") if p.is_file() and p.suffix.lower() in (".cns", ".st", ".st1", ".st2", ".st3", ".st4", ".zss")]
    for path in files:
        data = text(path)
        for match in re.finditer(r"(?ims)^\s*\[Statedef\s+(-?\d+)\](.*?)(?=^\s*\[Statedef|\Z)", data):
            anim = re.search(r"(?im)^\s*anim\s*=\s*(-?\d+)", match.group(2))
            if anim: mapping[int(match.group(1))] = int(anim.group(1))
    return mapping

def command_states(cmd, live):
    state_anim = state_animations(live)
    found = []
    data = text(cmd)
    for block in re.split(r"(?=^\s*\[State\s+-1)", data, flags=re.I | re.M):
        names = re.findall(r'(?im)command\s*=\s*"([^"]+)"', block)
        change = re.search(r"(?im)^\s*(?:value|state)\s*=\s*(-?\d+)\s*$", block)
        if not names or not change: continue
        state = int(change.group(1)); animation = state_anim.get(state)
        for name in names:
            row = (name, state, animation)
            if row not in found: found.append(row)
    return found

def command_inputs(cmd):
    return {m.group(1).strip(): m.group(2).strip() for m in re.finditer(r'(?ims)^\s*\[Command\].*?^\s*name\s*=\s*"?([^";\r\n]+).*?^\s*command\s*=\s*([^;\r\n]+)', text(cmd))}

def neutral_scale(action, archive):
    heights = []
    for frame in action:
        if frame["key"] in archive.keys:
            image = archive.decode(archive.keys[frame["key"]]).convert("RGBA")
            box = image.getchannel("A").getbbox()
            if box: heights.append((box[3] - box[1]) * abs(frame.get("scale_y", 1)))
    reference = max(heights, default=80)
    return min(3.5, 220 / max(1, reference))

def render(action, archive, output, world_scale):
    decoded = []
    for frame in action[:40]:
        if frame["key"] not in archive.keys: continue
        index = archive.keys[frame["key"]]
        image = archive.decode(index).convert("RGBA")
        axis = archive.headers[index][4:6]
        if frame["flip"]: image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        decoded.append((frame, image, axis))
    if not decoded: return False
    canvases = []
    durations = []
    for frame, image, axis in decoded:
        scale_x = world_scale * abs(frame.get("scale_x", 1))
        scale_y = world_scale * abs(frame.get("scale_y", 1))
        image = image.resize((max(1, round(image.width * scale_x)), max(1, round(image.height * scale_y))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (640, 420), (14, 17, 27, 255))
        x = 320 + round(frame["x"] * world_scale - axis[0] * scale_x)
        y = 360 + round(frame["y"] * world_scale - axis[1] * scale_y)
        canvas.alpha_composite(image, (x, y))
        canvases.append(canvas.convert("RGB"))
        durations.append(max(50, min(250, (frame["ticks"] if frame["ticks"] > 0 else 6) * 17)))
    canvases[0].save(output, save_all=True, append_images=canvases[1:], duration=durations, loop=0, optimize=True)
    return True

progress = json.loads((GAME / "style-wave2/conversion-progress.json").read_text())
targets = sys.argv[1:] or list(progress["installed"])
for slug in targets:
    if slug not in progress["installed"]: raise SystemExit(f"Unknown installed fighter: {slug}")
    live = GAME / "engine/ikemen-go-v1.0.0/chars" / slug
    definition = live / f"{slug}.def"
    if not definition.exists(): definition = next(live.glob("*.def"))
    cmd_name = ref(definition, "cmd")
    air_name = ref(definition, "anim")
    sff_name = ref(definition, "sprite")
    cmd = live / cmd_name if cmd_name else next(p for p in live.rglob("*") if p.suffix.lower() in (".cmd", ".cmnd"))
    air = live / air_name if air_name else next(live.glob("*.air"))
    sff = live / sff_name if sff_name else next(live.glob("*.sff"))
    action_map = actions(air); labels = action_labels(air); inputs = command_inputs(cmd); candidates = []
    for name, state, animation in command_states(cmd, live):
        if animation in action_map and name in inputs and len(action_map[animation]) > 1:
            priority = 0 if re.search(r"ultimate|super|finisher|skill|special|domain|susanoo|clash|hollow|meteor|dragon", name, re.I) else 1
            row = (priority, name, inputs[name], state, animation)
            if all(existing[4] != animation for existing in candidates): candidates.append(row)
    candidates.sort(key=lambda row: (row[0], row[1].lower()))
    chosen = []
    special_words = re.compile(r"ultimate|super|finisher|domain|bankai|hollow|purple|muryo|chidori|kirin|susanoo|amaterasu|dragon|special|hyper|meteor|transform|ougi", re.I)
    non_move_words = re.compile(r"portrait|spark|background|\bbg\b|charge|\bfx\b|opponent|hit by|cancel|finish flash", re.I)
    named = [(animation, label) for animation, label in labels.items() if animation in action_map and len(action_map[animation]) > 1 and special_words.search(label) and not non_move_words.search(label)]
    named.sort(key=lambda row: (0 if re.search(r"ultimate|hyper|bankai|domain|kirin|meteor|dragon|level 3", row[1], re.I) else 1, row[0]))
    for animation, label in named:
        if animation in action_map:
            input_ = next((value for command, value in inputs.items() if len(command.strip()) > 2 and command.lower() not in GENERIC_NAMES and (command.lower() in label.lower() or label.lower() in command.lower())), "See moveset")
            chosen.append((0, label, input_, animation, animation))
    for row in candidates:
        if all(existing[4] != row[4] for existing in chosen): chosen.append(row)
    if not chosen:
        fallback = sorted(((len(frames), animation) for animation, frames in action_map.items() if animation >= 1000 and len(frames) > 1 and all(row[4] != animation for row in chosen)), reverse=True)
        for _, animation in fallback:
            chosen.append((1, labels.get(animation, f"Special animation {animation}"), "See moveset", animation, animation))
            if len(chosen) >= 10: break
    # Guarantee recognizable movement/normal pictures when state routing is highly dynamic.
    for label, animation in (("Standing", 0), ("Light attack", 200), ("Heavy attack", 210)):
        if animation in action_map and all(row[4] != animation for row in chosen):
            chosen.append((2, label, "See controls", animation, animation))
    output = GAME / "characters" / slug / "gameplay-previews"
    output.mkdir(parents=True, exist_ok=True)
    archive = Sff(sff); records = []
    world_scale = neutral_scale(action_map.get(0, next(iter(action_map.values()))), archive)
    for index, (_, name, input_, state, animation) in enumerate(chosen):
        filename = f"{index:02d}-{re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')[:45]}.gif"
        if render(action_map[animation], archive, output / filename, world_scale):
            if re.search(r"ultimate|hyper|bankai|domain|kirin|meteor|dragon|level 3|black chidori", name, re.I): category = "Ultimate"
            elif re.search(r"super", name, re.I): category = "Super"
            elif name in ("Standing", "Light attack", "Heavy attack"): category = "Normal"
            else: category = "Special"
            records.append({"name": name, "category": category, "input": input_, "state": state, "animation": animation, "file": filename, "frames": min(40, len(action_map[animation]))})
    ultimate_count = sum(item["category"] == "Ultimate" for item in records)
    if slug == "zoro":
        zoro_moves = {
            1000: ("Oni Giri", "Special", "A"),
            1100: ("Rising Dragon", "Special", "Down + A"),
            1200: ("Three Sword Cyclone", "Special", "Back + A"),
            3000: ("Rokudou no Tsuji", "Super", "S"),
            3100: ("Kokujou Oo Tatsumaki", "Super", "Back + S"),
            3200: ("San Zen Sekai", "Ultimate", "D"),
        }
        for item in records:
            if item["state"] in zoro_moves:
                item["name"], item["category"], item["input"] = zoro_moves[item["state"]]
            elif item["animation"] == 824:
                item["category"] = "Special"
        ultimate_count = sum(item["category"] == "Ultimate" for item in records)
    (output / "index.json").write_text(json.dumps({"status": "SPRITE_ANIMATION_PREVIEWS", "character": slug, "source_sff": sff.name, "source_air": air.name, "scale_policy": "One neutral-reference scale for every move; authored AIR x/y scale applied per frame", "neutral_world_scale": world_scale, "canvas": [640, 420], "moves": records, "ultimate_preview_status": "PRESENT" if ultimate_count else "NOT_IDENTIFIABLE_IN_SOURCE_AIR", "ultimate_previews": ultimate_count, "native_capture": False}, indent=2), encoding="utf-8")
    print(slug, len(records), "move previews")
