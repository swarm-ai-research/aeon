#!/usr/bin/env node
// bridge-cli — run the enforcement bridge as a service.
//
//   node bridge-cli.mjs run [--events <file.json>]
//
// Wires a Bridge from the same on-disk fleet state the gitlawb-fleet skill
// uses (shared operator root + revocation blocklist), then enforces every
// event from a source.
//
// Source selection:
//   • --events <file>  replay a JSON array of write events (testing / audit)
//   • (default)        the production source is GossipEventSource, which needs
//                      a libp2p host + bootstrap peers and is NOT runnable in
//                      this sandbox (Phase 1 infra dependency). Without
//                      --events the CLI explains this and exits.
//
// Paths mirror fleet-cli (env-overridable): GITLAWB_REGISTRY, GITLAWB_VAULT,
// GITLAWB_REVOCATIONS.

import { readFileSync } from "node:fs";
import { createBridgeFromStore } from "./src/bridge.mjs";
import { MockEventSource, GossipEventSource } from "./src/transport.mjs";

const P = {
  registryPath: process.env.GITLAWB_REGISTRY ?? "memory/gitlawb-fleet.json",
  vaultPath: process.env.GITLAWB_VAULT ?? ".gitlawb-vault/keys.json",
  revocationsPath: process.env.GITLAWB_REVOCATIONS ?? "memory/gitlawb-revocations.json",
};

function flag(args, name, def) {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
}

async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  if (cmd !== "run") {
    console.error("usage: node bridge-cli.mjs run [--events <file.json>]");
    process.exitCode = 1;
    return;
  }

  const bridge = createBridgeFromStore({
    ...P,
    onDecision: (d) => {
      const mark = d.decision === "allow" ? "ALLOW" : "DENY";
      console.log(`${mark}\t${d.action}\t${d.repo ?? ""}\t${d.sender ?? ""}\t${d.reason ?? "ok"}`);
    },
  });

  const eventsFile = flag(args, "events", null);
  let source;
  if (eventsFile) {
    source = new MockEventSource(JSON.parse(readFileSync(eventsFile, "utf8")));
  } else {
    source = new GossipEventSource();
    try {
      await source.subscribe(() => {});
    } catch (e) {
      console.error(`bridge: ${e.message}`);
      console.error("Provide --events <file.json> to replay events in the meantime.");
      process.exitCode = 1;
      return;
    }
  }

  const decisions = await bridge.run(source);
  const denied = decisions.filter((d) => d.decision === "deny").length;
  console.error(`bridge: ${decisions.length} events, ${denied} denied`);
}

main();
