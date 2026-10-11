# 01 — `find-skills`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

> Supersedes the premature selection framing in `research/SKILL_DISTILLATION_01_FIND_SKILLS_2026-10-11.md`. That older artifact remains historical evidence; this entry is the neutral library record.

## A. Identity and evidence provenance

- Source: `vercel-labs/skills`
- Pinned repository HEAD: `13e4063a1cf913f5606d57d42ab83a86f5001e04`
- Skill: `skills/find-skills/SKILL.md`
- Skill blob: `a41bdd074bb587afd861332cf2f473f3154de4d7`
- Executable implementation: `src/find.ts`
- Implementation blob: `9fe60ce81be21a65508299b469519af4b67155b2`
- Regression: `src/find.test.ts`
- Test blob: `c11d9ec081cfa1724ea2d025e3004ab71c78a451`
- Broader CLI architecture inspected through repository README.
- Leaderboard popularity is discovery context only, not quality proof.

## B. Problem model and intended outcome

The Skill treats **capability discovery** as a first-class agent task. The user often knows the outcome they want but does not know that a reusable Skill already exists.

Its desired outcome is not “answer the question” but:

1. recognize that the need may map to an installable capability;
2. locate plausible candidates;
3. apply a lightweight trust/quality screen;
4. present an executable acquisition path;
5. install/use the selected capability when desired;
6. fall back safely when no suitable Skill exists.

Architectural role: **discovery/router + acquisition funnel**, not the capability executor itself.

It intentionally does not define how each discovered Skill works or prove that popular Skills are correct.

## C. Activation and invocation model

### Explicit triggers

- “find a skill for X”
- “is there a skill that can…”
- user asks to extend capabilities
- user asks for a reusable tool/template/workflow.

### Latent triggers

The original Skill also treats “how do I do X?” and “can you do X?” as possible discovery opportunities when X is specialized/common enough that a Skill may exist.

### Invocation style

`find-skills` is instructions for the agent; the executable search is delegated to the `npx skills find` CLI/API.

### Exit conditions

- candidate found and surfaced/installed;
- no candidate found, then fall back to general assistance or Skill creation.

### Wrong-trigger risk

If invoked for every ordinary request, discovery becomes latency/context theater. The source does not mechanically enforce a materiality threshold.

## D. Inputs, outputs, side effects

### Inputs

- natural-language need;
- inferred domain + specific task;
- optional GitHub owner scope;
- skills.sh search API results.

### Outputs

- ranked Skill candidates;
- source owner/repo;
- install count;
- install command;
- skills.sh reference.

### Mutations

Search itself is read-only. Installation (`npx skills add`) mutates the target agent/project/global Skill directories. The wider CLI supports project/global installation, symlink/copy modes, update and remove.

### Lower-persistence lane

The repository also supports `skills use`, which generates/uses Skill instructions without permanently installing them. This creates an important reversible-trial path even though the `find-skills` prose emphasizes installation more heavily.

## E. End-to-end workflow

### F0 — Need recognition

Entry: user expresses a specialized task/capability gap.

Actions:
- infer domain;
- infer concrete task;
- decide whether Skill discovery is plausible.

Exit: search-worthy capability hypothesis or direct-answer fallback.

### F1 — Curated discovery

The Skill instructs the agent to inspect the skills.sh leaderboard first for well-known domain matches.

Purpose: use popularity/reputation as a fast prior, not a full global search.

Exit: candidate(s) or move to targeted search.

### F2 — Targeted search

Command form:

`npx skills find <query> [--owner <owner>]`

Implementation details:
- owner is normalized to lower case;
- GitHub owner syntax is validated;
- API query includes owner scope when supplied;
- result limit is 20;
- result metadata is sanitized;
- results are sorted by install count.

### F3 — Candidate inspection

Original prose asks the agent to consider:
- installs;
- source reputation;
- repository stars.

These are heuristics, not verification of behavior.

### F4 — Presentation

Surface candidate name, purpose, source/popularity context, install command, and discovery URL.

### F5 — Acquisition

Interactive mode can hand the selected result directly into `runAdd`.

Non-interactive/agent mode prints candidates and leaves acquisition as a separate explicit step.

### F6 — No-result fallback

If API/search returns no results:
- report no suitable Skill;
- continue using general capability if possible;
- optionally suggest creating a custom Skill for recurring needs.

The implementation catches search/API errors and returns an empty set rather than inventing a result.

## F. Core methodology / mental model

The underlying methodology is a **widening capability-acquisition funnel**:

`NEED → DECOMPOSE → CURATED DISCOVERY → TARGETED SEARCH → VERIFY → ACQUIRE/TRIAL → FALLBACK/CREATE`

Important ideas:

- **reuse before building**;
- decompose vague capability demand into domain + task;
- rank discovery candidates to control search cost;
- use narrower trusted/owner scope where possible;
- treat “no result” as legitimate;
- keep search separate from execution.

The source conflates lightweight popularity screening with “verify quality”; that distinction must remain visible in the library.

## G. Decision-rights model

- User: owns whether they want the capability installed/used.
- Agent: classifies need, forms search terms, screens and presents candidates.
- Search API: supplies candidate metadata.
- CLI runtime: performs installation/use/update/remove.
- Ecosystem/repository: owns actual Skill behavior.

Potential rights leak: an agent could treat ranking/popularity as enough to choose for the user and install globally. The source encourages offering installation, but does not establish a strict permission model for persistence scope.

## H. State machine and lifecycle

No durable state machine inside the Skill itself.

The wider CLI has lifecycle operations:

`DISCOVER → INSTALL/USE → LIST → UPDATE → REMOVE`

Installation scope is either project or global. Symlink mode creates a canonical copy shared to agent-specific directories; copy mode creates independent copies and therefore greater drift risk.

## I. Memory, durability, provenance

Search is stateless.

Durability appears when a Skill is installed:
- project installation becomes repository/project state;
- global installation becomes user-level state;
- symlink mode reduces duplicate copies;
- copy mode can diverge.

Provenance retained in the user-facing package/source string, but the `find-skills` Skill itself does not define lockfile-level provenance guarantees in the inspected files.

## J. Composition and dependency graph

`find-skills` depends on:
- Skills CLI;
- skills.sh search API;
- downstream source repositories.

It is a router into **other Skills** rather than a shared primitive those Skills invoke.

Dependency risk: discovery infrastructure availability affects search, but search failure degrades to no-result rather than fabricated behavior.

## K. Skill / Agent / Runtime / Harness architecture

- `SKILL.md`: need recognition, discovery/recommendation workflow.
- `src/find.ts`: actual API query, TTY/non-TTY interaction, install handoff.
- `src/find.test.ts`: option parsing, API query, non-interactive output regression.
- Skills CLI runtime: installation/source resolution/update/removal.

This is a useful separation: prose defines **when/why**, runtime defines **how**.

Weakness: quality verification remains mostly prose/heuristic rather than an executable verification Harness.

## L. Context engineering and progressive disclosure

The Skill does not preload all ecosystem Skills. It discovers by query and only installs/loads selected candidates.

This is inherently progressive disclosure at ecosystem scale.

Non-interactive agent mode avoids fzf-style UI and prints deterministic textual results, which is better for automation/context capture.

## M. Concurrency, isolation, idempotency, replay

The inspected `find` implementation has no sophisticated concurrency/lease model.

Search is safe/read-only. Installation can be repeated, but idempotency/update semantics belong to the wider `skills add/update` implementation and were not fully reverse-engineered for this entry.

No claim is made that global installation is transactionally isolated across concurrent agents.

## N. Safety and trust boundaries

Observed safety measures:
- result metadata is sanitized before display;
- owner scope is syntactically validated;
- private/public repository behavior is distinguished elsewhere in CLI;
- repository sources can use existing Git/GitHub credentials.

Missing from this Skill:
- executable permission review of discovered Skill contents;
- supply-chain trust scoring;
- sandboxed trial requirement;
- malicious Skill detection.

The original “official source / stars / installs” screen is a **trust prior**, not a security boundary.

## O. Failure semantics and recovery

- Search API error → empty result, no invented candidate.
- Invalid owner → explicit parse error.
- No result → direct-help/create fallback.
- Non-TTY/agent environment → skip interactive chooser.

Potential failure: a poor query returns irrelevant highly-installed candidates; the Skill has no semantic reranker beyond the model's judgement.

## P. Verification / Harness / Eval model

Observed tests verify:
- owner argument normalization and validation;
- owner forwarded into search API;
- non-interactive mode displays all returned candidates, including result #11.

Not observed:
- held-out quality eval for candidate relevance;
- malicious result/supply-chain tests;
- empirical comparison showing leaderboard-first beats broader search;
- outcome eval showing installed Skill improves the user's task.

## Q. Portability and compatibility

The broader Skills CLI supports many agents and multiple source formats.

The `find` implementation explicitly differentiates TTY versus agent/non-interactive execution, improving harness portability.

External dependency: skills.sh API/search service.

## R. Cost, latency, complexity and ergonomics

Benefits:
- search narrows reusable capability selection;
- owner scope reduces noise;
- leaderboard-first reduces exploratory search cost.

Costs:
- network call;
- model query formulation/screening;
- installation/migration burden if adopted;
- potential architecture bloat if every need causes a new Skill install.

Ergonomic pattern: interactive humans get a selector; agents get deterministic output.

## S. Anti-patterns and negative knowledge

Explicit or inferred negative rules:
- do not recommend solely from search output;
- do not pretend no-result is failure requiring a weak recommendation;
- do not make agent execution depend on interactive TTY selection.

Library caution:
- fixed popularity thresholds should not be mistaken for universal quality gates;
- global install should not be the only acquisition mode when reversible trial exists.

## T. Hidden assumptions and inferred invariants

1. The skills.sh index is sufficiently current and representative.
2. Skill name/description metadata is enough to shortlist by semantic fit.
3. Install count is useful as at least a weak prior.
4. The user trusts the CLI/source resolution path.
5. Installing a Skill changes capability more cheaply than custom engineering.
6. The agent can reason about source reputation without a deterministic trust engine.

## U. Reusable primitives — neutral extraction

### U1 — Latent capability-gap detector

Invariant: specialized/repeated needs may indicate an existing reusable capability.

Limitation: can over-trigger and increase latency.

### U2 — Widening discovery funnel

Minimal form: curated → scoped → broad.

Limitation: curated popularity can bias against new/niche solutions.

### U3 — Reuse-before-build gate

Invariant: inspect existing capability before creating permanent architecture.

Limitation: reuse still needs compatibility/security verification.

### U4 — Non-interactive agent discovery path

Invariant: automation must not depend on interactive selection UI.

### U5 — Reversible capability trial

Observed in the wider CLI through `skills use`: try without permanent install.

## V. Cross-Top10 links

Potential complementarity to revisit after 10/10:
- `setup-matt-pocock-skills`: acquisition versus per-repo setup/configuration;
- `agent-browser`: thin Skill points into a richer runtime-delivered capability set;
- `handoff`: suggested Skills can act as capability-routing hints for a future session.

Potential tension:
- `frontend-design`, `tdd`, etc. may be better treated as direct installed methods versus dynamically discovered dependencies.

No resolution yet.

## W. Open questions for final synthesis

- Should capability search be a cold-path architecture function, a normal agent behavior, or both?
- What evidence should be required before installing third-party capability?
- Should reversible trial be mandatory before persistent/global adoption?
- Can a unified capability registry cover built-in tools, Plugins, Skills, MCP servers and owner-local runtimes without bloating the hot path?

## X. Evidence ceiling

- Original Skill inspected: **YES**
- Runtime implementation inspected: **YES**
- Unit regression inspected: **YES**
- Broader CLI architecture inspected: **YES, partial**
- Dedicated relevance/security eval observed: **NO**
- Live outcome improvement proven: **NO**
- Independent quality verification: **NO**

Current conclusion is descriptive only: `find-skills` is a discovery/acquisition architecture with real executable support, but its quality/trust screening is substantially more heuristic than its search/runtime mechanics.
