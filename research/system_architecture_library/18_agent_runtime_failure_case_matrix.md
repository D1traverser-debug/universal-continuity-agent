# 18 — Agent Runtime Failure-Case Matrix

Status: `LEARNING_EVIDENCE / NON_AUTHORITY / PASS2`

This file records implementation-level failure evidence as a supplement to normative/official documentation. Issues and bug reports show where real runtimes have broken; they do not define the intended framework contract by themselves.

## OpenAI Agents SDK

Observed class: **lost acknowledgement / duplicate pending input on resume**.

A reported RunState/Session case committed a client-managed Session append and then raised as if acknowledgement had been lost. Retrying from the durable RunState could treat the same logical input as pending, append it again, and repeat an already-passed guardrail. The expected repair was to use fail-closed session-write reconciliation: recognize the checkpoint-owned exact pending batch, distinguish atomic failure from lost ACK where possible, and avoid rerunning completed tool/guardrail work.

Implication: even with a serializable RunState, persistence needs occurrence identity and reconciliation around a separate Session backend.

## Microsoft Agent Framework

Observed classes in current issue history include:

- approval/request restoration identity conflicts after reconnect;
- approval resume depending on the same session/context provider lineage;
- external side effects replaying when failure occurs after tools execute but before the next workflow checkpoint;
- context compaction mutating/deleting history or breaking tool-call / approval / structured-output pairings;
- MCP/protocol-version incompatibility at integration boundaries.

Implication: a rich harness creates control state beyond chat messages. Compaction, approval requests, provider sessions, checkpoints and external effects all need distinct lineage/compatibility evidence.

## Google ADK 2.x

Observed classes in current releases/issues include:

- resumable checkpoint/history growth from repeatedly embedding resume input/history;
- external delivery redelivery creating a new session and repeating side effects when transport identity is not propagated to tools;
- resumable execution accepting/replaying function-call-shaped inputs where author/provenance checking becomes security-relevant;
- confirmation/HITL resume loops or skipped later confirmations;
- release semantics where failed workflow nodes rerun on resume, requiring effectful nodes to be idempotent.

Implication: graph persistence needs explicit replay contracts and provenance, not just “resume supported.”

## LangGraph

Observed/documented failure classes include:

- an interrupted node restarts from the beginning, so code before the interrupt can execute again;
- a tool/side effect can be repeated after error/resume unless effect identity is durable;
- parallel/nested subgraph resume can replay already-completed sibling work when checkpoint namespaces/lineage are mishandled;
- durability timing (`sync`, `async`, `exit`) changes persistence timing but does not imply exactly-once external effects;
- checkpoint namespace/time-travel/replay boundaries are correctness-critical for nested graphs.

Implication: node checkpointing solves graph-state durability, not arbitrary effect transactions.

## Cross-runtime failure families

| Failure family | Typical symptom | Architectural question Universal should ask |
|---|---|---|
| Lost ACK | duplicate input/tool/effect after retry | Can the exact prior outcome be reconciled by durable operation identity? |
| Replay after checkpoint gap | external effect executes twice | What is the replay unit and is the effect idempotent/receipted? |
| Duplicate writers/restores | two continuations from one snapshot | What exclusive-writer/session lease or conflict detection exists? |
| Approval drift | old approval authorizes new occurrence | Is approval bound to exact action subject, call/run identity and version? |
| Compaction corruption | pending tool/approval obligations disappear | Is compaction provenance/versioned and are control pairs invariant-checked? |
| State-class confusion | memory treated as workflow truth | Are session/workflow/memory/artifact/external-state semantics explicit? |
| Namespace/identity drift | nested work resumes under wrong subflow | Are parent/child execution identities stable and collision-free? |
| Transport redelivery | duplicate external operation | Does transport message ID reach the business-effect idempotency layer? |
| Protocol drift | integration silently breaks/misinterprets | Is protocol/version compatibility negotiated and evidence-bound? |
| Observability illusion | trace exists but outcome unverified | Does passive/live evidence independently establish the claimed effect? |
| Common-mode multi-agent failure | many agents agree on same wrong premise | Which independence axes are actually distinct? |

## Research conclusion

The repeated pattern across unrelated agent frameworks is not “frameworks are unreliable.” It is that **durable agent execution is a distributed-systems problem once state, approvals, tools and external effects cross persistence boundaries**. Any future Universal refactor should therefore be judged against concrete failure timelines, not just feature checklists.