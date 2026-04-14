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
PER_TRIAL_TIMEOUT="${PER_TRIAL_TIMEOUT:-600}"

[[ -f "${SOURCE_FILE}" ]] || { echo "fixture missing: ${SOURCE_FILE}" >&2; exit 12; }
[[ -f "skills/wiki-ingest/SKILL.md" ]] || { echo "skills/wiki-ingest/SKILL.md missing" >&2; exit 13; }

# Clean scratch wiki (keep the parent .autoresearch for results.tsv)
rm -rf "${SCRATCH}"
mkdir -p "${SCRATCH}/wiki"/{concepts,entities,sources,comparisons,questions}

PROMPT=$(cat <<PROMPT_EOF
You are running an eval trial. Do not ask questions. Work autonomously.

Task: Ingest a source document into a scratch wiki, following the current protocol in skills/wiki-ingest/SKILL.md exactly as written.

Source: ${SOURCE_FILE}
Scratch wiki root: ${SCRATCH}/wiki/

Meta-rules (scratch harness only, not ingestion guidance):
- Read skills/wiki-ingest/SKILL.md end-to-end and follow it.
- Write every new page under ${SCRATCH}/wiki/ (the concepts/, entities/, sources/, comparisons/, questions/ subdirectories already exist). Treat ${SCRATCH}/wiki/ as the wiki root for this session.
- Do NOT read, modify, or link to the main wiki/ directory.
- Do NOT update any index.md or log.md.
- Do NOT ask for confirmation.
- When done, print exactly: TRIAL_DONE
PROMPT_EOF
)

# Run headless claude with a portable timeout (perl alarm). macOS has no `timeout` by default.
TRIAL_LOG="${SCRATCH}/trial.log"
run_with_timeout() {
    local secs="$1"; shift
    perl -e '
        my $secs = shift @ARGV;
        my $pid = fork();
        if ($pid == 0) { exec @ARGV; exit 127; }
        local $SIG{ALRM} = sub { kill "TERM", $pid; sleep 2; kill "KILL", $pid; exit 124; };
        alarm $secs;
        waitpid $pid, 0;
        exit($? >> 8);
    ' "$secs" "$@"
}
set +e
run_with_timeout "${PER_TRIAL_TIMEOUT}" \
    "${CLAUDE_BIN}" -p "${PROMPT}" \
    --permission-mode acceptEdits \
    --allowedTools "Read Write Edit Glob Grep Bash WebSearch WebFetch" \
    --output-format json \
    --max-budget-usd 3 \
    > "${TRIAL_LOG}" 2>&1
rc=$?
set -e
if [[ "$rc" -ne 0 ]]; then
    if [[ "$rc" -eq 124 ]]; then
        echo "claude headless invocation timed out after ${PER_TRIAL_TIMEOUT}s (see ${TRIAL_LOG})" >&2
    else
        echo "claude headless invocation failed rc=${rc} (see ${TRIAL_LOG})" >&2
    fi
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
