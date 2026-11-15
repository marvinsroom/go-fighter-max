"""Lossless export of Nexus Gaming's SFF v1; production PNG SFF v2 writer."""
from pathlib import Path
from PIL import Image
import io, struct


def read_v1(path):
    data=Path(path).read_bytes()
    assert data[:12]==b'ElecbyteSpr\0' and data[15]==1
    count,offset=struct.unpack_from('<II',data,20)
    sprites=[];palette=None
    for i in range(count):
        nxt,length,x,y,group,number,link,same=struct.unpack_from('<IIhhHHHB',data,offset)
        if length:
            im=Image.open(io.BytesIO(data[offset+32:offset+32+length]))
            if im.mode in ('P','L'):
                if im.mode=='P' and (not same or palette is None):palette=im.getpalette()
                else:
                    im=Image.frombytes('P',im.size,im.tobytes());im.putpalette(palette)
                im.info['transparency']=0
            im=im.convert('RGBA')
        else:im=sprites[link]['image'].copy()
        sprites.append(dict(key=(group,number),axis=(x,y),image=im))
        offset=nxt
    return sprites


def write_v2(path,sprites):
    headers=[];payload=bytearray();keys=set()
    for s in sprites:
        if s['key'] in keys:continue
        keys.add(s['key']);im=s['image'].convert('RGBA');buf=io.BytesIO();im.save(buf,format='PNG')
        raw=struct.pack('<I',im.width*im.height*4)+buf.getvalue()
        headers.append(struct.pack('<HHHHhhHBBIIHH',*s['key'],im.width,im.height,*s['axis'],0,12,32,len(payload),len(raw),0,0))
        payload.extend(raw)
    header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2))
    lo=512+28*len(headers)
    struct.pack_into('<IIIIIIII',header,36,512,len(headers),lo,0,lo,len(payload),lo+len(payload),0)
    Path(path).write_bytes(header+b''.join(headers)+payload)


if __name__=='__main__':
    from PIL import ImageDraw
    import json
    root=Path(__file__).resolve().parents[1];folder=root/'sprite-fighter/characters/edward'
    sprites=read_v1(folder/'source/upstream/Edward/Sprite.sff')
    out=folder/'reference';out.mkdir(exist_ok=True)
    for s in sprites:s['image'].save(out/f"{s['key'][0]}-{s['key'][1]}.png")
    body=[s for s in sprites if s['key'][0]<8000 and s['image'].height>30 and s['image'].width<250]
    selected=body[::max(1,len(body)//32)][:32]
    sheet=Image.new('RGB',(1280,4*210),(24,29,40));d=ImageDraw.Draw(sheet)
    for i,s in enumerate(selected):
        im=s['image'];scale=min(145/im.width,175/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
        x=(i%8)*160+(160-im.width)//2;y=(i//8)*210+185-im.height
        sheet.paste(im,(x,y),im);d.text(((i%8)*160+8,(i//8)*210+190),str(s['key']),fill='white')
    sheet.save(out/'source-contact.png')
    (out/'sprites.json').write_text(json.dumps([dict(key=s['key'],axis=s['axis'],size=s['image'].size) for s in sprites],indent=2))
    print('EDWARD_EXPORTED',len(sprites),'sprites;',len(body),'body candidates')
