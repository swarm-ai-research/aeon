#!/usr/bin/env node
// Sandbox-safe fingerprint runner: invokes .notegraph-fingerprint.sh through node's
// execSync (the bash tool can't run multi-op pipelines directly).
import { execSync } from 'node:child_process';
const out = execSync('bash .notegraph-fingerprint.sh', { encoding: 'utf8' });
process.stdout.write(out);
