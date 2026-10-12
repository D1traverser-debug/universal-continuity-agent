# Continuity monitor liveness incident — 2026-10-12

## Classification

- subject: `UNIVERSAL_CONTINUITY_RECURRING_MONITORS`
- signal: `D1traverser-debug/universal-continuity-agent#12`
- status: `OPEN_BOUNDARY_REDUCED`
- business_state_mutated: `false`
- business_lease_taken: `false`

## What was actually observed

During a live architecture-watch run, the product automation surface reported `Agent Architecture Watch` and `Continuity Self Audit` as disabled after both had previously been observed enabled in the same broader maintenance window. `Continuity Learning Scout` had also previously been observed disabled. The tasks were subsequently observed enabled again.

Current product-state reread on 2026-10-12 shows all three core Universal monitors enabled:

- `Continuity Self Audit` — enabled
- `Agent Architecture Watch` — enabled
- `Continuity Learning Scout` — enabled

The available automation surface exposes current task state and update timestamps but not mutation provenance. Therefore this incident does **not** establish that deleting automation-generated chats disabled the tasks, nor does it establish another actor or scheduler bug as the cause.

## Parent-system failure model

The unsafe design would be to let each monitor assume its own previous chat is durable state or to auto-reenable any disabled task without distinguishing product drift from an intentional user disable.

The smallest safe repair is reuse of the existing three monitors with cross-monitor liveness observation:

1. every run is a cold start and reconstructs state from current authority/product evidence rather than prior automation chat;
2. each core monitor checks the current product state of the other core monitors;
3. missing/disabled peers create or refresh the non-authoritative liveness signal with exact product-state evidence;
4. absence of mutation provenance must remain explicit;
5. a monitor must not auto-reenable a peer unless current user instruction explicitly authorizes that state change.

This avoids a new watchdog Agent/task while reducing the chance that one silently disabled monitor goes unnoticed by the others.

## Current limitation

A simultaneous disable of all three recurring monitors cannot be self-detected by those monitors. The current product tool does not expose immutable mutation provenance or an external always-on health channel. This remains an explicit product-boundary/open-world limitation, not a hidden PASS.

## Assurance boundary

This audit proves only the observed automation-state facts and the installed cross-monitor checking instructions. It does not prove the root cause of the prior disable transitions or guarantee future scheduler/product availability.
