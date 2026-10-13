# 12 — Cross-Framework Matrix

This matrix is a **question generator**, not a framework-adoption plan. Each family sees a different failure surface; combining them reduces blind spots without requiring literal transplantation.

| System dimension | Strong source lenses | Core question for Universal | Current state |
|---|---|---|---|
| Purpose / lifecycle / outline | NASA SE, IEC 61508, DO-178C public guidance | Are goals, requirements, interfaces, implementation, verification, validation, operation, modification and retirement connected end-to-end? | PARTIAL; strong local contracts, weak global trace matrix |
| Evolution | Evolutionary Architecture, AWS OE, SRE | Which architectural characteristics must remain fit as the system changes, and how are they measured? | PARTIAL; many tests, no unified fitness map |
| Inter-group interaction | Team Topologies, hierarchical MAPE-K | What interaction mode/dependency exists between Universal and each owner, and when is it temporary vs service-like? | GAP |
| Intra-group flow | UVM, NASA product realization | How does stimulus/input become actions, evidence, checking, transition and output inside an owner? | PARTIAL / owner-specific |
| Desired vs observed state | Kubernetes, GitOps, MAPE-K | Who owns desired state, who owns live observed state, and what reconciler is authorized? | PARTIAL; authority semantics strong but resource inventory absent |
| Control loop | MAPE-K, Kubernetes, STPA | What is monitored, analyzed, planned, executed; what process model can be stale; what effectors can cause harm? | PARTIAL / implicit |
| Change authority | GitOps, NASA CM, DO-178C/IEC lifecycle | How does a candidate change become accepted authority, and how is rollback/supersession controlled? | STRONG locally, promotion model not uniform |
| Distributed consistency | Raft, idempotency practice | Under which writer/topology assumptions is lease+CAS safe; how are ambiguous outcomes/retries handled? | Strong single-writer design; retry contract incomplete |
| Supervision / recovery | Erlang/OTP, NASA FDIR | What fails together, restarts together, escalates, degrades, or enters safe hold? | GAP as a general architecture |
| Reliability governance | Google SRE, AWS OE | What SLI/SLO/error budget governs reliability vs change velocity and operational toil? | GAP |
| Environment architecture | AWS OE, Twelve-Factor, execution-readiness contract | What can execute in chat/CI/owner runtime/plugin/external verifier, with what parity and evidence promotion? | PARTIAL; capability handshake exists, no unified matrix |
| Verification architecture | UVM, NASA V&V, DO-178C | Are driver and monitor independent; what is the reference model; what coverage is closed? | PARTIAL; no unified coverage closure |
| Formal correctness | TLA+, Raft formal-spec practice | Have core concurrency/state invariants been modeled across all interleavings? | GAP |
| Diverse assurance | N-version research | Are reviewers/models actually independent across failure domains, or merely different labels on correlated paths? | PARTIAL; strong self-attestation rules, no common-mode matrix |
| Safety/hazards | STPA, IEC 61508, NASA FDIR | What system losses/hazards can occur from unsafe control actions even without component failure? | GAP |
| Resilience experiments | Chaos Engineering, UVM fault stimulus, NASA test | What steady state should survive which injected fault, with what blast radius? | PARTIAL; synthetic scenarios exist, no steady-state/coverage model |
| Observability | SRE, MAPE-K, Kubernetes status/conditions | Which signals show user-facing health, control-plane health, saturation, and degradation? | PARTIAL; incidents/signals exist, operational metrics fragmented |
| Knowledge / learning | MAPE-K Knowledge, Evolutionary Architecture, SRE postmortems | What knowledge is authoritative vs cached vs candidate vs historical, and how does accepted learning change future behavior? | Strong authority precedence; typed knowledge-plane view absent |

## Framework complementarity

### MAPE-K + Kubernetes + GitOps

Together they distinguish **control-loop cognition**, **declarative reconciliation**, and **change authority**. They should not be collapsed into one mechanism. MAPE-K asks how the controller reasons; Kubernetes asks how current and desired state converge; GitOps asks how desired state is versioned/distributed/reconciled.

### OTP + NASA FDIR + SRE

OTP gives dependency-aware restart/escalation; FDIR gives fault detection/isolation/recovery and safe/degraded response; SRE gives measurable reliability objectives and budgeted operational risk. Together they expose the difference between “we detected a defect” and “the system has a bounded, observable recovery strategy.”

### UVM + NASA V&V + TLA+

UVM emphasizes reusable drivers/monitors/scoreboards/coverage; NASA/assurance practice emphasizes requirement-to-verification/validation traceability; TLA+ explores state/concurrency properties. A system with all three evidence types is much harder to fool than one with only unit tests or reviewer prose.

### STPA + N-version research

STPA attacks unsafe system control and flawed process models; N-version research attacks false confidence from apparently independent redundancy. Together they warn that several reviewers can agree on the same unsafe action if they share a flawed specification or evidence source.

### Evolutionary Architecture + Team Topologies + Operational Excellence

These lenses prevent the remedy itself becoming the next problem: use fitness functions to guide change, explicit interaction modes to prevent coordination sprawl, and small reversible changes to limit blast radius.

## Negative-space questions now required by the benchmark

A future architecture review should be able to answer, at minimum:

1. What is the system outline and lifecycle boundary?
2. What are the control loops and their sensors/effectors?
3. What are the desired/observed states and reconcilers?
4. What are the inter-owner and intra-owner interaction/dependency paths?
5. What environments execute/verify each capability?
6. What are the reliability objectives and budgets?
7. What detects, isolates, recovers and escalates failures?
8. What hazards/unsafe control actions exist?
9. What requirements map to which verification and validation evidence?
10. What transition/interaction/failure coverage remains untested?
11. Which core algorithms need formal model checking?
12. Which “independent” reviewers share common-mode failure domains?
13. How is architecture evolution fitness measured?
14. How are changes promoted, canaried, rolled back and retired?
15. What chaos/fault experiments are safe and what steady state must survive them?

These questions are research output only until the user authorizes refactor/adoption.
