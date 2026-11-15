"""Point existing review entry points to current stature evidence."""
from pathlib import Path
import json, os, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sprite-fighter/face-audit/identity-scale-v5'

def update(path):
    path = Path(path)
    if not path.exists() or not (OUT / 'profiles.json').exists():
        return
    page = path.read_text(encoding='utf-8')
    page = re.sub(r'<!-- stature-v5 -->.*?<!-- /stature-v5 -->', '', page, flags=re.S)
    url = os.path.relpath(OUT / 'review.html', path.parent).replace('\\', '/')
    fresh = path.parent.name in ('jin-mu-won', 'eugene')
    text = ('Move captures below include the new likeness and stature.' if fresh else
            'Earlier move captures below predate the stature correction; the comparison has current size captures.')
    banner = ('<!-- stature-v5 --><aside style="padding:16px;margin:16px;background:#24364a;color:#eef4ff;line-height:1.5">'
              '<a style="color:#b6d9ff" href="' + url + '">Current likenesses and all 26 fighter proportions</a>. ' + text + '</aside><!-- /stature-v5 -->')
    if path.name == 'style-v4-review.html':
        previews = ''
        for slug, label, reference in [('jin-mu-won', 'Jin Mu-Won', 'jin-mu-won-panel.jpg'), ('eugene', 'Older Eugene', 'eugene-adult-comic.jpg')]:
            art = ROOT / 'sprite-fighter/characters' / slug / 'art/comic-face-v6'
            if not (art / 'visual-review.json').exists():
                continue
            ref = os.path.relpath(OUT / 'references' / reference, path.parent).replace('\\', '/')
            portrait = os.path.relpath(art / 'portrait.png', path.parent).replace('\\', '/')
            previews += '<figure style="flex:1 1 400px;margin:10px"><figcaption>' + label + ': comic reference / revised face</figcaption><div style="display:flex"><img style="width:50%;height:300px;object-fit:contain" src="' + ref + '" alt="Original comic reference"><img style="width:50%;height:300px;object-fit:contain" src="' + portrait + '" alt="Revised comic face"></div></figure>'
        if previews:
            banner = banner.replace('</aside>', '<div style="display:flex;flex-wrap:wrap">' + previews + '</div></aside>')
    if re.search(r'<body[^>]*>', page, re.I):
        page = re.sub(r'(<body[^>]*>)', lambda m: m[0] + banner, page, count=1, flags=re.I)
    elif '<main>' in page:
        page = page.replace('<main>', '<main>' + banner, 1)
    else:
        page = page.replace('</style>', '</style>' + banner, 1)
    path.write_text(page, encoding='utf-8')

if __name__ == '__main__':
    state = json.loads((OUT / 'profiles.json').read_text())
    for row in state['fighters']:
        update(ROOT / 'sprite-fighter/characters' / row['slug'] / 'review.html')
    update(OUT.parent / 'style-v4-review.html')
