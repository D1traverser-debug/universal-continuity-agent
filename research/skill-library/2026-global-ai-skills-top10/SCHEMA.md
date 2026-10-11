# Complete Skill Distillation Schema

Every Top10 entry uses this schema. Sections may say `NOT_PRESENT`, `NOT_OBSERVED`, or `NOT_APPLICABLE`, but they may not silently disappear.

The schema deliberately separates **what the source actually does** from **what we may later want to adopt**. Adoption is a second-phase activity after 10/10 completion.

## A. Identity and evidence provenance

1. Skill name and source owner/repository.
2. Pinned upstream repository HEAD.
3. Exact Skill path/blob.
4. Delegated primitive/reference/runtime files inspected.
5. Tests/evals/workflows/issue/changelog evidence inspected.
6. Popularity/ranking context, explicitly marked non-quality evidence.
7. Evidence freshness and known blind spots.

## B. Problem model and intended outcome

1. What problem class the Skill believes exists.
2. What success looks like.
3. What it intentionally does **not** solve.
4. Whether it is a router, primitive, driver, reference, setup step, periodic maintenance tool, execution tool, review tool, or handoff tool.

## C. Activation and invocation model

1. Explicit/manual invocation triggers.
2. Implicit/model-invoked triggers.
3. Delegated invocation by another Skill/Agent.
4. Whether implicit invocation is disabled.
5. Preconditions before activation.
6. Stop/exit criteria.
7. Wrong-trigger failure modes.

## D. Inputs, outputs, side effects

1. User inputs.
2. Environment/repository/tool inputs.
3. Structured/unstructured outputs.
4. Durable artifacts created/modified.
5. Temporary artifacts.
6. External side effects.
7. Mutating vs read-only operations.

## E. End-to-end workflow

Recover the real workflow as a state/phase sequence, not a prose summary.

For each phase record:

- entry condition;
- actions;
- tools/delegates;
- decision owner;
- artifacts/state changed;
- exit condition;
- failure/recovery path.

## F. Core methodology / mental model

1. Named concepts and vocabulary.
2. Decision framework.
3. Search/exploration strategy.
4. Decomposition strategy.
5. Prioritization/ranking strategy.
6. Feedback loop.
7. Stopping rule.
8. Heuristics versus invariants.
9. Any explicit theory/source the Skill builds on.

## G. Decision-rights model

Separate who decides what:

- user/human;
- model/agent;
- deterministic runtime;
- external tool/environment;
- reviewer/grader;
- repository authority.

Record where the source accidentally lets one actor decide something another actor was supposed to own.

## H. State machine and lifecycle

1. States/roles/stages.
2. Legal transitions.
3. Transition evidence/guards.
4. Resume/re-entry behavior.
5. Terminal states.
6. Timeouts/expiration/staleness.
7. Whether state is explicit, inferred, or only conversational.

## I. Memory, durability, provenance

1. Stateless vs stateful.
2. What lives only in context.
3. What becomes files/issues/ADRs/glossaries/session state/etc.
4. Authority versus cache/reference.
5. How stale artifacts are handled.
6. Whether decisions are linked to later implementation/tests.
7. Secret/PII handling.

## J. Composition and dependency graph

1. Skills/primitives this Skill calls.
2. Skills that call this one.
3. Runtime/CLI/MCP dependencies.
4. Shared vocabulary/contracts.
5. Dependency-loading assumptions.
6. Failure behavior when a dependency does not load.
7. Whether composition is explicit/mechanical or merely instructed in prose.

## K. Skill / Agent / Runtime / Harness architecture

Classify where behavior actually lives:

- installed `SKILL.md`;
- delegated/shared Skill;
- Agent prompt/instructions;
- executable runtime/CLI;
- state machine/workflow;
- reference docs;
- test/eval/harness;
- automation/scheduler/CI.

Record duplication and drift risks between these surfaces.

## L. Context engineering and progressive disclosure

1. Hot-path context size/shape.
2. Thin-router or full-instruction model.
3. On-demand loading.
4. Context compaction/handoff behavior.
5. Token-reduction mechanisms.
6. How stale versioned instructions are prevented.
7. Context-window failure modes.

## M. Concurrency, isolation, idempotency, replay

1. Session/worktree isolation.
2. Multiple-agent behavior.
3. Duplicate execution risk.
4. Retry semantics.
5. Unknown-outcome semantics.
6. Idempotency assumptions.
7. Replay/stale-ref protections.
8. Lock/claim/lease semantics where present.

## N. Safety and trust boundaries

1. Untrusted-input model.
2. Prompt-injection posture.
3. Credential/secret model.
4. Permission/authorization boundaries.
5. Network/domain containment.
6. Destructive-action confirmation.
7. Sensitive artifact handling.
8. What is only advisory versus mechanically enforced.

## O. Failure semantics and recovery

For each material failure class record:

- detection signal;
- whether it fails open/closed;
- retry/recovery behavior;
- what evidence may be uncertain;
- whether the user must intervene;
- whether partial progress is durable.

Include source-author documented complaints and known unfixed bugs.

## P. Verification / Harness / Eval model

1. Unit/static tests.
2. Behavioral/trajectory tests.
3. Synthetic fault injection.
4. Live E2E tests.
5. LLM judges.
6. Independent outcome verification.
7. Context-footprint/performance measurements.
8. What tests explicitly **cannot** prove.
9. Missing evals that materially weaken confidence.

## Q. Portability and compatibility

1. Model sensitivity.
2. Harness/agent compatibility.
3. OS/runtime assumptions.
4. Vendor-specific tool assumptions.
5. Graceful degradation.
6. Compatibility layers.
7. Known portability bugs.

## R. Cost, latency, complexity and ergonomics

1. Interaction rounds.
2. Tool-call/search/runtime cost.
3. Context cost.
4. Human attention cost.
5. Setup/migration burden.
6. Ongoing maintenance burden.
7. Complexity added versus removed.
8. UX/interaction design choices.

## S. Anti-patterns and negative knowledge

Capture explicit "do not" rules, rejected framings, out-of-scope ideas, and lessons learned from earlier versions. Negative knowledge is first-class evidence, not a footnote.

## T. Hidden assumptions and inferred invariants

Reverse-engineer assumptions that are required for success but not always stated in the main Skill. Mark each inference as such and cite its supporting implementation/test/documentation evidence.

Examples:

- the user is available synchronously;
- another Skill will actually load when named;
- the repository uses Git;
- a browser action is safe to retry;
- current conversation context remains intact;
- popularity correlates with usefulness;
- a visual report can render external CDN assets.

## U. Reusable primitives — neutral extraction

List reusable mechanisms without deciding whether Universal should adopt them.

Each primitive gets:

- name;
- invariant it tries to enforce;
- minimal form;
- evidence source;
- known limitation.

## V. Cross-Top10 links

Record likely overlaps/complements/conflicts with other entries, but do not resolve them until Phase B.

## W. Open questions for final synthesis

Questions that cannot be answered from this Skill alone and should be revisited after all ten are normalized.

## X. Evidence ceiling

End every entry with explicit assurance labels:

- source inspected;
- runtime inspected;
- tests/evals inspected;
- live outcome evidence observed or not;
- independent verification observed or not;
- unknowns.

No entry may infer global quality from install count, stars, author reputation, or a single demo.
