# Universal Continuity — Continuous Learning Policy

Status: ACTIVE
Applies to: Universal Continuity maintenance/evolution

## Purpose

Universal Continuity should proactively learn from relevant agent systems, Skills, harnesses, durable-execution frameworks, official product documentation, engineering write-ups, videos and high-signal community evidence. Learning is not permission to accumulate instructions indefinitely. The goal is to discover missing capabilities, verify them, distill only scope-relevant improvements, and leave mechanical evidence when the system changes.

System maintenance autonomy is governed by `SYSTEM_MAINTENANCE_POLICY.json`. Artifact/context authority and promotion are governed by `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`. Learning is one input to maintenance, not a reason to wait for the user to notice adjacent defects.

## Trigger model

Proactive scouting is allowed and expected when any of these are true:

1. the user explicitly asks Continuity to learn/evolve;
2. a real recovery exposes a capability gap, drift or weak owner conformance;
3. the assistant itself detects a systemic gap, propagation failure, stale authority assumption, duplicated mechanism or weak maintenance boundary;
4. OpenAI/agent-runtime authority materially changes;
5. the maintenance task reaches a learning/audit stage;
6. a new owner integration requires a pattern not covered by the current contract.

When a trigger reveals a concrete maintenance defect, do not stop at diagnosis or a user-facing explanation. Continue through the autonomous maintenance loop in `SYSTEM_MAINTENANCE_POLICY.json` unless the exact boundary requires external account/UI action, permission, credential, irreversible user choice, or a fact that cannot be safely inferred/retrieved.

Do not put broad web/video scouting on the steady-state path of ordinary business turns. Continuity exists to reduce context and latency, not to make every response a research project.

## Source lanes

Prefer evidence in this order for adoption decisions:

1. current first-party OpenAI product/API/Agents/Skills documentation for OpenAI behavior;
2. original engineering documentation/repos from the system being studied;
3. original conference/video/media evidence;
4. same-author companion material;
5. independent papers and high-signal engineering analysis;
6. community discussion as discovery/experience evidence only.

For video/media evidence, `MEDIA_DISTILLATION_PROTOCOL.md` remains authoritative. Transcript evidence and visual evidence must not be conflated.

## Learning loop

For each candidate improvement:

1. name the observed problem or opportunity;
2. gather the strongest practical evidence available;
3. store material observations as `LEARNING_EVIDENCE` with provenance when they may matter later;
4. distinguish invariant, reusable design principle, heuristic and product-specific behavior;
5. test scope fit against Universal Continuity ownership;
6. compare the idea with the current contract instead of assuming novelty;
7. reject duplicated, brittle or out-of-scope guidance;
8. when adopted, encode it in the smallest appropriate contract/policy/Skill/runtime surface;
9. add a regression or acceptance test when the behavior is mechanically testable;
10. record the accepted/rejected disposition in a learning-pass artifact;
11. checkpoint the maintenance task only after authoritative writes are verified.

A thought, critique, heuristic or improvement that exists only in chat is not durable evolution. It must either be intentionally persisted as provenance-bearing `LEARNING_EVIDENCE`, promoted into an owner/system authority surface after acceptance, or explicitly left uncommitted. Raw learning evidence must never silently mutate owner business rules.

If the learning pass exposes adjacent defects that are within the same maintenance authority and can be safely repaired, include them in the same maintenance closure rather than waiting for the user to point them out one by one. Avoid scope creep: adjacent repairs must be causally related, bounded, and validated.

## Epistemic independence and candidate-adoption gate

The user is the authority for the user's goals, explicit requirements, external facts they uniquely control, and high-impact choices that genuinely require them. The user is **not automatically the authority for an implementation pattern, architecture analogy, diagnosis, or proposed mechanism** merely because they suggested it. The same rule applies to the assistant's own first idea, another agent's recommendation, a popular framework, or a web source: each is a candidate until evaluated.

Before promoting a non-trivial design or evolution candidate:

1. separate the underlying goal/constraint from the proposed solution or analogy;
2. restate the actual failure mode that must be solved without assuming the proposed mechanism is correct;
3. inspect current authority and implementation before proposing a new abstraction;
4. generate or retrieve at least one credible alternative, including modification/deletion of an existing mechanism when applicable;
5. compare candidates on correctness, failure containment, coupling, maintainability, observability, migration cost, hot-path cost, reversibility and owner boundaries as relevant;
6. actively search for a counterexample, failure mode, or condition under which the initially attractive candidate is wrong;
7. prefer the smallest solution that satisfies the invariant and produces testable evidence;
8. explicitly reject, narrow or transform the user's or assistant's initial proposal when another candidate is better;
9. preserve an explicit user-mandated implementation choice only when it is truly a user decision rather than an inferred architecture preference, and surface the tradeoff if material;
10. require evaluation/regression evidence before claiming the candidate is an improvement.

Analogies such as inheritance trees, operating systems, organizations, UVM, Kubernetes, or biological evolution may help generate candidates, but an analogy never establishes architecture by itself.

A response that merely mirrors the user's proposed mechanism and adds detail is not evidence of independent learning. Repeated cases where the user must correct the system for prematurely treating their suggested solution as canonical are a reliability signal and should feed the maintenance incident loop.

For trivial, reversible, low-coupling changes, this gate may be lightweight; it must not become ritual overhead. For cross-agent architecture, persistence, authority, execution, safety, or evolution changes, the gate is mandatory.

## What belongs where

- Global invariants: `CONTINUITY_CONTRACT.json` / `PROTOCOL.md`.
- System-maintenance autonomy and recordkeeping: `SYSTEM_MAINTENANCE_POLICY.json`.
- Cross-agent artifact/context/cache lifecycle: `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`.
- Narrow reusable procedure: a Skill or focused policy file.
- Owner business behavior: owner repository, never duplicated into Universal Continuity.
- Current task progress: short handoff/checkpoint.
- Evidence/research detail: `research/` or `audits/`, referenced from handoff rather than copied into it.

## Anti-bloat rule

A new learning artifact does not justify enlarging startup context. `ENTRYPOINT.md` remains a map. Skills are loaded on demand. Research artifacts are read only when the active next action needs them. If a new rule can be derived from an existing authoritative artifact, reference it instead of copying it.

## Adoption standard

An improvement is accepted only when all are true:

- evidence is strong enough for the claim;
- it solves a concrete Continuity problem or closes a plausible recovery failure mode;
- it survives the epistemic-independence/candidate-adoption gate for non-trivial changes;
- it does not duplicate domain business logic;
- it has a clear authority location;
- it does not introduce a worse hot-path cost than the problem it solves;
- mechanically testable behavior has a test or acceptance check;
- promotion preserves provenance and invalidates or removes superseded active mechanisms where applicable.

## Current recurring scout topics

Keep these as research lanes, not hard dependencies:

- durable agent session/run state and resumability;
- observable progress/turn receipts and tracing;
- context engineering and compaction;
- Agent Skills and capability discovery;
- single-writer / concurrency / replay safety;
- long-running agent harnesses and incremental progress artifacts;
- multi-agent delegation and independent verification;
- durable execution/checkpoint systems;
- owner adapters and cross-store versioning;
- proactive system maintenance closure and drift detection;
- artifact lifecycle, cache invalidation and authority drift;
- independent candidate critique, falsification and anti-sycophancy in architecture/evolution decisions.
