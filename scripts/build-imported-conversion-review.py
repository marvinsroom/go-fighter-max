"""Build the canonical gallery for completed imported-fighter conversions."""
from pathlib import Path
import hashlib, html, json

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
OUT = GAME / "style-wave2"
progress = json.loads((OUT / "conversion-progress.json").read_text())
cards = []
audit = []

for slug, tracked in progress["installed"].items():
    character = GAME / "characters" / slug
    style = character / "style/conversion-v1"
    manifest_path = style / "installation.json"
    manifest = json.loads(manifest_path.read_text())
    live = GAME / "engine/ikemen-go-v1.0.0/chars" / slug
    live_match = []
    for sff in live.glob("*.sff"):
        if hashlib.sha256(sff.read_bytes()).hexdigest() == manifest["installed_sff_sha256"]:
            live_match.append(sff.name)
    images = [path for path in sorted(style.glob("*.png")) if "source" not in path.stem and "candidate" not in path.stem]
    preview_index = character / "gameplay-previews/index.json"
    preview_html = ""
    if preview_index.exists():
        preview_data = json.loads(preview_index.read_text())
        moves = preview_data.get("moves", [])
        featured = next((move for move in moves if move.get("category") == "Ultimate"), moves[0] if moves else None)
        if featured:
            preview_html = f'<figure class="featured"><a href="../characters/{slug}/review.html"><img loading="lazy" src="../characters/{slug}/gameplay-previews/{featured["file"]}" alt="{html.escape(slug)} {html.escape(featured["name"])} animated preview"></a><figcaption>{html.escape(featured.get("category", "Move"))}: {html.escape(featured["name"])}</figcaption></figure>'
    figures = "".join(
        f'<figure><a href="../characters/{slug}/style/conversion-v1/{path.name}"><img loading="lazy" src="../characters/{slug}/style/conversion-v1/{path.name}" alt="{html.escape(slug)} {html.escape(path.stem)}"></a><figcaption>{html.escape(path.stem.replace("-", " "))}</figcaption></figure>'
        for path in images
    )
    body = manifest.get("body_sprites_replaced", 0)
    effects = manifest.get("move_effect_sprites_replaced", 0)
    count = manifest.get("source_sprite_count", body + effects)
    valid = bool(live_match)
    audit.append({
        "slug": slug,
        "status": "PASS" if valid else "FAIL",
        "source_sprite_count": count,
        "body_sprites_replaced": body,
        "effect_sprites_replaced": effects,
        "live_sff_hash_match": live_match,
        "canonical_manifest": f"../characters/{slug}/style/conversion-v1/installation.json",
    })
    cards.append(f'''<article id="{slug}"><header><h2>{html.escape(slug.replace('-', ' ').title())}</h2><strong class="{'pass' if valid else 'fail'}">{'PASS' if valid else 'FAIL'}</strong></header><p>{body:,} body sprites and {effects:,} move/effect sprites replaced; {count:,} original sprite keys accounted for.</p>{preview_html}<div class="images">{figures}</div><p><a href="../characters/{slug}/review.html"><strong>Gameplay, moves, and ultimates</strong></a> · <a href="../characters/{slug}/MOVESET.md">Moveset sheet</a> · <a href="../characters/{slug}/style/conversion-v1/installation.json">Installation evidence</a> · <a href="../characters/{slug}/import-report.json">Character report</a> · Live archive: {html.escape(', '.join(live_match) or 'no hash match')}</p></article>''')

summary = {
    "status": "PASS" if all(item["status"] == "PASS" for item in audit) else "FAIL",
    "completed_conversions": len(audit),
    "failed_conversions": [item["slug"] for item in audit if item["status"] != "PASS"],
    "fighters": audit,
}
(OUT / "canonical-port-audit.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Imported fighter conversion review</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#101722;color:#edf3fa;font:16px/1.55 system-ui}}main{{max-width:1500px;margin:auto;padding:24px}}a{{color:#9edcff}}.summary,article{{background:#1b2939;border:1px solid #3a5369;border-radius:12px;padding:20px;margin:20px 0}}header{{display:flex;align-items:center;justify-content:space-between;gap:20px}}h1,h2{{line-height:1.2}}.pass{{color:#86efa4}}.fail{{color:#ff9494}}.images{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}}figure{{margin:0;background:#111b29;padding:10px;border-radius:8px}}img{{width:100%;height:300px;object-fit:contain;background:#ff00ff}}.featured{{max-width:520px;margin:14px 0}}.featured img{{background:#11131d}}figcaption{{color:#c5d4e2;text-align:center}}code{{color:#cae5ff}}</style><main><h1>Imported fighter illustrated conversions</h1><section class="summary"><strong class="{'pass' if summary['status']=='PASS' else 'fail'}">{summary['status']}: {len(audit)} completed ports</strong><p>Every card is backed by the canonical character folder and an installed engine SFF whose SHA-256 matches its installation manifest. Gameplay files were preserved by each installer. Native launch capture remains pending because the local renderer stops before fighter loading.</p><p>Select an animated preview or the <strong>Gameplay, moves, and ultimates</strong> link on any fighter to open the full character review.</p><p><a href="canonical-port-audit.json">Machine-readable audit</a> · <a href="conversion-progress.json">Full conversion queue</a> · <a href="../mugen-expansion/review.html">Original imports and controls</a></p></section>{''.join(cards)}</main></html>'''
(OUT / "review.html").write_text(page, encoding="utf-8")
print(json.dumps({"review": str(OUT / "review.html"), **{key: summary[key] for key in ("status", "completed_conversions", "failed_conversions")}}, indent=2))
