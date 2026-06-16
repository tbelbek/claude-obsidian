#!/usr/bin/env python3
"""test_triage.py — hermetic tests for scripts/triage.py.

Covers filename classification, frontmatter override, manifest persistence
(triage key written, sources key untouched), the ingestable filter, and root
discovery. No network, no LLM. Pure stdlib + a temp vault.

Usage:
  python3 tests/test_triage.py
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPER = ROOT / "scripts" / "triage.py"

spec = importlib.util.spec_from_file_location("triage", HELPER)
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)


class Fail(SystemExit):
    pass


def assert_eq(label, expected, actual):
    if expected != actual:
        raise Fail(f"FAIL {label}: expected {expected!r}, got {actual!r}")
    print(f"  ok: {label}")


def assert_true(label, cond, hint=""):
    if not cond:
        raise Fail(f"FAIL {label}: {hint}")
    print(f"  ok: {label}")


def make_vault(files: dict) -> Path:
    """files: {relpath: content}. Returns a temp vault root containing .raw/."""
    root = Path(tempfile.mkdtemp())
    (root / ".raw").mkdir()
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return root


def test_classify_filename():
    assert_eq("checkpoint → log", "log", triage.classify_filename("checkpoint-2026-04-02.md"))
    assert_eq("conversation-review → log", "log", triage.classify_filename("conversation-review-2026-03-13.md"))
    assert_eq("article → reference", "reference", triage.classify_filename("Volvo Cars Developer Portal.md"))
    assert_eq("case-insensitive", "log", triage.classify_filename("Checkpoint-x.md"))


def test_classify_file_decisions():
    root = make_vault({
        ".raw/inbox/checkpoint-1.md": "log body",
        ".raw/research/Article.md": "real content",
    })
    log = triage.classify_file(root / ".raw/inbox/checkpoint-1.md")
    ref = triage.classify_file(root / ".raw/research/Article.md")
    assert_eq("log decision", "archive", log["decision"])
    assert_eq("log tag", "triage/log", log["tag"])
    assert_eq("ref decision", "ingest", ref["decision"])
    assert_eq("ref by", "default", ref["by"])


def test_frontmatter_override_wins():
    root = make_vault({
        ".raw/research/Article.md": "---\ntriage: skip\ntags:\n  - x\n---\nbody",
        ".raw/inbox/checkpoint-2.md": "---\ntriage: ingest\n---\nbody",
    })
    ref = triage.classify_file(root / ".raw/research/Article.md")
    log = triage.classify_file(root / ".raw/inbox/checkpoint-2.md")
    assert_eq("override skip", "skip", ref["decision"])
    assert_eq("override by", "override", ref["by"])
    assert_eq("override promotes log to ingest", "ingest", log["decision"])


def test_invalid_override_ignored():
    root = make_vault({".raw/research/A.md": "---\ntriage: bogus\n---\nbody"})
    v = triage.classify_file(root / ".raw/research/A.md")
    assert_eq("bogus override falls back to default", "ingest", v["decision"])


def test_skip_names_excluded():
    root = make_vault({
        ".raw/README.md": "x",
        ".raw/Dashboard.md": "x",
        ".raw/real.md": "x",
    })
    rels = set(triage.build_triage(root).keys())
    assert_true("README excluded", ".raw/README.md" not in rels)
    assert_true("Dashboard excluded", ".raw/Dashboard.md" not in rels)
    assert_true("real included", ".raw/real.md" in rels)


def test_apply_writes_triage_not_sources():
    root = make_vault({".raw/inbox/checkpoint-9.md": "x", ".raw/blog/Post.md": "y"})
    # Seed a manifest with an existing sources entry — must be preserved & untouched.
    triage.save_manifest(root, {"version": 1, "sources": {".raw/blog/Post.md": {"hash": "abc"}}})
    triage.apply_triage(root)
    manifest = json.loads((root / ".raw/.manifest.json").read_text(encoding="utf-8"))
    assert_true("triage key present", "triage" in manifest)
    assert_true("sources preserved", manifest["sources"] == {".raw/blog/Post.md": {"hash": "abc"}})
    log = manifest["triage"]["files"][".raw/inbox/checkpoint-9.md"]
    assert_eq("log archived in ledger", "archive", log["decision"])
    assert_true("log NOT in sources", ".raw/inbox/checkpoint-9.md" not in manifest["sources"])


def test_apply_idempotent():
    root = make_vault({".raw/inbox/checkpoint-9.md": "x", ".raw/blog/Post.md": "y"})
    first = triage.apply_triage(root)
    second = triage.apply_triage(root)
    assert_eq("idempotent classification", first, second)


def test_ingestable_filter():
    root = make_vault({
        ".raw/inbox/checkpoint-9.md": "x",
        ".raw/blog/Post.md": "y",
        ".raw/research/conversation-review-z.md": "z",
    })
    ingestable = [r for r, v in triage.build_triage(root).items() if v["decision"] == "ingest"]
    assert_eq("only the article is ingestable", [".raw/blog/Post.md"], ingestable)


def test_ai_generated_defaults_pending():
    root = make_vault({
        ".raw/articles/block.md": "---\ntags:\n  - source\n  - ai-generated\n---\nbody",
        ".raw/articles/inline.md": "---\ntags: [ai-generated, source]\n---\nbody",
    })
    block = triage.classify_file(root / ".raw/articles/block.md")
    inline = triage.classify_file(root / ".raw/articles/inline.md")
    for label, v in (("block", block), ("inline", inline)):
        assert_eq(f"{label} ai-gen → skip", "skip", v["decision"])
        assert_eq(f"{label} ai-gen class", "pending", v["class"])
        assert_eq(f"{label} ai-gen tag", "triage/pending", v["tag"])
        assert_eq(f"{label} ai-gen by", "ai-generated", v["by"])
        assert_true(f"{label} ai_generated flag", v["ai_generated"] is True)


def test_log_filename_beats_ai_generated():
    # An ai-generated session log is still a log → archive, not pending.
    root = make_vault({".raw/inbox/conversation-review-x.md": "---\ntags:\n  - ai-generated\n---\nb"})
    v = triage.classify_file(root / ".raw/inbox/conversation-review-x.md")
    assert_eq("log wins over ai-generated", "archive", v["decision"])
    assert_true("ai_generated still recorded", v["ai_generated"] is True)


def test_override_beats_ai_generated():
    root = make_vault({".raw/articles/a.md": "---\ntriage: ingest\ntags:\n  - ai-generated\n---\nb"})
    v = triage.classify_file(root / ".raw/articles/a.md")
    assert_eq("override beats ai-generated pending", "ingest", v["decision"])
    assert_eq("override by", "override", v["by"])


def test_non_ai_human_source_ingests():
    root = make_vault({".raw/articles/human.md": "---\ntags:\n  - source\n---\nb"})
    v = triage.classify_file(root / ".raw/articles/human.md")
    assert_eq("human (no ai-generated) → ingest", "ingest", v["decision"])
    assert_true("ai_generated false", v["ai_generated"] is False)


def test_find_root_walks_up():
    root = make_vault({".raw/blog/Post.md": "y"})
    deep = root / ".raw" / "blog"
    assert_eq("finds root from nested dir", root.resolve(), triage.find_root(deep))


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} triage tests...")
    for t in tests:
        print(t.__name__)
        t()
    print("\nAll triage tests passed.")


if __name__ == "__main__":
    main()
