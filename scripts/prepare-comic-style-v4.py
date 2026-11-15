"""Checkpoint the visual correction independently of the installed v3 build."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
import json, shutil

prior = json.loads((R/'.tmp/comic-body-requests.json').read_text()) + json.loads((R/'.tmp/comic-legacy-requests.json').read_text())
requests = []
for q in prior:
    slug, kind = q['slug'], q['kind']
    spec = SPECS[slug]
    current = C/slug/'art/comic-identity-v3'
    output = C/slug/'art/comic-style-v4'
    output.mkdir(exist_ok=True)
    count = q.get('count', q['columns']*q['rows'])
    refs = [str(REF/(name+'.png')) for name in spec['refs']]
    if slug == 'baam': refs.append(str(REF/'viole.png'))
    refs.append(str(current/(kind+'.png')))
    forms = {
      'baam': 'Keep EACH CELL in its existing form: short-haired Baam keeps red waistcoat and simple youthful oval eyes; long-haired Viole keeps black high collar, FUG circles and long black fringe hiding the eyes. Reference 2 is Viole only. Never exchange costumes or head silhouettes between cells.',
      'jin-mori': 'Keep EACH CELL in its existing form: base Mori has olive-green goggles; Monkey King has a GOLD circlet, tiger pelt and staff, NEVER green goggles. Keep transformation intermediates gradual, with existing individual expressions.',
      'vikir': 'Preserve EACH CELL costume and head covering exactly. Night Hound cells keep their entire hood and long black beaked MASK; no exposed face or red eyes through the mask. Academy and Hunter exposed faces follow the comic. Never exchange these forms.',
      'jinwoo': 'Keep adult proportions, current dagger/greatsword choices and each existing shadow form. Clothing and pose stay per cell.',
      'pyowol': 'Keep the delicate androgynous comic face, long white hair and existing white snake placement. Do not turn him into a rugged male swordsman.'
    }.get(slug, '')
    prompt = f'''Use case: style-transfer and identity-preserve.
Asset: production full-body fighting-game animation atlas for {spec['name']}.
The FIRST image(s) are original comic identity and drawing-language references. The LAST image is the existing atlas to REDRAW, used ONLY for exact pose, facing, costume/form, weapon, anatomy placement and cell order. Its dense rendering and generic small faces are rejected.
Replace every body drawing with economical COMIC INKS and a visibly simpler cel-animation treatment. Preserve {spec['name']}'s particular face from the comic, including eye opening, brow angle, nose length, cheek and jaw width; do not substitute a standard handsome anime face. {spec['identity']}
{forms}
RENDERING RULES: opaque flat fills, crisp dark ink contour, ONE hard-edged shadow color per material. Skin: base plus one shadow. Hair: one large dark/colored shape plus at most one broad highlight shape; no individual glossy strands. Cloth: base plus one broad shadow shape; simplify folds to a few purposeful ink strokes at joints. Delete dense wrinkle webs, leather shine, reflective edging, airbrush and ornamental surface texture. Keep character-specific color blocks. Faces must remain visible and readable, with the reference's eyes and brows, even at gameplay scale. Keep individual expressions and pose gestures rather than stamping the same face. Ordinary human anatomy and comic proportions, not a beautified figurine. Render at 2048px or larger so ink and facial features survive extraction.
STRICT LAYOUT: {q['columns']} columns x {q['rows']} rows, EXACTLY {count} separate COMPLETE head-to-toe drawings in the SAME row-major order as the last image. Preserve the exact pose and number of actors in each cell, including held props. Last row may be partial. Keep at least 30px of empty transparent space between every drawing and the cell edges. Both feet, every hair/robe tip, weapon and companion entirely inside their own cells. Shrink each whole pose if necessary. No extras, alternate portraits, closeups, labels, text, panels, scenery or baked attack trails. TRUE TRANSPARENT background. Priority: recognisable comic face and simple flat inked artwork, exact pose order, clear separated complete silhouettes.'''
    if slug == 'arthur' and kind == 'story':
        prompt += '\nPreserve exactly one tiny black Sylvie on the shoulder in existing story pose13; do not add Sylvie to other cells.'
    item = dict(slug=slug, kind=kind, columns=q['columns'], rows=q['rows'], count=count, prompt=prompt, references=refs, destination=str(output/(kind+'.png')), current=str(current/(kind+'.png')))
    (output/(kind+'.prompt.txt')).write_text(prompt, encoding='utf-8')
    requests.append(item)

audit = dict(revision='comic-style-v4', status='in progress', scope='14-fighter body artwork; preserve stronger comic-led portraits', requirements=['Visual comparison to original comic', 'One shadow tone per material', 'Readable individual faces', 'Preserve form masks/headwear/costumes', 'Complete separated poses', 'Fresh installed runtime and browser validation'], fighters={slug:dict(status='pending', sheets=sum(q['slug']==slug for q in requests)) for slug in SPECS})
path=REF/'style-v4-progress.json'
if not path.exists(): path.write_text(json.dumps(audit,indent=2))
(R/'.tmp/comic-style-v4-requests.json').write_text(json.dumps(requests,indent=2))
print('Prepared',len(requests),'body sheets across',len(SPECS),'fighters')
