"""Package untouched native window captures as a timed looping replay."""
from pathlib import Path
from PIL import Image
import json,sys,re
SOURCE=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/urkel'
name=sys.argv[1].lower();assert name in ('robot','gadget','stefan')
capture=sys.argv[2] if len(sys.argv)>2 else name
assert re.fullmatch(r'[a-z0-9-]+',capture)
folder=SOURCE/'replays'/capture
rows=json.loads((folder/'timing.json').read_text(encoding='utf-8-sig'))
frames=[Image.open(folder/row['file']).convert('RGB') for row in rows]
durations=[max(20,rows[i+1]['milliseconds']-row['milliseconds']) if i+1<len(rows) else 900 for i,row in enumerate(rows)]
path=SOURCE/(name+'-replay.gif')
frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=0)
print('REPLAY_SAVED',path,len(frames),'native captures')
