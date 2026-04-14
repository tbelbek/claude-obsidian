#!/usr/bin/env python3
"""Score a wiki directory against a rubric. Stdlib only.

Usage:
    python eval/ingest_eval.py --wiki wiki --rubric eval/rubric.json
    python eval/ingest_eval.py --wiki wiki --rubric eval/rubric.json --json
    python eval/ingest_eval.py --wiki wiki --rubric eval/rubric.json --fixture eval/fixtures/<name>

Emits a single composite scalar in [0, 1] plus per-metric components. The loop
parses the scalar from stdout as the trial metric.
"""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal frontmatter: returns {field_name: raw_value_string} and body.

    Only records presence + simple scalar string value. Lists/blocks are
    recorded as present with value '<block>'. Enough for completeness checks.
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5 :]
    fm: dict[str, str] = {}
    current_key: str | None = None
    for line in fm_raw.splitlines():
        if not line.strip():
            current_key = None
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = val if val else "<block>"
            current_key = key if not val else None
        elif current_key and line.startswith(("  ", "\t", "- ")):
            # list continuation — mark parent as populated
            if fm.get(current_key) in (None, "", "<block>"):
                fm[current_key] = "<block>"
    return fm, body


def load_pages(wiki_dir: Path, subdirs: list[str]) -> list[dict]:
    pages = []
    for sub in subdirs:
        d = wiki_dir / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.md")):
            if p.name.startswith("_"):
                continue
            text = p.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            pages.append(
                {
                    "path": p,
                    "rel": str(p.relative_to(wiki_dir)),
                    "fm": fm,
                    "body": body,
                    "title": p.stem,
                    "subdir": sub,
                }
            )
    return pages


def wiki_links(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]", text)


# ---- metrics: each returns a float in [0, 1] ----

_STOPWORDS = {"the", "a", "an", "of", "and", "to", "in", "for", "on", "with", "by", "as", "at"}


def _norm(s: str) -> str:
    """Normalize for title matching: lower, hyphens/underscores/dots to spaces, collapse whitespace."""
    s = s.lower().replace("-", " ").replace("_", " ").replace(".", " ")
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s: str) -> set[str]:
    return {t for t in _norm(s).split() if t and t not in _STOPWORDS}


def _matches(expected: str, title: str) -> bool:
    """Token-subset match. Expected matches title if every expected content token
    (after stopword removal) appears in the title's token set. This handles:
    - 'Parallel Sessions' ~ 'parallel-claude-sessions' (subset match)
    - 'Git Worktrees' ~ 'worktree-isolation' (fails — 'git' not present; correct rejection)
    - 'CLAUDE.md' ~ 'claude-md-project-instructions' (subset match on {claude, md})
    """
    e_toks = _tokens(expected)
    if not e_toks:
        return False
    t_toks = _tokens(title)
    return e_toks.issubset(t_toks)


def m_entity_recall(pages, expected):
    if not expected:
        return 1.0
    titles = [p["title"] for p in pages if p["subdir"] == "entities"]
    hits = sum(1 for e in expected if any(_matches(e, t) for t in titles))
    return hits / len(expected)


def m_concept_recall(pages, expected):
    if not expected:
        return 1.0
    titles = [p["title"] for p in pages if p["subdir"] == "concepts"]
    hits = sum(1 for e in expected if any(_matches(e, t) for t in titles))
    return hits / len(expected)


def m_frontmatter_completeness(pages, required):
    if not pages or not required:
        return 1.0 if not required else 0.0
    ok = 0
    for p in pages:
        if all(f in p["fm"] and p["fm"][f] not in (None, "") for f in required):
            ok += 1
    return ok / len(pages)


def m_citation_density(pages, min_per_page):
    if not pages:
        return 0.0
    scores = []
    for p in pages:
        links = len(wiki_links(p["body"]))
        scores.append(min(1.0, links / max(1, min_per_page)))
    return sum(scores) / len(scores)


def m_orphan_rate(pages):
    """1.0 means no orphans. Ignores the newest page if corpus is size 1."""
    if len(pages) < 2:
        return 1.0
    inbound = Counter()
    for p in pages:
        for link in wiki_links(p["body"]):
            inbound[link] += 1
    orphans = sum(1 for p in pages if inbound.get(p["title"], 0) == 0)
    return 1.0 - (orphans / len(pages))


def m_dedup(pages):
    titles = [p["title"].lower() for p in pages]
    if not titles:
        return 1.0
    dupes = sum(c - 1 for c in Counter(titles).values() if c > 1)
    return 1.0 - (dupes / len(titles))


def m_page_length_sanity(pages, min_words, max_words):
    """Penalize stubs and bloat. 1.0 if within range, linearly falls off."""
    if not pages:
        return 0.0
    scores = []
    for p in pages:
        words = len(p["body"].split())
        if words < min_words:
            scores.append(words / max(1, min_words))
        elif words > max_words:
            scores.append(max(0.0, 1 - (words - max_words) / max_words))
        else:
            scores.append(1.0)
    return sum(scores) / len(scores)


def m_entity_research_depth(pages, min_words, min_outlinks):
    """Entity pages should have real content and at least one outlink (citation/source).

    Rewards the skill for researching authors rather than filing empty stubs.
    """
    ents = [p for p in pages if p["subdir"] == "entities"]
    if not ents:
        return 1.0
    scores = []
    for p in ents:
        words = len(p["body"].split())
        links = len(wiki_links(p["body"]))
        word_score = min(1.0, words / max(1, min_words))
        link_score = min(1.0, links / max(1, min_outlinks))
        scores.append((word_score + link_score) / 2)
    return sum(scores) / len(scores)


METRICS = {
    "entity_recall": lambda p, r: m_entity_recall(p, r.get("expected_entities", [])),
    "concept_recall": lambda p, r: m_concept_recall(p, r.get("expected_concepts", [])),
    "entity_research_depth": lambda p, r: m_entity_research_depth(
        p, r.get("entity_min_words", 80), r.get("entity_min_outlinks", 1)
    ),
    "frontmatter_completeness": lambda p, r: m_frontmatter_completeness(
        p, r.get("required_frontmatter", [])
    ),
    "citation_density": lambda p, r: m_citation_density(
        p, r.get("min_citations_per_page", 2)
    ),
    "orphan_rate": lambda p, r: m_orphan_rate(p),
    "dedup": lambda p, r: m_dedup(p),
    "page_length_sanity": lambda p, r: m_page_length_sanity(
        p,
        r.get("min_words_per_page", 50),
        r.get("max_words_per_page", 800),
    ),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", required=True, help="path to wiki/ directory")
    ap.add_argument("--rubric", required=True, help="path to rubric.json")
    ap.add_argument(
        "--fixture",
        help="optional fixture dir overriding expected_entities/concepts from rubric",
    )
    ap.add_argument("--json", action="store_true", help="emit JSON to stdout")
    args = ap.parse_args()

    rubric = json.loads(Path(args.rubric).read_text(encoding="utf-8"))

    if args.fixture:
        fdir = Path(args.fixture)
        ent_f = fdir / "expected_entities.json"
        con_f = fdir / "expected_concepts.json"
        if ent_f.exists():
            rubric["expected_entities"] = json.loads(ent_f.read_text())
        if con_f.exists():
            rubric["expected_concepts"] = json.loads(con_f.read_text())

    wiki = Path(args.wiki)
    subdirs = rubric.get("score_subdirs", ["concepts", "entities", "sources"])
    pages = load_pages(wiki, subdirs)

    weights = rubric["weights"]
    scores = {}
    for name, w in weights.items():
        fn = METRICS.get(name)
        if fn is None:
            print(f"unknown metric: {name}", file=sys.stderr)
            sys.exit(2)
        scores[name] = round(fn(pages, rubric), 4)

    total_w = sum(weights.values()) or 1
    composite = round(sum(scores[n] * w for n, w in weights.items()) / total_w, 4)

    if args.json:
        print(
            json.dumps(
                {
                    "metric": composite,
                    "components": scores,
                    "pages": len(pages),
                    "subdirs": subdirs,
                }
            )
        )
    else:
        print(f"pages scored: {len(pages)} ({', '.join(subdirs)})")
        print("-" * 54)
        for n, s in scores.items():
            print(f"  {n:28s} {s:.3f}  (weight {weights[n]})")
        print("-" * 54)
        print(f"  {'COMPOSITE METRIC':28s} {composite:.3f}")


if __name__ == "__main__":
    main()
