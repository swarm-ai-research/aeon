import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const prevRaw = execFileSync('git', ['show', 'HEAD:notegraph.json'], { maxBuffer: 200 * 1024 * 1024, encoding: 'utf8' });
const prev = JSON.parse(prevRaw);
const curr = JSON.parse(readFileSync('notegraph.json', 'utf8'));

const p = prev.stats, c = curr.stats;
const node_delta = c.nodes - p.nodes;
const edge_delta = c.edges - p.edges;
const hard_delta = (c.hard||0) - (p.hard||0);
const soft_delta = (c.soft||0) - (p.soft||0);
const orphan_delta = (c.orphans||0) - (p.orphans||0);
const bundled_delta = (c.bundled||0) - (p.bundled||0);
const atomic_delta = (c.atomic||0) - (p.atomic||0);

const prevOrphans = new Set((prev.nodes||[]).filter(n => (n.inDegree||0)===0 && (n.outDegree||0)===0).map(n => n.id));
const currOrphans = new Set((curr.nodes||[]).filter(n => (n.inDegree||0)===0 && (n.outDegree||0)===0).map(n => n.id));
const new_orphans = [...currOrphans].filter(x => !prevOrphans.has(x));
const resolved_orphans = [...prevOrphans].filter(x => !currOrphans.has(x));

const prevBundled = new Set((prev.nodes||[]).filter(n => n.bundled).map(n => n.id));
const currBundled = new Set((curr.nodes||[]).filter(n => n.bundled).map(n => n.id));
const new_bundled = [...currBundled].filter(x => !prevBundled.has(x));
const resolved_bundled = [...prevBundled].filter(x => !currBundled.has(x));

let verdict;
if (new_bundled.length > 0) verdict = `${new_bundled.length} new bundled note(s): ${new_bundled[0]}…`;
else if (new_orphans.length > 0) verdict = `${new_orphans.length} new orphan(s): ${new_orphans[0]}…`;
else if (node_delta > 0 && orphan_delta <= 0 && bundled_delta <= 0) verdict = `+${node_delta} notes wired in`;
else if (edge_delta > 10) verdict = `+${edge_delta} new edges`;
else verdict = `graph refreshed (${c.nodes}n / ${c.edges}e / ${c.bundled}b)`;

const out = {
  prev_stats: p,
  curr_stats: c,
  deltas: { node_delta, edge_delta, hard_delta, soft_delta, orphan_delta, bundled_delta, atomic_delta },
  new_orphans, resolved_orphans, new_bundled, resolved_bundled,
  verdict
};
writeFileSync('.notegraph_delta.json', JSON.stringify(out, null, 2));
console.log(JSON.stringify(out, null, 2));
