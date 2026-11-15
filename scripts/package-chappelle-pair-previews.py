from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1]
for slug in ['prince','tyrone']:
    source=ROOT/'sprite-fighter/characters'/slug;report=json.loads((source/'paired-preview-report.json').read_text())
    files=sorted((source/'replays'/report['capture_directory']).glob('Chappelle_pair_'+slug+'*.png'))
    assert len(files)==len(report['frames']),(slug,len(files),len(report['frames']))
    frames=[Image.open(p).convert('RGB') for p in files]
    for im in frames:im.thumbnail((720,405))
    info=report['frames'];durations=[max(20,round((info[i+1]['tick']-f['tick'])*1000/60)) if i+1<len(info) else 150 for i,f in enumerate(info)]
    frames[0].save(source/'paired-replay-v2.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False)
    print('CHAPPELLE_PAIR_REPLAY',slug,len(frames),flush=True)
