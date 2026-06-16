#!/usr/bin/env python3
"""test_verify.py — hermetic tests for scripts/verify.py.

Heaviest coverage on add_tags() — it mutates real wiki pages, so block-list,
inline, missing-tags, missing-frontmatter, and idempotency must all be exact.
Plus classification (sourced/unsourced/log-derived), knowledge-page filtering,
and the review filter. Pure stdlib + a temp vault.

Usage:
  python3 tests/test_verify.py
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPER = ROOT / "scripts" / "verify.py"
spec = importlib.util.spec_from_file_location("verify", HELPER)
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


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


# ---- add_tags ----

def test_add_tags_block_list():
    text = "---\ntype: concept\ntags:\n  - concept\nstatus: seed\n---\n\n# Body\n"
    out = verify.add_tags(text, ["provenance/unsourced", "needs-review"])
    assert_true("block: keeps existing", "  - concept" in out)
    assert_true("block: adds provenance", "  - provenance/unsourced" in out)
    assert_true("block: adds needs-review", "  - needs-review" in out)
    assert_true("block: body intact", out.endswith("# Body\n"))
    assert_true("block: status preserved", "status: seed" in out)


def test_add_tags_idempotent():
    text = "---\ntags:\n  - provenance/sourced\n---\n\nx\n"
    out = verify.add_tags(text, ["provenance/sourced"])
    assert_eq("idempotent: unchanged", text, out)
    assert_eq("idempotent: single occurrence", 1, out.count("provenance/sourced"))


def test_add_tags_inline():
    text = "---\ntags: [concept, foo]\n---\n\nx\n"
    out = verify.add_tags(text, ["provenance/unsourced"])
    assert_true("inline: merged", "tags: [concept, foo, provenance/unsourced]" in out)


def test_add_tags_inline_idempotent():
    text = "---\ntags: [provenance/sourced]\n---\n\nx\n"
    out = verify.add_tags(text, ["provenance/sourced"])
    assert_eq("inline idempotent", text, out)


def test_add_tags_no_tags_field():
    text = "---\ntype: concept\nstatus: seed\n---\n\nx\n"
    out = verify.add_tags(text, ["provenance/unsourced"])
    assert_true("no-tags: inserts block", "tags:\n  - provenance/unsourced" in out)
    assert_true("no-tags: keeps type", "type: concept" in out)
    assert_true("no-tags: body intact", out.endswith("\nx\n"))


def test_add_tags_no_frontmatter():
    text = "# Just a body\nno fm here\n"
    out = verify.add_tags(text, ["provenance/unsourced"])
    assert_true("no-fm: prepends frontmatter", out.startswith("---\ntags:\n  - provenance/unsourced\n---\n"))
    assert_true("no-fm: body preserved", out.endswith("# Just a body\nno fm here\n"))


# ---- classification ----

def test_classify_log_derived():
    cls = verify.classify_text("see .raw/inbox/conversation-review-2026-01-01.md", "concepts", set())
    assert_eq("log-derived wins", "log-derived", cls)


def test_classify_sourced_via_raw_link():
    cls = verify.classify_text("body cites [[.raw/articles/x.md]]", "sources", set())
    assert_eq("raw link → sourced", "sourced", cls)


def test_classify_sourced_via_url():
    cls = verify.classify_text("---\nurl: https://example.com/a\n---\nbody", "sources", set())
    assert_eq("url → sourced", "sourced", cls)


def test_classify_sourced_via_source_link():
    cls = verify.classify_text("derived from [[Some Source]]", "concepts", {"Some Source"})
    assert_eq("links to a source page → sourced", "sourced", cls)


def test_classify_unsourced():
    cls = verify.classify_text("---\ntype: concept\n---\nFloating claims, no source.", "concepts", set())
    assert_eq("no grounding → unsourced", "unsourced", cls)


# ---- filtering / wiring ----

def test_is_knowledge_page_filters():
    assert_true("template excluded", not verify.is_knowledge_page("wiki/_templates/concept.md"))
    assert_true("index excluded", not verify.is_knowledge_page("wiki/concepts/_index.md"))
    assert_true("lint-report excluded", not verify.is_knowledge_page("wiki/meta/lint-report-2026-04-13.md"))
    assert_true("archive excluded", not verify.is_knowledge_page("wiki/meta/archive/old-session.md"))
    assert_true("real concept included", verify.is_knowledge_page("wiki/concepts/OAuth.md"))


def test_tags_for():
    assert_eq("sourced → 1 tag", ["provenance/sourced"], verify.tags_for("sourced"))
    assert_eq("unsourced → +needs-review", ["provenance/unsourced", "needs-review"], verify.tags_for("unsourced"))
    assert_eq("log-derived → +needs-review", ["provenance/log-derived", "needs-review"], verify.tags_for("log-derived"))


def make_vault(files: dict) -> Path:
    root = Path(tempfile.mkdtemp())
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return root


def test_apply_writes_tags_and_skips_meta():
    root = make_vault({
        "wiki/concepts/Floating.md": "---\ntype: concept\ntags:\n  - concept\n---\nNo source.",
        "wiki/sources/Real.md": "---\nurl: https://x.com\ntags:\n  - source\n---\nbody",
        "wiki/_templates/concept.md": "---\ntags:\n  - concept\n---\nTEMPLATE",
        "wiki/index.md": "# index",
    })
    result = verify.apply_all(root)
    assert_true("template skipped from result", "wiki/_templates/concept.md" not in result)
    assert_true("index skipped from result", "wiki/index.md" not in result)
    floating = (root / "wiki/concepts/Floating.md").read_text(encoding="utf-8")
    assert_true("unsourced tagged", "provenance/unsourced" in floating and "needs-review" in floating)
    real = (root / "wiki/sources/Real.md").read_text(encoding="utf-8")
    assert_true("sourced tagged", "provenance/sourced" in real)
    assert_true("sourced not flagged", "needs-review" not in real)
    template = (root / "wiki/_templates/concept.md").read_text(encoding="utf-8")
    assert_true("template untouched", "provenance" not in template)


def test_review_lists_only_risky():
    root = make_vault({
        "wiki/concepts/Floating.md": "---\ntags:\n  - concept\n---\nNo source.",
        "wiki/sources/Real.md": "cites [[.raw/articles/x.md]]",
    })
    risky = [rel for rel, cls in verify.classify_all(root).items() if cls in ("unsourced", "log-derived")]
    assert_eq("only the unsourced page is risky", ["wiki/concepts/Floating.md"], risky)


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    print(f"Running {len(tests)} verify tests...")
    for t in tests:
        print(t.__name__)
        t()
    print("\nAll verify tests passed.")


if __name__ == "__main__":
    main()
