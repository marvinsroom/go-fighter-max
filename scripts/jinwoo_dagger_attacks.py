"""Dual-dagger normals for human Jinwoo — greatsword-grade multi-frame atlases."""
from pathlib import Path
import json
import re
import numpy as np
from PIL import Image
from scipy import ndimage

from jinwoo_hybrid_art import drawing, complete_atlas_figures, GAMEPLAY_HEIGHT, ROOT_SCALE

SHEET_DIR = Path('sprite-fighter/characters/jinwoo/art/daggers/animations')
REGISTRATION = Path('sprite-fighter/characters/jinwoo/art/daggers/attack-registration.json')
CLEAN_CYCLE = Path('sprite-fighter/characters/jinwoo/art/daggers/dagger-cycle-clean-v2.png')
COMBAT_V2 = Path('sprite-fighter/characters/jinwoo/art/combat-v2/registration.json')
LOCOMOTION_V3 = Path('sprite-fighter/characters/jinwoo/art/combat-v2/locomotion-loadouts-v3.png')
ATTACK_ACTIONS = {
    200, 210, 220, 260, 300, 310, 320, 350, 400, 410, 415, 416, 420, 426,
    430, 440, 450, 460, 465, 600, 610, 620, 630, 650,
}
MOVEMENT_ACTIONS = {0, 5, 6, 10, 11, 12, 20, 21, 100, 105}


def _knockout_white(rgb, soft=220, hard=240):
    """Remove ONLY edge-connected backdrop — never punch holes in the black coat.

    Generated atlases sit on solid black (or light gray). A global black key
    made the trench coat transparent. Flood-fill from the canvas border instead.
    """
    from collections import deque
    arr = np.asarray(rgb.convert('RGB'), dtype=np.uint8)
    h, w = arr.shape[:2]
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    chroma = mx - mn
    # Strict backdrop only (pure black / near-white). Loose thresholds ate the coat.
    is_bg = ((mx <= 12) & (chroma <= 8)) | ((mn >= hard) & (chroma <= 18))
    alpha = np.full((h, w), 255, dtype=np.uint8)
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg[y, x]:
                visited[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        alpha[y, x] = 0
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
    # Keep purple FX fully solid even if anti-aliased against the backdrop.
    purple = (arr[:, :, 2] > arr[:, :, 1] + 20) & (arr[:, :, 2] > arr[:, :, 0] + 10) & (arr[:, :, 2] > 80)
    alpha = np.where(purple, 255, alpha)
    out = np.dstack([arr, alpha])
    return Image.fromarray(out, 'RGBA')


def _grid_figures(rgba, cols=2, rows=4, alpha_min=24):
    """Extract one figure per cell — reliable when components merge across gutters."""
    pixels = np.asarray(rgba.convert('RGBA'))
    h, w = pixels.shape[:2]
    cw, ch = w // cols, h // rows
    figures = []
    for row in range(rows):
        for col in range(cols):
            x1, y1 = col * cw, row * ch
            x2 = (col + 1) * cw if col < cols - 1 else w
            y2 = (row + 1) * ch if row < rows - 1 else h
            cell = pixels[y1:y2, x1:x2].copy()
            mask = cell[:, :, 3] > alpha_min
            if not mask.any():
                raise AssertionError(f'empty cell {row},{col}')
            ys, xs = np.where(mask)
            lx1, ly1, lx2, ly2 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
            tile = cell[ly1:ly2, lx1:lx2].copy()
            tile[:, :, 3] = np.where(tile[:, :, 3] > alpha_min, tile[:, :, 3], 0)
            rect = (x1 + lx1, y1 + ly1, x1 + lx2, y1 + ly2)
            figures.append((Image.fromarray(tile), rect))
    return figures


def core_metrics(tile, alpha_min=24):
    """Head-to-boot height through the torso column — ignores side arms/weapons/FX."""
    arr = np.asarray(tile.convert('RGBA'))
    mask = arr[:, :, 3] > alpha_min
    assert mask.any(), 'empty dagger tile'
    ys, xs = np.where(mask)
    x0, x1 = int(xs.min()), int(xs.max())
    mid = (x0 + x1) / 2
    half = max(6, (x1 - x0) * 0.18)
    col = mask[:, max(0, int(mid - half)):int(mid + half) + 1]
    assert col.any(), 'empty core column'
    cy, _ = np.where(col)
    top, bot = int(cy.min()), int(cy.max())
    band_top = max(top, bot - max(4, int((bot - top) * 0.10)))
    foot = mask[band_top:bot + 1, x0:x1 + 1]
    if foot.any():
        _, fx = np.where(foot)
        axis_x = int(round(fx.mean() + x0))
    else:
        axis_x = int(round(mid))
    return dict(core_height=bot - top + 1, axis=[axis_x, bot], full_height=int(ys.max() - ys.min() + 1))


def install_from_generated(root, sources):
    """Convert generated atlases into transparent PNGs + registration.

    sources: dict name -> path, e.g. {'light': '...', 'heavy': '...', 'aerial': '...'}
    """
    root = Path(root)
    out_dir = root / SHEET_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    registration = {'weapon': 'dual daggers', 'sheets': {}}
    for name, src in sources.items():
        rgba = _knockout_white(Image.open(Path(src)))
        path = out_dir / f'{name}.png'
        rgba.save(path)
        try:
            figures = complete_atlas_figures(rgba, cols=2, rows=4, alpha_min=24)
        except AssertionError:
            figures = _grid_figures(rgba, cols=2, rows=4, alpha_min=24)
        frames = []
        core_heights = []
        for tile, rect in figures:
            metrics = core_metrics(tile)
            core_heights.append(metrics['core_height'])
            frames.append({
                'rect': [int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])],
                'components': [1],
                'axis': metrics['axis'],
                'core_height': metrics['core_height'],
            })
        body_height = float(np.median(core_heights))
        registration['sheets'][name] = {
            'file': f'animations/{name}.png',
            'alpha_min': 24,
            'body_height': body_height,
            'frames': frames,
        }
        print(name, 'frames', len(frames), 'size', rgba.size,
              'core_median', round(body_height, 1), 'cores', core_heights)
    (root / REGISTRATION).write_text(json.dumps(registration, indent=2), encoding='utf-8')
    return registration


def load(root, art):
    """Load dagger attack sheets into art as dagger:light:i / dagger:heavy:i / dagger:aerial:i."""
    root = Path(root)
    combat_registration = root / COMBAT_V2
    if combat_registration.exists():
        combat = json.loads(combat_registration.read_text(encoding='utf-8'))
        folder = combat_registration.parent
        for name, sheet in combat['sheets'].items():
            with Image.open(folder / sheet['file']) as source:
                source = source.convert('RGBA')
                for i, frame in enumerate(sheet['frames']):
                    rect = frame['rect']
                    tile = source.crop(rect)
                    metrics = core_metrics(tile, 16)
                    art[f'combat:{name}:{i}'] = drawing(
                        tile, metrics['axis'], 1.0,
                        str((folder / sheet['file']).relative_to(root)), rect)
    locomotion = root / LOCOMOTION_V3
    if locomotion.exists():
        with Image.open(locomotion) as source:
            source = source.convert('RGBA')
            assert source.size == (2048, 768), source.size
            for row, mode in enumerate(('bare', 'dagger', 'sword')):
                for i in range(8):
                    rect = [i * 256, row * 256, (i + 1) * 256, (row + 1) * 256]
                    tile = source.crop(rect)
                    metrics = core_metrics(tile, 12)
                    m = drawing(tile, metrics['axis'], 1.0,
                                str(locomotion.relative_to(root)), rect)
                    m['scale_body'] = metrics['core_height']
                    art[f'combat:locomotion-{mode}:{i}'] = m
    clean_cycle = root / CLEAN_CYCLE
    if clean_cycle.exists():
        with Image.open(clean_cycle) as source:
            assert source.mode == 'RGBA', clean_cycle
            figures = _grid_figures(source, cols=4, rows=2, alpha_min=16)
        assert len(figures) == 8
        for i, (tile, rect) in enumerate(figures):
            metrics = core_metrics(tile, 16)
            art[f'base:dagger-cycle_{i}'] = drawing(
                tile,
                metrics['axis'],
                1.0,
                str(clean_cycle.relative_to(root)),
                rect,
            )
    reg_path = root / REGISTRATION
    if not reg_path.exists():
        return
    registration = json.loads(reg_path.read_text(encoding='utf-8'))
    folder = root / 'sprite-fighter/characters/jinwoo/art/daggers'
    for name, sheet in registration['sheets'].items():
        path = folder / sheet['file']
        with Image.open(path) as im:
            assert im.mode == 'RGBA', path
            pixels = np.array(im)
        labels, _ = ndimage.label(pixels[:, :, 3] > sheet['alpha_min'])
        for i, frame in enumerate(sheet['frames']):
            x1, y1, x2, y2 = frame['rect']
            tile = pixels[y1:y2, x1:x2].copy()
            local = labels[y1:y2, x1:x2]
            ids = sorted({int(v) for v in local.ravel() if v}, key=lambda c: (local == c).sum(), reverse=True)
            if ids:
                tile[:, :, 3] = np.where(np.isin(local, ids[:4]), tile[:, :, 3], 0)
            image = Image.fromarray(tile)
            metrics = core_metrics(image, sheet['alpha_min'])
            key = f'dagger:{name}:{i}'
            full = metrics['full_height']
            m = drawing(
                image,
                metrics['axis'],
                GAMEPLAY_HEIGHT / (full * ROOT_SCALE),
                str(path.relative_to(root)),
                frame['rect'],
            )
            m['scale_body'] = full
            m['core_height'] = metrics['core_height']
            art[key] = m
    # Aerial fallback from jump cycle when no aerial sheet is registered.
    if not any(k.startswith('dagger:aerial:') for k in art):
        for i in range(8):
            jump = art.get(f'base:jump_{i}')
            if jump:
                art[f'dagger:aerial:{i}'] = jump

    # Full human-art replacement.  Summon remains the registered source pose
    # and shadow transformations live in their own banks; every ordinary
    # Jinwoo movement/combat alias points at combat-v2.
    # normal-locomotion 4x3: 0-1 idle, 2-3 walk, 4-5 run/dash, 6-7 crouch, 8-11 jump.
    # Walk must NOT bleed into run frames (old 2+(i%4) mixed walk+sprint and looked broken).
    aliases = {
        'base:idle': 'combat:normal-locomotion:0',
        'base:crouch': 'combat:normal-locomotion:6',
        'base:slash': 'combat:normal-reactions:1',
        'base:lunge': 'combat:normal-reactions:3',
        'base:kick': 'combat:normal-reactions:3',
        'base:hurt': 'combat:normal-reactions:6',
        'base:down': 'combat:normal-reactions:10',
    }
    for i in range(8):
        aliases[f'base:walk_{i}'] = f'combat:locomotion-bare:{i % 4}'
        aliases[f'base:run_{i}'] = f'combat:locomotion-bare:{4 + (i % 4)}'
        aliases[f'base:jump_{i}'] = f'combat:normal-locomotion:{8 + min(3, i // 2)}'
        aliases[f'base:dagger-cycle_{i}'] = f'combat:special:{i}'
        aliases[f'sword:stance:{i}'] = f'combat:sword-ground:{0 if i < 4 else 11}'
        aliases[f'sword:movement:{i}'] = f'combat:sword-ground:{i % 12}'
        aliases[f'sword:light:{i}'] = f'combat:sword-ground:{1 + min(3, i // 2)}'
        aliases[f'sword:heavy:{i}'] = f'combat:sword-ground:{4 + min(3, i // 2)}'
        aliases[f'sword:aerial:{i}'] = f'combat:sword-air-special:{min(6, i)}'
        aliases[f'sword:reactions:{i}'] = f'combat:sword-reactions-finishers:{min(5, i)}'
        aliases[f'sword:super:{i}'] = f'combat:sword-air-special:{min(11, 7 + i // 2)}'
        aliases[f'sword:finisher:{i}'] = f'combat:sword-reactions-finishers:{min(11, 7 + i // 2)}'
    missing = [(target, source) for target, source in aliases.items() if source not in art]
    assert not missing, missing
    for target, source in aliases.items():
        art[target] = art[source]


def stabilize_attack_sizes(art):
    """Fit every dagger attack frame to the same lore silhouette height as idle."""
    report = {}
    for sheet in ('light', 'heavy', 'aerial'):
        keys = [f'dagger:{sheet}:{i}' for i in range(8) if f'dagger:{sheet}:{i}' in art]
        if not keys:
            continue
        worlds = []
        for k in keys:
            m = art[k]
            body = m['bounds'][3] - m['bounds'][1]
            m['scale_body'] = body
            m['scale'] = GAMEPLAY_HEIGHT / (body * ROOT_SCALE)
            worlds.append(body * m['scale'] * ROOT_SCALE)
        report[sheet] = dict(
            frames=len(keys),
            world_min=round(min(worlds), 4),
            world_max=round(max(worlds), 4),
            world_delta=round(max(worlds) - min(worlds), 6),
            scales=[round(art[k]['scale'], 9) for k in keys],
        )
        assert report[sheet]['world_delta'] < 0.01, report[sheet]
    return report


def optimize_runtime_rasters(art, supersample=3):
    """Prefilter attack art before Ikemen's nearest-neighbour downscale."""
    target_h = max(96, int(round(GAMEPLAY_HEIGHT * supersample)))
    optimized = {}
    keys = [f'base:dagger-cycle_{i}' for i in range(8)]
    keys += [f'dagger:aerial:{i}' for i in range(8)]
    keys += [key for key in art if key.startswith('combat:')]
    for key in keys:
        if key not in art:
            continue
        m = art[key]
        b = m['bounds']
        body_h = b[3] - b[1]
        if body_h <= target_h:
            continue
        world = body_h * m['scale'] * ROOT_SCALE
        frame_target_h = max(72, int(round(world * supersample)))
        ratio = frame_target_h / body_h
        image = m['image']
        size = (max(1, int(round(image.width * ratio))),
                max(1, int(round(image.height * ratio))))
        resized = image.resize(size, Image.Resampling.LANCZOS)
        axis = [int(round(m['axis'][0] * ratio)), int(round(m['axis'][1] * ratio))]
        scale = world / (frame_target_h * ROOT_SCALE)
        # Mutate in place. base:/sword: aliases deliberately share these
        # records; replacing the dict left aliases on stale large rasters and
        # produced different apparent sizes between loadouts.
        updated = drawing(resized, axis, scale, m['source'], m.get('rect'))
        m.clear()
        m.update(updated)
        optimized[key] = {'before': image.size, 'after': size, 'scale': scale}
    return {'target_body_pixels': target_h, 'frames': optimized}


def pose_for(action, index, total, active):
    """Route attacks onto the identity-matched dagger cycle or aerial atlas."""
    n = action % 10000
    sample = lambda start, end: start + min(end - start, index * (end - start + 1) // max(1, total))
    sheet = 'light'
    if 600 <= n < 700 or n in (350, 630):
        sheet = 'aerial'
    elif n in (200, 210, 220, 260):
        sheet = 'light'
    elif n in (300, 310, 320):
        sheet = 'light'
    elif n in (400, 410, 415, 416, 420, 426, 430, 440, 450, 460, 465):
        sheet = 'heavy'
    else:
        sheet = 'heavy' if (n // 100) % 2 else 'light'
    heavy_feel = n in (300, 310, 320, 350) or sheet == 'heavy'
    frame = sample(2, 5) if sheet == 'aerial' else sample(0, 7)
    if active and sheet in ('light', 'heavy', 'aerial'):
        first, last = active[0], active[-1]
        if index < first:
            frame = min(4 if heavy_feel else 2, index * (5 if heavy_feel else 3) // max(1, first))
        elif index <= last:
            base = 5 if heavy_feel or sheet == 'aerial' else 3
            frame = base + min(1 if heavy_feel else 2, (index - first) * (2 if heavy_feel else 3) // max(1, last - first + 1))
        else:
            frame = 7 if heavy_feel else 6 + min(1, (index - last - 1) * 2 // max(1, total - last - 1))
        if sheet == 'aerial':
            frame = min(7, max(0, frame))
    # Normal attacks have their own authored dagger sheets.  Routing them
    # through combat-v2 made the small in-game sprites noisy: the large special
    # effects collapsed into bright outlines and the four-stage sampling made
    # several attacks appear to snap between unrelated silhouettes.  Keep the
    # combat-v2 bank for specials/supers, but preserve all eight purpose-built
    # frames for light, heavy, and aerial normals.
    return f'dagger:{sheet}:{frame}'


def attack_pose(art, sheet, frame):
    """Choose coherent human art, with old atlas frames as a fallback."""
    if sheet != 'aerial':
        key = f'base:dagger-cycle_{frame % 8}'
        if key in art:
            return key
    key = f'dagger:{sheet}:{frame % 8}'
    if key in art:
        return key
    return f'dagger:light:{frame % 8}'


def strip_human_normals(air):
    """Remove remapped source movement + normals so authored/cloned defs win first."""
    drop = MOVEMENT_ACTIONS | ATTACK_ACTIONS
    parts = re.split(r'(?=^\[Begin Action )', air, flags=re.I | re.M)
    kept = []
    for part in parts:
        m = re.match(r'\[Begin Action (\d+)\]', part, re.I)
        if m and int(m[1]) in drop:
            continue
        kept.append(part)
    return ''.join(kept)


def clone_normals(source, mapping, art):
    """Clone upstream attack AIR timing/Clsn, swap bodies to dagger atlases (like greatsword)."""
    if not any(f'dagger:light:{i}' in art for i in range(8)):
        return ''
    out = []
    for block in re.split(r'(?=^\[Begin Action )', source, flags=re.M | re.I):
        match = re.match(r'\[Begin Action (\d+)\]', block, re.I)
        if not match:
            continue
        n = int(match[1])
        if n not in ATTACK_ACTIONS and (n % 10000) not in ATTACK_ACTIONS:
            continue
        if n >= 500000:
            continue
        rows = block.splitlines()
        body_rows = []
        active_rows = []
        pending = None
        default = False
        for j, line in enumerate(rows):
            collision = re.match(r'\s*Clsn1(Default)?\s*:\s*(\d+)', line, re.I)
            if collision:
                if collision[1]:
                    default = int(collision[2]) > 0
                else:
                    pending = int(collision[2]) > 0
            if re.match(r'^\s*\d+\s*,\s*\d+\s*,', line):
                fields = line.split(';')[0].split(',')
                pose = mapping.get(tuple(map(int, fields[:2])))
                if pose and pose.startswith('base:'):
                    if (pending if pending is not None else default):
                        active_rows.append(len(body_rows))
                    body_rows.append(j)
                pending = None
        if not body_rows:
            continue
        positions = {line: i for i, line in enumerate(body_rows)}
        changed = False
        for i, line in enumerate(rows):
            if not re.match(r'^\s*\d+\s*,\s*\d+\s*,', line):
                continue
            p = [v.strip() for v in line.split(';')[0].split(',')]
            pose = mapping.get(tuple(map(int, p[:2])))
            if not pose or not pose.startswith('base:'):
                continue
            key = pose_for(n, positions[i], len(body_rows), active_rows)
            if key not in art:
                aerial = 600 <= (n % 10000) < 700
                key = attack_pose(art, 'aerial' if aerial else 'light', positions[i])
            m = art[key]
            p[:2] = [str(m['group']), str(m['number'])]
            while len(p) < 9:
                p.append('')
            # Drop source translucent flags (field 6 = ASxxDxx) — made attacks see-through.
            if re.search(r'[ASD]', p[6], re.I):
                p[6] = ''
            p[7] = p[8] = f"{m['scale']:.9f}"
            rows[i] = ','.join(p)
            changed = True
        if changed:
            rows[0] = f'[Begin Action {n}]'
            out.append('\n'.join(rows))
    return '\n' + '\n\n'.join(out) + '\n' if out else ''


def author_movement(art):
    """Idle / walk / run / crouch — attacks come from clone_normals."""
    required = ['base:idle', 'base:crouch']
    if any(k not in art for k in required):
        return ''
    out = []

    def action(n, frames, posture='S', loop=False):
        hurt = (-10, -28, 10, 0) if posture == 'C' else (-12, -59, 12, 0)
        lines = [f'[Begin Action {n}]', 'Clsn2Default: 1',
                 f'Clsn2[0] = {hurt[0]},{hurt[1]},{hurt[2]},{hurt[3]}']
        if loop:
            lines.append('LoopStart')
        for key, t in frames:
            m = art[key]
            # Per-frame AIR scale — do not force idle scale onto run/walk rasters.
            s = m['scale']
            lines.append(f"{m['group']},{m['number']},0,0,{t},,,{s:.9f},{s:.9f}")
        out.append('\n'.join(lines))

    idle, crouch = 'base:idle', 'base:crouch'
    walks = [f'base:walk_{i}' for i in range(8) if f'base:walk_{i}' in art]
    runs = [f'base:run_{i}' for i in range(8) if f'base:run_{i}' in art]
    walk_cycle = walks or [idle]
    run_cycle = runs or walks or [idle]
    hop = 'base:run_1' if 'base:run_1' in art else (run_cycle[0] if runs else idle)
    lift = 'base:jump_0' if 'base:jump_0' in art else idle
    action(0, [(idle, 36)], loop=True)
    action(5, [(idle, 16)])
    # Native throws/helpers fall back to Action 6 — was blank (-1,0) = vanish.
    action(6, [(idle, 20)])
    action(20, [(key, 6) for key in walk_cycle], loop=True)
    action(21, [(key, 6) for key in reversed(walk_cycle)], loop=True)
    # Common StateDef 100 (run fwd) / 105 (hop back) — Action 100 was missing.
    action(100, [(key, 4) for key in run_cycle], loop=True)
    action(105, [(hop, 3), (lift, 8)])
    # Explicit airborne actions prevent the source character's crouch/downed
    # drawings from leaking into no-weapon jumps.
    jump_cycle = [f'base:jump_{i}' for i in range(8) if f'base:jump_{i}' in art] or [lift]
    for n in (40, 41, 42, 43, 44, 45, 47, 50, 52):
        action(n, [(key, 3 if i < len(jump_cycle)-1 else 8)
                   for i,key in enumerate(jump_cycle)], 'A')
    action(10, [(idle, 1), (crouch, 5)], 'C')
    action(11, [(crouch, 20), (crouch, 20)], 'C', loop=True)
    action(12, [(crouch, 3), (idle, 5)])
    return '\n' + '\n\n'.join(out) + '\n'


def author_air(art):
    """Legacy entry: movement only. Prefer clone_normals + author_movement in build."""
    return author_movement(art)


def authored_fallback_attacks(art):
    """If clone finds no body rows, still ship 8-frame atlas normals."""
    if not all(f'dagger:light:{i}' in art for i in range(8)):
        return ''
    out = []

    def action(n, sheet, ticks, active, posture='S'):
        hurt = (-10, -28, 10, 0) if posture == 'C' else (
            (-10, -52, 10, 4) if posture == 'A' else (-12, -59, 12, 0))
        hit = (-4, -40, 70, 2) if posture == 'C' else (
            (-6, -55, 78, 10) if posture == 'A' else (0, -55, 72, -4))
        lines = [f'[Begin Action {n}]', 'Clsn2Default: 1',
                 f'Clsn2[0] = {hurt[0]},{hurt[1]},{hurt[2]},{hurt[3]}']
        for i, t in enumerate(ticks):
            if i in active:
                lines += ['Clsn1: 1', f'Clsn1[0] = {hit[0]},{hit[1]},{hit[2]},{hit[3]}']
            key = attack_pose(art, sheet, i)
            m = art[key]
            lines.append(f"{m['group']},{m['number']},0,0,{t},,,{m['scale']:.9f},{m['scale']:.9f}")
        out.append('\n'.join(lines))

    # Light / medium / heavy / crouch / air — full 8-frame arcs.
    action(200, 'light', (3, 3, 3, 4, 4, 4, 4, 6), (3, 4, 5))
    action(210, 'light', (2, 3, 3, 4, 4, 4, 5, 6), (3, 4, 5))
    action(220, 'light', (3, 3, 4, 4, 5, 4, 5, 7), (3, 4, 5))
    action(300, 'light', (4, 4, 4, 5, 5, 5, 5, 7), (3, 4, 5))
    action(310, 'light', (4, 4, 4, 5, 5, 5, 5, 7), (3, 4, 5))
    action(400, 'heavy', (4, 4, 5, 5, 5, 5, 6, 8), (3, 4, 5))
    action(410, 'heavy', (3, 3, 4, 4, 5, 4, 5, 6), (3, 4), 'C')
    action(420, 'heavy', (3, 4, 4, 5, 5, 5, 5, 7), (3, 4, 5), 'C')
    action(600, 'aerial', (3, 3, 3, 4, 4, 4, 4, 5), (3, 4, 5), 'A')
    action(610, 'aerial', (3, 3, 3, 4, 4, 4, 4, 5), (3, 4, 5), 'A')
    action(620, 'aerial', (3, 3, 4, 4, 4, 4, 5, 6), (3, 4, 5), 'A')
    action(350, 'aerial', (3, 3, 4, 4, 4, 4, 5, 6), (3, 4, 5), 'A')
    action(630, 'aerial', (3, 3, 4, 4, 5, 4, 5, 6), (3, 4, 5), 'A')
    return '\n' + '\n\n'.join(out) + '\n'
