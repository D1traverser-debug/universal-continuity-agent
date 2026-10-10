# Cross-Agent Methodology Composition Review — 2026-10-10

Status: UNIVERSAL SELF-PILOT ACTIVE
Scope: Universal Continuity control plane; owner rollout not yet claimed complete

## Trigger

The user raised a valid systems question: common capabilities such as artifact I/O, cleanup, reliability management and evolution should not need to be re-taught independently to every business Agent, but a giant parent/child inheritance tree could make both the Universal parent and domain children bloated, tightly coupled and difficult to evolve safely.

A second reliability defect was exposed during discussion: the assistant initially followed the user's UVM `extends` analogy too readily. That led to the epistemic-independence hardening already present in `SYSTEM_MAINTENANCE_POLICY.json` v1.4 and `CONTINUOUS_LEARNING_POLICY.md`: user goals/constraints may be requirements, but user-proposed mechanisms, assistant first ideas and other framework proposals are candidates that require independent comparison and failure-mode search.

This review therefore did not assume inheritance, composition or modules in advance. It evaluated practical operating patterns and then piloted the chosen model in Universal itself before owner rollout.

## Practical evidence reviewed

### controller-runtime / Kubernetes reconciliation

The actual `controller-runtime/pkg/reconcile/reconcile.go` implementation exposes a narrow `Reconciler` contract. Reconciliation is level-based: the controller re-reads actual state and compares it with desired state rather than treating the triggering event description as durable truth. Separate resource types normally use separate controllers.

Practical implication for Universal: share a small reconciliation/authority contract, but keep domain-specific business reconciliation local to each owner.

Source: `kubernetes-sigs/controller-runtime`, `pkg/reconcile/reconcile.go`.

### Backstage backend plugins/modules

Backstage's production backend uses services plus extension points. Modules extend one plugin through explicitly exported extension points; the documentation recommends multiple narrow extension points rather than a few very large ones because smaller surfaces are easier to evolve and deprecate. Modules are initialized before the plugin and do not need to depend directly on the plugin implementation package.

Practical implication: reusable cross-agent behavior should expose narrow hook contracts and owner-local implementations rather than forcing owners to copy a giant shared behavior document.

Sources: Backstage backend architecture, plugin modules and extension-point documentation.

### OPA bundles / ownership roots

OPA bundles make policy/data ownership explicit through roots. With multiple sources, overlapping ownership creates conflicts and can put OPA into an error state; scoped roots constrain what a bundle can overwrite. OPA explicitly warns that multiple sources have no load-order guarantee and recommends central aggregation when possible.

Practical implication: shared methodology profiles need explicit ownership/namespaces and forbidden cross-profile overrides. A child owner must not silently shadow a kernel invariant or another profile.

Source: Open Policy Agent `Bundles` documentation.

### Temporal durable workflow evolution

Temporal replays durable Event History against Workflow code. Running executions can break when new code is nondeterministic relative to recorded history, so Temporal recommends Worker Versioning for safe production evolution and uses patching as a compatibility fallback. Running state is not simply overwritten by whatever code is newest.

Practical implication: owner methodology/profile versions must be pinned and compatible; floating `latest` is unsafe for durable tasks.

Sources: Temporal Workflow Definition, Worker deployment/versioning and Event History documentation.

### OpenAI Agent Improvement Loop

OpenAI's practical improvement-loop example starts from execution traces plus human/model feedback, converts them into rerunnable evals, gates changes, ranks harness improvements and hands evidence-backed changes to Codex. The harness is treated as the entire contract around the model: instructions, tools, routing, output requirements and validation.

Practical implication: durable evolution must remain evidence/eval-gated; naming an Evolution Agent or writing a learning document is not production evolution.

Source: OpenAI Developers, `Build an Agent Improvement Loop with Traces, Evals, and Codex`, 2026-05-12.

## Candidate architectures considered

### Rejected: giant parent-Agent inheritance tree

Reason:
- encourages a God Object that gradually learns every domain;
- base-class changes can have wide, implicit blast radius;
- child overrides can silently weaken safety semantics;
- durable old owners become difficult to version independently;
- inherited prose still has to be loaded and interpreted, so inheritance alone does not solve context cost.

UVM-style reuse remains a useful analogy for base invariants plus controlled override, but it is not the architecture.

### Rejected: copy common policies into every owner repository

Reason:
- creates N drifting copies;
- requires repeated owner migrations for compatible policy improvements;
- makes it hard to know whether a child is actually on the current shared method;
- increases prompt/context surface and maintenance burden.

### Rejected: Universal owns every domain evolution pipeline

Reason:
- domain evaluation is fundamentally different across Financial Writing, Video Growth, A-share and Novel;
- centralizing domain methods would violate owner/business-truth boundaries;
- Universal would become both control plane and business executor.

### Accepted pilot: small stable kernel + composable methodology profiles + owner-local bindings + executable conformance

The pilot is now implemented in `OWNER_ADAPTER_CONTRACT.json` without adding a new root methodology policy.

Kernel invariants include authority precedence, single-writer lease, verified commit, candidate/production separation, evidence-gated promotion and destructive-mutation safety.

Profiles:
- `artifact_io@1.0`
- `operational_hygiene@1.0`
- `evolution@1.0`

Each profile points to an existing semantics owner instead of duplicating prose. Owners pin exact profile versions and bind domain-local hooks. Allowed specialization includes implementation binding, taxonomy, thresholds, artifact locations, evaluator choice and safe domain retention. Forbidden overrides include kernel authority/evidence/lease/commit/destructive-mutation invariants.

`runtime/methodology_conformance.py` mechanically validates profile versions, required hooks and forbidden overrides. `tests/test_methodology_conformance.py` proves:
- thin owner bindings can compose all three profiles;
- floating `latest` fails;
- a missing post-write verification hook fails;
- attempting to override `candidate_is_not_production_authority` fails;
- no parallel `METHODOLOGY_POLICY.json` / `METHODOLOGY_PROFILE_POLICY.json` may appear.

Initial composition CI: run `38035540056`, job `114165070221`, head `adec4dbede134648b427022e79fed364d8087d39`, `99 passed`.

## Universal-first hot-path audit

The initial repository still contained a contradiction: `ENTRYPOINT.md` said broad research/context must stay off the hot path, yet ended with an 11-file `Read next` list. `STARTUP_HOOK.md` also told chats to preload `ENTRYPOINT`, `SYSTEM_BLUEPRINT`, protocol/bootstrap/owner/discovery/maintenance surfaces before knowing which action was needed.

That was not acceptable as a model for child owners.

Changes:
- `ENTRYPOINT.md` now defines a minimal bootstrap of `ENTRYPOINT.md + CURRENT_PROTOCOL.json` and an event-driven authority-loading matrix;
- `STARTUP_HOOK.md` now routes first and loads only event-specific authorities;
- `SYSTEM_BLUEPRINT.md` is now a small-kernel/composable-profile architecture map and explicitly says referenced authorities are ownership pointers, not a command to preload them;
- `SYSTEM_BLUEPRINT`, audits/research, unrelated owners, inactive profiles and old transcripts are cold-path by default;
- methodology profiles are loaded only when their activation event occurs.

`ENTRYPOINT.md` shrank from roughly 11.2 KB to roughly 8.9 KB while adding the composition/load matrix. More important than byte count, the fixed 11-file preload instruction was removed.

## Regression evidence from slimming

The hot-path refactor intentionally relied on existing tests to detect semantic over-deletion. Three intermediate CI failures were useful and were not suppressed:

1. run `38035776737`: `101 passed / 1 failed` because the slimmed account hook had dropped explicit coverage of already-open/inherited durable chats;
2. run `38035840541`: `101 passed / 1 failed` because mandatory final `进度提交` wording had been weakened;
3. run `38035972287`: `101 passed / 1 failed` because the slim blueprint dropped the explicit `VERSION_LIFECYCLE_POLICY.json` ownership pointer.

All three were classified as real invariants, restored without restoring broad preload behavior.

Final current engineering validation for this refactor:
- run `38036023965`
- job `114166494334`
- head `f07c3b5a6a746f0adb70ed1878093d659c60b7c9`
- package `universal-continuity-agent 3.7.0`
- pytest `102 passed in 0.20s`

This is the desired practical behavior: slimming is accepted only when tests prove required semantics survived.

## Current architecture decision

Current accepted direction:

`SMALL STABLE KERNEL`
`+ VERSIONED COMPOSABLE METHODOLOGY PROFILES`
`+ OWNER-LOCAL HOOKS / DOMAIN EXTENSIONS`
`+ CENTRAL EXECUTABLE CONFORMANCE`
`+ EVENT-DRIVEN LOADING`

This is not unrestricted self-modification and is not a universal parent class.

Universal owns cross-agent invariants and profile contracts. Domain owners own business-specific implementation/evidence/evaluation. Children may specialize the method, but cannot bypass kernel evidence, authority, lease, commit or destructive-mutation safety.

## Owner rollout rule

Do not copy these profiles wholesale into Financial Writing, Video Growth, A-share or Novel.

During a valid owner maintenance/writer turn:
1. declare only the profiles that owner actually needs;
2. pin exact supported profile versions;
3. bind existing domain-local hooks to profile hooks;
4. retain domain-specific evolution pipelines locally;
5. run `methodology_conformance` plus owner-specific regression/eval;
6. only after all supported readers migrate may legacy duplicated `owner_must_expose` mirrors be removed.

Financial Writing's writing-feedback/eval method and Video Growth's Methodologist/Evolution-candidate/Red-Team learning sequence remain domain implementations; they should consume shared evolution invariants rather than be replaced by one universal learning algorithm.

## Remaining boundaries / risks

1. Profile packaging is currently a contract/runtime pilot in Universal, not yet a separately distributed package/service. Do not claim every owner has inherited it until each owner declaration and conformance test is present.
2. The account-level Custom Instructions product surface does not update merely because GitHub changed. The new minimal-bootstrap semantics require real account/existing-chat/fresh-chat product evidence before claiming propagation.
3. No background scheduler/event watch exists. Reconciliation/maintenance/evolution runs on active material/maintenance turns unless a real scheduled/watch executor is added.
4. Profile version compatibility/migration needs real owner evidence once the first profile contract changes; v1.0 alone does not prove future migration is correct.
5. Universal still has multiple root contracts/policies. The new admission gate + event-driven loading reduces hot-path bloat, but future maintenance should continue to consolidate any surface whose unique ownership no longer justifies existence.

## Next action

Use Universal as the reference implementation. Migrate owners incrementally on their valid maintenance/writer turns, beginning with owners already having strong runtime evidence (Financial Writing and Video Growth) only after confirming the profile binding reduces duplication rather than adding another layer. Continue A-share/Novel operational-hygiene conformance separately. Keep product-level Custom Instructions/session propagation and fresh-chat E2E as explicit external validation boundaries.
