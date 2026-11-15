"""Audit the installed comic pass and its current native evidence."""
from comic_identity_v3 import SPECS, C, R
from pathlib import Path
import hashlib
import json
import sys

ENGINE = R / 'sprite-fighter/engine/ikemen-go-v1.0.0/chars'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

records = []
visual_review = json.loads((R / 'sprite-fighter/face-audit/comic-v3/form-review.json').read_text())
reviewed_forms = {row['slug']: row for row in visual_review['fighters']}
for slug in sys.argv[1:] or SPECS:
    folder = C / slug
    art = folder / 'art/comic-identity-v3'
    legacy = (art / 'installed.json').exists()
    build = json.loads((art / 'installed.json' if legacy else folder / 'build-report.json').read_text())
    native = ENGINE / (json.loads((art / 'runtime-templates.json').read_text())['engine'] if legacy else slug.replace('-', '_'))
    runtime = build['runtime_sha256']
    assert all(sha(native / name) == digest for name, digest in runtime.items()), ('Stale runtime registration', slug)
    archive = folder / 'archive/before-comic-identity-v3/runtime'
    for original in archive.iterdir():
        if original.suffix in ('.cns', '.cmd', '.air', '.snd', '.zss'):
            assert sha(original) == sha(native / original.name), ('Gameplay changed', slug, original.name)
    template = art / 'runtime-templates.json'
    sheets = [Path(page['destination']) for page in json.loads(template.read_text())['pages']] if template.exists() else [art / (kind + '.png') for kind in ('movement', 'combat', 'story')]
    for sheet in sheets + [art / 'portrait.png']:
        assert sheet.is_file() and sheet.with_suffix('.prompt.txt').is_file() and sheet.with_suffix('.generation.json').is_file(), sheet
    style_review = folder / 'art/comic-style-v4/visual-review.json'
    style_installed = folder / 'art/comic-style-v4/installed.json'
    if style_installed.exists():
        style = json.loads(style_review.read_text())
        assert style['status'] == 'Reviewed candidate' and style.get('native_review', {}).get('status') == 'Reviewed', ('V4 visual/native review incomplete', slug)
        assert all(style['assets'][sheet.name] == sha(sheet) == sha(style_review.parent / sheet.name) for sheet in sheets), ('V4 artwork review stale', slug)
        before = folder / 'archive/before-comic-style-v4'
        assert sha(art / 'portrait.png') == sha(before / 'art/portrait.png'), ('V4 portrait changed', slug)
        for original in (before / 'runtime').iterdir():
            if original.suffix in ('.cns', '.cmd', '.air', '.snd', '.zss'):
                assert sha(original) == sha(native / original.name), ('V4 gameplay changed', slug, original.name)
    if legacy:
        assert reviewed_forms[slug]['status'] == 'Reviewed'
        assert all(reviewed_forms[slug]['assets'][sheet.name] == sha(sheet) for sheet in sheets), ('Visual form review is stale', slug)
    if slug == 'jinwoo':
        roster = ENGINE / 'jinwoo'
        installation = json.loads((art / 'roster-installation.json').read_text())
        assert installation['status'] == 'Complete' and installation['runtime_sha256'] == runtime
        assert all(sha(roster / name) == digest for name, digest in runtime.items()), 'Jinwoo playable roster copy is stale'
        assert (roster / 'jinwoo.def').is_file(), 'Canonical Jinwoo definition is missing'
        proof = json.loads((folder / 'validation/current.json').read_text())
        assert json.loads((folder / 'validation/runtime.json').read_text()) == runtime
        assert json.loads((folder / 'validation/super-motion-preview-runtime.json').read_text()) == runtime
        intro = json.loads((folder / 'validation/shadow-intro.json').read_text())
        assert intro['runtime'] == runtime
        proportions = json.loads((folder / 'validation/proportions-native.json').read_text())
        assert proportions['runtime'] == runtime and proportions['failed'] == 0
    else:
        proof = json.loads((folder / 'runtime-validation.json').read_text())
        assert proof['runtime_sha256'] == runtime, ('Stale native captures', slug)
    assert proof['status'] == 'Complete' and proof['failed'] == 0, slug
    count = len(proof['frames'])
    for frame in proof['frames']:
        if 'src' in frame:
            capture = folder / frame['src']
        elif 'file' in frame:
            capture = folder / 'replays' / frame.get('capture_directory', proof['capture_directory']) / frame['file']
        else:
            capture = folder / 'replays' / proof['capture_directory'] / ('Jinwoo_hybrid%03d.png' % (frame['index'] - 1))
        assert capture.is_file(), capture
    viewer_path = folder / 'comic-viewer-validation.json'
    viewer = json.loads(viewer_path.read_text())
    assert viewer['status'] == 'PASS' and viewer['review_sha256'] == sha(folder / 'review.html'), ('Stale browser proof', slug)
    record = dict(slug=slug, status='PASS', native_checks=proof['passed'], captures=count,
                  browser_assertions=viewer['assertions'], runtime_sha256=runtime,
                  review_sha256=viewer['review_sha256'], gameplay_unchanged=True,
                  visual_forms_reviewed=legacy,
                  body_sheets=len(sheets), artwork='art/comic-identity-v3/design-review.html')
    if style_installed.exists():
        record.update(visual_revision='comic-style-v4', visual_review=str(style_review.relative_to(R)))
    (art / 'verification.json').write_text(json.dumps(record, indent=2))
    records.append(record)
    print('COMIC_INSTALLATION_VERIFIED', slug, proof['passed'], 'native checks', count, 'captures', flush=True)
if len(records) == len(SPECS):
    report = dict(status='Complete', revision='comic-style-v4' if all(row.get('visual_revision') == 'comic-style-v4' for row in records) else 'comic-identity-v3', fighters=records,
                  total_native_checks=sum(row['native_checks'] for row in records),
                  total_captures=sum(row['captures'] for row in records),
                  total_browser_assertions=sum(row['browser_assertions'] for row in records))
    (R / 'sprite-fighter/face-audit/completion.json').write_text(json.dumps(report, indent=2))
