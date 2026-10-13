# 12 — Cross-Framework Matrix — Pass 2

Status: `QUESTION_GENERATOR / NON_AUTHORITY`

The matrix combines mature systems/reliability disciplines with current agent runtimes. It is not an adoption checklist.

| System dimension | Strong lenses | Current Universal assessment |
|---|---|---|
| Purpose/lifecycle/outline | NASA SE, V-model, IEC/DO public guidance | PARTIAL — local contracts strong; global requirement/evidence lifecycle incomplete |
| Evolution/fitness | Evolutionary Architecture, SRE, AWS OE | PARTIAL — many checks; no unified fitness map |
| Inter-owner interaction | Team Topologies, hierarchical MAPE-K, multi-agent runtimes | GAP — ownership clearer than interaction/backpressure/escalation mode |
| Deterministic vs model routing | Google ADK 2.x, Microsoft workflows, LangGraph | STRENGTH/PARTIAL — deterministic maintenance exists; owner-specific business routing not uniformly modeled |
| Desired vs observed | Kubernetes, GitOps, MAPE-K, LangSmith deployment reconciler | PARTIAL — authority semantics strong; per-resource reconciler inventory absent |
| Execution environment | OpenAI Agents API, MS hosting, ADK, LangGraph, Twelve-Factor | GAP/PARTIAL — readiness exists; substrate/persistence/isolation/replay/evidence matrix absent |
| Durable execution lineage | OpenAI RunState/Session, MS AgentSession+checkpoint, ADK session/events, LangGraph thread/checkpoint | GAP — task lease lineage strong, runtime-nested lineage not unified |
| State taxonomy | current agent runtimes | GAP — session/workflow/memory/artifact/live external state distinctions not declared across adapters |
| Replay/idempotency | distributed systems, all four current runtimes | PARTIAL — Git CAS/unknown outcome strong; shared external-effect replay contract absent |
| HITL/approval | OpenAI SDK, MS RequestPort, ADK HITL, LangGraph interrupt | PARTIAL — user authority strong; exact approval occurrence binding not shared |
| Context transformation | MS Harness compaction, OpenAI managed compaction, long-run agents | GAP/PARTIAL — Git truth protects business state, but compaction/control-obligation invariants not first-class |
| Supervision/recovery | OTP, NASA FDIR | GAP — no shared dependency-aware restart/retry/degraded/escalation topology |
| Reliability governance | Google SRE, AWS OE | GAP — no measurable SLI/SLO/error budget/toil governance |
| Verification architecture | UVM, NASA V&V, DO public assurance, LangSmith/Agents CLI eval | PARTIAL — strong tests/fault injection, weak coverage closure/trace matrix |
| Formal correctness | TLA+, Raft formal reasoning | GAP — core writer/CAS interleavings not model checked |
| Independence/common mode | N-version research, multi-agent orchestrators | PARTIAL — self-attestation boundary strong; no independence matrix |
| Hazard/control | STPA, IEC/NASA safety reasoning | GAP — no explicit losses/hazards/UCA model for high-impact controls |
| Resilience experiments | Chaos Engineering, UVM fault stimulus | PARTIAL — synthetic failures exist; steady-state/blast-radius contracts absent |
| Evaluation feedback | Agents CLI, LangSmith, MS evaluation, OpenAI traces/evals | PARTIAL/GAP — tests exist; live failure → reproducible eval → promotion lifecycle fragmented |
| Protocol compatibility | MCP/A2A/provider integrations | PARTIAL — some pinning exists; selected-runtime protocol compatibility not first-class evidence |
| Knowledge/learning | MAPE-K, postmortems, evolution system | STRONG/PARTIAL — authority precedence strong; typed control-loop knowledge view absent |

## Complementary groups

### MAPE-K + Kubernetes + GitOps
MAPE-K explains control-loop cognition; Kubernetes explains reconciliation; GitOps explains desired-state change authority. They are complementary, not synonyms.

### OTP + FDIR + SRE
OTP gives dependency-aware bounded restart/escalation; FDIR adds detection/isolation/recovery/safe-state reasoning; SRE adds measurable objectives and operational-risk budgets.

### UVM + V&V + TLA+
UVM asks who drives/observes/checks and what coverage remains; V&V asks whether requirements and intended use are proven; TLA+ explores concurrency/state interleavings tests may miss.

### STPA + N-version/common-mode analysis
STPA catches unsafe control even when components nominally work; common-mode analysis prevents “many reviewers” from being mistaken for independent evidence.

### Current agent runtimes
OpenAI, Microsoft, ADK and LangGraph independently converge on several difficult boundaries: durable run identity, pause/resume, approval binding, checkpoint replay, external-effect idempotency, environment separation, tracing/evaluation and nested execution identity. Their differences are useful: there is no one generic “agent state” semantics.

## Negative-space questions required after Pass 2

A future global architecture review should be able to answer:

1. What is the parent-system outline and lifecycle boundary?
2. Which decisions are deterministic workflow versus model judgment?
3. What are every control loop’s sensors, process model, planner, effectors and authority?
4. What are desired-state and observed-state authorities per managed resource?
5. What owner/inter-owner interaction/dependency/backpressure paths exist?
6. Which environment/runtime executes each capability, with what persistence, isolation and evidence ceiling?
7. What exact durable lineage identifies task, runtime session, run, checkpoint, nested execution, tool request and external effect?
8. Which state class is conversation/session, workflow/checkpoint, memory, artifact, cache or external live state?
9. What is the replay unit after interruption/crash/restore for each runtime?
10. How are external mutations idempotently identified and reconciled after unknown outcomes?
11. What exact occurrence does an approval authorize, and when is it invalidated?
12. Can compaction/summarization remove an obligation or change execution semantics without detection?
13. What detects, isolates, recovers, degrades and escalates failures; what are retry/restart budgets?
14. What SLI/SLO/error budget and toil data govern reliability versus change velocity?
15. Which requirements map to which guards/tests/fault/model/live evidence?
16. What states/transitions/interactions/environments/recovery paths remain uncovered?
17. Which concurrency algorithms need model checking?
18. Which reviewers share common-mode failure sources?
19. What losses/hazards/unsafe control actions exist for high-impact mutations?
20. What safe chaos/fault experiment would falsify the design, with what steady-state/blast-radius/abort rule?
21. How does a live failure become a reproducible eval and then a promoted regression guard?
22. What version/protocol combination produced the evidence being relied on?
23. What topology change would invalidate the current single-writer consistency model?

These are research requirements only until the user authorizes implementation/refactor.