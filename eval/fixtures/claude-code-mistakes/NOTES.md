# Fixture: claude-code-mistakes

## Source

Twitter article by @zodchiii (2026-04-06) titled "7 Claude Code Mistakes That Are Costing You Hours". 270 lines. Single-author, single-thread, 7 enumerated mistakes + fixes + a cheat sheet.

Original URL: https://x.com/zodchiii/status/2041107570258018801

## Why this source

Well-structured, bounded, English-only, single-author. Good signal for entity extraction (author handle + product + cited third party). Good signal for concept extraction (each mistake is a reusable concept, plus the umbrella).

## What "good ingestion" should produce

### Entities (3 expected)

- **@zodchiii** — the author. Every source must have an author entity.
- **Claude Code** — the product under discussion. Already exists in most wikis; ingestion should link, not re-create.
- **Boris Cherny** — cited as "Claude Code creator" in mistake #3. Attribution matters; ingestion should capture third-party authorities mentioned in a source.

### Concepts (5 expected)

- **Claude Code Best Practices** — umbrella concept that ties the mistakes together. Primary output.
- **CLAUDE.md** — mistake #4's subject. Foundational artifact referenced repeatedly; warrants its own concept.
- **Parallel Sessions** — mistake #7's subject. Reusable across future sources.
- **Git Worktrees** — mistake #5's fix. Reusable concept.
- **Context Window Management** — mistake #1's subject. Reusable and already a concern across the wiki.

### What NOT to expect

- One page per mistake (that's sub-section granularity, not concept granularity)
- A page titled after the article itself in concepts/ (that belongs in sources/)
- Pages for every CLI flag mentioned (`--permission-mode`, `--allowedTools`, etc.) — those are details, not concepts

## How recall is scored

`ingest_eval.py` checks case-insensitive filename-stem match against these lists. So "Claude Code Best Practices" matches `Claude-Code-Best-Practices.md` → no; wait, hyphens don't match spaces. Titles in the expected list must match the filename stem after hyphen/space normalization.

If the ingestion writes `Claude-Code-Best-Practices.md`, the scorer should match `"Claude Code Best Practices"` in expected. Current implementation uses exact stem match — this fixture stress-tests that and may require the scorer to be upgraded to normalize hyphens↔spaces before matching. Noted; fix in a follow-up if recall scores zero on trivially-formatted names.

## Rerunning

```bash
python3 eval/ingest_eval.py \
  --wiki <scratch-wiki-dir> \
  --rubric eval/rubric.json \
  --fixture eval/fixtures/claude-code-mistakes \
  --json
```
