"""Register completion only after current native and browser evidence passes."""
from pathlib import Path
import hashlib, json
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';O=S/'face-audit/identity-scale-v5'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=read(O/'completion.json');native=read(O/'native-validation.json');browser=read(O/'browser-validation.json')
revision='comic-face-v6' if all((S/'characters'/slug/'art/comic-face-v6/visual-review.json').exists() for slug in ('jin-mu-won','eugene')) else 'identity-scale-v5'
assert report['status']==native['status']=='Complete' and len(report['fighters'])==len(native['fighters'])==26
assert report['total_current_native_checks']==native['checks']
assert browser['status']=='PASS' and browser['review_sha256']==sha(O/'review.html')
full=[]
for slug in ('jin-mu-won','eugene'):
 f=S/'characters'/slug;proof=read(f/'runtime-validation.json');row=next(x for x in report['fighters'] if x['slug']==slug)
 assert proof['status']=='Complete' and proof['failed']==0 and proof['passed']==66 and proof['runtime_sha256']==row['runtime_sha256']
 for name in ('viewer-validation.json','comic-viewer-validation.json'):
  v=read(f/name);assert v['status']=='PASS' and v['review_sha256']==sha(f/'review.html')
 full.append(dict(slug=slug,checks=proof['passed'],captures=len(proof['frames']),proof=str((f/'runtime-validation.json').relative_to(S))))
state=read(O/'profiles.json');state['status']='Complete';state['visual_review']='Current shared-scale roster lineup, corrected portraits and full sheets, both corrected native ultimates, and additional shadow/Choco contacts inspected.'
(O/'profiles.json').write_text(json.dumps(state,indent=2))
report.update(likeness_revision=revision,full_move_suites=full,browser_validation='browser-validation.json',review='review.html',visual_review=state['visual_review'])
(O/'completion.json').write_text(json.dumps(report,indent=2))
(O.parent/'completion.json').write_text(json.dumps(dict(status='Complete',revision=revision,scope='All 26 playable fighters, with existing forms; original comic faces for Jin Mu-Won and older silver-haired Eugene',report='identity-scale-v5/completion.json',review='identity-scale-v5/review.html',current_native_checks=native['checks'],full_move_suites=full,historical_artwork_report='identity-scale-v5/archive/completion-before-v5.json'),indent=2))
readme=S/'README.md';text=readme.read_text(encoding='utf-8');intro='The [current likeness and stature review](face-audit/identity-scale-v5/review.html) shows all 26 playable fighters at a shared world scale, with height sources and clearly labelled estimates. Jin Mu-Won has a revised adult face based on stronger comic references; Eugene uses his older silver-haired design. Current size, form and attack-contact checks passed for every fighter; both new likenesses also passed fresh full move suites. Artwork, exact prompts and generation provenance are linked in the review.\n\n'
if not text.startswith(intro):readme.write_text(intro+text,encoding='utf-8')
memory=R/'PROJECT_MEMORY.md'
with memory.open('ab') as stream:stream.write(('\n\n## Identity and stature v5 COMPLETE (2026-10-21)\nUser confirmed older silver-haired Eugene and EVERY playable fighter. Both new likenesses installed and visually inspected; exact prompts/provenance retained. All 26 production fighters now use proportional native sizes, with estimates explicitly labelled and prior files archived. '+str(native['checks'])+' current native checks passed, including both facings, real attack contact, all existing human/form banks, Jinwoo shadows and Vikir Choco. Jin Mu-Won and Eugene each passed 66 fresh gameplay checks plus presentation and startup; '+str(sum(x['captures'] for x in full))+' fresh move captures total. Both review players pass browser QA, and current roster comparison passes desktop/narrow viewport QA. Current entry: sprite-fighter/face-audit/identity-scale-v5/review.html. Existing style-v4 and per-fighter reviews link here; other older full move captures explicitly labelled pre-stature. Audit confirms controller logic/action timing preserved, with only requested size/collision geometry and two likeness SFF replacements. completion.json is current v5 evidence, previous v4 report archived. No further work pending for this request.\n').encode('utf-8'))
print('IDENTITY_SCALE_V5_COMPLETE',native['checks'],'native checks',full)
if revision=='comic-face-v6':
 intro='The current comic-face correction is installed for **both Jin Mu-Won and older silver-haired Eugene**, in their portraits and every body sheet. Compare the original comic panels with the revised faces at the top of [the artwork review](face-audit/style-v4-review.html), or open the [full current roster review](face-audit/identity-scale-v5/review.html). Exact built-in generation prompts and source records are linked there.\n\n'
 text=readme.read_text(encoding='utf-8')
 if not text.startswith(intro):readme.write_text(intro+text,encoding='utf-8')
 with memory.open('ab') as stream:stream.write(('\n\n## Comic face v6 COMPLETE (2026-10-21)\nSupersedes the v6 in-progress note. User confirmed BOTH Jin Mu-Won and Eugene. Replaced portraits and all six body sheets using original comic facial geometry; final eight files inspected and installed. Exact prompts and generated sources retained at characters/{jin-mu-won,eugene}/art/comic-face-v6. Two missing Jin combat poses restored with separately generated face-corrected drawings, then atlas packed in original slots with documented uniform registration; story spacing and portrait margins repaired. New full native gameplay suites (66 each), presentation/startup, browser players and current native size/contact samples passed; all26 current roster registrations still pass. V5 stature retained and earlier work archived. Active style-v4-review.html now shows original comic references beside the new portraits at its top. Global completion revision comic-face-v6. No requested work pending.\n').encode('utf-8'))
 print('COMIC_FACE_V6_COMPLETE')
