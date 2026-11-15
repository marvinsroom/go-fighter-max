"""Engine and visual smoke test for Jinwoo's three-style arsenal and shockwave."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0"
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
PREVIEW = BASE / "arsenal-v35-preview"
REPORT = BASE / "arsenal-engine-smoke-v35.json"
MODULE = ENGINE / "external/mods/-jinwoo-arsenal-v35-smoke.lua"
CONFIG = ENGINE / "save/jinwoo-arsenal-v35-smoke.ini"

# Three toggles prove bare -> daggers -> sword -> bare. The forced supers then
# visually validate that each style owns separate weapon art.
TARGETS = (870220, 870220, 870220, 876290, 876300, 876310)
SHOTS = {
    870220: (5, 15, 23, 31),
    876290: (8, 16, 25),
    876300: (10, 19, 28),
    876310: (10, 22, 29, 38),
}


def q(value: object) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    PREVIEW.mkdir(parents=True, exist_ok=True)
    for old in PREVIEW.glob("Jinwoo_Arsenal_v35*.png"):
        old.unlink()
    targets = "{" + ",".join(str(x) for x in TARGETS) + "}"
    shot_map = "{" + ",".join(
        f"[{state}]={{{','.join(str(t) for t in times)}}}" for state, times in SHOTS.items()
    ) + "}"
    lua = r'''local tick,index,localtick,shot,pending=0,0,0,0,nil
local targets=TARGETS
local shotmap=SHOTMAP
local report={status='RUNNING',targets=targets,entered={},frames={},states={},runtime='jinwoo/jinwoo.def'}
local function save() jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/arsenal-engine-smoke-v35.json') end
local function wants(state,t)
 local times=shotmap[state] or {}
 for _,v in ipairs(times) do if v==t then return true end end
 return false
end
hook.add('loop','jinwoo-arsenal-v35-smoke',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1;report.states[tostring(stateNo())]=true
 if pending then
  local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/arsenal-v35-preview/'..pending.file
  local f=io.open(path,'rb')
  if f then f:close();table.insert(report.frames,pending);pending=nil;save() end
 end
 if localtick==1 then
  index=index+1
  if targets[index] then setPower(3000);changeState(targets[index]);report.entered[tostring(index)..':'..tostring(targets[index])]=true end
 end
 if targets[index] and wants(targets[index],localtick) and not pending then
  local file='Jinwoo_Arsenal_v35'..string.format('%03d',shot)..'.png'
  pending={target=targets[index],tick=localtick,state=stateNo(),animation=anim(),file=file}
  shot=shot+1
  screenshot()
 end
 if localtick>=72 then localtick=0 end
 if index>#targets and localtick>=50 and not pending then report.status='PASS';report.active_round_ticks=tick;report.frame_count=#report.frames;save();os.exit(0) end
 if tick>900 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)
'''.replace("TARGETS", targets).replace("SHOTMAP", shot_map)
    MODULE.write_text(lua, encoding="utf-8")
    config = (ENGINE / "save/config.ini").read_text(encoding="utf-8")
    values = {
        "Modules": "external/mods/-jinwoo-arsenal-v35-smoke.lua",
        "ScreenshotFolder": "../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/arsenal-v35-preview/",
        "WindowTitle": "Jinwoo_Arsenal_v35",
        "MasterVolume": "0",
    }
    for key, value in values.items():
        config = re.sub(rf"(?im)^{re.escape(key)}\s*=.*$", f"{key} = {value}", config)
    CONFIG.write_text(config, encoding="utf-8")
    if REPORT.exists():
        REPORT.unlink()
    args = [
        "-config", "save/jinwoo-arsenal-v35-smoke.ini", "-loadmotif",
        "-p1", "jinwoo/jinwoo.def", "-p2", "kfm", "-p1.ai", "0", "-p2.ai", "0",
        "-p1.power", "3000", "-p2.power", "3000", "-s", "stages/stage0-720.def",
        "-time", "-1", "-speedtest", "4",
    ]
    stdout = BASE / "arsenal-engine-smoke-stdout-v35.log"
    stderr = BASE / "arsenal-engine-smoke-stderr-v35.log"
    command = (
        "$p=Start-Process -FilePath " + q(ENGINE / "Ikemen_GO.exe")
        + " -WorkingDirectory " + q(ENGINE)
        + " -ArgumentList @(" + ",".join(q(x) for x in args) + ")"
        + " -WindowStyle Hidden -RedirectStandardOutput " + q(stdout)
        + " -RedirectStandardError " + q(stderr)
        + " -PassThru; $null=$p.Handle; if(!$p.WaitForExit(180000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode"
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", command], cwd=ROOT, timeout=195)
    errors = stderr.read_text(encoding="utf-8", errors="replace") if stderr.exists() else ""
    if result.returncode or re.search(r"(?im)Panic:|stack traceback:|error parsing|error loading|failed to load", errors):
        raise RuntimeError(f"arsenal smoke failed ({result.returncode}):\n{errors[-6000:]}")
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    if data.get("status") != "PASS" or data.get("frame_count", 0) < 18:
        raise RuntimeError(f"incomplete arsenal smoke: {data}")
    absent = [frame["file"] for frame in data["frames"] if not (PREVIEW / frame["file"]).is_file()]
    if absent:
        raise RuntimeError(f"missing captures: {absent}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
