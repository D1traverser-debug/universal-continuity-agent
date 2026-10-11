# Phase B — Top10 Selection After 10/10 Distillation

Status: SELECTION_COMPLETE__IMPLEMENTATION_DELTA_SEPARATE
Prerequisite satisfied: all ten entries normalized under one schema before selection.

## Selection rule

We are **not choosing the most popular Skills** and we are not installing/copying all ten.

Selection criteria:

1. **Evidence maturity** — implementation/eval evidence is stronger than prose popularity.
2. **Net-new value** — do not add a second mechanism when Universal already has an equal/stronger one.
3. **Cross-owner generality** — kernel only gets invariants that are genuinely cross-agent.
4. **Mechanical enforceability** — prefer runtime/schema/harness over extra prompt text.
5. **Context/complexity cost** — avoid hot-path growth and permanent Agents without unique responsibility.
6. **Failure containment** — preserve owner/business boundaries.
7. **Reversibility** — trial/observe before persistent architecture when possible.

## Whole-Skill disposition

| Skill | Disposition | Why |
|---|---|---|
| `find-skills` | **ADAPT METHOD** | Explicit capability-acquisition funnel closes a real “custom-build before reuse” gap. Do not import fixed popularity thresholds/global-install default. |
| `grill-me` | **ADAPT BOUNDED PRIMITIVES** | Decision tree/frontier + facts-vs-decisions are useful. Do not turn every task into a giant questionnaire or make user operate internal maintenance. |
| `grill-with-docs` | **EXTRACT PRIMITIVES, REJECT PROSE-ONLY COMPOSITION** | Inline crystallization and sparse durable-decision admission are useful; cross-Skill loading is source-acknowledged unreliable. |
| `improve-codebase-architecture` | **ADAPT MAINTENANCE HEURISTICS** | Payoff-weighted scan, deletion test, report-before-mutation and durable rejection memory fit architecture maintenance. Do not globalize its exact vocabulary/report stack. |
| `agent-browser` | **STRONGEST ARCHITECTURE REFERENCE** | Thin discovery Skill + runtime-versioned knowledge + session isolation + context-footprint eval + unknown-outcome semantics + final-state eval are the strongest executable patterns in Top10. |
| `tdd` | **ADAPT EVIDENCE/FEEDBACK PRIMITIVES** | Pre-agreed seam, independent expected truth, vertical tracer bullets and boundary-only mocks generalize to harness design. Do not pretend prompt guarantees red-before-green chronology. |
| `setup-matt-pocock-skills` | **ADAPT OWNER-ADMISSION/CONFIG METHOD** | Inspect-before-configure, ask only true choices, conditional setup, evidence-gated complexity and idempotent in-place updates fit new-owner onboarding. |
| `frontend-design` | **OWNER-LOCAL QUALITY METHOD** | Valuable for Video/visual-generation/UI owners, but subjective creative rules should not enter Universal kernel. Needs stronger independent visual eval before broad promotion. |
| `handoff` | **REFERENCE ONLY / UNIVERSAL ALREADY STRONGER** | Pointer-over-copy and purpose-conditioned compaction are already explicit in `CONTEXT_RECOVERY_POLICY`; Universal adds task/owner/stage/lease/version authority that source Skill lacks. |
| `triage` | **STRONG ADAPT TO SIGNAL/WORK-ADMISSION LAYERS** | Verify-before-clarify, explicit readiness states, durable Agent Brief and negative institutional memory directly complement Signal Plane and owner work admission. |

## Selected cross-agent primitives

### P1 — Capability acquisition before architecture creation

Source: `find-skills`.

Selected invariant:

`NEED → CHECK_INSTALLED/BUILT_IN → CURATED/TRUSTED SEARCH → SCOPED SEARCH → BROAD SEARCH → VERIFY → REVERSIBLE TRIAL → ADOPT → BUILD_ONLY_IF_NEEDED`

Reason: current Universal admission gate checks whether an **existing authority** can own a new mechanism, but it does not explicitly require checking whether an existing capability/Skill/Plugin/runtime already solves the need before custom-building one.

Promotion target: existing maintenance/learning authority, not a new Find-Skills Agent.

### P2 — Retrieve facts; ask humans only for genuine decisions

Sources: `grilling`, `setup`, `triage` independently reinforce this.

Selected invariant:
- environment/repository/tool facts are agent work;
- user questions are reserved for preferences, irreversible choices, genuinely unavailable facts, and explicit business decisions.

Boundary: this must **reduce** operator dependence, not become a reason to interview the user about internal architecture.

Promotion target: maintenance autonomy/meta-maintenance decision model.

### P3 — Dependency frontier for unresolved decisions

Source: `grilling`.

Selected in bounded form:
- when multiple genuine user decisions remain, model prerequisites;
- batch independent decisions;
- defer dependent decisions;
- do not block unrelated work on one pending fact.

Not selected as universal default conversation style. Full grilling requires explicit/high-impact design need.

### P4 — Inline crystallization with sparse durable admission

Source: `grill-with-docs` / `domain-modeling`.

Selected principle:
- when a material term/decision becomes stable, persist it at the smallest correct authority immediately;
- do not batch all durable capture to session end;
- only create new durable decision artifacts when reversibility/surprise/trade-off or equivalent owner criteria justify them.

Universal already has authority-surface admission and chat-only material-change rules, so this mostly validates/clarifies existing direction rather than creating a new subsystem.

### P5 — Payoff-weighted maintenance + deletion test

Source: `improve-codebase-architecture` + `codebase-design`.

Selected invariant:
- before adding/refactoring an abstraction, ask whether deleting it would **concentrate** complexity elsewhere or merely remove pass-through ceremony;
- prioritize maintenance where repeated change/incidents/future work justify payback.

This is stronger than generic “simplify” wording and is directly relevant to anti-bloat governance.

### P6 — Thin stable discovery surface + runtime-versioned operating knowledge

Source: `agent-browser`.

Selected as an **optional architecture pattern**, not a mandatory implementation for every owner.

Use when:
- executable runtime has a versioned operating surface;
- static Skill instructions risk drifting from runtime;
- runtime can expose current Skill/reference content cheaply.

Invariant:
- thin installed/router surface points to current runtime-owned instructions;
- evaluator checks agents actually load the right current content;
- static discovery surface does not duplicate runtime manual.

This sharpens Universal's existing Thin Skill architecture by identifying a particularly strong way to implement it.

### P7 — Context footprint is measurable, not rhetorical

Source: `agent-browser` evals.

Selected invariant:
- when claiming a new router/bootstrap/tool exposure is “thin” or more efficient, measure bytes/approx tokens/tool surface rather than relying only on prose/line count.

Universal already enforces Skill byte budgets, but cross-path context footprint comparison remains weaker than agent-browser's dedicated measurement.

### P8 — Explicit mutation `outcome_unknown`

Source: `agent-browser` current runtime fix.

Selected invariant:
- if a non-idempotent mutation may have reached the executor but the response was lost, do **not** blindly retry;
- re-observe state or classify outcome unknown;
- read-only/pre-send failures may use different retry rules.

This fills a real cross-agent operational-hygiene gap beyond “reread after successful write.”

Promotion target: artifact/operation transaction semantics.

### P9 — Independent expected truth / evidence seam

Source: `tdd`, reinforced by `triage` and `agent-browser` final-state grading.

Selected invariant:
- before evaluating a behavior, define where it is observed and where expected truth comes from;
- verifier must not compute expected output with the same logic it is supposed to test;
- tests/evals should prefer public behavior/final state over implementation-detail self-report.

Universal already has evidence-ceiling and independent-verifier concepts; this adds a useful “evidence seam + independent oracle” formulation.

### P10 — Tracer-bullet validation

Source: `tdd`.

Selected invariant:
- for uncertain multi-layer changes, prove one narrow end-to-end path first, then expand based on evidence;
- avoid writing the entire test/implementation architecture from imagined behavior before the first real trajectory.

This is especially appropriate for new owner/runtime integrations.

### P11 — Inspect → recommend default → ask only unresolved choices

Source: `setup-matt-pocock-skills`.

Selected for owner onboarding/configuration:
- inspect current environment first;
- derive defaults from evidence;
- hide irrelevant options;
- ask user only when a real choice remains;
- update existing canonical config in place rather than create parallel authority.

This directly supports the user's requirement not to be the internal maintenance operator.

### P12 — Evidence-gated complexity admission

Source: `setup` + `improve-codebase-architecture`.

Selected invariant:
- advanced/multi-context/additional-layer architecture is not offered merely because it exists;
- admit complexity only when topology, repeated failure, scale or real variation demonstrates need.

### P13 — Verify before clarify before delegate

Source: `triage`.

Selected invariant:
- re-observe the claim against current environment before asking a long set of clarification questions;
- only then determine whether work is ready, needs information, needs human judgement, or can be delegated.

This is highly compatible with current Signal Plane's “re-observe before acting.”

### P14 — Durable agent-ready brief separate from noisy history

Source: `triage`.

Selected pattern for work admission:
- behavior/current state/desired state;
- stable interfaces/contracts;
- testable acceptance criteria;
- explicit out-of-scope;
- avoid line-number/file-layout micromanagement that will stale.

Potential target: owner work-order/task handoff conventions, not Universal business truth.

### P15 — Negative institutional memory

Source: `triage`, also architecture ADR rejection and frontend anti-default knowledge.

Selected invariant:
- durable rejection/failure rationale should be searchable by **concept/failure class**, so the system does not relitigate or reintroduce rejected mechanisms;
- temporary “not now” must not be misclassified as permanent rejection.

Universal already stores incidents/failure classes; this suggests making rejected architecture/capability decisions equally searchable rather than leaving them only in old audit prose.

## Owner-local selections

### Video / visual-generation owners

From `frontend-design`:
- brief-grounded aesthetic direction;
- compact visual plan before generation/build;
- counterfactual genericity test;
- one-bold-gesture restraint;
- rendered/screenshot critique;
- known-model-default catalog as a **justification trigger**, not absolute blacklist.

Do not promote these subjective design rules into Universal kernel.

### Engineering-heavy owners

From `tdd`:
- behavioral seams;
- independent oracles;
- tracer-bullet slices;
- boundary-only mocking.

Adopt through owner Harness/method profiles when relevant, not mandatory for writing/video tasks.

## Already stronger in Universal — do not duplicate

### Handoff/context recovery

External `handoff` contributes useful simplicity, but current Universal already requires:
- task_id/owner/stage/next_action;
- blockers;
- authority/contract version;
- exact artifact refs;
- optional lease/epoch;
- pointer-over-copy;
- old chat only as last resort.

Therefore no new handoff subsystem is selected.

### One canonical authority / avoid parallel steering

`setup` reinforces an invariant Universal already uses extensively. No new root config layer.

### Signal re-observation before action

`triage` validates current Signal Plane consumption design; no duplicate triage control plane is needed.

## Explicitly rejected mechanisms

1. **Install/popularity thresholds as hard quality gates.**
2. **Global install as default after discovery.** Reversible/local trial preferred where possible.
3. **One-line Skill delegation as proof dependency executed.** `grill-with-docs` documents real failures here.
4. **Chat-only decision state for long-running work.**
5. **Prompt-only chronology claims** such as red-before-green without execution evidence.
6. **Same-agent visual self-critique as independent quality proof.**
7. **CDN-dependent diagnostic report as required control-plane artifact.**
8. **Fixed question counts or always-grill behavior.**
9. **Architecture review that must always output findings.** No-change is a legitimate result.
10. **Copying all Top10 methods into Universal Skill/startup context.** Selected methods belong in existing cold-path policy/runtime/harness or owner-local profiles.

## Highest-value findings by evidence + fit

### Tier 1 — strongest system-level value

1. `agent-browser`: thin/runtime-versioned Skill architecture, context-footprint eval, session isolation, `outcome_unknown`, independent final-state eval.
2. `triage`: work-admission state, verify-before-clarify, agent-ready brief, negative memory.
3. `find-skills`: explicit reuse-before-build capability acquisition.
4. `setup-matt-pocock-skills`: inspect/default/ask-only-real-choice and evidence-gated setup complexity.
5. `tdd`: independent expected truth/evidence seam and tracer bullets.

### Tier 2 — valuable bounded methods

6. `grill-me`: dependency frontier and facts-vs-decisions.
7. `improve-codebase-architecture`: deletion test, payoff weighting, report-before-mutation.
8. `grill-with-docs`: inline crystallization and sparse persistence.

### Tier 3 — scoped/reference

9. `frontend-design`: strong owner-local creative method, weak cross-agent generality/eval.
10. `handoff`: useful minimalist reference, but Universal's current recovery contract is materially stronger.

This ranking is **not** the original install ranking. It is the result of complete normalized comparison against the current system.

## Implementation boundary

Selection is complete. Promotion into live control-plane authority should modify existing surfaces rather than create a “Top10 policy” or new supervisory Agent.

Candidate bounded deltas:

- `SYSTEM_MAINTENANCE_POLICY.json`: capability-reuse discovery, facts-vs-decisions, payoff/deletion-test decision points.
- `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`: explicit non-idempotent `OUTCOME_UNKNOWN` retry semantics.
- existing Harness/tests: context-footprint/evidence-seam regression where mechanically useful.
- Signal Plane/work-order conventions: verify-before-clarify and agent-ready brief, only where a real missing control exists.
- owner-local visual methodology: separate future Video/visual maintenance, not kernel.

No selected mechanism justifies a new permanent root Agent.
