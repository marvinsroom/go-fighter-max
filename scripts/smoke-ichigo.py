from pathlib import Path
import subprocess,re
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
config=(E/'save/config.ini').read_text()
config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-ichigo-smoke.lua',config,flags=re.M)
(E/'save/ichigo-smoke.ini').write_text(config)
(E/'external/mods/-ichigo-smoke.lua').write_text('local ticks=0\nfunction loop()\n ticks=ticks+1\n if ticks>180 then print("ICHIGO_SMOKE_OK");os.exit() end\nend\n')
args=[str(E/'Ikemen_GO.exe'),'-config','save/ichigo-smoke.ini','-loadmotif','-p1','ichigo','-p2','will_full','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1']
try:
 p=subprocess.run(args,cwd=E,capture_output=True,timeout=90,creationflags=0x08000000)
 print(p.stdout.decode(errors='replace')[-4000:]);print(p.stderr.decode(errors='replace')[-4000:]);print('EXIT',p.returncode)
except subprocess.TimeoutExpired as e:print('TIMEOUT',e.stdout,e.stderr)
