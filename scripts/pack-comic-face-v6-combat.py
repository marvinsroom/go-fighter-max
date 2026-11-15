"""Pack generated complete cutouts, restoring the two omitted combat slots."""
from pathlib import Path
from PIL import Image
from isolated_sprite_atlas import extract
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];a=R/'sprite-fighter/characters/jin-mu-won/art/comic-face-v6';p=a/'combat.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=a/'combat.rejected-count14.png';assert not source.exists()
for ext in ('.png','.generation.json','.prompt.txt'):shutil.move(p.with_suffix(ext),a/('combat.rejected-count14'+ext))
missing=a/'combat-restored-two.png';shutil.copy2(sys.argv[1],missing)
q=json.loads((R/'.tmp/comic-face-v6-missing-request.json').read_text());q.update(tool='built-in image_gen.imagegen',original_generated_file=sys.argv[1],sha256=sha(missing));missing.with_suffix('.generation.json').write_text(json.dumps(q,indent=2));missing.with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
main=extract(source,2,7,count=14);two=extract(missing,2,1,count=2);before=R/'sprite-fighter/characters/jin-mu-won/art/identity-scale-v5';neutral=Image.open(before/'extracted/combat-00.png');factor=main[0][0].height/neutral.height
restored=[];registration=[]
for i,(im,bounds) in enumerate(two):
 old=Image.open(before/f'extracted/combat-{12+i:02}.png');scale=old.height*factor/im.height
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);restored.append(im);registration.append(dict(slot=12+i,uniform_scale=scale,reference=str((before/f'extracted/combat-{12+i:02}.png').relative_to(R)),method='Retain the existing corresponding pose size relative to the unchanged neutral body'))
tiles=[im for im,b in main[:12]]+restored+[im for im,b in main[12:]]
assert len(tiles)==16
cw=max(500,max(im.width for im in tiles)+100);ch=max(350,max(im.height for im in tiles)+100);board=Image.new('RGBA',(cw*2,ch*8))
for i,im in enumerate(tiles):board.alpha_composite(im,(i%2*cw+(cw-im.width)//2,i//2*ch+(ch-im.height)//2))
board.save(p);check=extract(p,2,8,count=16)
out=a/'extracted';out.mkdir(exist_ok=True)
for i,(im,b) in enumerate(check):im.save(out/f'combat-{i:02}.png')
parent=json.loads(source.with_suffix('.generation.json').read_text());parent.update(tool='built-in image_gen.imagegen drawings; deterministic atlas packing',sha256=sha(p),assembly=dict(note='The tall tool output omitted two poses. Fourteen complete generated cutouts plus two separately generated face-corrected cutouts are packed in original slot order. No new drawing was created by code.',sources=[dict(file=source.name,sha256=sha(source),count=14),dict(file=missing.name,sha256=sha(missing),count=2)],restored_pose_registration=registration),layout_validation=dict(status='PASS',count=16,bounds=[b for im,b in check]))
p.with_suffix('.generation.json').write_text(json.dumps(parent,indent=2));p.with_suffix('.prompt.txt').write_text(parent['prompt']+'\n\nTWO RESTORED POSES:\n'+q['prompt'],encoding='utf-8')
print('COMIC_FACE_COMBAT_PACKED',board.size,registration)
