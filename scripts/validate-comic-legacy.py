"""Record fresh native evidence for the established fighters after a redraw."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / 'sprite-fighter/characters'
ENGINE = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0'
STATE = ROOT / os.environ.get('COMIC_VALIDATION_STATE', '.tmp/comic-legacy-validation.json')
state = json.loads(STATE.read_text()) if STATE.exists() else {
    'stamp': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), 'completed': []}
stamp = 'comic-' + state['stamp']
state.setdefault('runtime', {})
for slug in ('baam', 'jin-mori', 'vikir', 'jinwoo', 'pyowol'):
    installed = json.loads((CHARACTERS / slug / 'art/comic-identity-v3/installed.json').read_text())
    hashes = installed['runtime_sha256']
    if state['runtime'].get(slug) != hashes:
        state['completed'] = [name for name in state['completed'] if not name.startswith(slug + '-')]
        state['runtime'][slug] = hashes
STATE.write_text(json.dumps(state, indent=2))

def fresh_run(slug, label):
    name = stamp + '-' + label
    if (CHARACTERS / slug / 'replays' / name).exists():
        name += '-retry-' + datetime.datetime.now().strftime('%H%M%S%f')
    return name

def run(*args):
    print('RUN', *args, flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)

def py(script, *args):
    run(sys.executable, 'scripts/' + script + '.py', *args)

def step(name, action):
    if name in state['completed']:
        print('RESUME_SKIP', name, flush=True)
        return
    action()
    state['completed'].append(name)
    STATE.write_text(json.dumps(state, indent=2))

def psquote(value):
    return "'" + str(value).replace("'", "''") + "'"

def game(config, p1, p2, speed=4, ai=0):
    args = ['-config', 'save/' + config + '.ini', '-loadmotif', '-p1', p1,
            '-p2', p2, '-p1.ai', str(ai), '-p2.ai', '0',
            '-p1.power', '3000', '-p2.power', '3000',
            '-s', 'stages/stage0-720.def', '-time', '-1']
    if speed != 1:
        args = ['-speedtest', str(speed)] + args
    command = ("$ErrorActionPreference='Stop'; $game=Start-Process -FilePath "
               + psquote(ENGINE / 'Ikemen_GO.exe') + ' -WorkingDirectory '
               + psquote(ENGINE) + ' -ArgumentList @('
               + ','.join(map(psquote, args)) + ') -WindowStyle Hidden'
               + ' -RedirectStandardOutput ' + psquote(ROOT / '.tmp' / (config + '-stdout.log'))
               + ' -RedirectStandardError ' + psquote(ROOT / '.tmp' / (config + '-stderr.log'))
               + ' -PassThru; $null=$game.Handle; $game.WaitForExit(); exit $game.ExitCode')
    print('GAME', config, p1, 'vs', p2, 'speed', speed, flush=True)
    subprocess.run(['powershell', '-NoProfile', '-Command', command], cwd=ROOT, check=True)

def proof(slug, count, filename='runtime-validation.json'):
    report = json.loads((CHARACTERS / slug / filename).read_text())
    assert report['status'] == 'Complete' and report['failed'] == 0, (slug, report.get('failed'))
    assert report['passed'] == count, (slug, report['passed'], count)
    return report

def record(slug, count, presentation=False, physical=False):
    options = (['--presentation'] if presentation else []) + (['--physical'] if physical else [])
    name = fresh_run(slug, 'presentation' if presentation else 'full')
    py('setup-' + slug + '-tests', name, *options)
    config, p1, p2 = ('baam-tests', 'baam/baam_test.def', 'will_full/will_baam_test.def') if slug == 'baam' else ('mori-tests', 'jin_mori/mori_test.def', 'will_full/will_mori_test.def')
    game(config, p1, p2, speed=1 if presentation else 4)
    report = proof(slug, count)
    directory = CHARACTERS / slug / 'validation'
    directory.mkdir(exist_ok=True)
    (directory / (stamp + ('-presentation' if presentation else '-full') + '.json')).write_text(json.dumps(report, indent=2))

def merge(slug):
    folder = CHARACTERS / slug
    original = json.loads((folder / 'validation' / (stamp + '-full.json')).read_text())
    retake = json.loads((folder / 'validation' / (stamp + '-presentation.json')).read_text())
    assert original['runtime_sha256'] == retake['runtime_sha256']
    replacements = {row['name']: row for row in retake['checks']}
    original['checks'] = [replacements.get(row['name'], row) for row in original['checks']]
    original['frames'] = [dict(frame, capture_directory=frame.get('capture_directory', report['capture_directory']))
                          for report in (original, retake) for frame in report['frames']
                          if report is retake or frame['case_name'] not in replacements]
    original['presentation_retake'] = {'source': stamp + '-presentation.json', 'same_runtime': True}
    (folder / 'runtime-validation.json').write_text(json.dumps(original, indent=2))

def startup(slug):
    py('setup-' + slug + '-startup', fresh_run(slug, 'startup'))
    if slug == 'baam':
        game('baam-startup', 'baam', 'will_full', speed=1, ai=4)
        result = json.loads((CHARACTERS / slug / 'startup-ai-validation.json').read_text())
    else:
        game('mori-startup', 'jin_mori', 'will_full', speed=1)
        result = json.loads((CHARACTERS / slug / 'startup-validation.json').read_text())
    assert result['passed'], result

def jinwoo_current():
    py('setup-jinwoo-current-tests', '--run', fresh_run('jinwoo', 'current'))
    game('jinwoo-current-tests', 'jinwoo/jinwoo_test.def', 'will_full/will_sword_test.def')
    report = json.loads((CHARACTERS / 'jinwoo/validation/current.json').read_text())
    assert report['status'] == 'Complete' and report['failed'] == 0

def jinwoo_motion():
    name = fresh_run('jinwoo', 'motion')
    py('setup-jinwoo-current-tests', '--run', name, '--slow-motion',
       *[arg for name in ('Daggers super hit', 'Greatsword super hit', 'Igris super', 'Beru super', 'Iron super', 'Tank super') for arg in ('--case', name)])
    game('jinwoo-focus-tests', 'jinwoo/jinwoo_test.def', 'will_full/will_sword_test.def', speed=1)
    folder = CHARACTERS / 'jinwoo/validation'
    report = json.loads((folder / (name + '.json')).read_text())
    assert report['status'] == 'Complete' and report['passed'] == 6 and report['failed'] == 0
    (folder / 'super-motion-preview.json').write_text(json.dumps(report, indent=2))
    (folder / 'super-motion-preview-runtime.json').write_bytes((folder / (name + '-runtime.json')).read_bytes())

def jinwoo_intro():
    py('setup-jinwoo-intro-test', '--run', fresh_run('jinwoo', 'intro'))
    game('jinwoo-intro-test', 'jinwoo/jinwoo.def', 'will_full/will_sword_test.def', speed=1)
    report = json.loads((CHARACTERS / 'jinwoo/validation/shadow-intro.json').read_text())
    assert report['status'] == 'Complete' and report['passed'] == 4 and report['failed'] == 0

def jinwoo_proportions():
    py('setup-jinwoo-proportions', '--run', fresh_run('jinwoo', 'proportions'))
    game('jinwoo-proportions', 'jinwoo/jinwoo.def', 'will_full/will_sword_test.def')
    report = json.loads((CHARACTERS / 'jinwoo/validation/proportions-native.json').read_text())
    assert report['status'] == 'Complete' and report['passed'] == 448 and report['failed'] == 0

def pyowol_record():
    py('setup-pyowol-tests', fresh_run('pyowol', 'full'), '--animation', '--silk')
    game('pyowol-tests', 'pyowol/pyowol_test.def', 'will_full/will_pyowol_test.def', speed=1)
    expected = len(json.loads((CHARACTERS / 'pyowol/test-cases.json').read_text()))
    proof('pyowol', expected)

if __name__ == '__main__':
    requested = sys.argv[1:] or ['baam', 'jin-mori', 'vikir', 'jinwoo', 'pyowol']
    for slug, count, presentations in [('baam', 130, 38), ('jin-mori', 71, 11)]:
        if slug not in requested:
            continue
        step(slug + '-full', lambda: record(slug, count, physical=slug == 'jin-mori'))
        step(slug + '-presentation', lambda: record(slug, presentations, True, slug == 'jin-mori'))
        step(slug + '-merge', lambda: merge(slug))
        step(slug + '-startup', lambda: startup(slug))
        if slug == 'baam':
            step(slug + '-contact-sheet', lambda: py('baam-cinematic-contact'))
        step(slug + '-package', lambda: py('package-' + slug))
        step(slug + '-verify', lambda: py('verify-' + slug))
        step(slug + '-browser', lambda: py('verify-' + slug + '-review'))
    if 'vikir' in requested:
        step('vikir-validation', lambda: run('powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/validate-vikir.ps1'))
    if 'jinwoo' in requested:
        for name, action in [('current', jinwoo_current), ('motion', jinwoo_motion), ('intro', jinwoo_intro), ('proportions', jinwoo_proportions)]:
            step('jinwoo-' + name, action)
        step('jinwoo-verify', lambda: py('verify-jinwoo-current'))
        step('jinwoo-package', lambda: py('package-jinwoo-current'))
        step('jinwoo-browser', lambda: py('verify-comic-review', 'jinwoo'))
    if 'pyowol' in requested:
        step('pyowol-record', pyowol_record)
        step('pyowol-package', lambda: py('package-pyowol'))
        step('pyowol-verify', lambda: py('verify-pyowol'))
        step('pyowol-browser', lambda: py('verify-pyowol-viewers'))
        step('pyowol-comic-browser', lambda: py('verify-comic-review', 'pyowol'))
    py('build-comic-identity-review')
    print('COMIC_LEGACY_COMPLETE', *requested, flush=True)
