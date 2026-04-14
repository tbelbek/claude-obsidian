#!/usr/bin/env bash
# Multi-run averaging wrapper around run_trial.sh.
#
# Runs the single-trial script N times (fresh scratch each time) and emits
# a single JSON line with the MEAN metric and components, plus std and run count.
#
# Usage:
#   eval/run_trial_avg.sh [fixture_name]
#
# Env vars:
#   RUNS_PER_TRIAL   number of runs to average (default: 3)
#   (plus every env var accepted by run_trial.sh)
#
# Output JSON shape:
#   {"metric": <mean>, "metric_std": <stdev>, "runs": N,
#    "components": {<name>: <mean>, ...},
#    "components_std": {<name>: <stdev>, ...},
#    "pages": <mean>, "runs_json": [<per-run JSON>, ...]}
#
# Exit codes:
#   0 success
#   10 at least one underlying run failed (stderr logged; stdout still emits partial summary if >=1 run succeeded)
#   20 all runs failed
set -euo pipefail

FIXTURE_NAME="${1:-claude-code-mistakes}"
RUNS_PER_TRIAL="${RUNS_PER_TRIAL:-3}"

RUN_OUT_DIR="${TRIAL_SCRATCH:-.autoresearch/scratch}/_avg"
mkdir -p "${RUN_OUT_DIR}"

successes=()
for i in $(seq 1 "${RUNS_PER_TRIAL}"); do
    echo "[avg] run ${i}/${RUNS_PER_TRIAL}" >&2
    out_file="${RUN_OUT_DIR}/run_${i}.json"
    if bash eval/run_trial.sh "${FIXTURE_NAME}" > "${out_file}" 2>> "${RUN_OUT_DIR}/run_${i}.err"; then
        successes+=("${out_file}")
    else
        echo "[avg] run ${i} failed; see ${RUN_OUT_DIR}/run_${i}.err" >&2
    fi
done

if [[ "${#successes[@]}" -eq 0 ]]; then
    echo "all ${RUNS_PER_TRIAL} runs failed" >&2
    exit 20
fi

python3 - "${successes[@]}" <<'PY'
import json, statistics, sys

files = sys.argv[1:]
runs = []
for f in files:
    with open(f) as fh:
        # run_trial.sh emits multiple lines (scorer + JSON); JSON is the last
        # non-empty line
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]
        if not lines:
            continue
        try:
            runs.append(json.loads(lines[-1]))
        except json.JSONDecodeError:
            continue

if not runs:
    sys.stderr.write("no parseable runs\n")
    sys.exit(20)

def agg(key_path):
    vals = []
    for r in runs:
        cur = r
        for k in key_path:
            if not isinstance(cur, dict) or k not in cur:
                cur = None
                break
            cur = cur[k]
        if isinstance(cur, (int, float)):
            vals.append(float(cur))
    if not vals:
        return None, None
    mean = sum(vals) / len(vals)
    std = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    return round(mean, 4), round(std, 4)

metric_mean, metric_std = agg(["metric"])
pages_mean, _ = agg(["pages"])

comp_keys = set()
for r in runs:
    comp_keys.update((r.get("components") or {}).keys())

components_mean = {}
components_std = {}
for k in sorted(comp_keys):
    m, s = agg(["components", k])
    components_mean[k] = m
    components_std[k] = s

out = {
    "metric": metric_mean,
    "metric_std": metric_std,
    "runs": len(runs),
    "components": components_mean,
    "components_std": components_std,
    "pages": pages_mean,
    "runs_json": runs,
}
print(json.dumps(out))
PY

# Non-zero exit if any run failed but >=1 succeeded
if [[ "${#successes[@]}" -lt "${RUNS_PER_TRIAL}" ]]; then
    exit 10
fi
