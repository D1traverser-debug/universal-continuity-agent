# 05 — MAPE-K and Kubernetes Controller / Operator

## MAPE-K

IBM autonomic-computing architecture organizes self-management as an explicit closed loop:

`Monitor -> Analyze -> Plan -> Execute`, sharing `Knowledge`, with sensors observing managed resources and effectors changing them.

The key engineering value is separation of concerns:

- **Monitor** gathers/filter/aggregates observations rather than deciding policy;
- **Analyze** correlates observations and recognizes conditions;
- **Plan** turns policy/objectives into an action sequence;
- **Execute** applies the plan through controlled effectors;
- **Knowledge** stores the models, policies and historical/state information used across the loop.

IBM also discusses flat versus hierarchical autonomic managers, which is relevant to whether one central controller should manage everything or local owner controllers should coordinate under a smaller higher-level manager.

### Universal mapping

Current Universal roughly maps as:

- Monitor: signal plane, live rereads, CI/remote observations, user failure evidence;
- Analyze: triage, maintenance diagnosis, failure-class/history logic;
- Plan: maintenance stages, alternatives, next_action, Agent-ready brief;
- Execute: owner/runtime actions, Git mutations, tool calls;
- Knowledge: policies, manifests, research/audits, checkpoints, evidence and historical failure records.

The mapping is real but **implicit and fragmented**. In particular, “Knowledge” is not one authority—and should not become a giant database—but there is no typed derived map that says which knowledge class is authoritative, cached, historical, candidate, operational evidence or business truth for each loop.

## Kubernetes controller pattern

Kubernetes controllers are non-terminating reconciliation loops. Resources expose desired state (commonly `.spec`); controllers observe current state, take actions and update status until reality approaches the declared intent. Custom resources plus controllers create declarative APIs; Operators add domain-specific operational knowledge around lifecycle tasks such as deployment, upgrades, backup/restore and recovery.

Important transferable properties:

- **spec/status separation** — desired intent is distinct from observed state;
- **level-based reconciliation** — repeatedly converge on the latest desired state rather than assuming one event is processed exactly once;
- **narrow controllers** — each controller focuses on a bounded resource/domain;
- **domain-specific operator knowledge** — lifecycle procedures live near the managed domain;
- **idempotent reconciliation** — repeated runs should converge safely;
- **conditions/status** — observed blockers and progress are first-class state.

### Universal mapping

Universal already has some controller-like behavior:

- owner manifests/checkpoints describe desired/current task state;
- `maintenance_controller.py` guards legal workflow transitions;
- external observations are re-read before present-tense claims;
- state plane and signal plane are explicitly separated;
- BUSINESS owners retain domain-specific lifecycle semantics.

But current Universal is still more **workflow/transaction oriented** than continuously reconciled. A task can have `next_action`, blockers and checkpoints, but there is no general resource model with explicit desired spec, observed status, conditions, observed generation and reconciler identity for every control-plane object.

## Where reconciliation should and should not apply

Good candidate uses:

- registry/observation cache convergence;
- external tool/service desired-vs-observed configuration when the user has authorized continuous management;
- architecture observation freshness;
- task execution where repeated reconciliation is safely idempotent.

Bad use:

- silently re-enabling a user-disabled automation because Git says it “should” exist;
- forcing BUSINESS state from Universal;
- continuously mutating systems whose authority lives externally;
- treating historical evidence as desired state.

The current monitor-deletion incident is evidence that GitOps/controller reconciliation needs a **resource authority classification** before it can act.

## Main current gaps

1. No first-class, consistent `desired / observed / conditions / generation / reconciler` schema across control-plane resources.
2. No explicit typed knowledge-plane view for MAPE-K loops; knowledge is authority-disciplined but distributed.
3. No general idempotent reconcile contract for owner/tool mutations.
4. No explicit hierarchy of local owner controllers versus higher-level Universal controller responsibilities beyond prose/contracts.

## What not to transplant

Do not turn every task into a Kubernetes CRD or introduce endless reconciliation loops. ChatGPT interactions and user-authorized external state have different cost and consent boundaries. Use reconcile semantics where repeated observation/convergence is valuable and safe; preserve event-driven cold paths elsewhere.

## Current assessment

- Monitor/analyze/plan/execute capabilities: **PRESENT**.
- Shared knowledge authority discipline: **PRESENT, but no typed MAPE-K knowledge view**.
- Desired/observed separation: **PARTIAL**.
- Continuous reconciliation: **SELECTIVE / not generalized**.
- Operator-style owner-local lifecycle knowledge: **PRESENT in principle**.
