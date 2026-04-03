#!/usr/bin/env bash
set -euo pipefail

SCENARIOS=(smoke load stress spike soak breakpoint)

for s in "${SCENARIOS[@]}"; do
  bash scripts/run_test.sh "$s"
done

echo "✅ All scenarios completed"
