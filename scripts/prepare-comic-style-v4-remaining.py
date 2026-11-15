"""Explicit costumes, weapon designs and sequential poses for remaining native banks."""
from comic_identity_v3 import *
import json

vm=['relaxed standing guard, sword lowered','same idle, small breathing change','walking left foot leading right','walking right foot leading right','low crouch with sword forward','jump launch, torso leaning right','airborne tuck with knees raised','airborne extension, legs angled right','standing sword guard across chest','chest-hit recoil leaning back','airborne knocked-back hurt','lying defeated, sword beside body','crouched recovery, free hand near ground','upright charge stance, sword close','free hand adjusting mask beside face OR adjusting spectacles for Academy','standing calm victory, sword lowered']
vc=['overhead sword attack preparation','extended sword thrust right','cross-cut follow-through','standing recovery, blade down','low coiled sword windup','rising slash right','descending overhead cut right','low attack recovery','low sword sweep right','extended ground lunge right','airborne sword slash right','descending airborne thrust right','upright sword power stance','low forward dash right','wide finishing slash right','quiet standing recovery']
vp=['rear-loaded sword windup, crouched ready','horizontal chest-height cut fully extended right','same cut follow-through, arm across chest','reverse rising diagonal cut right','reverse cut follow-through','forward thrust windup, point aimed right','full thrust, arm extended right','relaxed standing recovery, blade lowered','blade held close gathering power','deep forward stabbing lunge right','blade pulled back toward right hip','quiet grounded recovery','overhead downward cut right','low-to-high rising cut right','forward-leaning diagonal cut down-right','finishing horizontal sweep right']
pm=['neutral standing alert, hands relaxed','walk left foot forward right','passing walk, feet near center','walk right foot forward right','rear toe pushing off in walk cycle','low combat ready, hands raised','ascending jump, knees lifted','airborne forward tuck','low crouch with hand near ground','forearm guard at chest','hurt leaning backward','knocked down prone horizontally','composed entrance, one hand raised in fine thread gesture','victory upright relaxed','low forward evasive dash','upright channeling, hands near chest']
pc=['forward short dagger thrust at chest height right','fingers casting thread, arm extended right','horizontal outward dagger slash, torso twisted','low forward evasive lunge right','crouching forward dagger thrust near knees','low crouched thread sweep right near ground','rising diagonal dagger uppercut from half crouch','airborne descending dagger strike, knees bent','low trap placement, hand on ground','backward guarded evade, leaning left while facing right','upright neutral thread-control gesture, one hand lifted','powerful two-handed thread pull, wide stable stance']
pq=['neutral planted breathing pose','tiny inhale, shoulders rise slightly','breath peak, knees soften and hands shift slightly','exhale returns toward neutral','walk left foot forward contact','walk passing pose, rear knee under pelvis','opposite walk contact, right foot forward','opposite passing pose, left foot under pelvis','dash anticipation, bent knees and compressed torso','explosive low forward step right','low passing running stride, arms reverse','dash deceleration to low ready','compact low crouch ready','crouch guard, forearms protect chest','beginning rise, knees extend','standing guard, relaxed forearms at chest']
pa=['dagger windup, elbow back near ribs, weight on rear foot','stepping dagger thrust fully extended right at chest','dagger follow-through, elbow across body','dagger returns to waist, torso rises to ready','thread cast windup, hand near opposite shoulder','arm fully extended right, fingers splayed to cast','both elbows pull toward ribs, thread-reel gesture','relax near-neutral with hands at waist','low crouched dagger windup','low dagger cut right at ankle height','low follow-through, free palm near floor','balanced crouch, dagger near waist','airborne compact dagger windup, knees bent','descending diagonal dagger cut down-right','airborne follow-through, knees untuck for landing','light low landing, dagger settling at waist']
pu=['upright winding silk gesture, one hand across chest','both hands rise and spread as if opening a net','hands cross sharply at chest tightening web','hands pull down and apart near waist','low coiled dagger windup near rear hip','powerful stepping diagonal dagger slash right','follow-through cut down-right, planted boots','finishing balanced low crouch, dagger close','composed standing, thread pinched near chest','one hand extends right drawing thread taut','small decisive two-handed pull near waist','calm standing recovery, hand lowering at side']
pw=['walk left heel ahead contact, right toe pushing off behind','passing walk, right knee under pelvis, left supporting leg straight','opposite contact, right heel forward and left toe behind','opposite passing, left knee under pelvis and right leg supporting']
jbase=['relaxed upright dual-dagger guard','horizontal dagger slash right','deep forward dagger lunge right','high kick right, daggers held safely','low crouch guard','summoning command, free hand extended','chest-hit recoil','lying flat knocked down']
jwalk=['left heel forward contact','left foot rolling weight','right foot passing under pelvis','right knee advancing','right heel forward contact','right foot rolling weight','left foot passing under pelvis','left knee advancing']
jdag=['neutral two-dagger ready','dagger windup, torso coils','dagger cut extends right','dagger follow-through across torso','opposite dagger thrust right','both arms extend in crossing cut right','follow-through, blades near hip','returning to balanced dagger guard']
jjump=['jump anticipation crouch','jump takeoff extending legs','ascending jump tucked knees','airborne apex tucked knees','descending with legs extending','landing crouch','rising from landing crouch','standing recovery']
jsuper=['low dual-dagger ready','coiled windup with bent knees','driving dagger thrust right','wide crossing dual-dagger cut right','low forward lunging slash','rising uppercut dagger sweep right','both daggers cutting horizontally right','standing recovery']
jmutilate=['relaxed dual-dagger stance','lowering into a coiled crouch','full forward dagger lunge right','wide crossing cut right','both daggers crossed at chest','both daggers raised overhead','deep finishing forward dual-dagger lunge right','standing relaxed recovery']
sstance=['relaxed upright idle, sword diagonally down-right','idle breath, slight shoulder lift','lowering into crouch, sword guard','full crouch guard, sword forward','summoning windup, left hand at chest, sword down in right','summoning command, left hand extended right, sword down','equipping sword by lifting it from low ready','equipped ready, sword upright beside shoulder']
slight=['neutral low sword guard','drawing sword back across shoulder','first horizontal cut right at chest','first cut follows across body','low forward sword thrust right','reverse rising cut right','sword returns across hip','standing low sword recovery']
sheavy=['neutral heavy-sword ready','two-handed windup, blade back by shoulder','sword raised high over head','overhead windup apex, torso coiled','downward cut right, bent knees','low finishing follow-through right','pulling sword back toward hip','standing recovery with blade down']
sair=['low jump anticipation, free hand near ground','ascending jump, sword upright','airborne overhead sword windup','descending overhead sword strike down-right','airborne follow-through across body','descending side cut right','landing crouch, sword close to ground','standing recovery']
shurt=['standing chest-hit recoil','stronger backward recoil, sword still gripped','airborne fall backward, sword held safely','lying flat knocked down, sword by right hand','pushing torso off ground with free hand','kneeling on one knee lifting sword','half-standing rise from crouch','fully upright ready stance']
ssuper=['low coiled sword ready','low forward charging sword windup','sword raised overhead in deep stance','full-power diagonal overhead cut down-right','low follow-through, blade near ground','forward rising sword slash right','second driving forward sword thrust right','balanced recovery, blade aimed diagonally right']
sfinish=['neutral sword stance','gathering resolve, sword held before torso','deep forward sword lunge right','long sideways follow-through right','sword lifted overhead, torso twisted','jumping overhead windup','low finishing downward sword impact right','standing recovery, sword lowered']

path=R/'.tmp/comic-style-v4-requests.json';items=json.loads(path.read_text());legacy=json.loads((R/'.tmp/comic-legacy-requests.json').read_text())
for q in items:
 slug=q['slug']
 if slug not in ('vikir','jinwoo','pyowol'):continue
 source=next(v for v in legacy if v['slug']==slug and v['kind']==q['kind']);poses=[]
 q['references']=[str(REF/(slug+'.png'))]
 if slug=='vikir':
  group=source['frames'][0]['keys'][0][0]
  form='NIGHT HOUND' if group in (51,55) else 'ACADEMY' if group in (53,56) else 'HUNTER'
  identity=SPECS[slug]['identity']+' Keep head about 1/6.5 of standing height for a readable youthful face, not an adult model. Compact solid dark crimson sword, no red laser cloud.'
  if form=='HUNTER':identity+=' HUNTER costume: charcoal high-collar long coat, black zipper tunic, gray cuffs, dark gloves, brown belt, slim black trousers and boots.'
  if form=='NIGHT HOUND':
   identity='NIGHT HOUND in EVERY CELL. Entire face FULLY COVERED by fitted dark reddish bronze LONG POINTED BEAK mask with ROUND ivory lenses and fine gold rims; hood UP, charcoal cape over black combat clothing, gray cuffs, brown belt, dark trousers/boots. Human head, no animal ears or horns, no exposed face. Compact crimson sword. Image1 is mask/color context only, Image2 shows exact existing covered-head costume. Simplify rendering, preserve mask and body costume throughout.'
   q['references']=[str(C/slug/'references/tapas-cover.jpg'),str(C/slug/'archive/before-comic-style-v4/art/extracted/night-costume-reference.png')]
  if form=='ACADEMY':
   identity+=' ACADEMY costume in EVERY CELL: fitted charcoal/olive-black high mandarin collar with thin gold center stripe and collar edge, dark shoulder panels with small gold outlined shield patches, WHITE sleeves and WHITE side torso panels, gold-edged dark cuffs, dark trousers and simple shoes. Thin round dark spectacles, clear lenses with youthful red-brown eyes visible. No hunter coat, cape, blazer, tie, backpack or brown vest. Second image is actual comic uniform reference.'
   q['references'].append(str(C/slug/'references/academy-manhwa.png'))
  for frame in source['frames']:
   g,n=frame['keys'][0];bank=vp if g in (54,55,56) else vc if n>=16 else vm
   pose=bank[n if g in (54,55,56) else n%16]
   if form=='NIGHT HOUND' and n==14 and g==51:pose='free hand adjusting covered beak mask, hood stays up, face remains hidden'
   elif form=='HUNTER' and n==14:pose='holding a spare narrow beak mask beside exposed face in free hand, sword lowered'
   elif form=='ACADEMY' and n==14:pose='free hand adjusting thin round spectacles, sword lowered'
   poses.append(form+': '+pose)
 elif slug=='pyowol':
  identity=SPECS[slug]['identity']+' Preserve accepted costume and hair: high-tied waist-long WHITE hair with broad falling bangs, black long martial outer robe with navy crossed lapels, black throat collar, plain dark sash and trousers, dark wrapped boots. WHITE snake loops around back of neck and drapes down RIGHT shoulder onto chest, ATTACHED to torso in every pose, same size throughout. Pale delicate adult face, long outer eyelashes, red slit pupils. No rugged masculine jaw, short hair, white robe or bulky muscles.'
  for frame in source['frames']:
   g,n=frame['keys'][0]
   if n<16:pose=pm[n]
   elif n<28:pose=pc[n-16]
   elif 100<=n<116:pose=pq[n-100]
   elif 120<=n<136:pose=pa[n-120]
   elif 140<=n<152:pose=pu[n-140]
   else:pose=pw[n-160]
   poses.append(pose)
 else:
  sword=source['frames'][0]['keys'][0][0]==61005
  identity=SPECS[slug]['identity']+' All drawings keep OPEN BLACK long coat over plain WHITE crewneck T-shirt, black trousers and boots, pale adult face. Dense black fringe in broad shapes, narrow pale blue-violet eyes under low straight brows, long angular cheeks, restrained mouth. No boyish round face, ornate armor or spiky redesign.'
  if sword:
   identity+=' Every pose has ONE Demon King longsword: medium-broad straight PALE ICE-BLUE/CYAN blade with branching BLACK internal pattern, dark demon-wing crossguard, dark long handle and pointed pommel; blade about 70% of character height. Image2 is weapon shape ONLY, not a style reference. Do not copy its text, dimensions, shield or white background.'
   q['references'].append(str(C/slug/'art/greatsword/references/weapon-shape.jpg'))
  else:identity+=' TWO compact curved dark daggers with thin violet edges, one in each hand, throughout ordinary attacks. No giant blades, no glow clouds.'
  for frame in source['frames']:
   g,n=frame['keys'][0]
   if sword:
    bank=[sstance,['walk '+p+', sword carried diagonally by right shoulder' for p in jwalk],slight,sheavy,sair,shurt,ssuper,sfinish][n//8];pose=bank[n%8]
   elif n<8:pose=jbase[n]
   elif n<16:pose='walk '+jwalk[n-8]+', daggers lowered'
   elif n<24:pose=jdag[n-16]
   elif n<32:pose=jjump[n-24]+', daggers held safely'
   elif n<56:pose=jsuper[n-48]
   else:pose=jmutilate[n-56]
   poses.append(pose)
 q['pose_descriptions']=poses
 q['prompt']=f'''Production game animation atlas for {SPECS[slug]['name']}. Original comic face is the identity authority; any additional references have their explicit limited roles below. Draw new clear comic animation artwork.
{identity}
ART: economical comic ink contours, large flat color shapes, ONE broad HARD-EDGED shadow color per material. Hair is a few broad masses, not many glossy strands. Clothing uses only a few fold strokes near joints, not dense wrinkles. Skin base plus one shadow. No gradients, airbrush, leather shine, tiny decorative textures, sculpted superhero anatomy or generic anime beautification. Readable action-specific facial expressions, reference-specific eye openings and cheek proportions. Flowing cloth/hair simplified into clear graphic shapes.
EXACTLY {q['count']} separate COMPLETE full-body drawings in STRICT {q['columns']} columns x {q['rows']} rows, row-major list below. Each row's sequential action keeps the SAME head size, anatomy, camera and planted foot baseline; low poses naturally shorter without body enlargement. All active figures face screen-RIGHT, faces slightly toward viewer. Every sole, fingertip, blade tip, snake, robe and hair tip fully drawn inside its own cell, broad empty transparent gutters and at least 50px outer clearance. SHRINK whole poses to fit; no touching neighbours and no clipped parts or invisible-cell-edge truncation. No text, labels, panels, extra heads, extra actors, floor or scenic background. No baked attack arcs or giant effects: the game draws those separately.
'''+ '\n'.join(f'{i+1}. {pose}' for i,pose in enumerate(poses))+'''
TRUE TRANSPARENT background. Spacious production atlas, 2048 pixels or larger.'''
 Path(q['destination']).with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
path.write_text(json.dumps(items,indent=2));print('Fresh explicit requests prepared: Vikir, Jinwoo, Pyo Wol, 21 sheets')
