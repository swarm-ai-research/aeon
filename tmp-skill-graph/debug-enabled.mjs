import fs from 'node:fs';
process.chdir('/home/runner/work/aeon/aeon');
const mod = await import('./build-graph.mjs').catch(e => { console.error(e); process.exit(1); });
