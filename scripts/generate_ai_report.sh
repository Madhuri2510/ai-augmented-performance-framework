#!/usr/bin/env bash
set -euo pipefail

echo "🧠 Installing Python dependencies..."
python -m pip install -r ai-engine/requirements.txt

echo "🧪 Detecting anomalies..."
python ai-engine/anomaly_detection.py

echo "📝 Generating AI insights..."
python ai-engine/insights_generator.py

echo "✅ AI report generated in results/analysis"
