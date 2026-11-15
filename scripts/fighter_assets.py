"""Original-PNG sprite containers and AIR authoring for standalone fighters."""
from pathlib import Path
from PIL import Image
import hashlib, io, math, struct, wave

class FighterAssets:
    def __init__(self,root,slug):
        self.root=Path(root);self.source=self.root/'sprite-fighter/characters'/slug
        self.output=self.root/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'/slug
        self.output.mkdir(parents=True,exist_ok=True)
        self.payload=bytearray(b''.join(bytes((i,i,i,0 if i==0 else 255)) for i in range(256)))
        self.headers=[];self.meta={};self.air=[]
    def png(self,key,path,height,number,group=50):
        path=Path(path);raw=path.read_bytes()
        with Image.open(path) as im:
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,path
            w,h=im.size;bounds=im.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()
        assert bounds,path
        axis=((bounds[0]+bounds[2])//2 if key=='down' else w//2,bounds[3])
        offset=len(self.payload);block=struct.pack('<I',w*h*4)+raw;self.payload.extend(block)
        self.headers.append(struct.pack('<HHHHhhHBBIIHH',group,number,w,h,*axis,0,12,32,offset,len(block),0,0))
        self.meta[key]={'group':group,'number':number,'axis':axis,'bounds':bounds,'scale':height/(bounds[3]-bounds[1]),
                        'file':str(path.relative_to(self.root)),'sha256':hashlib.sha256(raw).hexdigest()}
    def alias(self,group,number,key):
        m=self.meta[key]
        index=next(i for i,h in enumerate(self.headers) if struct.unpack_from('<HH',h)==(m['group'],m['number']))
        fields=list(struct.unpack('<HHHHhhHBBIIHH',self.headers[index]))
        fields[0]=group;fields[1]=number;fields[6]=index;fields[9]=0;fields[10]=0
        self.headers.append(struct.pack('<HHHHhhHBBIIHH',*fields))
    def raw(self,number,width,height,fn,axis=None):
        pixels=bytearray()
        for y in range(height):
            for x in range(width):pixels.extend(fn(x,y))
        offset=len(self.payload);self.payload.extend(pixels)
        self.headers.append(struct.pack('<HHHHhhHBBIIHH',7000,number,width,height,*(axis or (width//2,height//2)),0,0,32,offset,len(pixels),0,0))
    def write_sff(self,name):
        header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2))
        pal=512+28*len(self.headers);start=pal+16
        struct.pack_into('<IIIIIIII',header,36,512,len(self.headers),pal,1,start,len(self.payload),start+len(self.payload),0)
        archive=bytes(header)+b''.join(self.headers)+struct.pack('<HHHHII',1,1,256,0,0,1024)+self.payload
        keys=[struct.unpack_from('<HH',h) for h in self.headers];assert len(keys)==len(set(keys))
        for m in self.meta.values():
            entry=struct.unpack('<HHHHhhHBBIIHH',self.headers[keys.index((m['group'],m['number']))])
            offset,size=entry[9:11]
            assert hashlib.sha256(archive[start+offset+4:start+offset+size]).hexdigest()==m['sha256']
        (self.output/name).write_bytes(archive);return len(archive)
    def action(self,number,frames,active=(),kind='S',attack=(20,-315,220,-100),hurt=True):
        self.air.append(f'\n[Begin Action {number}]')
        for i,(key,duration,*extra) in enumerate(frames):
            if hurt:
                box=(-60,-225,65,0) if kind=='C' else (-55,-355,65,0)
                self.air.extend(['Clsn2: 1','Clsn2[0] = '+','.join(map(str,box))])
            if i in active:self.air.extend(['Clsn1: 1','Clsn1[0] = '+','.join(map(str,attack))])
            m=self.meta[key];s=m['scale']
            self.air.append(f'{m["group"]},{m["number"]},0,0,{duration},,,{s:.7f},{s:.7f},{extra[0] if extra else 0}')
    def write_air(self,name):(self.output/name).write_text('\n'.join(self.air)+'\n',encoding='utf-8')
    def sounds(self,name,cues):
        sounds=[]
        for frequency,duration in cues:
            rate=22050;pcm=bytearray()
            for i in range(int(rate*duration)):
                t=i/rate;sample=int(11000*(1-t/duration)**2*math.sin(2*math.pi*(frequency*t+120*t*t)))
                pcm.extend(struct.pack('<h',sample))
            stream=io.BytesIO()
            with wave.open(stream,'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(pcm)
            sounds.append(stream.getvalue())
        snd=bytearray(512);snd[:12]=b'ElecbyteSnd\0';snd[12:16]=bytes((0,0,0,1));struct.pack_into('<II',snd,16,len(sounds),512)
        for i,sound in enumerate(sounds):
            nxt=len(snd)+16+len(sound) if i<len(sounds)-1 else 0
            snd.extend(struct.pack('<IIII',nxt,len(sound),0,i)+sound)
        (self.output/name).write_bytes(snd)
