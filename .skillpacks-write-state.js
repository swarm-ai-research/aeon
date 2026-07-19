// Write memory/state/skillpacks.json based on current skillpacks.json + delta output.
import { readFileSync, writeFileSync } from 'node:fs';

const current = JSON.parse(readFileSync('skillpacks.json', 'utf8'));

const packMembership = {};
for (const p of current.packs || []) {
  packMembership[p.slug] = (p.members || []).slice().sort();
}

const state = {
  input_fingerprint: '7a0aeb25f26805aa7cadea73d1f90235c1860008',
  last_run: '2026-07-19',
  stats: current.stats,
  last_verdict: '1 new pack(s): outages-fleet',
  last_pr: 'https://github.com/swarm-ai-research/aeon/pull/new/skillpacks/2026-07-19',
  last_branch: 'skillpacks/2026-07-19',
  pack_membership: packMembership,
};

writeFileSync('memory/state/skillpacks.json', JSON.stringify(state, null, 2) + '\n');
console.log('wrote memory/state/skillpacks.json');
