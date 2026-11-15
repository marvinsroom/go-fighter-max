"""Key, validate and register Jinwoo's fixed-cell combat-v2 atlases."""
from pathlib import Path
import json

import numpy as np
from PIL import Image
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'sprite-fighter/characters/jinwoo/art/combat-v2'
NAMES = (
    'ground', 'air-low', 'special', 'reactions',
    'normal-locomotion', 'normal-reactions',
    'sword-ground', 'sword-air-special', 'sword-reactions-finishers',
)
COLS, ROWS = 4, 3


def key_green(source):
    pixels = np.asarray(source.convert('RGBA')).copy()
    rgb = pixels[:, :, :3].astype(np.int16)
    green = ((rgb[:, :, 1] > 90) &
             (rgb[:, :, 1] - rgb[:, :, 0] > 20) &
             (rgb[:, :, 1] - rgb[:, :, 2] > 20))
    green = ndimage.binary_dilation(green, iterations=1)
    distance = ndimage.distance_transform_edt(~green)
    alpha = np.clip(distance * 170, 0, 255).astype(np.uint8)
    alpha[distance >= 1.5] = 255
    pixels[:, :, 3] = alpha
    # Despill green from antialiased edge pixels.
    edge = (alpha > 0) & (alpha < 255)
    pixels[:, :, 1][edge] = np.minimum(
        pixels[:, :, 1][edge],
        np.maximum(pixels[:, :, 0][edge], pixels[:, :, 2][edge]),
    )
    return Image.fromarray(pixels, 'RGBA')


prepared = {}
all_tiles = []
for name in NAMES:
    image = key_green(Image.open(FOLDER / 'source' / f'{name}.png'))
    if image.size != (1536, 1024):
        image = image.resize((1536, 1024), Image.Resampling.LANCZOS)
    w, h = image.size
    assert w % COLS == 0 and h >= ROWS
    cw, ch = w // COLS, h // ROWS
    rgba = np.asarray(image)
    labels, count = ndimage.label(rgba[:, :, 3] > 24)
    components = []
    for component, obj in enumerate(ndimage.find_objects(labels), 1):
        if obj is None:
            continue
        area = int((labels[obj] == component).sum())
        if area < 20:
            continue
        cy = (obj[0].start + obj[0].stop) / 2
        cx = (obj[1].start + obj[1].stop) / 2
        components.append({'id': component, 'area': area, 'cx': cx, 'cy': cy})
    seeds = sorted(components, key=lambda item: item['area'], reverse=True)[:COLS*ROWS]
    assert len(seeds) == COLS*ROWS, (name, len(seeds))
    seeds.sort(key=lambda item: item['cy'])
    ordered = []
    for row in range(ROWS):
        ordered.extend(sorted(seeds[row*COLS:(row+1)*COLS], key=lambda item: item['cx']))
    buckets = [[seed['id']] for seed in ordered]
    seed_ids = {seed['id'] for seed in seeds}
    for item in components:
        if item['id'] in seed_ids:
            continue
        nearest = min(range(len(ordered)), key=lambda i: (ordered[i]['cx']-item['cx'])**2 + (ordered[i]['cy']-item['cy'])**2)
        buckets[nearest].append(item['id'])
    tiles = []
    for index, ids in enumerate(buckets):
            assert ids, (name, index, 'empty')
            mask = np.isin(labels, ids)
            ys, xs = np.where(mask)
            bounds = (int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1)
            isolated = rgba[bounds[1]:bounds[3], bounds[0]:bounds[2]].copy()
            isolated[:, :, 3] = np.where(mask[bounds[1]:bounds[3], bounds[0]:bounds[2]], isolated[:, :, 3], 0)
            tile = Image.fromarray(isolated)
            tiles.append(tile)
            all_tiles.append(tile)
    prepared[name] = (w, h, cw, ch, tiles)

# One reduction factor for the complete replacement bank keeps anatomy size stable. Recenter
# every result inside its cell with a guaranteed transparent safety gutter.
PAD = 12
scale = min(1.0, min((cw-2*PAD)/tile.width for tile in all_tiles),
            min((ch-2*PAD)/tile.height for tile in all_tiles))
registration = {'version': 2, 'grid': [COLS, ROWS], 'padding': PAD,
                'uniform_scale': scale, 'sheets': {}}
for name, (w, h, cw, ch, tiles) in prepared.items():
    output = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    frames = []
    for index, tile in enumerate(tiles):
        row, col = divmod(index, COLS)
        if scale < 1:
            tile = tile.resize((max(1, round(tile.width*scale)), max(1, round(tile.height*scale))),
                               Image.Resampling.LANCZOS)
        x1, y1 = col*cw, row*ch
        x = x1 + (cw-tile.width)//2
        y = y1 + ch-PAD-tile.height
        output.alpha_composite(tile, (x, y))
        bounds = (x-x1, y-y1, x-x1+tile.width, y-y1+tile.height)
        margin = min(bounds[0], bounds[1], cw-bounds[2], ch-bounds[3])
        assert margin >= PAD-1, (name, row, col, bounds, margin)
        frames.append({'rect': [x1, y1, x1+cw, y1+ch], 'bounds': list(bounds), 'margin': margin})
    output.save(FOLDER / f'{name}.png')
    registration['sheets'][name] = {'file': f'{name}.png', 'size': [w, h], 'frames': frames}

(FOLDER / 'registration.json').write_text(json.dumps(registration, indent=2), encoding='utf-8')
print('JINWOO_COMBAT_V2_INSTALLED', sum(len(s['frames']) for s in registration['sheets'].values()), 'frames')
