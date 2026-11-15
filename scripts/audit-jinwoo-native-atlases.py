"""Audit source and generated atlas cells for clipping/cross-cell contamination."""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen-reskin/art/native-comic-v4"
requests = json.loads((ART / "requests.json").read_text(encoding="utf-8"))
report = {"status": "PASS", "sheets": [], "failures": []}

for request in requests:
    row = {"kind": request["kind"], "template": [], "generated": []}
    for phase, path in (("template", ART / "templates" / f"{request['kind']}.png"),
                        ("generated", ART / f"{request['kind']}.png")):
        image = Image.open(path).convert("RGBA")
        for index in range(request["count"]):
            column, atlas_row = index % request["columns"], index // request["columns"]
            left = round(column * image.width / request["columns"])
            right = round((column + 1) * image.width / request["columns"])
            top = round(atlas_row * image.height / request["rows"])
            bottom = round((atlas_row + 1) * image.height / request["rows"])
            bounds = image.crop((left, top, right, bottom)).getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
            margins = None if bounds is None else [bounds[0], bounds[1], right-left-bounds[2], bottom-top-bounds[3]]
            entry = {"cell": index, "bounds": bounds, "margins": margins,
                     "source": request["frames"][index].get("source")}
            row[phase].append(entry)
            if bounds is None or min(margins) < 8:
                report["failures"].append({"kind": request["kind"], "phase": phase, **entry})
    report["sheets"].append(row)

if report["failures"]:
    report["status"] = "FAIL"
(ART / "atlas-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"status": report["status"], "failures": len(report["failures"]),
                  "by_phase": {phase: sum(item["phase"] == phase for item in report["failures"])
                               for phase in ("template", "generated")}}, indent=2))
