"""Prepare complete native pose templates, grouped by transformation identity."""
from pathlib import Path
from collections import defaultdict
import json,hashlib,math,shutil,sys
from PIL import Image
from mugen_sff import Sff
from edward_assets import read_v1
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0/chars'
FORM_GROUPS={
 'naruto':{
  'base':[0,6,20,40,120,122,200,210,220,5000],
  'sage':[11000,11020,11200,11300,12000],
  'ashura':[2000,2200,2210,2220,6000],
  'kcm1':[13000,13200,13300,14000],
  'kcm2':[15000,15200,15300,16000],
  'four-tails':[17000,17200,18000],
  'six-tails':[19000,19200,20000],
  'kurama':[2300]},
 'saitama':{'hero':[0,11,20,40,100,120,170,180,190,195,200,205,210,220,221,230,240,245,260,280,610,1000,1100,1110,1200,1300,1400,1500,1700,2002,2005,5000,5001,5002,5010,5011,5012,5020,5030,5031,5032,5040,5041,5042,5052,5060,5061,5062,5070,5071,5072],
 'genos':[250],'tatsumaki':[255],'king':[302],'silver-fang':[310]}}
IDENTITY={
 'base':'Naruto Uzumaki, Shippuden teenage human, spiky blond hair, blue eyes, three whisker marks per cheek, leaf forehead protector on black cloth with two trailing ties, black-shouldered orange zip jacket, orange trousers, black open-toed shinobi sandals. Preserve special cell-specific changes shown by the template; occasional final transition cells develop gold chakra, copy those rather than forcing base colors.',
 'sage':'Naruto Sage Mode: same teenage blond Naruto and orange/black outfit, orange-red pigmentation around eyes, horizontal toad pupils. NO invented red cape: this installed version wears his regular jacket. Match template clothing and props in each pose.',
 'ashura':'The installed Ashura Naruto: flame-shaped golden-orange chakra hair, black forehead band, gold/orange long open cloak panels with black magatama/line markings, black inner jacket and black trousers, glowing orange shoes. Match the specific black-and-gold balance and chakra extensions in the template; not KCM1. Long extra chakra arms/tails appear ONLY in the cells where the template has them.',
 'kcm1':'Naruto Kurama Chakra Mode 1: entire HUMAN body, hair, jacket and trousers luminous warm yellow-gold/orange, BLACK graphic magatama circles and stripe markings. Broad flame-shaped blond/gold hair, visible face/eyes/whisker marks. No normal orange cloth, no black trousers, no fox head or giant cloak. Extend chakra arms ONLY when shown in the template.',
 'kcm2':'Naruto Kurama Chakra Mode 2: HUMAN Naruto in golden long open chakra coat with black collar/magatama/circle marks, black inner clothing and trousers visible, golden flamelike hair, gold footwear and coat tails. Preserve exact garment silhouette and additional chakra limbs shown in each template cell. Do not revert to KCM1 gold trousers.',
 'four-tails':'Four-tailed Naruto transformed creature: deep crimson-red lean quadrupedal foxlike humanoid chakra body, pointed fox ears, white predatory eyes and mouth, FOUR long red tails. Low animal anatomy, elongated clawed arms, hunched back. No blond human head, no clothes. Keep EXACT silhouette, tail sweep, claws and limb direction of each template pose. Flat two-tone crimson/coral with clean dark ink contours, not a glossy fire cloud.',
 'six-tails':'Six-tailed Naruto transformed creature: dark crimson quadrupedal foxlike chakra body, SIX long red tails, white skeletal fox skull mask and white exposed rib cage/spine armor over torso, white pointed bony protrusions. Predatory low animal anatomy. No human clothes or blond hair. Preserve actual white bone mask/ribs and sweeping tails in each cell. Flat crimson and bone-white shapes with hard shadows.',
 'kurama':'Kurama golden chakra avatar: giant slender golden-orange NINE-TAILED FOX, long pointed ears and muzzle, black graphic chakra bands/circles on shoulders and limbs, angular feral eyes. Preserve specific fox pose and huge flowing nine-tail silhouettes in each source cell. No human Naruto, no extra head, no blue armor. Flat gold/ochre/cream comic shapes with black contours.',
 'hero':'Saitama, One Punch Man: bald lean adult man, simple oval head, flat deadpan oval eyes in calm poses and narrow serious eyes in forceful attacks, yellow zip-front bodysuit, short white cape attached with round dark clasps, red gloves and red boots, black belt with round gold buckle. Adult long-limbed anatomy around seven heads tall, visible neck, natural-sized head/hands/boots. Preserve props, outfit changes, detached flying fists or cutaway portions ONLY where explicitly present in the template. Full body drawings where source is full body. Match specific expressive mouth/eye changes, not generic handsome anime face.',
 'genos':'Genos assisting Saitama: slim adult cyborg, short spiky blond hair, black sclera with gold eyes, sleeveless BLACK fitted shirt, dark blue-black trousers, metallic silver/black mechanical arms with simple orange ports. Preserve every pose and hand blast geometry; flat illustrated comic style.',
 'tatsumaki':'Tatsumaki assisting Saitama: petite adult woman with short curled green hair, dark green eyes, black long-sleeved high-neck dress with flowing split skirt panels, bare legs and black shoes. Intentionally petite, not a tall fighter. Preserve each floating/casting pose.',
 'king':'King assisting Saitama: tall adult man, slicked-back blond hair, long scar lines over left eye, stern anxious long face, gray long-sleeved shirt and BLUE JEANS, dark shoes. Preserve slouch, walking and crouching poses. Special exclamation mark only where the template explicitly has it.',
 'silver-fang':'Silver Fang / Bang assisting Saitama: elderly athletic man, white swept spiky hair and heavy white eyebrows/mustache, black long-sleeved fitted martial shirt, WHITE trousers and dark slippers. Preserve martial poses and lean elderly build, flat comic ink.'}
for slug in sys.argv[1:] or ['naruto','saitama']:
 n=E/slug;a=G/'characters'/slug/'art/comic-style-v10';b=a/'before';b.mkdir(exist_ok=True);t=a/'templates';t.mkdir(exist_ok=True)
 for p in n.iterdir():
  if p.is_file() and p.suffix.lower() in ['.sff','.air','.cns','.cmd','.def','.zss','.snd','.act'] and not (b/p.name).exists():shutil.copy2(p,b/p.name)
 sf=next(b.glob('*.sff'));raw=sf.read_bytes()
 if raw[15]==1:sprites=read_v1(sf)
 else:
  s=Sff(sf);sprites=[dict(key=k,axis=s.headers[i][4:6],image=s.decode(i)) for k,i in s.keys.items()]
 bykey={s['key']:s for s in sprites};requests=[];allframes=[]
 for form,groups in FORM_GROUPS[slug].items():
  selected=sorted([s for s in sprites if s['key'][0] in groups],key=lambda s:s['key']);frames=[];seen={}
  for s in selected:
   key=s['key'];im=s['image'];bounds=im.getbbox()
   if bounds is None:continue
   # Speech/exclamation graphics remain native UI, not fighter bodies.
   if (slug=='saitama' and (key in [(195,1),(195,2),(302,23)] or (key[0]==1700 and im.width>200))) or (slug=='saitama' and key[0]==260 and key[1]!=9):continue
   cropped=im.crop(bounds);digest=hashlib.sha256(str(cropped.size).encode()+cropped.tobytes()).hexdigest()
   alias=dict(key=key,axis=s['axis'],size=im.size,bounds=bounds)
   if digest in seen:frames[seen[digest]]['aliases'].append(alias);continue
   source=t/(form+'-source-'+str(len(frames)).zfill(3)+'.png');cropped.save(source);seen[digest]=len(frames)
   frames.append(dict(form=form,source=str(source.relative_to(R)),bounds=bounds,size=im.size,axis=s['axis'],keys=[key],aliases=[alias],rgba_sha256=digest))
  # Slot one on every sheet is the same anatomical calibration figure.
  anchor=frames[0];capacity=23;cols=6
  for start in range(0,len(frames),capacity):
   chunk=frames[start:start+capacity];pageframes=[dict(anchor,calibration=True)]+chunk;count=len(pageframes);rows=math.ceil(count/cols);kind=form+'-'+str(start//capacity).zfill(2)
   canvas=Image.new('RGBA',(cols*480,rows*520));maxw=max(Image.open(R/f['source']).width for f in pageframes);maxh=max(Image.open(R/f['source']).height for f in pageframes);scale=min(360/maxw,400/maxh)
   for i,f in enumerate(pageframes):
    im=Image.open(R/f['source']);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.NEAREST);canvas.alpha_composite(im,(i%cols*480+(480-im.width)//2,i//cols*520+(520-im.height)//2))
   src=t/(kind+'.png');canvas.save(src)
   prompt=f'''Use case: style-transfer. Production illustrated fighting game sprite atlas. Image1 is POSE AND COSTUME TEMPLATE: redraw all {count} figures as new clear non-pixel illustrations. Preserve EXACT {cols} columns x {rows} rows, row-major order, partial final row as pictured; first figure is a repeated scale calibration reference, keep it. Do not merge, omit, rearrange or invent poses. Copy each cell's unique gesture, facing, limb extension, camera angle, weapon and expression. Small differences are animation inbetweens and MUST remain separate drawings.
IDENTITY: {IDENTITY[form]}
STYLE: clean expressive manga/manhwa comic ink matching the game's illustrated roster, strong economical contours, broad flat colors and ONE hard-edged shadow per material. No pixel art, gradients, airbrush, painterly textures, glossy skin or dense wrinkle detail. Humans have lean natural long-limbed proportions and smaller heads (about seven heads in standing height), never short-legged chibi. Low poses remain low, airborne poses remain airborne; do not stand up or replace unusual gestures. Match specific tail count/limbs on creature forms. Continuous figure silhouette, avoid detached accessories except where source has a separate projectile.
LAYOUT: every full figure, finger, toe, cape, tail tip and weapon completely inside its own cell. At least 65px empty transparent gutters between complete figures, 65px outer margins. Shrink entire figures consistently to fit the longest pose. Use one consistent physical anatomy/body scale across every cell, not equal bounding-box height. No floor, shadows, captions, labels, grid lines, scenic background, extra heads or extra actors. Any unused final cells remain transparent. TRUE TRANSPARENT background. Spacious atlas about 2880x2080px or larger.'''
   q=dict(slug=slug,form=form,kind=kind,count=count,columns=cols,rows=rows,frames=pageframes,prompt=prompt,references=[str(src)],destination=str(a/(kind+'.png')));requests.append(q);(a/(kind+'.prompt.txt')).write_text(prompt,encoding='utf-8')
  allframes.extend(frames);print(slug,form,len(frames),'unique drawings;',len(selected),'native keys',flush=True)
 (a/'requests.json').write_text(json.dumps(requests,indent=2),encoding='utf-8');(a/'coverage.json').write_text(json.dumps(dict(slug=slug,forms=list(FORM_GROUPS[slug]),drawings=len(allframes),keys=sum(len(f['aliases']) for f in allframes),sheets=len(requests)),indent=2));print('PREPARED',slug,len(requests),'sheets',flush=True)
