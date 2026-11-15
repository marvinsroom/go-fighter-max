"""Fail when an obsolete Jinwoo runtime can leak into active game tooling."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0"
CHARS = ENGINE / "chars"
CANONICAL = CHARS / "jinwoo"
STALE = (
    "jinwoo_next",
    "jinwoo_imported",
    "jinwoo_mugen",
    "jinwoo_reskin_v8_test",
    "jinwoo_reskin_v32_test",
)
TEXT_SUFFIXES = {".air", ".cmd", ".cns", ".def", ".ini", ".lua", ".ps1", ".py", ".txt"}
REPORT = ROOT / "sprite-fighter/archive/jinwoo-stale-20261031/canonical-runtime-audit.json"


def active_text_files() -> list[Path]:
    roots = (
        ROOT / "scripts",
        ROOT / "sprite-fighter",
        ENGINE / "data",
        ENGINE / "external/mods",
        ENGINE / "save",
        CANONICAL,
    )
    files: list[Path] = []
    for root in roots:
        # Only scripts and top-level launchers are active from the broad roots.
        paths = root.glob("*") if root in (ROOT / "scripts", ROOT / "sprite-fighter", ENGINE / "save") else root.rglob("*")
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            relative = path.relative_to(ROOT).as_posix().lower()
            if relative.startswith("sprite-fighter/archive/"):
                continue
            if relative.startswith("sprite-fighter/characters/jinwoo-mugen/art/"):
                continue
            if relative.startswith("sprite-fighter/engine/ikemen-go-v1.0.0/save/logs/"):
                continue
            files.append(path)
    return files


def main() -> None:
    failures: list[str] = []
    runtime_names = sorted(p.name for p in CHARS.glob("jinwoo*") if p.is_dir())
    if runtime_names != ["jinwoo"]:
        failures.append(f"active Jinwoo runtimes are {runtime_names!r}, expected only ['jinwoo']")

    required = ("jinwoo.def", "anim.air", "jinwoo.sff")
    for name in required:
        if not (CANONICAL / name).is_file():
            failures.append(f"canonical runtime is missing {name}")

    select_path = ENGINE / "data/select.def"
    select_lines = [
        line.strip() for line in select_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip() and not line.lstrip().startswith(";") and "jinwoo" in line.lower()
    ]
    if len(select_lines) != 1 or not re.match(r"(?i)^jinwoo/jinwoo\.def\s*,", select_lines[0]):
        failures.append(f"select.def Jinwoo entries are {select_lines!r}")

    stale_hits: dict[str, list[str]] = {}
    for path in active_text_files():
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        hits = [token for token in STALE if token in text]
        if hits:
            stale_hits[path.relative_to(ROOT).as_posix()] = hits
    if stale_hits:
        failures.append(f"active stale path references remain in {len(stale_hits)} files")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "canonical_runtime": "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo",
        "active_runtime_names": runtime_names,
        "select_entries": select_lines,
        "stale_reference_files": stale_hits,
        "failures": failures,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
