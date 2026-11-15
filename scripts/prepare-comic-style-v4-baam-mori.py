"""Fresh comic-led drawing requests, with every legacy pose and form explicit."""
from comic_identity_v3 import *
import json

bm=['open-palm guard','alternate breathing guard','walk left foot leading screen-right','walk right foot leading screen-right','low crouching guard','running stride screen-right','rising jump with tucked knee','airborne kicking-ready pose','standing crossed-forearm block','crouching crossed-forearm block','chest recoil hurt','shoulder recoil hurt','airborne falling backwards hurt','lying defeated on side','rising on one knee','calm standing victory, hand on chest']
bc=['open-palm guard','punch anticipation, fist back','straight punch fully extended right','elbow anticipation across chest','forward elbow strike right','knee lift preparation','high roundhouse kick right','finishing spinning kick right','hands gathered at hip, charging','forward open-palm thrust right','both cupped palms forward casting','one palm defensive stop','low sweeping kick right','crouching palm thrust right','airborne forward palm thrust right','palm thrust follow-through recovering guard']
bs=['relaxed arms down','raises open greeting hand toward opponent','adjusting dark sleeve cuff with other hand','nods and settles in guard','hands gather at hip','cupped palms held forward at chest','compressing a SMALL black orb with thin cyan rim between palms','both hands extended right to release','hands gather at hip','cupped palms held forward at chest','compressing a SMALL black orb with thin cyan rim between palms','both hands extended right to release','leaning advancing palm strike','palm follow-through','separates hands recovering','calm open-palm guard']
bt=['neutral open-palm stance','palm anticipation, torso turned back, hand cocked at shoulder','explosive forward palm strike, deep weight transfer, other hand at hip','recoil recovery, hand sweeping down','low forward dash, hands gathered at rear hip','driving palm lunge right, rear leg extended','reverse-flow stop gesture, upright palm, broad low stance','upward counterstrike with rising palm heel','aiming index and middle fingers right, other hand at hip','one-handed snapping palm launch right','coiled anticipation, elbows crossed','stepping double-palm thrust right','close-range elbow strike, torso twisting','rising double-palm strike, bent knees','overhead diagonal palm-cut windup, arm high','downward diagonal palm-cut finish']
bu=['neutral open-palm guard','commanding gathering stance, one arm above head, other palm by waist','arms spread wide opening a field, planted feet','both hands closing toward chest, torso twisted','single palm lifting upward toward opponent','full-power release, BOTH arms extended right in deep braced lunge','recoil aftermath, leaning forward, one arm extended, other near chest','composed finish, palms lowering into guard']
transition=['EARLY BAAM: short hair, red waistcoat, tan pants, calm open-palm guard','EARLY BAAM: lowers hands to waist, scarf flutters','TRANSITION: hair extends to nape, dark robe starts forming over red vest at shoulders','TRANSITION: hair extends to shoulders, black robe reaches knees, red vest partly visible','TRANSITION: hair extends to mid-back, robe nears ankles, tan trousers darkening','VIOLE: waist-length hair tied low, black robe closes, white/red FUG rings appear on side panel','VIOLE: hands settle into open-palm guard, full black FUG robe and long tied hair','VIOLE: finished calm guard with full black FUG robe and long tied hair']
mm=['relaxed fighting guard','alternate idle breathing guard','walking left foot leading right','walking right foot leading right','low crouch, one hand near ground','running forward, torso leaning','jumping with tucked knees','jumping extended descent, both legs angled right','high crossed-forearm guard','low crouching forearm guard','chest-hit recoil','head-hit recoil','falling sideways through air','lying defeated on side','rising from one knee','cheerful two-finger greeting']
mc=['fighting guard','straight punch preparation, fist back','straight punch fully extended right','elbow strike preparation across chest','elbow strike extended right','roundhouse kick chamber, knee lifted','roundhouse kick fully extended horizontally right','roundhouse kick follow-through','high-kick knee chamber','high kick fully extended diagonally up-right','high-kick retract','airborne spinning-kick chamber','airborne spinning kick extended right','airborne kick landing recovery, hand low','low sweep crouching windup','low sweeping leg kick extended right']
ms=['upright hands gathering energy','hand-blade slash windup','hand-blade horizontal slash right','defensive open-hand counter stance','palm counter extended right','powerful kick chamber, knee raised','horizontal side kick fully extended right','landing recovery with bent knees','upright confident ready stance, hands down','hand near forehead, alert eyes','gripping red staff with gold end caps at waist','sweeping staff horizontally right','lifting staff overhead','jumping overhead staff windup','downward staff impact lunge right','dignified recovery, staff planted vertically']
km=['fighting guard','walking left foot leading right','walking right foot leading right','low crouch, hand near ground','running forward','rising jump with knee raised','airborne horizontal kick right','high crossed-forearm block','punch preparation, fist back','straight punch fully extended right','knee chamber for high kick','high kick extended diagonally right','knee chamber with fist raised','high kick extended upward right','chest-hit recoil leaning back','falling sideways through air']
ks=['regular guard, black wristbands','touches goggles near forehead','holds fingers at goggles, thoughtful expression','extends free palm right in a calm gesture','standing relaxed with arms down','hands gather near waist, head lowered','touches forehead, eyes serious','arms spread, head tilted up, gathering resolve']+ms[8:]
mt=['BASE: green goggles, black wristbands, no pelt; clenched fists low','BASE: green goggles, black wristbands, no pelt; slightly tightened resolve','TRANSITION: goggles replaced by thin gold circlet, wristbands begin turning red; no pelt yet','KING: gold circlet, red wrist guards, tiger pelt now appearing; fists low','KING: gold circlet, red wrist guards and full pelt; firm stance','KING: gold circlet, red wrist guards and full pelt; slightly raised elbows','KING: gold circlet, red wrist guards and full pelt; fists rising toward face','KING: gold circlet, red wrist guards and full pelt; finished fighting guard']

path=R/'.tmp/comic-style-v4-requests.json';items=json.loads(path.read_text())
legacy=json.loads((R/'.tmp/comic-legacy-requests.json').read_text())
for q in items:
 if q['slug'] not in ('baam','jin-mori'):continue
 slug=q['slug'];source=next(v for v in legacy if v['slug']==slug and v['kind']==q['kind']);poses=[]
 if slug=='baam':
  for frame in source['frames']:
   group,n=frame['keys'][0]
   if group==62300:pose=transition[n]
   else:
    bank={62000:bm,62001:bc,62100:bm,62101:bc,62200:bs,62400:bt,62500:bt,62600:bu}[group]
    viole=group in (62100,62101,62500) or (group==62200 and n>=8) or (group==62600 and n>=8)
    pose=('VIOLE: ' if viole else 'EARLY BAAM: ')+bank[n%8 if group==62600 else n]
   poses.append(pose)
  identity='Two forms of the same slim youthful Baam. EARLY BAAM has the first panel’s small gentle youthful face, golden-brown eyes, short rounded dark fringe, RED buttoned waistcoat, charcoal scarf and shirt, TAN trousers and dark boots. VIOLE has very LONG straight black/dark-brown hair tied low, broad bangs concealing eyes, BLACK high-collar ankle-length FUG robe with red/white circle motifs on hanging side panel, black trousers/boots. Second panel is Viole. Apply outfits ONLY where the individual pose says so. No invented armor, horns, weapons or new clothes.'
  if all(p.startswith('VIOLE:') for p in poses):q['references']=[str(REF/'viole.png')]
  elif all(p.startswith('EARLY BAAM:') for p in poses):q['references']=[str(REF/'baam.png')]
  else:q['references']=[str(REF/'baam.png'),str(REF/'viole.png')]
 else:
  for frame in source['frames']:
   group,n=frame['keys'][0]
   if group==62304:pose=mt[n]
   else:
    bank={62000:mm,62001:mc,62002:ms,62300:km,62301:mc,62302:ks}[group]
    king=group in (62300,62301) or (group in (62002,62302) and n>=8)
    pose=('KING: ' if king else 'BASE: ')+bank[n]
   poses.append(pose)
  identity='Jin Mori exactly as the original early manhwa face: huge dark brown oval irises, simple youthful rounded cheeks, thin expressive brows, tiny nose and action-appropriate mouth. Spiky brown-black hair. BASE has broad olive GREEN goggles with diamond pattern, white short-sleeve martial shirt with black collar/cuffs, loose BLUE rolled trousers, RED sash, black wristbands, blue shoes and white ankle wraps. KING keeps the SAME YOUTHFUL FACE and anatomy, but has a thin GOLD curling circlet (NEVER green goggles), red wrist guards, white-edged tiger pelt at waist, long red sash; the same white shirt and blue trousers. Staff only where named: RED shaft, GOLD end caps. No stern narrow-eyed adult redesign. Preserve individual expressions: composed guard, focus during attacks, pain during hurt, cheerful greeting, dignified King.'
  q['references']=[str(REF/'jin-mori.png')]
 q['pose_descriptions']=poses
 q['prompt']=f'''Production comic character animation atlas, {SPECS[slug]['name']}. Supplied panel(s) are the ONLY visual identity reference. New drawings, not polished promotional anime art.
{identity}
Use economical expressive comic ink contours, bold flat color blocks and ONE broad hard-edged shadow tone per material. Skin is base plus one shadow, hair is one clear mass with at most one broad highlight. Cloth folds are a FEW purposeful strokes at joints. No gradients, airbrush, glossy strands, dense wrinkle webs, leather shine, ornamental additions or sculpted model anatomy. Make specific comic facial geometry readable. Do not stamp the same grin on every action.
EXACTLY {q['count']} separate COMPLETE full-body drawings in STRICT {q['columns']} columns x {q['rows']} rows; last row partial if needed. Read the numbered list for the exact form AND pose in EACH CELL. Every active figure faces screen-right in three-quarter view. Same head size, physical anatomy and ground baseline across related frames; crouches/jumps naturally alter height without changing body scale. Entire hair, both feet, fingertips, robe, staff and all props MUST fit inside their own cell with generous transparent gutters and at least 50px outer clearance. Make figures smaller to fit. No touching figures, scenery, text, inset portraits, extra actors or baked giant energy effects.
'''+ '\n'.join(f'{n+1}. {p}' for n,p in enumerate(poses))+'''
True transparent background. Render spacious production atlas at 2048px or larger.'''
 Path(q['destination']).with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
path.write_text(json.dumps(items,indent=2))
print('Fresh form-specific requests prepared: Baam and Mori, 16 sheets')
