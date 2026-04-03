#!/usr/bin/env bash
set -euo pipefail

SCENARIO="${1:-load}"
SCRIPT="load-tests/scenarios/${SCENARIO}.js"
SUMMARY="results/raw/${SCENARIO}_summary.json"
STREAM="results/raw/${SCENARIO}_stream.json"

if [[ ! -f "$SCRIPT" ]]; then
  echo "❌ Scenario script not found: $SCRIPT"
  echo "Available scenarios: smoke, load, stress, spike, soak, breakpoint"
  exit 1
fi

mkdir -p results/raw results/analysis

echo "🚀 Running k6 scenario: $SCENARIO"
k6 run "$SCRIPT" \
  --summary-export "$SUMMARY" \
  --out "json=$STREAM"

echo "✅ Scenario completed: $SCENARIO"
echo "   Summary: $SUMMARY"
echo "   Stream:  $STREAM"
