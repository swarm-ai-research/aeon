// fleet-dids.mjs — Fallback DID constants for Aeon fleet roles.
//
// Authoritative source: memory/instances.json (reconciled from *_PEM secrets).
// These values are the static fallback used when that file is absent or missing
// an entry. Both task-generator.mjs and goal-reconciler.mjs import from here so
// a DID update only needs one edit.
export const FLEET_ROLE_DIDS = {
  researcher: "did:key:z6MkfnrSDgdDbkvfCCnMyaR4HqoWfWEfGoTFajX1HGkSHRUH",
  reviewer:   "did:key:z6Mks2KSBfbindXsw2SBEGfqdgMJ4HwxJPfPQjkPKHY7U7SZ",
  deployer:   "did:key:z6MknGJBoQsbNL956GNiTJRRWKJqMcprWmdYxJPbVGCwcAuS",
  sentinel:   "did:key:z6MksUuVYyp93QA6pc2qAnXFQZdaoHq46dugXVweeehX4S2M",
};
