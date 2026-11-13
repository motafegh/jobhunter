#!/usr/bin/env bash
# Persist one bounded local LM Studio source-bound translation attempt.
# Never commit the private evidence directory, raw translation or model logs.
set -u -o pipefail

if [ "$#" -ne 5 ]; then
  echo "usage: bash scripts/run_p16_source_bound_trial_v1.sh <database> <job-id> <source-span-id> <model-id> <ignored-output-directory>" >&2
  exit 2
fi

database="$1"
job="$2"
span="$3"
model="$4"
out="$5"
case "$out" in
  data/local-acceptance/*) ;;
  *) echo "refusing a private output outside data/local-acceptance/" >&2; exit 2 ;;
esac

if [ ! -f AGENTS.md ] || [ ! -f scripts/translate_p16_original_span_v1.py ]; then
  echo "run from the JobHunter repository root" >&2
  exit 2
fi
if [ ! -x .venv/bin/python ]; then
  echo "JobHunter virtual environment not found" >&2
  exit 2
fi

record="$out/PRIVATE_TRANSLATION_$job.json"
status="$out/TRANSLATION_$job.status"
log="$out/TRANSLATION_$job.log"
if [ -e "$record" ] || [ -e "$status" ] || [ -e "$log" ]; then
  echo "refusing to overwrite retained trial evidence" >&2
  exit 2
fi
mkdir -p "$out"

start=$(date +%s)
timeout 180 .venv/bin/python scripts/translate_p16_original_span_v1.py \
  --database "$database" --job "$job" --span "$span" \
  --model "$model" --base-url http://127.0.0.1:18080/v1 \
  --out "$record" > "$log" 2>&1
rc="$?"
duration="$(( $(date +%s) - start ))"
printf 'source_job_id=%s\nspan_id=%s\nmodel=%s\nexit_code=%s\nelapsed_seconds=%s\n' \
  "$job" "$span" "$model" "$rc" "$duration" > "$status"

echo "source_bound_trial_job=$job"
echo "exit_code=$rc"
echo "duration_seconds=$duration"
echo "private_status=$status"
echo "private_log=$log"
if [ "$rc" -eq 0 ]; then
  echo "private_candidate=$record"
fi
exit "$rc"
