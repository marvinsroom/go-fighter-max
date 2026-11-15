"""Convert unsupported PCM32 clips to PCM24 without changing rate or duration."""
from pathlib import Path
import struct,json,hashlib
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def convert(wav):
 assert wav[:4]==b'RIFF' and wav[8:12]==b'WAVE';chunks=[];cursor=12;fmt=None
 while cursor+8<=len(wav):
  key,size=struct.unpack_from('<4sI',wav,cursor);value=wav[cursor+8:cursor+8+size];assert len(value)==size;chunks.append((key,value));cursor+=8+size+(size%2)
  if key==b'fmt ':fmt=struct.unpack_from('<HHIIHH',value)
 if not fmt or fmt[-1]!=32:return wav,None
 encoding,channels,rate,byte_rate,align,bits=fmt;assert encoding==1 and align==channels*4
 result=[];samples=0;discarded_max=0
 for key,value in chunks:
  if key==b'fmt ':value=struct.pack('<HHIIHH',1,channels,rate,rate*channels*3,channels*3,24)+value[16:]
  if key==b'data':
   assert len(value)%(channels*4)==0
   discarded_max=max(value[0::4],default=0)
   original=value;value=b''.join(original[i+1:i+4] for i in range(0,len(original),4));samples=len(original)//(channels*4)
   assert all(original[i*4+1:i*4+4]==value[i*3:i*3+3] for i in range(len(original)//4))
  result.append(key+struct.pack('<I',len(value))+value+(b'\0' if len(value)%2 else b''))
 body=b'WAVE'+b''.join(result);return b'RIFF'+struct.pack('<I',len(body))+body,dict(channels=channels,sample_rate=rate,sample_frames=samples,conversion='PCM32 to PCM24; no resampling',lossless=discarded_max==0,maximum_normalized_amplitude_error=discarded_max/(2**31))
for slug in ['leonardo','donatello','michelangelo']:
 folder=G/'characters'/slug;rp=folder/'import-report.json';report=json.loads(rp.read_text());original=folder/'source/upstream/sound.snd';native=E/'chars'/slug/'sound.snd';raw=original.read_bytes();assert sha(raw)==report['source_files_sha256']['sound.snd']
 if report.get('native_compatibility',{}).get('sound.snd'):
  assert sha(native.read_bytes())==report['native_compatibility']['sound.snd']['installed_sha256'];continue
 assert native.read_bytes()==raw
 count,offset=struct.unpack_from('<II',raw,16);entries=[];converted=[]
 for i in range(count):
  nxt,length,g,n=struct.unpack_from('<IIII',raw,offset);wav=raw[offset+16:offset+16+length];new,meta=convert(wav);entries.append((g,n,new))
  if meta:converted.append(dict(group=g,number=n,**meta))
  else:assert wav==new
  offset=nxt
 assert converted
 header_size=struct.unpack_from('<I',raw,20)[0];out=bytearray(raw[:header_size])
 for i,(g,n,wav) in enumerate(entries):out.extend(struct.pack('<IIII',len(out)+16+len(wav) if i+1<count else 0,len(wav),g,n)+wav)
 assert struct.unpack_from('<I',out,16)[0]==count
 native.write_bytes(out);report.setdefault('native_compatibility',{})['sound.snd']=dict(original_sha256=sha(raw),installed_sha256=sha(out),original_retained='source/upstream/sound.snd',converted_entries=converted,unaffected_wav_payloads='Byte-identical; all sound groups/numbers retained')
 report['modifications'].append('PCM32 to PCM24 format conversion for '+str(len(converted))+' source sound clips unsupported by Ikemen; original SND retained unchanged')
 rp.write_text(json.dumps(report,indent=2));validation=G/'mugen-expansion/validation'/(slug+'.json')
 if validation.exists():
  v=json.loads(validation.read_text());v['status']='Retest required after sound compatibility conversion';validation.write_text(json.dumps(v,indent=2))
 print(slug,len(converted),'clips converted to supported PCM24')
