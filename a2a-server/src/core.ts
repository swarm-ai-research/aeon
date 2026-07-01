/**
 * Shared core for the Aeon HTTP gateway: skill loading, slug resolution, the
 * default LLM plan, and skill-prompt construction. Both the A2A JSON-RPC layer
 * (index.ts) and the REST/SSE layer (rest-api.ts) sit on top of this so there
 * is a single definition of "what running a skill means".
 */

import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import type { ManifestSkill as Skill, SkillsManifest } from "./skills.types.js";
import type { LlmPlan } from "./llm-runner.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// a2a-server/dist/<file>.js → a2a-server/ → repo root
export const REPO_ROOT = join(__dirname, "..", "..");

export type { Skill };

let cachedSkills: Skill[] | null = null;

export function getSkills(): Skill[] {
  if (cachedSkills) return cachedSkills;
  const manifestPath = join(REPO_ROOT, "skills.json");
  if (!existsSync(manifestPath)) {
    process.stderr.write(`[aeon-gateway] skills.json not found at ${manifestPath}\n`);
    cachedSkills = [];
    return cachedSkills;
  }
  const manifest: SkillsManifest = JSON.parse(readFileSync(manifestPath, "utf-8"));
  cachedSkills = manifest.skills ?? [];
  return cachedSkills;
}

export function getSkillBySlug(slug: string): Skill | undefined {
  return getSkills().find((s) => s.slug === slug);
}

export function skillFileExists(slug: string): boolean {
  return existsSync(join(REPO_ROOT, "skills", slug, "SKILL.md"));
}

/**
 * Build the prompt that drives a skill run. Mirrors the A2A path so REST and
 * A2A produce identical behavior for the same (slug, var).
 */
export function buildSkillPrompt(slug: string, varValue: string): string {
  const today = new Date().toISOString().split("T")[0];
  let prompt = `Today is ${today}. Read and execute the skill defined in skills/${slug}/SKILL.md`;
  if (varValue) {
    prompt += `\n\nUse this variable (override the default in the skill file):\nvar=${varValue}`;
  }
  return prompt;
}

/**
 * The primary + fallback LLM plan, derived from runtime env. Kept here so both
 * transports route through the same multi-target chain (hxmp.3).
 */
export function defaultPlan(): LlmPlan {
  const primaryModel = process.env.AEON_LLM_MODEL ?? "claude-opus-4-7";
  const primaryGateway = process.env.AEON_LLM_GATEWAY === "bankr" ? "bankr" : "direct";
  const plan: LlmPlan = {
    primary: { provider: "claude", model: primaryModel, gateway: primaryGateway },
  };
  if (primaryGateway === "direct" && process.env.BANKR_LLM_KEY) {
    plan.fallbacks = [{ provider: "claude", model: primaryModel, gateway: "bankr" }];
  } else if (primaryGateway === "bankr" && process.env.ANTHROPIC_API_KEY) {
    plan.fallbacks = [{ provider: "claude", model: primaryModel, gateway: "direct" }];
  }
  return plan;
}
