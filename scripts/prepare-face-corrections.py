"""Keep exact prompts and immutable source copies for the manhwa face pass."""
from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parents[1]
specs={
 'gang-ryong':('sprite-fighter/characters/gang-ryong/art/illustrated-v1/references/panel-reference.png','Replace the stocky rounded boy with the lean serious Gang Yong design shown in reference2: slender athletic torso, trim waist, long limbs, narrower cheekbones and jaw, narrow focused dark eyes, long black ponytail and forward bangs. Gray long martial robe with dark crossed collar, black sash, gray trousers and black cloth shoes. No round belly, no chubby cheeks, no weapon. Match reference2 silhouette and face. Keep each original pose and its combat purpose.'),
 'cha-yeon-woo':('sprite-fighter/face-audit/references/cha-yeon-woo-mask.png','Correct ONLY the head/mask to the actual comic mask in reference2: ivory white slim angular face mask, clearly open black almond-shaped eye sockets with small amber eyes visible inside, sculpted angular nose bridge, tiny understated mouth line, pointed chin, short dark fringe. Keep mask ON in EVERY pose. No blank featureless plate, no skull teeth. Preserve all bodies, anatomy, black clothing, cloak, dagger, exact poses, composition, grid and framing.'),
 'kim-dokja':('sprite-fighter/face-audit/references/kim-dokja-white-coat.png','Correct ONLY the faces and hair to Kim Dokja in reference2: pale soft oval face, slender nose, straight naturally parted black hair with rounded falling fringe, open horizontal dark gray eyes, thin relaxed brows and restrained knowing expression. Avoid spiky hair or angry generic hero face. Preserve all bodies, white coats, black shirts, sword, exact poses, composition, grid and framing.')}
requests=[]
for slug,(ref,change) in specs.items():
 a=R/'sprite-fighter/characters'/slug/'art';old=a/'illustrated-v1';new=a/'manhwa-faces-v2';new.mkdir(exist_ok=True)
 backup=a/'before-manhwa-faces-v2';backup.mkdir(exist_ok=True)
 for kind in ('movement','combat','story','portrait'):
  for suffix in ('.png','.prompt.txt'):
   src=old/(kind+suffix);dst=backup/src.name
   if src.exists() and not dst.exists():shutil.copy2(src,dst)
  prompt='Use case: precise-object-edit. Input1 is the EDIT TARGET production fighting game asset. Input2 is the original comic identity reference, NOT a style change. '+change+' Preserve detailed cel-shaded roster rendering. True transparent background. '
  prompt+=('ONE waist-up selection portrait, complete head and shoulders, same framing.' if kind=='portrait' else 'EXACTLY sixteen isolated FULL BODY drawings in the SAME strict 4 columns by 4 rows and same row-major pose order as input1. Generous empty gutters and outer margins. Every hair tip, cloak, hand, weapon and both feet must remain inside its own cell. No overlap, no cropped anatomy, no text, no scenery. Keep all sixteen different poses.')
  (new/(kind+'.prompt.txt')).write_text(prompt,encoding='utf-8')
  requests.append(dict(slug=slug,kind=kind,prompt=prompt,references=[str(old/(kind+'.png')),str(R/ref)],destination=str(new/(kind+'.png'))))
(R/'.tmp/face-generation-requests.json').write_text(json.dumps(requests,indent=2))
print('Prepared',len(requests),'non-destructive edits')
