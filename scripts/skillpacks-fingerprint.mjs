#!/usr/bin/env node
import { execSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const files = execSync("git ls-files -- 'skills/*/SKILL.md'", { encoding: "utf8" })
  .trim()
  .split("\n")
  .sort();

const outer = createHash("sha1");
for (const f of files) {
  const h = createHash("sha1").update(readFileSync(f)).digest("hex");
  outer.update(`${h}  ${f}\n`);
}
const extractor = createHash("sha1").update(readFileSync("scripts/skillpacks.mjs")).digest("hex");
outer.update(`${extractor}  scripts/skillpacks.mjs\n`);
process.stdout.write(outer.digest("hex") + "\n");
