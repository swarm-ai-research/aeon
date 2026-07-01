#!/usr/bin/env bash
# Regenerate TypeScript types from schema/skills.schema.json into every consumer
# that reads skills.json. Run after editing the schema; commit the regenerated
# .ts files alongside the schema change.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA="$REPO_ROOT/schema/skills.schema.json"
BANNER='/* Generated from schema/skills.schema.json. Do not edit by hand. Run scripts/gen-skill-types.sh to regenerate. */'

TARGETS=(
  "$REPO_ROOT/mcp-server/src/skills.types.ts"
  "$REPO_ROOT/a2a-server/src/skills.types.ts"
)

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

npx --yes json-schema-to-typescript@15 "$SCHEMA" \
  --no-additionalProperties \
  --bannerComment "$BANNER" \
  > "$TMP"

for target in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$target")"
  cp "$TMP" "$target"
  echo "wrote $target"
done

# Validate skills.json against the schema as a smoke test.
REPO_ROOT="$REPO_ROOT" node - <<'NODE'
const path = require('path');
const root = process.env.REPO_ROOT;
let Ajv, addFormats;
try {
  Ajv = require('ajv').default;
  addFormats = require('ajv-formats').default;
} catch {
  console.error('skipping validation: install ajv@8 ajv-formats@2 to enable');
  process.exit(0);
}
const ajv = new Ajv({allErrors: true, strict: false});
addFormats(ajv);
const schema = require(path.join(root, 'schema/skills.schema.json'));
const data = require(path.join(root, 'skills.json'));
const validate = ajv.compile(schema);
if (validate(data)) {
  console.log('skills.json validates');
} else {
  console.error('skills.json INVALID:', JSON.stringify(validate.errors, null, 2));
  process.exit(1);
}
NODE
