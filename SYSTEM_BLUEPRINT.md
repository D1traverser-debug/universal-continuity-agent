# Universal Continuity — System Blueprint

Status: ACTIVE
Protocol: v3.7
Engineering authority: `D1traverser-debug/universal-continuity-agent@main`

## Purpose

This file is the top-level architecture map for Universal Continuity. Lower-level contracts, policies, Skills and owner adapters implement this blueprint; they must not contradict it.

The user is not the migration operator. Universal Continuity owns protocol evolution, compatibility decisions, owner adaptation, progress observability and version hygiene. Domain owners retain business truth.

## Architecture layers

1. **Account routing layer** — `STARTUP_HOOK.md`. Personalization/Custom Instructions route explicit continuation intent into Continuity. They are an account-level trigger, not task storage.
2. **Discovery and routing layer** — `BARE_INHERIT_DISCOVERY.json`, `OWNER_REGISTRY.json`, executable harness. Finds exact durable tasks without treating chat memory as authority.
3. **Recovery layer** — `CONTEXT_RECOVERY_POLICY.json`. Loads metadata -> short handoff -> exact artifacts -> selective history.
4. **Compatibility and protocol reconciliation layer** — `VERSION_LIFECYCLE_POLICY.json`, `LIVE_CHAT_RECONCILIATION_POLICY.json`. Reconciles old task/chat protocol metadata to the current protocol without making the user migrate anything.
5. **Domain owner layer** — owner runtime/checkpoint. Business rules, business state machines and business artifacts stay with the domain owner.
6. **Writer ownership layer** — `resume_epoch` + `active_lease`. New-chat takeover changes the lease; an in-place protocol upgrade in the same active chat does not.
7. **Progress observability layer** — `PROGRESS_OBSERVABILITY_POLICY.json`. Shows pre-resume durable progress and verified per-turn commit status.
8. **Learning/evolution layer** — `CONTINUOUS_LEARNING_POLICY.md`, `MEDIA_DISTILLATION_PROTOCOL.md`, modular Skills and tests. Learning is distilled into the smallest authoritative surface.
9. **Lifecycle/cleanup layer** — current executable protocol stays in the working tree; superseded implementations live in Git history. Historical business evidence is never deleted merely because the protocol changed.

## Authority order

1. Compatible authoritative domain business checkpoint/runtime.
2. Authoritative per-task/per-system manifest for routing, lease and protocol metadata.
3. Universal registry/index cache.
4. Migration/audit/history artifacts.
5. Chat memory.

A lower authority may never overwrite fresher higher-authority business truth.

## Version model

- The active working-tree protocol is singular: v3.7.
- Old executable protocol copies are not kept active for convenience. Git history is the historical implementation archive.
- Historical task/business facts remain durable even if created under an older protocol.
- `continuity_protocol_version` identifies the Universal Continuity protocol.
- `contract_version` remains accepted as a legacy compatibility field until all owners migrate; new manifests should also expose `continuity_protocol_version` so Universal protocol and business/domain contract versions cannot be confused.
- An old chat is not permanently pinned to the protocol version it started with.

## Live-chat upgrade invariant

A chat that already owns a valid task lease may continue after Universal Continuity is upgraded.

Before its next material checkpoint/final durable response, it must reconcile against the current protocol:

1. read current protocol marker/policies;
2. compare persisted task protocol metadata;
3. classify COMPATIBLE / MIGRATABLE / INCOMPATIBLE / UNKNOWN;
4. apply a safe additive migration in place when supported;
5. preserve the existing lease and `resume_epoch` for the same active chat;
6. persist and re-read the adaptation record before claiming it is migrated;
7. then apply current progress-observability rules.

Only a genuine new-chat takeover increments `resume_epoch` and supersedes the old lease.

## User responsibility boundary

The user does **not**:

- choose migration paths;
- rewrite old checkpoints;
- decide which obsolete implementation files to keep;
- manually adapt each old chat;
- reason about owner schema differences;
- verify whether a write really persisted.

The user only supplies genuinely external facts/actions or decisions that cannot be inferred safely.

## Upgrade classification

- **PATCH / hardening**: tests, cleanup, documentation, owner conformance, compatible adapter additions. Keep the same protocol version.
- **MINOR protocol change**: new required semantics that remain migratable from the previous active protocol. Version bump required with an explicit migration edge.
- **BREAKING protocol change**: incompatible task semantics or persistence model. Version bump required; affected state must fail closed or migrate through an explicit audited path.

Do not increment the protocol number for every internal improvement.

## Cleanup invariant

Delete or archive from the active root any completed migration/cutover artifact that is no longer part of runtime/bootstrap authority. Before deletion, consolidate any still-useful audit facts into `archive/` or a current status artifact. Git history preserves the original files.

Do not delete:

- current business checkpoints;
- historical decisions/evidence needed for audit or causality;
- artifacts referenced by active `next_action`;
- compatibility evidence still required by a supported migration edge.

## Required final-response behavior

For every active durable task, every final response follows `PROGRESS_OBSERVABILITY_POLICY.json`. `COMMITTED` is only valid after authoritative re-read verification. The outer account instruction is a routing/UX backstop; owner persistence remains the proof.

## Read order

`ENTRYPOINT.md` -> `SYSTEM_BLUEPRINT.md` -> `STARTUP_HOOK.md` -> `CONTINUITY_CONTRACT.json` -> `VERSION_LIFECYCLE_POLICY.json` -> `LIVE_CHAT_RECONCILIATION_POLICY.json` -> domain-specific policy/artifacts as needed.
