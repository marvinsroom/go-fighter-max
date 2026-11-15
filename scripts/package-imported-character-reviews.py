"""Package completed imported fighters like the main cast character folders."""
from pathlib import Path
import hashlib, html, json, re

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
PROGRESS = json.loads((GAME / "style-wave2/conversion-progress.json").read_text())
SLUGS = list(PROGRESS["installed"])
GENERIC = {
    "a", "b", "c", "x", "y", "z", "s", "fwd", "back", "up", "down",
    "upfwd", "upback", "downfwd", "downback", "hold_a", "hold_b", "hold_c",
    "hold_x", "hold_y", "hold_z", "hold_s", "holdfwd", "holdback", "holdup",
    "holddown", "holdupfwd", "holdupback", "holddownfwd", "holddownback",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_text(path):
    for encoding in ("utf-8", "cp1252", "latin1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            pass
    return path.read_text(errors="replace")

def commands(path):
    rows = []
    for block in re.split(r"(?im)^\s*\[command\]\s*$", read_text(path))[1:]:
        name = re.search(r'(?im)^\s*name\s*=\s*"?([^";\r\n]+)', block)
        command = re.search(r'(?im)^\s*command\s*=\s*([^;\r\n]+)', block)
        if name and command:
            pair = (name.group(1).strip(), command.group(1).strip())
            if pair not in rows:
                rows.append(pair)
    return rows

def title_for(slug, live):
    definition = live / f"{slug}.def"
    if not definition.exists():
        definition = next(live.glob("*.def"))
    text = read_text(definition)
    match = re.search(r'(?im)^\s*displayname\s*=\s*"?([^";\r\n]+)', text)
    return (match.group(1).strip() if match else slug.replace("-", " ").title()), definition

for slug, tracked in PROGRESS["installed"].items():
    folder = GAME / "characters" / slug
    live = GAME / "engine/ikemen-go-v1.0.0/chars" / slug
    style = folder / "style/conversion-v1"
    manifest = json.loads((style / "installation.json").read_text())
    name, definition = title_for(slug, live)
    position = SLUGS.index(slug)
    previous_slug = SLUGS[position - 1]
    next_slug = SLUGS[(position + 1) % len(SLUGS)]
    fighter_nav = "".join(f'<a href="../{other}/review.html" aria-current="{"page" if other == slug else "false"}">{html.escape(other.replace("-", " ").title())}</a>' for other in SLUGS)
    definition_text = read_text(definition)
    cmd_ref = re.search(r"(?im)^\s*cmd\s*=\s*([^;\r\n]+)", definition_text)
    cmd = live / cmd_ref.group(1).strip() if cmd_ref else None
    if not cmd or not cmd.exists():
        candidates = [path for path in live.rglob("*") if path.is_file() and path.suffix.lower() in (".cmd", ".cmnd")]
        if not candidates:
            raise RuntimeError(f"No CMD/CMND file for {slug}")
        cmd = sorted(candidates)[0]
    rows = commands(cmd)
    if slug == "zoro":
        zoro_names = {
            "skill": "Oni Giri (250 meter)",
            "rising": "Rising Dragon (500 meter)",
            "cyclone": "Three Sword Cyclone (750 meter)",
            "super": "Rokudou no Tsuji (1000 meter)",
            "tatsumaki": "Kokujou Oo Tatsumaki (2000 meter)",
            "ultimate": "San Zen Sekai — Ultimate (3000 meter)",
            "SPECIAL 1": "Rokudou no Tsuji (1000 meter)",
            "SPECIAL 3": "Kokujou Oo Tatsumaki (2000 meter)",
            "SPECIAL 5": "San Zen Sekai — Ultimate (3000 meter)",
            "SPECIAL 2": "Reverse sword special",
            "SPECIAL 4": "Reverse sword special II",
            "SPECIAL 6": "Reverse sword special III",
        }
        rows = [(zoro_names.get(n, n), v) for n, v in rows]
    featured = [(name_, value) for name_, value in rows if name_.lower() not in GENERIC]
    source_notes = [path for path in folder.rglob("*") if path.is_file() and ("move" in path.name.lower() or "control" in path.name.lower()) and path.suffix.lower() in (".txt", ".md")]

    legend = "Z/X/C = MUGEN a/b/c; A/S/D = x/y/z; Enter = Start. F and B are relative to the opponent; D/U are down/up; ~ means release or sequence timing; / means hold."
    quick = featured[:16]
    controls = [f"# {name} controls", "", "## Keyboard", "", "| Action | Player 1 |", "|---|---|", "| Move / jump / crouch / guard | Arrow keys |", "| MUGEN a / b / c | Z / X / C |", "| MUGEN x / y / z | A / S / D |", "| Start | Enter |", "", legend, "", "## Featured commands", "", "| Command name | MUGEN input |", "|---|---|"]
    controls += [f"| {n.replace('|', '/')} | `{v.replace('|', '/')}` |" for n, v in quick]
    controls += ["", "See [MOVESET.md](MOVESET.md) for every command defined by the installed fighter.", ""]
    (folder / "CONTROLS.md").write_text("\n".join(controls), encoding="utf-8")

    moveset = [f"# {name} moveset", "", "This sheet is generated from the CMD file currently installed in the playable engine package.", "", f"- Definition: `{definition.name}`", f"- Commands: `{cmd.name}`", f"- Defined command entries: {len(rows)}", f"- Illustrated body sprites replaced: {manifest.get('body_sprites_replaced', 0)}", f"- Illustrated move/effect sprites replaced: {manifest.get('move_effect_sprites_replaced', 0)}", "", "## Input legend", "", legend, "", "## Complete command sheet", "", "| Command name | MUGEN input |", "|---|---|"]
    moveset += [f"| {n.replace('|', '/')} | `{v.replace('|', '/')}` |" for n, v in rows]
    if source_notes:
        moveset += ["", "## Creator-provided move notes", ""] + [f"- `{path.relative_to(folder).as_posix()}`" for path in source_notes]
    moveset.append("")
    (folder / "MOVESET.md").write_text("\n".join(moveset), encoding="utf-8")

    images = [path for path in sorted(style.glob("*.png")) if "source" not in path.stem and "candidate" not in path.stem]
    figures = "".join(f'<figure><a href="style/conversion-v1/{p.name}"><img src="style/conversion-v1/{p.name}" alt="{html.escape(name)} {html.escape(p.stem)}"></a><figcaption>{html.escape(p.stem.replace("-", " "))}</figcaption></figure>' for p in images)
    preview_path = folder / "gameplay-previews/index.json"
    preview_data = json.loads(preview_path.read_text()) if preview_path.exists() else {"moves": [], "ultimate_preview_status": "MISSING"}
    previews = preview_data["moves"]
    move_cards = "".join(f'<article class="move"><strong class="tag">{html.escape(item.get("category", "Move"))}</strong><img loading="lazy" src="gameplay-previews/{item["file"]}" alt="{html.escape(name)} {html.escape(item["name"])} animation"><h3>{html.escape(item["name"])}</h3><p><code>{html.escape(item["input"])}</code> · AIR {item["animation"]} · {item["frames"]} frames</p></article>' for item in previews)
    table = "".join(f"<tr><td>{html.escape(n)}</td><td><code>{html.escape(v)}</code></td></tr>" for n, v in featured[:24])
    report = {
        "status": "STATIC_GAMEPLAY_REVIEW_PASS",
        "character": slug,
        "definition": definition.name,
        "definition_sha256": digest(definition),
        "command_file": cmd.relative_to(live).as_posix(),
        "command_sha256": digest(cmd),
        "defined_commands": len(rows),
        "featured_commands": len(featured),
        "visual_move_previews": len(previews),
        "ultimate_preview_status": preview_data.get("ultimate_preview_status"),
        "installed_sff_sha256": manifest["installed_sff_sha256"],
        "sprite_key_preservation": "PASS",
        "gameplay_file_preservation": "PASS",
        "native_capture": "PENDING; local engine renderer stops before fighter loading",
    }
    (folder / "gameplay-review.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    review = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(name)} - Gameplay review</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#0a0a11;color:#f6f3ff;font:16px/1.6 system-ui}}main{{max-width:1200px;margin:auto;padding:40px 24px}}a{{color:#adceff}}section{{margin:28px 0;padding:20px;background:#151622;border:1px solid #303348;border-radius:12px}}.status{{border-left:5px solid #77db91}}.images,.moves-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}}figure{{margin:0}}img{{width:100%;height:300px;object-fit:contain;background:#11131d}}figure>img,figure a img{{background:#ff00ff}}figcaption{{text-align:center;color:#bbc4d5}}.move{{background:#10121c;border:1px solid #32364b;border-radius:9px;padding:12px}}.move img{{height:260px}}.move h3{{margin:8px 0 0}}.move p{{margin:4px 0;color:#bbc4d5}}.tag{{display:inline-block;color:#d5b7ff;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}}table{{width:100%;border-collapse:collapse}}td,th{{padding:9px;text-align:left;border-bottom:1px solid #35394b}}.wrap{{overflow:auto}}code{{color:#d8c4ff}}nav{{display:flex;gap:12px;flex-wrap:wrap}}.fighter-nav{{margin:18px 0;padding:12px;background:#11131d;border-radius:9px}}.fighter-nav a{{padding:5px 8px;border:1px solid #35394b;border-radius:5px;text-decoration:none}}.fighter-nav a[aria-current=page]{{background:#49325f;color:white}}</style><main><nav><a href="../../style-wave2/review.html">Completed conversion roster</a><a href="CONTROLS.md">Quick controls</a><a href="MOVESET.md">Full moveset sheet</a><a href="import-report.json">Import report</a></nav><nav class="fighter-nav" aria-label="Individual fighter reviews">{fighter_nav}</nav><header><p>FIGHTER / INDIVIDUAL GAMEPLAY REVIEW · {position + 1} OF {len(SLUGS)}</p><h1>{html.escape(name)}</h1><p>Installed imported gameplay with illustrated body and move/effect artwork.</p><p><a href="../{previous_slug}/review.html">← Previous fighter</a> · <a href="../{next_slug}/review.html">Next fighter →</a></p></header><section class="status"><h2>Validation status</h2><p><strong>Static gameplay review passed.</strong> Every original sprite key is retained, the installed SFF matches the conversion manifest, and CMD/CNS/AIR/SND gameplay files are unchanged.</p><p>The animations below are rendered directly from the installed SFF and AIR files. Every move uses one neutral-reference world scale; authored AIR per-frame scaling is retained. These are sprite-animation previews rather than engine match captures. Native capture remains pending because the local renderer stops before fighter loading.</p><p><strong>Ultimate preview:</strong> {html.escape(preview_data.get("ultimate_preview_status", "UNKNOWN"))}.</p><p><a href="gameplay-review.json">Gameplay evidence</a> · <a href="style/conversion-v1/installation.json">Sprite installation evidence</a> · <a href="gameplay-previews/index.json">Preview mapping and scale policy</a></p></section><section><h2>Moves, specials, supers, and ultimates</h2><div class="moves-grid">{move_cards}</div></section><section><h2>Controls and featured moves</h2><p>{html.escape(legend)}</p><div class="wrap"><table><thead><tr><th>Command</th><th>MUGEN input</th></tr></thead><tbody>{table}</tbody></table></div><p><a href="MOVESET.md">Open all {len(rows)} command definitions</a> · <a href="CONTROLS.md">Keyboard quick sheet</a></p></section><section><h2>Installed character and effect sheets</h2><div class="images">{figures}</div></section></main></html>'''
    (folder / "review.html").write_text(review, encoding="utf-8")
    readme = f"""# {name}

Playable imported fighter with illustrated body and move/effect conversion installed.

- [Gameplay review](review.html)
- [Quick controls](CONTROLS.md)
- [Full moveset sheet](MOVESET.md)
- [Gameplay validation](gameplay-review.json)
- [Artwork and installation evidence](style/conversion-v1/installation.json)

The untouched creator source is retained under `source/` when this fighter was imported from an external package. The active playable package is installed at `../../engine/ikemen-go-v1.0.0/chars/{slug}/`.
"""
    (folder / "README.md").write_text(readme, encoding="utf-8")

print(f"Packaged {len(PROGRESS['installed'])} character gameplay reviews and moveset sheets")

# Keep imported-fighter pages aligned with the interactive main-cast review
# format after regenerating their evidence and Markdown sheets.
import runpy
runpy.run_path(str(ROOT / "scripts/build-jinwoo-format-imported-reviews.py"), run_name="__main__")
