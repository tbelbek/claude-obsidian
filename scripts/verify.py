#!/usr/bin/env python3
"""verify.py — provenance / groundedness tagger for wiki/ pages.

Hallucination control, not slop control. Each wiki/ knowledge page is classified
by whether its claims trace to a real source, and a provenance tag is stamped
into the page's frontmatter so the risky ones surface. This is the STRUCTURAL
(no-LLM) tier; the semantic faithfulness pass (does the page actually match its
source?) is a separate skill/agent step over the `needs-review` set emitted by
`verify.py review`.

Classes (added to the page's frontmatter `tags:` list):
  provenance/sourced      → has a resolvable .raw link, a URL, or links to a
                            wiki/sources page. Lower hallucination risk.
  provenance/unsourced    → no traceable source at all. Highest risk → also
                            tagged `needs-review`.
  provenance/log-derived  → synthesized from a chat log (conversation-review /
                            checkpoint). → also tagged `needs-review`.

The LLM pass later upgrades a reviewed page to `verified` (and drops
`needs-review`) or adds `contradicts-source`. This script never sets those.

NON-knowledge pages are skipped: meta files (_index, index, log, hot, overview,
dashboard, Wiki Map, getting-started, lint-report*), anything under
wiki/meta/archive/, and wiki/_templates/.

CLI:
  verify.py report   # classify, print table, NO write (default)
  verify.py apply    # write provenance + needs-review tags into frontmatter
  verify.py review   # one path per line needing the LLM faithfulness pass
  verify.py stats    # counts per class

Exit codes:
  0 — success
  2 — wiki/ directory not found

# ponytail: groundedness is a structural heuristic (has-a-source-link), NOT proof
# of faithfulness — that's the deliberate ceiling; the LLM pass closes the gap.
"""
import re
import sys
from pathlib import Path

META_NAMES = {
    "_index.md", "index.md", "log.md", "hot.md", "overview.md",
    "dashboard.md", "Wiki Map.md", "getting-started.md",
}
PROVENANCE = {
    "sourced": "provenance/sourced",
    "unsourced": "provenance/unsourced",
    "log-derived": "provenance/log-derived",
}
NEEDS_REVIEW = "needs-review"
LOG_RE = re.compile(r"conversation-review|checkpoint-", re.IGNORECASE)
SOURCE_LINK_FOLDERS = {"concepts", "entities", "comparisons", "questions", "projects"}


def find_root(start: Path) -> Path | None:
    """Walk upward for a dir containing wiki/."""
    cur = start.resolve()
    for d in (cur, *cur.parents):
        if (d / "wiki").is_dir():
            return d
    return None


def is_knowledge_page(rel: str) -> bool:
    """rel is a posix path like 'wiki/concepts/Foo.md'."""
    parts = rel.split("/")
    name = parts[-1]
    if name in META_NAMES or name.startswith("lint-report"):
        return False
    if "_templates" in parts:
        return False
    if "meta" in parts and "archive" in parts:
        return False
    return True


def _split_frontmatter(text: str):
    """Return (fm_body, rest) where rest begins at the closing '---'. fm_body is
    None if there is no frontmatter."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end:]


def classify_text(text: str, folder: str, source_titles: set) -> str:
    """Pure classifier. folder is the immediate wiki/ subfolder."""
    if LOG_RE.search(text):
        return "log-derived"
    fm, _ = _split_frontmatter(text)
    fm = fm or ""
    has_raw_link = bool(re.search(r"\.raw/[^\]\)\s\"]+", text))
    has_url = bool(re.search(r"https?://", fm))
    links = re.findall(r"\[\[([^\]|#]+)", text)
    links_to_source = any(l.strip() in source_titles for l in links)
    if has_raw_link or has_url or (folder in SOURCE_LINK_FOLDERS and links_to_source):
        return "sourced"
    return "unsourced"


def add_tags(text: str, new_tags: list) -> str:
    """Add each tag to the frontmatter `tags:` list if absent. Idempotent.

    Handles: block-list `tags:` (the dominant template form), inline
    `tags: [a, b]`, a missing tags field, and a missing frontmatter block.
    """
    new_tags = [t for t in new_tags if t]
    if not new_tags:
        return text
    fm, rest = _split_frontmatter(text)
    if fm is None:
        block = "tags:\n" + "".join(f"  - {t}\n" for t in new_tags)
        return "---\n" + block + "---\n\n" + text

    # inline form: tags: [a, b]
    m = re.search(r"^tags:\s*\[(.*?)\]\s*$", fm, re.MULTILINE)
    if m:
        existing = [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
        merged = existing + [t for t in new_tags if t not in existing]
        if merged == existing:
            return text
        line = "tags: [" + ", ".join(merged) + "]"
        new_fm = fm[: m.start()] + line + fm[m.end():]
        return "---" + new_fm + rest

    # block-list form: tags:\n  - x\n  - y
    lines = fm.splitlines()
    out, i, handled = [], 0, False
    while i < len(lines):
        out.append(lines[i])
        if re.match(r"^tags:\s*$", lines[i]):
            i += 1
            block, present = [], set()
            while i < len(lines) and re.match(r"^\s+-\s*(.+)$", lines[i]):
                block.append(lines[i])
                present.add(re.match(r"^\s+-\s*(.+?)\s*$", lines[i]).group(1).strip("\"'"))
                i += 1
            out.extend(block)
            for t in new_tags:
                if t not in present:
                    out.append(f"  - {t}")
            handled = True
            continue
        i += 1
    if not handled:
        # no tags field — insert a block at the top of frontmatter
        out = ["tags:"] + [f"  - {t}" for t in new_tags] + out
    return "---" + "\n".join(out) + rest


def iter_pages(root: Path):
    for p in sorted((root / "wiki").rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        if is_knowledge_page(rel):
            yield p, rel


def source_titles(root: Path) -> set:
    return {
        p.stem for p, rel in iter_pages(root) if rel.split("/")[1] == "sources"
    } if (root / "wiki" / "sources").is_dir() else set()


def classify_all(root: Path) -> dict:
    titles = source_titles(root)
    out = {}
    for p, rel in iter_pages(root):
        folder = rel.split("/")[1] if len(rel.split("/")) > 2 else "root"
        text = p.read_text(encoding="utf-8", errors="replace")
        out[rel] = classify_text(text, folder, titles)
    return out


def tags_for(cls: str) -> list:
    tags = [PROVENANCE[cls]]
    if cls in ("unsourced", "log-derived"):
        tags.append(NEEDS_REVIEW)
    return tags


def apply_all(root: Path) -> dict:
    result = classify_all(root)
    for rel, cls in result.items():
        p = root / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        updated = add_tags(text, tags_for(cls))
        if updated != text:
            p.write_text(updated, encoding="utf-8")
    return result


def main(argv) -> int:
    cmd = argv[1] if len(argv) > 1 else "report"
    root = find_root(Path.cwd())
    if root is None:
        print("verify: no wiki/ directory found above cwd", file=sys.stderr)
        return 2

    result = apply_all(root) if cmd == "apply" else classify_all(root)

    if cmd == "review":
        for rel, cls in sorted(result.items()):
            if cls in ("unsourced", "log-derived"):
                print(rel)
        return 0

    from collections import Counter
    counts = Counter(result.values())
    if cmd == "stats":
        print(f"total knowledge pages: {len(result)}")
        for k in ("sourced", "unsourced", "log-derived"):
            print(f"  {k}: {counts.get(k, 0)}")
        print(f"  needs-review (unsourced+log-derived): {counts.get('unsourced',0)+counts.get('log-derived',0)}")
        return 0

    for rel, cls in sorted(result.items()):
        flag = "  needs-review" if cls in ("unsourced", "log-derived") else ""
        print(f"{cls:<14} {rel}{flag}")
    where = " (tags written)" if cmd == "apply" else " (dry run; use `apply` to write tags)"
    review = counts.get("unsourced", 0) + counts.get("log-derived", 0)
    print(f"\n{len(result)} pages | sourced={counts.get('sourced',0)} "
          f"unsourced={counts.get('unsourced',0)} log-derived={counts.get('log-derived',0)} "
          f"| {review} need LLM review{where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
