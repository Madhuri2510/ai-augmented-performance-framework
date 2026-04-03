import { hitHomepage, thresholds } from '../lib/common.js';

const cfg = JSON.parse(open('../../config/config.json'));

export const options = {
  vus: cfg.scenarios.load.vus,
  duration: cfg.scenarios.load.duration,
  thresholds: thresholds(),
};

export default function () {
  hitHomepage();
}
