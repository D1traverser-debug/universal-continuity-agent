# Learning Pass — Progress Observability and Durable Continuation

Date: 2026-10-10
Scope: Universal Continuity
Disposition: PARTIAL ADOPTION; no blanket framework dependency

## Problem observed

A real cross-chat recovery exposed two separate gaps:

1. owner handoffs vary in conformance quality;
2. the user cannot easily see the exact pre-inheritance persisted progress or whether each later turn actually changed and persisted the durable resume point.

A runtime drift was also found: the public contract had advanced beyond the executable harness schema, and the harness's normal lease helper did not support explicit SYSTEM_INFRA maintenance takeover even though the contract permits explicitly named infrastructure recovery.

## Evidence reviewed

### OpenAI — Agents API sessions / observability / tracing

Current first-party docs model a durable session as a sequence of turns and provide event/history/turn status surfaces for following progress. A completed turn must still be inspected; session idleness alone does not prove success. This supports making user-visible progress/commit state explicit rather than implicit.

Refs:
- https://developers.openai.com/api/docs/guides/agents-api/sessions
- https://developers.openai.com/api/docs/guides/agents-api/observability
- https://developers.openai.com/api/docs/guides/agents-api/tracing

### OpenAI — Agents SDK RunState / sessions

RunState is a serializable resume boundary for interrupted work and warns against concurrent independent resumes against the same session history. This reinforces single-writer takeover and re-read verification.

Refs:
- https://openai.github.io/openai-agents-python/ref/run_state/
- https://openai.github.io/openai-agents-python/sessions/

### OpenAI — Agent Skills

Skills are reusable, versionable procedure bundles and are loaded when needed rather than being baked into every system prompt. This supports a thin Continuity Skill/map and keeping research/procedures out of startup context.

Ref:
- https://developers.openai.com/api/docs/guides/tools-skills

### OpenAI — Harness engineering

The published harness-engineering case recommends repository knowledge as the system of record and a small map pointing to deeper docs rather than one giant instruction file. This directly supports the v3.6/v3.7 short-handoff direction.

Ref:
- https://openai.com/index/harness-engineering/

### Anthropic — context engineering and long-running harnesses

The original engineering articles emphasize curated context, compaction/structured notes, incremental progress, clear artifacts and clean handoffs across sessions. These are consistent with progressive recovery and turn-level durable checkpoints.

Refs:
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

### LangGraph — persistence

LangGraph distinguishes thread-scoped checkpoints from longer-term stores. This reinforces the existing Continuity distinction between current execution state and durable cross-task learning/preferences rather than merging both into one checkpoint.

Ref:
- https://langchain-ai.github.io/langgraph/concepts/durable_execution/

### Temporal — durable execution

Temporal's durable-execution model preserves workflow state/progress across failures. The transferable principle is exact continuation without replaying completed work; Temporal itself is not adopted as a dependency.

Refs:
- https://docs.temporal.io/temporal
- https://docs.temporal.io/ai

### Video lane — OpenAI DevDay / Cursor context engineering

Official media identity resolved: `Context Engineering & Coding Agents with Cursor`, OpenAI DevDay 2025. Official OpenAI pages confirm the session topic. A third-party transcript surface was available and used only as lower-authority spoken-content evidence; it was not treated as a first-party full transcript or full visual review.

Observed/corroborated themes useful to Continuity:
- intentional/minimal high-quality context;
- self-gathering context through tools;
- specialized agents for distinct losses;
- agents must run/test/verify their own work;
- long-running agents should show what they tried rather than forcing humans to start from scratch.

Refs:
- https://www.youtube.com/watch?v=3KAI__5dUn0
- https://openai.com/devday/2025/
- https://www.textpurr.com/transcript/context-engineering-coding-agents-with-cursor

Evidence label: `ORIGINAL_VIDEO_METADATA_CONFIRMED`; `THIRD_PARTY_TRANSCRIPT_PARTIAL_REVIEW`; `VISUAL_NOT_REVIEWED_IN_THIS_PASS`.

## Accepted changes

1. Add `Resume Progress Receipt` captured from authoritative persisted state before takeover mutation.
2. Add `Turn Commit Receipt` to every final response while a durable task is active.
3. Distinguish `COMMITTED`, `NO_MATERIAL_CHANGE`, `COMMIT_FAILED`, `STALE_WRITER`, and `NOT_APPLICABLE`.
4. `COMMITTED` requires authoritative re-read verification; a successful write call alone is not enough.
5. Do not create heartbeat writes when no material state changed.
6. Add a narrow Continuity Skill/map instead of expanding startup instructions.
7. Add evidence-gated proactive learning as a maintenance behavior, not a steady-state business hot-path tax.
8. Repair executable harness/version drift and support explicitly named SYSTEM_INFRA lease takeover while keeping such tasks excluded from bare USER discovery.

## Reinforced but not new

- progressive context loading;
- handoff as current execution truth;
- repository/artifact references over duplication;
- single active writer;
- execution state separated from durable learning;
- exact owner authority beats caches.

## Explicit non-adoptions

- no dependency on LangGraph, Temporal, Cursor or Anthropic runtime;
- no requirement to use multi-agent execution for every recovery;
- no fixed token threshold;
- no assumption that a video transcript equals full visual review;
- no write-on-every-message heartbeat that would create meaningless version churn;
- no migration of domain business logic into Universal Continuity.
