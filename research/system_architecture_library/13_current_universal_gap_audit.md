# 13 — Current Universal Gap Audit Against the Benchmark Library

Status: `DIAGNOSIS_ONLY / NO_REFACTOR_AUTHORIZED`  
Baseline: `main@11d0657cfa42e41b4ed8ecbf1df716baa6450730`, Universal durable revision `UC-20261013-r91` before this research checkpoint.

## Scope actually inspected

Current-system evidence used:

- `ENTRYPOINT.md`
- `SYSTEM_BLUEPRINT.md`
- `ORCHESTRATION_BLUEPRINT.md`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `OWNER_REGISTRY.json`
- `OWNER_ADAPTER_CONTRACT.json`
- `EXECUTION_READINESS_CONTRACT.json`
- `CONTROL_SIGNAL_CONTRACT.json`
- `runtime/maintenance_controller.py`
- `runtime/system_audit.py`
- `runtime/mutation_outcome.py`
- v67 global audit and v68 current maintenance handoff/manifest
- code-search negative checks for SLO/error-budget, TLA/STPA/MAPE/UVM/FDIR/supervision/coverage-traceability terminology.

Absence of a named framework is not itself a defect. Findings below are based on missing *capability/question/evidence*, not missing brand names.

## Priority model

- **HIGH** — current control/assurance blind spot with material relevance to continuity, mutation integrity, recovery or architecture evolution.
- **MEDIUM** — meaningful maintainability/reliability gap that does not presently prove unsafe behavior.
- **CONDITIONAL** — only becomes a defect if the threat model/topology changes.
- **STRENGTH** — current design already satisfies much of the benchmark; do not rebuild it.

## Findings

### G01 — Architecture benchmark taxonomy is not a durable part of the maintenance method — HIGH

**Evidence:** v67's bounded global audit inspected many concrete control-plane surfaces, but its scope taxonomy did not include control/reconciliation, supervision, formal methods, hazard analysis, SLO/error-budget, environment parity, verification coverage, or common-mode independence as explicit architecture families. The user had to enumerate these dimensions again.

**Why it matters:** a “global” audit can be internally complete against its checklist while the checklist itself has a blind spot.

**Root layer:** maintenance meta-method / learning-scout breadth.

**Status:** confirmed method gap. The present library repairs knowledge availability, not the runtime method.

### G02 — No unified system-outline / architecture graph view — HIGH

**Current strengths:** `SYSTEM_BLUEPRINT.md`, registry pointers, state/signal-plane prose and owner manifests expose many relationships.

**Gap:** there is no single **derived, non-authoritative** graph/view joining owners, authorities, environments, control loops, state transitions, signal paths, dependencies, effectors, evidence obligations and recovery boundaries.

**Risk:** impact analysis remains partly prose/manual; interaction omissions are harder to detect.

**Constraint:** creating a new central authority would be worse. Any future graph should be generated from existing authorities plus explicitly non-authoritative annotations.

### G03 — Inter-owner interaction contracts are under-specified — HIGH

`OWNER_REGISTRY.json` says who owns what and where authority lives. It does not first-class the interaction mode, dependency direction, service expectation, backpressure, escalation, temporary collaboration, or facilitation relationship between Universal and an owner or among owners.

This is distinct from ownership. A dependency can be clear in code yet operationally ambiguous in failure and upgrade paths.

### G04 — Environment/substrate architecture is fragmented — HIGH

`EXECUTION_READINESS_CONTRACT.json` correctly separates declared, wired, session-executable and isolated capabilities. However there is no one environment matrix covering ChatGPT chat, GitHub connector, GitHub Actions, owner Python/runtime, chat-bridged execution, MCP/plugin, external product state and independent verifier contexts.

Missing cross-environment questions include parity, permissions, persistence, isolation, promotion of evidence, destructive-test eligibility, secrets, rollback and what claim each environment can prove.

This is directly relevant to the earlier user confusion over “GitHub has the code” versus “this chat can execute the backend.”

### G05 — No quantitative Universal SLI/SLO/error-budget governance — HIGH

No current repository evidence defines measurable service objectives for inheritance correctness, false-commit prevention, routing accuracy, recovery, bootstrap latency, stale-writer behavior, external-state freshness or user-restatement reliability.

The system has hard deterministic gates but no quantitative reliability budget governing change velocity or freeze policy.

### G06 — No complete requirement/invariant -> implementation -> verification -> validation trace matrix — HIGH

Universal has contracts, runtime checks and tests, but no bidirectional matrix proving for every material architecture invariant:

`goal/requirement -> owner -> implementation/guard -> unit/trajectory/fault test -> independent/live evidence -> residual risk`.

This is the largest V-model/DO-178C/NASA-style assurance gap. It enables “test exists” and “rule exists” without mechanically proving every rule has an executable verification path or every test maps to a current requirement.

### G07 — No formal model checking for core writer/authority algorithms — HIGH assurance gap

The lease/resume-epoch/HEAD-CAS/state-signal rules are concurrency-sensitive. Tests and synthetic fault scenarios are strong but trace-selected. No TLA+/equivalent formal model explores bounded interleavings for stale-writer safety, CAS races, unknown mutation outcomes and commit-receipt invariants.

This is not evidence of an existing bug. It is missing assurance on the system's highest-value algorithmic invariants.

### G08 — Runtime supervision/recovery topology is not explicit — HIGH

The maintenance controller can block/reopen and policy contains owner-scoped failure containment, but there is no dependency-aware supervision model comparable to OTP's `one_for_one`/`one_for_all`/`rest_for_one`, restart intensity, escalation and safe shutdown.

Tool/runtime/owner/cache failures therefore have individually designed recovery semantics rather than a shared analyzable recovery topology.

### G09 — FDIR decomposition is incomplete — HIGH

Signals and triage cover detection; owner scoping provides some containment. But fault **isolation**, recovery mode, degraded state, retry/restart budget, escalation and concurrent-fault interactions are not uniformly represented across subsystems.

A failure can be classified without the system having a standard answer for “what exactly is isolated, what remains healthy, what recovers automatically, and when do we stop?”

### G10 — System-level hazard / unsafe-control-action model is absent — HIGH

Current failure classes are incident/defect oriented. There is no STPA-like layer starting from unacceptable system outcomes and deriving unsafe control actions for takeover, commit, retry, re-enable, invalidate, delegate, delete or promote actions.

This means the system may miss unsafe interactions where every component behaves nominally but timing/order/context makes the control action wrong.

### G11 — Verification coverage closure is absent — MEDIUM-HIGH

`runtime/system_audit.py` retains a valuable list of synthetic fault scenarios. There is no coverage model answering which lifecycle states, transition edges, owner/profile combinations, environments, interaction modes, failure/recovery classes and authority conflicts have or have not been exercised.

Number of tests is not coverage closure.

### G12 — Driver/monitor/reference-model separation is only partial — MEDIUM

Universal carefully separates self-attested from independent evidence, but not every subsystem explicitly identifies the actor driving a change, the passive monitor observing it, and the expected reference model/scoreboard evaluating it. Some checks derive expectation from the same configuration they validate, creating possible common-source blind spots.

### G13 — Multi-model/agent common-mode failure is under-modeled — MEDIUM-HIGH

The system correctly refuses to equate role-play with independent review. It does not yet maintain an independence matrix across provider/model, context, prompt/specification, evidence source, tool/runtime, evaluator/reference model and upstream authority.

Thus future “5-model” or N-reviewer workflows could overclaim diversity while sharing the same failure source.

### G14 — Architectural fitness functions are fragmented — MEDIUM

Tests/audits defend many architectural characteristics, but no derived map says:

`architecture characteristic -> metric/check -> threshold -> owner -> failure action`.

This weakens evolutionary-architecture governance and makes it harder to know which quality has no executable protection.

### G15 — MAPE-K knowledge is disciplined but not typed as a control-loop knowledge view — MEDIUM

Authority precedence is strong. Yet policies, manifests, checkpoints, observations, incidents, research, execution receipts and live external evidence are scattered knowledge classes. There is no derived control-loop view specifying what knowledge each monitor/analyzer/planner/executor may consume and at what freshness/authority.

Do **not** fix this by building one giant knowledge database; the likely need is a typed view over existing authorities.

### G16 — GitOps desired/observed/reconciler applicability is not inventoried per resource — MEDIUM-HIGH

Current policy correctly says external live state can outrank stale repository observations. But no resource inventory declares desired-state authority, observed-state authority, reconciler, consent, reconciliation mode and idempotency per managed resource.

The historical monitor-deletion incident shows why this distinction matters.

### G17 — Shared control-plane rollout/canary strategy is ad hoc — MEDIUM

v68 prudently piloted Human Durable Revision only in Universal and deferred owner rollout, which is a good pattern. But there is no reusable progressive-rollout/canary/shadow protocol for cross-owner control-plane changes with entry/exit criteria, observation period, rollback and promotion.

### G18 — Chaos/fault-injection experiments lack explicit steady-state and blast-radius contracts — MEDIUM

Synthetic fault injection is already present. The missing layer is a formal experiment declaration: steady-state metric, fault variable, environment, blast radius, abort condition, recovery expectation and evidence.

### G19 — Retry/backoff/idempotency semantics are not shared across external mutations — MEDIUM-HIGH

`runtime/mutation_outcome.py` handles unknown outcomes well. `EXECUTION_READINESS_CONTRACT` binds execution receipts. There is no shared per-capability contract for idempotency key, semantic equivalence, timeout, retry layer, backoff/jitter cap and post-timeout reconciliation.

### G20 — Platform/control-plane responsibility growth is not measured — MEDIUM

Universal coordinates routing, continuity, execution readiness, methodology profiles, signals, remote observations, maintenance, learning/evolution, architecture audit and progress observability. Anti-bloat rules exist, but there is no operational measure of owner cognitive/context load, central coupling or platform bottleneck cost.

### G21 — Operational toil is not quantified — MEDIUM

Repeated manual cache convergence, evidence assembly, owner scanning, user restatement and ad hoc environment diagnosis can accumulate without a toil budget. Current anti-bloat logic is qualitative.

### G22 — Promotion lifecycle is not uniform across all knowledge/change types — MEDIUM

Candidate-vs-authority separation is strong, but research, architecture candidates, test prototypes, temporary branches, owner pilots and production rules do not all share one machine-readable promotion/supersession lifecycle. Different subsystems implement parts of it.

### G23 — Concurrent/multiple-fault analysis is not first-class — MEDIUM-HIGH

Tests exercise named single scenarios and some races, but NASA-style analysis of simultaneous faults and interactions between nominal control and recovery control is not a required audit dimension.

Examples: stale writer + provider timeout + external head movement; owner outage + stale cache + delayed signal; independent-review outage + fallback route + user urgency.

### G24 — Writer-model transition trigger is not formally governed — CONDITIONAL

The current `SINGLE_ACTIVE_CHAT` + lease + HEAD CAS design is intentionally sufficient for the current threat model. The gap is not “missing Raft.” The gap is that no machine-readable trigger says when topology changes—multiple authoritative writers, replicated state, autonomous parallel reconcilers—force reclassification and a new consistency model.

Do not implement consensus now.

## Existing strengths that should not be discarded

1. Minimal hot-path bootstrap and cold-path maintenance loading.
2. Single source of owner membership via `OWNER_REGISTRY.json`.
3. Clear domain-owner boundary; Universal may not rewrite BUSINESS truth.
4. Active lease/resume epoch and stale-writer protection.
5. Direct-main observed-HEAD CAS under the current writer model.
6. State plane vs non-authoritative signal plane.
7. Current-session execution readiness separated from repository declaration.
8. Action-bound receipts and anti-replay checks.
9. Self-attested versus isolated/independent assurance distinction.
10. Deterministic maintenance controller with reopen/invalidation.
11. Synthetic fault-injection regression suite.
12. Anti-bloat and authority-surface admission rules.
13. Candidate/learning evidence separated from production authority.
14. Bounded closure claims rather than false global perfection.

## Bottom line

The current system is not “bad”; it is **strong in authority, continuity, evidence honesty and bounded maintenance**, but **underdeveloped in architecture-wide reliability science**: measurable reliability, environment modeling, supervision/FDIR, hazard/control analysis, formal verification, coverage closure, inter-owner interaction topology and cross-framework benchmark discipline.

This audit intentionally stops before implementation. Every proposed repair remains a candidate until the user issues a separate refactor command and the maintenance controller enters M7.
