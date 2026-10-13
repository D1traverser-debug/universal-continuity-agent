# 17 — State, Resume and External Side-Effect Semantics Matrix

Status: `LEARNING_EVIDENCE / NON_AUTHORITY / PASS2`

The central cross-framework finding is that persistence, resume and exactly-once external effects are different problems. This matrix records the semantic boundary rather than treating “has checkpoints” as “safe to retry.”

| System | Durable identity/state | Resume/replay unit | External-side-effect boundary | HITL identity | Important failure mode |
|---|---|---|---|---|---|
| Universal current | task_id + manifest_version + lease_id + resume_epoch + Git HEAD | owner/controller transition/checkpoint | tool/provider/external product; mutation outcome may be unknown | owner-specific / action receipt | shared idempotency and lineage model incomplete across adapters |
| OpenAI Agents API | Agent Session + saved items; environment has separate identity/lifecycle | asynchronous turn/session continuation | function tools/app handlers or sandbox commands | session/tool call/action identity | event/lifecycle handler failure; session can outlive environment; app owns arbitrary external effect reconciliation |
| OpenAI Agents SDK | Session + serializable RunState | interrupted run; pending session-write reconciliation | application tools/MCP/provider calls | interruption + exact call/tool/agent identity | committed append with lost ACK; concurrent restored snapshots; changed session history |
| Microsoft Agent Framework | AgentSession + workflow checkpoint + pending request identity | executor/workflow checkpoint; request re-emission | executor/tool/provider | RequestPort/request_id/tool approval bound to pending workflow state | side effect between checkpoints; session/checkpoint mismatch; context compaction changing control history |
| Google ADK 2.x | Session + ordered events + State + workflow run/history; Memory/Artifacts separate | workflow/node re-entry/replay depending mode | node/tool/external service | interrupt/request/confirmation identity | failed/resumed nodes can rerun; delivery redelivery can duplicate side effects; parallel state writes race |
| LangGraph | thread_id + checkpoint namespace/state; Store is separate long-term memory | interrupted node restarts from beginning; task/subgraph replay | node/task external calls | interrupt ID + thread/checkpoint lineage | side effects before interrupt/checkpoint can repeat; subgraph namespace/replay races |

## Invariants learned across runtimes

1. **Durable conversation is not durable workflow.** Session/chat history and workflow/controller state need explicit binding.
2. **Durable workflow is not an external transaction.** A checkpoint cannot atomically cover arbitrary email/payment/Git/API effects unless the effect system participates in a transaction or exposes idempotent identity/reconciliation.
3. **Replay granularity must be declared.** Frameworks may rerun a node, executor, tool plan, failed node, or pending write; application code must know the boundary.
4. **Lost acknowledgement is a first-class state.** `not observed success` is not the same as `did not happen`.
5. **Idempotency is semantic.** A key must bind to an operation and its parameters/subject; reusing a key for a materially different request must fail.
6. **Approval is occurrence-specific.** A prior approval must not drift onto a replayed/different action after restore, handoff, compaction or graph restructuring.
7. **Resume needs exclusivity or reconciliation.** Restoring the same durable snapshot in two writers can duplicate work even when each writer is individually correct.
8. **State classes must remain distinct.** conversation/session, workflow/checkpoint, memory, artifact, external observed state and authority are not interchangeable.

## Failure timeline patterns to test

### F1 — effect committed, acknowledgement lost
`prepare -> external effect commits -> response lost -> retry`

Required question: can the system identify the original operation and query/reconcile it before reissuing?

### F2 — local checkpoint persisted before effect
`checkpoint says ready -> process crashes -> restart -> effect executes`

Usually safe if transition semantics explicitly say effect remains pending.

### F3 — effect executed before local checkpoint
`effect commits -> crash before checkpoint -> restart from old checkpoint`

High duplicate risk. Requires idempotency/receipt/reconciliation.

### F4 — approval restored against changed subject
`approval requested -> pause -> code/spec/context changes -> resume`

Approval must be invalidated or rebound only after proving same semantic action.

### F5 — context compaction loses obligation
`pending control pair/approval/tool result -> compaction -> resume`

Compaction must preserve control obligations or make loss detectable.

### F6 — two restored writers
`snapshot S -> restore A and B -> both execute`

Requires exclusive session/lease or effect-layer idempotency plus conflict detection.

### F7 — nested execution identity changes
`parent -> subagent/subgraph -> interrupt -> restore under changed namespace/agent identity`

Requires stable lineage for parent run, nested run, tool call and pending approval.

### F8 — redelivery after external queue timeout
`delivery accepted -> consumer effect -> ack failure -> queue redelivery`

Message/delivery ID must reach the effect boundary, not stop at transport metadata.

## Universal diagnosis

Universal already has strong writer identity for its own Git authority and explicit unknown mutation outcomes, but it does not yet have one shared contract describing all of the following for every effectful capability:

`execution_lineage_id -> action_id/idempotency_key -> semantic subject+parameters -> replay unit -> timeout owner -> retry owner -> backoff/budget -> effect receipt -> ambiguous-outcome query -> approval identity -> post-effect checkpoint`

This is a research finding, not a refactor decision.