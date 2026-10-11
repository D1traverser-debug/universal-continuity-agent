# Universal Control Signal Plane

The Signal Plane reports observations; it does not mutate authoritative task or business state.

## Transport

Preferred transport: a GitHub Issue in this repository with title prefix `[CONTROL_SIGNAL]` and a body conforming to `CONTROL_SIGNAL_CONTRACT.json`.

Signal emitters may include a stale chat, owner CI, a remote monitor or a current maintenance writer. A signal emitter does **not** acquire or bypass a writer lease by emitting a signal.

## Consumption: verify before clarify before delegate

The current valid Universal maintenance writer must not treat the signal body as established truth or immediately turn missing internal facts into user questions. Consumption follows the current contract/runtime sequence:

1. **REOBSERVE** — re-check the reported claim against current authority/environment;
2. **RESOLVE_RETRIEVABLE_FACTS** — current HEAD, CI, manifests, runtime state and other accessible facts are system work, not user decisions;
3. **CLASSIFY_ACTIONABILITY** — decide whether a real maintenance action exists;
4. **ASK_ONLY_UNAVAILABLE_FACT_OR_HUMAN_JUDGMENT** — interrupt the user only when the fact cannot be safely retrieved/inferred or a genuine judgment/irreversible choice is required;
5. **BUILD_AGENT_READY_BRIEF** — actionable delegated work gets a compact brief with behavior, current/desired state, stable interfaces, acceptance criteria, out-of-scope boundaries and evidence refs;
6. **DELEGATE_OR_CLOSE** — delegate from the stable brief or close/retain the signal with an evidence-backed reason.

Raw chat/issue history is not an Agent-ready brief. A work-admission state is process evidence only; it does not prove the diagnosis is semantically correct.

Closing an issue does not rewrite owner business truth.

## Monitoring boundary

Local Universal CI can detect self-drift and validate recorded owner observations. It cannot discover newer private owner repository HEADs unless an execution surface with access to those repositories performs the remote observation.

Recurring remote monitoring must therefore run through an authorized GitHub-connected execution surface and compare current owner HEAD/AGENT_MANIFEST/CI against `OWNER_ARCHITECTURE_OBSERVATIONS.json`. Detected drift should emit or update a `[CONTROL_SIGNAL]` issue, not write task state directly.
