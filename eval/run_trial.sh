#!/usr/bin/env bash
# Run a single ingestion trial for karpathy-autoresearch.
#
# 1. Spins up a scratch wiki directory
# 2. Invokes headless Claude to ingest the fixture source into it,
#    following the current skills/wiki-ingest/SKILL.md
# 3. Scores the result with ingest_eval.py
# 4. Emits JSON: {"metric": 0.xyz, "components": {...}, "pages": N}
#
# Usage:
#   eval/run_trial.sh [fixture_name]            # default: claude-code-mistakes
#   eval/run_trial.sh claude-code-mistakes
#
# Env vars:
#   TRIAL_SCRATCH        override scratch dir (default: .autoresearch/scratch)
#   CLAUDE_BIN           override claude binary (default: claude)
#   PER_TRIAL_TIMEOUT    wall-clock seconds (default: 300)
#
# Exit codes:
#   0 success, JSON on stdout
#   10 claude headless invocation failed or timed out
#   11 scorer failed
#   12 fixture missing
#   13 wiki-ingest skill missing
set -euo pipefail

FIXTURE_NAME="${1:-claude-code-mistakes}"
FIXTURE_DIR="eval/fixtures/${FIXTURE_NAME}"
SOURCE_FILE="${FIXTURE_DIR}/source.md"
SCRATCH="${TRIAL_SCRATCH:-.autoresearch/scratch}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
PER_TRIAL_TIMEOUT="${PER_TRIAL_TIMEOUT:-300}"

[[ -f "${SOURCE_FILE}" ]] || { echo "fixture missing: ${SOURCE_FILE}" >&2; exit 12; }
[[ -f "skills/wiki-ingest/SKILL.md" ]] || { echo "skills/wiki-ingest/SKILL.md missing" >&2; exit 13; }

# Clean scratch wiki (keep the parent .autoresearch for results.tsv)
rm -rf "${SCRATCH}"
mkdir -p "${SCRATCH}/wiki"/{concepts,entities,sources,comparisons,questions}

PROMPT=$(cat <<PROMPT_EOF
You are running an eval trial. Do not ask questions. Work autonomously.

Task: Ingest the following source document into the scratch wiki at ${SCRATCH}/wiki/, following the ingestion protocol in skills/wiki-ingest/SKILL.md.

Source: ${SOURCE_FILE}

Rules:
- Read skills/wiki-ingest/SKILL.md end-to-end before starting.
- Write ALL new pages under ${SCRATCH}/wiki/ (concepts/, entities/, sources/, etc.). The subdirectories already exist.
- Do NOT read or modify the main wiki/ directory.
- Do NOT update any index.md or log.md.
- Do NOT ask for confirmation.
- Frontmatter must include: type, title, created, updated, tags (both created and updated are required).
- For every author, handle, or notable person cited in the source: create an entity page with researched content (≥80 words). You may use WebSearch/WebFetch to research them.
- Target concept granularity: distilled sub-topics, not one page per section and not one umbrella page. Aim for 3–6 concept pages on a source of this size.
- When done, print exactly: TRIAL_DONE
PROMPT_EOF
)

# Run headless claude with timeout. Capture stderr separately.
TRIAL_LOG="${SCRATCH}/trial.log"
if ! timeout "${PER_TRIAL_TIMEOUT}" "${CLAUDE_BIN}" -p "${PROMPT}" > "${TRIAL_LOG}" 2>&1; then
    echo "claude headless invocation failed or timed out (see ${TRIAL_LOG})" >&2
    exit 10
fi

# Score it
if ! python3 eval/ingest_eval.py \
    --wiki "${SCRATCH}/wiki" \
    --rubric eval/rubric.json \
    --fixture "${FIXTURE_DIR}" \
    --json; then
    echo "scorer failed" >&2
    exit 11
fi
