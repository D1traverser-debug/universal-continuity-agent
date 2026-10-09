# Universal Continuity — Continuous Learning Policy

Status: ACTIVE
Applies to: Universal Continuity maintenance/evolution

## Purpose

Universal Continuity should proactively learn from relevant agent systems, Skills, harnesses, durable-execution frameworks, official product documentation, engineering write-ups, videos and high-signal community evidence. Learning is not permission to accumulate instructions indefinitely. The goal is to discover missing capabilities, verify them, distill only scope-relevant improvements, and leave mechanical evidence when the system changes.

## Trigger model

Proactive scouting is allowed and expected when any of these are true:

1. the user explicitly asks Continuity to learn/evolve;
2. a real recovery exposes a capability gap, drift or weak owner conformance;
3. OpenAI/agent-runtime authority materially changes;
4. the maintenance task reaches a learning/audit stage;
5. a new owner integration requires a pattern not covered by the current contract.

Do not put broad web/video scouting on the steady-state path of ordinary business turns. Continuity exists to reduce context and latency, not to make every response a research project.

## Source lanes

Prefer evidence in this order for adoption decisions:

1. current first-party OpenAI product/API/Agents/Skills documentation for OpenAI behavior;
2. original engineering documentation/repos from the system being studied (for example Anthropic, LangGraph, Temporal);
3. original conference/video/media evidence;
4. same-author companion material;
5. independent papers and high-signal engineering analysis;
6. community discussion as discovery/experience evidence only.

For video/media evidence, `MEDIA_DISTILLATION_PROTOCOL.md` remains authoritative. Transcript evidence and visual evidence must not be conflated.

## Learning loop

For each candidate improvement:

1. name the observed problem or opportunity;
2. gather the strongest practical evidence available;
3. distinguish invariant, reusable design principle, heuristic and product-specific behavior;
4. test scope fit against Universal Continuity ownership;
5. compare the idea with the current contract instead of assuming novelty;
6. reject duplicated, brittle or out-of-scope guidance;
7. when adopted, encode it in the smallest appropriate contract/policy/Skill/runtime surface;
8. add a regression or acceptance test when the behavior is mechanically testable;
9. record the accepted/rejected disposition in a learning-pass artifact;
10. checkpoint the maintenance task only after authoritative writes are verified.

## What belongs where

- Global invariants: `CONTINUITY_CONTRACT.json` / `PROTOCOL.md`.
- Narrow reusable procedure: a Skill or focused policy file.
- Owner business behavior: owner repository, never duplicated into Universal Continuity.
- Current task progress: short handoff/checkpoint.
- Evidence/research detail: `research/` or `audits/`, referenced from handoff rather than copied into it.

## Anti-bloat rule

A new learning artifact does not justify enlarging startup context. `ENTRYPOINT.md` remains a map. Skills are loaded on demand. Research artifacts are read only when the active next action needs them. If a new rule can be derived from an existing authoritative artifact, reference it instead of copying it.

## Adoption standard

An improvement is accepted only when all are true:

- evidence is strong enough for the claim;
- it solves a concrete Continuity problem or closes a plausible recovery failure mode;
- it does not duplicate domain business logic;
- it has a clear authority location;
- it does not introduce a worse hot-path cost than the problem it solves;
- mechanically testable behavior has a test or acceptance check.

## Current recurring scout topics

Keep these as research lanes, not hard dependencies:

- durable agent session/run state and resumability;
- observable progress/turn receipts and tracing;
- context engineering and compaction;
- Agent Skills and capability discovery;
- single-writer / concurrency / replay safety;
- long-running agent harnesses and incremental progress artifacts;
- multi-agent delegation and independent verification;
- durable execution/checkpoint systems;
- owner adapters and cross-store versioning.
