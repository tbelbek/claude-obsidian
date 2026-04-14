# Ingest Eval Harness

Scores a `wiki/` directory against a JSON rubric. Pure stdlib Python. No deps.

The composite scalar is what karpathy-autoresearch hill-climbs.

## Run

```bash
python3 eval/ingest_eval.py --wiki wiki --rubric eval/rubric.json
```

Add `--json` for machine-readable output (one object to stdout). The loop parses `{"metric": 0.7234, ...}`.

## Rubric (`rubric.json`)

| Field | What it does |
|---|---|
| `score_subdirs` | Which wiki subfolders contribute pages to scoring |
| `required_frontmatter` | Field names that must be present + non-empty on every page |
| `min_citations_per_page` | Target wiki-links per page body; pages below this lose proportional credit |
| `min_words_per_page` / `max_words_per_page` | Sanity range — stubs and bloat both penalized |
| `expected_entities` / `expected_concepts` | Golden-fixture lists. If empty, recall metrics return 1.0 (neutral) |
| `weights` | Weighted sum → one composite in [0, 1] |

## Metrics

| Metric | Signal |
|---|---|
| `entity_recall` | % of expected entity titles present in output |
| `concept_recall` | % of expected concept titles present in `concepts/` |
| `frontmatter_completeness` | % of pages with all required fields populated |
| `citation_density` | Avg wiki-links per page, capped at `min_citations_per_page` |
| `orphan_rate` | 1 minus (pages with zero backlinks / total) |
| `dedup` | 1 minus (duplicate titles / total titles) |
| `page_length_sanity` | Stubs and bloat get fractional credit |

## Fixtures

Each fixture is a directory under `eval/fixtures/<name>/`:

```
eval/fixtures/<name>/
  source.md                 # copy of the .raw/ source
  expected_entities.json    # ["Person A", "Org B", "Product C"]
  expected_concepts.json    # ["Concept A", "Concept B"]
  NOTES.md                  # human notes on what "good" looks like
```

Pass `--fixture eval/fixtures/<name>` to override the recall lists in the rubric for that run.

## Workflow with karpathy-autoresearch

1. `eval/fixtures/<name>` = fixed input (source + expected)
2. Loop edits `skills/wiki-ingest/SKILL.md`
3. Each trial: headless `claude -p "ingest eval/fixtures/<name>/source.md"` into a clean `wiki/` scratch dir
4. `python3 eval/ingest_eval.py --wiki <scratch> --rubric eval/rubric.json --fixture eval/fixtures/<name> --json` → metric
5. Keep commit if metric improved; reset if not
6. `program.md` authors the above as the run command

## Sanity-check it first

Before wiring into a loop, run the scorer against the current vault and look at the number. If it doesn't roughly match your gut sense of quality, fix the rubric before optimizing against it. A bad rubric produces a polished prompt that writes worse pages.
