"""Jinwoo v75 idle art: full-body stance, near hand in coat pocket, weapon low.

The old sword/dagger idle drawings (61017,0 / 61016,0) are cropped at the
shins, so he always looked sunk into the floor. This builds idle sprites from
the full-body relaxed stance 61013,24 (shoes included): the near hand is
removed below the wrist, the coat is inpainted behind it and a pocket opening
is drawn; the far hand holds the extracted longsword (61091,14) low with the
tip toward the floor. Writes PNGs only; the installer packs them.
"""
import math, sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from mugen_sff import Sff

LIVE = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo'
OUT = ROOT / 'sprite-fighter/characters/jinwoo-mugen/idle-v75'

HAND_BOX = (104, 232, 144, 286)      # near (viewer-left) hand, sprite px
POCKET = ((105, 241), (140, 236))    # pocket opening across the wrist
COAT_EDGE = ((104, 240), (97, 289))  # bulged coat edge under the hand
FAR_GRIP = (282, 268)                # far fist centre, sprite px
# Output is built at the longsword bank's resolution (61017 frame scale) so the
# extracted sword is used 1:1; the full-body stance is downscaled to match.
BODY_K = 0.096128000 / 0.196294992   # 61013 -> 61017 pixel ratio (both axes)
GRIP_FROM_MID = 76                   # v72 sword canvas: hand just under the guard
TIP_CLEAR = 6                        # tip stops this far above the soles
DAGGER_K = 0.167301691 / 0.208072691  # 61016 -> 61017 pixel ratio
DAGGER_FIST = (219, 187)             # far fist on 61016,0 (dagger hilt inside)
DAGGER_TIP = (288, 228)
DAGGER_HALF = 13                     # half width of the blade + glow strip


def pocket_hand(base):
    rgba = np.array(base).copy()
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = HAND_BOX
    r, g, b, a = (rgba[..., k].astype(int) for k in range(4))
    skin = (r > 150) & (g > 95) & (b < 175) & (r > b + 30) & (a > 0)
    top = POCKET[1][1] + 2                       # forearm stays above this
    hand = np.zeros((h, w), np.uint8)
    hand[y0:y1, x0:x1] = skin[y0:y1, x0:x1].astype(np.uint8) * 255
    hand = cv2.dilate(hand, np.ones((9, 9), np.uint8))
    hand[:top, :] = 0
    # A hand in the pocket pushes the coat out: its edge now runs from the
    # wrist down to where the original coat edge resumes below the hand.
    yy, xx = np.mgrid[0:h, 0:w]
    (ex0, ey0), (ex1, ey1) = COAT_EDGE
    edge_x = ex0 + (yy - ey0) * (ex1 - ex0) / (ey1 - ey0)
    region = (yy >= top) & (yy <= ey1) & (xx >= edge_x) & (xx < x1)
    hole = (hand > 0) | (region & (a < 128))
    coat = region | ((hand > 0) & (xx >= edge_x))
    # Flat coat cloth: median of the dark coat pixels around the hand (inpainting
    # smeared forearm skin and lining purple into the patch).
    near = np.zeros((h, w), bool)
    near[y0 - 10:y1 + 20, x0 - 10:x1 + 30] = True
    lum = (r + g + b) / 3
    cloth = near & ~hole & (a > 200) & (lum < 70) & (np.abs(r - b) < 20)
    colour = np.median(rgba[cloth][:, :3], axis=0).astype(np.uint8)
    shade = np.clip((xx - edge_x) / 30.0, 0, 1)[..., None]       # a touch lighter inward
    fill = np.clip(colour[None, None, :] * (0.85 + 0.25 * shade), 0, 255).astype(np.uint8)
    rgba[..., :3] = np.where(hole[..., None], fill, rgba[..., :3])
    rgba[..., 3] = np.where(hole & coat, 255, np.where(hole & ~coat, 0, rgba[..., 3]))
    img = Image.fromarray(rgba).copy()
    d = ImageDraw.Draw(img)
    d.line([COAT_EDGE[0], COAT_EDGE[1]], fill=(8, 8, 10, 255), width=3)        # bulged coat outline
    (px0, py0), (px1, py1) = POCKET
    d.line([(px0, py0 + 2), (px1, py1 + 2)], fill=(16, 16, 20, 255), width=3)   # pocket opening
    d.line([(px0 + 2, py0 + 5), (px1 - 1, py1 + 5)], fill=(62, 60, 72, 255), width=1)  # lip highlight
    return img


def sword_low(sff, floor, grip_at):
    """Longsword 61091,14 (upright) rotated so the tip points forward-down."""
    sw = sff.decode(sff.keys[(61091, 14)]).convert('RGBA')
    a = np.array(sw)[..., 3] > 40
    ys, xs = np.nonzero(a)
    pts = np.stack([xs, ys], 1).astype(float)
    mid = np.array([sw.width / 2, sw.height / 2])
    _, _, vt = np.linalg.svd(pts - pts.mean(0), full_matrices=False)
    axis = vt[0] if vt[0][1] > 0 else -vt[0]            # unit vector toward pommel
    grip = mid + axis * GRIP_FROM_MID
    tip_len = float(((pts - grip) @ -axis).max())       # grip -> tip
    drop = (floor - TIP_CLEAR) - grip_at[1]
    ang = math.degrees(math.asin(max(-1, min(1, drop / tip_len))))
    cur = math.degrees(math.atan2(-axis[1], -axis[0]))  # current tip direction
    rot = cur - ang                                     # PIL rotates counter-clockwise
    big = Image.new('RGBA', (sw.width * 3, sw.height * 3))
    centre = (sw.width * 3 // 2, sw.height * 3 // 2)
    big.paste(sw, (centre[0] - round(grip[0]), centre[1] - round(grip[1])))
    big = big.rotate(rot, resample=Image.BICUBIC, center=centre)
    return big, centre, ang


def dagger_low(sff):
    """Far-hand Antares dagger cut from 61016,0 along its blade line."""
    src = np.array(sff.decode(sff.keys[(61016, 0)]).convert('RGBA'))
    h, w = src.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    f, t = np.array(DAGGER_FIST, float), np.array(DAGGER_TIP, float)
    d = (t - f) / np.linalg.norm(t - f)
    n = np.array([-d[1], d[0]])
    along = (xx - f[0]) * d[0] + (yy - f[1]) * d[1]
    perp = (xx - f[0]) * n[0] + (yy - f[1]) * n[1]
    r, g, b = (src[..., k].astype(int) for k in range(3))
    skin = (r > 150) & (g > 95) & (r > b + 30)
    keep = (along > -8) & (along < np.linalg.norm(t - f) + 10) & (np.abs(perp) < DAGGER_HALF) & ~skin
    out = src.copy()
    out[~keep, 3] = 0
    img = Image.fromarray(out).copy()
    img = img.resize((round(w * DAGGER_K), round(h * DAGGER_K)), Image.LANCZOS)
    return img, (round(f[0] * DAGGER_K), round(f[1] * DAGGER_K))


def compose(body, layer, anchor, grip_at):
    """Sword behind the body; canvas grown to fit both; returns image + axis shift."""
    lb = layer.getbbox()
    ox, oy = round(grip_at[0]) - anchor[0], round(grip_at[1]) - anchor[1]
    x0 = min(0, ox + lb[0]); y0 = min(0, oy + lb[1])
    x1 = max(body.width, ox + lb[2]); y1 = max(body.height, oy + lb[3])
    canvas = Image.new('RGBA', (x1 - x0, y1 - y0))
    canvas.alpha_composite(layer, (ox - x0, oy - y0))
    canvas.alpha_composite(body, (-x0, -y0))
    return canvas, (-x0, -y0)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sff = Sff(LIVE / 'spr.sff')
    i = sff.keys[(61013, 24)]
    body = pocket_hand(sff.decode(i).convert('RGBA'))
    body.save(OUT / 'idle-pocket-full.png')
    ax, ay = sff.headers[i][4:6]
    body = body.resize((round(body.width * BODY_K), round(body.height * BODY_K)), Image.LANCZOS)
    alpha = np.array(body)[..., 3]
    floor = int(np.nonzero(alpha.max(1) > 40)[0].max())  # sole line
    grip_at = (FAR_GRIP[0] * BODY_K, FAR_GRIP[1] * BODY_K)
    layer, anchor, ang = sword_low(sff, floor, grip_at)
    img, shift = compose(body, layer, anchor, grip_at)
    img.save(OUT / 'idle-sword.png')
    dlayer, danchor = dagger_low(sff)
    dimg, dshift = compose(body, dlayer, danchor, grip_at)
    dimg.save(OUT / 'idle-dagger.png')
    daxis = (round(ax * BODY_K) + dshift[0], floor + dshift[1])
    body.save(OUT / 'idle-pocket.png')
    axis = (round(ax * BODY_K) + shift[0], floor + shift[1])
    (OUT / 'idle-axis.txt').write_text(
        f'pocket {round(ax * BODY_K)},{floor}\nsword {axis[0]},{axis[1]}\n'
        f'dagger {daxis[0]},{daxis[1]}\nangle {ang:.1f}\n')
    prev = Image.new('RGBA', img.size, (200, 200, 210, 255)); prev.alpha_composite(img)
    ImageDraw.Draw(prev).line([(0, axis[1]), (img.width, axis[1])], fill=(255, 0, 0, 255))
    dprev = Image.new('RGBA', dimg.size, (200, 200, 210, 255)); dprev.alpha_composite(dimg)
    both = Image.new('RGBA', (prev.width + dprev.width, max(prev.height, dprev.height)), (200, 200, 210, 255))
    both.paste(prev, (0, 0)); both.paste(dprev, (prev.width, 0)); prev = both
    prev = prev.resize((prev.width * 2, prev.height * 2), Image.LANCZOS)
    prev.convert('RGB').save(OUT / 'idle-sword-preview.png')
    print('floor', floor, 'axis', axis, 'angle', round(ang, 1), 'size', img.size)


if __name__ == '__main__':
    main()
