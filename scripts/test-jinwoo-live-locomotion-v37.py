"""Capture the exact live Jinwoo definition's core locomotion states.

This intentionally targets chars/jinwoo/jinwoo.def, the same character used by
Play Jinwoo.cmd.  It also records the rendered AIR sprite key so duplicate AIR
actions and accidental fallback art cannot pass unnoticed.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0"
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
PREVIEW = BASE / "live-locomotion-v37-preview"
REPORT = BASE / "live-locomotion-v37.json"
MODULE = ENGINE / "external/mods/-jinwoo-live-locomotion-v37.lua"
CONFIG = ENGINE / "save/jinwoo-live-locomotion-v37.ini"

CASES = (
    ("idle", 0, 42),
    ("crouch", 10, 42),
    ("walk-forward", 20, 54),
    ("walk-back", 21, 54),
    ("jump-start", 40, 30),
    ("jump-rise", 41, 30),
    ("jump-forward", 42, 30),
    ("jump-back", 43, 30),
    ("jump-apex", 44, 30),
    ("jump-land", 47, 30),
)


def quote(value: object) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for path in PREVIEW.glob("Jinwoo_Live_Locomotion_v37*.png"):
        path.unlink()
    REPORT.unlink(missing_ok=True)

    cases = "{" + ",".join(
        "{name='%s',state=%d,length=%d}" % case for case in CASES
    ) + "}"
    lua = r'''local cases=CASES
local tick,index,localtick,shot,pending=0,0,0,0,nil
local report={status='RUNNING',runtime='jinwoo/jinwoo.def',frames={}}
local function save()
 jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/live-locomotion-v37.json')
end
hook.add('loop','jinwoo-live-locomotion-v37',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1
 if pending then
  local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/live-locomotion-v37-preview/'..pending.file
  local f=io.open(path,'rb')
  if f then f:close();table.insert(report.frames,pending);pending=nil;save() end
 end
 if localtick==1 then
  index=index+1
  if cases[index] then changeState(cases[index].state) end
 end
 local c=cases[index]
 if c and not pending and (localtick==2 or localtick==8 or localtick==16 or localtick==28 or localtick==40) then
  local file='Jinwoo_Live_Locomotion_v37'..string.format('%03d',shot)..'.png';shot=shot+1
  pending={case=index,name=c.name,target=c.state,tick=localtick,state=stateNo(),animation=anim(),
   group=spriteVar('group'),image=spriteVar('image'),pos_x=posX(),pos_y=posY(),file=file}
  screenshot()
 end
 if c and localtick>=c.length then localtick=0 end
 if index>#cases and localtick>=20 and not pending then
  report.status='PASS';report.frame_count=#report.frames;save();os.exit(0)
 end
 if tick>700 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)'''.replace("CASES", cases)
    MODULE.write_text(lua, encoding="utf-8")

    config = (ENGINE / "save/config.ini").read_text(encoding="utf-8")
    values = {
        "Modules": "external/mods/-jinwoo-live-locomotion-v37.lua",
        "ScreenshotFolder": "../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/live-locomotion-v37-preview/",
        "WindowTitle": "Jinwoo_Live_Locomotion_v37",
        "MasterVolume": "0",
    }
    for key, value in values.items():
        config = re.sub(rf"(?im)^{re.escape(key)}\s*=.*$", f"{key} = {value}", config)
    CONFIG.write_text(config, encoding="utf-8")

    args = [
        "-config", "save/jinwoo-live-locomotion-v37.ini", "-loadmotif",
        "-p1", "jinwoo/jinwoo.def", "-p2", "kfm", "-p1.ai", "0", "-p2.ai", "0",
        "-s", "stages/stage0-720.def", "-time", "-1", "-speedtest", "4",
    ]
    stdout = BASE / "live-locomotion-v37-stdout.log"
    stderr = BASE / "live-locomotion-v37-stderr.log"
    command = (
        "$p=Start-Process -FilePath " + quote(ENGINE / "Ikemen_GO.exe")
        + " -WorkingDirectory " + quote(ENGINE)
        + " -ArgumentList @(" + ",".join(quote(arg) for arg in args) + ")"
        + " -WindowStyle Hidden -RedirectStandardOutput " + quote(stdout)
        + " -RedirectStandardError " + quote(stderr)
        + " -PassThru; $null=$p.Handle;"
        + " if(!$p.WaitForExit(180000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode"
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", command], cwd=ROOT, timeout=195)
    errors = stderr.read_text(encoding="utf-8", errors="replace") if stderr.exists() else ""
    if result.returncode or re.search(r"(?im)Panic:|stack traceback:|error parsing|error loading|failed to load", errors):
        raise RuntimeError(f"smoke failed ({result.returncode}):\n{errors[-5000:]}")
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    if data.get("status") != "PASS":
        raise RuntimeError(str(data))
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
