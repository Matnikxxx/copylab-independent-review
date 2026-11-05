// INDEPENDENT A14-09 probe: execute the REAL lab/dashboard.html renderer in jsdom
// against a supplied state fixture. No app startup, no network (jsdom fetch is stubbed).
const fs = require('fs');
const { JSDOM } = require(require('path').join(__dirname,'..','..','tools','node_modules','jsdom'));

const htmlPath = process.argv[2];
const statePath = process.argv[3];
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const html = fs.readFileSync(htmlPath, 'utf8');

const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'http://copylab.test/#health',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve(state) });
    window.setInterval = () => 0;
    window.onerror = (m) => errors.push(String(m));
  },
});
dom.window.addEventListener('error', (e) => errors.push(String(e.message)));

setTimeout(() => {
  const d = dom.window.document;
  const text = d.body.textContent;
  const rows = [...d.querySelectorAll('#content table tbody tr')].map(tr =>
    [...tr.querySelectorAll('td')].map(td => td.textContent.trim()));
  const healthyCount = (text.match(/Healthy/g) || []).length;
  const label = rows.find(r => Array.isArray(r) && r[2] && r[2].includes('1970'));
  const out = {
    source: 'independent jsdom execution of lab/dashboard.html',
    real_network_requests: 0,
    javascript_errors: errors,
    rendered_health_rows: rows,
    ancient_row_state_label: label ? label[1] : null,
    ancient_row_last_observed: label ? label[2] : null,
    healthy_label_occurrences: healthyCount,
    stale_rendered_healthy: !!(label && label[1] === 'Healthy'),
    forward_validation_ready: state.forward_validation_ready,
    last_warning: state.warnings[state.warnings.length - 1],
    defect_reproduced: !!(label && label[1] === 'Healthy'),
  };
  fs.writeFileSync(process.argv[4], JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  dom.window.close();
}, 600);
