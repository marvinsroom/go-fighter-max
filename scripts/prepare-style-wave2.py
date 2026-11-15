"""Inventory original assets and prepare reviewable briefs; does not restyle runtime art."""
from pathlib import Path
import json,re,struct,io,hashlib,html
from PIL import Image,ImageDraw,ImageOps
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'style-wave2'
d=json.loads((O/'queue.json').read_text());sources={r['slug']:r for r in json.loads((G/'mugen-expansion/queue.json').read_text())['fighters']}
briefs={
'hiei':(46,'Compact, lean teenage swordsman; sharp black hair with a white forelock, white headband concealing Jagan eye, black outfit and white scarf, katana. Keep a mature athletic silhouette and the source Jagan and dragon techniques.'),
'itachi':(52,'Lean adult Uchiha, long black hair and framing bangs, forehead protector, Akatsuki black cloak with red clouds and high collar, controlled expression, Sharingan. Keep source crow, genjutsu and Susanoo assets distinct from his body.'),
'kisame':(55,'Tall muscular adult with blue-grey skin, cheek gills, small predatory eyes, short spiky dark-blue hair and Akatsuki cloak; huge wrapped Samehada sword. Preserve shark-form and water techniques present in the release.'),
'ash-ketchum':(40,'Recognizable young Pokemon trainer with cap, messy black hair, blue jacket, gloves, jeans and trainers, matching the imported costume. Visibly younger and shorter than adults. Preserve each of the six imported Pokemon as distinct characters with their own anatomy.'),
'ben-10':(46,'Recognizable teenage Ben Tennyson, brown hair, green eyes, source green jacket with black-and-white details, blue trousers, Omnitrix on left wrist. Keep lean teenage proportions and the source costume. Every imported alien needs an individual design and coherent size; Way Big and Ultimate Way Big stay genuinely giant.'),
'leonardo':(50,'Athletic green teenage mutant turtle with blue mask, brown shell and belt, two katana, three fingers, two toes. Readable long limbs and a solid shell, serious leader expression; preserve both sword silhouettes and source moves.'),
'donatello':(51,'Athletic green teenage mutant turtle with purple mask, brown shell and belt, long bo staff, three fingers and two toes. Slightly leaner silhouette, long limbs, clear two-hand staff grips. Match Leonardo in rendering and scale.'),
'raphael':(50,'Athletic muscular green teenage mutant turtle with red mask, brown shell and belt, paired sai, three fingers and two toes. Tough expression and a strong torso without stubby limbs; match the other turtles in rendering and scale.'),
'michelangelo':(50,'Athletic green teenage mutant turtle with orange mask, brown shell and belt, paired nunchaku, three fingers and two toes. Energetic expression, clear chain and weapon grips. Match the other turtles in rendering and scale.'),
'shredder':(55,'Adult human antagonist in source grey-purple armor and dark cloth, bladed helmet, obscured lower face, sharp shoulder and forearm blades, purple cape. Lean powerful anatomy, clear metal edges; preserve original weapon and transformation moves.'),
'kenpachi':(56,'Tall powerful adult swordsman, wild spiked black hair, scarred face, eyepatch, torn white captain haori over black shihakusho, worn jagged katana. Long legs and adult anatomy, fierce grin, no dwarf proportions. Preserve the source release abilities and any eyepatch states.'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def refs(path):
 text=path.read_text(encoding='cp1252',errors='replace');block=re.search(r'(?ims)^\[Files\](.*?)(?=^\[|\Z)',text)[1]
 return {k.lower():v.split(';')[0].strip().strip('"') for k,v in re.findall(r'(?im)^\s*([\w.]+)\s*=\s*(.*?)\s*$',block)}
class OriginalSprites:
 def __init__(self,path):
  self.raw=path.read_bytes();self.version=self.raw[15];self.records=[];self.keys={}
  if self.version==1:
   count,offset=struct.unpack_from('<II',self.raw,20);pal=None
   for i in range(count):
    nxt,length,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',self.raw,offset);pcx=self.raw[offset+32:offset+32+length]
    if length and len(pcx)>=769 and pcx[-769]==12 and (not same or pal is None):pal=pcx[-768:]
    self.records.append(dict(key=[g,n],axis=[x,y],link=link,pcx=pcx,palette=pal));self.keys.setdefault((g,n),i);offset=nxt
  else:
   self.sff=Sff(path)
   for i,h in enumerate(self.sff.headers):self.records.append(dict(key=list(h[:2]),axis=list(h[4:6]),size=list(h[2:4]),link=h[6] if h[10]==0 else None));self.keys.setdefault(h[:2],i)
 def decode(self,key):
  index=self.keys[key]
  if self.version!=1:return self.sff.decode(index)
  seen=set()
  while not self.records[index]['pcx']:
   assert index not in seen;seen.add(index);index=self.records[index]['link']
  r=self.records[index];im=Image.open(io.BytesIO(r['pcx']))
  try:im.load()
  except OSError:
   # A few upstream PCX streams overrun their final row. Match the engine's
   # bounded 8-bit row decoder instead of modifying the retained source asset.
   raw=r['pcx'];assert raw[3]==8 and raw[65]==1
   xmin,ymin,xmax,ymax=struct.unpack_from('<HHHH',raw,4);w=xmax-xmin+1;h=ymax-ymin+1;stride=struct.unpack_from('<H',raw,66)[0];pixels=bytearray();cursor=128
   assert 0<w<=stride<=4096 and 0<h<=4096
   while len(pixels)<stride*h:
    value=raw[cursor];cursor+=1;count=1
    if raw[2]==1 and value>=192:count=value&63;value=raw[cursor];cursor+=1
    pixels.extend(bytes([value])*min(count,stride*h-len(pixels)))
   im=Image.frombytes('P',(w,h),b''.join(pixels[y*stride:y*stride+w] for y in range(h)))
  if im.mode in ['P','L']:
   im=Image.frombytes('P',im.size,im.tobytes())
   if r['palette']:im.putpalette(r['palette'])
   im.info['transparency']=0
  return im.convert('RGBA')
 def metadata(self):
  out=[]
  for r in self.records:
   item={k:v for k,v in r.items() if k not in ['pcx','palette']}
   if self.version==1:
    data=r['pcx'];seen=set();index=r['link']
    while not data:
     assert index not in seen;seen.add(index);rr=self.records[index];data=rr['pcx'];index=rr['link']
    xmin,ymin,xmax,ymax=struct.unpack_from('<HHHH',data,4);item['size']=[xmax-xmin+1,ymax-ymin+1]
   out.append(item)
  return out
cards=[];totals={'fighters':0,'sprites':0,'actions':0,'frames':0}
for row in d['targets']:
 slug=row['slug'];folder=E/'chars'/slug;out=O/slug;out.mkdir(parents=True,exist_ok=True);files=refs(folder/(slug+'.def'));sf=OriginalSprites(folder/files['sprite']);air=(folder/files['anim']).read_text(encoding='cp1252',errors='replace')
 actions=[]
 for m in re.finditer(r'(?ims)^\s*\[Begin Action\s+(-?\d+)\s*\]([^\[]*(?:(?!\[Begin Action)[\s\S])*?)(?=^\s*\[Begin Action|\Z)',air):
  frames=[]
  for line in m[2].splitlines():
   parts=line.split(';')[0].split(',')
   if len(parts)>=5 and all(re.fullmatch(r'\s*-?\d+\s*',p) for p in parts[:5]):frames.append(dict(key=[int(parts[0]),int(parts[1])],offset=[int(parts[2]),int(parts[3])],duration=int(parts[4])))
  actions.append(dict(action=int(m[1]),frames=frames))
 amap={a['action']:a for a in actions};selected=[]
 for action in [0,20,21,40,50,200,210,220,230,300,400,5000,5150,10000,20000,30000,40000,50000,60000,70000,80000,90000]:
  if action not in amap:continue
  for f in amap[action]['frames'][:3 if action in [0,20,21] else 1]:
   key=tuple(f['key'])
   if key in sf.keys and key not in [s[1] for s in selected]:selected.append((action,key))
 # Source-only samples include helper/effect cells; they are explicitly not classified as body art.
 for a in actions:
  if len(selected)>=24:break
  if a['action']>=1000 and a['action']%1000==0 and a['frames']:
   key=tuple(a['frames'][0]['key'])
   if key in sf.keys and key not in [s[1] for s in selected]:selected.append((a['action'],key))
 selected=selected[:24];sheet=Image.new('RGB',(960,((len(selected)+5)//6)*190),'#1b2433');draw=ImageDraw.Draw(sheet);samples=[]
 for i,(action,key) in enumerate(selected):
  im=sf.decode(key);bounds=im.getbbox();cropped=im.crop(bounds) if bounds else im;cropped.save(out/(f'source-{key[0]}-{key[1]}.png'));fit=ImageOps.contain(cropped,(136,142),Image.Resampling.NEAREST)
  x=(i%6)*160;y=(i//6)*190;sheet.paste(fit,(x+(160-fit.width)//2,y+145-fit.height),fit);draw.text((x+8,y+151),f'Action {action}',fill='white');draw.text((x+8,y+167),f'Sprite {key[0]},{key[1]}',fill='#b6c6dd');samples.append(dict(action=action,key=list(key),source_size=list(im.size),visible_bounds=bounds))
 sheet.save(out/'original-samples.png');height,identity=briefs[slug]
 prompt='Create a production character design reference for our illustrated 2D fighter. Match the clean hand-drawn ink contours, restrained flat cel shading and readable side-view silhouettes of the installed Cid redesign-v7 and adult proportions-v9 references. Avoid glossy 3D rendering, painterly gradients, excessive surface detail, super-deformed bodies or oversized heads. '+identity+' Draw full body facing right, three-quarter fighting profile, transparent background, all weapons and costume edges inside the image. Adult fighters use long believable limbs; proposed neutral gameplay height '+str(height)+' world units, pending comparison with the existing lineup. Do not apply this height to summons or transformed bodies. This first design is not a replacement animation sheet. Later pose conversion must match each original frame, with fixed anatomy and ground root, explicit alternating support legs in locomotion, and separate body, weapon, summon and effect mappings. Preserve every original gameplay state, AIR timing, collision box, command and sound. Use original-samples.png only as an imported source pose/costume reference: some samples are effects and must not become whole characters.'
 (out/'design-brief.txt').write_text(prompt,encoding='utf-8')
 command_text=(folder/files['cmd']).read_text(encoding='cp1252',errors='replace')
 form_labels=list(dict.fromkeys(re.findall(r'(?im)^\s*\[State\s+-1,\s*GOLPE 1\s+([^\]]+)\]',command_text))) if slug=='ben-10' else []
 record=dict(slug=slug,name=row['name'],status='Original imported; style generation pending usage-limit reset',proposed_neutral_world_height=height,height_applied=False,identity_brief=identity,source_sff_version=sf.version,files=files,source_sha256={k:sha(folder/files[k]) for k in ['sprite','anim','cmd','sound']},sprites=sf.metadata(),actions=actions,samples=samples,source_form_labels=form_labels,classification='Raw complete archive inventory; body/form/effect separation requires manual review before any replacement',runtime_art_modified=False)
 (out/'inventory.json').write_text(json.dumps(record,indent=2));row.update(status=record['status'],inventory=slug+'/inventory.json',brief=slug+'/design-brief.txt',samples=slug+'/original-samples.png',proposed_neutral_world_height=height,height_applied=False)
 for k,n in [('fighters',1),('sprites',len(sf.records)),('actions',len(actions)),('frames',sum(len(a['frames']) for a in actions))]:totals[k]+=n
 cards.append('<article><h2>'+html.escape(row['name'])+'</h2><p>Original imported. Style conversion pending.</p><a href="../characters/'+slug+'/review.html">Controls and play</a> &middot; <a href="'+slug+'/inventory.json">Complete source inventory</a> &middot; <a href="'+slug+'/design-brief.txt">Design brief</a><p>'+str(len(sf.records))+' sprites / '+str(len(actions))+' actions. Proposed neutral height '+str(height)+'; not applied.</p><img src="'+slug+'/original-samples.png" alt="Original imported source samples for '+html.escape(row['name'])+'"><p>'+html.escape(identity)+'</p></article>')
 print(slug,len(sf.records),'sprites',len(actions),'actions',flush=True)
d.update(status='All original imports complete; art generation blocked by built-in usage limit',inventory_totals=totals,runtime_art_modified=False,recordings=False,generator_reset_epoch=1792672252,style_references=['../characters/cid/art/redesign-v7/movement-a.png','../proportions-v9/standing-comparison.png','../size-fix-v8/lineup-current.png'])
(O/'queue.json').write_text(json.dumps(d,indent=2))
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Next character style pass</title><style>body{font:16px/1.6 system-ui;background:#111824;color:#edf2fa;max-width:1100px;margin:auto;padding:24px}a{color:#a8d9ff}article,aside{background:#1d2a3c;margin:20px 0;padding:20px;border-radius:12px}img{display:block;width:100%;max-width:960px;height:auto;image-rendering:pixelated}h1{line-height:1.2}</style><h1>Next character style pass</h1><p><a href="../mugen-expansion/review.html">Original imports and controls</a> &middot; <a href="queue.json">Task status</a></p><aside><b>11 fighters ready for styling; new artwork has not been generated.</b><p>All ten new originals imported; Kenpachi uses his existing release. The built-in generator is usage-limited. Existing artwork remains installed. No recordings made. These images are source samples, not styled results.</p><p>Match <a href="../characters/cid/art/redesign-v7/movement-a.png">Cid linework</a>, <a href="../proportions-v9/standing-comparison.png">adult proportions</a> and the <a href="../size-fix-v8/lineup-current.png">JUS size lineup</a>. Child bodies stay shorter; large aliens and other giant forms retain separate sizes. Complete body/form/effect classification is required before pose replacement.</p></aside>'+''.join(cards)+'</html>'
(O/'review.html').write_text(page,encoding='utf-8');(G/'Review Next Character Styles.cmd').write_text('@echo off\nstart "" "%~dp0style-wave2\\review.html"\n')
print(json.dumps(totals))
