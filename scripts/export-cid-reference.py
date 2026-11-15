"""Extract original indexed SFF sprites as PNG references, without repainting."""
from pathlib import Path
import struct,json
from PIL import Image
import io
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'sprite-fighter/characters/cid';data=(S/'source/upstream/.Cid/Cid.sff').read_bytes()
spriteoff,count,paloff,palcount,lo,ls,to,ts=struct.unpack_from('<IIIIIIII',data,36)
headers=[struct.unpack_from('<HHHHhhHBBIIHH',data,spriteoff+i*28) for i in range(count)]

def lz5(raw,size):
    i=1;out=bytearray();ct=raw[0];cts=0;rb=0;rbc=0
    while len(out)<size:
        d=raw[i];i+=1
        if ct&(1<<cts):
            if d&63==0:
                d=((d<<2)|raw[i])+1;i+=1;n=raw[i]+2;i+=1
            else:
                rb|=(d&192)>>rbc;rbc+=2;n=d&63
                if rbc<8:d=raw[i]+1;i+=1
                else:d=rb+1;rb=0;rbc=0
            for _ in range(n+1):
                if len(out)<size:out.append(out[-d])
        else:
            if d&224==0:n=raw[i]+8;i+=1
            else:n=d>>5;d&=31
            out.extend(bytes([d])*min(n,size-len(out)))
        cts+=1
        if cts==8:
            cts=0
            if i<len(raw):ct=raw[i];i+=1
    return out

def decode(index):
    h=headers[index]
    if h[10]==0:return decode(h[6])
    raw=data[(to if h[12]&1 else lo)+h[9]:(to if h[12]&1 else lo)+h[9]+h[10]]
    if h[7] in (11,12):return Image.open(io.BytesIO(raw[4:])).convert('RGBA')
    if h[7]==4:pixels=lz5(raw[4:],h[2]*h[3])
    elif h[7]==10:pixels=Image.open(io.BytesIO(raw[4:])).tobytes()
    else:raise ValueError(('Unsupported reference format',h[7],h[:2]))
    p=struct.unpack_from('<HHHHII',data,paloff+h[11]*16)
    while not p[5]:p=struct.unpack_from('<HHHHII',data,paloff+p[3]*16)
    palette=data[lo+p[4]:lo+p[4]+p[5]];rgba=bytearray()
    for color in pixels:rgba.extend(palette[color*4:color*4+3]+bytes([0 if color==0 else 255]))
    return Image.frombytes('RGBA',(h[2],h[3]),bytes(rgba))

folder=S/'reference';folder.mkdir(exist_ok=True)
references=[]
for group,number in [(0,32),(0,33),(0,34),(0,35)]:
    h=next(h for h in headers if h[:2]==(group,number));assert h[7]==4
    pixels=lz5(data[(to if h[12]&1 else lo)+h[9]+4:(to if h[12]&1 else lo)+h[9]+h[10]],h[2]*h[3])
    p=struct.unpack_from('<HHHHII',data,paloff+h[11]*16)
    while not p[5]:p=struct.unpack_from('<HHHHII',data,paloff+p[3]*16)
    palette=data[lo+p[4]:lo+p[4]+p[5]]
    rgba=bytearray()
    for index in pixels:rgba.extend(palette[index*4:index*4+3]+bytes([0 if index==0 else 255]))
    im=Image.frombytes('RGBA',(h[2],h[3]),bytes(rgba));path=folder/f'cid-idle-{number}.png';im.save(path)
    references.append({'file':str(path.relative_to(ROOT)),'sprite':[group,number],'size':list(im.size),'axis':list(h[4:6])})
(folder/'sprites.json').write_text(json.dumps(references,indent=2))
print('CID_ORIGINAL_PIXEL_REFERENCES_EXTRACTED',len(references))
