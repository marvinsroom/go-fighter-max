"""Validate and extract GT Goku pose sheets; does not imply runtime readiness."""
import hashlib
import json
from pathlib import Path
from PIL import Image
from isolated_sprite_atlas import extract

ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / 'sprite-fighter/characters/gt-goku'
ART = CHARACTER / 'art/illustrated-v1'
FORMS = [('base-tail-v3', 'Base Kid Goku'), ('ss1-tail-v2', 'Super Saiyan'),
         ('ss2', 'Super Saiyan 2'), ('ss3-tail-v2', 'Super Saiyan 3'), ('ss4', 'Super Saiyan 4')]

def main():
    reports = []
    for key, name in FORMS:
        path = ART / f'{key}.png'
        with Image.open(path) as image:
            assert image.mode == 'RGBA', (key, 'Missing alpha channel')
            low, high = image.getchannel('A').getextrema()
            assert low == 0 and high >= 250, (key, 'Not transparent')
            size = list(image.size)
        poses = extract(path, 4, 4)
        assert len(poses) == 16
        folder = ART / 'poses' / key
        folder.mkdir(parents=True, exist_ok=True)
        for index, (tile, _) in enumerate(poses):
            tile.save(folder / f'{index:02}.png')
        reports.append({'key': key, 'name': name, 'atlas': f'illustrated-v1/{key}.png',
                        'size': size, 'pose_count': len(poses),
                        'tail_color': 'red' if key == 'ss4' else 'brown',
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'bounds': [list(bounds) for _, bounds in poses]})
    ready = False
    if (CHARACTER / 'verification.json').exists():
        verification = json.loads((CHARACTER / 'verification.json').read_text())
        build = json.loads((CHARACTER / 'build-report.json').read_text())
        ready = verification.get('status') == 'Complete' and verification.get('runtime_sha256') == build.get('runtime_sha256')
    report = {'status': 'playable_validated' if ready else 'art_ready_runtime_pending', 'generator': 'built-in image_gen',
              'playable_ready': ready, 'forms': reports,
              'pending': [] if ready else ['Runtime integration and validation']}
    (CHARACTER / 'art/generation-status.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'forms': len(reports), 'poses': sum(r['pose_count'] for r in reports),
                      'status': report['status']}))

if __name__ == '__main__':
    main()
