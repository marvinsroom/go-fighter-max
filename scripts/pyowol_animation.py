"""Connected animation sequences, registered body anchors and cut/impact audio."""
from pathlib import Path
import io,json,math,random,struct,wave
from PIL import Image
from isolated_sprite_atlas import extract

# Torso registration, rather than the middle of a flowing-hair/extended-arm box.
ANCHORS={
 'q':[.64,.64,.64,.64,.64,.64,.64,.64,.56,.56,.56,.60,.62,.62,.62,.62],
 'a':[.60,.46,.61,.64,.64,.49,.65,.64,.61,.47,.63,.63,.60,.60,.63,.63],
 'u':[.63,.55,.62,.64,.60,.47,.61,.62,.64,.50,.62,.64],
 'w':[.65,.67,.65,.67],
}

def load_sequences(assets):
    folder=assets.source/'art/animation-v5';(folder/'poses').mkdir(exist_ok=True)
    for sheet,columns,rows,prefix,reference,start in [('motion',4,4,'q',0,100),('combat',4,4,'a',4,120),('supers',4,3,'u',0,140),('walk',2,2,'w',0,160)]:
        tiles=extract(folder/f'{sheet}.png',columns,rows);scale=375/tiles[reference][0].height
        for i,(im,_) in enumerate(tiles):
            path=folder/f'poses/{prefix}{i}.png';im.save(path)
            assets.png(f'{prefix}{i}',path,375,start+i)
            meta=assets.meta[f'{prefix}{i}'];meta['scale']=scale;meta['bank']=sheet
            axis=[round(im.width*ANCHORS[prefix][i]),meta['bounds'][3]]
            meta['axis']=axis
            entry=list(struct.unpack('<HHHHhhHBBIIHH',assets.headers[-1]));entry[4:6]=axis
            assets.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*entry)

def author_sequences(A,NORMALS):
    act=A.action
    act(0,[('q0',12),('q1',10),('q2',12),('q3',10)])
    act(5,[('q0',-1)])
    for n in (6,10,11,47):act(n,[('q12',-1)],kind='C')
    act(12,[('q14',4),('q0',2)])
    for n,indices in [(20,[4,5,6,7]),(21,[7,6,5,4])]:
        act(n,[(f'w{i-4}',6 if n==20 else 7) for i in indices])
    act(22,[('w1',3),('q0',3)])
    act(40,[('q12',3)])
    act(41,[('a12',5),('a13',4)])
    act(42,[('a14',5)])
    act(43,[('a14',5)])
    act(52,[('a15',3),('q14',3),('q0',2)])
    for n in list(range(120,123))+list(range(130,134))+list(range(140,144))+list(range(150,157)):
        act(n,[('q13' if n in (131,141,151) else 'q15',8)])
    act(5120,[('m11',6),('q12',4),('q14',5),('q0',3)])
    act(190,[('q8',5),('q9',4),('q10',4),('q11',6),('u8',12),('u9',8),('u11',12),('q0',10)])
    act(191,[('q0',1)])
    for n in (180,181,195):act(n,[('u8',8),('u9',5),('u10',4),('u11',20)])
    for n,name,pose,start,damage,kind in NORMALS:
        row=12 if kind=='A' else 8 if kind=='C' else 4 if n==210 else 0
        recovery=5 if n%100==0 else 7 if n%100==10 else 10
        seq=[(f'a{row}',start),(f'a{row+1}',3),(f'a{row+2}',4),(f'a{row+3}',recovery)]
        if n==220:seq=[('u4',start),('u5',3),('u6',4),('u7',recovery)]
        if n==610:seq=[('a12',start),('a5',3),('a6',4),('a14',recovery)]
        box=(0,-155,300,0) if kind=='C' and n!=420 else (0,-345,330,-25)
        act(n,seq,active=(1,),kind=kind,attack=box)
    # Specials have their own connected casting / low-step paths.
    act(1000,[('a8',6),('a9',4),('a10',4),('a11',5),('q14',4),('q0',3)],kind='C')
    act(1100,[('a4',8),('a5',4),('a6',4),('a5',4),('a6',4),('a5',4),('a6',4),('a7',6),('q0',4)])
    for n in (1120,3200,4000):
        act(n,[('u0',10),('u1',4),('u2',4),('u3',6),('q0',6)],active=(1,),attack=(0,-360,380,-10))
    act(1200,[('q8',4),('q9',4),('q10',4),('q9',4),('q11',5),('q14',3)])
    act(1300,[('q15',3),('q11',4),('q10',4),('q8',4),('q14',5),('q0',8)])
    act(500,[('u8',10),('u9',7),('u10',4),('u11',8)])
    act(3000,[('a4',10),('a5',4),('a6',5),('a5',4),('a6',5),('a5',4),('a6',5),('a7',6),('q0',5)],active=(1,3,5),attack=(0,-360,550,-10))
    act(3100,[('a4',10),('a5',4),('a6',4),('a5',4),('a6',4),('a5',4),('a6',4),('a7',8),('q0',6)])
    act(1121,[('a5',6),('a6',4),('a5',5),('a6',4),('a7',7),('q0',22)])
    act(3201,[('u0',10),('u1',8),('u2',4),('u3',10),('u1',6),('u2',4),('u3',10),('u8',10),('u9',10),('u10',4),('u11',24)])
    act(4001,[('u0',10),('u1',6),('u2',4),('u3',12),
              ('u4',4),('u5',4),('u6',6),('u7',8),
              ('u8',18),('u9',16),('u4',4),('u5',4),('u6',6),('u7',8),
              ('u8',12),('u9',10),('u10',4),('u11',20)])

def write_audio(path):
    """Short filtered-noise cuts/impacts instead of repeated oscillator beeps."""
    randomizer=random.Random(1705);sounds=[];rate=22050
    for cue,duration in enumerate((.10,.15,.10,.55,.24)):
        samples=bytearray();low=0.;prev=0.
        for i in range(round(rate*duration)):
            t=i/rate;phase=t/duration;noise=randomizer.uniform(-1,1)
            low+=.16*(noise-low);high=noise-low
            if cue==0:sample=(high*.75+math.sin(2*math.pi*(3400*t-7000*t*t))*.16)*math.sin(math.pi*phase)**1.5
            elif cue==1:sample=(low*.7+high*.2+math.sin(2*math.pi*90*t)*.4)*math.exp(-phase*7)
            elif cue==2:sample=(high*.35+math.sin(2*math.pi*1800*t)*.3)*math.exp(-phase*10)
            elif cue==3:sample=(low*.5+math.sin(2*math.pi*(62*t-8*t*t))*.35)*math.sin(math.pi*phase)**2
            else:sample=(high*.3+low*.45)*math.sin(math.pi*phase)**1.3
            samples+=struct.pack('<h',round(max(-1,min(1,sample)) * 21000));prev=noise
        stream=io.BytesIO()
        with wave.open(stream,'wb') as wav:
            wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(samples)
        sounds.append(stream.getvalue())
    snd=bytearray(512);snd[:12]=b'ElecbyteSnd\0';snd[12:16]=bytes((0,0,0,1));struct.pack_into('<II',snd,16,len(sounds),512)
    for i,sound in enumerate(sounds):
        nxt=len(snd)+16+len(sound) if i<len(sounds)-1 else 0
        snd.extend(struct.pack('<IIII',nxt,len(sound),0,i)+sound)
    path.write_bytes(snd)

def export_player(A,air):
    """Expose the actual AIR frame timings/axes, including every short drawing."""
    import re
    lookup={(v['group'],v['number']):(k,v) for k,v in A.meta.items()}
    clips={}
    names={0:'Idle',20:'Forward walk',21:'Backward walk',200:'Hidden Fang',210:'Silk Finger',220:'Crescent Dagger',400:'Low Fang',410:'Ankle Thread',420:'Rising Fang',600:'Falling Fang',610:'Air Silk',620:'Descending Reaper',1000:'Silk Snare',1100:'Ghost Daggers',1120:'Thread Reel opening',1121:'Thread Reel',1200:'Silent Step',1300:'Silken Veil',3000:'Soul-Reaping Thread',3100:'Ghost Dagger Rain',3201:'Heavenly Silk Prison',4001:'Reaper of the Drifting Moon'}
    for block in re.split(r'(?=\[Begin Action )',air):
        match=re.match(r'\[Begin Action (\d+)\]',block)
        if not match or int(match[1]) not in names:continue
        frames=[]
        for line in block.splitlines():
            if not re.match(r'^\d+,\d+,',line):continue
            values=line.split(',');key,m=lookup[int(values[0]),int(values[1])]
            frames.append(dict(key=key,src=Path(m['file']).relative_to('sprite-fighter/characters/pyowol').as_posix(),ticks=int(values[4]),scale=m['scale'],axis=m['axis']))
        clips[names[int(match[1])]]=frames
    (A.source/'animation-data.js').write_text('window.PYO_ANIMATION='+json.dumps(clips)+';',encoding='utf-8')
