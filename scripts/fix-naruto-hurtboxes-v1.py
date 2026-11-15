"""Naruto v1: rescale collision boxes to his high-resolution body art.

The live SFF replaced the original ~50px body sprites with ~4.5x larger
drawings and dropped [Size] to 0.18, but the AIR Clsn1/Clsn2 boxes kept the
original 1.0-scale numbers, so the engine shrank them to a sliver at his feet.
Every box that belongs to a frame drawn with a replaced body sprite is scaled
by live_height / upstream_height of that sprite. Effect sprites (ratio ~1) and
helpers with their own size are untouched. Idempotent from the backup.
"""
import re, shutil, struct, sys, json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from mugen_sff import Sff

LIVE = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto'
UP = ROOT / 'sprite-fighter/characters/naruto/source/upstream/Naruto_JUS2'
OUT = ROOT / 'sprite-fighter/characters/naruto-hurtbox-v1'
AIR = 'Naruto_Ashura_JUS.air'
BACKUP = OUT / 'live-before-v1' / AIR


def upstream_heights():
    d = (UP / 'Naruto_Ashura_JUS.sff').read_bytes()
    _, count, off = struct.unpack_from('<III', d, 16)
    heights, order = {}, []
    for _ in range(count):
        nxt, ln, _ax, _ay, g, n, link = struct.unpack_from('<IIhhHHH', d, off)
        if ln == 0:
            h = order[link]
        else:
            _x0, y0, _x1, y1 = struct.unpack_from('<HHHH', d, off + 36)
            h = y1 - y0 + 1
        order.append(h)
        heights.setdefault((g, n), h)
        if nxt == 0:
            break
        off = nxt
    return heights


def sprite_ratios():
    up = upstream_heights()
    live = Sff(LIVE / 'Naruto_Ashura_JUS.sff')
    ratios = {}
    for key, i in live.keys.items():
        if key in up and up[key] > 0:
            r = live.headers[i][3] / up[key]
            if r > 2:  # replaced body art; effects stay ~1
                ratios[key] = r
    return ratios


BOX = re.compile(r'^(\s*Clsn[12]\[\d+\]\s*=\s*)(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)(.*)$', re.I)
FRAME = re.compile(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,')
ACTION = re.compile(r'^\s*\[Begin Action', re.I)


def main():
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(LIVE / AIR, BACKUP)
    ratios = sprite_ratios()
    lines = BACKUP.read_bytes().decode('latin-1').splitlines(keepends=True)

    # Group lines into actions; resolve each box line to the frame it describes.
    actions, cur = [], []
    for ln in lines:
        if ACTION.match(ln) and cur:
            actions.append(cur); cur = []
        cur.append(ln)
    actions.append(cur)

    out, changed_boxes, changed_actions = [], 0, 0
    for act in actions:
        frame_ratio = []  # ratio of each frame line, in order
        for ln in act:
            m = FRAME.match(ln)
            if m and not BOX.match(ln):
                frame_ratio.append(ratios.get((int(m.group(1)), int(m.group(2)))))
        body = [r for r in frame_ratio if r]
        default_r = median(body) if body else None
        fi, in_default, touched = 0, False, False
        for ln in act:
            low = ln.strip().lower()
            if low.startswith('clsn2default') or low.startswith('clsn1default'):
                in_default = True
            elif re.match(r'clsn[12]\s*:', low):
                in_default = False
            m = BOX.match(ln)
            if m:
                r = default_r if in_default else (frame_ratio[fi] if fi < len(frame_ratio) else None)
                if r:
                    nums = [round(int(m.group(k)) * r) for k in range(2, 6)]
                    ln = m.group(1) + ', '.join(str(n) for n in nums) + m.group(6) + ('\n' if ln.endswith('\n') else '')
                    changed_boxes += 1; touched = True
            elif FRAME.match(ln):
                fi += 1
            out.append(ln)
        changed_actions += touched

    (LIVE / AIR).write_text(''.join(out), encoding='latin-1', newline='')
    report = {'body_sprites': len(ratios), 'actions': changed_actions, 'boxes': changed_boxes,
              'median_ratio': round(median(ratios.values()), 3)}
    (OUT / 'install-v1.json').write_text(json.dumps(report, indent=2))
    print(report)


if __name__ == '__main__':
    main()
