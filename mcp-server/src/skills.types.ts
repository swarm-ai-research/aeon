/* Generated from schema/skills.schema.json. Do not edit by hand. Run scripts/gen-skill-types.sh to regenerate. */

/**
 * Aeon skills manifest. Generated from skills/ by scripts/build-skills-json (or equivalent). Consumed by mcp-server, a2a-server, and dashboard.
 */
export interface SkillsManifest {
  /**
   * Manifest schema version (e.g. "1.0").
   */
  version: string;
  /**
   * ISO-8601 timestamp of last generation.
   */
  generated?: string;
  /**
   * Source repository in owner/repo form.
   */
  repo: string;
  /**
   * Total skill count. Must equal skills.length.
   */
  total?: number;
  /**
   * Category slug → human-readable label map.
   */
  categories?: {
    [k: string]: string;
  };
  /**
   * Shell command to install every skill.
   */
  install_all?: string;
  /**
   * Shell command template to install one skill (placeholder: <skill-name>).
   */
  install_one?: string;
  skills: ManifestSkill[];
}
/**
 * A single skill entry as it appears in skills.json. Distinct from dashboard runtime SkillConfig.
 */
export interface ManifestSkill {
  /**
   * Kebab-case identifier; matches skills/<slug>/SKILL.md path.
   */
  slug: string;
  /**
   * Human-readable skill name.
   */
  name: string;
  /**
   * One-line summary used in tool descriptions and listings.
   */
  description: string;
  /**
   * Top-level grouping. Keep in sync with manifest.categories keys.
   */
  category: "research" | "dev" | "crypto" | "social" | "productivity" | "other";
  /**
   * Cron expression or "on-demand" or empty string for unscheduled.
   */
  schedule: string;
  /**
   * Default value or description for the skill's variable input. Empty if not used.
   */
  var: string;
  /**
   * File count under skills/<slug>/.
   */
  files?: number;
  /**
   * Git short-SHA of the skill's last update.
   */
  sha?: string;
  /**
   * ISO-8601 date of last update, or empty string if unknown.
   */
  updated?: string;
  /**
   * Shell command to install this specific skill.
   */
  install?: string;
}
