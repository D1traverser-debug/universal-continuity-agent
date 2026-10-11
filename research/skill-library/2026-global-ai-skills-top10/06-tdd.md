# 06 — `tdd`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Skill: `skills/engineering/tdd/SKILL.md`
- Skill blob: `01eadaa34e7c9a63a67d6dc3cce1cc81b0e49985`
- Test-quality examples: `skills/engineering/tdd/tests.md`
- Mocking reference: `skills/engineering/tdd/mocking.md`
- User docs: `docs/engineering/tdd.md`
- Shared interface/deep-module vocabulary: `skills/engineering/codebase-design/SKILL.md`

## B. Problem model and intended outcome

Problem: “test-first” work often degenerates into implementation-coupled tests, tautologies, broad batches of speculative tests, internal mocks, or tests placed at unstable seams.

Desired outcome:
- define a behavioral public seam first;
- agree which seams deserve tests;
- write one failing behavioral test;
- implement only enough to satisfy it;
- repeat in vertical slices;
- preserve tests across internal refactors.

Architectural role: **method/reference**, not full work driver. In the main build chain, `implement` drives work while `tdd` supplies rules.

It intentionally does not own refactoring anymore; review owns that phase.

## C. Activation and invocation model

May be explicit or model-invoked when:
- user requests test-first feature/bug work;
- says TDD/red-green-refactor;
- asks for integration testing around a concrete behavior.

Best fit: behavior with meaningful input/output and independent expected result.

Poor fit/gap acknowledged by source:
- glue/config/wiring/type-only changes;
- simple delegation/CRUD with no independent behavioral oracle;
- unclear feature behavior—specification should come first.

Precondition: test seam must be agreed before writing tests.

## D. Inputs, outputs, side effects

Inputs:
- concrete behavior/spec/ticket;
- repository code;
- glossary/ADRs where present;
- user-approved test seams;
- independent expected values/examples.

Outputs:
- tests at approved public seams;
- minimal implementation per cycle;
- code changes and test results through the driver/session applying this reference.

The Skill itself is stateless and does not own the overall commit/workflow lifecycle.

## E. End-to-end workflow

### T0 — Understand behavior

Establish concrete capability and observable outcome. If unclear, route upstream to specification/design.

### T1 — Load domain/architecture context

Read glossary for terminology and ADRs for local constraints.

If interface/seam itself is in question, consult `codebase-design` rather than inventing test structure first.

### T2 — Propose seams

Name candidate public interfaces and explain:
- what each seam catches;
- what it misses.

Wait for user confirmation. No test at an unconfirmed seam.

### T3 — Red

Write **one** test for one behavior at one agreed seam.

Run it and establish that it fails for the intended reason.

### T4 — Green

Write only enough implementation to make that test pass.

Do not anticipate later cases.

### T5 — Observe/learn

Use what the slice taught you to choose the next behavior/test.

### T6 — Repeat vertically

One seam/test/minimal implementation per cycle. Avoid all-tests-first horizontal batch.

### T7 — Leave refactor/review downstream

Current methodology deliberately removes “refactor” from the loop. Review stage handles architecture/refactoring separately.

## F. Core methodology / mental model

### Behavior over implementation

Tests are specifications through public interfaces.

### Seam-first testing

Testing budget is finite. First decide where observable boundaries matter.

### Vertical tracer bullets

Each cycle proves one end-to-end slice and lets later tests react to knowledge gained.

### Independent expected truth

Expected values should come from literals, worked examples, specs or other independent sources—not recompute the same algorithm.

### Mock only system boundaries

External API/time/randomness/filesystem/database where appropriate; do not mock owned internal modules just to make tests easy.

### Minimal green

No speculative implementation before a test requires it.

## G. Decision-rights model

User:
- approves test seams;
- supplies/accepts intended behavior and business truth.

Agent:
- proposes seams and trade-offs;
- writes/runs test;
- implements minimum behavior;
- detects anti-patterns.

Spec/known example:
- should own expected behavioral truth where available.

Runtime/test runner:
- provides actual pass/fail feedback.

A structural weakness is explicit: instructions do not mechanically prevent the model from writing implementation first.

## H. State machine and lifecycle

Logical cycle:

`BEHAVIOR_DEFINED → SEAMS_PROPOSED → SEAMS_CONFIRMED → RED → GREEN → NEXT_SLICE → ... → BUILD_COMPLETE → REVIEW`

Failure branches:
- unclear behavior → spec/design;
- wrong seam → revisit seam decision;
- slow browser/E2E feedback → move to a faster useful seam or defer E2E;
- test cannot get independent expected value → question whether TDD is appropriate.

No persistent internal state object observed.

## I. Memory, durability, provenance

Durable outputs are repository tests/code created by the driver using the method.

The Skill itself keeps no state.

Glossary/ADR are read as prior design memory.

Seam approval is largely conversational unless earlier spec captures it; source notes full chain does better because `to-spec` agrees seams before implementation and review later checks them.

## J. Composition and dependency graph

Dependencies/relations:
- `codebase-design`: seam/interface vocabulary;
- `to-spec`: upstream behavior and agreed seams;
- `implement`: work driver that calls TDD per ticket;
- `code-review`: downstream standards/spec review and refactoring responsibility.

This separation is deliberate: `tdd` is methodology, `implement` is orchestration.

## K. Skill / Agent / Runtime / Harness architecture

- `SKILL.md`: core rules/anti-patterns.
- `tests.md`: concrete good/bad behavioral examples.
- `mocking.md`: boundary-mocking method.
- `codebase-design`: shared vocabulary.
- actual test runner/build tooling: repository-dependent external runtime.

No central deterministic Harness enforces red-before-green chronology. Compliance is primarily prompt-guided plus observable test runner outputs.

## L. Context engineering and progressive disclosure

Good decomposition:
- concise main methodology;
- examples/mocking split into references;
- interface theory delegated to shared `codebase-design` rather than duplicated.

The source itself evolved by deleting duplicated deep-module/refactoring content and moving it to shared/downstream Skills.

This is a concrete **Skill deduplication/evolution** pattern.

## M. Concurrency, isolation, idempotency, replay

No special concurrency model.

Potential conflict: multiple agents modifying same tests/code require repository/worktree isolation outside this Skill.

The loop is naturally incremental and replayable via test runner, but execution chronology (test genuinely red before implementation) is not attested.

## N. Safety and trust boundaries

Operational safety is indirect:
- tests constrain behavior;
- minimal implementation reduces speculative change;
- public interface tests reduce internal coupling.

No credential/security trust model is central.

Mocking guidance reduces false confidence by not substituting mocks for owned code.

## O. Failure semantics and recovery

### Implementation before red

Known real failure. Source documents that models may read the rule and still default to code-first.

Recovery: observe run; enforce externally if strict chronology matters. Stronger prose is not assumed to solve it.

### Bad seam choice

Source says this is common; user may not understand seam names. Workaround: explain what each catches/misses before confirmation.

### Browser test first

Slow E2E feedback can make red-green loop unusably slow and lead agent to debug the test instead of missing feature. Source suggests browser tests later.

### Tautological test

If no independent expected truth exists, reconsider whether change should use this method.

### Sibling-ticket blindness

TDD run on one ticket may invent work belonging to another; broader spec/ticket sizing must prevent that.

## P. Verification / Harness / Eval model

The Skill uses the repository test runner as immediate behavioral feedback, but no dedicated meta-eval was observed for instruction compliance.

Manual trajectory rubric:
- seams named/approved before test file;
- one red test appears first;
- minimal code makes it green;
- next test only after prior green;
- test names describe capability;
- expected values trace to independent source;
- internals can be renamed/refactored without test failure;
- mocks only at external boundaries.

Critical evidence gap: passing test suite does not prove chronology or absence of implementation-coupled tests unless reviewed.

## Q. Portability and compatibility

Method is language/framework agnostic conceptually.

Actual runner/mocking idioms vary by repo.

Source acknowledges model compliance variability.

Works better where behavior has fast deterministic feedback; worse for visual/browser/manual systems.

## R. Cost, latency, complexity and ergonomics

Benefits:
- tight feedback loop;
- reduces speculative implementation;
- tests become durable behavior contracts.

Costs:
- repeated runner cycles;
- human seam confirmation;
- can over-test low-value glue;
- integration/browser seams can be expensive.

Horizontal batching is rejected partly because it front-loads incorrect assumptions.

## S. Anti-patterns and negative knowledge

Explicit:
- implementation-coupled tests;
- mocking internal collaborators;
- private-method assertions/call-count coupling;
- tautological expected values;
- horizontal test batches;
- speculative green code;
- tests at unapproved seams.

Evolution negative knowledge:
- refactor phase was removed because agents rarely executed it reliably; moved to review.
- duplicated architecture guidance was removed into shared Skill.

## T. Hidden assumptions and inferred invariants

1. There is a runnable feedback loop fast enough to be useful.
2. Observable public behavior can be isolated at meaningful seam.
3. Expected values can be sourced independently.
4. User/spec can decide important seams.
5. Test environment resembles behavior enough for the result to matter.
6. Separating implementation and review produces better compliance than asking one Skill to do all phases.

## U. Reusable primitives — neutral extraction

### U1 — Pre-agreed observation seam

Do not test/verify everywhere; agree the public evidence boundary first.

### U2 — One behavioral tracer bullet per cycle

Small end-to-end slice creates feedback before next design commitment.

### U3 — Independent expected truth

Verifier must not derive expected result using same logic as candidate.

### U4 — Boundary-only mocking

Mock uncertainty outside owned system, not the system under test.

### U5 — Method/reference separated from work driver

A Skill can own methodology without owning execution orchestration.

### U6 — Evolution by responsibility extraction

Remove weak/duplicated phases from one Skill and hand them to better-owned stages rather than growing prompt forever.

## V. Cross-Top10 links

- `improve-codebase-architecture`: seam/depth determines test surface.
- `triage`: bug verification can generate a reproducible behavior target before TDD.
- `grill-with-docs`: terminology/ADR informs tests.
- `handoff`: cross-session implementation needs durable seam/spec rather than conversational-only state.
- `frontend-design`: visual work highlights limits of deterministic red-green feedback.

## W. Open questions for final synthesis

- Can test-seam approval be machine-readable and inherited into review?
- Should red-before-green chronology produce execution receipts rather than rely on prompt?
- What gate determines when TDD is not worth applying?
- Can Universal generalize “independent expected truth” into non-code evals?
- How should long-running/expensive E2E evidence be staged relative to fast unit/integration loops?

## X. Evidence ceiling

- Main Skill inspected: **YES**
- Supporting examples/mocking reference inspected: **YES**
- User docs/known failures inspected: **YES**
- Shared architecture reference inspected: **YES**
- Deterministic TDD-compliance Harness observed: **NO**
- Test-runner feedback exists in real use: **YES conceptually, repo-dependent**
- Outcome evidence that this exact Skill improves production quality: **NOT OBSERVED**

The Skill contains strong testing methodology and candid failure knowledge, but the most important chronology/process rules remain instruction-enforced rather than attested by a harness.
