"""Check Jinwoo v76 redraw PNGs against REDRAW_SPEC.md before installing.

Reports missing files per tier and, for each image: canvas size, transparent
background, nothing touching the canvas edge, soles on the floor line for
grounded poses, and standing height for idle frames.
Usage: python scripts/check-jinwoo-redraw-v76.py [--tier N]
"""
import argparse, json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'sprite-fighter/characters/jinwoo-mugen/redraw-v76'
INCOMING = DIR / 'incoming'

CANVAS, FLOOR, HEIGHT = 1024, 960, 600
FLOOR_TOL, HEIGHT_TOL = 4, 24

BOTH = ('sword', 'dagger')
TIERS = {
    1: [(BOTH, 'idle', 4), (BOTH, 'walk', 8), (BOTH, 'walkback', 6), (BOTH, 'run', 6),
        (BOTH, 'dashback', 2), (BOTH, 'jump', 5), (BOTH, 'crouch', 2), (BOTH, 'turn', 2),
        (BOTH, 'guard', 3)],
    2: [(BOTH, p, 3) for p in ('light', 'light2', 'medium', 'heavy', 'finisher', 'dashslash',
                               'launcher', 'crouchlight', 'crouchmedium', 'sweep', 'airlight',
                               'airmedium', 'airheavy', 'airspike', 'throw')],
    3: [(('body',), 'hithigh', 2), (('body',), 'hitlow', 2), (('body',), 'hitcrouch', 1),
        (('body',), 'hitair', 2), (('body',), 'liedown', 1), (('body',), 'getup', 2),
        (('body',), 'ko', 1), (('body',), 'dizzy', 1)],
    4: [(('sword',), p, 3) for p in ('arise', 'rulersauthority', 'bladefall', 'mutilate',
                                     'dragonfear', 'monarchdomain', 'baransword', 'charge',
                                     'taunt', 'intro', 'win')] + [(('dagger',), 'antaresgambit', 3)],
}
# Frames whose soles are off the floor on purpose.
AIRBORNE = {('dashback', 1), ('jump', 1), ('jump', 2), ('jump', 3), ('guard', 2),
            ('airlight', None), ('airmedium', None), ('airheavy', None), ('airspike', None),
            ('hitair', None), ('bladefall', 0)}
NOT_FEET = {'liedown', 'ko', 'getup', 'hitair', 'monarchdomain'}  # lowest pixel is not a sole


def expected(tiers):
    for t in tiers:
        for sets, pose, n in TIERS[t]:
            for s in sets:
                for f in range(n):
                    yield t, f'{s}-{pose}-{f}.png', pose, f


def check(path, pose, frame):
    issues = []
    im = Image.open(path)
    if im.size != (CANVAS, CANVAS):
        issues.append(f'canvas {im.size}, want {CANVAS}x{CANVAS}')
    if im.mode != 'RGBA':
        return issues + [f'mode {im.mode}, want RGBA']
    a = np.array(im)[..., 3]
    if (a[0, :] > 0).any() or (a[:, 0] > 0).any() or (a[:, -1] > 0).any():
        issues.append('drawing touches the canvas edge (cropped?)')
    corners = [a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]
    if max(corners) > 0:
        issues.append('background not transparent')
    rows = np.nonzero(a.max(1) > 40)[0]
    if not len(rows):
        return issues + ['empty image']
    top, bottom = int(rows.min()), int(rows.max())
    airborne = (pose, frame) in AIRBORNE or (pose, None) in AIRBORNE
    if not airborne and pose not in NOT_FEET and abs(bottom - FLOOR) > FLOOR_TOL:
        issues.append(f'soles at y={bottom}, want {FLOOR}±{FLOOR_TOL}')
    if pose == 'idle' and abs((bottom - top) - HEIGHT) > HEIGHT_TOL:
        issues.append(f'standing height {bottom - top}px, want {HEIGHT}±{HEIGHT_TOL}')
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tier', type=int, action='append', help='limit to tier(s)')
    tiers = ap.parse_args().tier or sorted(TIERS)
    report = {'missing': [], 'problems': {}, 'ok': 0}
    for t, name, pose, frame in expected(tiers):
        p = INCOMING / name
        if not p.exists():
            report['missing'].append(name)
            continue
        issues = check(p, pose, frame)
        if issues:
            report['problems'][name] = issues
        else:
            report['ok'] += 1
    every = {name for _, name, _, _ in expected(TIERS)}
    stray = sorted(p.name for p in INCOMING.glob('*.png') if p.name not in every)
    report['unrecognised'] = stray
    (DIR / 'check-v76.json').write_text(json.dumps(report, indent=2))
    total = report['ok'] + len(report['problems']) + len(report['missing'])
    print(f"tiers {tiers}: {report['ok']}/{total} ok, {len(report['problems'])} with problems, "
          f"{len(report['missing'])} missing, {len(stray)} unrecognised")
    for name, issues in list(report['problems'].items())[:20]:
        print(' ', name, '-', '; '.join(issues))


if __name__ == '__main__':
    main()
