# 03 — `grill-with-docs`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Wrapper: `skills/engineering/grill-with-docs/SKILL.md`
- Wrapper blob: `62b9efb6f991d1b229adee7506962f13ced0c499`
- Interview primitive: `skills/productivity/grilling/SKILL.md`
- Domain persistence primitive: `skills/engineering/domain-modeling/SKILL.md`
- User docs: `docs/engineering/grill-with-docs.md`
- Related domain-consumption convention inspected through setup/domain docs.

The wrapper is almost empty; the real system is a composition of `grilling + domain-modeling` plus repository conventions.

## B. Problem model and intended outcome

Problem: a fuzzy codebase design discussion can reach useful conclusions but lose them when the chat ends, and agents/humans can use inconsistent domain language or repeatedly relitigate hard decisions.

Desired result:
- shared understanding through the same decision-tree interview as `grill-me`;
- canonical domain vocabulary captured as it crystallizes;
- only truly durable architectural decisions captured as ADRs;
- resulting conversation immediately usable by the next planning step.

Architectural role: **stateful interview front door + domain-model persistence composition**.

It is not a full spec writer. Most decisions deliberately do not qualify for glossary/ADR storage.

## C. Activation and invocation model

- Explicit only: `disable-model-invocation: true`.
- Intended for a repository/working-directory context.
- Appropriate when a change can be clarified in one session.
- `wayfinder` is positioned for multi-session efforts.
- Wrapper calls two other Skills: `grilling` and `domain-modeling`.

Critical dependency assumption: merely naming those two Skills causes them to load. Source docs explicitly say this can fail across harnesses/models.

## D. Inputs, outputs, side effects

Inputs:
- user's fuzzy plan/design;
- repository code;
- current glossary/map if present;
- relevant ADRs;
- user decisions and environmental facts.

Outputs/artifacts:
- conversation with resolved choices;
- inline `GLOSSARY.md` changes for canonical terms;
- optional ADR files for qualifying hard decisions.

No standalone spec is produced by this Skill.

Mutations are real repository writes, unlike stateless `grill-me`.

## E. End-to-end workflow

### D0 — Context bootstrap

Detect repository/domain-doc layout:
- root `GLOSSARY.md`, or
- `GLOSSARY-MAP.md` for multi-context repositories;
- relevant `docs/adr/` locations.

Absence is not an error; files are created lazily only when there is something worth recording.

### D1 — Start grilling primitive

Use design-tree/frontier rounds:
- ask only unblocked decision questions;
- batch independent questions;
- agent researches facts;
- user owns decisions.

### D2 — Challenge language continuously

While discussing:
- compare user's terms with existing glossary;
- call out conflicts immediately;
- split overloaded/fuzzy concepts;
- propose precise canonical terms;
- invent concrete scenarios to stress boundaries;
- compare claimed behavior against actual code.

### D3 — Persist vocabulary inline

As soon as a term is resolved, write/update `GLOSSARY.md` immediately rather than batching at end.

Glossary constraint:
- domain vocabulary only;
- no implementation detail;
- not a spec;
- not a scratchpad.

### D4 — ADR admission gate

Only offer/write ADR when all are true:
1. decision is meaningfully hard to reverse;
2. future reader would find it surprising without context;
3. it represents a genuine trade-off among alternatives.

Otherwise keep the decision in conversation.

### D5 — Continue frontier

Repository changes may influence later questions. Recompute the interview frontier after user decisions as in `grilling`.

### D6 — Close and hand to next flow

When shared understanding is confirmed:
- keep the same conversation;
- normally pass it to `to-spec` so the non-glossary/non-ADR decisions are not lost.

## F. Core methodology / mental model

It combines two disciplines:

### 1. Dependency-aware decision elicitation

Same design-tree/frontier methodology as `grilling`.

### 2. Domain-model curation

Words are part of architecture. The Skill treats naming ambiguity as a design defect and uses:
- canonical terminology;
- concrete edge-case scenarios;
- code-to-language consistency checks;
- immediate capture.

### 3. Selective durability

Not every conversation fact deserves persistence.

Durability tiers:
- canonical term → glossary;
- hard/surprising/trade-off decision → ADR;
- ordinary implementation decision → conversation only, later spec capture.

This is an explicit anti-bloat policy for durable knowledge.

## G. Decision-rights model

User:
- chooses trade-offs;
- resolves terminology when ambiguity exists;
- confirms shared understanding.

Agent:
- researches code/facts;
- identifies terminology conflicts;
- proposes canonical language;
- determines whether to offer ADR based on the three gates;
- performs file updates.

Repository:
- existing glossary/ADRs constrain vocabulary and prior decisions.

Risk: agent judgement controls what qualifies for persistence; it may under-capture critical decisions or overproduce ADRs.

## H. State machine and lifecycle

Conversation lifecycle resembles `grill-me`, with extra inline artifact mutations:

`BOOTSTRAP_DOCS → FRONTIER_ROUND → USER_DECISIONS → DOMAIN_RECONCILIATION → GLOSSARY/ADR_WRITE_IF_QUALIFIED → RECOMPUTE → ... → SHARED_UNDERSTANDING → HANDOFF_TO_SPEC`

No explicit machine state object was observed.

Repository artifacts survive future sessions and become input to later Skills.

## I. Memory, durability, provenance

Three durability classes are explicit:

1. **Glossary**: canonical domain concepts.
2. **ADR**: exceptional durable decisions.
3. **Conversation**: everything else.

This selective model is elegant but creates the Skill's most serious documented weakness: many exact decisions remain only in the context window. The docs explicitly warn that later spec steps can soften ordering guarantees, numeric defaults, and negative requirements.

No observed mechanism links each answer to a later spec/ticket/test.

## J. Composition and dependency graph

Wrapper depends on:
- `grilling`;
- `domain-modeling`.

`domain-modeling` itself depends on repository conventions (`GLOSSARY`, `GLOSSARY-MAP`, ADR locations).

Downstream:
- normally `to-spec`, then tickets/implementation/review.

Composition is instructed, not mechanically guaranteed. Partial loading can produce:
- good interview with no files;
- unstructured all-at-once interview if `grilling` also fails.

## K. Skill / Agent / Runtime / Harness architecture

- wrapper Skill: only orchestration instruction;
- `grilling`: interview method;
- `domain-modeling`: domain artifact method;
- filesystem/repo: durable state;
- docs: explain lifecycle/known failures.

No deterministic runtime orchestrator was observed enforcing that both delegated Skills execute.

This is a clean conceptual decomposition but weak execution binding.

## L. Context engineering and progressive disclosure

Positive:
- tiny wrapper;
- methodology deduplicated into two primitives;
- persistent glossary/ADRs reduce repeated rediscovery in future sessions.

Negative:
- critical ordinary decisions still live only in current context;
- same-conversation requirement couples next planning step to context survival;
- wrapper composition can silently under-load.

## M. Concurrency, isolation, idempotency, replay

Source docs explicitly acknowledge drift risk when multiple people/agents write the real repository artifacts.

No locking, compare-and-swap, writer identity, or merge protocol is defined.

Inline immediate glossary writes improve capture latency but can increase concurrent-edit collision risk.

ADR duplication/supersession semantics are not mechanically specified in inspected sources.

## N. Safety and trust boundaries

No strong security model is central here.

Important authority boundary:
- code, glossary and ADRs are evidence to reconcile against—not automatically overwritten by conversational claims.

The Skill may mutate files based on user decisions; there is no explicit transactional preview/approval step beyond the ongoing conversation.

## O. Failure semantics and recovery

### Nothing written

Could be legitimate: no new term or qualifying ADR.

Could also indicate dependency-loading failure.

Source advises checking working directory/output rather than assuming success.

### Partial dependency loading

- `grilling` loaded, `domain-modeling` absent → structured interview, no paper trail.
- both absent → model improvises.

This is a known unfixed weakness.

### Context-only decision loss

Mitigation: keep same conversation and move directly to `to-spec`, then reread spec against actual decisions.

### Concurrent artifact drift

Acknowledged but no built-in recovery protocol.

## P. Verification / Harness / Eval model

No dedicated automated Harness observed.

Manual success rubric includes:
- glossary changes during session, not one batch;
- glossary contains vocabulary only;
- code-answerable facts are read from code;
- few/no ADRs is normal;
- terminology conflicts are challenged.

Source documentation itself supplies negative evidence through known user reports and unfixed dependency-loading issues.

No live comparative evidence proving glossary capture improves model performance was observed; docs explicitly note disagreement about whether value is mostly human communication.

## Q. Portability and compatibility

Conceptually portable across code repositories.

Execution portability is weaker:
- cross-Skill loading reliability varies by harness/model;
- stateful writes assume filesystem/repository access;
- domain-doc conventions are repository-specific.

## R. Cost, latency, complexity and ergonomics

Adds:
- multi-round human interview;
- repository reads;
- inline writes;
- terminology governance overhead.

Removes/reduces:
- repeated vocabulary negotiation;
- future explanation of durable architectural trade-offs.

The three-gate ADR rule is explicitly designed to prevent documentation explosion.

## S. Anti-patterns and negative knowledge

- Do not put implementation details in glossary.
- Do not create glossary/ADR files upfront without content.
- Do not turn every decision into an ADR.
- Do not silently accept terminology that contradicts existing glossary.
- Do not assume a successful interview means file-writing primitive loaded.
- Do not clear the conversation before downstream spec capture.

## T. Hidden assumptions and inferred invariants

1. A shared vocabulary is valuable enough to justify maintenance cost.
2. File-based glossary/ADR conventions are discoverable by future agents.
3. Same-conversation transition to spec is available.
4. Model can judge ADR worthiness consistently.
5. Repository is writable and has a safe single-writer situation.
6. Cross-Skill delegation works—explicitly contradicted often enough to be a known bug.

## U. Reusable primitives — neutral extraction

### U1 — Inline knowledge crystallization

Persist a term/decision at the moment it becomes stable, not after the whole session.

### U2 — Three-gate durable-decision admission

Only durable if costly to reverse + surprising + real trade-off.

### U3 — Vocabulary/code contradiction check

Compare conceptual claims against implementation evidence.

### U4 — Lazy artifact creation

Do not create empty governance files; create at first qualifying content.

### U5 — Layered knowledge durability

Different knowledge classes deserve different persistence surfaces.

### U6 — Shared-method composition

Thin wrapper composes interview + domain persistence rather than duplicating either.

Known limitation: prose composition without invocation attestation.

## V. Cross-Top10 links

- `grill-me`: stateless version of same interview primitive.
- `improve-codebase-architecture`: consumes glossary/ADRs and also calls domain-modeling while exploring a chosen refactor.
- `setup-matt-pocock-skills`: scaffolds the repository conventions this Skill consumes.
- `tdd`: uses glossary terms for test names and ADR constraints.
- `triage`: can call the same interview/domain-modeling pair.
- `handoff`: potential alternative persistence mechanism, but may duplicate or soften existing artifacts.

## W. Open questions for final synthesis

- How should composition be mechanically verified so both delegated primitives actually ran?
- Should ordinary resolved decisions get an explicit temporary decision log before spec conversion?
- How can concurrent writers safely update glossary/ADRs?
- What should be authority when code, glossary and conversation disagree?
- Does glossary investment improve agent outcomes or mostly human coordination?

## X. Evidence ceiling

- Wrapper inspected: **YES**
- Both delegated primitives inspected: **YES**
- Detailed docs/known failure reports inspected: **YES**
- Deterministic composition enforcement: **NO**
- Dedicated automated eval/Harness: **NOT OBSERVED**
- Live quality improvement evidence: **NOT OBSERVED**
- Known dependency-loading failure: **SOURCE-ACKNOWLEDGED**

The architecture is conceptually modular and stateful, but its most important orchestration invariant—both delegated Skills actually executing—is not mechanically guaranteed in the inspected design.
