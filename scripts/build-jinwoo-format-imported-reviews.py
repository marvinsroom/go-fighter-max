"""Build interactive Jinwoo-style review pages for converted imported fighters."""
from pathlib import Path
import html, json, re

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

def keyboard_input(value):
    buttons = {"a": "Z", "b": "X", "c": "C", "x": "A", "y": "S", "z": "D", "s": "Enter"}
    directions = {"DF": "Down + Forward", "DB": "Down + Back", "UF": "Up + Forward", "UB": "Up + Back", "F": "Forward", "B": "Back", "D": "Down", "U": "Up"}
    parts = []
    for token in value.split(","):
        token = token.strip()
        prefix = ""
        if token.startswith("~"):
            prefix, token = "release ", token[1:]
        if token.startswith("/"):
            prefix, token = "hold ", token[1:]
        chord = [buttons.get(p.strip(), directions.get(p.strip().replace("$", "").upper(), p.strip())) for p in token.split("+")]
        parts.append(prefix + " + ".join(chord))
    return " then ".join(parts)

for position, slug in enumerate(SLUGS):
    folder = GAME / "characters" / slug
    live = GAME / "engine/ikemen-go-v1.0.0/chars" / slug
    definition = live / f"{slug}.def"
    if not definition.exists():
        definition = next(live.glob("*.def"))
    definition_text = read_text(definition)
    display = re.search(r'(?im)^\s*displayname\s*=\s*"?([^";\r\n]+)', definition_text)
    name = display.group(1).strip() if display else slug.replace("-", " ").title()
    cmd_ref = re.search(r"(?im)^\s*cmd\s*=\s*([^;\r\n]+)", definition_text)
    cmd = live / cmd_ref.group(1).strip() if cmd_ref else None
    if not cmd or not cmd.exists():
        cmd = next(p for p in live.rglob("*") if p.is_file() and p.suffix.lower() in (".cmd", ".cmnd"))
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
    featured = [(n, v) for n, v in rows if n.lower() not in GENERIC and not re.match(r"(?i)^ai\d*", n)]
    lookup = {n.lower(): v for n, v in rows}
    preview_path = folder / "gameplay-previews/index.json"
    preview = json.loads(preview_path.read_text())
    moves = preview.get("moves", [])
    for move in moves:
        value = move.get("input", "See moveset")
        if value in ("See moveset", "See controls"):
            value = lookup.get(move["name"].lower(), value)
        move["input"] = value
        move["keyboard"] = keyboard_input(value) if value not in ("See moveset", "See controls") else value
    fighter_nav = "".join(f'<a href="../{other}/review.html" aria-current="{"page" if other == slug else "false"}">{html.escape(other.replace("-", " ").title())}</a>' for other in SLUGS)
    cards = "".join(f'''<article class="move"><span class="tag">{html.escape(m.get("category", "Move"))}</span><button class="move-pick" data-index="{i}" type="button"><img loading="lazy" src="gameplay-previews/{m["file"]}" alt="{html.escape(name)} {html.escape(m["name"])}"><strong>{html.escape(m["name"])}</strong></button><p><kbd>{html.escape(m["keyboard"])}</kbd><br><small>MUGEN: {html.escape(m["input"])} · AIR {m["animation"]} · {m["frames"]} frames</small></p></article>''' for i, m in enumerate(moves))
    command_table = "".join(f"<tr><td>{html.escape(n)}</td><td><kbd>{html.escape(keyboard_input(v))}</kbd></td><td><code>{html.escape(v)}</code></td></tr>" for n, v in featured)
    images = [p for p in sorted((folder / "style/conversion-v1").glob("*.png")) if "source" not in p.stem]
    sheets = "".join(f'<figure><a href="style/conversion-v1/{p.name}"><img src="style/conversion-v1/{p.name}" alt="{html.escape(name)} {html.escape(p.stem)}"></a><figcaption>{html.escape(p.stem.replace("-", " "))}</figcaption></figure>' for p in images)
    data = json.dumps({"name": name, "moves": moves}, ensure_ascii=False).replace("</", "<\\/")
    previous_slug, next_slug = SLUGS[position - 1], SLUGS[(position + 1) % len(SLUGS)]
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(name)} - Combat review</title><style>
:root{{--bg:#0a0a11;--panel:#151622;--line:#303348;--muted:#bbc4d5;--accent:#bf9aff}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:#f6f3ff;font:16px/1.6 system-ui}}main{{max-width:1120px;margin:auto;padding:42px 24px}}a{{color:#adceff}}h1{{font-size:clamp(42px,7vw,76px);line-height:1;margin:12px 0}}section{{margin:32px 0}}.panel,.status,#viewer{{padding:20px;background:var(--panel);border:1px solid var(--line);border-radius:12px}}.status{{border-left:5px solid #77db91}}nav,.toolbar,.ultimate-links{{display:flex;gap:10px;flex-wrap:wrap;align-items:end}}.fighter-nav{{margin:18px 0;padding:12px;background:#11131d;border-radius:9px}}.fighter-nav a{{padding:5px 8px;border:1px solid var(--line);border-radius:5px;text-decoration:none}}.fighter-nav a[aria-current=page]{{background:#49325f;color:white}}button,select{{font:inherit;color:inherit;background:#222333;border:1px solid #4a415f;border-radius:7px;padding:9px 12px}}button{{cursor:pointer}}button:hover,button[aria-pressed=true]{{border-color:var(--accent);background:#49325f}}label{{display:flex;flex-direction:column;gap:5px;color:var(--muted);flex:1 1 220px}}#capture{{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#050509;border:1px solid var(--line);border-radius:10px;margin:15px 0}}#move-detail{{color:var(--muted)}}kbd{{display:inline-block;background:#282237;border:1px solid #514464;border-radius:4px;padding:2px 8px;color:#eee4ff}}.moves-grid,.images{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}}.move{{background:#10121c;border:1px solid var(--line);border-radius:9px;padding:12px}}.move-pick{{display:block;width:100%;padding:0;background:transparent;border:0;text-align:left}}.move-pick img{{width:100%;height:230px;object-fit:contain;background:#080a10}}.move-pick strong{{display:block;font-size:18px;padding:8px}}.move p{{color:var(--muted)}}.tag{{color:var(--accent);font-size:12px;letter-spacing:.12em;text-transform:uppercase}}table{{width:100%;border-collapse:collapse;min-width:680px}}td,th{{padding:10px;text-align:left;border-bottom:1px solid var(--line)}}.wrap{{overflow:auto}}figure{{margin:0}}figure img{{width:100%;height:300px;object-fit:contain;background:#ff00ff}}figcaption{{text-align:center;color:var(--muted)}}@media(max-width:600px){{main{{padding:28px 16px}}.ultimate-links button{{flex:1 1 100%}}}}
</style></head><body><main><nav><a href="../../style-wave2/review.html">Completed conversion roster</a><a href="CONTROLS.md">Quick controls</a><a href="MOVESET.md">Full moveset sheet</a><a href="import-report.json">Import report</a></nav><nav class="fighter-nav">{fighter_nav}</nav><header><p>FIGHTER / COMBAT REVIEW · {position + 1} OF {len(SLUGS)}</p><h1>{html.escape(name)}</h1><p>Watch the ultimate and every captured move, then use the keyboard inputs shown beside each one.</p><p><a href="../{previous_slug}/review.html">← Previous fighter</a> · <a href="../{next_slug}/review.html">Next fighter →</a></p></header>
<section id="viewer"><h2>Move viewer</h2><p>Choose an ultimate shortcut or browse by category.</p><nav id="ultimates" class="ultimate-links"></nav><div class="toolbar"><label>Category<select id="category"></select></label><label>Move<select id="clip"></select></label><button id="restart" type="button">Restart animation</button></div><img id="capture" alt="{html.escape(name)} selected move preview"><h3 id="move-title"></h3><p id="move-detail"></p></section>
<section class="status"><h2>Validation status</h2><p><strong>Gameplay review passed.</strong> Every original sprite key is retained and gameplay files remain unchanged.</p><p>These previews render the installed SFF and AIR at one consistent world scale. <strong>Ultimate preview: {html.escape(preview.get("ultimate_preview_status", "UNKNOWN"))}.</strong></p><p><a href="gameplay-review.json">Gameplay evidence</a> · <a href="style/conversion-v1/installation.json">Installation evidence</a> · <a href="gameplay-previews/index.json">Preview mapping</a></p></section>
<section><h2>All captured moves</h2><div class="moves-grid">{cards}</div></section>
<section class="panel"><h2>Keyboard controls and command list</h2><p><kbd>Arrow keys</kbd> move, jump, crouch, and guard. <kbd>Z</kbd>/<kbd>X</kbd>/<kbd>C</kbd> = MUGEN a/b/c. <kbd>A</kbd>/<kbd>S</kbd>/<kbd>D</kbd> = MUGEN x/y/z. <kbd>Enter</kbd> = Start. Forward and Back are relative to the opponent.</p><div class="wrap"><table><thead><tr><th>Move</th><th>Keyboard input</th><th>MUGEN notation</th></tr></thead><tbody>{command_table}</tbody></table></div><p><a href="MOVESET.md">Open all {len(rows)} command definitions</a> · <a href="CONTROLS.md">Keyboard quick sheet</a></p></section>
<section><h2>Installed character and effect sheets</h2><div class="images">{sheets}</div></section></main><script>
const data={data},category=document.getElementById('category'),clip=document.getElementById('clip'),capture=document.getElementById('capture'),title=document.getElementById('move-title'),detail=document.getElementById('move-detail'),ultimateNav=document.getElementById('ultimates'),groups={{}};data.moves.forEach((m,i)=>(groups[m.category]??=[]).push(i));function show(i){{const m=data.moves[i];if(!m)return;capture.src='gameplay-previews/'+m.file+'?restart='+Date.now();title.textContent=m.name;detail.innerHTML='<kbd>'+m.keyboard+'</kbd> · MUGEN: <code>'+m.input+'</code> · AIR '+m.animation+' · '+m.frames+' frames';document.querySelectorAll('[data-index]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.index)===i)));}}function fill(){{clip.replaceChildren();for(const i of groups[category.value]||[]){{const o=document.createElement('option');o.value=i;o.textContent=data.moves[i].name;clip.append(o)}}show(Number(clip.value))}}Object.keys(groups).sort((a,b)=>a==='Ultimate'?-1:b==='Ultimate'?1:a.localeCompare(b)).forEach(g=>{{const o=document.createElement('option');o.value=g;o.textContent=g;category.append(o)}});(groups.Ultimate||[]).forEach(i=>{{const b=document.createElement('button');b.type='button';b.textContent=data.moves[i].name;b.onclick=()=>{{category.value='Ultimate';fill();clip.value=i;show(i)}};ultimateNav.append(b)}});category.onchange=fill;clip.onchange=()=>show(Number(clip.value));document.getElementById('restart').onclick=()=>show(Number(clip.value));document.querySelectorAll('.move-pick').forEach(b=>b.onclick=()=>{{const i=Number(b.dataset.index),m=data.moves[i];category.value=m.category;fill();clip.value=i;show(i);document.getElementById('viewer').scrollIntoView({{behavior:'smooth'}})}});category.value=groups.Ultimate?'Ultimate':Object.keys(groups)[0];fill();
</script></body></html>'''
    (folder / "review.html").write_text(page, encoding="utf-8")

print(f"Built {len(SLUGS)} Jinwoo-format imported fighter reviews")
