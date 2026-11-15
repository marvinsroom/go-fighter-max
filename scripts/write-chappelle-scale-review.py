"""Show the exact old/new pose scales and pivots with unmodified source art."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];CH=ROOT/'sprite-fighter/characters'
data={}
for slug in ['prince','tyrone']:
    report=json.loads((CH/slug/'paired-build-report.json').read_text())
    for form,label in enumerate(report['forms']):
        prefix='alt_' if form else ''
        data[label]={key.removeprefix(prefix):dict(m,file='../../'+m['file'].replace('\\','/').removeprefix('sprite-fighter/'))
                     for key,m in report['sprites'].items() if key.startswith('alt_')==bool(form)}
(CH/'chappelle/scale-data.js').write_text('window.CHAPPELLE_SCALES='+json.dumps(data)+';',encoding='utf-8')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chappelle pose proportions</title><style>
body{margin:0;background:#0b1120;color:#eef1ff;font:16px/1.6 system-ui}main{max-width:1100px;margin:auto;padding:30px 22px}a{color:#acd6ff}h1{font-size:38px}p{color:#bdc9e0}button,select{font:inherit;background:#243553;color:#fff;border:1px solid #7185a9;border-radius:7px;padding:9px 14px;margin:5px}button{cursor:pointer}canvas{width:100%;background:radial-gradient(ellipse at bottom,#2b3858,#10172a);border:1px solid #526486;border-radius:12px;margin-top:20px}img{width:100%;border-radius:12px}label{white-space:nowrap}
</style><main><a href="review.html">← Chappelle fighters</a><h1>Consistent proportions, pose to pose</h1><p>Compare the previous size and alignment with the corrected pose. Heads and bodies keep their proportions as knees bend and arms extend; feet stay on the ground line.</p>
<label>Form <select id="form"><option>Prince</option><option>Rick James</option><option>Tyrone Biggums</option><option>Negan</option></select></label>
<label>Pose <select id="pose"><option value="idle">Standing</option><option value="walk_a">Walk A</option><option value="walk_b">Walk B</option><option value="palm">Strike</option><option value="kick">Kick</option><option value="special">Special / jump</option><option value="crouch">Crouch</option><option value="hurt">Hit reaction</option><option value="down">Knockdown</option></select></label>
<button id="play">Cycle poses</button><button id="next">Next pose</button><canvas width="1100" height="530" aria-label="Previous and corrected Chappelle pose side by side"></canvas>
<p>Body size follows the pose; a crouch stays shorter and a raised arm can extend above the standing silhouette. The correction preserves the original drawings. Some perspective and drawing differences remain.</p>
<h2>Updated native gameplay</h2><img src="../prince/signature-replay-v3.gif" alt="Corrected Prince and Rick gameplay"><img src="../tyrone/signature-replay-v3.gif" alt="Corrected Tyrone and Negan gameplay">
<script src="scale-data.js"></script><script>
const data=window.CHAPPELLE_SCALES,form=document.querySelector('#form'),pose=document.querySelector('#pose'),canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d'),images={};
for(const poses of Object.values(data))for(const m of Object.values(poses)){const im=new Image();im.src=m.file;images[m.file]=im;}
let playing=false,last=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Cycle poses';};
document.querySelector('#next').onclick=()=>{playing=false;document.querySelector('#play').textContent='Cycle poses';pose.selectedIndex=(pose.selectedIndex+1)%pose.options.length;};
function draw(t){if(playing&&t-last>700){pose.selectedIndex=(pose.selectedIndex+1)%pose.options.length;last=t;}ctx.clearRect(0,0,1100,530);const m=data[form.value][pose.value],im=images[m.file];
for(let i=0;i<2;i++){const x=i?825:275,y=465,s=i?m.scale:m.previous_scale,a=i?m.axis:m.previous_axis;ctx.save();ctx.beginPath();ctx.rect(i*550,0,550,530);ctx.clip();ctx.strokeStyle='#596d91';ctx.beginPath();ctx.moveTo(i*550+25,y);ctx.lineTo(i*550+525,y);ctx.stroke();ctx.strokeStyle='#33445e';ctx.beginPath();ctx.moveTo(x,65);ctx.lineTo(x,y);ctx.stroke();ctx.fillStyle=i?'#b3edc8':'#bdc9e0';ctx.font='18px system-ui';ctx.fillText(i?'Corrected':'Previous',i*550+25,35);if(im.complete&&im.naturalWidth)ctx.drawImage(im,x-a[0]*s,y-a[1]*s,im.width*s,im.height*s);ctx.restore();}requestAnimationFrame(draw);}requestAnimationFrame(draw);
</script></main></html>'''
(CH/'chappelle/scale-review.html').write_text(html,encoding='utf-8')
print('CHAPPELLE_SCALE_REVIEW_WRITTEN')
