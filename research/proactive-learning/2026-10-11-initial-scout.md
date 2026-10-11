# Proactive Learning Scout — 2026-10-11

Status: LEARNING_EVIDENCE_NOT_PRODUCTION_AUTHORITY
Scope: Universal Continuity + owner-local candidate discovery

## Why this scout exists

A user correction exposed a declaration-to-operation gap: `CONTINUOUS_LEARNING_POLICY.md` required proactive learning, but no live recurring scout was enforcing ecosystem discovery. This artifact is the first evidence pass after operationalizing that loop. It is research evidence, not production authority.

## Discovery lanes exercised

- current Agent Skill/source repositories;
- popular/trending Skill discovery surfaces;
- ChatGPT plugin/tool capability discovery;
- niche/self-improvement and code-understanding candidates;
- source/runtime/test evidence beyond README-level claims.

Popularity was used only to discover candidates, not to rank adoption.

## Candidate 1 — Anthropic `skill-creator`

Classification: `UNIVERSAL_CANDIDATE`  
Deep-dive status: SOURCE/RUNTIME EVIDENCE INSPECTED; production adoption NOT YET PROMOTED

Pinned source:
- repo: `anthropics/skills`
- observed main revision: `dbd4588f9e1033efb41dad4bef2f7947c8993d44`
- Skill: `skills/skill-creator/SKILL.md`
- scripts inspected: `scripts/run_loop.py`; directory also exposes `run_eval.py`, `aggregate_benchmark.py`, `generate_report.py`, `improve_description.py`, `quick_validate.py`, `package_skill.py`.

Observed mechanisms worth distilling:

1. **Skill vs baseline evaluation** — new skills are tested against no-skill baselines; modified skills can be tested against a snapshot of the old version.
2. **Trigger-quality evaluation** — eval sets distinguish `should_trigger` / `should_not_trigger` and compute precision, recall and accuracy rather than assuming a description is good because it reads well.
3. **Repeated runs** — trigger decisions can be evaluated multiple times per query instead of trusting one stochastic sample.
4. **Train/test holdout** — `run_loop.py` stratifies trigger/non-trigger examples into train and held-out test sets and hides test results from the improvement step, explicitly reducing overfit risk.
5. **Iterative improvement with bounded iterations** — description optimization loops until pass or max iterations, records history and selects the best held-out result.
6. **Quantitative + qualitative evidence** — pass rates, time/token cost and qualitative output review are kept separate rather than collapsed into one score.
7. **Progressive disclosure** — Skill metadata, body and bundled resources have different loading roles; executable scripts can carry deterministic work without bloating the prompt.

Adoptable Universal primitive:
- build/extend owner Skill/router evaluation around **trigger false-positive/false-negative cases + baseline comparison + held-out evaluation + cost/context measurement**;
- use it to test whether a thin Skill/router actually activates correctly and improves the target task, not merely whether its file size is small.

Rejected direct-copy elements:
- Claude-specific subagent/runtime commands are implementation details, not Universal architecture;
- user-review ceremony is useful for subjective skill creation but must not become a hard gate for autonomous system maintenance;
- the entire 500-line Skill should not be copied into Universal bootstrap or owner Skills.

Required next evidence before production promotion:
- map these evaluation primitives against existing Universal `runtime/context_footprint.py`, owner architecture harness and router-size drift checks;
- implement the smallest reusable eval primitive only if current tests cannot already express trigger precision/recall/holdout behavior;
- run it on at least one current owner Skill plus a held-out case before claiming production benefit.

## Candidate 2 — `self-improving-agent` family

Classification: `REJECT_DUPLICATE` for direct architecture adoption; `MONITOR` for event-taxonomy ideas

Observed source behavior:
- activates on command/tool failures, user corrections, missing capabilities, stale knowledge and better recurring approaches;
- stores `LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md` and promotes selected entries into workspace instruction/memory files;
- current `pskoett/self-improving-agent` explicitly describes its current version as OpenClaw-only, with OpenClaw bootstrap/reset hooks.

Comparison with Universal:
- event capture overlaps existing maintenance triggers, user-correction assimilation, durable incident evidence, candidate-vs-authority separation and continuous-learning promotion gates;
- markdown workspace memory is a weaker authority model than Universal task/owner authority + provenance + regression-backed promotion;
- blindly importing its promotion path would reintroduce exactly the prompt/instruction bloat and authority ambiguity Universal is designed to avoid.

Distilled useful reminder:
- keep **tool failure / correction / missing capability / stale knowledge / repeated better approach** as explicit scout/maintenance triggers and ensure product-level triggers are actually enabled.

## Candidate 3 — `last30days`

Classification: `OWNER_LOCAL_CANDIDATE`

Observed mechanism:
- recent-public-discussion research over Reddit, Hacker News, GitHub, X, YouTube, Polymarket and topic-specific sources;
- captures engagement context and merges duplicate stories;
- current variants add watchlists/cron-style recurring research and YouTube transcript extraction.

Potential fit:
- useful for Video Growth trend sensing, market/content research and other recency-heavy owner workflows;
- not a Universal bootstrap dependency and not a replacement for authoritative source ordering;
- social engagement is discovery evidence, never correctness evidence.

Next step if an owner needs it:
- owner-local deep dive should inspect the exact implementation/runtime, API dependencies, rate limits, source coverage and evidence provenance before adoption.

## Candidate 4 — `Understand Anything`

Classification: `MONITOR` / `OWNER_LOCAL_CANDIDATE`

Observed mechanism:
- multi-agent codebase analysis builds a knowledge graph of files/functions/classes/dependencies and provides interactive exploration;
- current source advertises multi-platform use including Codex; the core `understand` Skill is large and delegates substantial analysis work.

Potential fit:
- useful cold-path aid for deep architecture audits or unfamiliar large owner repositories;
- poor fit for Continuity hot-path bootstrap because graph construction and multi-agent analysis add material context/tool/latency cost;
- should be evaluated against existing repository search + architecture audit before adding another permanent dependency.

## Plugin/tool discovery snapshot

Current Plugin Directory discovery exposed, among others:
- installed: TinyFish, Opera Browser Connector;
- available candidates: Superpowers, OpenAI Developers, Exa, Tavily, G2 MCP, Vercel, Replit, Firebase and others.

No plugin was installed merely because it exists. Plugin availability is a capability-discovery signal; adoption must be task-relevant and user-approved where installation/connection is required.

## Scout conclusion

The main reusable gap found in this pass is **Skill/router effectiveness evaluation**, not another self-improvement memory layer. Anthropic `skill-creator` supplies concrete evaluation primitives — baseline comparison, repeated trigger trials, held-out testing and cost/quality separation — that are materially stronger than file-size-only Skill quality checks. This is a `UNIVERSAL_CANDIDATE`, not yet production authority.

The system-level fix from this scout is already narrower than importing any candidate: make proactive discovery operational, keep candidate states explicit, deep-read runtime/evals before promotion, bound the queue, and preserve child-owner boundaries through `evolution@1.0`.
