// Transport — how the bridge receives node events.
//
// GitLawb propagates ref-update events over libp2p Gossipsub. The bridge
// doesn't care which source it subscribes to, as long as the source yields
// events shaped like `makeWriteEvent` produces. That lets us run the full
// bridge against a deterministic MockEventSource here, and drop in the real
// gossip source (which needs libp2p — a Phase 1 infra dependency) unchanged.

import { signRequest } from "./httpsig.mjs";
import { signBytes } from "./identity.mjs";
import { serializeToken } from "./ucan.mjs";

// Build a signed write request, exactly as an Aeon agent would emit one before
// it hits the node. The request is signed by the SENDER's key (RFC 9421); the
// UCAN capability rides alongside.
export function makeWriteEvent({ sender, token, action, repo, ref, proposal, nodeIdentity }) {
  const method = "POST";
  const url = `gitlawb://${repo}/${action}`;
  // The proposal rides INSIDE the signed body so the bridge's per-change merge
  // caveat can't be swapped for a different diff after signing.
  const body = JSON.stringify({ action, repo, ref, sender: sender.did, ...(proposal ? { proposal } : {}) });
  const headers = signRequest({ method, url, did: sender.did, privateKey: sender.privateKey, body });

  const event = {
    action,
    repo,
    ref,
    sender: sender.did,
    token: serializeToken(token),
    request: { method, url, headers, body },
  };

  // The relaying node attests it relayed THIS request by signing the sender's
  // signature with its OWN key (models a signed libp2p gossip envelope). The
  // node id is its did:key — authenticated, not a self-asserted string — so an
  // unstaked node can't claim a staked node's id without that node's key.
  if (nodeIdentity) {
    event.node = nodeIdentity.did;
    event.nodeSig = signBytes(nodeIdentity.privateKey, headers["Signature"]).toString("base64");
  }
  return event;
}

// Deterministic in-process source for tests/demos. `subscribe` drives the
// handler over a fixed list of events and resolves when done.
export class MockEventSource {
  constructor(events = []) {
    this.events = events;
  }

  async subscribe(handler) {
    for (const event of this.events) await handler(event);
  }
}

// The real source. Subscribes to a GitLawb node's gossip topic for
// ref-update events. Intentionally not implemented in the prototype: it
// requires a libp2p host + the node's bootstrap peers, which can't run in this
// sandbox. The bridge treats it identically to MockEventSource.
export class GossipEventSource {
  constructor({ bootstrapPeers, topic = "gitlawb/ref-updates" } = {}) {
    this.bootstrapPeers = bootstrapPeers;
    this.topic = topic;
  }

  async subscribe() {
    throw new Error(
      "GossipEventSource not wired — Phase 1 infra dependency: stand up a libp2p " +
        "host, dial bootstrap peers, and map gossip ref-update messages to the " +
        "makeWriteEvent shape. See ROADMAP Phase 1.",
    );
  }
}
