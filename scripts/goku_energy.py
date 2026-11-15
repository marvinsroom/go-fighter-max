"""Dedicated charge, firing and projectile drawings, retaining native AIR events."""
from PIL import Image
from isolated_sprite_atlas import extract
import json

SPECIAL_OFFSETS = (0, 24000, 26000, 28000, 30000, 32000)
COMMON_OFFSETS = (0, 2000, 11000, 13000, 15000, 17000)


def body_frame(action, index, total):
    if action == 31200:
        # Native barrage loops exact elements 4–6 while the bullets are emitted.
        return [11, 11, 12, 13, 14, 13, 15][min(index, 6)]
    ultimates = {
        3200: [0, 1, 2, 3, 3, 4, 5, 6, 7, 7, 8, 9],
        3400: [0, 1, 2, 3, 3, 3, 3, 4, 5, 6, 7, 9],
        4000: [0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 9],
        4100: [0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 9],
        4300: [0, 1, 2, 3] + [3] * 12 + [5],
    }
    if action in ultimates:
        return ultimates[action][min(index, len(ultimates[action]) - 1)]
    if action == 31500:
        return [1, 3, 4, 5, 9][min(index, 4)]
    if action == 37500:
        return [11, 11, 12, 13, 14, 15, 10][min(index, 6)]
    for offset in SPECIAL_OFFSETS:
        local = action - offset
        if local == 1400:
            return min(3, index * 4 // total)
        if local in (1401, 1402, 1701):
            return [4, 5, 6, 7, 8, 9][min(5, index * 6 // total)]
        if local == 1700:
            return min(3, 1 + index * 3 // total)
        if local == 1500:
            return [11, 12, 12, 11, 13, 14, 13, 14, 15][min(8, index * 9 // total)]
        if local == 1580:
            return 11
    for offset in COMMON_OFFSETS:
        if action - offset in (400, 401, 620, 621):
            return [11, 11, 12, 13, 14, 15][min(5, index * 6 // total)]
    return None


def load(art, banks, sprites, out):
    assets = json.loads((art / 'provenance.json').read_text())['assets']
    for bank, slug in enumerate(banks):
        tiles = extract(art / assets['body-' + slug]['file'], 4, 4)
        factor = 208 / tiles[0][0].height
        for index, (tile, _) in enumerate(tiles):
            tile = tile.resize((max(1, round(tile.width * factor)),
                                max(1, round(tile.height * factor))), Image.Resampling.LANCZOS)
            # Feet retain one world origin through charge, recoil and recovery.
            # Hands extend right of that origin rather than recentering each pose.
            proportion = .30 if index in range(4, 9) or index in (12, 13, 14) else .5
            axis = (round(tile.width * proportion), tile.height)
            sprites.append(dict(key=(62200 + bank, index), image=tile, axis=axis))
            tile.save(out / f'energy-{slug}-{index}.png')
    effects = {}
    for name in ('beam', 'ki-impact'):
        sheet = Image.open(art / (name + '.png')).convert('RGBA')
        effects[name] = [sheet.crop((x * sheet.width // 4, y * sheet.height // 4,
                                    (x + 1) * sheet.width // 4, (y + 1) * sheet.height // 4))
                         for y in range(4) for x in range(4)]
    return effects


def effect_image(effects, group, number, motif):
    if group == 1015:
        return effects['ki-impact'][4 + (number if number < 4 else 2 + number % 2)]
    if group == 411 or motif == 2:
        return effects['ki-impact'][number % 4]
    if group == 420:
        return effects['ki-impact'][12 + (number % 8) // 2]
    if group == 415:
        return effects['ki-impact'][12 + min(3, number * 4 // 15)]
    if group == 1030:
        return effects['ki-impact'][8 + min(3, number * 4 // 31)]
    if motif == 1 or group == 1057:
        # Ignition resolves into a travelling flow instead of flashing through
        # the dissipating tail repeatedly while the helper is still attacking.
        return effects['beam'][number if number < 4 else 4 + (number - 4) % 8]
    if motif == 0 and group not in (9000, 180):
        return effects['ki-impact'][8 + number % 4]
    return None
