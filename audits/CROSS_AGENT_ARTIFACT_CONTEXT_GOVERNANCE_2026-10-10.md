# Cross-Agent Artifact / Context Governance Audit — 2026-10-10

## Problem
The cross-agent system already had Continuity checkpoints, protocol migration, owner-specific cleanup, and execution-readiness rules, but it did not yet have one universal classification for caches, scratch files, learning evidence, external references, personalization context, durable task state, business evidence, and engineering authority. That left a drift risk: stale Library/Drive/Notion/project/chat context or rebuildable caches could be mistaken for current owner truth, while useful learning might remain chat-only and disappear.

## Root cause
Lifecycle semantics were fragmented across owner repositories and Continuity policies. The system distinguished authoritative checkpoint vs chat memory, but not the full cross-store artifact lifecycle. Owner-specific implementations (for example Financial Writing v0.6 stale-artifact invalidation and deleted legacy surfaces) were stronger than the universal contract, so other owners could diverge.

## Changed authority surfaces
- Added `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` v1.0.
- Added the artifact/context governance layer and explicit authority ordering to `SYSTEM_BLUEPRINT.md`.
- Updated `SYSTEM_MAINTENANCE_POLICY.json` to treat artifact/cache/context drift and chat-only material changes as autonomous-maintenance triggers.
- Updated `OWNER_ADAPTER_CONTRACT.json` so owners must expose durable task-state location, business-evidence authority, cache/reference-only stores, invalidation rules, and superseded-artifact cleanup rules.
- Updated `CONTINUOUS_LEARNING_POLICY.md` so material learning is provenance-bearing evidence before promotion; chat-only ideas are not durable evolution.
- Added `tests/test_artifact_context_governance.py` regression coverage.

## Storage / authority model
1. `ENGINEERING_AUTHORITY`: current GitHub main code/contracts/Skills/policies. One active implementation; superseded implementation lives in Git history unless a migration edge still needs it.
2. `DURABLE_TASK_STATE`: owner manifest/checkpoint/runtime state/lease. Never delete merely because system code changed; migrate through compatibility rules.
3. `BUSINESS_EVIDENCE`: source documents, accepted/published outputs, audit/decision evidence. Owner-retained; never delete while needed for causality, audit, publication, or active next_action.
4. `LEARNING_EVIDENCE`: edits, feedback, performance observations, research notes, candidate heuristics. Cannot directly drive execution or become a rule without owner maintenance/evolution acceptance.
5. `REBUILDABLE_CACHE`: indexes, derived summaries, render/search caches, mirrors, temporary extraction. Delete/rebuild on drift; never commit proof or task authority.
6. `SESSION_SCRATCH`: temporary analysis/intermediate local files/unpromoted tool outputs. Ephemeral unless intentionally promoted.
7. `EXTERNAL_REFERENCE`: Library, Drive, Notion, Slack, connected apps, project sources. Evidence/reference by default; only owner contract or explicit task provenance can elevate it.
8. `CHAT_PERSONALIZATION_CONTEXT`: Custom Instructions, Project instructions, Memory, past chats. Behavioral/routing context, not durable business state.

## Product-surface verification
Current first-party OpenAI documentation was rechecked on 2026-10-10 for maintenance decisions:
- Custom Instructions updates are applied across existing chats.
- Project instructions are scoped to the Project and override global Custom Instructions inside that Project.
- Memory may use past chats, Custom Instructions, Library files, and connected-app content depending on plan/settings.
- ChatGPT Library automatically saves uploaded/generated files; deleting a chat does not by itself delete a saved Library file.
These are product facts, not permanent protocol invariants; reverify when material.

## Financial Writing v0.6 claim audit
The statement that v0.6 behaves more like maintainable software is materially supported, not merely rhetoric:
- architecture explicitly separates deterministic outer runtime from model-driven stages;
- upstream revision invalidates downstream gates/artifacts;
- stale render pages are cleared before rerender;
- old `mcp_server.py`, `CHAT_TEXT`, visual/sticker contracts and canned structure-pattern library are explicitly removed and forbidden from returning;
- learning samples remain `RAW_EVIDENCE_ONLY` until maintenance promotion;
- current v0.6 main has a successful regression run (`38018238323`) at head `5d5e2493de1ff6b940366b133611cd3cd929244d`.
This proves concrete lifecycle/cleanup/regression mechanisms exist. It does not prove the Agent can autonomously discover every future defect; that requires the shared maintenance/evolution contract plus ongoing evidence.

## Validation
Universal Continuity CI at head `8c02cea278a4009c848d6d3430ea411d25bc9e85`:
- run: `38019817158`
- job: `114118106198`
- package: `3.7.0`
- result: `84 passed in 0.23s`

## Behavioral effect
- A cache or stale mirror can no longer be treated as checkpoint authority by contract.
- Material ideas that exist only in chat cannot be called durable evolution.
- Connected sources are context/evidence unless explicitly designated by the owner/task.
- Superseded engineering files are removed/demoted from the active path rather than accumulated indefinitely.
- Domain owners keep control over business-specific retention/invalidation, preventing Universal maintenance from deleting valid business evidence or stealing an owner lease.

## Remaining risks / external boundaries
- Project instructions can override global Custom Instructions, so a conflicting Project can suppress the global Continuity UX hook. This is a ChatGPT product precedence boundary; owner/business authority still remains in GitHub/checkpoints. Project-specific compatibility may require user/project configuration if a real conflict is observed.
- The new universal owner-conformance fields are a contract requirement; existing owners should be audited/adapted incrementally by their valid writers. Universal maintenance must not rewrite active owner business state merely to satisfy conformance metadata.
- External stale copies in Library/Drive/Notion should only be deleted when safe and when they materially risk drift; there is no blanket deletion rule.
- The broader self-evolution system is intentionally deferred for a separate design discussion. This patch only guarantees evidence/promotion/lifecycle boundaries, not unrestricted self-modification.

## Current stage
`V3_7_CROSS_AGENT_ARTIFACT_GOVERNANCE_ACTIVE__OWNER_CONFORMANCE_AND_PRODUCT_E2E_PENDING`

## Next action
Audit/adapt Financial Writing, A-share, Video Growth, and other durable owners against the new artifact/context lifecycle declarations on their valid maintenance/writer turns; keep current account Custom Instructions/product-level E2E work pending at the precise external boundary. Discuss broader evolution architecture separately as requested.
