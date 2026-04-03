#!/bin/bash

echo "🧠 Running AI Analysis..."

pip install -r ai-engine/requirements.txt

python ai-engine/anomaly_detection.py
python ai-engine/insights_generator.py

echo "✅ AI Report Generated"