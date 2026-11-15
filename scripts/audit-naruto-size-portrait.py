"""Audit Naruto portraits, per-action screen height, and Kurama vs Jinwoo summons."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
ENG = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0"
NAR = ENG / "chars/naruto"
JIN = ENG / "chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/naruto/audit-size-v1"
OUT.mkdir(parents=True, exist_ok=True)

BASE = 0.18  # [Size] xscale


def body_h(im: Image.Image) -> int:
    a = np.array(im.convert("RGBA"))
    ys = np.where(a[:, :, 3] > 20)[0]
    if len(ys) == 0:
        return 0
    return int(ys.max() - ys.min() + 1)


def parse_air(path: Path):
    text = path.read_text(encoding="latin-1", errors="replace")
    actions = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"\[Begin Action\s+(-?\d+)\]", line, re.I)
        if m:
            current = int(m.group(1))
            actions[current] = []
            continue
        if current is None:
            continue
        s = line.split(";")[0].strip()
        if not s or s.startswith("Clsn") or s.startswith("Loop") or s.startswith("Interpolate"):
            continue
        if not re.match(r"^-?\d+\s*,", s):
            continue
        parts = [p.strip() for p in s.split(",")]
        if len(parts) < 5:
            continue
        try:
            g, i = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        xs = ys = 1.0
        if len(parts) >= 9 and parts[7] and parts[8]:
            try:
                xs = float(parts[7])
                ys = float(parts[8])
            except ValueError:
                pass
        actions[current].append((g, i, xs, ys))
    return actions


def main():
    nsff = Sff(NAR / "Naruto_Ashura_JUS.sff")
    jsff = Sff(JIN / "spr.sff")

    # portraits
    portraits = [(g, i) for (g, i) in nsff.keys if g in (9000, 9001)]
    print("PORTRAITS", sorted(portraits)[:40], "count", len(portraits))
    board_items = []
    for key in sorted(k for k in nsff.keys if k[0] == 9000):
        im = nsff.decode(nsff.keys[key])
        im.save(OUT / f"portrait-{key[0]}-{key[1]}.png")
        print(f"  {key} {im.size}")
        board_items.append((key, im))

    # idle reference
    idle = nsff.decode(nsff.keys[(0, 0)])
    idle_h = body_h(idle)
    idle_screen = idle_h * BASE
    print(f"IDLE sprite H={idle_h} screen~{idle_screen:.1f}px at scale {BASE}")

    actions = parse_air(NAR / "Naruto_Ashura_JUS.air")
    rows = []
    for act, frames in actions.items():
        heights = []
        for g, i, xs, ys in frames[:8]:
            if (g, i) not in nsff.keys or g < 0:
                continue
            h = body_h(nsff.decode(nsff.keys[(g, i)]))
            if h <= 0:
                continue
            heights.append(h * BASE * ys)
        if not heights:
            continue
        med = float(np.median(heights))
        ratio = med / max(1, idle_screen)
        if ratio > 1.25 or ratio < 0.7:
            rows.append((ratio, act, round(med, 1), frames[0]))
    rows.sort(reverse=True)
    print("\nGROW/SHRINK actions (screen height vs idle):")
    for ratio, act, med, fr in rows[:40]:
        print(f"  act {act:5d} screen~{med:6.1f} x{ratio:.2f} first={fr}")

    # Kurama sprites
    print("\nKURAMA / 2300 group")
    kkeys = sorted(k for k in nsff.keys if k[0] in (2300, 2200))
    print(" count", len(kkeys), "sample", kkeys[:12])
    for key in [(2300, 12), (2300, 13), (2300, 0), (2200, 72)]:
        if key not in nsff.keys:
            print(" missing", key)
            continue
        im = nsff.decode(nsff.keys[key])
        h = body_h(im)
        im.save(OUT / f"kurama-{key[0]}-{key[1]}.png")
        print(f"  {key} {im.size} bodyH={h} at AIR 5.833 screen~{h*BASE*5.833:.0f} at player 0.18 only~{h*BASE:.0f}")

    # Jinwoo summons
    print("\nJINWOO SUMMONS")
    for label, key, air_scale, char_scale in [
        ("tusk", (200, 29), 0.224, 1.0),
        ("kaisel", (1000, 27), 0.06, 1.0),
        ("igris-ish", (1000, 20), 0.075, 1.0),
    ]:
        if key not in jsff.keys:
            print(" missing", label, key)
            continue
        im = jsff.decode(jsff.keys[key])
        h = body_h(im)
        # jinwoo char xscale from cns is 1.5
        screen = h * 1.5 * air_scale
        im.thumbnail((400, 400))
        im.save(OUT / f"jinwoo-{label}.png")
        print(f"  {label} {key} bodyH={h} char1.5 * air {air_scale} => screen~{screen:.0f}")

    if board_items:
        cell = 180
        cols = min(6, len(board_items))
        rows_n = (len(board_items) + cols - 1) // cols
        board = Image.new("RGB", (cols * cell, rows_n * cell + 24), (30, 30, 36))
        draw = ImageDraw.Draw(board)
        draw.text((8, 4), "Naruto group 9000 portraits", fill=(240, 240, 250))
        for n, (key, im) in enumerate(board_items[:18]):
            fit = im.convert("RGBA").copy()
            fit.thumbnail((cell - 16, cell - 28))
            x = (n % cols) * cell + (cell - fit.width) // 2
            y = 24 + (n // cols) * cell + (cell - 28 - fit.height) // 2
            board.paste(fit, (x, y), fit)
            draw.text(((n % cols) * cell + 4, 24 + (n // cols) * cell + cell - 22), f"{key[0]},{key[1]}", fill=(255, 220, 80))
        board.save(OUT / "portraits-board.jpg", quality=90)
    print("OUT", OUT)


if __name__ == "__main__":
    main()
