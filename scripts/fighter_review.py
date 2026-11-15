"""Shared local review shell for the illustrated fighter roster."""
from pathlib import Path
import hashlib,html,json,re

ROOT=Path(__file__).resolve().parents[1]
TEMPLATES=ROOT/'scripts/templates'
CHARACTERS=ROOT/'sprite-fighter/characters'
NAMES={'rimuru':'Rimuru Tempest','cid':'Cid Kagenou','jinwoo':'Sung Jinwoo','pyowol':'Pyo Wol','edward':'Edward Elric','vikir':'Vikir van Baskerville','jin-mori':'Jin Mori','baam':'Baam','jin-mu-won':'Jin Mu-Won','lloyd':'Lloyd Frontera'}
INTROS={
 'jin-mu-won':'Snow Flower swordplay, confirmed attack chains, Northern Sect techniques and the Ten Thousand Shadows cinematic.',
 'lloyd':'Shovel combat, construction techniques, the Nightmare Grin and a giant hamster Grand Excavation finisher.',
 'baam':'The Twenty-Fifth Baam: Shinsu palms, connected attack chains, reactive counters, Jue Viole Grace and the Endless Sky Shinsu cinematic.',
 'jin-mori':'Jin Mori and a persistent Monkey King form. A goggles-adjusting entrance, buffered taekwondo chains, dragon supers and a readable three-stage staff ultimate.',
 'vikir':'Hunter, Night Hound, Choco and the Colosseo academy uniform. Three sword supers, the cinematic Crimson Execution ultimate, four guest assists and animated Academy Anubis archery.',
 'edward':'Illustrated Fullmetal Alchemist: automail strikes, transmuted weapons and stone constructs, EX attacks, four supers and the Elric brothers team finisher.',
 'pyowol':'Thread assassin: fine silk, hidden daggers, evasive steps, three supers and a quiet execution ultimate.',
 'rimuru':'Three playable forms with independent movesets: masked human, Demon Lord and slime. Each form has three supers and its own ultimate.',
 'cid':'Illustrated Shadow combat, Alpha and Beta summon supers, three Atomic branches and the Seven Shadows team ultimate.',
 'jinwoo':'Daggers, the Demon King’s Longsword and four playable shadows. Preview the shadow-exchange intro, six supers and form-specific ultimates.'}

from manhwa_expansion import BATCH
for _slug,_profile in BATCH.items():
    if (CHARACTERS/_slug/'review.html').exists():
        NAMES[_slug]=_profile['name'];INTROS[_slug]=_profile['description']

def read_data(slug):
    raw=(CHARACTERS/slug/'review-data.js').read_text(encoding='utf-8')
    return json.loads(re.sub(r'^window\.\w+\s*=\s*','',raw).strip().removesuffix(';'))

def content_from_page(page):
    content=re.search(r'<main\b[^>]*>(.*?)</main>',page,re.S)[1]
    content=re.sub(r'^.*?(?=<section\b|<div class="weapons")','',content,flags=re.S)
    content=re.sub(r'<section\b[^>]*>.*?</section>',lambda m:'' if 'id="capture"' in m[0] else m[0],content,flags=re.S)
    return content

def write_review(slug,page=None,data=None):
    folder=CHARACTERS/slug;data=data or read_data(slug)
    content=content_from_page(page) if page else (TEMPLATES/f'{slug}-review-content.html').read_text(encoding='utf-8')
    if page:(TEMPLATES/f'{slug}-review-content.html').write_text(content,encoding='utf-8')
    # Controls always follow the capture player, with character details below.
    controls=[]
    def take_controls(m):
        if re.search(r'<h2[^>]*>(?:What to press|Controls(?: and movesets)?)</h2>',m[0]):
            controls.append(re.sub(r'<h2[^>]*>.*?</h2>','<h2 id="controls">Controls</h2>',m[0],count=1,flags=re.S));return ''
        return m[0]
    content=re.sub(r'<section\b[^>]*>.*?</section>',take_controls,content,flags=re.S)
    # Tables scroll within the section instead of widening the whole page.
    content=re.sub(r'(<table\b.*?</table>)',r'<div class="table-wrap">\1</div>',content,flags=re.S)
    groups=data['groups']
    if slug=='rimuru':
        groups={'Ultimates':groups.get('Form ultimates',groups.get('Ultimates',[])),
                'Supers':groups.get('Form supers',groups.get('Supers',[])),
                **{k:v for k,v in groups.items() if k not in ('Form ultimates','Form supers','Ultimates','Supers')}}
    elif slug=='cid':
        groups={'Ultimates':groups.get('Team ultimate',[])+groups.get('Atomics',[]),
                'Supers':groups.get('Summon supers',[]),
                **{k:v for k,v in groups.items() if k not in ('Team ultimate','Atomics','Summon supers')}}
    elif slug=='jinwoo':
        shadow_ults=[n for n in groups['Shadows'] if 'ultimate' in n.lower()]
        groups=dict(groups,Ultimates=groups['Ultimates']+shadow_ults,Shadows=[n for n in groups['Shadows'] if n not in shadow_ults])
        groups={k:groups[k] for k in ('Ultimates','Supers',*groups) if k in groups}
    data=dict(data,groups={k:v for k,v in groups.items() if v},slug=slug,name=NAMES[slug])
    assert set(data['cases'])=={n for rows in data['groups'].values() for n in rows}
    data['shortcuts']=[dict(category='Ultimates',clip=n) for n in data['groups'].get('Ultimates',[]) if not any(word in n.lower() for word in ('blocked','miss','insufficient','empty meter','corner','interrupted'))]
    if slug=='jin-mori':
        for group,names in [('Entrance and forms',('Entrance','Transform into Monkey King','Return to Jin Mori')),('Combos',('Z Z Z chain','X X X chain','Z X C chain'))]:
            data['shortcuts'] += [dict(category=group,clip=n) for n in names if n in data['groups'].get(group,[])]
    if slug=='baam':
        data['shortcuts']=[s for s in data['shortcuts'] if 'wall' not in s['clip'] and 'Light into' not in s['clip']]
        for group,names in [('Entrance and forms',('Entrance','Transform into Viole','Return to base')),('Combos',('Base / Z Z Z','Base / X X X','Base / Z X C'))]:
            data['shortcuts'] += [dict(category=group,clip=n) for n in names if n in data['groups'].get(group,[])]
    if slug in ('jin-mu-won','lloyd') or slug in BATCH:
        data['shortcuts']=[s for s in data['shortcuts'] if 'wall' not in s['clip'] and 'Light into' not in s['clip']]
        personality=BATCH[slug]['taunt'] if slug in BATCH else 'Quiet Resolve' if slug=='jin-mu-won' else 'Nightmare Grin'
        for group,names in [('Entrance and personality',('Entrance',personality)),('Combos',('Z Z Z','X X X','Z X C'))]:
            data['shortcuts'] += [dict(category=group,clip=n) for n in names if n in data['groups'].get(group,[])]
    data['sheets']=[]
    if slug=='cid':
        for name,src in [('Movement A','illustrated-v1/movement-a'),('Movement B','illustrated-v1/movement-b'),('Combat','illustrated-v1/combat'),('Atomic','illustrated-v1/cinematic'),('Taunt','taunt-v1/taunt'),('Alpha','summons-v1/alpha'),('Beta','summons-v1/beta'),('Gamma / Delta / Epsilon','garden-ultimate-v1/gamma-delta-epsilon'),('Zeta / Eta','garden-ultimate-v1/zeta-eta')]:
            data['sheets'].append(dict(name=name,src='art/'+src+'.png'))
    status=[f"{data['passed']} native combat checks passed"]
    if slug=='cid':status += [f"{data['summonPassed']} summon checks",f"{data['gardenPassed']} team-ultimate checks"]
    if slug=='jinwoo':status += [f"{data['introPassed']} intro checks"]
    data['status']=' · '.join(status)+'. Frames play at recorded tick intervals.'
    # Keep the legacy data global for existing tooling; the player consumes one
    # common schema embedded together with the page, avoiding data-cache drift.
    payload=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    css=re.search(r'<style>(.*?)</style>',(TEMPLATES/'cid-review.html').read_text(encoding='utf-8'),re.S)[1]
    css+='\n'+(TEMPLATES/'fighter-review.css').read_text(encoding='utf-8')
    script=(TEMPLATES/'fighter-review.js').read_text(encoding='utf-8')
    revision=hashlib.sha256((payload+css+script+content+''.join(controls)).encode()).hexdigest()[:12]
    data['pageRevision']=revision
    payload=json.dumps(data,ensure_ascii=False).replace('</','<\\/')
    nav=''.join(f'<a href="../{other}/review.html"'+(' aria-current="page"' if other==slug else '')+'>'+name+'</a>' for other,name in NAMES.items())
    if slug=='cid':
        audit='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cid - Proportion audit</title><style>'+css+'</style><main><nav class="character-nav" aria-label="Character reviews">'+nav+'</nav><h1>Cid proportions</h1><p><a href="review.html">Back to combat review</a></p>'
        for title,src in [('Illustrated poses','proportions-v6.jpg'),('Native proportions','native-proportions-v6.jpg'),('Walking','walking-review-v4.jpg'),('Seven Shadows ultimate','garden-native-review.jpg')]:
            assert (folder/src).exists(),src
            audit+=f'<section><h2>{title}</h2><a href="{src}"><img class="atlas" src="{src}" alt="Cid {title.lower()}"></a></section>'
        (folder/'proportion-audit.html').write_text(audit+'</main></html>',encoding='utf-8')
    links='<a href="proportion-audit.html">Proportion audit</a> · <a href="README.md">Build notes</a>'
    if (folder/'art/comic-identity-v3/portrait.png').exists():
        links+=' | <a href="art/comic-identity-v3/design-review.html">Current comic redraws and prompts</a> | <a href="../../face-audit/review.html">Comic comparisons</a>'
    if slug=='jin-mori':links+=' · <a href="art/awakening-v3/design-review.html">Awakening artwork</a>'
    if slug=='baam':links+=' | <a href="art/combat-v3/design-review.html">Combat artwork and prompts</a> | <a href="art/canonical-v2/design-review.html">Character designs</a>'
    if slug in ('jin-mu-won','lloyd') or slug in BATCH:links+=' | <a href="art/illustrated-v1/design-review.html">Artwork and prompts</a>'
    validation='validation/current.json' if slug=='jinwoo' else 'runtime-validation.json'
    links+=f' · <a href="{validation}">Native validation</a>'
    page=(TEMPLATES/'fighter-review.html').read_text(encoding='utf-8')
    replacements={'NAME':html.escape(NAMES[slug]),'INTRO':html.escape(INTROS[slug]),'CSS':css,'NAV':nav,'REVISION':revision,'LINKS':links,'CONTENT':''.join(controls)+content,'DATA':f'window.FIGHTER_REVIEW=window.{slug.upper().replace("-","_")}_REVIEW={payload};','SCRIPT':script}
    page=re.sub(r'@@(\w+)@@',lambda m:replacements[m[1]],page)
    if slug=='jin-mori':page=page.replace('aria-label="Ultimate previews"','aria-label="Move previews"').replace('Choose an ultimate below, or browse supers, movement and other recorded moves.','Use the quick previews for the entrance, transformation, combos and staff ultimate, or choose a category below.')
    if slug=='baam':page=page.replace('aria-label="Ultimate previews"','aria-label="Move previews"').replace('Choose an ultimate below, or browse supers, movement and other recorded moves.','Preview Shinwonryu, Jue Viole Grace, the entrance and combo chains, or browse the move categories.')
    if slug in ('jin-mu-won','lloyd') or slug in BATCH:page=page.replace('aria-label="Ultimate previews"','aria-label="Move previews"').replace('Choose an ultimate below, or browse supers, movement and other recorded moves.','Preview the ultimate, entrance, personality action and combo chains, or browse all recorded moves.')
    for target in re.findall(r'(?:src|href)="([^"]+)"',page):
        if not target.startswith(('http','#','data:')):
            local=(folder/target.split('?')[0]).resolve()
            assert local==(folder/'review.html').resolve() or local.exists(),(slug,target)
    (folder/'review.html').write_text(page,encoding='utf-8')
    from stature_review_banner import update as update_stature_banner
    update_stature_banner(folder/'review.html')
    if slug=='rimuru':
        for alias in ('review-forms-v3.html','review-forms-v4.html'):(folder/alias).write_text(page,encoding='utf-8')
    print('SHARED_REVIEW',slug,len(data['cases']),'clips',revision)

if __name__=='__main__':
    for slug in NAMES:write_review(slug)
