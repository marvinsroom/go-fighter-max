"""Publish authentic native captures in the shared fighter review."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
from fighter_review import write_review
from pyowol_silk import write_silk_review
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/pyowol'
report=json.loads((S/'runtime-validation.json').read_text());assert report['status']=='Complete' and report['failed']==0
cases={}
for f in report['frames']:
    path=S/'replays'/f.get('capture_directory',report['capture_directory'])/f['file']
    with Image.open(path) as im:im.verify()
    cases.setdefault(f['case_name'],[]).append(dict(f,src=path.relative_to(S).as_posix()))
super_names=['Soul-Reaping Thread','Ghost Dagger Rain','Heavenly Silk Prison']
groups={'Ultimates':['Reaper of the Drifting Moon'],'Supers':super_names,'Skills':[n for n in cases if n in ('Silk Snare','Ghost Daggers','Thread Reel','Silent Step','Silken Veil')],'Normals':[m['name'] for m in json.loads((S/'build-report.json').read_text())['normal_moves']],'Intro and movement':[n for n in cases if n not in super_names+['Reaper of the Drifting Moon','Silk Snare','Ghost Daggers','Thread Reel','Silent Step','Silken Veil'] and n not in [m['name'] for m in json.loads((S/'build-report.json').read_text())['normal_moves']]]}
showcases=[name for name in cases if name in ('Light medium heavy chain','Normal to thread cancel','Ultimate facing left')]
if showcases:
    groups['Combos and positioning']=showcases
    groups['Intro and movement']=[name for name in groups['Intro and movement'] if name not in showcases]
data=dict(passed=report['passed'],cases=cases,groups=groups,revision=hashlib.sha256(json.dumps(report).encode()).hexdigest()[:12])
(S/'review-data.js').write_text('window.PYOWOL_REVIEW='+json.dumps(data)+';',encoding='utf-8')
build=json.loads((S/'build-report.json').read_text());poses=[(k,v) for k,v in build['poses'].items() if v['group']==50]
tiles=[]
for key,m in poses:
    im=Image.open(R/m['file']);scale=m['scale']*.62;im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    tiles.append((key,im))
cell_width=max(240,max(im.width for _,im in tiles)+32)
cell_height=max(300,max(im.height for _,im in tiles)+54)
canvas=Image.new('RGB',(6*cell_width,((len(poses)+5)//6)*cell_height),(17,19,29));draw=ImageDraw.Draw(canvas)
for i,(key,im) in enumerate(tiles):
    x=(i%6)*cell_width+(cell_width-im.width)//2;y=(i//6)*cell_height+cell_height-35-im.height
    canvas.paste(im,(x,y),im);draw.text(((i%6)*cell_width+10,(i//6)*cell_height+cell_height-22),key,fill='white')
canvas.save(S/'proportions-v5.jpg',quality=93)
(S/'proportion-audit.html').write_text('<!doctype html><meta charset="utf-8"><title>Pyo Wol proportions</title><style>body{background:#11131d;color:white;font:18px system-ui}img{max-width:100%}a{color:#bacbff}</style><a href="review.html">Back to review</a><h1>Pyo Wol proportions</h1><p>The comic redraw retains the existing visible height and foot registration of each compiled pose. Crouches and lunges keep their natural height.</p><img src="proportions-v5.jpg" alt="All registered body animation drawings at shared scale">',encoding='utf-8')
if (S/'art/thread-v6/backdrop.png').exists():write_silk_review(S,report)
write_review('pyowol')
