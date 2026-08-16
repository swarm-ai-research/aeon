import fs from 'node:fs';
process.chdir('/home/runner/work/aeon/aeon');

// Load parser output
const summary = JSON.parse(fs.readFileSync('tmp-skill-graph/result.json', 'utf8'));
const state = summary.state;

// Re-run parser inline to inspect list
const { execSync } = await import('node:child_process');
execSync('node tmp-skill-graph/build-graph.mjs > tmp-skill-graph/last-run.json');

// Load parser's enabled set by re-parsing aeon.yml directly
const modUrl = new URL('./build-graph.mjs', 'file:///home/runner/work/aeon/aeon/tmp-skill-graph/').href;

// Simpler: run parser and monkey-print the enabled set
const src = fs.readFileSync('tmp-skill-graph/build-graph.mjs', 'utf8');
const patched = src.replace('console.log(JSON.stringify(summary));', 'console.log(JSON.stringify({ enabled: result.slugs.filter(s => require_aeon.skills[s]?.enabled) }));');
fs.writeFileSync('tmp-skill-graph/probe.mjs', patched.replace('const aeon = parseAeon();', 'const aeon = parseAeon(); globalThis.require_aeon = aeon;'));
