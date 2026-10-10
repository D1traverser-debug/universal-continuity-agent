# Control-plane Architecture Review — 2026-10-10

## Trigger
User challenged a reactive maintenance pattern: symptom reported -> add another policy. That challenge was valid. The immediate file-operation gap was real, but solving it with a new parallel root policy would itself increase authority fragmentation and future drift risk.

## External patterns reviewed
- OpenAI Agents: sessions/traces/observability make execution and tool activity inspectable; trace grading/evals support evidence-driven improvement rather than unverifiable self-claims.
- LangGraph: checkpointed graph state is explicit durable state; recovery does not rely on conversational recollection.
- Temporal: durable execution relies on persisted event history and explicit workflow versioning/compatibility for long-lived executions.
- OpenAI agent improvement loop: traces + feedback -> evals -> harness changes; improvement should be promoted from evidence, not accumulated as ad-hoc prompt/policy text.

## Architecture conclusions
1. Durable execution state must be explicit, versioned and independently recoverable from chat context.
2. File/artifact mutation needs stable identity, conflict/version checks and postcondition verification when material.
3. Cache, scratch, external references and memory must never silently become execution authority.
4. Long-lived owner workflows need compatibility/reconciliation rules rather than destructive migration or replay.
5. Learning/evolution must be evidence -> eval/validation -> accepted harness change, not unrestricted self-modification.
6. One invariant should have one authoritative home. New root policies/contracts/registries/agents require an admission gate proving that an existing authority cannot own the concern cleanly.
7. Cleanup is part of architecture: replacement should normally remove/demote superseded active mechanisms rather than leave parallel copies.

## User concerns: disposition
### Accepted as system risks
- stale files and stale reads;
- ambiguous file location/identity;
- write/delete claims without reread verification;
- duplicate or superseded active files;
- chat-only ideas being mistaken for durable evolution;
- external stores influencing execution despite not being current authority;
- total-control-plane vs owner drift;
- old chats using stale owner assumptions;
- owner-specific evolution diverging from Universal contracts.

### Direction correct, but treatment corrected
- Deleting Library/Notion/Drive may reduce clutter, but deletion must not be a correctness prerequisite. The control plane must remain correct even if stale external material exists. External stores are non-authoritative by default.
- Google Drive is suitable as an optional user-facing artifact vault for Word/PDF/slides/spreadsheets or explicit business evidence, but not as an implicit checkpoint or engineering-rule authority.
- Universal should govern cross-agent invariants and conformance, not absorb domain-specific file retention/business state into a mega-agent.
- Autonomous improvement should not mean unrestricted self-modification. Promotion requires evidence and validation.

## Changes made
- Consolidated verified file-operation semantics into `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` v1.1.
- Deleted the redundant root `FILE_OPERATION_GOVERNANCE_POLICY.json` created earlier in the same maintenance turn.
- Extended `OWNER_ADAPTER_CONTRACT.json` so owners must expose stable artifact stores/identity, read freshness, mutation conflict handling, post-write verification, invalidation and retention/delete rules.
- Upgraded `SYSTEM_MAINTENANCE_POLICY.json` to v1.2 with an `authority_surface_admission_gate` that defaults to rejecting a new authority surface when an existing authority can own the invariant.
- Added regression tests that forbid reintroducing the parallel file-operation policy and enforce verified file mutation plus authority-surface admission.
- Restored the canonical `HARNESS_STATUS.startup_trigger.acceptance_evidence.authoritative_default_candidate_count` key after CI exposed prior metadata drift.

## Validation
- Failed intermediate CI: run `38021429230`, `87 passed / 1 failed`; failure was canonical status-key drift, not the consolidated file-governance logic.
- Final validated CI: run `38021590796`, job `114123561213`, head `44c9af2d05752df5be35ec279d6fb8458591bbef`, package `3.7.0`, `89 passed in 0.20s`.

## Remaining boundaries
- Owner conformance still must be applied by each valid owner writer/maintenance path; Universal must not steal active leases or rewrite domain truth.
- Account-level Custom Instructions propagation and fresh/existing-chat product E2E remain external/product-layer acceptance work.
- Broader self-evolution architecture is intentionally deferred for separate design, per user request.

## Current architecture rule
When a new failure or idea appears, do not default to adding another prompt/policy/role/file. First classify the existing authority, ask whether code/test/schema/owner adapter is the right layer, remove or merge superseded mechanisms, and create a new authority surface only if it has a unique responsibility, owner, load trigger and deprecation path.
