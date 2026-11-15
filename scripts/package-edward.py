"""Package native engine proof and exact compiled AIR playback for Edward."""
from pathlib import Path
import json,re,hashlib,html
from PIL import Image
from mugen_sff import Sff
from fighter_review import write_review

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/edward';O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/edward'
report=json.loads((S/'runtime-validation.json').read_text());assert report['status']=='Complete' and report['failed']==0
cases={}
for f in report['frames']:
    p=S/'replays'/f.get('capture_directory',report['capture_directory'])/f['file']
    with Image.open(p) as im:im.verify()
    cases.setdefault(f['case_name'],[]).append(dict(f,src=p.relative_to(S).as_posix()))
groups={}
for name in cases:
    group='Ultimates' if name.startswith('Elric Final') else 'EX and MAX' if any(x in name for x in (' Ex',' Max',' Medium',' Strong')) and not name.startswith(('Standing','Crouching','Air')) else 'Supers' if name in ('Rapid Fire Cannon','Stone Wall','Machine Gun Barrage','Stone Spike Barrage') else 'Normals' if name.startswith(('Standing','Crouching','Air ')) else 'Alchemy' if name in ('Cannon Fire','Machine Gun','Stone Pillar','Ed Bat','Stone Spike','Stone Hand') else 'Movement and charge'
    groups.setdefault(group,[]).append(name)
for name,group in [('Stone Spike facing left','Alchemy'),('Stone Spike Barrage facing left','Supers')]:
    if name in groups.get('Movement and charge',[]):
        groups['Movement and charge'].remove(name);groups.setdefault(group,[]).append(name)
groups={k:groups[k] for k in ('Ultimates','Supers','Alchemy','EX and MAX','Normals','Movement and charge') if k in groups}
data=dict(passed=report['passed'],cases=cases,groups=groups,revision=hashlib.sha256(json.dumps(report).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.EDWARD_REVIEW='+json.dumps(data)+';',encoding='utf-8')
art=S/'art/illustrated-v1'
design='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Edward — illustrated artwork</title><style>body{margin:32px auto;max-width:1100px;background:#101722;color:#e9edf3;font:17px system-ui;padding:20px}a{color:#a4e3fa}img{max-width:100%;background:#202a37;border-radius:12px}section{margin:38px 0}p{line-height:1.6}</style><a href="../../review.html">Back to combat review</a><h1>Edward Elric — illustrated artwork</h1><p>Based on Nexus Gaming’s 2025 release. The source sprites guide poses and costume; new artwork uses the illustrated roster style. Some source in-betweens share a semantic drawing. Native timing remains in the game.</p>'
for name in ('portrait','motion','combat','alchemy','reactions'):
    design+=f'<section><h2>{name.title()}</h2><p><a href="{name}.prompt.txt">Exact generation prompt</a></p><img src="{name}.png" alt="Edward {name} artwork"></section>'
design+='<section><h2>Original animation reference</h2><img src="../../reference/source-contact.png" alt="Source sprite contact sheet"><img src="../../reference/alchemy-contact.png" alt="Original alchemy and Alphonse sprites"></section></html>'
(art/'design-review.html').write_text(design,encoding='utf-8')
(S/'proportion-audit.html').write_text('<!doctype html><meta charset="utf-8"><title>Edward proportions</title><style>body{background:#101722;color:white;font:18px system-ui;padding:28px}img{max-width:100%}a{color:#a4e3fa}</style><a href="review.html">Back to combat review</a><h1>Edward proportions</h1><p>Uniform .92 body scale, shared anatomical scale per source bank, and separately registered Alphonse/construct layers.</p>'+''.join(f'<h2>{n.title()}</h2><img src="art/illustrated-v1/{n}.png" alt="{n} drawings">' for n in ('motion','combat','alchemy','reactions')),encoding='utf-8')
archive=Sff(O/'Edward.sff');rendered=S/'rendered';rendered.mkdir(exist_ok=True);sprite_data={}
for i,h in enumerate(archive.headers):
    key=f'{h[0]}-{h[1]}';p=rendered/(key+'.png');archive.decode(i).save(p)
    sprite_data[key]=dict(src='rendered/'+p.name,axis=list(h[4:6]),size=list(h[2:4]))
air=(O/'Animation.air').read_text(encoding='utf-8');actions={}
for block in re.split(r'(?=\[Begin Action\s+)',air,flags=re.I):
    match=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
    if not match:continue
    rows=[]
    for line in block.splitlines():
        if not re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',line):continue
        f=[x.strip() for x in line.split(';',1)[0].split(',')]
        while len(f)<9:f.append('')
        key=f'{int(f[0])}-{int(f[1])}'
        if key not in sprite_data:continue
        rows.append(dict(sprite=key,dx=int(f[2]),dy=int(f[3]),ticks=int(f[4]),flags=f[5],sx=float(f[7]) if f[7] else 1,sy=float(f[8]) if f[8] else 1))
    actions[match[1]]=rows
payload=json.dumps(dict(actions=actions,sprites=sprite_data))
(S/'animation-data.js').write_text('window.EDWARD_ANIMATIONS='+payload+';',encoding='utf-8')
viewer='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Edward — AIR animation review</title><style>body{max-width:1100px;margin:24px auto;padding:20px;background:#101722;color:#edf1f5;font:16px system-ui}a{color:#a4e3fa}canvas{width:100%;background:#202a37;border:1px solid #4b596a;border-radius:12px}button,select{font:inherit;padding:9px;margin:5px;background:#29394a;color:white;border:1px solid #596c7e;border-radius:6px}</style></head><body><a href="review.html">Back to native combat review</a><h1>Edward — compiled animation timing</h1><p>These are individual AIR actions. The combat review shows movement, helpers, sound timing and hit reactions together in the engine.</p><select id="action" aria-label="Animation action"></select><button id="play">Pause</button><button id="previous">Previous</button><button id="next">Next</button><select id="speed" aria-label="Playback speed"><option value="1">1×</option><option value=".5">½×</option><option value=".25">¼×</option></select><p id="detail"></p><canvas id="canvas" width="1000" height="650"></canvas><script src="animation-data.js"></script><script>
const data=window.EDWARD_ANIMATIONS,menu=document.getElementById('action'),canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d'),detail=document.getElementById('detail'),play=document.getElementById('play'),speed=document.getElementById('speed');
let index=0,playing=true,timer=null,images=new Map(),zoom=3,origin=[500,550];
const labels={0:'Idle',20:'Forward walk',21:'Backward walk',200:'Light punch',210:'Medium punch',220:'Heavy punch',1000:'Cannon Fire',3000:'Machine Gun Barrage',3010:'Rapid Fire Cannon',3020:'Stone Spike Barrage',3030:'Stone Wall',3100:'Elric Final opening',3105:'Elric Final confirmed',3115:'Alphonse',8525:'Ultimate cut-in'};
for(const id of Object.keys(data.actions)){const o=document.createElement('option');o.value=id;o.textContent=id+' · '+(labels[id]||'Animation');menu.append(o)}
function rows(){return data.actions[menu.value]||[]}
function fit(){let minX=0,maxX=0,minY=0,maxY=0;for(const f of rows()){const s=data.sprites[f.sprite];minX=Math.min(minX,f.dx-s.axis[0]*f.sx);maxX=Math.max(maxX,f.dx+(s.size[0]-s.axis[0])*f.sx);minY=Math.min(minY,f.dy-s.axis[1]*f.sy);maxY=Math.max(maxY,f.dy+(s.size[1]-s.axis[1])*f.sy)}zoom=Math.min(3,900/Math.max(1,maxX-minX),550/Math.max(1,maxY-minY));origin=[500-(minX+maxX)*zoom/2,325-(minY+maxY)*zoom/2]}
function schedule(){clearTimeout(timer);if(playing&&rows().length){const ticks=rows()[index].ticks;timer=setTimeout(()=>show(1),Math.max(16,(ticks<0?60:Math.max(1,ticks))*1000/60/Number(speed.value)))}}
function paint(){ctx.clearRect(0,0,1000,650);const f=rows()[index];if(!f){detail.textContent='Empty source action';return}const s=data.sprites[f.sprite],im=images.get(f.sprite);if(!im)return;ctx.save();ctx.translate(origin[0]+f.dx*zoom,origin[1]+f.dy*zoom);ctx.scale(f.flags.includes('H')?-1:1,f.flags.includes('V')?-1:1);ctx.drawImage(im,-s.axis[0]*f.sx*zoom,-s.axis[1]*f.sy*zoom,s.size[0]*f.sx*zoom,s.size[1]*f.sy*zoom);ctx.restore();detail.textContent='Action '+menu.value+' · Frame '+(index+1)+' / '+rows().length+' · '+f.ticks+' ticks · Sprite '+f.sprite}
function show(delta=0){clearTimeout(timer);if(rows().length)index=(index+delta+rows().length)%rows().length;const f=rows()[index];if(!f){paint();return}if(!images.has(f.sprite)){const im=new Image();images.set(f.sprite,im);im.onload=()=>{paint();schedule()};im.onerror=()=>{detail.textContent='Image failed to load: '+f.sprite};im.src=data.sprites[f.sprite].src}else{paint();schedule()}}
menu.onchange=()=>{index=0;fit();show()};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play';schedule()};document.getElementById('next').onclick=()=>{playing=false;play.textContent='Play';show(1)};document.getElementById('previous').onclick=()=>{playing=false;play.textContent='Play';show(-1)};speed.onchange=schedule;menu.value='0';fit();show();
</script></body></html>'''
(S/'animation-review.html').write_text(viewer,encoding='utf-8')
write_review('edward')
print('EDWARD_PACKAGE',len(cases),'native clips;',len(actions),'AIR actions')
