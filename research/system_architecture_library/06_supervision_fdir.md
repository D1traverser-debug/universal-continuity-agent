# 06 — Erlang/OTP Supervision, NASA FDIR and Recovery Architecture

## Erlang/OTP supervision

OTP supervision trees treat failure recovery as a structural responsibility rather than scattered exception handling. A supervisor starts, stops and monitors children and applies a declared restart strategy:

- `one_for_one`: restart only the failed child;
- `one_for_all`: restart the whole sibling group;
- `rest_for_one`: restart the failed child plus dependents started after it.

Restart intensity/period limits stop endless restart loops; if a supervisor exceeds its restart budget, it terminates and the next supervisory level can handle the failure. This creates **hierarchical escalation and bounded recovery**, not “retry forever.”

### Universal mapping

Universal already has failure containment principles: an owner-local failure should not freeze healthy owners, and systemic maintenance can reopen earlier stages. However, there is no general machine-readable supervision tree declaring:

- which control-plane components depend on which others;
- which failure should restart/reconcile only one component versus a dependency group;
- restart/retry intensity limits;
- when to escalate to a higher controller;
- when to enter degraded/safe mode instead of retrying.

The system therefore has good maintenance recovery semantics but a weaker **runtime supervision model**.

## NASA fault management / FDIR

NASA software-safety and architecture guidance treats fault management as an architecture concern because it can interact with nominal control and create hazards of its own. FDIR decomposes response into detection, isolation and recovery/response; NASA guidance also emphasizes concurrent or near-simultaneous faults, diagnosis support, persistence thresholds and response breadth.

A broader fault-management control chain can be represented as:

`monitor -> assess -> decide -> mitigate/recover`

This resembles MAPE-K but with fault-specific emphasis on detection confidence, isolation, degraded modes and safe response.

### Critical lesson: the recovery mechanism can itself be hazardous

A false-positive fault detector can disable a healthy function; an overly broad recovery can damage unrelated state; repeated recovery can produce oscillation; concurrent faults can invalidate assumptions made for single-fault handling.

### Universal mapping

Current Universal has:

- detection signals and triage;
- user/system defect classification;
- owner-scoped containment;
- stale-writer protection;
- blocker states;
- fault-injection regression cases;
- separate state and signal planes.

But detection → isolation → recovery is not uniformly modeled for every subsystem. For example, tool/runtime loss, stale cache, owner drift, malformed evidence, external product-state mismatch and CI failure each follow somewhat different recovery logic.

## Candidate recovery-state taxonomy for later design

Non-authoritative candidate vocabulary:

- HEALTHY
- DEGRADED
- SUSPECTED_FAULT
- ISOLATED
- RECOVERING
- RECOVERY_FAILED
- SAFE_HOLD / USER_ACTION_REQUIRED
- RETIRED

A generic taxonomy might improve observability, but only if it can be mapped without erasing owner-specific semantics. This should not be added until the later refactor design compares alternatives.

## Main current gaps

1. No explicit dependency-aware supervision tree across control-plane components.
2. No restart/retry intensity/escalation policy comparable to OTP supervision.
3. Fault detection and maintenance triage exist, but isolation/recovery states are not normalized.
4. Concurrent-fault and recovery-interaction analysis is not a first-class audit dimension.
5. Safe/degraded-mode semantics are owner/capability specific rather than globally classified.

## What not to transplant

ChatGPT/GitHub/connector operations are not Erlang processes; “restart” may mean reread, rebind, reconcile, retry, reopen a stage, reacquire a capability, or stop and ask for user action. A literal OTP tree would be misleading. Adopt dependency-aware recovery and escalation concepts only after mapping the actual component graph.

## Current assessment

- Failure containment: **PRESENT**.
- Recovery after maintenance validation failure: **PRESENT**.
- Runtime supervision tree: **CURRENT GAP**.
- Fault-isolation model: **PARTIAL**.
- Recovery-budget/escalation model: **CURRENT GAP**.
- Concurrent-fault analysis: **CURRENT GAP**.
