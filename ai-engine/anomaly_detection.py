from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path('results/raw')
OUT_DIR = Path('results/analysis')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _flatten_sample(sample: dict) -> dict:
    data = sample.get('data', {})
    point = data.get('point', {})
    tags = data.get('tags', {})
    return {
        'metric': data.get('metric'),
        'time': data.get('time'),
        'value': point.get('value'),
        'url': tags.get('url'),
        'status': tags.get('status'),
        'scenario': tags.get('scenario'),
    }


def _load_stream_file(path: Path) -> pd.DataFrame:
    records = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get('type') == 'Point':
                records.append(_flatten_sample(row))

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)
    df = df.dropna(subset=['time', 'value'])
    return df


def detect_latency_anomalies() -> pd.DataFrame:
    stream_files = sorted(RAW_DIR.glob('*_stream.json'))
    if not stream_files:
        print('No k6 stream files found in results/raw')
        return pd.DataFrame()

    frames = []
    for file in stream_files:
        df = _load_stream_file(file)
        if df.empty:
            continue
        df['source_file'] = file.name
        frames.append(df)

    if not frames:
        print('No valid data points found for anomaly detection')
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    latency = combined[combined['metric'] == 'http_req_duration'].copy()

    if latency.empty:
        print('No http_req_duration metric available')
        return pd.DataFrame()

    latency['mean'] = latency['value'].mean()
    latency['std'] = latency['value'].std(ddof=0)
    if latency['std'].iloc[0] == 0:
        latency['z_score'] = 0.0
    else:
        latency['z_score'] = (latency['value'] - latency['mean']) / latency['std']

    anomalies = latency[latency['z_score'] > 3].copy()
    anomalies = anomalies.sort_values('value', ascending=False)

    out_file = OUT_DIR / 'anomalies.csv'
    anomalies.to_csv(out_file, index=False)

    print(f'🚨 Anomalies Found: {len(anomalies)}')
    print(f'Saved: {out_file}')
    return anomalies


if __name__ == '__main__':
    detect_latency_anomalies()
