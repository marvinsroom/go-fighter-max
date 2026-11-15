"""Save official identity references and exact built-in generation prompts."""
from manhwa_expansion import BATCH
from pathlib import Path
from html import unescape
from urllib.parse import quote
import subprocess,re,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
for slug,p in BATCH.items():
    if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
    art=ROOT/'sprite-fighter/characters'/slug/'art/illustrated-v1';refs=art/'references';refs.mkdir(parents=True,exist_ok=True)
    page=refs/'official-page.html'
    if not page.exists():subprocess.run(['curl.exe','-L','--fail','--silent','--show-error',p['source'],'-o',str(page)],check=True)
    raw=page.read_text(encoding='utf-8');tags=re.findall(r'<meta\b[^>]+>',raw)
    tag=next(t for t in tags if re.search(r'(?:property|name)=["\']og:image["\']',t))
    url=quote(unescape(re.search(r'content=["\']([^"\']+)',tag)[1]),safe=':/?=&%')
    original=refs/'official-cover-original.img'
    if not original.exists():subprocess.run(['curl.exe','-L','--fail','--silent','--show-error',url,'-o',str(original)],check=True)
    im=Image.open(original).convert('RGB');im.save(refs/'official-cover.png')
    (refs/'sources.json').write_text(json.dumps(dict(official_series=p['source'],cover_url=url,credits=p['credits'],purpose='Identity and outfit reference; original retained, not runtime sprite.'),indent=2))
    (refs/'import-search.json').write_text(json.dumps(dict(status='No usable verifiable downloadable release found',date='2026-10-20',queries=[f'{p["name"]} MUGEN download',f'{p["series"]} MUGEN character',f'{p["name"]} JUS IKEMEN',f'site:mugenarchive.com {p["name"]}',f'site:mugenfreeforall.com {p["name"]}'],decision='Custom fan adaptation using local authored combat foundation; no upstream import claimed.'),indent=2))
    common='Use case: stylized-concept. Production hand-painted anime fighting-game sprite atlas. Reference1 supplies character identity and outfit ONLY. Reference2 supplies roster style ONLY: crisp clean linework, detailed cel shading, sculpted cloth and consistent anatomy. '+p['identity']+' True transparent background, no scenery, no text, no labels. '
    grid='EXACTLY16 isolated FULL BODY drawings in STRICT4columns4rows, HUGE clear gutters and outer margins. Every hair tip, weapon, cloak and BOTH feet wholly inside its own cell. Same character, clothing, head size and anatomy throughout. Right-facing three-quarter view. NO baked giant VFX. Row-major order: '
    movement=['relaxed standing combat guard','second breathing guard','walking left foot leading','walking right foot leading','low crouching guard','fast forward run','rising jump','airborne attack preparation','standing block','crouching block','chest recoil hurt','shoulder recoil hurt','airborne falling backwards hurt','lying defeated on side','rising on one knee','FULL BODY calm victory']
    combat=['standing weapon-ready guard','light attack windup','light forward strike contact','light attack followthrough','low sweeping strike','forward lunge windup','long forward lunge contact','rising strike','heavy overhead attack preparation','heavy downward strike contact','off-hand forward casting thrust','defensive counter guard','jumping diagonal strike','explosive counterattack contact','crouching low strike','settled attack recovery guard']
    story=['walking into fight','checking weapon or wrapping hands','confident pre-fight gesture','settling into combat guard','full-body neutral cinematic guard','ultimate anticipation crouch','ultimate open-hand focus forward','ultimate wide sweeping strike','ultimate weapon or palm raised skyward','ultimate strongest low forward strike','ultimate recoil and settle','ultimate calm aftermath guard']+[p['personality'].split(',')[min(i,len(p['personality'].split(','))-1)].strip() for i in range(4)]
    requests=[]
    for name,poses in [('movement',movement),('combat',combat),('story',story)]:
        prompt=common+grid+'; '.join(f'{i} {pose}' for i,pose in enumerate(poses))+'. Combat language: '+p['weapon']+'.'
        (art/(name+'.prompt.txt')).write_text(prompt,encoding='utf-8');requests.append(dict(file=name+'.png',prompt=name+'.prompt.txt',tool='built-in image_gen.imagegen',transparent_background=True,reference_images=['references/official-cover.png','../../../vikir/art/v3/movement.png']))
    prompt='Use case: stylized-concept. Production anime fighting-game VFX atlas. EXACTLY16 separate motifs in STRICT4columns4rows, TRUE TRANSPARENT BACKGROUND, enormous gutters, centered in own cell with thick enough opaque core for extraction. No text, labels, scenery or extra objects. All motifs fully inside cell, no overlap. Theme '+p['name']+': '+p['palette']+'. Row-major: '+'; '.join(str(i)+' '+v for i,v in enumerate(p['motifs']))+'.'
    (art/'effects.prompt.txt').write_text(prompt,encoding='utf-8');requests.append(dict(file='effects.png',prompt='effects.prompt.txt',tool='built-in image_gen.imagegen',transparent_background=True,reference_images=[]))
    prompt=common+'ONE SINGLE waist-up character selection portrait, centered complete head and shoulders, looking towards viewer with signature expression, weapon visible at side. No duplicate bodies, no panels, no text. Detailed polished illustration, clean silhouette, true transparent background.'
    (art/'portrait.prompt.txt').write_text(prompt,encoding='utf-8');requests.append(dict(file='portrait.png',prompt='portrait.prompt.txt',tool='built-in image_gen.imagegen',transparent_background=True,reference_images=['references/official-cover.png','../../../vikir/art/v3/movement.png']))
    (art/'generation-requests.json').write_text(json.dumps(requests,indent=2))
    print('PREPARED',slug,im.size)
