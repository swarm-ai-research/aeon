// SwarmCoordinator — steering a GitLawb fleet on top of the capability layer.
//
// This is what the trustworthy capability layer buys you: coordination where
// authority is least-privilege and self-expiring. Every sub-task is dispatched
// with a freshly-minted, short-lived capability scoped to exactly what that
// worker needs — so a coordinated run can't leave lingering authority, and a
// compromised worker's grant dies on its own.
//
//   • runParallel    — operator mints a scoped cap to each worker; fan out.
//   • runHierarchical — operator mints to a lead; the lead DELEGATES attenuated
//                       caps to its children (the chain the bridge verifies).
//
// `capFor(task, worker)` returns the capabilities a worker needs (must be an
// attenuation of the lead's, in the hierarchical case). `execute({worker,
// task, token})` performs the work and returns a result (or throws).

import { nowSec } from "./ucan.mjs";

export class SwarmCoordinator {
  constructor({ operator, guard, metrics = null }) {
    this.operator = operator;
    this.guard = guard;
    this.metrics = metrics;
  }

  async runParallel({ task, workers, capFor, ttlSeconds = 120, execute }) {
    const results = await Promise.all(
      workers.map((w) => this.#dispatch({ issuer: this.operator, worker: w, task, capFor, ttlSeconds, execute })),
    );
    return { pattern: "parallel", task: task.id, results };
  }

  async runHierarchical({ task, lead, children, capFor, ttlSeconds = 120, execute }) {
    // Lead receives its capability directly from the operator.
    const leadCaps = capFor(task, lead);
    const leadToken = this.guard.mint({ issuer: this.operator, audienceDid: lead.did, capabilities: leadCaps, ttlSeconds });
    this.metrics?.record("dispatch", { did: lead.did, task: task.id, role: "lead" });

    // Lead delegates attenuated caps to each child (the guard rejects any child
    // cap that isn't an attenuation of the lead's — enforced when authorized).
    const childResults = await Promise.all(
      children.map((c) =>
        this.#dispatch({ issuer: lead, worker: c, task, capFor, ttlSeconds, execute, proof: leadToken, role: "child" }),
      ),
    );

    let leadResult = null;
    if (execute) {
      try {
        leadResult = { worker: lead.did, ok: true, out: await execute({ worker: lead, task, token: leadToken }) };
      } catch (e) {
        leadResult = { worker: lead.did, ok: false, error: String(e) };
      }
    }
    return { pattern: "hierarchical", task: task.id, lead: leadResult, children: childResults };
  }

  async #dispatch({ issuer, worker, task, capFor, ttlSeconds, execute, proof, role = "worker" }) {
    const capabilities = capFor(task, worker);
    const token = proof
      ? this.guard.delegate({ issuer, audienceDid: worker.did, capabilities, ttlSeconds, proof })
      : this.guard.mint({ issuer, audienceDid: worker.did, capabilities, ttlSeconds });
    this.metrics?.record("dispatch", { did: worker.did, task: task.id, role, expiresAt: token.payload.exp });

    try {
      const out = execute ? await execute({ worker, task, token }) : null;
      return { worker: worker.did, ok: true, out };
    } catch (e) {
      return { worker: worker.did, ok: false, error: String(e) };
    }
  }
}

export { nowSec };
