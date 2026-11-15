"""Preserve actual comic-panel references separately from generated game art."""
from pathlib import Path
from PIL import Image
import subprocess,json,shutil
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/face-audit/comic-v3';O.mkdir(exist_ok=True)
downloads={
'zhuo-fan':('https://i.pinimg.com/originals/de/9a/b3/de9ab3ecc5c307bc2f0e7665d855838d.jpg','https://www.pinterest.com/pin/615445105365563757/'),
'zhuo-fan-face':('https://i.pinimg.com/originals/1f/20/a4/1f20a40ffe7cfdc90831bdf70062b4f4.jpg','https://www.pinterest.com/pin/653303489715044050/'),
'arthur':('https://i.pinimg.com/736x/38/d4/ed/38d4ed4717cbe4d927094ef060910f8f.jpg','https://br.pinterest.com/pin/699324648392057874/'),
'mok-gyeongwoon':('https://i.pinimg.com/originals/b3/ea/d7/b3ead7cbf7afdb3a138a932c70257a97.jpg','https://www.pinterest.com/pin/mok-gyeongwoon-jeong-chapter-48-myst-might-mayhem--221943087881653712/'),
'eugene':('https://i.pinimg.com/originals/08/03/1d/08031d6eee3a5f7ced5f3428fe3adc74.jpg','https://br.pinterest.com/pin/eugene-lionhart-damn-reincarnation--718887159283790993/'),
'jin-mu-won':('https://static.wikia.nocookie.net/vsbattles/images/4/48/Jinbetter.png/revision/latest?cb=20211026194831','https://vsbattles.fandom.com/wiki/Jin_Mu-Won_(Manhwa)')}
for slug,(url,page) in downloads.items():
 original=O/(slug+'.original');p=O/(slug+'.png')
 if not original.exists():subprocess.run(['curl.exe','-L','--fail','--silent','--show-error','--max-time','30',url,'-o',str(original)],check=True)
 Image.open(original).convert('RGB').save(p)
 (O/(slug+'.source.json')).write_text(json.dumps(dict(image_url=url,page=page,kind='Reposted comic panel; source chapter attribution retained where available; not a generated game image'),indent=2));print('PANEL',slug,flush=True)
locals={
'gang-ryong':'characters/gang-ryong/art/illustrated-v1/references/panel-reference.png',
'lloyd':'characters/lloyd/art/illustrated-v1/references/panel-reference.png',
'cha-yeon-woo':'face-audit/references/cha-yeon-woo-mask.png',
'kim-dokja':'face-audit/references/kim-dokja-white-coat.png',
'jin-mori':'face-audit/references/jin-mori-early.png',
'pyowol':'characters/pyowol/art/v3/references/face-three-quarter.jpg'}
for slug,src in locals.items():
 Image.open(R/'sprite-fighter'/src).convert('RGB').save(O/(slug+'.png'))
 (O/(slug+'.source.json')).write_text(json.dumps(dict(preserved_reference=src,kind='Previously downloaded comic panel; original source metadata retained alongside original file'),indent=2))
