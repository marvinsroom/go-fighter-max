from comic_identity_v3 import *
import json
requests=[]
for slug,p in SPECS.items():
 if not all((REF/(n+'.png')).exists() for n in p['refs']):continue
 art=C/slug/'art/comic-identity-v3';art.mkdir(exist_ok=True)
 prompt='Use case: background-extraction. Extract the protagonist '+p['name']+' from the supplied ORIGINAL COMIC PANEL reference. Keep their actual published face, eye shapes, jaw, brows, nose, mouth, hairstyle and clothes AS DRAWN. Do not reinterpret or beautify the face into generic anime art. No new character design and no roster-style reference. '+p['identity']+' ONE SINGLE head-and-shoulders/upper-chest portrait, same expression and viewing angle as the main reference. Keep complete hair, entire head, neck and shoulders with generous margin. Remove background, speech bubbles, writing, other characters, battle gore and scenery. TRUE TRANSPARENT background. Preserve original comic linework and simple flat cel-shading. No glossy painted highlights or ornamental costume additions.'
 (art/'portrait.prompt.txt').write_text(prompt,encoding='utf-8');requests.append(dict(slug=slug,kind='portrait',prompt=prompt,references=[str(REF/(n+'.png')) for n in p['refs']],destination=str(art/'portrait.png')))
(R/'.tmp/comic-portrait-requests.json').write_text(json.dumps(requests,indent=2));print('COMIC_PORTRAITS',len(requests))
