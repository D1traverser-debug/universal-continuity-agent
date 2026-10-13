# 12 — Chaos Engineering and Controlled Fault Injection

## Core method

Chaos Engineering is disciplined experimentation about resilience, not random destruction. The Principles of Chaos Engineering frame experiments around:

1. a measurable steady-state hypothesis;
2. a control and experiment condition;
3. realistic failure variables;
4. an attempt to disprove that the system remains within acceptable steady state;
5. minimizing blast radius while increasing confidence.

## Universal already has a related mechanism

`runtime/system_audit.py` contains deterministic synthetic fault-injection scenarios such as stale registry override, incomplete discovery, stale-writer commit claims, missing executor evidence and repeated failure-class repair. This is a strong foundation and already avoids production-side destructive chaos.

## Main gap: fault injection is scenario-based, not hypothesis/coverage based

Current synthetic faults answer:

> “Does this known bad condition get rejected?”

Chaos-style reasoning adds:

> “What measurable service property should remain acceptable while a dependency degrades, and what failure variables have we never exercised?”

Candidate steady-state metrics for Universal could include:

- authoritative state remains uncorrupted;
- healthy owners remain usable when another owner fails;
- continuation either resumes correctly or fails closed within bounded work;
- no duplicate external side effect occurs after ambiguous transport;
- bootstrap overhead remains bounded under one unavailable dependency;
- control-plane evidence never silently upgrades assurance class;
- recovery converges or exposes a stable blocker rather than oscillating.

## Failure variables worth modeling later

- GitHub read succeeds but write result times out;
- writer loses lease between preparation and publish;
- external state changes between observation and decision;
- owner repository becomes temporarily unreadable;
- CI result is delayed, duplicated or stale;
- signal arrives after condition is already resolved;
- two independent-looking reviewers share a corrupted evidence source;
- cache survives after authority changes;
- one owner enters repeated recovery while others stay healthy;
- context/token/tool limits interrupt a long maintenance run;
- tool returns syntactically valid but semantically stale data.

## Blast-radius policy

For this system, production chaos must be conservative:

- never inject destructive mutations into user BUSINESS truth merely to test resilience;
- never intentionally corrupt authoritative `main` or checkpoints;
- prefer model checking, synthetic fixtures, sandbox branches/environments and deterministic fault injection;
- if a live experiment is ever justified, declare affected resource, steady state, abort condition, rollback path and user-impact boundary first.

This is stricter than some service-chaos practice because the control plane operates directly on durable user artifacts and repositories.

## Relationship to SRE and FDIR

Chaos experiments discover whether recovery assumptions hold. SRE supplies the steady-state/SLO metrics; FDIR supplies detection/isolation/recovery structure; formal models explore algorithmic interleavings; deterministic tests prevent regressions. These evidence types should complement rather than substitute for one another.

## Current assessment

- Synthetic fault injection: **PRESENT / GOOD**.
- Steady-state hypothesis model: **CURRENT GAP**.
- Fault-space/coverage inventory: **CURRENT GAP**.
- Explicit blast-radius/environment policy for resilience experiments: **PARTIAL / implicit safety rules**.
- Production chaos against authoritative business state: **NOT RECOMMENDED by default**.
