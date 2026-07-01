# schema/

Single source of truth for the shape of `skills.json`.

## Files
- `skills.schema.json` — JSON Schema (Draft-7) for the skills manifest.
- TS types are generated into each consumer that reads `skills.json`:
  - `mcp-server/src/skills.types.ts`
  - `a2a-server/src/skills.types.ts`

## Editing the schema
1. Edit `skills.schema.json`.
2. Run `scripts/gen-skill-types.sh` from the repo root to regenerate the `.ts` files.
3. Commit the schema change and the regenerated types together.

The regen script also validates `skills.json` against the schema as a smoke test
(if `ajv` and `ajv-formats` are available — install them as dev deps to enable).

## Two distinct "Skill" concepts
- **`ManifestSkill`** (this schema) — entries in `skills.json`: `slug`, `name`,
  `description`, `category`, `schedule`, `var`, plus optional install metadata.
  Used by `mcp-server` and `a2a-server`.
- **`Skill`** in `dashboard/lib/types.ts` — runtime config: `enabled`, `model`,
  `tags`, plus a few overlapping fields. Different concept; do not unify.
