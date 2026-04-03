import http from 'k6/http';
import { check, sleep } from 'k6';

const cfg = JSON.parse(open('../../config/config.json'));
const baseUrl = __ENV.BASE_URL || cfg.base_url;

export function thresholds() {
  return cfg.thresholds;
}

export function hitHomepage() {
  const res = http.get(`${baseUrl}/`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'homepage under 1500ms': (r) => r.timings.duration < 1500,
  });

  sleep(1);
}
