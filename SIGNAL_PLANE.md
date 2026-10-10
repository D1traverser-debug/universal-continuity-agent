# Universal Control Signal Plane

The Signal Plane reports observations; it does not mutate authoritative task or business state.

## Transport

Preferred transport: a GitHub Issue in this repository with title prefix `[CONTROL_SIGNAL]` and a body conforming to `CONTROL_SIGNAL_CONTRACT.json`.

Signal emitters may include a stale chat, owner CI, a remote monitor or a current maintenance writer. A signal emitter does **not** acquire or bypass a writer lease by emitting a signal.

## Consumption

The current valid Universal maintenance writer re-observes the evidence before acting. It then either:

- consumes the signal into an authorized maintenance action; or
- closes/rejects it with an evidence-backed reason.

Closing an issue does not rewrite owner business truth.

## Monitoring boundary

Local Universal CI can detect self-drift and validate recorded owner observations. It cannot discover newer private owner repository HEADs unless an execution surface with access to those repositories performs the remote observation.

Recurring remote monitoring must therefore run through an authorized GitHub-connected execution surface and compare current owner HEAD/AGENT_MANIFEST/CI against `OWNER_ARCHITECTURE_OBSERVATIONS.json`. Detected drift should emit or update a `[CONTROL_SIGNAL]` issue, not write task state directly.
