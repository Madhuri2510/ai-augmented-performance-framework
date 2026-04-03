# 🚀 AI-Augmented Performance Testing Framework

A portfolio-ready framework that demonstrates how a **QA Test Manager / Performance Test Architect** can design, run, and explain realistic load tests against a real web application.

This framework includes:
- **k6 performance testing** against `https://test.k6.io` (real public app)
- Multiple scenario types used in enterprise performance engineering
- **Automated analysis** (SLO checks, anomaly detection, trend insights)
- **AI-generated executive summary** using OpenAI (optional, key-based)
- CI-ready workflow for repeatable test evidence

---

## ✅ Scenarios Included

Each scenario maps to a common non-functional testing objective:

1. **Smoke / Baseline** – quick health and basic latency check
2. **Load** – expected peak traffic profile
3. **Stress** – beyond expected peak to identify degradation behavior
4. **Spike** – sudden traffic surge and recovery validation
5. **Soak** – endurance run for stability / memory leak indicators
6. **Breakpoint** – incremental ramp to discover system limits

All scripts hit a real app (`https://test.k6.io`) and validate response status + latency thresholds.

---

## 🧠 AI Capabilities

The AI pipeline performs:
- Statistical anomaly detection on latency/error series
- SLO pass/fail evaluation
- Scenario ranking by risk
- LLM-generated management summary (if `OPENAI_API_KEY` is provided)

Output artifacts:
- `results/analysis/anomalies.csv`
- `results/analysis/analysis_report.json`
- `results/analysis/ai_executive_summary.md`

---

## 📁 Project Structure

```text
load-tests/
  scenarios/
    smoke.js
    load.js
    stress.js
    spike.js
    soak.js
    breakpoint.js
ai-engine/
  anomaly_detection.py
  insights_generator.py
scripts/
  run_test.sh
  run_all_scenarios.sh
  generate_ai_report.sh
config/
  config.json
```

---

## ⚙️ Prerequisites

- k6
- Python 3.10+
- pip
- (Optional) `OPENAI_API_KEY` for LLM executive summary

---

## ▶️ Quick Start

Run one scenario:

```bash
bash scripts/run_test.sh load
```

Run all scenarios:

```bash
bash scripts/run_all_scenarios.sh
```

Generate analysis after tests:

```bash
bash scripts/generate_ai_report.sh
```

---

## 📊 Design Notes for Interview/Portfolio Use

This repo intentionally demonstrates how to:
- Separate **test execution** from **analysis/reporting**
- Drive repeatability via configuration
- Keep scenario scripts small and purpose-specific
- Translate technical metrics into business-facing summaries

---

## 🔐 Safety

- Public target app only (`test.k6.io`)
- No destructive API behavior
- No secrets committed

