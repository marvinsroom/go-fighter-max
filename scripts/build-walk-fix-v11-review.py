"""Compare native walk timing and ground travel without recording the game."""
from pathlib import Path
import json,re
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'walk-fix-v11';(O/'sprites').mkdir(exist_ok=True)
report=json.loads((O/'installation.json').read_text());items=[]
lloyd_art=json.loads((O/'artwork/lloyd/installation.json').read_text())
assert lloyd_art['status'].startswith('Complete; installed')
for row in report['files']:
 if row['slug']=='lloyd':row['sff_sha256']=lloyd_art['installed_sff_sha256']
report['status']='Complete; cadence, ground speed and Lloyd alternating-leg artwork installed'
report['artwork_blocker']=None
report['artwork_completion']={'character':'lloyd','status':'Installed and statically validated','report':'artwork/lloyd/installation.json'}
(O/'installation.json').write_text(json.dumps(report,indent=2))
labels={}
for p in (G/'jus-upgrade/art').glob('*/form-cycles-packing.json'):
 for cycle in json.loads(p.read_text()).get('cycles',[]):labels[(p.parent.name,cycle['output_group'])]=cycle['label']
def actions(data):
 return {int(m[1]):m[2] for m in re.finditer(r'(?ims)^\s*\[Begin Action\s+(\d+)\](.*?)(?=^\s*\[Begin Action|\Z)',data)}
for row in report['files']:
 n=E/'chars'/row['engine'];sf=Sff(n/row['sff']);before=actions((O/'before/chars'/row['engine']/row['air']).read_text(encoding='cp1252'));after=actions((n/row['air']).read_text(encoding='cp1252'))
 definition=(n/row['definition']).read_text(encoding='cp1252',errors='replace');width=float(re.search(r'(?im)^\s*localcoord\s*=\s*([\d.]+)',definition)[1]);cnsname=re.search(r'(?im)^\s*cns\s*=\s*([^;\r\n]+)',definition)[1].strip();cns=(n/cnsname).read_text(encoding='cp1252',errors='replace');size=re.search(r'(?ims)^\s*\[Size\](.*?)(?=^\s*\[|\Z)',cns)[1];xs=float(re.search(r'(?im)^\s*xscale\s*=\s*([\d.eE+-]+)',size)[1]);ys=float(re.search(r'(?im)^\s*yscale\s*=\s*([\d.eE+-]+)',size)[1])
 def frames(block):
  result=[]
  for line in block.splitlines():
   if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
   f=[s.strip() for s in line.split(';')[0].split(',')];key=tuple(map(int,f[:2]));i=sf.keys[key];h=sf.headers[i];file=f'sprites/{row["slug"]}-{key[0]}-{key[1]}.png';dest=O/file
   sf.decode(i).save(dest)
   result.append(dict(file=file,axis=list(h[4:6]),offset=[float(f[2]),float(f[3])],ticks=int(f[4]),scale=[(float(f[7]) if len(f)>7 and f[7] else 1)*xs*320/width,(float(f[8]) if len(f)>8 and f[8] else 1)*ys*320/width],key=key,flip=f[5] if len(f)>5 else ''))
  return result
 seen=set()
 for change in row['actions']:
  action=change['action'];group=change['group']
  if action%1000!=20 or group in seen:continue
  seen.add(group);back=next((r['action'] for r in row['actions'] if r['action']==action+1),None)
  if back is None:back=next((r['action'] for r in row['actions'] if r['action']%1000==21 and r['group']==group),None)
  item=dict(slug=row['slug'],group=group,label=labels.get((row['slug'],group),row['slug'].replace('-',' ').title()),forward=dict(before=frames(before[action]),after=frames(after[action])))
  if back is not None:item['backward']=dict(before=frames(before[back]),after=frames(after[back]))
  items.append(item)
data=dict(items=items,speed=report['world_speed'],artwork_pending=None,artwork_complete=report['artwork_completion']);(O/'review-data.json').write_text(json.dumps(data,indent=2))
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Walking cadence fixes</title><style>*{box-sizing:border-box}body{margin:0;background:#111824;color:#eef2fa;font:16px/1.6 system-ui}main{max-width:1120px;margin:auto;padding:24px}a{color:#a8d9ff}canvas{width:100%;background:#182536}button,select{font:inherit;padding:8px;margin:4px;max-width:100%}.note{padding:16px;background:#423b28}small{color:#c2d1e1}</style><main><h1>Walking: cadence and ground contact</h1><p>Left: previous native timing and pace. Right: installed timing and pace. Ground marks move at each fighter’s travel speed, so planted feet should hold against the ground during support. This is a sprite preview, not game footage.</p><p class="note">Timing fixes are installed. Some artwork still needs proper alternating leg phases, particularly Lloyd. The image generator is currently at its usage limit; those drawings are pending. Existing artwork, body scale and combat moves are retained.</p><select id="actor"></select><select id="direction"><option value="forward">Walk forward</option><option value="backward">Walk backward</option></select><button id="pause">Pause</button><button id="step">Next pose</button><button id="flip">Face left</button><p id="note"></p><canvas id="motion" width="1100" height="410"></canvas><p>Generated eight-pose loops now use 40 ticks forward and 48 backward instead of 16. Shared walking pace is 0.95 world units/tick forward and 0.72 backward; dash speed is retained.</p><p><a href="installation.json">Installation and pending artwork</a> · <a href="../roster.html">Main roster</a> · <a href="../proportions-v9/review.html">Earlier Lloyd/Mori artwork comparison</a></p></main><script>const data=DATA,cache={};let current=0,elapsed=0,paused=false,flip=false,last=null;
function img(path){if(!cache[path]){let im=new Image;im.src=path;cache[path]=im}return cache[path]}
function chosen(){return data.items[current][document.querySelector('#direction').value]||data.items[current].forward}
function pick(frames,ticks){let total=frames.reduce((n,f)=>n+f.ticks,0),t=((ticks%total)+total)%total;for(let i=0;i<frames.length;i++){if(t<frames[i].ticks)return {f:frames[i],i,total};t-=frames[i].ticks}return {f:frames[0],i:0,total}}
for(const [i,a] of data.items.entries()){let o=document.createElement('option');o.value=i;o.textContent=a.label+' ('+a.slug+')';document.querySelector('#actor').append(o)}
function select(){current=Number(document.querySelector('#actor').value);elapsed=0;last=null;for(const frames of Object.values(chosen()))frames.forEach(f=>img(f.file))}
document.querySelector('#actor').onchange=select;document.querySelector('#direction').onchange=select;
document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause';last=null};
document.querySelector('#step').onclick=()=>{paused=true;document.querySelector('#pause').textContent='Play';const a=chosen().after,p=pick(a,elapsed);elapsed=Math.floor(elapsed/p.total)*p.total+a.slice(0,p.i+1).reduce((n,f)=>n+f.ticks,0)};
document.querySelector('#flip').onclick=()=>{flip=!flip};
function draw(now){if(last!==null&&!paused)elapsed+=Math.min(100,now-last)*60/1000;last=now;const c=document.querySelector('#motion').getContext('2d');c.clearRect(0,0,1100,410);let pair=chosen(),direction=document.querySelector('#direction').value;let selected=[];
for(const [version,center] of [['before',275],['after',825]]){let p=pick(pair[version],elapsed);selected.push(p);let speed=data.speed[version][direction],f=p.f,im=img(f.file),z=4;c.save();c.beginPath();c.rect(center-270,0,540,410);c.clip();c.strokeStyle='#7990a4';c.beginPath();c.moveTo(center-270,355);c.lineTo(center+270,355);const shift=((elapsed*speed*z*(flip?-1:1))%48+48)%48;for(let x=center-320-shift;x<center+320;x+=48){c.moveTo(x,355);c.lineTo(x,367)}c.stroke();if(im.complete&&im.naturalWidth){c.translate(center,355);const reflected=(f.flip.includes('H')!==flip);if(reflected)c.scale(-1,1);c.drawImage(im,(-f.axis[0]*f.scale[0]+f.offset[0])*z,(-f.axis[1]*f.scale[1]+f.offset[1])*z,im.width*f.scale[0]*z,im.height*f.scale[1]*z)}c.restore();c.fillStyle='#eef2fa';c.font='18px system-ui';c.fillText(version==='before'?'Previous':'Installed',center-48,28)}
document.querySelector('#note').textContent=data.items[current].label+' · '+direction+' · cycle '+selected[0].total+' → '+selected[1].total+' ticks · '+(60/selected[1].total).toFixed(2)+' cycles/sec';requestAnimationFrame(draw)}
document.querySelector('#actor').value=String(data.items.findIndex(a=>a.slug==='lloyd'));select();requestAnimationFrame(draw);</script></html>'''
html=html.replace('Timing fixes are installed. Some artwork still needs proper alternating leg phases, particularly Lloyd. The image generator is currently at its usage limit; those drawings are pending. Existing artwork, body scale and combat moves are retained.','Complete: timing and ground-speed fixes are installed, and Lloyd now has a corrected eight-pose alternating-leg gait. Existing body scale and combat moves are retained.')
html=html.replace('Installation and pending artwork','Completed installation').replace('Earlier Lloyd/Mori artwork comparison','Lloyd/Mori artwork comparison')
(O/'review.html').write_text(html.replace('DATA',json.dumps(data)),encoding='utf-8');(G/'Review Walking Fixes.cmd').write_text('@echo off\nstart "" "%~dp0walk-fix-v11\\review.html"\n');print('WALK_REVIEW_BUILT',len(items),'body/form cycles')
