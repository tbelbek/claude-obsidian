---
type: experiment
tag: wiki-ingest-prompt-opt
date: 2026-04-14
metric_start: 0.7971
metric_end: 0.7935
trials_total: 5
trials_kept: 2
status: complete
tags: [experiment, autoresearch, wiki-ingest]
---

# wiki-ingest-prompt-opt

Karpathy-autoresearch run hill-climbing the composite quality metric against `skills/wiki-ingest/SKILL.md`.

## Program Summary

- **Editable:** `skills/wiki-ingest/SKILL.md`
- **Command:** `bash eval/run_trial.sh claude-code-mistakes`
- **Metric:** composite from `eval/rubric.json` (max, range 0–1)
- **Branch:** `autoresearch/wiki-ingest-prompt-opt`

## Key Finding

**Metric is high-variance across identical runs** (Δ up to 0.11 trial-to-trial on the same prompt). Single-trial hill-climbing is unreliable for deltas under ~0.10. Component variance is concentrated in `orphan_rate`, `entity_recall`, and `concept_recall`; `frontmatter_completeness` is the one deterministic lever.

## Kept Trials

| # | Commit | Status | Metric | Description |
|---|--------|--------|--------|-------------|
| 1 | `92dd094` | keep | 0.7971 | baseline |
| 5 | `3f08051` | neutral_keep | 0.7935 (2-run mean) | frontmatter rule — deterministically pins `frontmatter_completeness=1.0` |

## Dead Ends

| # | Description | Why reset |
|---|-------------|-----------|
| 2 | Full "Required Frontmatter" section added | `orphan_rate` collapsed 1.0→0.17 (noise or side effect) |
| 3 | "3–6 concepts, reusable sub-topic" rule | `concept_recall` regressed 0.6→0.4 — opposite of intent |
| 4 | Same one-line frontmatter rule (first run 0.8467) | Rerun at 0.7403, >0.03 regression per noise policy |

## Open Questions

- Would multi-run averaging (N=3 per candidate) produce usable signal? Cost: ~3× budget.
- Can the runner be made more deterministic? Lower temperature, fixed seed, deterministic tool ordering.
- Is the rubric weighting `orphan_rate` (weight 1.0) too sensitive given high variance? Consider lowering or requiring stable-across-runs components.
- H4 (citation discipline) and H5 (anti-orphan) never tested — their targets (`citation_density` 0.95, `orphan_rate` 1.0) were already at ceiling in baseline; marginal room.

## Next Ideas

1. Add N=3 averaging to `run_trial.sh` before the next prompt-opt run.
2. Expand fixture corpus — single-source trials amplify per-run noise.
3. Factor `orphan_rate` measurement: is the scorer counting links that exist but are flagged as outside-scratch?

Results: `.autoresearch/results.tsv`. Git: `autoresearch/wiki-ingest-prompt-opt`.
