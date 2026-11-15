"""Package acknowledged renderer screenshots as review GIFs."""
from pathlib import Path
from PIL import Image
import json,sys
ROOT=Path(__file__).resolve().parents[1]
for slug in sys.argv[1:] or ['prince','negan','rick']:
    source=ROOT/'sprite-fighter/characters'/slug;report=json.loads((source/'native-preview-report.json').read_text())
    files=sorted((source/'replays'/report.get('capture_directory','native-v1')).glob('Chappelle_'+slug+'*.png'))
    assert len(files)==len(report['frames']),(slug,len(files),len(report['frames']))
    moves=list(dict.fromkeys(f['move'] for f in report['frames']))
    for move in moves:
        selected=[(files[i],f) for i,f in enumerate(report['frames']) if f['move']==move]
        frames=[Image.open(path).convert('RGB') for path,f in selected]
        durations=[max(20,round((selected[i+1][1]['tick']-f['tick'])*1000/60)) if i+1<len(selected) else 150 for i,(path,f) in enumerate(selected)]
        for im in frames:im.thumbnail((720,405))
        frames[0].save(source/(move+'-replay-v1.gif'),save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False)
        print('CHAPPELLE_REPLAY',slug,move,len(frames),flush=True)
    Image.open(files[0]).save(source/'engine-preview.png')
