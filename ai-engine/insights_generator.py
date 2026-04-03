from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI

RAW_DIR = Path('results/raw')
OUT_DIR = Path('results/analysis')
CFG_FILE = Path('config/config.json')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def _safe_metric(summary: dict[str, Any], key: str, default: float = 0.0) -> float:
    metric = summary.get('metrics', {}).get(key, {})
    values = metric.get('values', {})
    for candidate in ('value', 'rate', 'avg'):
        if candidate in values and values[candidate] is not None:
            return float(values[candidate])
    return default


def _scenario_snapshot(summary_file: Path, slo: dict[str, float]) -> dict[str, Any]:
    data = _read_json(summary_file)

    duration_avg = _safe_metric(data, 'http_req_duration', 0.0)
    p95 = float(data.get('metrics', {}).get('http_req_duration', {}).get('values', {}).get('p(95)', 0.0))
    err_rate = float(data.get('metrics', {}).get('http_req_failed', {}).get('values', {}).get('rate', 0.0))
    rps = _safe_metric(data, 'http_reqs', 0.0)

    return {
        'scenario': summary_file.name.replace('_summary.json', ''),
        'avg_ms': round(duration_avg, 2),
        'p95_ms': round(p95, 2),
        'error_rate': round(err_rate, 4),
        'requests_per_sec': round(rps, 2),
        'slo_pass': bool(p95 <= slo['p95_ms'] and err_rate <= slo['error_rate']),
    }


def _build_report() -> dict[str, Any]:
    cfg = _read_json(CFG_FILE)
    slo = cfg['slo']

    summary_files = sorted(RAW_DIR.glob('*_summary.json'))
    snapshots = [_scenario_snapshot(f, slo) for f in summary_files]

    high_risk = sorted(
        snapshots,
        key=lambda s: (not s['slo_pass'], s['error_rate'], s['p95_ms']),
        reverse=True,
    )

    report = {
        'environment': cfg.get('environment', 'unknown'),
        'base_url': cfg.get('base_url', ''),
        'slo': slo,
        'scenario_results': snapshots,
        'highest_risk_scenarios': high_risk[:3],
    }

    with (OUT_DIR / 'analysis_report.json').open('w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    return report


def _generate_with_llm(report: dict[str, Any]) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return (
            '# AI Executive Summary (Fallback)\n\n'
            'OPENAI_API_KEY not set.\n\n'
            f"Scenarios analyzed: {len(report['scenario_results'])}. "
            'Review `analysis_report.json` and `anomalies.csv` for details.'
        )

    client = OpenAI(api_key=api_key)

    prompt = (
        'You are a principal performance architect. '\
        'Write an executive summary for non-technical leadership. '\
        'Include: health status, top risks, bottleneck hypotheses, and prioritized actions. '\
        f'Input data: {json.dumps(report)}'
    )

    response = client.responses.create(
        model='gpt-4.1-mini',
        input=prompt,
        temperature=0.2,
    )
    return response.output_text


def generate_insights() -> None:
    report = _build_report()
    narrative = _generate_with_llm(report)

    out_file = OUT_DIR / 'ai_executive_summary.md'
    out_file.write_text(narrative, encoding='utf-8')

    print(f'✅ Analysis JSON: {OUT_DIR / "analysis_report.json"}')
    print(f'✅ Executive summary: {out_file}')


if __name__ == '__main__':
    generate_insights()
