#!/usr/bin/env node
/**
 * Aeon MCP Server
 *
 * Exposes all Aeon skills as MCP tools so any Claude Desktop or Claude Code
 * user can invoke them directly from their Claude interface.
 *
 * Tool naming: aeon-{slug} (e.g. aeon-article, aeon-hacker-news-digest)
 * Each tool accepts a single optional `var` argument (the skill's variable input).
 *
 * Skill execution: spawns `claude -p -` with the skill prompt, exactly as
 * GitHub Actions does, so local runs are identical to scheduled runs.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import type { ManifestSkill as Skill, SkillsManifest } from "./skills.types.js";
import { runPrompt, type LlmPlan } from "./llm-runner.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// mcp-server/dist/index.js → mcp-server/ → repo root
const REPO_ROOT = join(__dirname, "..", "..");

function loadSkills(): Skill[] {
  const manifestPath = join(REPO_ROOT, "skills.json");
  if (!existsSync(manifestPath)) {
    process.stderr.write(
      `[aeon-mcp] skills.json not found at ${manifestPath}\n`
    );
    return [];
  }
  const manifest: SkillsManifest = JSON.parse(
    readFileSync(manifestPath, "utf-8")
  );
  return manifest.skills ?? [];
}

function skillToToolName(slug: string): string {
  return `aeon-${slug}`;
}

function toolNameToSlug(toolName: string): string {
  return toolName.replace(/^aeon-/, "");
}

function buildTools(skills: Skill[]) {
  return skills.map((skill) => ({
    name: skillToToolName(skill.slug),
    description: buildDescription(skill),
    inputSchema: {
      $schema: "http://json-schema.org/draft-07/schema#" as const,
      title: skill.name,
      description: skill.description,
      type: "object" as const,
      properties: {
        var: {
          type: "string",
          description: buildVarDescription(skill),
        },
      },
      required: [],
      additionalProperties: false,
    },
  }));
}

function buildDescription(skill: Skill): string {
  const categoryLabel = categoryName(skill.category);
  const scheduleLabel =
    skill.schedule === "on-demand"
      ? "on-demand"
      : `cron: ${skill.schedule}`;
  return `[Aeon · ${categoryLabel}] ${skill.description} (${scheduleLabel})`;
}

function buildVarDescription(skill: Skill): string {
  if (skill.var) return skill.var;
  const defaults: Record<string, string> = {
    research: "Topic or keyword to focus the skill on (e.g. 'AI agents'). Leave empty for auto-selection.",
    dev: "Repo in owner/repo format to narrow scope. Leave empty to scan all watched repos.",
    crypto: "Token symbol or contract address to focus on. Leave empty for all tracked tokens.",
    social: "Topic, handle, or keyword. Leave empty to use configured defaults.",
    productivity: "Focus area or goal. Leave empty for general operation.",
  };
  return (
    defaults[skill.category] ??
    `Optional variable input for the ${skill.name} skill.`
  );
}

function categoryName(category: string): string {
  const labels: Record<string, string> = {
    research: "Research",
    dev: "Dev",
    crypto: "Crypto",
    social: "Social",
    productivity: "Productivity",
  };
  return labels[category] ?? category;
}

function defaultPlan(): LlmPlan {
  const primaryModel = process.env.AEON_LLM_MODEL ?? "claude-opus-4-7";
  const primaryGateway = process.env.AEON_LLM_GATEWAY === "bankr" ? "bankr" : "direct";
  const plan: LlmPlan = {
    primary: { provider: "claude", model: primaryModel, gateway: primaryGateway },
  };
  // If a bankr key exists and primary is direct, fall back to bankr on failure (and vice versa).
  if (primaryGateway === "direct" && process.env.BANKR_LLM_KEY) {
    plan.fallbacks = [{ provider: "claude", model: primaryModel, gateway: "bankr" }];
  } else if (primaryGateway === "bankr" && process.env.ANTHROPIC_API_KEY) {
    plan.fallbacks = [{ provider: "claude", model: primaryModel, gateway: "direct" }];
  }
  return plan;
}

async function runSkill(slug: string, varValue: string): Promise<string> {
  const skillFile = join(REPO_ROOT, "skills", slug, "SKILL.md");
  if (!existsSync(skillFile)) {
    return [
      `Error: skill '${slug}' not found.`,
      `Expected SKILL.md at: ${skillFile}`,
      `Make sure you're running the MCP server from inside an Aeon repo clone.`,
    ].join("\n");
  }

  const today = new Date().toISOString().split("T")[0];
  let prompt = `Today is ${today}. Read and execute the skill defined in skills/${slug}/SKILL.md`;

  if (varValue.trim()) {
    prompt += `\n\nUse this variable (override the default in the skill file):\nvar=${varValue.trim()}`;
  }

  process.stderr.write(`[aeon-mcp] Running skill: ${slug}${varValue ? ` (var=${varValue})` : ""}\n`);

  const result = await runPrompt(prompt, defaultPlan(), {
    cwd: REPO_ROOT,
    onFailure: ({ index, target, error }) =>
      process.stderr.write(
        `[aeon-mcp] attempt ${index + 1} (${target.model}@${target.gateway ?? "direct"}) failed: ${error}\n`
      ),
  });

  if (!result.ok) {
    return `Skill '${slug}' failed across ${result.attempts.length} target(s): ${result.error}`;
  }
  return result.output || `Skill '${slug}' produced no output.`;
}

// ---- Server setup ----

const server = new Server(
  { name: "aeon-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

const skills = loadSkills();
const tools = buildTools(skills);

process.stderr.write(
  `[aeon-mcp] Loaded ${skills.length} skills from ${REPO_ROOT}\n`
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;
  const slug = toolNameToSlug(toolName);
  const skill = skills.find((s) => s.slug === slug);

  if (!skill) {
    return {
      content: [
        {
          type: "text" as const,
          text: `Unknown Aeon tool: ${toolName}\nAvailable tools: ${tools.map((t) => t.name).join(", ")}`,
        },
      ],
      isError: true,
    };
  }

  const varValue = (request.params.arguments?.var as string) ?? "";
  const output = await runSkill(slug, varValue);

  return {
    content: [{ type: "text" as const, text: output }],
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  process.stderr.write("[aeon-mcp] Server running on stdio\n");
}

main().catch((err: unknown) => {
  process.stderr.write(`[aeon-mcp] Fatal error: ${err}\n`);
  process.exit(1);
});
