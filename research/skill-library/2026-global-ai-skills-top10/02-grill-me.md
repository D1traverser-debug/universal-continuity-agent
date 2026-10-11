# 02 — `grill-me`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned repository HEAD: `49dd158d1076134a641b33efb035946536778336`
- Wrapper Skill: `skills/productivity/grill-me/SKILL.md`
- Wrapper blob: `3947ff9c4ad980d14fc07fccbf659d47c114e81d`
- Shared primitive: `skills/productivity/grilling/SKILL.md`
- Primitive blob: `df69d9936880cd3314c28858c6c52f48db23b856`
- User documentation: `docs/productivity/grill-me.md`
- Mechanism documentation: `docs/productivity/grilling.md`
- Repository docs/out-of-scope notes inspected for question-count and invocation design.

The wrapper is intentionally tiny; most behavior lives in the delegated `grilling` primitive. Treating only the wrapper as the Skill would miss nearly all methodology.

## B. Problem model and intended outcome

Problem: people begin with a vague idea, plan, decision or design and either:

- rush to implementation before exposing hidden decisions;
- ask an agent to produce a polished plan that silently chooses for them;
- serially answer questions without understanding dependency structure;
- confuse facts the environment can supply with decisions only the human should make.

Desired outcome: turn a loose idea into a set of consciously owned decisions and a shared human/agent understanding **before action**.

Architectural role:
- `grill-me`: manual, stateless front door;
- `grilling`: reusable decision-elicitation primitive.

It intentionally does not persist decisions, implement the result, produce a formal spec, or resolve questions that require seeing/prototyping rather than talking.

## C. Activation and invocation model

### Wrapper activation

`grill-me` has `disable-model-invocation: true`. It is explicitly user-invoked.

Its entire executable instruction is effectively “call the `grilling` Skill.” This is deliberate composition, but creates a dependency-loading risk.

### Primitive activation

`grilling` may be invoked directly or automatically when another Skill needs an interview.

### Recommended timing

- early, while the idea is still vague;
- preferably a fresh conversation for the standalone wrapper;
- before the agent has already written a plan that could anchor subsequent questioning.

### Stop rule

The session is not done merely when the model runs out of questions. It ends when:

1. the design-tree frontier is empty; and
2. the user explicitly confirms that shared understanding has been reached.

The primitive must not move into implementation on its own.

## D. Inputs, outputs, side effects

### Inputs

- the user's loose idea/decision/design;
- user answers per round;
- environmental facts discovered by the agent/sub-agent.

### Outputs

- clarified decision tree;
- shared conversational understanding;
- explicit decisions and reopened branches when contradictions emerge.

### Durable side effects

None. `grill-me` is intentionally stateless and writes no files.

### Important consequence

The useful product is mostly **context in the current conversation**. Clearing context destroys most of the value unless another Skill (for example `to-spec`) captures it.

## E. End-to-end workflow

### G0 — Scope intake

Entry: user invokes with a loose idea.

Agent constructs an implicit **design tree**: decisions with dependent decisions beneath them.

No implementation occurs.

### G1 — Compute the frontier

The frontier contains every decision whose prerequisites are already settled.

Rule:
- if Q2 depends on Q1, they may not appear in the same round;
- unrelated/unblocked decisions can appear together.

The graph is not actually computed by deterministic code. The model judges dependencies.

### G2 — Ask a round

Ask the whole frontier at once.

Each question:
- numbered;
- titled;
- can include multiple choices/context;
- followed by the agent's recommended answer;
- ideally worded so “yes” accepts the recommendation.

This lets the user respond compactly by number.

### G3 — Parallel fact acquisition

If a question depends on a fact the environment can answer:
- the agent must look it up rather than ask the user;
- it may dispatch a sub-agent;
- only downstream questions wait for that fact;
- unrelated frontier questions proceed immediately.

This is a dependency-aware partial-blocking model.

### G4 — Human decision input

The user answers decisions. The agent must not answer its own decision questions.

An answer may:
- settle a branch;
- change assumptions;
- reopen prior branches;
- reveal new dependent questions.

### G5 — Recompute frontier

Build the next round from scratch based on settled decisions and newly available facts.

### G6 — Detect ungrillable question

If an answer cannot reasonably be obtained from discussion—for example visual feel or choosing between experiential variants—the documented guidance is to stop interviewing and build/prototype something the user can react to, then return with the new evidence.

### G7 — Closure gate

When no unresolved branch remains, ask the user to confirm shared understanding.

Only after confirmation can another flow consume the result.

## F. Core methodology / mental model

### Design tree

Decisions form a dependency tree/graph rather than a flat checklist.

### Frontier scheduling

Ask only decisions whose prerequisites are resolved. This is effectively a topological wave/frontier heuristic.

### Batch independent questions, serialize dependent ones

The methodology tries to reduce round-trip latency without collapsing causal order.

### Facts vs decisions

- facts: agent/environment responsibility;
- decisions: human responsibility.

This is one of the strongest methodological boundaries in the Skill.

### Recommendation-first questioning

The agent does not pretend to be neutral. It proposes a recommended answer so the user can accept/reject quickly.

### Active disagreement as a quality signal

Documentation warns that a user who simply says “agreed” to dozens of questions may have outsourced decision-making rather than clarified it.

### No fixed question budget

The source deliberately rejects a hard question ceiling. Scope, not arbitrary count, determines how many questions are needed.

## G. Decision-rights model

### User owns

- scope;
- trade-offs/preferences;
- final decisions;
- whether shared understanding is sufficient;
- whether to stop/wrap early.

### Agent owns

- identifying hidden decisions;
- dependency ordering;
- recommendations;
- environmental research;
- surfacing contradictions and new branches.

### Environment/sub-agent owns

- empirical facts it can observe.

Failure condition: if the agent answers the user's decisions itself, the source explicitly treats the run as broken.

## H. State machine and lifecycle

Implicit conversational states:

`IDEA → DESIGN_TREE_FORMED → FRONTIER_ROUND → USER_ANSWERS → FRONTIER_RECOMPUTED → ... → FRONTIER_EMPTY → USER_CONFIRMATION → DONE`

Special branches:
- fact dependency → background lookup → downstream branch waits;
- ungrillable decision → prototype/evidence detour;
- discovered dependency error → reopen branch.

State is not machine-readable or durable; it lives in model context.

## I. Memory, durability, provenance

Stateless by design.

No glossary, ADR, issue or handoff is created.

This makes `grill-me` portable but creates a provenance weakness: exact decisions can be softened or lost when later summarized.

The docs advise keeping the same conversation when passing into `to-spec` because the current context is the actual state store.

## J. Composition and dependency graph

### `grill-me` calls

- `grilling` primitive.

### `grilling` is reused by

- `grill-with-docs`;
- `triage`;
- `wayfinder`;
- `improve-codebase-architecture`;
- other custom Skills requiring interview behavior.

This is explicit methodology deduplication: one interview primitive, many wrappers.

Known weakness: cross-Skill invocation is not mechanically reliable across models/harnesses. Merely telling a model to call/load another Skill does not guarantee it actually does.

## K. Skill / Agent / Runtime / Harness architecture

- `grill-me/SKILL.md`: thin manual router.
- `grilling/SKILL.md`: methodology implementation in instructions.
- docs: lifecycle, failure reports, UX guidance, limitations.
- no deterministic runtime/state-machine implementation observed.
- no dedicated regression Harness observed in inspected evidence.

This is predominantly **prompt-method architecture**, not executable enforcement.

## L. Context engineering and progressive disclosure

Strong positive:
- wrapper stays one line;
- methodology lives in shared primitive;
- reusable wrappers avoid duplicating interview text.

Context risks:
- long sessions enter a “dumb zone” as context fills;
- very large scopes should be split;
- loss of context loses the state;
- lower-capability models may collapse rounds and skip the confirmation gate.

Batching frontier questions reduces human/model round trips but can increase per-round cognitive load.

## M. Concurrency, isolation, idempotency, replay

No durable concurrency model.

Interesting partial concurrency model: background fact research can proceed while independent decision questions are asked.

The run is synchronous with respect to human decisions; the docs explicitly reject a fully async variant because unanswered decision questions would become the agent's own opinions.

No replay protection, decision IDs, or immutable action receipts.

## N. Safety and trust boundaries

Primary trust boundary is epistemic rather than security-oriented:
- facts can be researched;
- decisions must not be fabricated by the agent.

No dedicated credential/prompt-injection controls in this Skill.

No mutating tools are required in the standalone form, reducing operational blast radius.

## O. Failure semantics and recovery

### Dependency-order mistake

Symptom: two same-round questions turn out to be dependent.
Recovery: user/agent notices; reopen affected branch next round.

### Agent starts building

Symptom: frontier empties and agent moves directly to implementation.
Cause: model skips confirmation gate.
Recovery: explicit user/global instruction not to implement without permission.

### Agent answers own questions

Classified by docs as a broken run. No async workaround; re-establish user decision ownership.

### Too many questions

Usually means scope too large or an ungrillable question is being discussed instead of prototyped.

### Dependency Skill not loaded

The wrapper may appear installed but do nothing/use an improvised interview if `grilling` is absent or not loaded.

## P. Verification / Harness / Eval model

No deterministic behavioral Harness was observed for the interview mechanism.

The docs expose practical success criteria:
- questions arrive in rounds;
- same-round questions are independent;
- later rounds reflect earlier answers;
- facts are looked up, not pushed to user;
- background research blocks only dependent questions;
- agent waits for final confirmation.

These are effectively a manual trajectory rubric, not machine enforcement.

No independent study or held-out outcome evidence was inspected showing that the technique produces better real decisions.

## Q. Portability and compatibility

Highly portable at conceptual level because it only needs conversation plus optional fact tools.

However:
- cross-Skill loading varies by harness/model;
- model quality matters materially because the model must spot hidden branches and system failure modes;
- users may prefer sequential questioning, and the docs support a global override.

## R. Cost, latency, complexity and ergonomics

### Benefits

- parallelizes independent questions;
- reduces serial one-question round-trip count;
- recommendation-first format makes answering faster;
- no setup/files.

### Costs

- potentially dozens/hundreds of questions;
- significant human attention;
- high model-quality sensitivity;
- long context accumulation;
- large rounds can be cognitively heavy.

Ergonomics are deliberately opinionated: numbered rounds with recommendations.

## S. Anti-patterns and negative knowledge

- Do not implement before shared-understanding confirmation.
- Do not ask user for facts the environment can retrieve.
- Do not ask dependent questions in same round.
- Do not impose arbitrary fixed question cap.
- Do not mistake user passivity for agreement quality.
- Do not talk indefinitely about experiential questions that need a prototype.
- Do not build a second interview Skill when reusable `grilling` primitive suffices.

## T. Hidden assumptions and inferred invariants

1. The user is available synchronously for multiple rounds.
2. The model can infer a good-enough dependency graph without deterministic graph state.
3. User recommendations do not create excessive anchoring/compliance bias.
4. Current chat remains available until downstream capture.
5. The user understands enough of the domain to own the decisions.
6. The best next step for an ungrillable question is often prototype/evidence rather than more language.
7. The Skill-loading substrate will honor delegation—known to be false often enough to be documented.

## U. Reusable primitives — neutral extraction

### U1 — Decision dependency tree

Model choices as dependent decisions rather than a flat questionnaire.

### U2 — Frontier batching

Ask all currently unblocked, mutually independent decisions in one round.

### U3 — Fact/decision ownership split

Agent researches facts; human owns trade-off decisions.

### U4 — Non-blocking fact acquisition

Pending research blocks only downstream branches, not the whole interaction.

### U5 — Recommendation-backed questions

Provide a default/recommendation to reduce decision friction, while preserving explicit user override.

### U6 — Shared-understanding closure gate

No action until user confirms the elicitation result is complete enough.

### U7 — Ungrillable→prototype branch

When language cannot resolve experiential uncertainty, switch evidence mode.

## V. Cross-Top10 links

- `grill-with-docs`: same primitive plus durable domain artifacts.
- `improve-codebase-architecture`: uses grilling only after candidate selection.
- `triage`: uses grilling selectively to turn vague reports into agent-ready work.
- `handoff`: possible remedy for stateless conversational knowledge, but may lose decision detail.
- `setup-matt-pocock-skills`: environment setup supporting stateful cousins.

## W. Open questions for final synthesis

- Should design-tree/frontier state be made machine-readable rather than implicit in model context?
- Does recommendation-first questioning create anchoring/sycophancy risk that needs counterbalancing?
- When should rounds be batched versus one-at-a-time?
- Can closure be mechanically gated without making the conversation bureaucratic?
- How should exact decisions be captured so later specs do not soften them?

## X. Evidence ceiling

- Wrapper inspected: **YES**
- Shared primitive inspected: **YES**
- Detailed original docs/known failures inspected: **YES**
- Deterministic runtime enforcement: **NO**
- Dedicated automated eval/Harness observed: **NO**
- Live outcome improvement study observed: **NO**
- Cross-harness loading failure acknowledged by source: **YES**

The methodology is richly specified but largely instruction-enforced; execution fidelity depends strongly on model/harness behavior and user participation.
