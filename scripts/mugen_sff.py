"""Read MUGEN v2 sprites and append lossless RGBA drawings to a derived archive."""
from pathlib import Path
from PIL import Image
import io,struct

def decode_pcx(raw,palette=None):
    """Decode legacy sprite PCX, bounding overlong final RLE rows as Ikemen does."""
    im=Image.open(io.BytesIO(raw))
    try:im.load()
    except OSError:
        assert raw[3]==8 and raw[65]==1,'Unsupported PCX layout'
        xmin,ymin,xmax,ymax=struct.unpack_from('<HHHH',raw,4)
        w=xmax-xmin+1;h=ymax-ymin+1;stride=struct.unpack_from('<H',raw,66)[0]
        assert 0<w<=stride<=4096 and 0<h<=4096
        pixels=bytearray();cursor=128
        while len(pixels)<stride*h:
            value=raw[cursor];cursor+=1;count=1
            if raw[2]==1 and value>=192:count=value&63;value=raw[cursor];cursor+=1
            pixels.extend(bytes([value])*min(count,stride*h-len(pixels)))
        im=Image.frombytes('P',(w,h),b''.join(pixels[y*stride:y*stride+w] for y in range(h)))
    if im.mode in ('P','L'):
        original_palette=im.getpalette();im=Image.frombytes('P',im.size,im.tobytes())
        if palette is not None:im.putpalette(palette)
        elif original_palette:im.putpalette(original_palette)
        im.info['transparency']=0
    return im.convert('RGBA')


def lz5(raw,size):
    out=bytearray();i=1;control=raw[0];bit=0;recycle=0;recycle_bits=0
    while len(out)<size:
        value=raw[i];i+=1
        if control&(1<<bit):
            if value&63==0:
                distance=((value<<2)|raw[i])+1;i+=1;length=raw[i]+3;i+=1
            else:
                recycle|=(value&192)>>recycle_bits;recycle_bits+=2;length=(value&63)+1
                if recycle_bits<8:distance=raw[i]+1;i+=1
                else:distance=recycle+1;recycle=recycle_bits=0
            for _ in range(length):
                if len(out)<size:out.append(out[-distance])
        else:
            if value&224==0:length=raw[i]+8;i+=1
            else:length=value>>5;value&=31
            out.extend(bytes([value])*min(length,size-len(out)))
        bit+=1
        if bit==8:
            bit=0
            if i<len(raw):control=raw[i];i+=1
    return out


class Sff:
    def __init__(self,path):
        self.data=Path(path).read_bytes();assert self.data[:12]==b'ElecbyteSpr\0'
        self.offset,self.count,self.paloff,self.palcount,self.lo,self.ls,self.to,self.ts=struct.unpack_from('<IIIIIIII',self.data,36)
        self.headers=[struct.unpack_from('<HHHHhhHBBIIHH',self.data,self.offset+i*28) for i in range(self.count)]
        self.keys={h[:2]:i for i,h in reversed(list(enumerate(self.headers)))}
    def decode(self,index):
        h=self.headers[index]
        if h[10]==0:return self.decode(h[6])
        start=(self.to if h[12]&1 else self.lo)+h[9];raw=self.data[start:start+h[10]]
        if h[7]==0 and h[8]==32:return Image.frombytes('RGBA',h[2:4],raw)
        if h[7] in (11,12):return Image.open(io.BytesIO(raw[4:])).convert('RGBA')
        if h[7]==2:
            decoded=bytearray();cursor=4
            while len(decoded)<h[2]*h[3]:
                value=raw[cursor];cursor+=1
                if value&0xc0==0x40:
                    count=value&0x3f;value=raw[cursor];cursor+=1
                    decoded.extend(bytes([value])*count)
                else:decoded.append(value)
            pixels=bytes(decoded)
        elif h[7]==4:pixels=lz5(raw[4:],h[2]*h[3])
        elif h[7]==10:pixels=Image.open(io.BytesIO(raw[4:])).tobytes()
        else:raise ValueError(('Unsupported sprite',h))
        p=struct.unpack_from('<HHHHII',self.data,self.paloff+h[11]*16)
        while p[5]==0:p=struct.unpack_from('<HHHHII',self.data,self.paloff+p[3]*16)
        palette=self.data[self.lo+p[4]:self.lo+p[4]+p[5]];rgba=bytearray()
        for n in pixels:rgba.extend(palette[n*4:n*4+3]+bytes([0 if n==0 else 255]))
        return Image.frombytes('RGBA',h[2:4],bytes(rgba))
    def derive(self,replacements,additions):
        """Entries are {(group,number): {png,image,axis}}; preserve original payload."""
        assert self.ts==0 and self.lo+self.ls==len(self.data)
        data=bytearray(self.data);extra=[];first={}
        def encode(group,number,frame,index):
            w,h=frame['image'].size;identity=frame['rgba_sha256']
            if identity in first:offset=length=0;link=first[identity]
            else:
                block=struct.pack('<I',w*h*4)+frame['png'];offset=len(data)-self.lo;length=len(block);data.extend(block);link=0;first[identity]=index
            return struct.pack('<HHHHhhHBBIIHH',group,number,w,h,*frame['axis'],link,12,32,offset,length,0,0)
        for i,h in enumerate(self.headers):
            frame=replacements.get(h[:2])
            if frame:data[self.offset+i*28:self.offset+(i+1)*28]=encode(*h[:2],frame,i)
        for j,(key,frame) in enumerate(additions.items()):extra.append(encode(*key,frame,self.count+j))
        # Additional sprite headers must immediately follow the sprite table.
        # Some archives have palette/padding bytes before their image payload.
        table_end=self.offset+self.count*28
        data[table_end:table_end]=b''.join(extra);lo=self.lo+28*len(extra)
        palette_offset=struct.unpack_from('<I',self.data,44)[0]
        if palette_offset>=table_end:
            struct.pack_into('<I',data,44,palette_offset+28*len(extra))
        struct.pack_into('<I',data,40,self.count+len(extra));data[12:16]=bytes((0,0,1,2))
        struct.pack_into('<IIII',data,52,lo,len(data)-lo,len(data),0)
        return bytes(data)
