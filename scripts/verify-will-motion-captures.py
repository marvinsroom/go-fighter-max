"""Read captured game frames to check displacement and stopping after release."""
from pathlib import Path
from PIL import Image
import numpy as np,json
root=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/will'
names=['motion-before','motion-forward-released','motion-backward-released','motion-stopped']
values={}
for name in names:
    array=np.array(Image.open(root/(name+'.png')).convert('RGB'))
    r,g,b=[array[:,:,i].astype(float) for i in range(3)]
    yy,xx=np.indices(r.shape)
    mask=(yy>300)&(yy<690)&(xx<700)&(r>150)&(g>120)&(b<100)
    assert mask.sum()>100,'Will shirt region not detected'
    values[name]=round(float(xx[mask].mean()),2)
report={'checks':{
    'forward_displacement_visible':values[names[1]]>values[names[0]]+40,
    'backward_displacement_visible':values[names[2]]<values[names[1]]-40,
    'release_stops_motion':abs(values[names[3]]-values[names[2]])<3},
    'p1_yellow_pixel_centroid_x':values,
    'note':'Actual window captures; screen coordinates include camera movement. Not a world-speed measurement.'}
(root/'motion-runtime-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert all(report['checks'].values()),'A runtime movement check failed'
