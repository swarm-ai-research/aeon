import fs from "node:fs";

const TRACKED = [
  "notegraph", "suggest-edges", "weekly-shiplog", "changelog",
  "code-health", "compute-futures-eda", "compute-pulse",
  "compute-macro-correlate", "runpod-spot-pricing", "surplus-pulse",
];
const ALLOWED_AUTHORS = new Set(["aeonframework"]);
const DATE_RE = /^(\d{4}-\d{2}-\d{2})$/;

const prs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const groups = {};

const nonTracked = [];
const authorRejected = [];
const nonDate = [];

for (const pr of prs) {
  const [prefix, ...rest] = pr.headRefName.split("/");
  if (!TRACKED.includes(prefix)) { nonTracked.push({ n: pr.number, b: pr.headRefName }); continue; }
  if (!ALLOWED_AUTHORS.has(pr.author.login)) { authorRejected.push({ n: pr.number, b: pr.headRefName, a: pr.author.login }); continue; }
  const m = rest.join("/").match(DATE_RE);
  if (!m) { nonDate.push({ n: pr.number, b: pr.headRefName }); continue; }
  (groups[prefix] ||= []).push({ ...pr, branchDate: m[1] });
}

const stale = [];
for (const [prefix, list] of Object.entries(groups)) {
  list.sort((a, b) => b.branchDate.localeCompare(a.branchDate));
  const [survivor, ...rest] = list;
  for (const old of rest) stale.push({ ...old, supersededBy: survivor.number, prefix });
}

console.log(JSON.stringify({
  total_open: prs.length,
  n_tracked_matched: Object.values(groups).reduce((a, g) => a + g.length, 0),
  n_groups: Object.keys(groups).length,
  n_non_tracked_prefix: nonTracked.length,
  n_author_rejected: authorRejected.length,
  n_non_date_suffix: nonDate.length,
  groups,
  stale,
  author_rejected_sample: authorRejected.slice(0, 5),
  non_tracked_sample: nonTracked.slice(0, 5),
}, null, 2));
