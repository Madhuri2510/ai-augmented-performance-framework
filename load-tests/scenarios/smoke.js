import { hitHomepage, thresholds } from '../lib/common.js';

const cfg = JSON.parse(open('../../config/config.json'));

export const options = {
  vus: cfg.scenarios.smoke.vus,
  duration: cfg.scenarios.smoke.duration,
  thresholds: thresholds(),
};

export default function () {
  hitHomepage();
}
