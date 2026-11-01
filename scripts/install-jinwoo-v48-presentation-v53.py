"""Install corrected v48 aerial, intro, victory, and System-charge art."""
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
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/presentation-v53"
AIR = LIVE / "anim.air"
SFF_PATH = LIVE / "spr.sff"
CNS = LIVE / "cns.cns"
BACKUP = ART / "live-before-presentation-v53"
REPORT = ART / "installation.json"
SX, SY = 0.095218974, 0.089829218
MARKER = "; JINWOO V48 PRESENTATION V53"


def encoded(image: Image.Image, axis: tuple[int, int]) -> dict:
    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    return {
        "image": image,
        "png": payload.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
    }


def cells(path: Path, columns: int, rows: int, scale: float = 1.0) -> list[Image.Image]:
    sheet = Image.open(path).convert("RGBA")
    xs = [round(sheet.width * i / columns) for i in range(columns + 1)]
    ys = [round(sheet.height * i / rows) for i in range(rows + 1)]
    result = []
    for row in range(rows):
        for column in range(columns):
            cell = sheet.crop((xs[column], ys[row], xs[column + 1], ys[row + 1]))
            box = cell.getchannel("A").getbbox()
            if not box:
                raise RuntimeError(f"empty cell {column},{row} in {path.name}")
            crop = cell.crop(box)
            if scale != 1.0:
                crop = crop.resize(
                    (round(crop.width * scale), round(crop.height * scale)),
                    Image.Resampling.LANCZOS,
                )
            canvas = Image.new("RGBA", (crop.width + 32, crop.height + 32), (0, 0, 0, 0))
            canvas.alpha_composite(crop, (16, 16))
            result.append(canvas)
    return result


def six_body_components(path: Path) -> list[Image.Image]:
    """Extract six complete aerial bodies even when a fist crosses a grid line."""
    sheet = Image.open(path).convert("RGBA")
    alpha = np.asarray(sheet.getchannel("A"))
    mask = (alpha >= 96).astype(np.uint8)
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)
    candidates = sorted(
        range(1, count), key=lambda label: int(stats[label, cv2.CC_STAT_AREA]), reverse=True
    )[:6]
    if len(candidates) != 6 or stats[candidates[-1], cv2.CC_STAT_AREA] < 10000:
        raise RuntimeError("could not isolate six complete aerial bodies")
    candidates.sort(key=lambda label: (centroids[label][1] // (sheet.height / 2), centroids[label][0]))
    result = []
    for label in candidates:
        x, y, width, height, _ = stats[label]
        pad = 18
        left, top = max(0, x - pad), max(0, y - pad)
        right, bottom = min(sheet.width, x + width + pad), min(sheet.height, y + height + pad)
        crop = sheet.crop((left, top, right, bottom))
        local_labels = labels[top:bottom, left:right]
        local_alpha = np.asarray(crop.getchannel("A"))
        kept = np.where(local_labels == label, local_alpha, 0).astype(np.uint8)
        crop.putalpha(Image.fromarray(kept, mode="L"))
        canvas = Image.new("RGBA", (crop.width + 16, crop.height + 16), (0, 0, 0, 0))
        canvas.alpha_composite(crop, (8, 8))
        result.append(canvas)
    return result


def action(number: int, frames: list[int], group: int, times: list[int], loop: int | None = None) -> str:
    lines = [f"[Begin Action {number}]", "Clsn2Default: 1", "Clsn2[0] = -12,-59,12,0"]
    for index, frame in enumerate(frames):
        if loop is not None and index == loop:
            lines.append("LoopStart")
        duration = times[min(index, len(times) - 1)]
        lines.append(f"{group},{frame},0,0,{duration},,,{SX:.9f},{SY:.9f}")
    return "\n".join(lines)


def replace_action(text: str, number: int, replacement: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"(?ims)^\[Begin Action\s+{number}\][ \t]*\r?\n.*?(?=^\[Begin Action\s+-?\d+\][ \t]*\r?\n|\Z)"
    )
    updated, count = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    return updated, count == 1


def main() -> None:
    original_air = AIR.read_text(encoding="latin1")
    force = "--force" in sys.argv
    if MARKER in original_air and not force:
        print(REPORT.read_text(encoding="utf-8"))
        return

    if not BACKUP.exists():
        BACKUP.mkdir(parents=True, exist_ok=True)
        for path in (AIR, SFF_PATH, CNS):
            shutil.copy2(path, BACKUP / path.name)

    aerial = six_body_components(ART / "aerial-v53.png")
    presentation = cells(ART / "intro-idle-win-v53.png", 3, 2)
    # The charge source has larger 640px cells; 0.80 locks its model to the
    # same raw head/body scale as the 512px v48 presentation and aerial cells.
    charge = cells(ART / "system-charge-v53.png", 2, 2, 0.80)

    replacements: dict[tuple[int, int], dict] = {}
    additions: dict[tuple[int, int], dict] = {}
    frame_report = []
    for group, images, replace_existing in (
        (61015, aerial, True),
        (61018, presentation, force),
        (61019, charge, force),
    ):
        for index, image in enumerate(images):
            box = image.getchannel("A").getbbox()
            axis = (image.width // 2, box[3] - 16)
            image.save(ART / f"{group}-{index}.png", optimize=True)
            entry = encoded(image, axis)
            (replacements if replace_existing else additions)[(group, index)] = entry
            frame_report.append({
                "key": [group, index], "size": list(image.size),
                "bbox": list(box), "axis": list(axis),
            })

    sff = Sff(SFF_PATH)
    pending = SFF_PATH.with_suffix(".presentation-v53.pending")
    pending.write_bytes(sff.derive(replacements, additions))
    pending.replace(SFF_PATH)

    definitions = {
        # Defeat/round-end fallback and victory states: all remain v48.
        170: action(170, [4, 5], 61018, [18, -1]),
        180: action(180, [4, 5], 61018, [24, -1]),
        181: action(181, [3, 4], 61018, [18, -1]),
        # Shadow-exchange intro becomes a real arrival -> coat settle -> ready.
        878500: action(878500, [0, 1, 2], 61018, [18, 18, -1]),
        # Dedicated System charge loop for bare, dagger, and longsword modes.
        500: action(500, [0, 1, 2, 3, 2, 1], 61019, [7], loop=0),
        10500: action(10500, [0, 1, 2, 3, 2, 1], 61019, [7], loop=0),
        20500: action(20500, [0, 1, 2, 3, 2, 1], 61019, [7], loop=0),
        501: action(501, [1, 0], 61019, [4]),
        10501: action(10501, [1, 0], 61019, [4]),
        20501: action(20501, [1, 0], 61019, [4]),
        510: action(510, [3, 2, 0], 61019, [10, 30, 10]),
        10510: action(10510, [3, 2, 0], 61019, [10, 30, 10]),
        20510: action(20510, [3, 2, 0], 61019, [10, 30, 10]),
    }
    rewritten = original_air
    changed = []
    missing = []
    append_if_missing = {20510}
    for number, definition in definitions.items():
        rewritten, found = replace_action(rewritten, number, definition)
        if not found and number in append_if_missing:
            rewritten = rewritten.rstrip() + "\n\n" + definition + "\n"
            found = True
        (changed if found else missing).append(number)
    if missing:
        raise RuntimeError(f"missing live AIR actions: {missing}")
    AIR.write_text(rewritten.rstrip() + "\n\n" + MARKER + "\n", encoding="latin1", newline="")

    cns_text = CNS.read_text(encoding="latin1")
    cns_text, enclosure_count = re.subn(
        r"(?is)(\[State 500, System enclosure around Jinwoo\].*?trigger1\s*=\s*)time\s*=\s*2",
        r"\g<1>0 ; integrated into v53 charge body",
        cns_text,
        count=1,
    )
    cns_text, header_count = re.subn(
        r"(?is)(\[State 500, System status header\].*?trigger1\s*=\s*)time\s*=\s*5",
        r"\g<1>0 ; integrated into v53 charge body",
        cns_text,
        count=1,
    )
    if not force and (enclosure_count != 1 or header_count != 1):
        raise RuntimeError("could not disable both legacy charge overlay Explods")
    CNS.write_text(cns_text, encoding="latin1", newline="")

    report = {
        "status": "INSTALLED",
        "locked_scale": [SX, SY],
        "groups": {"aerial": 61015, "intro_idle_win": 61018, "system_charge": 61019},
        "actions_rewritten": changed,
        "legacy_charge_overlays_disabled": True,
        "source_charge_scale": 0.80,
        "frames": frame_report,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
