// Compute deltas between current skillpacks.json and HEAD:skillpacks.json
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const current = JSON.parse(readFileSync('skillpacks.json', 'utf8'));
const prevRaw = execSync('git show HEAD:skillpacks.json', { encoding: 'utf8' });
const previous = JSON.parse(prevRaw);

const packsCur = current.packs || [];
const packsPrev = previous.packs || [];

const membershipCur = {};
for (const p of packsCur) {
  membershipCur[p.slug] = (p.members || p.skills || []).map(s => (typeof s === 'string' ? s : s.slug));
}
const membershipPrev = {};
for (const p of packsPrev) {
  membershipPrev[p.slug] = (p.members || p.skills || []).map(s => (typeof s === 'string' ? s : s.slug));
}

const curPackSet = new Set(Object.keys(membershipCur));
const prevPackSet = new Set(Object.keys(membershipPrev));

const new_packs = [...curPackSet].filter(x => !prevPackSet.has(x));
const dropped_packs = [...prevPackSet].filter(x => !curPackSet.has(x));

// Build reverse maps: skill -> pack
const curSkillPack = new Map();
for (const [pk, sks] of Object.entries(membershipCur)) {
  for (const s of sks) curSkillPack.set(s, pk);
}
const prevSkillPack = new Map();
for (const [pk, sks] of Object.entries(membershipPrev)) {
  for (const s of sks) prevSkillPack.set(s, pk);
}

const moved_skills = [];
for (const [s, pk] of curSkillPack.entries()) {
  const prevPk = prevSkillPack.get(s);
  if (prevPk && prevPk !== pk) {
    moved_skills.push({ skill: s, from: prevPk, to: pk });
  }
}

const skill_delta = (current.stats?.skills ?? 0) - (previous.stats?.skills ?? 0);
const pack_delta = (current.stats?.packs ?? 0) - (previous.stats?.packs ?? 0);
const solo_delta = (current.stats?.solos ?? 0) - (previous.stats?.solos ?? 0);
const edges_delta = (current.stats?.edges ?? 0) - (previous.stats?.edges ?? 0);

let verdict = `clustering refreshed (${current.stats.packs}p / ${current.stats.skills}s)`;
if (new_packs.length > 0) {
  verdict = `${new_packs.length} new pack(s): ${new_packs[0]}${new_packs.length > 1 ? '…' : ''}`;
} else if (dropped_packs.length > 0) {
  verdict = `${dropped_packs.length} pack(s) dissolved`;
} else if (moved_skills.length > 5) {
  verdict = `${moved_skills.length} skills regrouped`;
} else if (solo_delta > 0) {
  verdict = `${solo_delta} new solo(s) — investigate`;
}

const result = {
  stats: current.stats,
  prev_stats: previous.stats,
  skill_delta,
  pack_delta,
  solo_delta,
  edges_delta,
  new_packs,
  dropped_packs,
  moved_skills,
  verdict_one_line: verdict,
  pack_membership_current: membershipCur,
};
console.log(JSON.stringify(result, null, 2));
