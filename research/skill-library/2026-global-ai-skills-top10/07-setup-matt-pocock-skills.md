# 07 — `setup-matt-pocock-skills`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Skill: `skills/engineering/setup-matt-pocock-skills/SKILL.md`
- Skill blob: `293c25b75590119794af03b037ba4288054a32b3`
- Domain consumer template: `skills/engineering/setup-matt-pocock-skills/domain.md`
- GitHub tracker template: `skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md`
- Related triage/ticket/spec/wayfinder consumers inspected.

## B. Problem model and intended outcome

Problem: a collection of reusable Skills cannot behave consistently if every repository uses different issue trackers, label vocabulary, steering files and domain-document layouts, or if each Skill rediscovers those conventions independently.

Desired outcome:
- perform a one-time environment inspection;
- make a small set of repository-local configuration decisions;
- persist those decisions in stable docs;
- let all downstream engineering Skills consume the same conventions without re-asking.

Architectural role: **run-once repository bootstrap/configuration Skill**.

It does not perform the downstream triage/spec/TDD work. It establishes the local contract they rely on.

## C. Activation and invocation model

- Manual only (`disable-model-invocation: true`).
- Intended before first use of the engineering Skill suite, or when switching/restarting repository conventions.
- Re-running is not normal steady-state behavior.

Preconditions:
- repository/workspace access;
- user available for choices that exploration cannot settle.

## D. Inputs, outputs, side effects

Inputs:
- git remotes/config;
- existing `CLAUDE.md` / `AGENTS.md`;
- current glossary/map/ADRs;
- existing `docs/agents/`;
- `.scratch/` convention;
- installed Skill set, especially `triage`;
- monorepo signals;
- user preferences where branching choices remain.

Outputs:
- `docs/agents/issue-tracker.md`;
- optional `docs/agents/triage-labels.md`;
- `docs/agents/domain.md`;
- compact `## Agent skills` pointer block in existing steering file;
- tracker labels where applicable.

Mutations are repository configuration/documentation, not business/domain implementation.

## E. End-to-end workflow

### S0 — Explore existing environment

Read first; do not assume.

Inspect:
- remote provider;
- existing steering file;
- existing setup block;
- domain docs;
- prior setup output;
- local issue-tracker signals;
- whether dependent Skill is installed;
- monorepo evidence.

### S1 — Present findings

Summarize present/missing configuration before proposing changes.

### S2 — Resolve Issue Tracker

Recommended default is inferred from repo remote:
- GitHub remote → GitHub;
- GitLab remote → GitLab;
- otherwise local markdown or user-described external tracker.

Record choice durably.

### S3 — Resolve triage vocabulary conditionally

Only ask/configure triage labels if `triage` is installed.

Default canonical roles are recommended. Existing repo labels can map to canonical meanings instead of creating duplicates.

This is **capability-conditional setup**.

### S4 — Resolve domain-doc layout

Default to single-context silently for ordinary repos.

Only surface multi-context choice when exploration found meaningful monorepo evidence.

This is **evidence-triggered complexity admission** rather than asking every user every option.

### S5 — Preview

Show exact intended steering block and docs before writing. Let user edit.

### S6 — Select steering authority carefully

- existing `CLAUDE.md` wins if present;
- else existing `AGENTS.md`;
- if neither exists, ask user which to create;
- never create parallel steering file when one already exists.

Update existing block in place; do not append duplicates.

### S7 — Write configuration

Write compact pointer block plus detailed `docs/agents/*` files.

Create labels only for configured tracker and only if missing.

### S8 — Finish

Explain which downstream Skills now consume configuration. Tell user they can edit the durable docs directly; setup does not need to be rerun for ordinary changes.

## F. Core methodology / mental model

### Inspect-before-configure

Existing repo structure is evidence and must be preserved when possible.

### Recommended defaults with branch suppression

Do not ask questions whose answer exploration already determines. Ask only genuine choices.

### One canonical local convention, many consumers

Downstream Skills read common repository-local docs rather than embedding tracker/domain assumptions individually.

### Progressive complexity

Single-context is default; multi-context admitted only with evidence.

### Conditional configuration

Do not configure an uninstalled capability.

### Preview-before-write

Configuration is reviewed before mutation.

## G. Decision-rights model

Agent:
- inspects repository;
- infers sensible defaults;
- suppresses irrelevant choices;
- drafts configuration.

User:
- selects real branching decisions (unknown tracker, steering-file creation, non-default layout/label mapping);
- edits draft before write.

Repository existing structure:
- constrains which steering file is authoritative;
- provides evidence for defaults.

## H. State machine and lifecycle

`UNCONFIGURED/UNKNOWN → EXPLORED → FINDINGS_PRESENTED → TRACKER_RESOLVED → OPTIONAL_TRIAGE_RESOLVED → DOMAIN_LAYOUT_RESOLVED → DRAFT_CONFIRMED → WRITTEN → CONFIGURED`

Lifecycle characteristic: **run once, then configuration itself becomes authority**.

Re-entry is mainly for deliberate convention changes.

## I. Memory, durability, provenance

Durable state is repository-local prose/configuration:
- steering pointer;
- tracker conventions;
- domain-doc conventions;
- label mapping.

This turns implicit conversation knowledge into project-owned configuration.

Important structure:
- hot steering block is small;
- detailed commands/policies live in `docs/agents/*`.

The source uses this to prevent every Skill from carrying tracker-specific logic in its main prompt.

## J. Composition and dependency graph

Setup config is consumed by:
- `triage`;
- `to-spec`;
- `to-tickets`;
- `wayfinder`;
- domain-aware exploration Skills.

The GitHub tracker template includes semantics for issue creation, sub-issues, dependency edges, map/frontier/claim operations.

`triage` installation itself changes what setup asks/writes.

## K. Skill / Agent / Runtime / Harness architecture

- setup Skill: interactive configuration workflow;
- templates: durable configuration schema by example/prose;
- steering file: compact project-level pointer;
- downstream Skills: consumers;
- GitHub/GitLab CLI: execution layer for labels/issues.

Source explicitly states this is **prompt-driven, not deterministic script**.

That means exploration/branch decisions depend on model interpretation even though outputs are structured.

## L. Context engineering and progressive disclosure

Strong pattern:
- small steering block contains summaries + links;
- detailed tracker/domain instructions live in separate docs;
- absent optional features do not load/configure irrelevant detail;
- multi-context guidance only activated when needed.

This is repository-level progressive disclosure.

## M. Concurrency, isolation, idempotency, replay

Idempotency patterns:
- detect existing `## Agent skills` block and update in place;
- do not create duplicate CLAUDE/AGENTS files;
- create only missing labels;
- detect prior `docs/agents/` output.

No explicit CAS/locking for concurrent writers. Two setup runs could still race.

## N. Safety and trust boundaries

Risk is bounded to repo configuration and issue-tracker labels.

Safety behaviors:
- preview changes before writing;
- preserve surrounding user edits;
- do not create alternative steering authority unnecessarily;
- existing labels can be reused/mapped rather than duplicated.

No secret-handling model is central.

## O. Failure semantics and recovery

- Missing domain docs → proceed silently; lazy creation later.
- Triage not installed → skip triage-label section entirely.
- No steering file → ask rather than guess.
- Existing block → update, not duplicate.
- Unknown tracker → user describes workflow; write freeform durable config.

Potential failure: model mis-detects monorepo/context and chooses wrong default. No deterministic validation Harness observed.

## P. Verification / Harness / Eval model

No dedicated eval observed for setup decisions.

The workflow itself contains verification steps:
- exploration inventory;
- findings presentation;
- user preview/confirmation;
- existing-state checks before mutation.

Downstream failures may indirectly reveal setup misconfiguration.

## Q. Portability and compatibility

Supports:
- GitHub;
- GitLab;
- local markdown;
- arbitrary tracker via prose.

Uses provider CLIs when known.

Steering file supports Claude/Codex-style conventions through existing `CLAUDE.md`/`AGENTS.md`, but file-selection policy is opinionated.

## R. Cost, latency, complexity and ergonomics

One-time human cost is traded for lower repeated downstream setup/questions.

Efficiency patterns:
- recommend defaults;
- skip settled/irrelevant questions;
- configure only installed capabilities;
- edit one existing steering file;
- avoid creating unused domain artifacts.

Ongoing maintenance is direct editing of config files, not rerunning the Skill.

## S. Anti-patterns and negative knowledge

- Do not assume repository state before inspecting.
- Do not create both `CLAUDE.md` and `AGENTS.md`.
- Do not append duplicate Agent-skills block.
- Do not ask for triage config when triage isn't installed.
- Do not default every repo to multi-context architecture.
- Do not create glossary/ADRs with no real content.
- Do not force a specific tracker when repository/user has another established workflow.

## T. Hidden assumptions and inferred invariants

1. Downstream Skills will consistently read `docs/agents/*`.
2. Prose files are sufficient machine-facing configuration.
3. Repository conventions change infrequently enough for run-once setup.
4. Remote/provider detection is a useful default signal.
5. Existing steering file should remain singular authority.
6. Human preview is enough to catch configuration mistakes.

## U. Reusable primitives — neutral extraction

### U1 — Run-once capability bootstrap

Separate environment adaptation/setup from recurring business workflow.

### U2 — Inspect → recommend default → ask only unresolved choices

Reduces needless questionnaire burden.

### U3 — Conditional setup by installed capability

Do not configure unused subsystems.

### U4 — Evidence-gated complexity

Admit multi-context/advanced structure only when repository signals justify it.

### U5 — Thin hot pointer + detailed local references

Keep steering entry compact while preserving rich owner-local configuration.

### U6 — In-place idempotent steering update

Modify existing canonical block rather than creating parallel authority.

## V. Cross-Top10 links

- `triage`: direct consumer of labels/tracker config.
- `grill-with-docs`: consumer of domain-doc layout.
- `tdd`: reads glossary/ADRs indirectly.
- `find-skills`: capability installation may precede per-repo setup.
- `agent-browser`: contrasting architecture—agent-browser serves current instructions from runtime rather than repository setup docs.
- `handoff`: setup artifacts should be referenced, not duplicated into handoff.

## W. Open questions for final synthesis

- Should repository-local configuration be machine-readable schema rather than prose templates?
- When should setup be auto-migrated after Skill version changes?
- How should concurrent agents safely modify shared configuration?
- Can installed-capability discovery be made deterministic across different agent environments?
- Which setup facts belong globally versus per-owner repository?

## X. Evidence ceiling

- Skill inspected: **YES**
- Main templates inspected: **YES**
- Downstream consumer relationships inspected: **YES**
- Deterministic setup runtime: **NO; source explicitly calls it prompt-driven**
- Automated eval of correct configuration choices: **NOT OBSERVED**
- Live setup outcome benchmark: **NOT OBSERVED**

The Skill is a strong example of one-time configuration and progressive disclosure, but its correctness remains heavily dependent on model inspection and human preview rather than schema/runtime enforcement.
