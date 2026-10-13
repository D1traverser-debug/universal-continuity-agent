# 09 — TLA+ and Formal Verification

## Why formal methods are relevant here

Universal's highest-value invariants are not primarily arithmetic; they are **state-transition and concurrency invariants**:

- only a valid writer may authoritatively mutate a task;
- takeover changes lease/epoch and invalidates stale writers;
- same-chat refresh does not accidentally look like takeover;
- a stale prepared Git commit must not overwrite a newer `main`;
- incomplete discovery must not auto-resume;
- external/cache state must not override higher authority;
- a signal must not mutate state without the valid writer;
- commit success requires post-write authoritative reread;
- protocol reconciliation must not rewrite owner business truth.

These are exactly the kind of safety/liveness properties for which state-machine specification and model checking can expose interleavings that conventional examples may miss.

## TLA+ model

TLA+ is a high-level formal specification language particularly suited to concurrent and distributed systems. TLC explores executable finite models and can check safety and liveness properties. The value is to model the algorithm above code, make state variables/actions explicit, and let the checker search interleavings rather than relying solely on hand-written test scenarios.

## Candidate Universal model scope

A bounded first model could include:

### State variables

- `mainHead`
- `observedHead`
- `preparedParent`
- `activeLease`
- `resumeEpoch`
- `writer`
- `taskVersion`
- `taskStage`
- `discoveryComplete`
- `signalState`
- `writeOutcome`

### Actions

- bootstrap/read authority
- same-writer refresh
- legal takeover
- prepare mutation
- concurrent/external head movement
- CAS publish
- reread/verify
- emit signal
- consume signal
- checkpoint task
- fail/timeout with unknown mutation outcome

### Safety properties

- stale writer never commits authoritative task state;
- a CAS publish never succeeds against a different parent than the observed head;
- `COMMITTED` never occurs without intended authoritative postcondition;
- incomplete discovery never causes auto-resume;
- non-authoritative signal never directly mutates task state;
- lower-authority observation never becomes business truth by presence;
- resume epoch never decreases.

### Liveness properties

Under explicit fairness assumptions and available dependencies:

- a valid writer can eventually checkpoint;
- a recoverable blocked/unknown mutation can eventually reconcile or remain truthfully blocked rather than deadlock silently.

## Why tests are not enough

Unit/fault-injection tests exercise selected traces. Model checking asks whether any state/interleaving in the bounded model violates the invariant. It does not replace implementation tests; it finds design bugs earlier and provides a different evidence class.

## Limits

- A model only proves what it models.
- TLC finite-state checking is not proof of arbitrary unbounded behavior.
- Mapping model variables/actions to code must be reviewed or the formal proof can drift away from implementation.
- Formalization overhead must be reserved for high-value concurrent/control invariants, not every writing workflow.

## Current gap

Universal currently has deterministic state-machine validation and synthetic fault injection, but no formal state specification or model-checking artifact for its core writer/authority/reconciliation invariants. This is an **assurance gap**, not evidence that the current implementation is wrong.

## Current assessment

- Explicit runtime state machines: **PRESENT**.
- Synthetic interleaving/fault tests: **PARTIAL**.
- Formal specification/model checking: **ABSENT / CURRENT ASSURANCE GAP**.
- Best initial target: **lease + resume epoch + HEAD CAS + commit receipt + signal/state separation**.
