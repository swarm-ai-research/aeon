# Private Vulnerability Report draft — yc-software/qm

**Status:** DRAFT — pending operator submission via
`https://github.com/yc-software/qm/security/advisories/new`

**Target commit:** `0f0e0adccce2d13e4aff3e5bf3efb0cccf312f7a`
**Detected:** 2026-08-08 via Aeon vuln-scanner (semgrep p/security-audit + p/owasp-top-ten)

QM's `SECURITY.md` directs reporters to the repository's `Security → Report a
vulnerability` flow. Both findings below are hardening / defense-in-depth issues,
not exploitable-as-shipped bugs, and both surface in code shipped to production.
Sending them privately per QM's stated policy.

---

## Finding 1 — AES-256-GCM decryption accepts truncated authentication tags (CWE-310, CWE-345)

### Severity
**Medium.** Defense-in-depth crypto weakness. Not exploitable through the current
public API surface (`getConnectorClientSecret` reads from a DB row that only org
admins can write), but a future path that lets a lower-privileged actor supply an
encrypted blob to `decryptSecret()` would inherit a weakened authenticity guarantee.

### Location
`src/connectors/connector-client-store.ts:87`

### Summary
`decryptSecret()` calls `crypto.createDecipheriv('aes-256-gcm', key, iv)` without
passing an `authTagLength`. Node.js then accepts any auth tag from 4 to 16 bytes
via `setAuthTag()`. An attacker who can supply the ciphertext blob to
`decryptSecret()` can present a 4-byte tag, dropping GCM's forgery resistance
from 2^128 to 2^32 — feasible for an online oracle in seconds to minutes.

The paired `encryptSecret()` (line 71) always writes a 16-byte tag via
`getAuthTag()`, so pinning the decrypt side to `authTagLength: 16` is
compatible with every legitimately stored ciphertext.

Both the v2 (`k.current`) and legacy (`k.legacy`) paths at line 87 share this
call, so a single fix covers both.

### Suggested fix
```ts
const decipher = createDecipheriv(
  "aes-256-gcm",
  v2 ? k.current : k.legacy,
  Buffer.from(ivB, "base64"),
  { authTagLength: 16 },
);
```

Consider also validating `Buffer.from(ivB, "base64").length === 12` before
constructing the decipher — the current code accepts any IV length, which is
another Node quirk worth closing.

### Reference
- Semgrep rule: `javascript.node-crypto.security.gcm-no-tag-length.gcm-no-tag-length`
- Node.js crypto docs: `createDecipheriv(algorithm, key, iv[, options])`
  <https://nodejs.org/api/crypto.html#cryptocreatedecipherivalgorithm-key-iv-options>

---

## Finding 2 — Release workflow inherits every repository secret into the CLI publish reusable workflow (CWE-250)

### Severity
**Medium.** Least-privilege violation with real supply-chain implications. The
public workflow file discloses the pattern.

### Location
`.github/workflows/release.yml:54`

### Summary
The `cli` job calls `./.github/workflows/publish-cli.yml` with
`secrets: inherit`, which forwards **every** repository secret into the reusable
workflow's scope. The reusable workflow only needs `NPM_TOKEN` (line 96 of
`publish-cli.yml`, `NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}`).

`publish-cli.yml` runs `npm ci` and `npm run test:pack` against `cli/`
dependencies. A compromise anywhere in that dependency tree — including install
scripts, transitive lifecycle hooks, or a maliciously-updated dev-dep — would
execute with access to every repo secret, not just `NPM_TOKEN`.

### Suggested fix
```yaml
  cli:
    name: CLI
    needs: images
    permissions:
      contents: read
      id-token: write
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
    uses: ./.github/workflows/publish-cli.yml
```

If any other repo secret is required by future changes to `publish-cli.yml`,
list it explicitly rather than reverting to `inherit`.

### Reference
- Semgrep rule: `yaml.github-actions.security.secrets-inherit.secrets-inherit`
- GitHub docs on `secrets: inherit`:
  <https://docs.github.com/en/actions/sharing-automations/reusing-workflows#passing-inputs-and-secrets-to-a-reusable-workflow>

---

## Scanner metadata

- Ruleset: `p/security-audit`, `p/owasp-top-ten`, `p/secrets`
- Excluded: `test`, `tests`, `__tests__`, `spec`, `specs`, `fixtures`, `examples`,
  `example`, `demo`, `vendor`, `node_modules`, `dist`, `build`, `.next`
- Semgrep OSS 1.172.0
- No verified leaked secrets (filesystem + git history TruffleHog `--only-verified`).
  Slither n/a — no `.sol` files.
- Total raw semgrep findings: 14 (this report ships the 2 that survived triage;
  the other 12 are Dockerfile-missing-USER inside sandboxed microVMs where the VM
  is the isolation boundary, Terraform hardening in
  `cli/templates/aws/main.tf` which is a customer-owned template not a running
  QM service, and Python `dynamic-urllib-use-detected` in `skills-seed/*/scripts/`
  where the URL base is hardcoded and the path is composed by trusted skill code).

## Requested handling

Please treat this as a private advisory in the GitHub Security → Advisories
flow. No exploit chain is included; the fixes above are small and local, and
we're happy to submit them as a follow-up PR against a maintainer-created
private-fork branch if that's preferred over cherry-picking.

---
_Filed by [Aeon](https://github.com/aeonframework/aeon)._
