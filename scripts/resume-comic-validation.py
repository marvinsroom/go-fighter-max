"""Resume the comic redraw checks with durable, per-fighter checkpoints."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.tmp/comic-validation-resume.json'
SLUGS = ['arthur', 'jin-mu-won', 'kim-dokja', 'lloyd', 'gang-ryong',
         'mok-gyeongwoon', 'cha-yeon-woo', 'zhuo-fan', 'eugene']

def run(args):
    print('RUN', *map(str, args), flush=True)
    subprocess.run(list(map(str, args)), cwd=ROOT, check=True)

def current(slug):
    folder = ROOT / 'sprite-fighter/characters' / slug
    build = json.loads((folder / 'build-report.json').read_text())
    proof = json.loads((folder / 'runtime-validation.json').read_text())
    startup = json.loads((folder / 'startup-ai-validation.json').read_text())
    native = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0/chars' / slug.replace('-', '_')
    return (proof.get('status') == 'Complete' and proof.get('failed') == 0
            and proof.get('passed', 0) >= 66
            and build['runtime_sha256'] == proof.get('runtime_sha256')
            and startup.get('passed')
            and startup.get('runtime_sha256') == build['runtime_sha256']
            and all(hashlib.sha256((native / n).read_bytes()).hexdigest() == h
                    for n, h in build['runtime_sha256'].items()))

if __name__ == '__main__':
    state = json.loads(STATE.read_text()) if STATE.exists() else {'fighters': {}}
    for slug in sys.argv[1:] or SLUGS:
        try:
            if not current(slug):
                revision = 'v' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                     'scripts/validate-manhwa-fighter.ps1', '-Character', slug, '-Revision', revision])
            else:
                run([sys.executable, 'scripts/package-manhwa.py', slug])
                run([sys.executable, 'scripts/verify-manhwa.py', slug])
            run([sys.executable, 'scripts/verify-manhwa-review.py', slug])
            state['fighters'][slug] = {'status': 'PASS', 'updated': datetime.datetime.now().isoformat()}
        except Exception as error:
            state['fighters'][slug] = {'status': 'FAIL', 'error': str(error)}
            print('FIGHTER_FAILED', slug, error, flush=True)
        STATE.write_text(json.dumps(state, indent=2))
        run([sys.executable, 'scripts/build-comic-identity-review.py'])
    print('COMIC_VALIDATION_BATCH', json.dumps(state), flush=True)
    if any(x['status'] != 'PASS' for x in state['fighters'].values()):
        sys.exit(1)
