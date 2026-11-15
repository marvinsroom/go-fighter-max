"""Use comic-only visual inputs and explicit native pose semantics for shared fighters."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
import json,sys

movement=['relaxed standing guard, weapon lowered forward, free palm relaxed','same standing guard, slight breathing change','walking forward screen-right, leading foot extended','opposite walking stride screen-right','low crouching guard, free hand near ground','jumping forward, knees bent and weapon trailing','ascending jump, knees tucked','descending jump, weapon above head','standing block, weapon or forearms diagonal across chest','crouching block, weapon or forearms shielding head','struck in torso, leaning back','struck low, torso folded, hand clutching side','airborne knockback, back arched and boots pointing right','lying face-down defeated, weapon beside body','kneeling recovery, braced free hand','standing ready with character-specific knowing/determined expression']
combat=['standing attack-ready','standing attack windup, weapon/striking hand drawn back','full standing slash/palm strike extended screen-right','standing follow-through recovery','crouching low attack windup','low sweeping attack extended screen-right','deep forward lunge, weapon/striking arm extended right','airborne slash/palm strike with knees bent','two-handed overhead or both-arms-raised heavy windup','heavy overhead downward strike, deeply bent knees','offhand casting/energy-release gesture extended right, weapon lowered','airborne forward attack, knees bent','airborne overhead windup','airborne downward follow-through','low landing, free hand near ground','standing attack recovery into guard']
story=['relaxed standing guard','checking hands or adjusting grip','open free palm in a calm self-assured introduction','lower combat guard','standing composed and focused','crouched dash preparation, hand low','offhand forward energy-casting gesture','deep forward weapon thrust/hand strike','weapon or both hands raised overhead','powerful downward/forward finish','low crouch with free hand near ground','standing recovery','personality gesture beginning','personality gesture held','personality gesture ending','returning to ordinary guard']
personality={
'kim-dokja':['opening a small worn black book in free hand, sword lowered','reading the open book with a small knowing smile','shutting the book, calm thoughtful eyes'],
'arthur':['looking at exactly one tiny black Sylvie perched on shoulder','gently petting the one tiny black Sylvie on shoulder','smiling briefly toward Sylvie before returning to sword guard'],
'cha-yeon-woo':['holding a small gold pocket watch in left hand, mask remains on','studying the open pocket watch, masked head tilted down','closing the pocket watch, dagger ready'],
'eugene':['resting sword on shoulder, reflective eyes','eyes closed in memory, sword resting on shoulder','opening eyes with a small determined grin'],
'lloyd':['shovel resting on shoulder, suspicious squint','absurdly broad crooked scheming grin, huge comic expression','a smug toothy lopsided grin, shovel on shoulder'],
'jin-mu-won':['sword lowered while quietly considering the blade','quietly wiping or inspecting blade, restrained closed mouth','resheathing or lowering sword with calm resolve'],
'gang-ryong':['holding a small plain steamed bun near face','taking a bite from the bun, round comic eyes','finishing the bun with a satisfied wide comic smile'],
'mok-gyeongwoon':['tilting head with an unsettling small smile','a calm slightly open unsettling smile, half-lidded eyes','relaxing back into poised sword guard'],
'zhuo-fan':['raising bare free hand, calculating asymmetric smirk','looking down at bare palm with a knowing smirk','lowering hand, robe and red lapels unchanged']}
path=R/'.tmp/comic-style-v4-requests.json';items=json.loads(path.read_text())
for q in items:
 if q['slug'] not in PROFILES or (len(sys.argv)>1 and q['slug'] not in sys.argv[1:]):continue
 slug=q['slug'];spec=SPECS[slug]
 # Retain the specifically reviewed first movement prompt for Dokja.
 if slug=='kim-dokja' and q['kind']=='movement':continue
 poses=list(dict(movement=movement,combat=combat,story=story)[q['kind']])
 if q['kind']=='story':poses[12:15]=personality[slug]
 if q['kind']=='combat' and q['count']==14:poses=poses[:12]+poses[14:]
 if slug in ('gang-ryong','zhuo-fan'):weapon='BARE HANDS, open palms and fists, no sword or weapon; use the hand-strike alternative wherever poses mention a weapon or sword'
 elif slug=='lloyd':weapon='long plain steel-headed SHOVEL, held with both hands in attack poses'
 elif slug=='cha-yeon-woo':weapon='compact steel DAGGER, mask stays on in every pose'
 else:weapon='slender dark or steel sword as appropriate to the original comic'
 refnames=spec['refs']
 q['references']=[str(REF/(n+'.png')) for n in refnames]
 q['prompt']=f'''New character animation atlas: {spec['name']}, {q['kind']}. Use the supplied original comic panel(s) as the ONLY authority for character appearance and drawing language. Draw a fresh set of game poses rather than a polished promotional illustration.
IDENTITY: {spec['identity']}
WEAPON: {weapon}.
ART: economical comic ink drawing, simple bold flat color shapes. ONE broad HARD shadow tone per material. Skin base and one shadow only. Hair a single clear dark/color mass with at most one broad highlight, not finely rendered strands. Cloth folds reduced to at most three purposeful ink strokes per limb. No airbrush, gradients, texture, shiny leather, dense wrinkles, ornamental redesign, idealised model anatomy or generic anime beautification. Copy the original's particular eye openings, brow spacing, cheek/jaw contour and mouth proportions. Keep face visible, individual expressions action-appropriate and readable at game size. Preserve each comic's different age, head proportions and personality.
STRICT {q['columns']} columns by {q['rows']} rows, EXACTLY {q['count']} separate complete full-body figures, row-major order below. All active poses face screen-right in three-quarter view. Each complete head, weapon, coat, both feet and any prop entirely inside its own cell, with broad empty transparent gutters and outer margins. No touching, no cropped parts, no labels, no extra portraits, no scenic background or attack effects. Pose list:
'''+ '\n'.join(f'{i+1}. {pose}' for i,pose in enumerate(poses))+f'''
One consistent {spec['name']} across every pose. Use human comic proportions rather than chibi. Render a spacious atlas at 2048 pixels or larger. TRUE TRANSPARENT background.'''
 Path(q['destination']).with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
path.write_text(json.dumps(items,indent=2))
print('Comic-only shared fighter prompts prepared')
