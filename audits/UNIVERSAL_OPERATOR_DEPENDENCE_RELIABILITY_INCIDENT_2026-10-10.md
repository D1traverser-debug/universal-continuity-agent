# Universal operator-dependence reliability incident — 2026-10-10

## Status

`PARTIALLY_REMEDIATED__PRODUCT_BEHAVIOR_EVAL_PENDING`

## Incident

The user had to explicitly remind the Universal maintenance writer that the point of the control system is independent diagnosis and evolution rather than waiting for the user to propose mechanisms or enumerate follow-up defects.

This is a reliability incident in the Universal control plane itself. It is not a missing reminder in a child owner.

## Why this is material

`SYSTEM_MAINTENANCE_POLICY.json` already says that the user is not the system maintenance operator, repeated correction is a reliability signal, the assistant must challenge its own first solution, and the active maintenance writer should continue internal diagnosis/repair without waiting for the user to enumerate follow-ups.

The failure therefore cannot be explained by missing policy prose. The observed failure is that those semantics were not reliably converted into execution behavior.

## Root-cause layers

### 1. Governance semantics were stronger than enforcement mechanics

The repository had correct maintenance semantics, but the live ChatGPT decision path is not routed through a repository-owned pre-decision or pre-write runtime on every turn. A rule in the repository can influence behavior when loaded, but repository presence alone is not proof that a live turn executed the rule.

### 2. Methodology conformance conflated declaration with operation

Before this incident response, `runtime/methodology_conformance.py` could prove that a profile version and hook bindings were declared, but it had no separate operational result proving that the required profile was actually activated, required hooks were observed, and referenced evidence was independently verified.

That created an architectural temptation to call a profile "integrated" when it was only structurally declared.

### 3. CI is a real choke point; direct GitHub mutation is not currently a repository-owned pre-write choke point

The Universal repository's GitHub Actions workflow always runs `runtime.system_audit` before pytest. This is an executable control point and can reject bad repository states after a write reaches the branch.

However, ChatGPT's GitHub connector writes do not currently pass through a Universal-owned maintenance dispatcher before the write occurs. Therefore Universal may truthfully claim `CI_ENFORCED_POST_WRITE` for these repository invariants, but must not claim `WRITE_PATH_ENFORCED` for arbitrary GitHub maintenance mutations.

Owner business runtimes can have stronger guarantees when all relevant mutations are already routed through their controller/dispatcher.

### 4. Autonomous escalation behavior still lacks a repeatable product-level eval

This incident itself is real negative product evidence: the user supplied the escalation that Universal should have initiated independently.

The repository now has stronger executable guards against false conformance claims, but that does not by itself prove that future live ChatGPT turns will recognize systemic/repeated-failure signals without user prompting. That behavior needs a trace/eval corpus and repeated product evidence before this incident can be closed.

## Changes made

### A. Declaration and operational methodology conformance are now separate

`runtime/methodology_conformance.py` now exposes:

- `evaluate_methodology_conformance(...)` — declaration-level compatibility only;
- `evaluate_operational_methodology_conformance(...)` — action-level operational evidence.

Operational conformance requires, for every profile activated by the current action:

- the profile is declaration-conformant;
- a real profile-run record exists;
- profile version matches;
- activation id and trigger are present;
- every required hook was observed;
- evidence refs are present;
- an independent caller-supplied evidence verifier accepts every evidence ref.

A receipt without an independent verifier cannot PASS. A declaration-only profile cannot PASS operational conformance.

### B. The separation is now an always-on CI preflight invariant

`runtime/system_audit.py` now includes `methodology_declaration_operational_separation` in `CORE_ALWAYS`.

The preflight runs synthetic negative checks proving that:

- declaration PASS without execution evidence is operational FAIL;
- a self-reported receipt without an independent evidence verifier is operational FAIL.

The fault-injection inventory also includes both failure classes.

### C. Regression evidence

Final behavioral head for this change before maintenance metadata closure:

- head: `0692cd6929370507e8a4d09b2715515520618af5`
- GitHub Actions run: `38042185203`
- job: `114184468600`
- `runtime.system_audit`: PASS
- pytest: `116 passed in 0.20s`

## Explicitly rejected fixes

The following were not adopted merely because they sounded managerial:

- adding a new root `QUALITY_POLICY`, `INCIDENT_POLICY`, or `SELF_CRITIQUE_POLICY`;
- creating `OWNER_RELIABILITY_MODE` before proving a real mutation choke point;
- treating a self-authored execution receipt as evidence by itself;
- binding Financial Writing profiles immediately and then calling the integration operational;
- claiming Universal can pre-block every GitHub write when the current connector write path does not traverse a Universal pre-write dispatcher.

## Remaining work before incident closure

1. Build a repeatable maintenance-decision / escalation eval from real negative traces and counterexamples. It must measure whether the live agent independently distinguishes symptom from systemic/repeated failure, challenges initial mechanisms, and escalates without waiting for the user to act as maintenance operator.
2. Calibrate that eval against real user judgments and held-out cases; do not reduce it to keyword matching such as the presence of "系统有问题".
3. For each owner rollout, require operational evidence only for profiles activated by the current action. Do not make every owner run every profile every turn.
4. For hard pre-write maintenance enforcement, first establish a real maintenance mutation dispatcher / PR gate / equivalent choke point. Until then, report the repository guarantee as `CI_ENFORCED_POST_WRITE`, not `WRITE_PATH_ENFORCED`.
5. Financial Writing remains a target owner for the first strict operational-conformance rollout, but its business task state and active lease must not be rewritten from Universal maintenance.

## External design evidence considered

The design direction is consistent with current agent-evaluation practice: use end-to-end traces, independently graded evidence and stable eval harnesses to measure agent workflow behavior rather than trusting self-reported success. These external sources are candidate evidence only; the accepted changes above are grounded in this repository's actual control points and regression behavior.
