"""Read Soulfire's SFF1, including PCX RLE runs crossing scanline boundaries."""
from pathlib import Path
from PIL import Image, ImageDraw
import struct, json, collections

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'sprite-fighter/characters/jin-mori'
U = S / 'source/upstream'
E = ROOT / 'sprite-fighter/engine/ikemen-go-v1.0.0'

def read_source():
    data = (U / 'Jin Mori.sff').read_bytes()
    count, offset = struct.unpack_from('<II', data, 20)
    sprites = []; palette = None
    for i in range(count):
        nxt, length, x, y, g, n, link, same = struct.unpack_from('<IIhhHHHB', data, offset)
        if length:
            raw = data[offset+32:offset+32+length]
            x1,y1,x2,y2 = struct.unpack_from('<HHHH', raw, 4)
            width,height = x2-x1+1,y2-y1+1
            stride = struct.unpack_from('<H', raw, 66)[0]
            assert raw[3] == 8 and raw[65] == 1
            if not same or palette is None:
                assert raw[-769] == 12
                palette = list(raw[-768:])
            decoded = bytearray(); pos = 128
            while len(decoded) < stride*height:
                v = raw[pos]; pos += 1
                if v >= 192:
                    decoded.extend([raw[pos]]*(v&63)); pos += 1
                else: decoded.append(v)
            im = Image.frombytes('P', (stride,height), bytes(decoded[:stride*height])).crop((0,0,width,height))
            im.putpalette(palette); im.info['transparency'] = 0; im = im.convert('RGBA')
        else: im = sprites[link]['image'].copy()
        sprites.append(dict(key=(g,n), axis=(x,y), image=im))
        offset = nxt
    return sprites

if __name__ == '__main__':
    ss=read_source(); out=S/'reference'; out.mkdir(exist_ok=True)
    groups=collections.defaultdict(list)
    for s in ss: groups[s['key'][0]].append(s)
    sheet=Image.new('RGB',(1200,((len(groups)+7)//8)*120),(28,32,43)); d=ImageDraw.Draw(sheet)
    for i,(g,items) in enumerate(groups.items()):
        s=items[0];v=s['image'].copy();v.thumbnail((140,90));x=i%8*150+(150-v.width)//2;y=i//8*120+92-v.height
        sheet.paste(v,(x,y),v);d.text((i%8*150+5,i//8*120+97),f'{g}: {len(items)}',fill='white')
    sheet.save(out/'source-groups.png')
    (out/'sprites.json').write_text(json.dumps([dict(key=s['key'],axis=s['axis'],size=s['image'].size) for s in ss],indent=2))
    print('Sprites',len(ss),'groups',list(groups))
