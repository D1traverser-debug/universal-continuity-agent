# 11 — STPA: System-Theoretic Hazard and Control Analysis

## Why STPA adds a different lens

Traditional defect/failure analysis often begins with component failures. STPA begins from unacceptable losses and treats accidents as control problems in complex systems. MIT's STPA process broadly asks analysts to:

1. define the purpose of the analysis, including losses and system-level hazards;
2. model the control structure;
3. identify unsafe control actions;
4. identify scenarios that could produce those unsafe actions;
5. derive constraints/requirements and mitigations.

This matters because a component can behave “as designed” while the overall control action is unsafe in context.

## Unsafe control-action categories

A useful STPA-style checklist is whether a control action is unsafe because:

- it is not provided when needed;
- it is provided when it should not be;
- it is provided too early, too late, or in the wrong order;
- it lasts too long or stops too soon.

For Universal, this applies naturally to control actions such as:

- taking over a task;
- committing authority changes;
- retrying external mutations;
- marking work `COMMITTED`;
- promoting research/candidate rules to authority;
- invalidating downstream evidence;
- re-enabling monitors/automations;
- delegating to a BUSINESS owner;
- blocking or freezing an owner;
- deleting/superseding artifacts;
- escalating a failure to a wider scope.

## Control structure for Universal

A simplified control structure contains:

- user goals/authorization;
- ChatGPT/Universal control plane;
- maintenance controller;
- owner registries/contracts;
- BUSINESS owner runtimes/state;
- GitHub engineering authority;
- signal/monitor/CI observers;
- external plugins/services/product state;
- evidence/verification harnesses;
- effectors that mutate repositories, business state or external systems.

Each controller makes decisions based on a process model. STPA asks what happens when that internal model is stale, incomplete or contradictory—even if the controller logic itself is locally correct.

## Example system-level hazards

Non-authoritative analysis candidates:

- H1: wrong owner/task receives or commits a material action;
- H2: stale/lower-authority state overwrites newer truth;
- H3: an action is declared complete without required evidence/outcome;
- H4: recovery/reconciliation reverses explicit user intent;
- H5: a local failure response damages unrelated healthy owners;
- H6: a high-impact external side effect is repeated after ambiguous outcome;
- H7: a candidate/learning artifact silently becomes production authority;
- H8: cross-owner propagation changes business truth without owner authority;
- H9: verification is self-confirming while labeled independent;
- H10: control-plane complexity makes a critical invariant unreachable or bypassable.

Universal already defends many concrete instances of these hazards. The gap is that hazards and unsafe control actions are not maintained as a first-class architecture layer that systematically generates constraints/tests.

## How this differs from current failure classes

Current maintenance failure classes are incident/repair oriented. STPA is complementary:

- failure class asks “what reusable kind of defect occurred?”;
- hazard/control analysis asks “what unsafe control action could cause an unacceptable system outcome, including when no component has failed?”

This distinction can reveal gaps that a bug-history search cannot.

## Human / model / automation interaction

STPA also encourages treating humans, automation and software as one control structure. That matters because the user is an authority source for goals/permissions but is not the maintenance operator; ChatGPT may infer intent incorrectly; plugins may report incomplete state; and automated recovery may conflict with a user's later decision.

## What not to transplant

Do not label ordinary editorial errors as safety hazards or create heavyweight hazard paperwork for low-impact tasks. Apply the method to control-plane and high-impact actions where incorrect control can cause durable loss, unwanted mutation, financial/user harm, or integrity failure.

## Current assessment

- Failure/incident classification: **PRESENT**.
- Explicit system-level loss/hazard catalog: **CURRENT GAP**.
- Unsafe-control-action analysis: **CURRENT GAP**.
- Control-structure modeling: **PARTIAL in prose, not formalized as hazard analysis**.
- Hazard-derived test/constraint traceability: **CURRENT GAP**.
