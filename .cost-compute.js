const fs = require('fs');
const csv = fs.readFileSync('memory/token-usage.csv', 'utf8').trim().split('\n');
const rows = csv.slice(1);

const TODAY = '2026-07-27';
const N = 7;
const CUTOFF = '2026-07-20';
const PRIOR_CUTOFF = '2026-07-13';

// Direct Anthropic pricing (per million tokens)
const PRICING = {
  'claude-opus-4-7':           { input: 15.00, output: 75.00, cache_read: 1.50,  cache_write: 18.75 },
  'claude-sonnet-4-6':         { input:  3.00, output: 15.00, cache_read: 0.30,  cache_write:  3.75 },
  'claude-haiku-4-5-20251001': { input:  0.80, output:  4.00, cache_read: 0.08,  cache_write:  1.00 },
};

let csv_malformed = 0;
let csv_ok = 0;
const inWindow = [];
const priorWindow = [];
const unknownModels = {};

for (const line of rows) {
  if (!line.trim()) continue;
  const parts = line.split(',');
  if (parts.length < 7) { csv_malformed++; continue; }
  const [date, skill, model] = parts;
  const input_tokens   = parseInt(parts[3]);
  const output_tokens  = parseInt(parts[4]);
  const cache_read     = parseInt(parts[5]);
  const cache_creation = parseInt(parts[6]);
  if (isNaN(input_tokens) || isNaN(output_tokens)) { csv_malformed++; continue; }

  let rates = PRICING[model];
  let is_unknown = false;
  if (!rates) {
    is_unknown = true;
    rates = PRICING['claude-opus-4-7'];
    if (!unknownModels[model]) unknownModels[model] = { input: 0, output: 0 };
    unknownModels[model].input  += input_tokens;
    unknownModels[model].output += output_tokens;
  }

  const row_cost = (input_tokens   / 1e6 * rates.input)
                 + (output_tokens  / 1e6 * rates.output)
                 + (cache_read     / 1e6 * rates.cache_read)
                 + (cache_creation / 1e6 * rates.cache_write);

  const row = { date, skill, model, input_tokens, output_tokens, cache_read, cache_creation,
                row_cost, is_unknown };

  if (date >= CUTOFF && date <= TODAY) { inWindow.push(row); csv_ok++; }
  else if (date >= PRIOR_CUTOFF && date < CUTOFF) { priorWindow.push(row); csv_ok++; }
}

// Core aggregates
const totalCost = inWindow.reduce((s, r) => s + r.row_cost, 0);
const totalRuns = inWindow.length;

// Input/output/cache breakdown
const totalInputCost  = inWindow.reduce((s,r) => {
  const rt = PRICING[r.model] || PRICING['claude-opus-4-7'];
  return s + r.input_tokens/1e6 * rt.input;
}, 0);
const totalOutputCost = inWindow.reduce((s,r) => {
  const rt = PRICING[r.model] || PRICING['claude-opus-4-7'];
  return s + r.output_tokens/1e6 * rt.output;
}, 0);
const totalCRCost = inWindow.reduce((s,r) => {
  const rt = PRICING[r.model] || PRICING['claude-opus-4-7'];
  return s + r.cache_read/1e6 * rt.cache_read;
}, 0);
const totalCWCost = inWindow.reduce((s,r) => {
  const rt = PRICING[r.model] || PRICING['claude-opus-4-7'];
  return s + r.cache_creation/1e6 * rt.cache_write;
}, 0);

// Per-skill
const skillMap = {};
for (const r of inWindow) {
  if (!skillMap[r.skill]) skillMap[r.skill] = { runs: 0, tokens: 0, cost: 0 };
  skillMap[r.skill].runs++;
  skillMap[r.skill].tokens += r.input_tokens + r.output_tokens;
  skillMap[r.skill].cost   += r.row_cost;
}
const topSkills = Object.entries(skillMap).sort((a,b) => b[1].cost - a[1].cost).slice(0,10);

// Per-model
const modelMap = {};
for (const r of inWindow) {
  if (!modelMap[r.model]) modelMap[r.model] = { runs: 0, tokens: 0, cost: 0 };
  modelMap[r.model].runs++;
  modelMap[r.model].tokens += r.input_tokens + r.output_tokens;
  modelMap[r.model].cost   += r.row_cost;
}

// Prior window total
const priorTotal = priorWindow.reduce((s, r) => s + r.row_cost, 0);
const hasPrior   = priorWindow.length > 0;
const wowDelta   = (hasPrior && priorTotal > 0)
  ? ((totalCost - priorTotal) / priorTotal * 100)
  : null;

// Burn forecast
const dailyAvg    = totalCost / N;
const projMonthly = dailyAvg * 30;

// Anomaly detection: per (skill, model) with >= 3 runs
const smMap = {};
for (const r of inWindow) {
  const key = r.skill + '|' + r.model;
  if (!smMap[key]) smMap[key] = [];
  smMap[key].push(r);
}
const anomalies = [];
for (const [key, runs] of Object.entries(smMap)) {
  if (runs.length < 3) continue;
  const costs = runs.map(r => r.row_cost);
  const mu = costs.reduce((a,b) => a+b, 0) / costs.length;
  const sigma = Math.sqrt(costs.reduce((a,c) => a + (c-mu)**2, 0) / costs.length);
  for (const r of runs) {
    if (r.row_cost > mu + 2*sigma && r.row_cost > 0.10) {
      anomalies.push({
        skill: r.skill, model: r.model, date: r.date,
        cost: r.row_cost, mu, sigma,
        input: r.input_tokens, output: r.output_tokens, cache_write: r.cache_creation
      });
    }
  }
}

// Skill WoW spike (>=2x prior, prior >= $0.25)
const priorSkillMap = {};
for (const r of priorWindow) {
  if (!priorSkillMap[r.skill]) priorSkillMap[r.skill] = 0;
  priorSkillMap[r.skill] += r.row_cost;
}
const skillSpikes = [];
for (const [sk, data] of Object.entries(skillMap)) {
  const prior = priorSkillMap[sk] || 0;
  if (prior >= 0.25 && data.cost >= 2 * prior) {
    skillSpikes.push({ skill: sk, thisCost: data.cost, priorCost: prior, ratio: data.cost / prior });
  }
}

// Optimization: model downgrade (opus, output/input < 0.3, avg cost > 0.25)
const opusSkillMap = {};
for (const r of inWindow) {
  if (r.model !== 'claude-opus-4-7') continue;
  if (!opusSkillMap[r.skill]) opusSkillMap[r.skill] = { runs: 0, totalCost: 0, totalInput: 0, totalOutput: 0 };
  const o = opusSkillMap[r.skill];
  o.runs++;
  o.totalCost   += r.row_cost;
  o.totalInput  += r.input_tokens;
  o.totalOutput += r.output_tokens;
}
const downgradeOpts = Object.entries(opusSkillMap).filter(([sk, o]) => {
  const avgCost = o.totalCost / o.runs;
  const ratio   = o.totalOutput / Math.max(o.totalInput, 1);
  return ratio < 0.3 && avgCost > 0.25;
}).map(([sk, o]) => {
  // Savings: weighted avg input+output rate comparison (simplified)
  const opusAvg   = (PRICING['claude-opus-4-7'].input + PRICING['claude-opus-4-7'].output) / 2;
  const sonnetAvg = (PRICING['claude-sonnet-4-6'].input + PRICING['claude-sonnet-4-6'].output) / 2;
  const weekSavings = o.totalCost * (1 - sonnetAvg / opusAvg);
  return { skill: sk, avgCost: o.totalCost / o.runs, ratio: o.totalOutput / Math.max(o.totalInput, 1),
           weekSavings, totalCost: o.totalCost };
}).sort((a,b) => b.weekSavings - a.weekSavings).slice(0,3);

// Optimization: cache underuse (direct gateway, cache_read/(cache_read+input) < 0.2, avg cost > $0.10)
const cacheUnderuse = Object.entries(skillMap).filter(([sk, data]) => {
  const skRows = inWindow.filter(r => r.skill === sk);
  const totalCR = skRows.reduce((s,r) => s + r.cache_read, 0);
  const totalIN = skRows.reduce((s,r) => s + r.input_tokens, 0);
  const ratio = totalCR / Math.max(totalCR + totalIN, 1);
  return ratio < 0.2 && (data.cost / data.runs) > 0.10;
}).map(([sk, data]) => {
  const skRows = inWindow.filter(r => r.skill === sk);
  const totalCR = skRows.reduce((s,r) => s + r.cache_read, 0);
  const totalIN = skRows.reduce((s,r) => s + r.input_tokens, 0);
  const ratio = totalCR / Math.max(totalCR + totalIN, 1);
  // If 50% of input became cache_read (10x cheaper), estimate savings
  const opusRate  = PRICING['claude-opus-4-7'];
  const savePer1M = opusRate.input - opusRate.cache_read;
  const weekSavings = (totalIN * 0.5) / 1e6 * savePer1M;
  return { skill: sk, cacheRatio: ratio, avgCost: data.cost / data.runs, weekSavings };
}).sort((a,b) => b.weekSavings - a.weekSavings).slice(0,2);

// Long-tail waste (>10 runs, avg cost/run < $0.01)
const longTail = Object.entries(skillMap)
  .filter(([sk, d]) => d.runs > 10 && d.cost/d.runs < 0.01)
  .map(([sk, d]) => ({ skill: sk, runs: d.runs, avgCost: d.cost/d.runs }));

const result = {
  totalCost, totalRuns, dailyAvg, projMonthly,
  totalInputCost, totalOutputCost, totalCRCost, totalCWCost,
  priorTotal, hasPrior, wowDelta,
  topSkills,
  modelMap,
  anomalies, skillSpikes,
  downgradeOpts,
  cacheUnderuse,
  longTail,
  unknownModels,
  csv_ok, csv_malformed,
  inWindowCount: inWindow.length,
  priorCount: priorWindow.length
};

process.stdout.write(JSON.stringify(result, null, 2) + '\n');
