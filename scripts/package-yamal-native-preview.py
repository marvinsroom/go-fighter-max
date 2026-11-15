"""Package native screenshot frames; no recreation of game visuals."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'sprite-fighter/characters/yamal'
report=json.loads((SOURCE/'native-preview-report.json').read_text())
files=sorted((SOURCE/'replays/native-release').glob('Yamal_Native_Review*.png'))
assert len(files)==len(report['frames']),(len(files),len(report['frames']))
for move in ['movement','curler','rainbow','super','ultimate']:
    selected=[(files[i],f) for i,f in enumerate(report['frames']) if f['move']==move]
    frames=[Image.open(path).convert('RGB') for path,f in selected]
    durations=[max(20,round((selected[i+1][1]['tick']-f['tick'])*1000/60)) if i+1<len(selected) else 150 for i,(path,f) in enumerate(selected)]
    assert frames,move
    for im in frames:im.thumbnail((800,450))
    frames[0].save(SOURCE/f'{move}-replay-v1.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False)
    print('YAMAL_REPLAY',move,len(frames))
Image.open(files[0]).save(SOURCE/'engine-preview.png')
