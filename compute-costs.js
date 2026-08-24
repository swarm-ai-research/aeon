const fs = require('fs');
const csv = fs.readFileSync('memory/token-usage.csv', 'utf8');
const lines = csv.trim().split('\n');
const rows = lines.slice(1);

const pricing = {
  'claude-opus-4-7':           { input: 15.00, output: 75.00, cache_read: 1.50,  cache_write: 18.75 },
  'claude-sonnet-4-6':         { input: 3.00,  output: 15.00, cache_read: 0.30,  cache_write: 3.75  },
  'claude-haiku-4-5-20251001': { input: 0.80,  output: 4.00,  cache_read: 0.08,  cache_write: 1.00  },
};

const today = new Date('2026-08-24');
const cutoff = new Date(today); cutoff.setDate(cutoff.getDate() - 7);
const priorCutoff = new Date(today); priorCutoff.setDate(priorCutoff.getDate() - 14);

let malformed = 0;
let inWindow = [];
let priorWindow = [];
let unknownModels = {};

for (const line of rows) {
  const parts = line.split(',');
  if (parts.length < 7) { malformed++; continue; }
  const [date, skill, model, inp, out, cread, cwrite] = parts;
  const d = new Date(date);
  if (isNaN(d)) { malformed++; continue; }
  const input_tokens = parseInt(inp, 10);
  const output_tokens = parseInt(out, 10);
  const cache_read = parseInt(cread, 10);
  const cache_creation = parseInt(cwrite, 10);
  if (isNaN(input_tokens) || isNaN(output_tokens) || isNaN(cache_read) || isNaN(cache_creation)) { malformed++; continue; }

  let rates = pricing[model];
  let isUnknown = false;
  if (!rates) {
    rates = pricing['claude-opus-4-7'];
    isUnknown = true;
    unknownModels[model] = (unknownModels[model] || 0) + input_tokens + output_tokens + cache_read + cache_creation;
  }

  const input_cost       = input_tokens    / 1e6 * rates.input;
  const output_cost      = output_tokens   / 1e6 * rates.output;
  const cache_read_cost  = cache_read      / 1e6 * rates.cache_read;
  const cache_write_cost = cache_creation  / 1e6 * rates.cache_write;
  const row_cost         = input_cost + output_cost + cache_read_cost + cache_write_cost;

  const row = { date, skill, model, input_tokens, output_tokens, cache_read, cache_creation, input_cost, output_cost, cache_read_cost, cache_write_cost, row_cost, isUnknown };

  if (d >= cutoff && d <= today) inWindow.push(row);
  else if (d >= priorCutoff && d < cutoff) priorWindow.push(row);
}

function aggregate(rows) {
  let total = 0, totalInput = 0, totalOutput = 0, totalCacheRead = 0, totalCacheWrite = 0;
  const bySkill = {};
  const byModel = {};
  for (const r of rows) {
    total += r.row_cost;
    totalInput += r.input_cost;
    totalOutput += r.output_cost;
    totalCacheRead += r.cache_read_cost;
    totalCacheWrite += r.cache_write_cost;
    if (!bySkill[r.skill]) bySkill[r.skill] = { runs: 0, tokens: 0, cost: 0, rows: [] };
    bySkill[r.skill].runs++;
    bySkill[r.skill].tokens += r.input_tokens + r.output_tokens + r.cache_read + r.cache_creation;
    bySkill[r.skill].cost += r.row_cost;
    bySkill[r.skill].rows.push(r);
    if (!byModel[r.model]) byModel[r.model] = { runs: 0, tokens: 0, cost: 0 };
    byModel[r.model].runs++;
    byModel[r.model].tokens += r.input_tokens + r.output_tokens + r.cache_read + r.cache_creation;
    byModel[r.model].cost += r.row_cost;
  }
  return { total, totalInput, totalOutput, totalCacheRead, totalCacheWrite, bySkill, byModel };
}

const win = aggregate(inWindow);
const prior = aggregate(priorWindow);

const pairs = {};
for (const r of inWindow) {
  const key = r.skill + '|' + r.model;
  if (!pairs[key]) pairs[key] = [];
  pairs[key].push(r);
}
const anomalies = [];
for (const [key, prows] of Object.entries(pairs)) {
  if (prows.length < 3) continue;
  const costs = prows.map(r => r.row_cost);
  const mu = costs.reduce((a,b) => a+b, 0) / costs.length;
  const sigma = Math.sqrt(costs.map(c => (c-mu)**2).reduce((a,b) => a+b, 0) / costs.length);
  for (const r of prows) {
    if (r.row_cost > mu + 2*sigma && r.row_cost > 0.10) {
      anomalies.push({ skill: r.skill, model: r.model, when: r.date, cost: r.row_cost, mu, sigma,
        why: 'inp=' + r.input_tokens + '/out=' + r.output_tokens + '/cw=' + r.cache_creation });
    }
  }
}

const skillSpikes = [];
for (const [skill, data] of Object.entries(win.bySkill)) {
  const priorData = prior.bySkill[skill];
  if (priorData && priorData.cost >= 0.25 && data.cost >= 2 * priorData.cost) {
    skillSpikes.push({ skill, thisWindow: data.cost, priorWindow: priorData.cost, ratio: data.cost / priorData.cost });
  }
}

const downgradeOpts = [];
for (const [skill, data] of Object.entries(win.bySkill)) {
  const opusRows = data.rows.filter(r => r.model === 'claude-opus-4-7');
  if (opusRows.length < 1) continue;
  const ratios = opusRows.map(r => r.output_tokens / Math.max(r.input_tokens, 1));
  const avgRatio = ratios.reduce((a,b) => a+b, 0) / ratios.length;
  const avgCost = opusRows.reduce((a,r) => a + r.row_cost, 0) / opusRows.length;
  if (avgRatio < 0.3 && avgCost > 0.25) {
    const opusCost = opusRows.reduce((a,r) => a + r.row_cost, 0);
    const savings = opusCost * 0.6;
    downgradeOpts.push({ skill, avgRatio: avgRatio.toFixed(3), avgCost: avgCost.toFixed(4), opusCost: opusCost.toFixed(4), estSavings: savings.toFixed(4) });
  }
}

const cacheOpts = [];
for (const [skill, data] of Object.entries(win.bySkill)) {
  const totalCacheRead = data.rows.reduce((a,r) => a + r.cache_read, 0);
  const totalInput = data.rows.reduce((a,r) => a + r.input_tokens, 0);
  const ratio = totalCacheRead / (totalCacheRead + totalInput);
  const avgCost = data.cost / data.runs;
  if (ratio < 0.2 && avgCost > 0.10 && data.runs >= 2) {
    cacheOpts.push({ skill, cacheRatio: ratio.toFixed(3), avgCost: avgCost.toFixed(4), cost: data.cost.toFixed(4) });
  }
}

const topSkills = Object.entries(win.bySkill).map(([skill, d]) => ({
  skill, runs: d.runs, tokens: d.tokens, cost: d.cost, avgPerRun: d.cost / d.runs
})).sort((a,b) => b.cost - a.cost);

const result = {
  window: { start: cutoff.toISOString().slice(0,10), end: '2026-08-24', rows: inWindow.length, malformed },
  priorWindow: { start: priorCutoff.toISOString().slice(0,10), end: cutoff.toISOString().slice(0,10), rows: priorWindow.length },
  total: win.total,
  totalInput: win.totalInput,
  totalOutput: win.totalOutput,
  totalCacheRead: win.totalCacheRead,
  totalCacheWrite: win.totalCacheWrite,
  priorTotal: prior.total,
  topSkills: topSkills.slice(0,10),
  byModel: win.byModel,
  anomalies,
  skillSpikes,
  downgradeOpts,
  cacheOpts,
  unknownModels
};

console.log(JSON.stringify(result, null, 2));
