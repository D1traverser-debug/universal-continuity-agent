# 15 — Prior Frameworks Deep Pass

Status: `LEARNING_EVIDENCE / NON_AUTHORITY / PASS2`

This pass corrects an overclaim in the first study. Pass 1 was an architecture-level distillation; Pass 2 requires a deeper template for every family: purpose, execution/control model, state and authority, failure semantics, recovery, verification/observability, lifecycle/change, limits/misuse, and concrete questions for Universal. Framework names remain lenses, not automatic design decisions.

## 1. NASA Systems Engineering / V-model reasoning

### Model
NASA systems engineering is lifecycle-oriented and recursive: stakeholder expectations and Concept of Operations feed architecture and requirements; requirements are decomposed and allocated; implementation is integrated upward; verification asks whether each product conforms to specified requirements; validation asks whether the resulting system satisfies intended use and stakeholder need. Lifecycle reviews and decision gates make evidence and unresolved actions visible before promotion.

### State / authority
Requirements need unique identity, source, allocation and controlled change. The useful pattern is bidirectional traceability rather than a prose-only specification. A Requirement Verification Matrix links each requirement to verification method, result and evidence. Validation evidence is distinct from verification evidence.

### Failure / recovery
A changed requirement invalidates downstream assumptions and may require reverification/revalidation. Review gates are not merely status meetings; they are state-transition admission points with explicit entrance/success criteria and action closure.

### Verification lesson for Universal
Universal already has contracts, guards and tests, but lacks one mechanically derived trace answering `requirement/invariant -> owner -> guard/implementation -> test/fault/model evidence -> live evidence -> residual assurance ceiling`. This is a stronger statement than “there are many tests.”

### Misuse boundary
Do not imitate aerospace paperwork density or certification ceremony for a chat control plane. Borrow traceability, evidence separation and lifecycle invalidation only where payoff exceeds maintenance cost.

## 2. Evolutionary Architecture / fitness functions

### Model
Evolutionary architecture treats architecture as intentionally changeable under guided constraints. A fitness function is an objective, repeatable check of an architectural characteristic. Multiple dimensions can conflict, so evolution needs explicit trade-offs rather than a single “architecture score.”

### State / change
Architecture characteristics should have an owner, measurable check, threshold, failure action and promotion semantics. A fitness function is valuable only if it remains coupled to the characteristic it protects.

### Universal question
Current tests defend many qualities—hot-path size, single-writer behavior, owner topology, signal/state separation—but there is no derived map from quality to check and threshold. The system therefore has fragmented fitness functions without a complete fitness portfolio.

### Misuse boundary
Do not add metrics because they are measurable. A metric without a decision rule becomes telemetry toil.

## 3. Team Topologies / inter-group flow

### Model
The relevant concepts are clear ownership plus explicit interaction modes. Collaboration is high-bandwidth and should normally be temporary; X-as-a-Service reduces cognitive load through a stable interface; Facilitation helps a team acquire capability. Platform-as-product exists to reduce repeated cognitive burden, not to centralize every responsibility.

### Universal question
`OWNER_REGISTRY` says who owns a domain, but ownership is not the same as interaction. Universal does not yet first-class whether a relationship is service-like, collaborative, facilitative, temporary, blocking, backpressured or escalation-only.

### Risk
A central platform can become a bottleneck even while ownership is formally correct. Repeated cross-owner manual diagnosis is a cognitive-load signal.

### Misuse boundary
Do not turn organizational terminology into new runtime entities. The useful object is a small interaction/dependency contract.

## 4. Distributed systems: consensus, stale writers, retries, idempotency

### Model
Distributed systems assume partial failure, delayed information and ambiguous outcomes. Consensus protocols such as Raft solve a specific replicated-authority problem; they are not generic reliability decoration. Idempotency and reconciliation solve a different problem: safely repeating operations when the caller cannot know whether the previous attempt took effect.

### Failure semantics
The dangerous case is `request committed -> acknowledgement lost`. Blind retry can duplicate side effects. Safe designs use an operation identity/idempotency key, compare expected parameters, persist or query result identity, and reconcile before retry when outcome is ambiguous. Retry should be bounded with backoff/jitter and should not multiply across layers uncontrolled.

### Universal mapping
The current `SINGLE_ACTIVE_CHAT + lease + resume_epoch + observed-HEAD CAS + reread` model is appropriate to the declared topology. It should not be replaced by consensus absent multiple authoritative writers. The real remaining gap is shared mutation semantics for external tools: idempotency identity, timeout class, retry owner, backoff ceiling, ambiguous-outcome reconciliation and evidence receipt.

### Transition trigger
The system needs an explicit condition that invalidates the single-writer model if autonomous authoritative writers or replicated writer state are introduced.

## 5. UVM verification architecture

### Model
UVM’s value here is separation of verification responsibilities: sequence/sequencer creates stimulus, driver applies it, monitor observes passively, agent packages reusable active/passive components, environment composes them, scoreboard/reference model checks expected versus observed behavior, and coverage asks what has actually been exercised.

### Failure semantics
A driver must not be the sole source of truth about the effect it caused. If expectation and observation come from the same implementation/configuration, self-confirming evidence is possible. Large test counts do not establish coverage closure.

### Universal mapping
Universal has stimulus/action requests, executors, signals/live rereads, deterministic guards and fault scenarios. Missing pieces are a uniform active/passive evidence classification, explicit reference-model identity per critical transition, and coverage across lifecycle states, transition edges, authority conflicts, environments, recovery paths and owner interactions.

### Misuse boundary
Do not recreate UVM class hierarchies/phases in Python. Reuse the separation and coverage ideas only.

## 6. IBM autonomic computing / MAPE-K

### Model
MAPE-K separates Monitor, Analyze, Plan and Execute around shared Knowledge. Sensors and effectors define the manageability interface to the managed element. Autonomic managers can be hierarchical or distributed, and the amount of autonomy may be manual, supervised or automatic.

### State / authority
Knowledge is not one undifferentiated database. Policies, topology, observations, plans, history and objectives can have different authority/freshness semantics. A stale process model can make a logically correct planner choose a harmful action.

### Universal mapping
Universal already performs M/A/P/E behavior across signals, diagnosis, controller planning and mutations, but the knowledge plane is only implicitly typed. A future derived view should state which control-loop step may consume which knowledge class at what freshness/authority.

### Misuse boundary
Do not centralize all knowledge in one store. The system’s current distributed authority model is a strength.

## 7. Kubernetes Controller / Operator

### Model
A controller continuously reconciles observed state toward desired state. It is normally level-triggered/idempotent: repeated reconciliation should converge rather than assume a single event is delivered exactly once. Multiple narrow controllers are preferable to one omniscient controller.

### State / lifecycle
Desired state, observed status and controller ownership are distinct. `ownerReferences` express dependency/garbage-collection relationships. Finalizers turn deletion into an asynchronous lifecycle transition so cleanup can finish before the object disappears.

### Universal mapping
The monitor-deletion history illustrates the core lesson: Git-held past desire is not automatically current desired-state authority for an external product. Each managed resource should declare desired authority, observed authority, reconciler, permission/consent boundary, reconciliation mode and idempotency semantics.

### Misuse boundary
Do not force every task into endless reconciliation. Many user tasks are finite workflows, not controllers.

## 8. Erlang/OTP Supervision

### Model
OTP separates workers from supervisors. Supervision strategy encodes dependency topology: `one_for_one`, `one_for_all`, `rest_for_one`; child restart types and shutdown semantics describe what may be restarted and when. Restart intensity limits stop infinite crash loops and escalate failure upward.

### Universal mapping
Universal can block/reopen and contains some owner-scoped failures, but there is no common supervision topology saying what failure boundary is isolated, what dependent work is invalidated, how often retry/restart is allowed, when to enter degraded/safe hold, and where escalation goes.

### Misuse boundary
LLM/tool calls are not BEAM processes. The transferable idea is dependency-aware bounded recovery, not literal process supervision.

## 9. NASA FDIR / fault management

### Model
Fault Detection, Isolation and Recovery is not just detection. Detection must balance rapid response against false triggers/persistence; isolation determines which component/function is actually affected; recovery must consider safe/degraded operation and the possibility that fault-management logic itself can disable a must-work function or activate a must-not-work function.

### Universal mapping
Control signals and triage are strong on detection/classification. Isolation, recovery mode, retry budget, safe hold, escalation and multiple simultaneous faults are not represented uniformly across subsystems.

### Important consequence
Recovery logic deserves the same assurance scrutiny as the primary path. A bad “repair” can be the hazard.

## 10. GitOps / OpenGitOps

### Model
OpenGitOps principles emphasize declarative desired state, versioned/immutable records, automatic pull/application and continuous reconciliation. Git captures declared intent/history; it does not magically become live observed-state authority.

### Universal mapping
Git `main` is strong engineering/task authority for declared state. External product state must still be reread live. A reconciler must know whether it is authorized to act and whether current user intent supersedes historical desired state.

### Misuse boundary
Do not use GitOps language to justify automatic recreation of user-deleted external resources.

## 11. Google SRE

### Model
SRE turns reliability into a measured product property. SLIs measure user/system behavior; SLOs define target reliability; an error budget quantifies tolerated unreliability and provides a policy mechanism for balancing feature/change velocity with reliability. Monitoring should focus on meaningful symptoms and the golden signals; toil is manual, repetitive, automatable, tactical operational work that should be controlled.

### Universal mapping
Universal has deterministic correctness gates but no quantitative SLI/SLO/error-budget layer for inheritance correctness, false commits, route errors, recovery time, stale external observations, bootstrap/tool cost or user-restatement incidents. Manual cache convergence and repeated evidence assembly are also not measured as toil.

### Misuse boundary
Do not invent unreliable percentages from sparse data. SLO adoption requires observable denominators and a response policy.

## 12. AWS Well-Architected Operational Excellence

### Model
Relevant principles include operations as code, small frequent reversible changes, testing/validation, anticipating failure, learning from events, runbooks/playbooks, operational readiness and guarded automation.

### Universal mapping
The maintenance controller and reopen behavior already embody small bounded changes and learning from failures. Cross-owner rollout/canary and explicit operational-readiness criteria remain ad hoc.

## 13. Twelve-Factor environment parity

### Model
Dev/prod parity minimizes time/person/tooling divergence and uses comparable backing-service semantics. The deeper lesson is not “all environments are identical,” but that unmodeled environment differences create false confidence.

### Universal mapping
Chat, GitHub connector, GitHub Actions, owner Python runtime, plugins/MCP, external product state and independent verifier have different permissions, persistence, isolation and assurance. These differences need a first-class environment/capability matrix; forcing identical behavior would be wrong.

## 14. DO-178C public assurance guidance

### Boundary
DO-178C itself is a copyrighted normative standard. This library uses public FAA/RTCA material and does **not** claim normative compliance.

### Useful assurance ideas
Public guidance supports disciplined lifecycle evidence, requirements-based verification, traceability, configuration control and stronger verification independence as assurance level rises. FAA AC 20-115D recognizes DO-178C as an acceptable means of compliance, not the only possible means or a generic software architecture recipe. Formal methods are addressed through the DO-333 supplement.

### Universal mapping
The transferable capability is bidirectional requirement/evidence trace and explicit assurance independence—not certification paperwork.

## 15. IEC 61508 public functional-safety lifecycle

### Boundary
The normative standard is not reproduced. Public IEC material establishes a safety lifecycle across specification, realization, operation, maintenance and modification, with safety-integrity concepts and independence/competency expectations.

### Universal mapping
Universal is not a safety-certified system, but lifecycle thinking is useful for high-impact control actions: identify safety/reliability constraints early, preserve them through change, and treat modification/maintenance as part of the lifecycle rather than post-design cleanup.

## 16. TLA+ / model checking

### Model
TLA+ specifies state machines and temporal properties; TLC explores bounded reachable states/interleavings and checks invariants/liveness conditions. It complements testing by exploring concurrency schedules developers may not anticipate.

### Universal target
The strongest candidate is the writer/commit protocol: lease ownership, resume epoch, task version, observed Git HEAD, CAS publication, external head movement, ambiguous transport result, authoritative reread, and state/signal separation. Safety examples: two writers must not both successfully claim the same authoritative transition; COMMITTED must not be emitted without verified persistence. Liveness properties need careful fairness assumptions.

### Misuse boundary
Do not formalize low-risk prose generation. Model the small high-value concurrency protocol.

## 17. N-version programming / common-mode failure

### Model
Classic N-version arguments assume independently developed implementations fail independently. Knight & Leveson’s experiments are important because coincident failures were correlated more than the independence assumption would predict.

### Universal mapping
Five agents, five reviewers or five model calls are not five independent evidence sources if they share model family/provider, prompt/specification, upstream authority, tools, evidence corpus or reference checker. High-assurance review needs an independence matrix, not a reviewer count.

## 18. STPA

### Model
STPA begins from unacceptable losses, derives hazards, models the control structure, identifies Unsafe Control Actions, then causal scenarios/constraints. Typical UCA categories include not providing a needed control action, providing one that causes a hazard, unsafe timing/order, and action stopped too soon/applied too long.

### Universal mapping
Useful high-impact controls include takeover, authoritative commit, external retry, deletion/invalidation, delegation, promotion, re-enable/recovery and assurance upgrade. STPA catches interaction hazards even when every component is nominal—for example, applying a valid recovery action under stale user intent.

### Misuse boundary
Do not run STPA on every writing stage. Scope it to control-plane or irreversible/high-impact mutations.

## 19. Chaos Engineering

### Model
Chaos Engineering defines a steady-state hypothesis from observable system behavior, varies realistic events, observes whether steady state persists, automates experiments where practical and minimizes blast radius. Production realism is a means, not permission to damage real state.

### Universal mapping
Synthetic fault injection is already strong. What is missing is an experiment contract: steady state, fault variable, environment, blast radius, abort condition, expected isolation/recovery, measured result and cleanup. Live destructive BUSINESS experiments remain prohibited absent separate justification/authorization.

## Pass-2 synthesis

The mature disciplines converge on a smaller set of recurring engineering obligations:

1. **Explicit state/authority identity** — what state exists, who owns it, what version/lineage it has.
2. **Control-loop separation** — desired vs observed; monitor vs effector; plan vs execution.
3. **Durable transition semantics** — checkpoint, replay, retry, idempotency and ambiguous-outcome reconciliation.
4. **Dependency-aware recovery** — isolation, restart/retry budget, degraded/safe hold and escalation.
5. **Independent verification and coverage** — reference model, passive observation, traceability and uncovered state space.
6. **Measured reliability** — observable objectives, error budgets and toil.
7. **Hazard/common-mode reasoning** — nominal interactions and correlated reviewers can fail together.
8. **Evolution discipline** — small reversible changes, fitness functions, controlled promotion and retirement.

This synthesis is research evidence only. It does not authorize adding named framework modules or changing the production architecture.