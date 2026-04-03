import { hitHomepage, thresholds } from '../lib/common.js';

const cfg = JSON.parse(open('../../config/config.json'));

export const options = {
  stages: cfg.scenarios.stress.stages,
  thresholds: thresholds(),
};

export default function () {
  hitHomepage();
}
