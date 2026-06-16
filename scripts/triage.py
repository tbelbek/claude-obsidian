#!/usr/bin/env python3
"""triage.py — classify .raw/ source files before ingestion.

The .raw/ inbox mixes high-signal reference material (clipped articles, project
notes) with low-signal auto-generated session logs (`checkpoint-*`,
`conversation-review-*`). Fanning session logs into the knowledge graph
pollutes entity/concept pages and the hot cache (the classic "bulk-dump into
RAG" failure mode). This helper is the deterministic triage gate consumed by:

  - skills/wiki-ingest/SKILL.md  (only ingest files whose decision == "ingest")

It classifies each .raw/ file by FILENAME pattern and records the verdict in
`.raw/.manifest.json` under a new top-level `triage` key — a logical-tag ledger.
Source files under .raw/ stay immutable (the skill's contract): the triage tag
lives in the manifest, never written into the source file.

Classification precedence (highest first):
  1. explicit `triage:` frontmatter override (ingest|archive|skip)
  2. filename log pattern (checkpoint-*, conversation-review-*) → archive
  3. `ai-generated` frontmatter tag → pending/skip (Claude authored it; awaits
     human sign-off before it can enter the wiki)
  4. default → reference → ingest (human-dropped source)

Tag taxonomy (the "track via tags" structure):
  triage/log        → session log              → decision: archive (never ingest)
  triage/pending    → ai-generated, unreviewed → decision: skip (needs human call)
  triage/reference  → human reference/project  → decision: ingest

Every entry also carries `ai_generated: true|false`, read from the `tags:` list.
Manual override: add `triage: ingest|archive|skip` to a file's own YAML
frontmatter and it wins over everything above (read-only; the script never
writes into source files).

CLI:
  triage.py report           # classify, print table, NO write (default)
  triage.py apply            # classify and write the `triage` map to manifest
  triage.py ingestable       # print one path per line where decision == ingest
  triage.py stats            # print counts per class/decision

Exit codes:
  0 — success
  2 — vault root (.raw/) not found

# ponytail: patterns are a hardcoded constant below — edit LOG_PATTERNS to tune.
# If rules ever need to be per-vault, lift them to .vault-meta/triage-rules.json.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

# Filename-prefix patterns that mark a file as an auto-generated session log.
LOG_PATTERNS = (
    re.compile(r"^checkpoint-", re.IGNORECASE),
    re.compile(r"^conversation-review-", re.IGNORECASE),
)

# Files that are never sources (vault meta / scaffolding inside .raw/).
SKIP_NAMES = {"README.md", "Dashboard.md", ".gitkeep"}

CLASS_TAG = {"log": "triage/log", "reference": "triage/reference", "pending": "triage/pending"}
CLASS_DECISION = {"log": "archive", "reference": "ingest", "pending": "skip"}
DECISION_CLASS = {"ingest": "reference", "archive": "log", "skip": "pending"}
VALID_DECISIONS = {"ingest", "archive", "skip"}


def find_root(start: Path) -> Path | None:
    """Walk upward from `start` looking for a dir that contains `.raw/`."""
    cur = start.resolve()
    for d in (cur, *cur.parents):
        if (d / ".raw").is_dir():
            return d
    return None


def _frontmatter_text(path: Path) -> str | None:
    """Return the inner YAML frontmatter block, or None if absent."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else None


def frontmatter_override(path: Path) -> str | None:
    """Return a `triage:` value from the file's YAML frontmatter, if valid."""
    fm = _frontmatter_text(path)
    if fm is None:
        return None
    for line in fm.splitlines():
        m = re.match(r"\s*triage\s*:\s*(\w+)\s*$", line)
        if m:
            val = m.group(1).lower()
            return val if val in VALID_DECISIONS else None
    return None


def has_ai_generated(path: Path) -> bool:
    """True if the frontmatter `tags:` list contains `ai-generated`.

    Handles both inline (`tags: [ai-generated, x]`) and block list forms.
    """
    fm = _frontmatter_text(path)
    if fm is None:
        return False
    inline = re.search(r"^tags:\s*\[(.*?)\]", fm, re.MULTILINE)
    if inline:
        return "ai-generated" in [t.strip().strip("\"'") for t in inline.group(1).split(",")]
    in_tags = False
    for line in fm.splitlines():
        if re.match(r"^tags:\s*$", line):
            in_tags = True
            continue
        if in_tags:
            item = re.match(r"\s+-\s*(.+?)\s*$", line)
            if item:
                if item.group(1).strip("\"'") == "ai-generated":
                    return True
            elif line.strip() and not line.startswith((" ", "\t")):
                break  # next top-level key ends the tags block
    return False


def classify_filename(name: str) -> str:
    """Pure filename → class. No I/O."""
    for pat in LOG_PATTERNS:
        if pat.search(name):
            return "log"
    return "reference"


def classify_file(path: Path) -> dict:
    """Classify one source file.

    Precedence: explicit `triage:` frontmatter override > filename log pattern >
    `ai-generated` tag (→ pending, awaits human sign-off) > default reference.
    """
    ai = has_ai_generated(path)
    override = frontmatter_override(path)
    if override:
        decision, cls, by = override, DECISION_CLASS[override], "override"
    elif classify_filename(path.name) == "log":
        decision, cls, by = "archive", "log", "pattern"
    elif ai:
        decision, cls, by = "skip", "pending", "ai-generated"
    else:
        decision, cls, by = "ingest", "reference", "default"
    return {"class": cls, "tag": CLASS_TAG[cls], "decision": decision, "by": by, "ai_generated": ai}


def iter_sources(root: Path):
    """Yield every candidate source path under .raw/ (relative to root)."""
    raw = root / ".raw"
    for p in sorted(raw.rglob("*.md")):
        if p.name in SKIP_NAMES:
            continue
        if any(part.startswith(".") for part in p.relative_to(root).parts[1:]):
            continue  # skip dotfiles/dot-dirs inside .raw (e.g. .manifest.json siblings)
        yield p


def build_triage(root: Path) -> dict:
    """Classify every source file → {relpath: verdict}."""
    out = {}
    for p in iter_sources(root):
        out[p.relative_to(root).as_posix()] = classify_file(p)
    return out


def load_manifest(root: Path) -> dict:
    mf = root / ".raw" / ".manifest.json"
    if mf.is_file():
        return json.loads(mf.read_text(encoding="utf-8"))
    return {"version": 1, "sources": {}}


def save_manifest(root: Path, manifest: dict) -> None:
    mf = root / ".raw" / ".manifest.json"
    mf.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def apply_triage(root: Path) -> dict:
    """Compute triage and persist it under the manifest `triage` key.

    Never touches the `sources` key — a skipped/archived file must not look
    ingested to the delta-check.
    """
    files = build_triage(root)
    manifest = load_manifest(root)
    manifest["triage"] = {
        "version": 1,
        "updated": date.today().isoformat(),
        "files": files,
    }
    save_manifest(root, manifest)
    return files


def _counts(files: dict) -> dict:
    c = {}
    for v in files.values():
        c[v["decision"]] = c.get(v["decision"], 0) + 1
    return c


def main(argv) -> int:
    cmd = argv[1] if len(argv) > 1 else "report"
    root = find_root(Path.cwd())
    if root is None:
        print("triage: no .raw/ directory found above cwd", file=sys.stderr)
        return 2

    if cmd == "ingestable":
        for rel, v in sorted(build_triage(root).items()):
            if v["decision"] == "ingest":
                print(rel)
        return 0

    files = apply_triage(root) if cmd == "apply" else build_triage(root)

    if cmd == "stats":
        counts = _counts(files)
        print(f"total: {len(files)}")
        for k in ("ingest", "archive", "skip"):
            print(f"  {k}: {counts.get(k, 0)}")
        return 0

    # report / apply → print a compact table
    for rel, v in sorted(files.items()):
        print(f"{v['decision']:<8} {v['tag']:<18} {v['by']:<9} {rel}")
    counts = _counts(files)
    summary = ", ".join(f"{k}={counts.get(k, 0)}" for k in ("ingest", "archive", "skip"))
    where = " (written to manifest)" if cmd == "apply" else " (dry run; use `apply` to persist)"
    print(f"\n{len(files)} files: {summary}{where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
