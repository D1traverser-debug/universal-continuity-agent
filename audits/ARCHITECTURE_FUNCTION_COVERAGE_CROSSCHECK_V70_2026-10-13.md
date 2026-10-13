# Architecture Function-Coverage Crosscheck — 2026-10-13

Status: `AUDIT_ONLY / NO_PRODUCTION_REFACTOR`

Purpose: describe the current Universal control-plane functions at system-outline level, then cross-check whether prior architecture/reliability audits (G01–G30), the six screened primitive families, and `23_refactor_execution_plan.md` actually cover the risks of each function.

This audit does not authorize implementation and does not modify production runtime semantics.

## Functional outline and coverage

| ID | Current control-plane function | Main current surfaces | Prior risk coverage | Current refactor-plan landing | Crosscheck result |
|---|---|---|---|---|---|
| F01 | Bootstrap / ingress triage / hot-path loading | `ENTRYPOINT.md`, `STARTUP_HOOK.md`, `CURRENT_PROTOCOL.json` | G01, G11, G20, G21 plus current exact-prose-test coupling finding | Phase 0, P3, P5 | COVERED WITH TEST-GOVERNANCE REPAIR: semantic behavior is strong, but bootstrap tests must stop binding long prose as contract. |
| F02 | Intent routing / owner selection / bare-inherit discovery | `OWNER_REGISTRY.json`, `BARE_INHERIT_DISCOVERY.json`, `runtime/owner_topology.py`, `runtime/universal_continuity.py` | G02, G03, G16 | P1 Derived System/Authority Model | PARTIAL: owner membership is strong; interaction mode, dependency direction, backpressure/service expectation and escalation semantics from G03 need explicit fields in the derived model. |
| F03 | Durable task continuity / handoff / recovery / selective context reload | task manifests/checkpoints, `CONTEXT_RECOVERY_POLICY.json`, lease/resume semantics | G25, G27, G28 | P2 lineage + P6 writer protocol | PARTIAL: lineage/replay are represented in the plan, but G27 context compaction as an execution-state transformation has no explicit implementation landing. |
| F04 | Single-writer lease / takeover / publish / commit receipt | `runtime/universal_continuity.py`, `PROGRESS_OBSERVABILITY_POLICY.json`, HEAD-CAS bootstrap guard | G07, G19, G23, G24 | P6 state machine + P2 effects | PARTIAL-STRONG: current writer model is strongly covered; G24 still needs a machine-readable trigger for when writer topology changes invalidate SINGLE_ACTIVE_CHAT assumptions. |
| F05 | Protocol/version lifecycle and reconciliation | `VERSION_LIFECYCLE_POLICY.json`, `LIVE_CHAT_RECONCILIATION_POLICY.json`, protocol adapters | G04, G24, G29 | only indirectly P1/P2/P6 | EXPLICIT PLAN GAP: G29 runtime/provider/protocol integration compatibility, capability negotiation and exact deployed-combination evidence are not explicitly scheduled in plan 23. |
| F06 | Execution readiness / capability handshake / internal dispatch | `EXECUTION_READINESS_CONTRACT.json`, `runtime/execution_readiness.py`, owner capability refs | G04, G25, G28, G29 | P2 + P3 | PARTIAL: action binding is strong, but the environment/substrate matrix from G04 and integration compatibility from G29 need explicit derived declarations. |
| F07 | Execution receipt / exact-action proof / anti-replay / HITL binding | `runtime/execution_receipt.py`, execution-readiness receipt contract | G19, G25, G26 | P2 | COVERED IN DIRECTION: plan includes lineage, effect metadata and approval binding; implementation must still define approval occurrence, subject, parameter/version, expiry/invalidation and resume/replay rules. |
| F08 | Domain-owner boundary / methodology composition / one-product entry | `OWNER_ADAPTER_CONTRACT.json`, methodology conformance, owner manifests/registry | G03, G13, G20, G29 | P1 + P3 | PARTIAL: authority boundary is strong; G03 interaction/service/backpressure semantics and G29 runtime-compatibility evidence remain under-specified. |
| F09 | Artifact/file/cache/external-reference governance | `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`, `runtime/mutation_outcome.py` | G16, G19, G22, G27 | P2 + P3 + P5 indirectly | PARTIAL: stable identity, verified mutation and unknown-outcome handling are strong; context-compaction governance and a uniform promotion/supersession trace remain incomplete. |
| F10 | State plane / signal plane / control-signal admission | `CONTROL_SIGNAL_CONTRACT.json`, `runtime/control_signal.py`, task/owner state authorities | G08, G09, G16, G23 | P4 + P5 | PARTIAL: authority separation is strong; typed isolation/recovery budgets and concurrent-fault behavior are planned only at high level. |
| F11 | Remote architecture observation / external product-state freshness | `OWNER_ARCHITECTURE_OBSERVATIONS.json`, remote-monitor policy in Blueprint/Handoff | G04, G05, G16, G17 | P1 + P5 | PARTIAL: desired/observed and freshness metrics fit P1/P5; actual monitor/scheduler liveness remains external product state and cannot be proven by repository architecture alone. |
| F12 | Architecture conformance / CI / regression / synthetic fault harness | `runtime/system_audit.py`, `runtime/agent_architecture_audit.py`, `.github/workflows/ci.yml`, pytest | G06, G11, G12, G13, G14, G18 | Phase 0 + P3 + P5 | COVERED WITH IMPORTANT REPAIR: replace raw test-count thinking and brittle prose anchors with invariant/failure-class/model coverage. |
| F13 | Autonomous maintenance / stage control / reopen / recurrence escalation | `SYSTEM_MAINTENANCE_POLICY.json`, `runtime/maintenance_controller.py`, `runtime/meta_maintenance.py` | G01, G08, G09, G10, G23 | P4 + P3 | PARTIAL: recurrence escalation is already strong; typed fault isolation, recovery budget, safe-hold/hazard semantics and multi-fault analysis still need explicit implementation. |
| F14 | Learning/evolution / research scouting / candidate adoption | `CONTINUOUS_LEARNING_POLICY.md`, research/audit artifacts, evolution profile | G22, G30 | P3 + P5 indirectly | EXPLICIT PLAN GAP: current policy has strong candidate/adoption gates, but plan 23 does not explicitly implement one derived lifecycle from live failure/user correction -> trace -> reproducible eval -> offline regression -> measured improvement -> promotion -> online monitoring -> retirement/supersession. |
| F15 | Assurance / evidence ladder / independence / claim calibration | learning policy, system audit, architecture audit, execution evidence | G06, G11, G12, G13, G14 | P3 Assurance Trace | STRONGLY COVERED IN PLAN: P3 is the correct consolidation point, including independence axes rather than reviewer counts. |
| F16 | Reliability measurement / rollout / chaos / complexity / toil | anti-bloat rules, synthetic fault injection, context budgets, CI/audit evidence | G05, G17, G18, G20, G21 | P5 | PARTIAL-STRONG: measurable reliability and progressive rollout are explicit; G20/G21 central coupling and operational toil need explicit metrics/baselines, not only wrong-route/recovery/test-duplication indicators. |
| F17 | Lifecycle cleanup / supersession / deprecation / migration | `VERSION_LIFECYCLE_POLICY.json`, artifact promotion/cleanup rules | G22, G24, G29 | deletion budget + P1/P5/P6 indirectly | PARTIAL: cleanup rules are strong, but cross-type promotion/retirement trace and compatibility-driven transition triggers remain fragmented. |
| F18 | Specialized evidence ingestion/media distillation | `MEDIA_DISTILLATION_PROTOCOL.md`, artifact governance, learning evidence classes | mainly G06, G12, G22 | P3 plus existing artifact governance | ADEQUATELY COVERED: provenance/evidence-class boundaries already exist; no separate framework primitive is justified unless future evidence shows a recurring failure class. |

## What prior review already covered well

The previous G01–G30 review was broad enough to touch every major current functional domain. There is no evidence here of a completely unaudited major kernel function. The strongest existing areas remain authority precedence, durable task state, single-writer/stale-writer protection, state-vs-signal separation, exact-action execution evidence, owner/business boundaries, deterministic maintenance control, candidate-vs-authority separation and bounded assurance claims.

## Gaps that were discovered but are too implicit in the new six-primitive plan

These must be made explicit before production refactor begins; they do not require new root subsystems.

1. **G27 Context compaction governance** — place under P2 and artifact/context governance. Model compaction/summarization as a versioned execution-state transformation when it can affect pending obligations, approvals, tool/result pairing, provenance or replay semantics.
2. **G29 Runtime/protocol/provider compatibility** — place under P1/P2. Derive an environment/runtime compatibility declaration for the exact active substrate/integration combination; include protocol family/version, capability negotiation, provider/runtime version and evidence binding where material. Do not build a global compatibility matrix unless required by an active capability.
3. **G30 + G22 Evaluation/promotion lifecycle** — place under P3/P5 and existing evolution/artifact policies. Derive a single promotion trace from live/user failure evidence through reproducible eval, regression, measured result, promotion, online observation and retirement/supersession.
4. **G24 Writer-model transition trigger** — place under P1/P6. Define machine-readable threat/topology conditions that invalidate SINGLE_ACTIVE_CHAT and force consistency-model re-evaluation; do not implement consensus now.
5. **G03 Inter-owner interaction semantics** — P1 must include interaction mode, dependency direction, service expectation/backpressure and escalation, not only owner/authority nodes.
6. **G04 Environment/substrate model** — P1/P2 must explicitly represent execution environment, persistence, permissions/isolation and the assurance claim each environment can prove.
7. **G23 Multiple-fault analysis** — P4/P5 must include selected concurrent-fault combinations, not only typed single faults.
8. **G20/G21 Platform coupling and toil** — P5 should measure central coupling/context/tool cost and repeated manual evidence/cache/recovery work so architecture growth has an observable cost model.
9. **G14 Fitness-function map** — P3/P5 should expose a derived `architecture characteristic -> check/metric -> threshold/decision rule -> owner -> failure action` view rather than leaving fitness functions implicit across tests.

## Overall conclusion

- Prior architecture review: **broad functional coverage; no major control-plane function was completely omitted.**
- Six-primitive applicability screen: **directionally correct consolidation.**
- `23_refactor_execution_plan.md`: **not yet complete enough to be the implementation checklist.** It covers the largest high-risk items but leaves several previously discovered findings implicit.
- Therefore the next refactor should not start from plan 23 verbatim. Before M7 implementation, amend the design so the nine items above have explicit owners/landing points and acceptance evidence.
- This audit does not authorize those amendments or production mutation now; the user's instruction is to inspect first and implement later.
