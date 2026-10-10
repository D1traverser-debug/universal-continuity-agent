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
10. perform the second-order challenge / closure calibration below before promoting a non-trivial fix as closed;
11. record the accepted/rejected disposition in a learning-pass artifact;
12. checkpoint the maintenance task only after authoritative writes are verified.

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

## Second-order challenge / closure calibration

A first-order fix can be directionally correct and still be overclaimed, incomplete, self-validating, or easy to bypass. Therefore every non-trivial evolution or systemic-reliability repair must challenge the **accepted fix itself** after the first implementation/regression pass and before closure.

The second-order review must ask, as applicable:

1. **Exact claim:** What precise claim is being promoted now? Separate wiring, regression behavior, action-level execution, independent attestation and real-world outcome claims.
2. **Evidence ceiling:** What is the strongest conclusion the current evidence can support, and what can it explicitly **not** prove?
3. **Negative space:** What relevant profile, hook, path, role, input, counterexample or failure class could be silently omitted because the validator only inspects declared/present items?
4. **Self-reference:** Is the same actor generating the result, writing the receipt, grading the result and verifying the evidence? If yes, do not call that independent evidence.
5. **Post-hoc provenance:** Could receipts, timestamps, summaries or role records be generated after the fact without proving the claimed execution chronology? More files or role names do not create attestation.
6. **Exact proof binding:** Is the proof bound to this exact task, stage, capability, action, subject/candidate/brief/replay set, immutable inputs and claimed result, or could a real but stale/foreign receipt be replayed to satisfy a different claim? When the claim requires distinct executions, are the relevant execution/provider/work-order identities checked for reuse?
7. **Obligation derivation:** If a canonical machine-readable plan declares required work, does the runtime derive proof obligations from that plan, or is there a separately maintained stage/role allowlist that can silently omit newly configured work?
8. **Escape path:** Can the new guard be bypassed through another entrypoint, stale cache, compatibility layer, optional path or lower-authority artifact?
9. **Test realism:** Does CI/synthetic regression prove only executable mechanics, or does the claim require a real product/business trajectory, held-out case, external outcome or independent judge?
10. **Generalization:** Did the fix improve only the triggering example, or is there a held-out/counterexample check that prevents overfitting and collateral regression?
11. **Supersession:** Did the accepted mechanism actually replace/demote the contradictory or weaker active mechanism, or are both still live?
12. **Closure boundary:** What remains OPEN, and what new evidence would be sufficient to advance it without asking the user to manufacture internal proof?

A second-order challenge is not a requirement to keep redesigning forever. If the accepted fix survives these questions, relevant regression/eval passes, and the remaining uncertainty is correctly bounded, stop changing the mechanism and proceed with normal owner work.

### Evidence assurance ladder

Do not collapse the following levels into each other:

1. **DECLARED** — rule/capability/profile is documented.
2. **WIRED** — executable path/hook/guard exists and is connected.
3. **REGRESSION_VERIFIED** — deterministic or synthetic tests/CI show the mechanism behaves as intended on covered cases.
4. **ACTION_LEVEL_SELF_ATTESTED** — a real action produced structured receipts bound to the exact action/subject/inputs, but evidence is produced within the same execution context and is not independently attested.
5. **ACTION_LEVEL_INDEPENDENTLY_VERIFIED** — the real action has exact-action evidence verified through an independent execution identity, trace, verifier or equivalent non-self-reporting surface appropriate to the claim.
6. **LIVE_OUTCOME_VERIFIED** — real user/business/product outcome evidence supports the promoted outcome claim (for example quality improvement, publication performance, or held-out product behavior).

Higher levels require their own evidence. A CI PASS cannot be promoted directly to action-level execution proof; a structured same-session receipt cannot be promoted to independent attestation; an independently verified action cannot by itself prove a long-run quality or business outcome. A receipt that is not bound to the exact claim/action does not qualify even for action-level self-attestation merely because the receipt is real.

When a level is unavailable, record the exact ceiling and keep only the corresponding gate OPEN. Do not downgrade the whole owner if unrelated capabilities remain healthy, and do not fabricate a higher assurance level to make the architecture look complete.

### Reusable failure patterns distilled from real maintenance

The following are general failure classes, not owner-specific rules:

- **silent applicable-item omission / negative-space blind spot** — validation inspects what is present but never asks what should have been present;
- **declaration-to-operation gap** — policy, profile or role exists, but the concrete action did not prove activation/execution;
- **self-attestation inflation** — structured self-report is described as independent execution evidence;
- **CI-to-product overclaim** — unit/synthetic/regression success is described as real product or quality improvement;
- **single-example overfit** — the triggering failure improves without held-out or collateral-regression evidence;
- **post-hoc receipt illusion** — more receipts/timestamps/files increase apparent ceremony without adding execution identity or chronological provenance;
- **unbound-proof replay / wrong-subject evidence** — a real receipt, trace or evidence ref exists but is not cryptographically or structurally bound to the exact action, subject, input version and claimed result, so stale or foreign proof can be reused;
- **shadow obligation list / configured-obligation drift** — a canonical plan/config declares required work but runtime enforcement depends on a separately maintained stage/role list, allowing new configured obligations to bypass execution proof;
- **cache/authority circularity** — two derived surfaces agree with each other and are mistaken for independent truth;
- **patch-without-distillation** — a local defect is fixed but the reusable failure class is not encoded into a guard/eval/methodology.

When one of these patterns appears in an owner, repair the true owner surface and, when cross-agent reusable, distill the pattern into this evolution semantics plus a bounded regression/fault case. Do not copy the triggering owner's business rule into Universal.

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
- it survives the second-order challenge / closure calibration for non-trivial evolution or systemic repair;
- its claimed assurance level does not exceed the evidence ceiling;
- action-level execution proof is bound to the exact action/subject/inputs and satisfies any owner-required anti-replay constraints;
- machine-readable configured obligations are enforced from their canonical declaration rather than a parallel shadow list when such a declaration exists;
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
- independent candidate critique, falsification and anti-sycophancy in architecture/evolution decisions;
- second-order challenge of accepted fixes, evidence-ceiling calibration, exact-proof binding, anti-replay and self-attestation detection.
