"""Capture Jinwoo idle, charge, summon calls, and greatsword wave with helper traces."""
from __future__ import annotations
import json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
BASE=ROOT/'sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32'
PREVIEW=BASE/'regressions-v36-preview'; REPORT=BASE/'regressions-v36.json'
MODULE=ENGINE/'external/mods/-jinwoo-regressions-v36.lua'; CONFIG=ENGINE/'save/jinwoo-regressions-v36.ini'
CASES=((0,110),(500,45),(870100,70),(870101,70),(870102,70),(870103,70),(876310,75))

def q(v): return "'"+str(v).replace("'","''")+"'"
def main():
 PREVIEW.mkdir(parents=True,exist_ok=True)
 for p in PREVIEW.glob('Jinwoo_Regressions_v36*.png'): p.unlink()
 cases='{'+','.join('{state=%d,length=%d}'%x for x in CASES)+'}'
 lua=r'''local cases=CASES
local tick,index,localtick,shot,pending=0,0,0,0,nil
local report={status='RUNNING',frames={},helpers={},runtime='jinwoo/jinwoo.def'}
local function save() jsonEncode(report,'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/regressions-v36.json') end
local function traceHelpers()
 local out={};player(1);local count=numHelper()
 for j=0,count-1 do
  player(1);if helper(-1,j) then table.insert(out,{state=stateNo(),anim=anim(),group=spriteVar('group'),image=spriteVar('image')}) end
 end
 player(1);return out
end
hook.add('loop','jinwoo-regressions-v36',function()
 if not player(1) or roundState()~=2 then return end
 tick=tick+1;localtick=localtick+1
 if pending then local path='../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/regressions-v36-preview/'..pending.file;local f=io.open(path,'rb');if f then f:close();table.insert(report.frames,pending);pending=nil;save() end end
 if localtick==1 then index=index+1;if cases[index] then setPower(3000);changeState(cases[index].state) end end
 local c=cases[index]
 if c and not pending and (localtick==2 or localtick==8 or localtick==16 or localtick==28 or localtick==44 or localtick==60 or localtick==90) then
  local file='Jinwoo_Regressions_v36'..string.format('%03d',shot)..'.png';shot=shot+1
  pending={case=index,target=c.state,tick=localtick,state=stateNo(),animation=anim(),group=spriteVar('group'),image=spriteVar('image'),file=file,helper_count=numHelper()}
  report.helpers[tostring(index)..':'..tostring(localtick)]=traceHelpers();screenshot()
 end
 if c and localtick>=c.length then localtick=0 end
 if index>#cases and localtick>=30 and not pending then report.status='PASS';report.frame_count=#report.frames;save();os.exit(0) end
 if tick>750 then report.status='FAIL';report.error='timeout';save();os.exit(1) end
end)'''.replace('CASES',cases)
 MODULE.write_text(lua,encoding='utf-8')
 config=(ENGINE/'save/config.ini').read_text(encoding='utf-8')
 for k,v in {'Modules':'external/mods/-jinwoo-regressions-v36.lua','ScreenshotFolder':'../../characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/regressions-v36-preview/','WindowTitle':'Jinwoo_Regressions_v36','MasterVolume':'0'}.items(): config=re.sub(rf'(?im)^{re.escape(k)}\s*=.*$',f'{k} = {v}',config)
 CONFIG.write_text(config,encoding='utf-8'); REPORT.unlink(missing_ok=True)
 args=['-config','save/jinwoo-regressions-v36.ini','-loadmotif','-p1','jinwoo/jinwoo.def','-p2','kfm','-p1.ai','0','-p2.ai','0','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1','-speedtest','4']
 stdout=BASE/'regressions-v36-stdout.log';stderr=BASE/'regressions-v36-stderr.log'
 cmd='$p=Start-Process -FilePath '+q(ENGINE/'Ikemen_GO.exe')+' -WorkingDirectory '+q(ENGINE)+' -ArgumentList @('+','.join(q(x) for x in args)+') -WindowStyle Hidden -RedirectStandardOutput '+q(stdout)+' -RedirectStandardError '+q(stderr)+' -PassThru; $null=$p.Handle; if(!$p.WaitForExit(180000)){Stop-Process -Id $p.Id -Force;exit 2};exit $p.ExitCode'
 result=subprocess.run(['powershell','-NoProfile','-Command',cmd],cwd=ROOT,timeout=195)
 err=stderr.read_text(encoding='utf-8',errors='replace') if stderr.exists() else ''
 if result.returncode or re.search(r'(?im)Panic:|stack traceback:|error parsing|error loading|failed to load',err): raise RuntimeError(f'smoke failed ({result.returncode}):\n{err[-5000:]}')
 data=json.loads(REPORT.read_text(encoding='utf-8'))
 if data.get('status')!='PASS': raise RuntimeError(str(data))
 print(json.dumps(data,indent=2))
if __name__=='__main__':main()
