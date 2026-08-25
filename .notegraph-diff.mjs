import { execSync } from 'child_process';
import fs from 'fs';

const cur = JSON.parse(fs.readFileSync('notegraph.json'));
const prevRaw = execSync('git show HEAD:notegraph.json').toString();
const prev = JSON.parse(prevRaw);

const curOrphans = new Set(cur.nodes.filter(n => n.inDegree===0 && n.outDegree===0).map(n => n.id));
const prevOrphans = new Set(prev.nodes.filter(n => n.inDegree===0 && n.outDegree===0).map(n => n.id));
const curBundled = new Set(cur.nodes.filter(n => n.bundled).map(n => n.id));
const prevBundled = new Set(prev.nodes.filter(n => n.bundled).map(n => n.id));

const newOrphans = [...curOrphans].filter(x => !prevOrphans.has(x));
const resolvedOrphans = [...prevOrphans].filter(x => !curOrphans.has(x));
const newBundled = [...curBundled].filter(x => !prevBundled.has(x));
const resolvedBundled = [...prevBundled].filter(x => !curBundled.has(x));

console.log(JSON.stringify({
  prevStats: prev.stats,
  curStats: cur.stats,
  node_delta: cur.stats.nodes - prev.stats.nodes,
  edge_delta: cur.stats.edges - prev.stats.edges,
  orphan_delta: cur.stats.orphans - prev.stats.orphans,
  bundled_delta: cur.stats.bundled - prev.stats.bundled,
  new_orphans: newOrphans,
  resolved_orphans: resolvedOrphans,
  new_bundled: newBundled,
  resolved_bundled: resolvedBundled,
}, null, 2));
