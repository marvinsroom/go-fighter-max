"""Run shared-fixture native suites sequentially, at most two games per suite."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
results=[]
for name in ('validate-jus-mobility.py','validate-jus-combat.py','validate-jus-form-cycles.py','validate-jus-camera.py'):
 print('SUITE',name,flush=True)
 result=subprocess.run([sys.executable,str(R/'scripts'/name)],cwd=R)
 results.append(dict(suite=name,exit_code=result.returncode))
(R/'sprite-fighter/jus-upgrade/suite-results.json').write_text(json.dumps(results,indent=2))
if any(r['exit_code'] for r in results):raise SystemExit(1)
