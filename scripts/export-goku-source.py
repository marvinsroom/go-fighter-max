"""Read source sprite registrations without loading the 318MB archive into RAM."""
from goku_model import *
import struct,json,collections
ref=S/'reference';ref.mkdir(exist_ok=True)
sprites=[]
with (U/'Goku.sff').open('rb') as stream:
 header=stream.read(512);count,offset=struct.unpack_from('<II',header,20)
 for index in range(count):
  stream.seek(offset);h=stream.read(32)
  nxt,length,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',h)
  if length:
   pcx=stream.read(128);x1,y1,x2,y2=struct.unpack_from('<HHHH',pcx,4);size=(x2-x1+1,y2-y1+1)
  else:size=sprites[link]['size']
  sprites.append(dict(key=(g,n),axis=(x,y),size=size,offset=offset,length=length,link=link,shared_palette=bool(same)))
  offset=nxt
(ref/'sprites.json').write_text(json.dumps(sprites,indent=2))
groups=collections.defaultdict(list)
for s in sprites:groups[s['key'][0]].append(s)
(ref/'groups.json').write_text(json.dumps({g:dict(count=len(v),number_range=[min(s['key'][1] for s in v),max(s['key'][1] for s in v)],first_size=v[0]['size']) for g,v in groups.items()},indent=2))
print('GOKU_EXPORTED',len(sprites),'sprites',len(groups),'groups')
