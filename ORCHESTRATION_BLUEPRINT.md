# Universal Agent Orchestration — Blueprint

Status: ACTIVE  
Execution-readiness contract: v1.0  
Continuity protocol: v3.7

## Purpose

This blueprint governs how ChatGPT coordinates GitHub-backed domain agents without confusing repository configuration with actual execution.

The orchestration layer is a **control plane**, not a replacement for domain runtimes. It decides which owner should execute, whether that owner is actually executable in the current session, what assurance is required, and what evidence must exist before the result can be trusted.

Universal Continuity remains responsible for task discovery/recovery/leases. Domain owners remain responsible for business state. This execution harness sits between routing and owner execution.

## Two control planes

### Continuity plane

`intent -> task discovery -> exact owner -> checkpoint -> compatibility -> writer lease -> progress receipt`

### Execution plane

`next_action -> owner capability manifest -> current-session handshake -> route decision -> owner executor/gateway -> execution receipt -> gate -> owner checkpoint`

The execution plane never invents business truth and never replaces the owner state machine.

## Core problem this solves

A GitHub repository may contain:

- Skills;
- role prompts;
- agent registries;
- workflow JSON;
- quality rubrics;
- policies;
- tests;
- code stubs.

None of those, by themselves, prove that a specialist actually ran.

Therefore every GitHub-backed agent is evaluated on four separate questions:

1. **Declared** — is the capability described?
2. **Wired** — is it connected to a real stage/invocation path that fails closed when missing?
3. **Executable now** — does the current ChatGPT/runtime window have the needed tools, credentials and modality access?
4. **Attested** — when independence matters, is there a distinct execution identity/context/trace proving the work did not collapse into one self-approving context?

## Assurance ladder

- `DECLARED_ONLY` — documentation/configuration only. Not execution.
- `HARNESS_WIRED` — owner code has a real invocation path and fail-closed binding.
- `SESSION_EXECUTABLE` — this execution window can run it now.
- `ATTESTED_ISOLATED` — distinct isolated execution with inspectable identity/evidence.

The dispatcher uses the minimum assurance required by the business gate. It must not silently lower the requirement.

## Current no-deployment operating model

The user does not currently need to deploy every agent to gain value from GitHub orchestration.

When safe, the current ChatGPT session may act as a **CHAT_BRIDGED executor substrate** for capabilities that:

- do not require true isolation;
- can be executed with tools available in the current session;
- can bind their work to the owner task/stage/artifacts;
- can leave an auditable receipt/reference;
- are allowed by the owner's capability manifest.

CHAT_BRIDGED is not equivalent to `ATTESTED_ISOLATED`. It cannot satisfy a gate that requires independent provider runs/contexts/traces.

This distinction lets the system execute aggressively where it can, while failing closed only at the real boundary instead of pretending the entire GitHub agent is unusable.

## Owner contract

Every GitHub-backed domain agent should expose:

`continuity/EXECUTION_CAPABILITIES.json`

The file is owner authority for execution wiring metadata, not business state. It should declare:

- capability/stage identity;
- invocation path;
- executor type/ref;
- assurance ceiling supported by owner code;
- required tools/modalities;
- receipt/evidence contract;
- whether conversational side-channel execution is allowed;
- safe degraded paths, if any;
- known owner-level blockers.

The universal registry is a cache/pointer only.

## Dispatcher algorithm

For every material next action:

1. Continuity/domain routing resolves the exact task and owner.
2. Read the owner capability manifest.
3. Identify only the capabilities required by the next action.
4. Run a current-session capability handshake.
5. Reject any capability that exists only as prompt/config documentation.
6. Compute effective assurance as the lower of the owner code ceiling and observed session assurance.
7. Select one of:
   - `OWNER_NATIVE`
   - `CHAT_BRIDGED`
   - `DETERMINISTIC_TOOL`
   - `ISOLATED_EXTERNAL`
   - safe `DEGRADED`
   - `BLOCKED`
8. Dispatch through the owner path/gateway.
9. Require the configured receipt/evidence before the gate is considered complete.
10. Persist business progress through the owner writer/version guard and re-read authority before reporting `COMMITTED`.

## Side-channel rule

A quality-critical tool may be callable from ChatGPT and still be illegal for a particular owner stage.

If an owner declares `side_channel_allowed=false`, the dispatcher must not do:

`chat -> tool`

It must do:

`chat -> owner work order/gateway -> guard -> tool -> artifact/receipt -> gate`

This is especially important for image/video generation, publishing, trading-data freeze, destructive mutations, and other operations where bypassing owner state invalidates review evidence.

## Agent-count rule

More roles are not automatically better.

Before creating a permanent new agent, classify the missing function as one of:

- existing role responsibility;
- deterministic gate;
- stage capability;
- on-demand specialist sidecar;
- permanent operational agent.

A permanent operational agent must have both:

1. an invocation path (scheduled stage or event trigger), and
2. an executor/evidence contract.

If either is absent, the role remains `DECLARED_ONLY` and should not be advertised as executed capability.

## Learning/evolution

Learning and system evolution are cross-cutting capabilities, not mandatory participants in every production stage.

Default loop:

`CAPABILITY GAP -> DIAGNOSE -> SCOUT -> COMPARE -> PROTOTYPE -> RED TEAM -> QA -> ACCEPT/REJECT -> EVOLUTION PATCH -> TEST -> DELETE SUPERSEDED MECHANISM`

Use this loop when there is a real gap, repeated failure, benchmark miss, tool/provider change or newly available capability. Do not tax every ordinary business turn with research/meta-agents.

## CI expectations

Each GitHub agent should eventually test at least:

- every operational role/capability has a valid invocation path;
- no configured stage references an unknown executor;
- hard gates fail closed when required executor capability is unavailable;
- direct side-channel paths cannot promote artifacts when forbidden;
- evidence/receipt binding is enforced;
- version drift between agent registry, execution plan and runtime package is detected;
- declared-only roles are not counted as completed execution.

## Current cross-agent principle

The orchestration layer optimizes for **maximum executable work under current capabilities**, not maximum formal process.

It should:

- run owner-native code where available;
- use current ChatGPT tools as a bridge where assurance permits;
- prefer deterministic checks over persona simulation;
- reserve true isolated execution for gates that actually need it;
- block only the missing hard capability;
- expose the exact blocker and continue all independent work that remains valid.
