# 16 — Current Agent Runtime Frameworks Deep Pass (2026)

Status: `LEARNING_EVIDENCE / NON_AUTHORITY / PASS2`

Scope: direct comparison of currently active agent frameworks that are closest to Universal’s problem domain. This is not a benchmark leaderboard and does not imply adoption. The goal is to learn concrete runtime/state/resume/HITL/evaluation/failure semantics that a control-plane architecture review should understand.

## A. OpenAI Agents API

### Product boundary
The Agents API is a managed agent harness. OpenAI runs the Codex harness and manages durable sessions, orchestration, context compaction and recovery; the application supplies tasks/tools and chooses an execution environment. The architecture separates:

- **Harness** — OpenAI-hosted model/tool loop and session orchestration.
- **Environment** — none, OpenAI-hosted sandbox, or self-hosted compute/files.
- **Application server** — submits work, consumes events/webhooks, executes function tools and may manage self-hosted environment lifecycle.

This separation matters because “agent code exists” and “the current chat can execute its environment” are different facts.

### State model
A **Session** is the durable work identity. A session persists configuration, conversation and saved work across asynchronous turns. Environment lifetime is distinct: a session can outlive its sandbox. Event streams report live progress; saved items are durable work objects. A quiet stream or completed turn is not sufficient proof that every external action succeeded—the application must inspect the actual turn outcome/tool results.

### Environment lifecycle
Self-hosted environments connect outward through a restricted environment key and executor. The application owns provisioning, reconnection, shutdown and preservation of files. One component should own a session environment; repeated or concurrent requests must not create duplicate environments. Credentials/environment identity are therefore part of the runtime correctness boundary.

### Failure/recovery questions
The managed harness reduces application orchestration burden but does not remove external-side-effect ambiguity, function-tool idempotency, webhook/event-handler failure, environment cleanup or credential isolation. Durable session state and environment state are intentionally separate.

### Security/data boundary
Self-hosting the sandbox does not make the Agents API equivalent to fully self-hosted inference/session infrastructure. Current official documentation states Agents API session retention/data-residency constraints separately from sandbox location.

## B. OpenAI Agents SDK

### Runtime model
The SDK is the application-controlled harness. Its core primitives include Agents, tools, handoffs/agents-as-tools, guardrails, Sessions, human-in-the-loop approvals, tracing and MCP. The Runner repeatedly invokes a model, interprets final output/handoff/tool work, executes the next step and continues until completion or a turn limit.

### Durable pause/resume
`RunState` is the durable human-in-the-loop pause/resume boundary. It serializes context, usage, model responses/generated items, interruption/approval state and optional server-managed identifiers.

Current SDK semantics make several important correctness rules explicit:

- resume against the **original Session backend/session ID**;
- restored snapshots require **exclusive access** to the same Session history;
- independently restored snapshots must not resume concurrently against one Session;
- pending Session writes are reconciled before another model call;
- changed or ambiguous Session history fails closed rather than silently guessing;
- a completed tool action must not be rerun merely because acknowledgement/persistence around it was uncertain.

These are directly analogous to Universal’s lease/CAS/reconciliation concerns.

### HITL / approval identity
Approvals may interrupt top-level tools, handoffs or nested `agent.asTool` execution. Correct resume requires stable call/tool/agent identity, not just a boolean “approved.” Approval state is part of durable run lineage.

### Tool lifecycle
The strongest pattern is to normalize model output into an execution plan before side effects, evaluate guardrails/approvals, execute tools with lifecycle hooks/timeouts/concurrency constraints, and then persist/continue. This cleanly separates model suggestion from effectful execution.

### Observability
Built-in tracing provides run/model/tool/handoff/guardrail spans, but observability availability is itself an environment/data-policy capability. Trace presence is evidence, not business correctness.

### Implementation failure evidence
Current SDK history contains real lost-ack/resume failure cases. One documented issue reproduced a Session append that committed and then lost acknowledgement, leaving pending input vulnerable to duplicate append/re-executed guardrail on retry. The fix direction was fail-closed Session-write reconciliation. This is evidence that checkpoint identity and exactly-once-ish reconciliation are not theoretical edge cases even in mature agent runtimes.

## C. Microsoft Agent Framework 1.x

### Current direction
Agent Framework unified Microsoft’s agent/workflow efforts and by current 1.x releases provides four broad layers: Agents, Harness Agent, Workflows and integrations/hosting/protocols. It is useful to distinguish **model-directed agency** from **developer-directed workflows**.

### Harness Agent
The Harness composes a chat client, function invocation, service-call history persistence, optional context compaction, todo/planning state, plan/execute modes, file memory/access, tool approval, OpenTelemetry and optional looping/background agents. `AgentSession` persists harness history plus session-scoped planning/todo state.

This is important for Universal because a “harness” is not merely a prompt. It is runtime scaffolding with state, policy and effect-control responsibilities.

### Workflow model
Workflows expose explicit graph/functional orchestration and built-in patterns:

- Sequential;
- Concurrent;
- Handoff;
- Group Chat;
- Magentic manager coordination.

Microsoft’s guidance draws a clean line: if the **model** should decide what happens next, agents-as-tools are appropriate; if the **developer** owns the path, use workflows. Universal should preserve this same distinction between deterministic business gates and high-judgment generation.

### Group/session topology
Group Chat does not force all agents to share one `AgentSession`; the orchestrator synchronizes conversation history into distinct sessions because heterogeneous agents may implement session state differently. This is a concrete warning against pretending “shared conversation” means “shared state object.”

### HITL
Workflow HITL uses request/response channels (`RequestPort` / request events). A pending request has an identity; responses route to the originating request/executor. Tool approvals use the same pause/resume mechanism. A restored checkpoint re-emits pending requests, so request identity survives process restart.

### Checkpoint state
Workflow checkpoints are not identical to `AgentSession`. Checkpoints capture workflow/executor state and pending external requests; agent executors may serialize an agent session into that checkpoint. Provider/server-managed sessions can have different capture semantics. This separation—workflow state vs conversational agent state—is highly relevant to Universal owner adapters.

### Observability/evaluation
Agent Framework uses OpenTelemetry traces/logs/metrics and exposes workflow events/delivery outcomes. Evaluation is a separate capability that can use local, managed or custom evaluators. Runtime execution, observability and evaluation therefore remain distinct evidence planes.

### Failure surface
Feature-rich harnesses introduce extra correctness surfaces: compaction can remove/rewrite history; approval resume must remain bound to the right session/request; side effects performed between checkpoints can replay after failure; protocol integrations can drift in version. These are not reasons to avoid a harness; they are reasons to model lineage, compaction and replay explicitly.

## D. Google ADK 2.x and Agents CLI

### Architectural direction
ADK 2.x adds graph-first workflows alongside autonomous agents. Google’s stated rationale is that deterministic business routing should not be delegated to an LLM when the process is known. Deterministic nodes, tool calls, HITL and specialized LLM agents can be composed in one graph/runtime.

### Graph/workflow model
Workflows support branching, fan-out, loops, retries, concurrency, timeouts and nested/dynamic execution. Single agents and graphs share the runner/session/event model. This reduces the accidental difference between “agent execution” and “workflow execution.”

### HITL/resume
ADK 2.x can durably pause a workflow for external input and later resume after restart. Re-entry semantics matter: a paused node may rerun with the resumed input. Completed child work can be replayed from history, while failed nodes may rerun depending on current workflow semantics. External side effects therefore need idempotency/reconciliation.

### Session/state/events
ADK distinguishes:

- **Session** — identity/conversation/event history;
- **State** — values changed through event deltas, with session/app/user/temp scopes;
- **Memory** — longer-term retrieved corpus/knowledge, not exact workflow state;
- **Artifacts** — versioned files/data associated with work;
- **Events** — execution/conversation record.

A SessionService owns persistence. In-memory storage is a development convenience; durable/database services have stronger stale-write/storage semantics. Parallel state updates and scope semantics remain an application concern; persistence alone is not serializability.

### Plugins/callbacks
Callbacks operate around particular agent/model/tool execution; plugins can apply application-wide behavior. This distinction resembles owner-local hooks versus Universal cross-cutting policy and should remain explicit.

### Agents CLI/evaluation lifecycle
Agents CLI covers scaffold/build/run/evaluate/deploy workflows. Evaluation can run datasets locally or against a deployed endpoint, generate/grade traces and measure quality/cost/latency dimensions. This is notable because it turns agent development into a lifecycle, not only a runtime loop.

### Failure surface
Current ADK development has exposed resumable-state growth, delivery redelivery/duplicate side effects, tool-confirmation resume problems and provenance questions around replayed function calls. A central lesson is the same as other runtimes: persistent workflow history does not automatically guarantee exactly-once external effects.

## E. LangGraph 1.2.x / LangSmith

### Execution model
LangGraph exposes explicit state graphs (Pregel-inspired execution), nodes, edges and dynamic routing (`Command`/fan-out patterns). State is an application-defined schema; nodes return state updates and routing decisions. It is deliberately lower-level than an opinionated agent harness.

### Persistence model
A **checkpointer** persists thread-scoped graph execution state. A **Store** provides longer-term cross-thread application memory. These should not be conflated. Production Agent Server deployments may add managed persistence around threads/runs/assistants.

### Interrupt/resume semantics
`interrupt()` persists graph state and pauses until resumed under the same thread identity. Crucially, when execution resumes, the interrupted **node restarts from its beginning**. Code/side effects before the interrupt may run again. Node granularity therefore defines replay granularity.

### Durability modes
`sync`, `async` and `exit` determine when checkpoints are durably written relative to graph progress. They are persistence timing choices; they do **not** create exactly-once semantics for external side effects. Effectful work must be idempotent or wrapped in a recoverable task/receipt pattern.

### Subgraphs / namespaces
Nested graphs introduce checkpoint namespaces and state propagation boundaries. Resume/time-travel/replay correctness depends on stable execution identity across parent/subgraph boundaries. This is directly analogous to nested agents/owner subflows needing lineage rather than only a human-readable name.

### Error/recovery model
LangGraph encourages explicit classification: transient retryable errors, LLM-recoverable errors, user-fixable interruptions, unexpected failures and compensation/saga patterns. This is stronger than a universal “retry on exception” rule.

### LangSmith lifecycle
LangSmith adds tracing and offline/online evaluation. Offline evaluation supports benchmark/regression/unit-like datasets and multiple evaluator types; online evaluation operates on production traces/feedback. Deployment infrastructure itself uses a desired/current reconciliation model. Runtime correctness and evaluation quality remain separate evidence types.

### Failure surface
Real graph systems can replay a completed external side effect after checkpoint or subgraph-resume races. The framework’s own documentation emphasizes idempotent side effects, stable thread identity and correct checkpoint boundaries. Persistence is a necessary substrate, not a transaction across arbitrary external systems.

## Cross-runtime comparison

| Concern | OpenAI Agents API/SDK | Microsoft Agent Framework | Google ADK 2.x | LangGraph/LangSmith | Universal implication |
|---|---|---|---|---|---|
| Deterministic workflow vs agent judgment | API harness + SDK routing/handoffs; app still owns deterministic gates | explicit “model decides vs developer decides” distinction | graph workflows explicitly separate routing from LLM reasoning | explicit graph nodes/edges plus agent nodes | keep deterministic business/control gates outside free-form model discretion |
| Durable work identity | Session; SDK RunState + Session | AgentSession + workflow checkpoint/request IDs | Session + event history + workflow run/resume | thread/checkpoint namespace | define one execution-lineage model across adapters |
| Memory vs workflow state | session/generated items vs app memory/tools | session/context providers vs workflow checkpoint | Session/State/Memory/Artifacts distinct | checkpoint state vs Store memory | stop using generic “state/memory” terminology when semantics differ |
| HITL | durable interruption/approval call identity | request ports + pending request/checkpoint identity | interrupt/resume / confirmation | interrupt + thread/checkpoint identity | approval needs stable subject/call/run identity and expiry/invalidation rules |
| Replay | Session-write reconciliation required | checkpoint replay and side-effect windows | failed/resumed nodes may rerun | interrupted node restarts; task may replay | declare replay granularity and side-effect idempotency per runtime |
| External effects | app/tool responsibility | tool/executor responsibility | node/tool responsibility | node/task responsibility | shared external-mutation receipt/idempotency contract is a real gap |
| Compaction | managed API / SDK context controls | Harness compaction | model/runtime context strategies | summarization/middleware depends stack | context transformation must be observable/versioned when it affects execution |
| Observability | session events, tracing, webhooks | OpenTelemetry + workflow events | events/traces/eval tooling | tracing + LangSmith | trace identity should link to durable task/action/evidence without becoming authority |
| Evaluation | eval ecosystem separate from execution | evaluator framework | Agents CLI/eval datasets | LangSmith offline/online | need a promotion loop from failures to durable regression evidence |
| Environment isolation | none/openai-hosted/self-hosted sandbox | hosting/protocol/provider dependent | local/deployed runtimes | local/Agent Server/sandbox backends | execution environment must be explicit in assurance claims |

## New architecture lessons for Universal

1. **Checkpoint identity is not enough; execution lineage is the real invariant.** Session/thread/run/checkpoint/subgraph/request/tool-call identities must compose without ambiguity.
2. **HITL approval is a stateful protocol.** It must bind to an exact action and durable execution identity; restoration/replay must not silently approve a different occurrence.
3. **Compaction is a mutation of execution context.** It needs provenance/observability and must preserve control pairs, pending approvals and durable obligations.
4. **Persistence is not exactly-once.** Every current runtime still pushes idempotency/reconciliation responsibility to the application boundary for arbitrary external side effects.
5. **Workflow state, conversation/session state, memory, artifacts and live external state are distinct classes.** Universal should not collapse them under one “state” label.
6. **Environment is part of assurance.** Sandbox/connector/hosted/self-hosted/provider boundaries change what can execute, persist, observe and prove.
7. **Evaluation belongs to a lifecycle.** Offline regression, online traces, production failure mining and promotion to durable tests should be connected but not conflated with runtime execution.
8. **Multi-agent topology is not evidence independence.** Separate sessions or agents may still share model/spec/evidence/runtime failure domains.

These lessons refine the research gap model. They do not authorize changing Universal or any BUSINESS owner.