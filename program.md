# Program — wiki-ingest-prompt-opt

Karpathy-autoresearch program. The loop hill-climbs the `wiki-ingest` skill prompt against an objective quality metric.

## Tag

`wiki-ingest-prompt-opt`

Branch: `autoresearch/wiki-ingest-prompt-opt`.

## Editable surface

Exactly one file. The loop may edit only this:

- `skills/wiki-ingest/SKILL.md`

## Frozen surface

Must not change:

- Everything in `eval/` (rubric, scorer, fixtures, runner)
- Every other file in `skills/`
- Every file in `commands/`, `agents/`, `hooks/`
- `.claude-plugin/`
- `README.md`, `CLAUDE.md`, `WIKI.md`, `LICENSE`

## Command

One shell command runs a single trial. Each trial averages N=3 headless runs to suppress variance. Emits one JSON line to stdout.

```bash
RUNS_PER_TRIAL=3 bash eval/run_trial_avg.sh claude-code-mistakes
```

Expected stdout:

```json
{"metric": 0.612, "metric_std": 0.04, "runs": 3, "components": {...}, "components_std": {...}, "pages": N, "runs_json": [...]}
```

Single-run fallback (for debugging only, never loop decisions):

```bash
bash eval/run_trial.sh claude-code-mistakes
```

## Metric

- **Name:** `metric` (composite from `eval/rubric.json`)
- **Direction:** `max` (higher is better, range [0, 1])
- **Extraction:** parse `metric` field from the single JSON line on stdout
- **Baseline:** 0.7971 single-run, ~0.79 averaged (measured 2026-04-14 on branch `autoresearch/wiki-ingest-prompt-opt`, trial 1). Re-baseline at the start of every new run.
- **Noise policy:** Headless Claude is non-deterministic. Single-run variance ~±0.1; N=3 averaging brings std into the ~0.02–0.05 range. A candidate is accepted only if `metric_mean` improves by more than `max(0.02, metric_std)` over the current baseline. If accepted, one additional averaged trial is run as a confirmation; accept only if it also clears the threshold.

## Secondary guards

A trial is rejected if any guard fails, regardless of metric:

- `pages >= 4` — a degenerate prompt that produces 0–3 pages is not a win even if metric is high
- Scorer exits 0
- Trial did not time out
- Scratch wiki contains at least one page in `sources/` AND at least one page in `concepts/` OR `entities/`

## Budgets

- **Per-run wall-clock:** 300 s soft / 600 s hard (inherited by `run_trial.sh`)
- **Per-trial wall-clock:** RUNS_PER_TRIAL × per-run (~15 min at N=3)
- **Total trials:** 12 (was 20 — each trial now costs 3× single-run)
- **Total wall-clock:** 3 hours
- **Stop after consecutive no-improvement trials:** 4

## Hypotheses (priority order)

The baseline flagged three high-impact gaps. Hypotheses target those directly.

1. **Require entity extraction for every cited author and mentioned product.** Add an explicit rule: "For every author, handle, or notable person/product mentioned in the source, create an entity page. Use WebSearch to populate with researched content (≥80 words) including role, affiliation, relevant links." Should lift `entity_recall` from 0.
2. **Require both `created` and `updated` in frontmatter.** Current skill emits `updated` only. Add both as non-negotiable. Should lift `frontmatter_completeness` from 0.37.
3. **Tune concept granularity rule.** Replace any "umbrella concept" default with: "Produce 3–6 concepts for a source of 200–500 lines. Each concept should be a reusable sub-topic, not a section summary. If a section deserves its own concept, extract it. If two sections share a theme, merge them." Should lift `concept_recall` from 0.2 without inflating page count.
4. **Add a citation-discipline clause.** "Every non-obvious claim must carry a wiki-link or `(Source: ...)` marker. Body paragraphs with zero links are a bug." Should lift `citation_density`.
5. **Add explicit anti-orphan pass.** "Before writing a new page, list at least 2 existing pages it will link to, and update at least one of those pages to link back." Should lift `orphan_rate`.
6. **Simplify.** Delete any sections of SKILL.md that don't contribute to the above. "Prefer code/prose deletion — a trial that shortens the skill without regressing the metric is a win." This is the Karpathy bias toward simplicity.

## Notes / constraints

- Prefer prompt deletion to prompt addition. A shorter skill that holds the metric is a win.
- One variable per trial. Do not combine hypotheses. If two signals look related, pick one and see if the other moves as a side effect.
- Do not add dependencies. Scorer is stdlib-only — keep it that way.
- Do not touch the rubric to improve the metric. That is goodhart cheating. If the rubric feels wrong, stop the loop and fix the rubric manually.
- If a trial crashes from a trivial error in the prompt (malformed YAML example, broken code fence), fix in place and re-run ONCE before deciding.

## Stopping criteria summary

Stop when ANY of these hit:
- 12 total trials (each = 3 averaged runs)
- 3 hours wall-clock
- 4 consecutive no-improvement trials
- Metric mean reaches 0.85 (high-enough; diminishing returns above this point)
- User interrupts

## Cost note

Each trial spawns RUNS_PER_TRIAL (=3) headless Claude runs with web search. Expect ~5–15 minutes and ~$1.50–$6 per trial. 12 trials ≈ 1–3 hr wall-clock, ~$20–$70 in API cost.
