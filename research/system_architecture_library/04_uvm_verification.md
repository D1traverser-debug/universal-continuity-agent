# 04 — UVM as a Verification-Architecture Lens

## What UVM actually is

Universal Verification Methodology (UVM) is a hardware verification methodology/library ecosystem, currently standardized around IEEE 1800.2 with Accellera reference implementations. It is not a general-purpose distributed-agent runtime. Its relevance here is the **separation of verification responsibilities and reusable testbench topology**.

Stable concepts from UVM practice include:

- **sequence/sequencer** — generates ordered stimulus/transactions;
- **driver** — converts abstract transactions into actions against the device/system under test;
- **monitor** — passively observes behavior and converts it back into transactions/events;
- **agent** — encapsulates reusable driver/sequencer/monitor structure; can be active or passive;
- **environment** — composes agents and environment-level monitors/checkers;
- **scoreboard/reference model** — compares observed behavior against expected behavior;
- **coverage** — measures what scenarios/features/states have actually been exercised;
- **phases/configuration/factory/overrides** — support controlled construction, connection, execution and reuse.

One important UVM principle is that monitors should not depend on drivers for the truth they observe. That preserves passive observation and reduces self-confirming test evidence.

## Universal mapping

Current Universal has partial analogues:

- work orders / owner actions ≈ stimulus;
- executor/tool gateway ≈ driver;
- signal plane / live rereads / external observations ≈ monitors;
- deterministic guards ≈ protocol/data checkers;
- expected-action contracts + evidence validation ≈ reference checking;
- CI fault scenarios ≈ directed verification stimulus;
- architecture harnesses ≈ environment-level checking.

The analogy is useful because Universal has repeatedly fought **self-attestation inflation**. UVM's separation of driving and monitoring reinforces the rule that the actor causing the transition should not be the only source claiming the transition occurred.

## Main gap: coverage closure

`runtime/system_audit.py` contains an explicit synthetic fault list, which is valuable. But a UVM-style question remains unanswered:

> What is the coverage model, and what important states/transitions/interactions have never been exercised?

Possible coverage dimensions include:

- task lifecycle states and transition edges;
- lease/takeover/stale-writer combinations;
- owner types and profile applicability combinations;
- state-plane/signal-plane races;
- tool mutation outcome classes;
- environment/substrate variants;
- owner-to-owner interaction modes;
- failure/recovery escalation classes;
- authority/cache conflict classes;
- user-intent vs external live-state combinations.

Without an explicit coverage model, a long list of tests can still leave silent holes.

## Active vs passive verification

Universal currently mixes some active probes with passive observations depending on tool/runtime. A future verification architecture should classify each verifier:

- **active**: injects or drives a test action;
- **passive**: observes without changing the subject;
- **self-attested**: evidence generated inside the action context;
- **independent**: evidence generated through a distinct trusted observation identity.

That classification is more informative than role names such as “reviewer” or “auditor.”

## Scoreboard/reference-model question

Universal has action expectations and contract validators, but not every subsystem has a single explicit reference model describing the expected state transition and outputs. When expectations are duplicated in tests, policies and runtime allowlists, shadow-obligation drift becomes possible.

## What not to transplant

Do not recreate UVM classes/phases in Python or create sequencer/driver/monitor Agents merely for architectural symmetry. UVM's value is verification separation, reusable test components, independent observation and measurable coverage—not its implementation syntax.

## Current assessment

- Deterministic checking: **STRONG**.
- Active/passive evidence distinction: **PARTIAL**.
- Driver/monitor independence: **PARTIAL; explicit in some evidence rules**.
- Reference-model centrality: **PARTIAL**.
- Functional/interaction/transition coverage closure: **CURRENT GAP**.
