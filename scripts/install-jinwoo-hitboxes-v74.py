"""Jinwoo v74: attack/hurt boxes that match what is drawn.

1. 320 dash slash: the only Clsn1 sat on elem 3, after the 18/tick dash had
   already carried him ~100 units past a close opponent. The dash frame now
   cuts too and the follow-through box reaches back over the dash path.
2. 1400/2100 sky drops (helpers 1410/1411/2100/2120) fell at a fixed 110
   units ahead; they now land on the opponent (clamped 40..200).
   320 only turns around when the opponent is actually behind him, so the
   dash always goes through them instead of away from them.
3. Clsn2 hurtboxes are trimmed to the drawn sprite (+margin) so he can no
   longer be hit in the empty air above his head or behind his coat.
   Boxes only ever shrink; a box that does not overlap its sprite is kept.
Idempotent from the backup.
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from mugen_sff import Sff

LIVE = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo'
OUT = ROOT / 'sprite-fighter/characters/jinwoo-mugen/hitboxes-v74'
BACKUP = OUT / 'live-before-v74'
FILES = ['anim.air', 'cns.cns', 'Mode.cns']
MARGIN = 3

DASH_ACTIONS = {320, 500320, 700320}
DASH_BOXES = {2: (-20, -47, 60, -4), 3: (-90, -47, 48, -4)}  # elem -> Clsn1
AIM = 'x = max(40,min(200,cond(numenemy>0,p2dist x,110)))'

BOX = re.compile(r'^(\s*Clsn([12])\[\d+\]\s*=\s*)(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)(.*?)(\r?\n?)$', re.I)
FRAME = re.compile(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)(.*?)(\r?\n?)$')
ACTION = re.compile(r'^\s*\[Begin Action\s+(-?\d+)', re.I)
HEADER = re.compile(r'^\s*Clsn([12])(Default)?\s*:\s*\d+', re.I)


def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if not (BACKUP / f).exists():
            shutil.copy2(LIVE / f, BACKUP / f)


def read(f):
    return (BACKUP / f).read_bytes().decode('latin-1').splitlines(keepends=True)


def frame_extent(sff, cache, g, n, x, y, rest):
    """Sprite bounds in Clsn coordinates (axis-relative, before [Size])."""
    key = (g, n)
    if key not in cache:
        i = sff.keys.get(key)
        bb = None
        if i is not None:
            img = sff.decode(i)
            bb = img.getchannel('A').getbbox()
            if bb:
                ax, ay = sff.headers[i][4:6]
                bb = (bb[0] - ax, bb[1] - ay, bb[2] - ax, bb[3] - ay)
        cache[key] = bb
    bb = cache[key]
    if not bb:
        return None
    parts = [p.strip() for p in rest.split(',')]
    flip = parts[1].upper() if len(parts) > 1 else ''
    sx = float(parts[3]) if len(parts) > 3 and parts[3] else 1.0
    sy = float(parts[4]) if len(parts) > 4 and parts[4] else 1.0
    x0, y0, x1, y1 = bb[0] * sx, bb[1] * sy, bb[2] * sx, bb[3] * sy
    if 'H' in flip:
        x0, x1 = -x1, -x0
    if 'V' in flip:
        y0, y1 = -y1, -y0
    return (x + x0, y + y0, x + x1, y + y1)


def trim(box, ext):
    a = [min(box[0], box[2]), min(box[1], box[3]), max(box[0], box[2]), max(box[1], box[3])]
    e = (ext[0] - MARGIN, ext[1] - MARGIN, ext[2] + MARGIN, ext[3] + MARGIN)
    t = [max(a[0], e[0]), max(a[1], e[1]), min(a[2], e[2]), min(a[3], e[3])]
    if t[0] >= t[2] or t[1] >= t[3]:
        return None  # no overlap: leave the authored box alone
    return [round(v) for v in t]


def fix_air(stats):
    sff = Sff(LIVE / 'spr.sff')
    cache = {}
    lines = read('anim.air')
    actions, cur = [], []
    for ln in lines:
        if ACTION.match(ln) and cur:
            actions.append(cur); cur = []
        cur.append(ln)
    actions.append(cur)

    out = []
    for act in actions:
        m = ACTION.match(act[0])
        num = int(m.group(1)) if m else None
        # Frame extents in order, and which frame each box line belongs to.
        extents = []
        for ln in act:
            fm = FRAME.match(ln)
            if fm and not BOX.match(ln) and not ACTION.match(ln):
                g, n, x, y = (int(fm.group(k)) for k in range(1, 5))
                extents.append(frame_extent(sff, cache, g, n, x, y, fm.group(6)) if g >= 0 else None)
        valid = [e for e in extents if e]
        union = (min(e[0] for e in valid), min(e[1] for e in valid),
                 max(e[2] for e in valid), max(e[3] for e in valid)) if valid else None

        fi, default, kind = 0, False, None
        new = []
        for ln in act:
            hm = HEADER.match(ln)
            if hm:
                kind, default = hm.group(1), bool(hm.group(2))
                # Dash slash: replace the Clsn1 block on elem 3 below.
                new.append(ln); continue
            bm = BOX.match(ln)
            if bm:
                if bm.group(2) == '2':
                    ext = union if default else (extents[fi] if fi < len(extents) else None)
                    box = [int(bm.group(k)) for k in range(3, 7)]
                    t = trim(box, ext) if ext else None
                    if t and t != [min(box[0], box[2]), min(box[1], box[3]), max(box[0], box[2]), max(box[1], box[3])]:
                        ln = bm.group(1) + ', '.join(map(str, t)) + bm.group(7) + bm.group(8)
                        stats['hurtboxes_trimmed'] += 1
                elif num in DASH_ACTIONS and (fi + 1) in DASH_BOXES:
                    b = DASH_BOXES[fi + 1]
                    ln = bm.group(1) + ', '.join(map(str, b)) + bm.group(7) + bm.group(8)
                    stats['dash_boxes'] += 1
                new.append(ln); continue
            fm = FRAME.match(ln)
            if fm and not ACTION.match(ln):
                # Dash slash: give elem 2 a Clsn1 if it has none.
                if num in DASH_ACTIONS and fi + 1 == 2 and not any(
                        re.match(r'\s*Clsn1\s*:', p, re.I) for p in new[-4:]):
                    eol = '\r\n' if ln.endswith('\r\n') else '\n'
                    b = DASH_BOXES[2]
                    new.append('Clsn1: 1' + eol)
                    new.append('  Clsn1[0] = ' + ', '.join(map(str, b)) + eol)
                    stats['dash_boxes'] += 1
                fi += 1
            new.append(ln)
        out.extend(new)
    (LIVE / 'anim.air').write_bytes(''.join(out).encode('latin-1'))


def fix_drops(stats):
    for f in ('cns.cns', 'Mode.cns'):
        lines = read(f)
        for i, ln in enumerate(lines):
            if re.match(r'^\s*x\s*=\s*110\s*(;.*)?\r?$', ln.rstrip('\n')) and i + 1 < len(lines) \
                    and re.match(r'^\s*y\s*=\s*-500', lines[i + 1]):
                eol = '\r\n' if ln.endswith('\r\n') else '\n'
                lines[i] = AIM + eol
                stats['drops_aimed'] += 1
        (LIVE / f).write_bytes(''.join(lines).encode('latin-1'))


def fix_dash_turn(stats):
    lines = (LIVE / 'cns.cns').read_bytes().decode('latin-1').splitlines(keepends=True)
    in320 = False
    for i, ln in enumerate(lines):
        if re.match(r'^\s*\[Statedef', ln, re.I):
            in320 = re.match(r'^\s*\[Statedef\s+320\s*\]', ln, re.I) is not None
        if in320 and re.match(r'^\s*type\s*=\s*Turn\s*$', ln.rstrip('\r\n'), re.I) \
                and re.match(r'^\s*trigger1\s*=\s*!time\s*$', lines[i + 1].rstrip('\r\n'), re.I):
            eol = '\r\n' if lines[i + 1].endswith('\r\n') else '\n'
            lines[i + 1] = 'trigger1 = !time && p2dist x < 0' + eol
            stats['dash_turn'] += 1
    (LIVE / 'cns.cns').write_bytes(''.join(lines).encode('latin-1'))


def main():
    backup()
    stats = {'hurtboxes_trimmed': 0, 'dash_boxes': 0, 'drops_aimed': 0, 'dash_turn': 0}
    fix_air(stats)
    fix_drops(stats)
    fix_dash_turn(stats)  # after fix_drops, which rewrites cns.cns from backup
    (OUT / 'install-v74.json').write_text(json.dumps(stats, indent=2))
    print(stats)


if __name__ == '__main__':
    main()
