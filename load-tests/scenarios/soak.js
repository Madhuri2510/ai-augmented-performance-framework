import { hitHomepage, thresholds } from '../lib/common.js';

const cfg = JSON.parse(open('../../config/config.json'));

export const options = {
  vus: cfg.scenarios.soak.vus,
  duration: cfg.scenarios.soak.duration,
  thresholds: thresholds(),
};

export default function () {
  hitHomepage();
}
