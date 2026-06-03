// Economic trust — Phase 4.
//
// GitLawb's economics (docs/ECONOMICS.md, contracts/) make node operators
// stake $GITLAWB and heartbeat to earn, with tiered weighting. The intent:
// being a trusted node costs real capital, and (once slashing lands)
// misbehavior burns it. This module is the CONSUMER side — the bridge's
// policy for which nodes it will accept events from, based on stake /
// heartbeat / slashing.
//
// IMPORTANT: GitLawb v1 has **no slashing**, and staking is on Base **Sepolia**
// (testnet), "disabled by default and currently paused." So the on-chain
// numbers aren't economically real yet. The oracle is therefore an INTERFACE:
// `BaseChainStakeOracle` is where the real reads of `GitlawbNodeStaking` /
// `GitlawbStaking` go once mainnet + slashing are live; `MockStakeOracle`
// stands in until then. The bridge logic doesn't change when the data goes
// real — only the oracle does.

// User-staker tiers from docs/ECONOMICS.md (min $GITLAWB → reward multiplier).
export const TIERS = [
  { name: "validator", min: 1_000_000, multiplier: 8 },
  { name: "steward", min: 100_000, multiplier: 4 },
  { name: "curator", min: 10_000, multiplier: 2 },
  { name: "observer", min: 1_000, multiplier: 1 },
];

export function tierFor(amount) {
  return TIERS.find((t) => amount >= t.min) ?? { name: "untiered", min: 0, multiplier: 0 };
}

// Node-operator economics from docs/ECONOMICS.md.
export const NODE_MIN_STAKE = 10_000; // GitlawbNodeStaking minimum
export const HEARTBEAT_MAX_AGE = 3 * 24 * 3600; // 3-day inactivity → excluded from rewards

// Real source of truth (skeleton). Reads the on-chain registries on Base.
//
// The hot path must stay SYNCHRONOUS — the bridge gates every event and can't
// do a chain RPC per event. So `nodeStatus()` reads a local cache; a scheduled
// job calls `refresh()` out-of-band to repopulate it from chain. Not
// implemented: mainnet staking + slashing are not live (testnet/paused).
export class BaseChainStakeOracle {
  constructor({ rpcUrl, nodeStaking, userStaking } = {}) {
    this.rpcUrl = rpcUrl;
    this.nodeStaking = nodeStaking;
    this.userStaking = userStaking;
    this.cache = new Map(); // nodeId → { registered, staked, lastHeartbeat, slashed }
  }

  // Out-of-band refresh from chain (periodic). NOT on the per-event path.
  async refresh() {
    throw new Error(
      "BaseChainStakeOracle.refresh not wired — Phase 4 dependency: read " +
        "GitlawbNodeStaking (stake, lastHeartbeat) + slashing on Base mainnet into " +
        "this.cache. v1 has no slashing and staking is paused on Sepolia, so there " +
        "is nothing real to read yet.",
    );
  }

  // Hot path: synchronous cache read (same contract as MockStakeOracle).
  nodeStatus(nodeId) {
    return this.cache.get(nodeId) ?? { registered: false, staked: 0, lastHeartbeat: 0, slashed: false };
  }
}

// In-memory stand-in. `nodes` maps nodeId → { staked, lastHeartbeat, slashed }.
export class MockStakeOracle {
  constructor(nodes = {}) {
    this.nodes = new Map(Object.entries(nodes));
  }

  setNode(nodeId, status) {
    this.nodes.set(nodeId, status);
  }

  nodeStatus(nodeId) {
    const s = this.nodes.get(nodeId);
    if (!s) return { registered: false, staked: 0, lastHeartbeat: 0, slashed: false };
    return { registered: true, staked: 0, lastHeartbeat: 0, slashed: false, ...s };
  }
}

// The bridge's economic gate: should we accept events relayed by this node?
export class NodeTrustPolicy {
  constructor({ oracle, minStake = NODE_MIN_STAKE, maxHeartbeatAge = HEARTBEAT_MAX_AGE, requireUnslashed = true } = {}) {
    this.oracle = oracle;
    this.minStake = minStake;
    this.maxHeartbeatAge = maxHeartbeatAge;
    this.requireUnslashed = requireUnslashed;
  }

  // Synchronous by design — runs on the bridge's per-event hot path against
  // cached oracle data (see BaseChainStakeOracle). `nodeId` MUST be an
  // authenticated identity (the bridge verifies the relaying node's signature
  // before calling this), never an attacker-supplied claim.
  evaluate(nodeId, { now = Math.floor(Date.now() / 1000) } = {}) {
    if (!nodeId) return { trusted: false, reason: "node_unspecified" };
    const s = this.oracle.nodeStatus(nodeId);
    if (!s.registered || s.staked <= 0) return { trusted: false, reason: "unregistered_node" };
    if (this.requireUnslashed && s.slashed) return { trusted: false, reason: "slashed" };
    if (s.staked < this.minStake) return { trusted: false, reason: `insufficient_stake:${s.staked}` };
    if (now - s.lastHeartbeat > this.maxHeartbeatAge) return { trusted: false, reason: "stale_heartbeat" };
    return { trusted: true, tier: tierFor(s.staked).name, stake: s.staked };
  }
}
